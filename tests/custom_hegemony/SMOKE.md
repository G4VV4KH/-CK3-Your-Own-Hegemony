# Your Own Hegemony [1.20] smoke checks

Target: installed CK3 1.20.0.2 (Crozier). Start with a disposable save and a
playset containing only Your Own Hegemony [1.20]; repeat the successful scenario with
the intended playset afterward. Record the actual game version and enabled
DLCs with the results. The scenarios below are a checklist, not a claim that
runtime testing has occurred.

## Static check

From the repository root, run:

```powershell
& C:\Python314\python.exe tests\custom_hegemony\check_source.py
```

The script checks braces outside comments/strings, local helper references,
installed vanilla helper definitions, and UTF-8 BOM localization. It evaluates
the actual realm requirement and eligible empire triggers with a deliberately
limited interpreter. It does not emulate title creation, all CK3 syntax, game
rules, engine callbacks or succession.

## Decision and boundary checks

Use an independent adult emperor at peace with enough resources and fame.
Keep all other prerequisites satisfied while changing each tested condition.
`sub_realm_size` counts counties held by the ruler and their vassals; it does
not count baronies or the ruler's personal domain alone.

| Eligible empire titles personally held | Realm counties | Expected realm requirement |
|---|---:|---|
| 1 | 360 or more | Fail |
| 2 | 359 | Fail |
| 2 | 360 | Pass |
| 3 | 239 | Fail |
| 3 | 240 | Pass |
| 1 landed + 1 landless | 360 | Fail |
| 2 landed + 1 landless | 240 | Fail |

- Check that king-tier characters and existing hegemons do not receive the
  creation decision. Check a vassal emperor, war, unavailable adult, missing
  fame/resources, and the relevant custom-title game rule independently.
- A realm with an active ceremonial liege must show a failed requirement:
  vanilla destroys that institution when its top liege becomes a hegemon.
- Inspect all supported languages (English, Russian, French, German, Spanish,
  Polish, Japanese, Korean, Simplified Chinese): decision name, requirements,
  costs, effect tooltip and event text resolve and distinguish empires from counties.
- Version 0.1.2: verify that the OR shows two AND branches, each with separate
  empire and county checks. Empire counters must exclude landless titles.
  On the supplied `pre_create` save expect 3/3 and 347 >= 240 in the first
  branch (both pass), 3/2 and 347 >= 360 in the second (county check fails).
  Change eligible titles/realm size and reopen the decision to check live values.
- Verify that failed requirements disable the decision and spend nothing.

## Creation and save persistence

Before clicking, record resources, government, realm laws, the old primary
empire's custom name, coat of arms, colour, capital and title succession laws.
Record personally held empire titles, their de jure lieges and their holders.

1. Create the hegemony once. It becomes the primary title at hegemony rank and
   keeps the intended name, coat of arms, colour and capital. Existing empire
   titles remain held, the government is unchanged, and costs are charged once.
2. Check realm laws and any supported title succession laws against the recorded
   state. Specifically test an elective primary empire if law preservation is
   supported; inspect the new hegemony's actual succession screen and heir.
3. Check that personally held eligible empires become de jure vassals of the
   new hegemony. Verify existing kingdom/duchy/county de jure relationships
   inside those empires and existing character vassals remain intact.
4. Separately test an uncreated empire whose entire de jure territory is under
   the founder: it moves under the hegemony without being created or awarded.
   An uncreated empire with any county outside the realm must not move.
5. Check an unrelated external empire and landless empire titles remain outside
   the transfer. If foreign land lies inside a personally held empire, verify
   only the intended de jure relationship changes, not its actual ruler.
6. Save, reload and inspect rank, name, capital, de jure hierarchy, laws and heir
   again. Advance through succession on a disposable branch of the save and
   verify that the resulting inheritance matches the displayed laws.
7. Confirm the decision is unavailable after creation. Close the game and check
   its `error.log` for new `chg_`/Custom Hegemony errors, missing scopes,
   localization, invalid effects and title hierarchy failures.

## Compatibility focus

- Test treasury-based and nomadic governments only if the decision supports
  them; inspect the actual resource used, government and succession afterward.
- If custom-title creation overlaps a pre-existing historical hegemony's de
  jure land, inspect both hierarchies and any affected human player's UI.
- A custom hegemony rank does not by itself establish support for China's
  special Hegemonic Tributary mission system. Do not count those mechanics as
  verified by ordinary title creation.
- With the intended playset enabled, repeat decision visibility, successful
  creation, save/reload and log checks. Record conflicting mods if behavior
  differs from the isolated run.

## Results

2026-10-01: static checks passed against installed CK3 1.20.0.2: four scripts,
two localization files, 14 real-trigger boundary cases, external helpers, realm
law references, illustration and localization key checks.

Additional scope/syntax/loc review with CK3-Tiger 1.19.0 identified and fixed the
event localization scope syntax. Its remaining `nomadic_authority_5` missing-law
report is a version mismatch: CK3 1.20 now defines this law at the top level of
`common/laws/00_realm_laws.txt:2105`; the validator expects the older law
structure. No suppression or workaround was added to game scripts. Tiger is
not certified for CK3 1.20 and is not a complete passing validation of 1.20.

### User playtest and save inspection, 2026-10-01 (mod 0.1.0)

The user ran the game and supplied three saves. Their zipped text gamestates
were inspected without modifying the originals. The active playset also
contained Parley (`ugc_3811090081.mod`), so this is not an isolated-mod test.

| Fact | pre_create | post_create | post_inherit |
| --- | --- | --- | --- |
| Game date | 1178.10.1 | 1178.10.1 | 1178.10.23 |
| Player | Yusuf, 52679 | Yusuf, 52679 | Ali, 58856 |
| Primary title | e_arabia, 8442 | x_script_672, 18353 | x_script_672, 18353 |
| Primary rank | empire (5) | hegemony (6) | hegemony (6) |
| Realm counties | 347 | 347 | 347 |
| Government | clan | clan | clan |

- The realm contains exactly the same 347 county IDs in all three saves,
  verified by the de facto liege chains. Creation adds precisely one title;
  no old title is deleted and no old title changes holder at creation.
- Gold: 36929 -> 33329 (-3600); prestige: 19984 -> 12484 (-7500);
  piety: 2120 -> 320 (-1800). Creation occurs on the same game date.
- e_arabia (8442), e_persia (6079), e_maghreb (8022) all gain the new hegemony
  as de jure liege. Existing lower de jure relationships are preserved.
- Displayed dynasty naming remains Ayyubid ("Империя Айюбидов" ->
  "Гегемония Айюбидов"). Coat-of-arms content is identical even though the
  copied coat has a new ID (1240 -> 31668).
- The title capital remains c_damascus (8941); the actual realm capital remains
  b_cairo (8770). These are distinct concepts and both were checked.
- The new title stores RGB 27/144/80 before and after succession. The old
  title has no explicit colour in the save; vanilla e_arabia's base is
  32/150/85. Exact old/new map-colour equality is **not established**.
- Yusuf dies on 1178.10.11. Ali (58856) inherits the hegemony and Arabia;
  Uthman (59049) inherits Persia; Ghazi (59178) inherits the Maghreb. Both
  junior imperial titles remain de facto and de jure under hegemony 18353.
  The clan partition law `clan_impassive_partition_succession_law` remains.
- Domain limit changes 7 -> 8 and vassal limit 60 -> 80 at creation, consistent
  with a real rank increase. The number of vassals counting toward the limit
  remains 31 immediately after creation.

This verifies a landed clan ruler taking the three-empire branch and subsequent
clan partition. It does not verify the two-empire branch in-game, uncreated
empire integration, elective/administrative/nomadic succession, ceremonial-liege
blocking, colour equality, or a separately observed load-and-resume sequence.

### Tooltip regression and 0.1.1 verification

The user's `error.log` contains 4522 mod-related blocks from 07:29:09 to
07:33:36: 2261 occurrences each at `chg_effects.txt:61` and the decision caller
at `chg_decisions.txt:83`. They are the same null landed-title condition while
building the effect tooltip, not an error during actual title creation.
Other mod-prefixed error types were not found in that log.

0.1.1 computes `chg_title_capital` before `create_dynamic_title`, in character
scope; the new-title scope contains only effects. The source checker now
rejects conditional predicates inside that unborn title scope and checks the
unwrapped native requirement tree. All 14 boundary fixtures also evaluate the
actual live empire-count script value and pass. CK3-Tiger 1.19.0 reports zero
warnings and only its known 1.20 law-lookup incompatibility documented above.

### Repeat user playtest, 2026-10-01, 07:55 (mod 0.1.1)

Read-only inspection and SHA256 comparison show that only `post_create` was
updated. `pre_create` and `post_inherit` are byte-identical to the first run.
The unchanged inheritance save belongs to a different hegemony and must not
be treated as the successor state of the new creation save.

| Fact | pre_create (unchanged) | post_create (new) | post_inherit (unchanged) |
| --- | --- | --- | --- |
| Game date | 1178.10.1 | 1178.11.3 | 1178.10.23 |
| Player | Yusuf, 52679 | Yusuf, 52679 | Ali, 58856 |
| Primary title | e_arabia, 8442 | x_script_691, 18372 | x_script_672, 18353 |
| Realm counties | 347 | 347 | 347 |

- The new primary title is a real dynamic hegemony. Yusuf holds exactly one
  hegemony; Arabia, Persia and the Maghreb remain personally held and all three
  have title 18372 as their de jure liege. Lower de jure relationships persist.
- The county set is exactly equal to `pre_create`: no counties gained or lost.
  The other 19 new titles over the elapsed 33 days are dynamic county titles,
  not duplicate hegemonies. No old title was removed.
- The coat of arms is identical (1240 -> 31739), the title capital remains
  Damascus (8941), and the realm capital remains Cairo (8770). Clan government
  and the serialized realm laws are unchanged. Domain/vassal limits are 8/80.
- Resource changes across 33 days cannot establish exact decision cost. The
  first run remains the same-day evidence for the configured costs.
- The fresh log (07:54:57–07:56:11) contains no instances of the former
  new-title tooltip errors. It does contain 1124 mod localization error blocks:
  562 each for `chg_three_empires_held_tt` and `chg_two_empires_held_tt`.
  This is not a clean mod log. Unrelated vanilla/Parley errors also remain.

Source hashes:

```text
pre_create   6b0e0f190153c404c82377d437160dd1510c7b41f65d519bc9b460c48056f748
post_create  2146009058dba7cc1389d1aa3f72f943ea06a487da844714cd1697a03bf6d111
post_inherit 6a82fffd4f3af3d8e78e7663130a7774e13909dc8db294def347d24112ade24e
error.log    5e17d8cc9a3ca7ff6508a42a097bdc95481c001f153765ade1a4cf8452d6d1a8
```

Local detailed evidence is retained under `_dev/chg_save_audit/run_0755/`
(`audit_summary.json`, `log_summary.json`, and the log snapshot).

### Counter localization fix, 0.1.2

Both RU/EN empire counters now use
`[GetPlayer.MakeScope.ScriptValue('chg_held_empire_count_value')|V0]` instead
of the unresolved `THIS.Char` binding. This matches the installed vanilla
Basque decision's live county counter: `00_major_decisions_iberia_north_africa.txt`
line 879, `decisions_l_english.yml` line 1354 and `03_dlc_fp2_script_values.txt`
line 353. Actual eligibility still evaluates the original character scope;
only UI display binds to the player.

The source check passes for five scripts, two localization files and all
14 trigger/count fixtures. The subsequent runtime log is recorded below.
Expected UI values for `pre_create` are 3/3 with 347/240, and 3/2 with 347/360;
only the latter county check fails. Actual rendered values and layout have
not been inspected in a screenshot or live interface.

### Repeat user playtest, 2026-10-01, 08:05 (mod 0.1.2)

Both `post_create` and `post_inherit` have new SHA256 hashes. `pre_create`
remains the unchanged baseline. The active launcher descriptor is 0.1.2,
with Custom Hegemony and Parley enabled on CK3 1.20.0.2.

| Fact | pre_create | post_create | post_inherit |
| --- | --- | --- | --- |
| Game date | 1178.10.1 | 1178.11.5 | 1179.1.7 |
| Player | Yusuf, 52679 | Yusuf, 52679 | Ali, 58856 |
| Primary title | e_arabia, 8442 | x_script_691, 18372 | x_script_691, 18372 |
| Primary rank | empire (5) | hegemony (6) | hegemony (6) |
| Realm counties | 347 | 347 | 347 |
| Government | clan | clan | clan |

- Title history records creation on 1178.11.5 and transfer to Ali on
  1178.12.18. Both post saves contain the same hegemony as the primary title.
  The ruler holds exactly one hegemony in each state.
- The exact set of 347 county IDs matches across all three saves. The new
  hegemony includes Arabia (8442), Persia (6079), and the Maghreb (8022)
  de jure and de facto before and after succession.
- Ali inherits the hegemony and Arabia; Uthman (59049) inherits Persia;
  Ghazi (59178) inherits the Maghreb. Both junior rulers remain within Ali's
  realm. The existing imperial titles are retained.
- The original coat of arms is copied identically (1240 -> 31740) and persists
  through succession. The title capital stays Damascus (8941), the realm
  capital stays Cairo (8770), and the hegemony's RGB 26/147/82 remains unchanged
  between the two post saves. Exact equality with the original empire colour
  is still not established.
- Government remains clan. `clan_impassive_partition_succession_law`,
  `male_only_law`, and `crown_authority_1` persist. The serialized coronation
  status changes from `crowned_king` to `uncrowned` for the new ruler; therefore
  the entire realm-law set must not be described as identical after succession.
- Domain/vassal limits are 8/80 after creation and 6/80 under Ali. These are
  different characters, so the lower personal domain limit is not evidence
  of a rank loss: hegemony rank and vassal limit remain intact.
- Creation is 35 days after the baseline; resource deltas include intervening
  gameplay. The exact price remains verified by the first same-day run, not
  by this new comparison.
- The log from 08:03:49 to 08:04:53 contains 105 error blocks and **zero
  Custom Hegemony references**. Neither former counter localization error nor
  the new-title tooltip error recurs. Remaining named sources are vanilla or
  Parley; two startup key-reference blocks provide no source filename.
  This supports the fixes but does not establish that the whole game log is
  clean or independently verify the rendered decision tree and numeric values.

Source hashes:

```text
pre_create   6b0e0f190153c404c82377d437160dd1510c7b41f65d519bc9b460c48056f748
post_create  669558fe2cfe58dfd035dd09034d48a19870edb279a6ae8b8a530b0bcf24a7b0
post_inherit ce83e1ee7acf852e412f3b5cf495ddecc18bccce9a96c4128d1864c699af0beb
error.log    7862ddd14c59c1b5dc18084b3ff79bb51714cae006637777a04eabc7a9509c9d
```

Read-only evidence and the audit script are retained locally under
`_dev/chg_save_audit/run_0805/`. No new gameplay fix was required by this run;
the mod version remains 0.1.2. Untested governments and alternative requirement
branches remain subject to the earlier limitations.

### Name and localization update, 2026-10-01 (mod 0.1.3)

The source and launcher descriptors now agree on `Your Own Hegemony [1.20]`,
version `0.1.3`, supported version `1.20.*`, and the Steam version tag
`1.20 'Crozier'`. The existing installation path and script identifiers remain.
Gameplay scripts, requirements, prices and title creation effects did not change.

All nine installed game languages have complete matching sets of 16 keys:
English, Russian, French, German, Spanish, Polish, Japanese, Korean and
Simplified Chinese. Files are UTF-8 with BOM; directory, filename and header
languages match. The source checker verifies full language coverage against
the installed game's decision files, key parity, and resolution of native
localization aliases in each language. It passes with five scripts, nine
localization files and all 14 boundary/live-counter cases.

The prose is derived from each language's own vanilla translations:

- Decision name, description and tooltip: `found_empire_decision` family in
  `decisions_l_<language>.yml`, adapting the rank and grammatical agreement.
- Confirmation: `$found_empire_decision_confirm$`.
- Event title: `$major_decisions.1101.t$` (custom kingdom).
- Event description: exact `major_decisions.1101.desc` text, replacing only
  `new_title.` with `chg_new_hegemony.`. Native dynamic ruler titles and
  language-specific forms are retained.
- Event option: exact `major_decisions.1103.a` text with the same scope change.

A separate comparison against all nine native files passed for the event
description and option. Both empire-counter expressions retain `GetPlayer`
and the appropriate thresholds. Local evidence is saved in
`_dev/chg_localization_v013_audit.json`.

The prior 0.1.2 creation/succession evidence still concerns the same gameplay
scripts. New 0.1.3 wording, native text aliases and rendering in all nine
languages have not been checked in a running game. No Workshop upload was
performed as part of this name/localization change.
