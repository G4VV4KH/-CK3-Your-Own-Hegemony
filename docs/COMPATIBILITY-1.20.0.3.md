# CK3 1.20.0.3 compatibility review

Reviewed on 2026-10-01 for **Your Own Hegemony 0.1.3** against CK3 **1.20.0.3 (Crozier)**, Steam build **25652598**. The preserved comparison baseline was CK3 1.20.0.2, build 25588574.

**No runtime patch was needed.** The public title remains **Your Own Hegemony [1.20]**, the mod version remains **0.1.3**, and the descriptor still supports **1.20.***. This was an upstream/source audit, not a new in-game playtest.

## Checks and findings

The existing source checker passed against the installed update: five scripts, nine localization files, all 14 actual requirement/live-counter boundary cases, native helper/law/illustration references, localization consistency and the unborn-title tooltip regression.

The two directly called native triggers resolve to nine reachable scripted helpers across three files. Their definitions remain unchanged: ceremonial-liege detection, imperial power projection and its targeting/faith-gate helpers. In total, 38 relevant upstream files are byte-identical to the preserved baseline, including the custom-empire reference decision/effects, title-gain and inheritance callbacks, realm/succession laws, governments, election definitions, game rules and defines.

Across all 3,731 archived script/GUI/data-binding files, 3,720 are identical, 11 changed and none are missing. The potentially relevant changes do not require adapting this mod:

- The native grant-title interaction no longer blocks an election candidate through its former unfairness condition. Hegemony never calls or replaces that interaction; it creates and grants its own dynamic title using title/vassal-change effects.
- The pilgrimage payment fix adds treasury-availability guards. Hegemony's decision already selects gold or treasury directly using `has_treasury`.
- Rite, anointment, court-conversion and Iberian-struggle fixes do not change Hegemony's native helper dependencies. The mod creates no faith/rite and calls none of the changed conversion effects.
- Transport-contract scope and the delayed Latin Empire event are outside this mod's references and overrides.

All 14 gameplay/localization files matched both the published source and prepared runtime. Current native localization aliases resolve in all nine languages, and the adapted event text matches the installed native text with its intended title-scope substitution.

## Evidence boundaries

The creation and clan-partition playtest remains **mod 0.1.2 on CK3 1.20.0.2**, with the exact set of 347 counties preserved. Version 0.1.3 retains the same gameplay scripts. Those facts do not establish that the same scenario was rerun on 1.20.0.3.

No engine launch was performed during this audit. The preserved script archive contains no engine binary or old localization snapshot. Two-empire gameplay, uncreated-empire incorporation, other governments, special/elective succession, removal, multiplayer and all nine languages' runtime rendering remain unverified. CK3-Tiger 1.19 was not presented as a certified validator for CK3 1.20.

The compatibility update changes maintained descriptions and developer documentation only. Existing game payloads, ZIPs and historical source locks/manifests remain intact. The local release journal retains full file hashes and comparison evidence.

See the [official 1.20.0.3 notes](https://store.steampowered.com/news/app/1158310?emclan=103582791465554434&emgid=684140727200907566) and the existing [gameplay evidence and untested scenarios](../tests/custom_hegemony/SMOKE.md).
