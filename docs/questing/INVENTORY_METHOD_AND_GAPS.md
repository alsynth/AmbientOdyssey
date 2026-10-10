# AO quest mapping — Inventory method and verification gaps

**Date:** 10 October 2026. **Status:** planning evidence only.

## Inputs

1. GitHub `INSTALLED_MOD_STRUCTURE_SCREENING.csv` includes **196 historically audited JARs** from Test5 Audit1; the screening covered their structure/resource footprint, **not their full gameplay content**.
2. `MISSING_JARS.txt` records **41 earlier-client JAR names not retrievable in that audit**. They were observed in logs, but that audit did not open their binaries. This is a partial evidence stream, not proof they are currently installed.
3. The live development branch `release_030/release-lock.json` contains **51 additions or repins**, alongside remove-project lists. Some are already present in the historical audit, others are shaders or libraries, and some were integrated only in the newer Test8.2 source candidate.
4. The older `requests.json` lists **177 requested named projects**, **not** a reliable installed-mod inventory. Use it only as a list of potential identity aliases or for cross-checks; don't silently promote requested-but-removed mods into quests.
5. The 0.3.1 source handoff ZIP contains a base v0.2.10 CurseForge manifest with **221 project/file entries**, which have integer project IDs without readable project names; direct current Test8.2 manifest / runtime reconciliation remains required.

After naming and splitting source integrations, `MOD_QUEST_COVERAGE_MATRIX.csv` has **265 provisional records** (including shaders, libraries and historical/repinned variants). **This count is coincidentally similar to the active source's ~265 CF refs and does not certify an exact 1:1 match.** Some records may be renamed, repinned or duplicate JARs until a current runtime full-mod list is extracted.

## Evidence statuses

- `Test5 resource audit`: JAR was inspected previously for resources; that alone doesn't validate every progression feature.
- `Test5 client-log uninspected JAR`: named in logs, no binary inspection at Test5.
- `Test8.2/8.3 source addition or repin`: listed in GitHub source lock. Confirm game-loaded state in the exact next runtime build.
- Multiple evidence statuses: merged records from the above sources; do not imply duplicate installations.
- `?` quest priority: actual gameplay scope unresolved; triage with source descriptions / recipe and registry dumps.

## Explicitly excluded from current content mapping

- Born in Chaos (removed); Dimensional Doors (removed due to creative mode crash); My Picture Frame (removed due to TwelveMonkeys module conflict); Companions / Modern Companions (removed); Tectonic and previous Amaranth/Twigonometry stack (removed).
- QoL, Origins addons and new structure candidates merely discussed but not accepted/pinned.
- Mine Cells Fabric/Sinytra, Big Globe and other parked future experiments **must not receive impossible installed quests** until actually included.
- Questlog itself is research only; *Questlog quest seeds* are abstract authoring input and cannot be mistaken for installed definitions.

## Editorial audit categories

The matrix priority class is an *initial decision about player-visible quest value*, not necessarily a count of features:
- **A**: major campaign (large combat/realm/gear gameplay); mod may appear in more than one shared content arc.
- **B**: significant optional adventure content.
- **C**: shorter optional experience.
- **D**: educational FTB manual.
- **E**: non-linear Explorer Journal tracking.
- **I**: dependency/integration merged under another module.
- **X**: technical, visual or no direct quest.
- **?**: investigate — default to NOT making unsupported claims.

A **content provider** can be technically complex even if it receives few Questlog tasks. Conversely a small mod adding a major boss/realm can deserve a large campaign.

## High-confidence versus high-risk information

**High confidence:** AO currently intends extensive Nether/End/Overworld exploration, enchanted diamond + two A-grade combat supports by Tier 2, Questlog 3.4.1's available task kinds and JSON authoring, original mod-pack preference, and current Github source lock.

**Medium confidence:** Broad presence of Twilight Forest, Eternal Starlight, Aether, Undergarden, Cataclysm, Mowzie, Aquamirae and sources from JAR names; verify actual version and natural worldgen.

**Require exact-version inspection:** NeoPasterDream `0.9.6` realm accessibility / boss completeness; Enigmatic Legacy Plus `1.1.2` cursed-and-standard items/access; difficult spellbook/Relics progression; content of small or newly ported mods, supported Origin backend and player effects.

## Before first actual Questlog JSON release

1. Get exact latest Test8.3 `latest.log` mod list and manifest with `projectID/fileID` or mod ID, reconcile every matrix row.
2. Pull entity/item/structure/dimension registries and real advancements; inspect `config/` and recipes for each major mod.
3. Mark each chapter beat as **verified achievable**, **optional/available**, **unobtainable in current release**, **needs custom trigger**, or **requires a specific version upgrade**. Unachievable beats must never ship.
4. Pilot a small set of beginner quests and modded structure/biome quests on a copied two-player server. Validate player progress, rewards and UI coexistence with FTB Quests.
5. Only then compile approved seeds into real `config/questlog/quests/...` JSON and FTB manual pages. Patch source authoring files and run validators before deploying.

## Attribution / public website

Descriptions and objective names must be written for AO and cite source mod IDs where appropriate. Don't copy the quest prose, rewards, illustrations or assets from other packs verbatim. Version labels and copyright/licensing of original images matter if later published publicly on the AO Wiki.
