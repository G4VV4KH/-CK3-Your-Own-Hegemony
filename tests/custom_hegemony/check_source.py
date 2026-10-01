"""Run with Python 3.10+: static checks and evaluation of the real realm trigger.

This deliberately limited interpreter is not a CK3 engine or a syntax validator.
Unknown trigger predicates fail loudly, so a changed implementation cannot pass
the boundary checks merely because the test silently ignores a new condition.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TOKEN = re.compile(r'\s+|\#[^\r\n]*|"(?:\\.|[^"\\])*"|[{}]|>=|<=|!=|\?=|=|>|<|[^\s{}=<>!?#"]+')
OPS = {"=", ">=", "<=", "!=", "?=", ">", "<"}


def tokens(text: str) -> list[str]:
    result, pos = [], 0
    for match in TOKEN.finditer(text):
        if match.start() != pos:
            raise AssertionError(f"Unrecognized script at offset {pos}: {text[pos:pos+40]!r}")
        pos = match.end()
        token = match.group()
        if not token.isspace() and not token.startswith("#"):
            result.append(token)
    assert pos == len(text), f"Unrecognized trailing script at offset {pos}"
    return result


def parse(text: str) -> list[tuple]:
    stream, pos = tokens(text), 0

    def block(nested: bool = False) -> list[tuple]:
        nonlocal pos
        entries = []
        while pos < len(stream) and stream[pos] != "}":
            key = stream[pos]
            assert pos + 2 < len(stream), f"Incomplete assignment after {key}"
            op = stream[pos + 1]
            assert op in OPS, f"Expected operator after {key}, got {op}"
            pos += 2
            if stream[pos] == "{":
                pos += 1
                value = block(True)
            else:
                value = stream[pos]
                pos += 1
            entries.append((key, op, value))
        if nested:
            assert pos < len(stream) and stream[pos] == "}", "Missing closing brace"
            pos += 1
        return entries

    result = block()
    assert pos == len(stream), "Unmatched closing brace"
    return result


def compare(actual, op: str, expected) -> bool:
    if op == "=":
        return actual == expected
    if op == "!=":
        return actual != expected
    if op == ">=":
        return actual >= expected
    if op == "<=":
        return actual <= expected
    if op == ">":
        return actual > expected
    if op == "<":
        return actual < expected
    raise AssertionError(f"Unsupported comparison: {op}")


def evaluate(entries: list[tuple], context: dict, definitions: dict) -> bool:
    def predicate(entry: tuple) -> bool:
        key, op, value = entry
        if key in {"AND", "OR", "NOT", "NOR"}:
            assert op == "=" and isinstance(value, list)
            checks = [predicate(child) for child in value]
            return {"AND": all(checks), "OR": any(checks),
                    "NOT": not all(checks), "NOR": not any(checks)}[key]
        if key == "custom_description":
            assert op == "=" and isinstance(value, list)
            # Formatting changes must not change the eligibility result.
            assert all(child[0] in {"text", "any_held_title"} for child in value), \
                f"Unsupported description predicates: {entry}"
            return evaluate([child for child in value if child[0] != "text"],
                            context, definitions)
        if key == "any_held_title":
            assert isinstance(value, list)
            counts = [child for child in value if child[0] == "count"]
            assert len(counts) <= 1, "Multiple count clauses are unsupported"
            filters = [child for child in value if child[0] != "count"]
            matches = sum(evaluate(filters, title, definitions) for title in context["titles"])
            return compare(matches, counts[0][1], int(counts[0][2])) if counts else matches > 0
        if key in definitions:
            assert op == "=" and value in {"yes", "no"}, f"Unsupported helper call: {entry}"
            return evaluate(definitions[key], context, definitions) == (value == "yes")
        if key == "sub_realm_size":
            return compare(context["size"], op, int(value))
        if key in {"tier", "title_tier"}:
            return compare(context["tier"], op, value.removeprefix("tier_"))
        if key == "is_landless_type_title":
            assert value in {"yes", "no"}, f"Invalid landless predicate: {entry}"
            return compare(context["landless"], op, value == "yes")
        if key == "always":
            assert op == "=" and value in {"yes", "no"}
            return value == "yes"
        raise AssertionError(f"Unsupported trigger predicate: {entry}")

    return all(predicate(entry) for entry in entries)


def evaluate_value(entries: list[tuple], context: dict, definitions: dict) -> float:
    """Evaluate the real live counter, including its real title filter."""
    result = 0
    for key, op, value in entries:
        assert op == "=", f"Unsupported value operator: {op}"
        if key == "value":
            result = float(value)
        elif key == "add":
            result += float(value)
        elif key == "every_held_title":
            filters = [child[2] for child in value if child[0] == "limit"]
            assert len(filters) == 1, "Live counter needs one explicit title filter"
            body = [child for child in value if child[0] != "limit"]
            for title in context["titles"]:
                if evaluate(filters[0], title, definitions):
                    result += evaluate_value(body, title, definitions)
        else:
            raise AssertionError(f"Unsupported value expression: {key}")
    return result


def check_boundaries(mod: Path) -> int:
    definitions = {}
    for path in sorted((mod / "common/scripted_triggers").glob("*.txt")):
        for key, op, value in parse(path.read_text(encoding="utf-8-sig")):
            assert op == "=" and isinstance(value, list), f"Invalid trigger definition: {key}"
            assert key not in definitions, f"Duplicate trigger: {key}"
            definitions[key] = value
    assert "chg_realm_requirement_trigger" in definitions, "Realm requirement trigger not found"
    assert "chg_eligible_empire_trigger" in definitions, "Eligible empire trigger not found"
    values = dict((key, value) for key, _, value in parse(
        (mod / "common/script_values/chg_values.txt").read_text(encoding="utf-8-sig")))
    empire = {"tier": "empire", "landless": False}
    landless = {"tier": "empire", "landless": True}
    kingdom = {"tier": "kingdom", "landless": False}
    cases = [(f"one empire, size {size}", [empire], size, False)
             for size in (0, 239, 240, 359, 360, 10000)]
    cases += [
        ("two empires below threshold", [empire] * 2, 359, False),
        ("two empires at threshold", [empire] * 2, 360, True),
        ("three empires below threshold", [empire] * 3, 239, False),
        ("three empires at threshold", [empire] * 3, 240, True),
        ("landless does not supply second empire", [empire, landless], 360, False),
        ("landless does not supply third empire", [empire] * 2 + [landless], 240, False),
        ("landless does not invalidate eligible realm", [empire] * 3 + [landless], 240, True),
        ("kingdoms do not supply an empire", [empire, kingdom, kingdom], 10000, False),
    ]
    for name, titles, size, expected in cases:
        actual = evaluate(definitions["chg_realm_requirement_trigger"],
                          {"titles": titles, "size": size}, definitions)
        assert actual == expected, f"{name}: expected {expected}, got {actual}"
        shown_count = evaluate_value(values["chg_held_empire_count_value"],
                                     {"titles": titles}, definitions)
        expected_count = titles.count(empire)
        assert shown_count == expected_count, \
            f"{name}: display count {shown_count} does not match {expected_count}"
    return len(cases)


def check_tooltip_structure(mod: Path) -> None:
    decisions = parse((mod / "common/decisions/chg_decisions.txt").read_text(encoding="utf-8-sig"))
    decision = next(value for key, _, value in decisions if key == "chg_found_hegemony_decision")
    validity = next(value for key, _, value in decision if key == "is_valid")
    assert ("chg_realm_requirement_trigger", "=", "yes") in validity, \
        "Realm requirements must expand directly, not be flattened by a description wrapper"
    effects = parse((mod / "common/scripted_effects/chg_effects.txt").read_text(encoding="utf-8-sig"))

    def walk(entries: list[tuple], in_new_title: bool = False) -> None:
        for key, _, value in entries:
            # Regression for the 0.1.0 preview error: its title does not yet
            # exist, even inside hidden_effect. Keep predicates outside it.
            assert not (in_new_title and key == "limit"), \
                "Tooltip preview must not evaluate predicates in the unborn title's scope"
            if isinstance(value, list):
                walk(value, in_new_title or key == "scope:chg_new_hegemony")

    walk(effects)


def check_sources(mod: Path, game: Path) -> tuple[int, int]:
    assert mod.is_dir(), f"Mod directory missing: {mod}"
    scripts = sorted(mod.rglob("*.txt"))
    assert scripts, "No mod scripts found"
    joined = "\n".join(path.read_text(encoding="utf-8-sig") for path in scripts)
    for path in scripts:
        depth = 0
        for token in tokens(path.read_text(encoding="utf-8-sig")):
            depth += (token == "{") - (token == "}")
            assert depth >= 0, f"Unmatched closing brace: {path}"
        assert depth == 0, f"Unclosed braces: {path}"
    definitions = set(re.findall(r"(?m)^\s*(chg_[\w]+)\s*=\s*\{", joined))
    calls = set(re.findall(r"\b(chg_[\w]+_(?:trigger|effect))\s*=", joined))
    assert calls <= definitions, f"Undefined mod helpers: {sorted(calls - definitions)}"
    assert "chg_found_hegemony_decision" in definitions, "Decision definition missing"
    decisions = "\n".join(path.read_text(encoding="utf-8-sig")
                          for path in (mod / "common/decisions").glob("*.txt"))
    assert re.search(r"\bchg_realm_requirement_trigger\s*=\s*yes\b", decisions), \
        "Decision does not use the boundary-tested realm trigger"
    # These names denote scripted helpers, not engine commands. Resolve actual
    # external calls against installed game definitions without hardcoding a list.
    external = set(re.findall(r"\b([a-z][\w]*_(?:trigger|effect))\s*=", joined)) - definitions
    vanilla_definitions = set()
    for folder in ("scripted_triggers", "scripted_effects"):
        directory = game / "common" / folder
        assert directory.is_dir(), f"Game script folder missing: {directory}"
        for path in directory.rglob("*.txt"):
            vanilla_definitions.update(re.findall(r"(?m)^\s*(\w+)\s*=\s*\{",
                                                 path.read_text(encoding="utf-8-sig")))
    # hidden_effect is a script container, not a scripted helper.
    external.discard("hidden_effect")
    assert external <= vanilla_definitions, f"Unknown vanilla helpers: {sorted(external - vanilla_definitions)}"
    # CK3 1.20 changed the law file structure; older third-party validators
    # may fail to find real laws. Resolve the names against top-level entries.
    laws = set()
    for path in (game / "common/laws").rglob("*.txt"):
        laws.update(re.findall(r"(?m)^(\w+)\s*=\s*\{",
                               path.read_text(encoding="utf-8-sig")))
    used_laws = set(re.findall(r"\bhas_realm_law\s*=\s*(\w+)", joined))
    assert used_laws <= laws, f"Unknown realm laws: {sorted(used_laws - laws)}"
    for asset in re.findall(r'\breference\s*=\s*"(gfx/[^\"]+)"', joined):
        assert (game / asset).is_file(), f"Missing illustration: {asset}"
    loc_files = sorted(mod.rglob("*.yml"))
    assert loc_files, "No localization files found"
    game_languages = {path.name for path in (game / "localization").iterdir()
                      if path.is_dir() and (path / f"decisions_l_{path.name}.yml").is_file()}
    mod_languages = {path.parent.name for path in loc_files}
    assert mod_languages == game_languages, \
        f"Language coverage mismatch: missing {sorted(game_languages - mod_languages)}, " \
        f"unexpected {sorted(mod_languages - game_languages)}"
    localization_key_sets = []
    for path in loc_files:
        raw = path.read_bytes()
        assert raw.startswith(b"\xef\xbb\xbf"), f"Localization requires UTF-8 BOM: {path}"
        text = raw.decode("utf-8-sig")
        used_values = set(re.findall(r"ScriptValue\('([a-z_]+)'\)", text))
        assert used_values <= definitions, f"Undefined display values: {sorted(used_values - definitions)}"
        lines = [line for line in text.splitlines() if line.strip() and not line.lstrip().startswith("#")]
        language = path.parent.name
        assert lines[0] == f"l_{language}:", f"Wrong language header: {path}"
        assert path.name.endswith(f"_l_{language}.yml"), f"Wrong localization filename: {path}"
        assert "\ufffd" not in text, f"Replacement character in localization: {path}"
        keys = set()
        for line in lines[1:]:
            match = re.fullmatch(r'\s+([\w.]+):(?:\d+)?\s+"(?:\\.|[^"\\])*"\s*', line)
            assert match, f"Malformed localization line in {path}: {line}"
            assert match[1] not in keys, f"Duplicate localization key {match[1]} in {path}"
            keys.add(match[1])
        localization_key_sets.append(keys)
        # Native text aliases need to exist in every language, not only English.
        aliases = set(re.findall(r"\$([\w.]+)\$", text)) - keys
        native_keys = set()
        for stem in ("decisions", "major_decisions"):
            native_text = (game / "localization" / language /
                           f"{stem}_l_{language}.yml").read_text(encoding="utf-8-sig")
            native_keys.update(re.findall(r"(?m)^\s*([\w.]+):", native_text))
        assert aliases <= native_keys, f"Unresolved native text aliases in {path}: {sorted(aliases - native_keys)}"
    assert all(keys == localization_key_sets[0] for keys in localization_key_sets), \
        "Supported languages have different localization keys"
    needed_loc = set(re.findall(r"\b(?:text|desc|title|name|custom_tooltip)\s*=\s*(chg_[\w]+|chg\.[\w.]+)", joined))
    needed_loc.update("chg_found_hegemony_decision" + suffix
                      for suffix in ("", "_desc", "_tooltip", "_confirm"))
    assert needed_loc <= localization_key_sets[0], \
        f"Missing mod localization: {sorted(needed_loc - localization_key_sets[0])}"
    return len(scripts), len(loc_files)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mod", type=Path, default=ROOT / "mod/custom_hegemony")
    parser.add_argument("--game", type=Path,
                        default=Path("D:/SteamLibrary/steamapps/common/Crusader Kings III/game"))
    args = parser.parse_args()
    scripts, loc = check_sources(args.mod, args.game)
    cases = check_boundaries(args.mod)
    check_tooltip_structure(args.mod)
    print(f"PASS: {scripts} scripts, {loc} localization files, {cases} real-trigger boundary cases "
          "and live counts, native requirement tree, tooltip scope regression")
    print("Static checks only; see SMOKE.md for save evidence and remaining in-game UI checks.")


if __name__ == "__main__":
    main()
