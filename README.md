# Your Own Hegemony [1.20]

Make late-game rule easier: unite your imperial crowns under a single hegemony, with a new primary title above empire rank.

## At a glance

- Version 0.1.3. Targets CK3 1.20.*; validation baseline: 1.20.0.2 (Crozier).
- Standalone: no other mod is required.
- Adds the major decision "Found a New Hegemony" and a founding event.
- Nine languages: English, Russian, French, German, Spanish, Polish, Japanese, Korean and Simplified Chinese.

## An empire is only the beginning

Bring several imperial crowns together under a new title above empire rank. Your Own Hegemony follows the structure of the vanilla custom-empire decision, with larger requirements and a single purpose: founding your own hegemony.

## Two paths to a hegemony

- Personally hold at least 3 landed empire titles and control at least 240 realm counties; OR
- Personally hold at least 2 landed empire titles and control at least 360 realm counties.
- County totals include your vassals' counties, not just your personal domain. Baronies do not add to this total. Landless imperial offices do not count as imperial crowns.

## Other requirements

- Be an independent, available adult emperor at peace, outside a confederation, with a landed empire as your primary title.
- Reach fame level 5. Nomadic rulers also need the highest nomadic authority.
- Your realm must have no active ceremonial liege: becoming a hegemon would otherwise dissolve that institution through vanilla behavior.
- The vanilla custom-kingdoms/empires game rule must allow creation, and the vanilla imperial power projection check must pass.
- Existing hegemons do not receive the decision. The requirement panel includes separate empire and county checks for each path.

## The price

3600 gold, 7500 prestige and 1800 piety. A government with a treasury pays 3600 treasury instead of gold. Nomadic rulers are exempt from the gold and piety costs, following the vanilla decision pattern. The county requirements stay the same.

## What founding does

- Creates a real dynamic hegemony title and makes it your primary title.
- Uses your former primary empire's base name, coat of arms, map color and de jure capital as the new title's identity. You can rename it through the ordinary title window.
- Moves every landed empire you personally hold under the new hegemony de jure.
- Also includes empires with no holder whose entire de jure territory you control, following the vanilla custom-empire pattern.
- Keeps your existing empire titles. Founding does not redistribute county ownership or existing vassals.
- De jure incorporation happens when you found the hegemony. Later conquests are not automatically incorporated by this mod.

## AI and scope

AI emperors use the same decision and requirements, with a check every 60 months. The mod adds its own files and does not overwrite vanilla files or add recurring global handlers. It does not add China's special tributary missions, the dynastic cycle or the unique privileges of historical hegemonies.

## Compatibility and testing

- Creation and subsequent clan-partition succession were checked on CK3 1.20.0.2 with version 0.1.2: the exact set of 347 realm counties was preserved, and junior heirs who inherited empires remained vassals of the new hegemon.
- The recorded playtest used All Under Heaven. No explicit DLC requirement was found in the mod or the vanilla helpers it uses; operation with that DLC disabled has not been separately tested.
- Version 0.1.3 changes the displayed mod name and adds complete nine-language text coverage; its gameplay scripts are unchanged. All 14 source boundary/count checks pass. English decision/result screenshots have been reviewed, including the exact 3600 gold, 7500 prestige and 1800 piety cost. The installed mod version is not visible in those screenshots; rendering of all nine languages has not been checked.
- The two-empire path, incorporation of unheld empires, other governments and special/elective succession have not been verified in gameplay. Special title succession laws are not explicitly copied; inspect the new title's succession before relying on them.
- The script copies the old map color, but exact old/new color equality was not established by the supplied save comparisons. Compatibility with total conversions and other hegemony-formation mods is untested.

## Installation

Subscribe on your chosen platform and enable Your Own Hegemony [1.20] in your launcher playset. For a manual download, use the supplied manual-install archive and follow its INSTALL instructions. Enable only one copy of the mod. If updating from Custom Hegemony, the internal installation name and script identifiers are unchanged. Back up a save before changing its mod list; removal after founding a hegemony has not been tested.

## Feedback

Questions, suggestions or a problem? Contact g4vv4kh@gmail.com. For a bug report, include the CK3 version, mod version, enabled DLCs and mods, the affected save if possible, and the steps that led to the issue.

## Credits and creation

Design and playtesting: G4VV4KH. The code, translations, cover artwork and publication text were created with generative AI from the author's design and direction. Localized decision and event prose adapts the corresponding vanilla CK3 text.

## Source and issue tracker

[Your Own Hegemony on GitHub](https://github.com/G4VV4KH/-CK3-Your-Own-Hegemony)

## More mods by G4VV4KH

Optional companions; neither is required by Your Own Hegemony.

- [Parley: The Negotiating Table](https://steamcommunity.com/sharedfiles/filedetails/?id=3811090081) — Negotiate agreements between rulers.

- [Marriage Calculation Assistant](https://steamcommunity.com/sharedfiles/filedetails/?id=3811100163) — Compare marriage candidates using an optional gameplay-potential score.

## Support development

[Want to support my work? Donate on Ko-fi 💛](https://ko-fi.com/g4vv4kh)
