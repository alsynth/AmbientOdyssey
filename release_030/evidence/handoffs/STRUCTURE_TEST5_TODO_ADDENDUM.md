# Ambient Odyssey — Structure Test 5 TODO Addendum

**Status:** Preparation and analysis completed in part; implementation remains pending.

## Priority 0 — Source reconciliation

- [ ] Extract current Test 4 and editable sources.
- [ ] Diff Test 4 against the original source build.
- [ ] Merge Test 3/4 corrections back into `structure-density.json` and appropriate compiler inputs.
- [ ] Ensure repeated compilation produces the same intended configuration.
- [ ] Preserve existing unrelated modpack configuration.

## Priority 1 — Structure registry and biome audit

- [ ] Inspect installed JARs for every major structure provider.
- [ ] Catalogue registered structure IDs and corresponding structure-set IDs.
- [ ] Resolve nested biome tags against the active AO biome roster.
- [ ] Identify genuinely vanilla-only spawning conditions.
- [ ] Separate surface, underground, ocean, Nether and End eligibility.
- [ ] Patch verified missing climate-appropriate modded biome membership.
- [ ] Fix obsolete IDAS BYG and optional Aether Villages references.
- [ ] Generate a per-mod, per-structure compatibility report.

## Priority 2 — Structure placement

- [ ] Remove Small Blimp entirely from every native and AO placement path.
- [ ] Remove Coliseum entirely.
- [ ] Reduce Bathhouse independently without reducing unrelated small structures.
- [ ] Verify and increase Dungeon Crawl placement.
- [ ] Increase ordinary IDAS houses and medium buildings.
- [ ] Correct WDA Heavenly trio placement, biome compatibility and individual rarity.
- [ ] Inspect Sky Villages and Sky Whale Ship's land/ocean placement behavior.
- [ ] Adjust Moog's Soaring Structures only where existing selectors or placement rules are insufficient.
- [ ] Investigate duplicated structure-set membership and competing placement salts.
- [ ] Preserve rarity for major boss landmarks and castles.

## Priority 3 — Structure integrity

- [ ] Check WDA Foundry missing jigsaw references.
- [ ] Check IDAS Dread Citadel and Ancient Mines missing pools.
- [ ] Check Integrated Villages Cabin Village missing pools.
- [ ] Check CTOV waystone pool references.
- [ ] Audit overlap prevention without adding StructureOverlapless.
- [ ] Verify Integrated API 1.9.0 disabling and unskippable-structure behavior.

## Priority 4 — Independent compatibility/performance

- [ ] Investigate Streams Reflowing slow terrain-sampling fallback.
- [ ] Review RAR-Compat/Artifacts slot-tag overwrite.
- [ ] Diagnose stale Traveloptics references.
- [ ] Diagnose Cataclysm Spellbooks missing recipe items.
- [ ] Prepare Tan's Huge Trees biome-specific density tuning.
- [ ] Preserve wildlife, biome-size and climate changes as separate test stages.

## Build acceptance checklist

- [ ] Source compilation succeeds.
- [ ] Every generated JSON file parses.
- [ ] All added structure IDs exist in the installed registry resources.
- [ ] Required biome tags resolve.
- [ ] Disabled structures have no intended remaining placement path.
- [ ] Source rebuild reproduces the exported configuration.
- [ ] CurseForge ZIP contains root `manifest.json`.
- [ ] ZIP archive integrity passes.
- [ ] All static changes are documented.
- [ ] Outstanding runtime tests are explicitly listed.

**Do not proceed to a new gameplay test until the static compatibility pass and Test 5 packaging are complete.**
