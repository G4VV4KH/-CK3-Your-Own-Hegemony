# Contributing to Your Own Hegemony

Your Own Hegemony 0.1.4 targets CK3 1.20.0.4 (Crozier), with `1.20.*` descriptor support. This isolated release candidate changes only the French founding-event complement and the descriptor version from the published 0.1.3 payload. Its complete candidate-bound localization gate passed for all nine supported CK3 languages: all 144 authored language/key cells and the required event and decision contexts were verified. The accepted report is bound to the exact 16-file 0.1.4 runtime; visual-layout coverage remains separately limited. Historical evidence below retains its original scope; it is not a new gameplay acceptance claim. Runtime source lives in `mod/custom_hegemony/`; source checks and recorded gameplay evidence are in `tests/custom_hegemony/`.

## Source and public documentation

- `mod/custom_hegemony/`: decision, event, helper scripts, localization, descriptor and runtime thumbnail.
- `mod/custom_hegemony/README.md`: preserved development history and implementation details; dated entries describe their original state.
- `tests/custom_hegemony/check_source.py`: limited source interpreter and consistency checks.
- `tests/custom_hegemony/SMOKE.md`: runtime scenarios, completed checks and evidence limits.
- `publishing/description.en.md`: published projection of the canonical public description; do not maintain it independently.
- `docs/images/`: reviewed screenshots used by the public README.

The local release workspace holds the publication renderer, platform links, deterministic packaging tools, deployment pack and platform journals. Its release registry identifies the editable canonical description in the current metadata revision's `02-TEXT/description.en.md`; older deployment packs remain frozen. The renderer reads that file together with `10-GITHUB-DEV.md` and `11-PUBLICATION-LINKS.json`, then writes a separate output directory. Keep functional facts identical across formats; platform-specific presentation and verified links may differ.

## Gameplay boundaries

Preserve the `chg_` namespace and the `custom_hegemony` installation identity. The decision requires either three eligible landed empires and 240 realm counties, or two and 360. Counts include vassal counties, exclude baronies and exclude landless imperial offices. Both player and AI use the same requirements; the AI checks every 60 months.

Founding creates one dynamic hegemony, makes it primary and incorporates eligible personally held empires and wholly controlled unheld empires de jure. Existing empire titles remain. Integration runs at founding, not continuously after conquest. The old primary empire supplies the base name, coat of arms, map color and de jure capital.

Retain the native custom-title and imperial power projection checks and the ceremonial-liege guard. Do not imply that special title succession laws are copied or that this mod supplies historical Chinese hegemony mechanics.

## Running the source check

From the repository root, with Python 3 and the matching installed CK3 game files:

```powershell
python tests/custom_hegemony/check_source.py --game 'D:/SteamLibrary/steamapps/common/Crusader Kings III/game'
```

Replace the game path for your installation. The checker also accepts `--mod` for an explicit mod directory. It checks five scripts, local helper references, referenced vanilla definitions, complete nine-language coverage and all 14 boundary/live-counter cases. Localization uses UTF-8 with BOM and matching 16-key sets.

The interpreter covers selected trigger and count behavior. It does not emulate all CK3 syntax, title creation, engine callbacks or succession. Runtime changes need the relevant scenarios from [SMOKE.md](tests/custom_hegemony/SMOKE.md), with the actual mod/game versions, DLCs, playset, save and observed result recorded.

## Evidence and current limits

The [1.20.0.3 compatibility audit](docs/COMPATIBILITY-1.20.0.3.md) found no required runtime patch: 38 relevant upstream files and the nine reachable native helper definitions remain unchanged, and the existing focused source checks pass against the installed update. No fresh engine run was performed. Compatibility prose changed; runtime scripts, descriptors and distributed ZIPs did not.

The 0.1.2 playtest on CK3 1.20.0.2 confirmed creation and subsequent clan-partition succession for the same hegemony, preserving the exact set of 347 counties. Junior heirs retained their empires as vassals of the new hegemon. The coronation state changed to `uncrowned`, so the entire realm-law state must not be described as unchanged. The game log was not globally clean; the scoped run had no `chg_` errors.

The 0.1.3 name and localization update leaves gameplay scripts unchanged. Source/localization checks passed. Later English screenshots show the decision, rank-gained ruler and Hegemonies, De Jure map; they do not show the installed mod version. Decision/result resource differences match 3,600 gold, 7,500 prestige and 1,800 piety. Screenshots alone do not verify a save's title structure.

The two-empire branch, incorporation of unheld empires, other governments, special/elective succession, multiplayer, removal after founding and rendering in all nine languages remain unverified. The playtest used All Under Heaven; no mandatory DLC gate was established, and a DLC-disabled run was not performed. Exact map-color equality was not established by the supplied save comparisons.

## Releases and contributions

Keep developer, generated game and downloaded store copies distinct. The author's active local development tree is recorded in the release workspace; this repository is its published source snapshot. Synchronize reviewed authoring changes before a release. Never use a downloaded Workshop copy as the source.

The local DEV descriptor may have the exact `[DEV] ` name prefix. Public artifacts must be named **Your Own Hegemony [1.20]**. The packager records this explicit name normalization and may add `picture="thumbnail.png"`; it preserves gameplay bytes. Keep tests, developer documentation, local paths, credentials, saves and logs out of runtime archives.

Steam uses the prepared runtime directory. Paradox receives a ZIP with `descriptor.mod` and runtime folders directly at the root. Nexus manual downloads use the mod folder, a sibling portable `.mod` wrapper and `INSTALL.txt`. Verify archive members and downloaded payloads, then append evidence to the dev-to-game and individual platform journals; a successful upload is not download verification. Documentation-only changes can require a GitHub update without changing the game package.

For a contribution, explain the player-visible change, affected files, relevant checks and remaining untested cases. Preserve all nine language keys and formatting tokens. No additional open-source license or redistribution permission is granted by this deployment preparation; platform terms and author permissions remain separate.
