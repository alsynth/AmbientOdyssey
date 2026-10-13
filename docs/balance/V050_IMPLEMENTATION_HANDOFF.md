# Ambient Odyssey v0.5 RPG design → safe implementation queue
**13 Oct 2026 · Handoff for ChatGPT Work mode / Claude · plan/spec only, not runtime executed**

## Permanent scope exclusion
**Origins is not part of Ambient Odyssey.** Do not install Origins / NeoOrigins, Origin race/power/class/background addons, or implement any Origins chapter, Origin objective, character selection or balancing. Source roster audits have no Origins/Apoli entry; verify current build but do not remove unrelated libraries or introduce a substitute class system. See `V050_ORIGINS_EXCLUSION_20261013.md`.

## Design source order
1. `docs/balance/V050_BOSS_ROSTER_AND_GATES_PROVISIONAL.md` and `V050_BOSS_ROSTER_PROVISIONAL.csv`
2. `docs/balance/V050_LOOT_GEAR_ECONOMY_PROVISIONAL.md`
3. `docs/questing/V050_QUEST_CAMPAIGN_BLUEPRINT_PROVISIONAL.md` and `V050_QUEST_BEATS_PROVISIONAL.csv`
4. `docs/balance/V050_ENCOUNTER_MULTIPLAYER_REPLAYABILITY_PROVISIONAL.md`
5. `docs/balance/V050_OWNER_DECISION_REGISTER.csv` for **explicit pending/provisional** choices
6. Existing v3.1 catalogue `docs/balance/AO_STRUCTURE_TIER_CATALOGUE_V3_2026-10-13.csv` and earlier boss editability evidence.

**No code, source release-lock, quest data, server config, third-party mod or game asset is changed by the v0.5 research branch.** The above files are additive.

## Priority 0 — reconcile live state (before touching game)
- [ ] Identify actual latest stable consolidated pack. Repository `AGENTS.md` identifies **v0484 r19**, 329 CF pins, **52 Questlog quests / 13 chapters**, 32 FTB field-manual pages; newer branch may supersede, so use current pinned import and actual client/server mods list, not default `main`.
- [ ] Inspect experimental native `ao-balance-lab` code and current Work-mode branch; avoid racing edits on the same Paxi, Dungeon Difficulty or Questlog files.
- [ ] Validate mod identities and exact boss spawn/arena IDs; **Bosses' Rise ≠ Block Factory's Bosses**.
- [ ] Confirm target **Remnant Bosses 2.7.0** and rebuild source config schema if needed; issue #43.
- [ ] Resolve three special audit claims separately: Maledictus in `cataclysm:frosted_prison`; Scylla in `cataclysm:acropolis`; Leviathan in `cataclysm:sunken_city`.
- [ ] Preserve `main`, known-good r19 zip, `structure/test6`, performance branch and port working commits. New implementation branch only.

## Priority 1 — design-to-code first slice (small and reversible)
**Slice A — midgame T5 route**
- [ ] Validate BOMD Lich and Void Blossom entity, spawn trigger and rarity. Confirm each is feasible for solo T5.
- [ ] Implement **two alternate T5 story milestones** (not mandatory both) using verified Questlog objectives or owner-authored advancement hook. No invented item ID, no forced 5-player party.
- [ ] Reward only a modest first-clear trophy / guide note. Native thematic drops unchanged initially.
- [ ] Capture party credit, restart and duplicate reward test.

**Slice B — T6 Pinnacle gate**
- [ ] Verify Iron's Dead King can represent stronger Tier 6 and find a second **comparable** T6 boss alternative. If no source-backed second route exists, **leave gate pending** rather than enforce a single inaccessible boss.
- [ ] Prototype per-player `pinnacle_unlocked` milestone state (data format only after Questlog save mechanics inspected); ensure old saves and new players migrate safely.
- [ ] Verify actual Ancient / Artifact grade data components in updated Apotheotic port before enabling rewards. The design grants T6 *boss-only* Artifact while Pinnacle unlocks Ancient-standard access.
- [ ] No cross-player progression auto-unlock unless explicitly built as optional party-sharing with proper credit.

**Slice C — two representative structure-loot tests**
- [ ] Pick one **T3 named dungeon** and one **T5 Bastion/major dungeon** whose source chest tables are proven and whose current JAR is present.
- [ ] Author preservation-first native loot wrappers/overrides for **Supply vs Treasure** chest classes without giving boss-exclusive high-grade gems.
- [ ] Keep **T0–T2 and early Mine Cells loot untouched**.
- [ ] Verify Lootr per-player open/reload, deterministic repeat test and no duplicate roll with Apotheosis global modifiers.
- [ ] If the chest source is too generic or shared across tiers, don't override globally; tag the exact structure/piece or isolate another sample.

## Priority 2 — campaign publishing
- [ ] Map the 101 v0.5 design seeds to existing **real 52 quest IDs**; do not overwrite a working same-name objective. Keep source id → design beat relationship explicit.
- [ ] Implement a small quest batch: 1 T3 optional arena discovery, 1 T5 two-option boss milestone, 1 Tier 6 preparation step. Respect gameplay proven triggers and FTB manual links.
- [ ] Keep nine main storyline chapters; T9 only an optional epilogue. The final held-item Heirloom upgrade is **a design requirement**, pending safe transactional tool support.
- [ ] Verify 12-of-16 End Remastered eye rule against exact active config; no forced collection of 16.
- [ ] Optional Pasterdream/TF/Aether dimension arcs are chapter outlines only until source IDs, versions and quest detection are audited.

## Priority 3 — boss tuning and replayability
- [ ] Run individual boss attribute + special-attack probes on **Cataclysm**, **Remnant 2.7.0**, **F.D. Bosses**, **Bosses’ Rise**, **Archaion**, **Iron's**. Do not conflate changed HP with changed spell/projectile/phase damage.
- [ ] Test native difficulty multipliers before adding any player count multiplier; identify which boss mods already scale and which may have hit counters or DPS caps.
- [ ] Optional trial multipliers in design doc only: 0.35× extra HP per nearby participant (cap 5), 0.08× attack (cap 5), and waves 0.20× (cap 4). **Never apply simultaneously without an explicit approved per-boss stacking model.**
- [ ] Validate boss reset on wipe / regen / logout; reward cooldown and farming.
- [ ] Only expand to all 386 named active structure candidates after verified per-structure gameplay path and targeted performance tests.

## Priority 4 — measurable balance loop
- [ ] Three sample kits per tier: shield/melee, bow/mobility, magic; choose real comparable gear supported by current mod binaries.
- [ ] Capture time-to-kill, deaths, consumables, expected clear reward, boss attack-specific damage, difficulty/affix stacking, AI spawner limits, dedicated server MSPT and shader-client FPS.
- [ ] Test solo, 2 players and 5–7 players. Keep mainline solo-feasible.
- [ ] Re-check T5–T6 and Tier 9 endgame after real data rather than relying on provisional quest design numbers.
- [ ] Produce CSV audit results and changelog; tag each claim `design_only`, `source_verified`, `static_pass`, `client_runtime_pass`, `server_runtime_pass` or `multiplayer_pass`.

## User-return decision agenda (avoid interrupting authoring)
The owner has explicitly allowed provisional choices. Work may use placeholders for all nonessential choices, **but may not silently publish those placeholders as settled gameplay**.
- Strong Tier 6 alternate boss; third Tier 9 End superboss; Geburah tier.
- Whether Bosses' Rise five fights are all equally difficult after testing.
- Trial gem scarcity, Goblin-Tuned economy changes, party sharing and PvP concerns.
- Whether the older Ignis/Leviathan T8 notion merits revisiting; most recent Tier 7 grouping is the working reference.

## Done condition
Deliver one separated experimental overlay and exact diff, manifest/JAR identity ledger, static check outputs, versioned quest mapping, duplicate-safe loot rule evidence, specific runtime checklist, and a concise list of owner decisions. **Do not claim game implementation on this design branch.**
