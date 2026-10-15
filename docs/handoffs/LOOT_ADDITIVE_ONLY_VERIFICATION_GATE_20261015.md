# Ambient Odyssey — additive-only loot verification gate
**15 October 2026 | Source-review findings and Work-mode implementation acceptance | NOT runtime-tested**

## Owner hard requirement
**Triple-check every proposed loot change is additive, not a replacement.** Preserve native contents, thematic/unique drops, vanilla and Apotheosis native chest-affix chances, existing gem drops and crafting, vanilla Bonus Chest base drops, and Lootr per-player instancing. For Tier2+ Scrap/Treasure and Tier3+ 5%-Grand Treasure, only add to the original roll; no wholesale rewrite. For bosses, preserve original loot and add guaranteed affixed item + Regalia (approved exclusions) + one random full-pool Simply Swords sword, plus approved T6–T8 rare bonus affix rolls. Native-only families untouched.

## Verified SOURCE-level observations from existing draft PRs (not proof of live behavior)
- PR #51 `tools/test_ao_loot_first_pass.py` explicitly checks **no** `data/minecraft/loot_table/chests/spawn_bonus_chest.json` replacement exists in the starter addon and checks Java append operations `loot.add(...)`; additionally checks `data/neoforge/loot_modifiers/global_loot_modifiers.json` contains **`"replace": false`**.
- PR #51 acceptance `docs/testing/V051_LOOT_ECONOMY_PILOT_ACCEPTANCE.md` explicitly requires original vanilla Bonus Chest tools/supplies still appear alongside additions, in two-player Lootr rolls. This is a checklist, not a completed runtime pass.
- **Important potential conflict:** PR #51 includes a datapack at `release_030/overrides/config/paxi/datapacks/ao_starter_apotheosis_exemptions/data/apotheosis/loot_modifiers/affix_conversion.json` that DEFINES replacement modifier parameters (not a simple add-only entry): 0 chance for spawn Bonus Chest, 0 for block table regex, 0.35 for generic entries. This may be an intentional scope-specific suppression of double affixing, but it is **not evidence that every native Apotheosis roll remains unchanged**. Work must source-diff effective original modifier and verify exactly which contexts are affected, including when combined with PR53/57 and other datapacks. Other affix/gem loot injection exemptions in this pack require the same scrutiny.
- PR #57 `addons/ao-campaign/.../loot_modifiers/rage_glove_gate.json` and its loot global modifier list are experimental; an older 10%-Monstrosity Rage Glove gate is not final owner-approved. Audit for remove/filter effects, not only appends.
- A loot modifier's `replace:false` in a *global modifier list* means entries are appended to the list, but DOES NOT independently guarantee the modifier's Java implementation preserves the passed native loot list. Verify it is non-destructive in code and runtime.

## Three independent proof layers — ALL REQUIRED
**1. Source/static proof (before PR):** For every modified table/source/loot modifier record old table ID, original content hash, new entries, exact original codepath preserved, pool conditions, datapack precedence, collision/mixin hooks, effective Lootr conversion, and whether any `replace`, `setLoot`, `clear`, `removeIf`, replacing native table namespace or full loot-list reconstruction exists. All such cases are BLOCKED unless explicitly approved for unrelated scoped legacy fixes. Diff final effective resources, not only branch files.
**2. Statistical proof (disposable world):** Draw comparable native baseline and patched loot samples from identical chest/table context using fixed test setup. Require original obtainable items remain obtainable, native unique weights unchanged where promised, native Apotheosis affix distribution unchanged, and observed supplemental 5% Grand proc roughly matches expectation within sample variability; don't infer zero probability from a 100-roll sample. Account for loot RNG and Lootr instanced context, not just identical absolute counts.
**3. Multiplayer/integration proof:** Two non-op players inspect unopened same Lootr chest independently. Original content and AO bonus both present. Reopen/relog/restart should not reroll extra. Check generation-time fixed NBT, one-time trophies, new player joining after prior open, and same chest sources loaded via different datapack paths. Repeat boss kills must preserve native drops even when AO guaranteed bonuses fire. Dedicated server confirms save/load.

## Mandatory negative cases
- No T3 Grand roll in T0–T2 or outside verified eligible dungeon structures.
- No Grand triggers on `minecraft:chests/spawn_bonus_chest`, unrelated villages, decorative barrels, generic shared vanilla chests in other contexts, fixed progression trophy chests or early Mine Cells.
- Grand **exactly one native best-pool draw** (not a full second loot table generation); avoid recursive trigger and duplicate unique boss trophies.
- Standard Apotheosis chest affix conversion and gem drops must not be globally diluted or suppressed by accidental replacement/datapack collision. Any intentional legacy Bonus Chest anti-double-roll logic requires separate explicit documentation and testing.
- No custom gems/apex gem recipe changes; no Regalia bonus entries from Enigmatic Legacy/Plus or Pasterdream accessories; native-only item drops never removed.
- A failed register lookup or missing source loot table MUST fail closed (skip optional bonus and report), not replace native contents with empty list.

## Scoped implementation-ready action list
1. Inspect the exact installed full pack *effective* resource stack against PR #50, #51, #53, #57 and post-PR overlays. Find the actual native and overridden Apotheosis affix conversion, affix injection, gem injection and global modifier registrations. Log conflicts with evidence.
2. From PR #45 `docs/balance/v3-evidence/LOOT_TABLE_INDEX.csv` and PR #56 native NBT audits (on their actual branch refs), build a verified chest mapping for representative Tier2–6 sites. Minimum 20 meaningful chest contexts before broad new roll activation. Do not invent IDs.
3. Implement minimal reusable additive bonus provider only for verified context; avoid wholesale table changes. Native best-pool roll requires a source-specific scoped pool selection with preserved native conditions; if impossible in an installed mod's loot format, mark blocked instead of faking.
4. Add CI/static tests asserting no touched native loot table replacement paths, unchanged native table bytes where expected, bonus only appends, native modifier conditions not broadened, and correct effective modifier list precedence. Include tests for overwriting global `replace:true` mistakes and duplicate registration.
5. Run native integrated client/dedicated-server test if environment supports it. If not, report static-only with exact manual 2-player checklist and never claim verified.
6. Keep one immutable rollback per changed loot modifier/datapack and a per-table audit matrix with PASS/BLOCKED/NOT TESTED and source commit+SHA256.

## Explicit statuses as of writing
- Existing PR51 *starter bonus* has source-level append assertions and checks for `replace:false`: **source evidence only**.
- Existing PR51 Apotheosis exemption pack changes effective modifier definitions: **potential interaction requiring review**, not a proven regression and not proof of untouched native odds.
- New Tier2+ Scrap/Treasure, Tier3+ Grand best-pool 5%, and guaranteed per-boss supplemental loot: **owner-approved design only; no production loot code or integrated runtime proof from this audit**.
