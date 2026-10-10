# Ambient Odyssey — Exploration Discovery, Titles and Journal Proposal

**Proposed:** 10 October 2026. **Target:** Minecraft 1.21.1 / NeoForge 21.1.252. **Status:** RESEARCH / DESIGN ONLY. No new mod JARs, manifest pins, resource-pack changes, datapacks or runtime tests were made. This belongs to a **later QoL / progression wave**, after Test8.3 and worldgen acceptance.

## User objectives

- Show polished biome and dimension names on entry, and major structure/dungeon names upon first visit.
- Record discoveries **silently and persistently, per player**, in normal survival; provide a checklist/progress percentages and filtering for visited vs not-yet-seen.
- Avoid biome-border notification spam and excessive HUD clutter.
- Make exploration intrinsically rewarding for 5–7 players and later bridge to the public Ambient Odyssey progression/wiki site.
- Consider extra optional exploration QoL, avoiding duplicate overlays already provided by Xaero/FTB Quests/other installed mods.

## Current candidate mods / technical evidence

| Component | Candidate | Status / caveats |
|---|---|---|
| Biome/dimension titles | **Traveler's Titles (NeoForge)** | Dedicated 1.21.1 NeoForge project (CF `1015155`, YUNGNICKYOUNG); v5.1.3 verified on project page. Biome + dimension title styling, modded biome support, optional sounds/blacklist/Waystones. Candidate only. https://www.curseforge.com/minecraft/mc-mods/travelers-titles-neoforge |
| Structure entry titles | **First Steps** | Advertises structure titles and out-of-box naming for Dungeons & Taverns, Repurposed Structures, Additional Structures, Structory, Moog's etc. Project aggregate lists NeoForge and 1.21.x, BUT **an exact 1.21.1 NeoForge file was not yet verified**; published supported-environment metadata are partly contradictory. Confirm an actual exact loader file and multiplayer test before adding. https://modrinth.com/mod/first-step-mod |
| Structure ID debugging | **WITS (What Is This Structure?)** | Server-side 1.21.1 NeoForge `909375:8412915` explicitly verified; `/wits` reports at-position structure identities. *Not* an automatic title or journal. Useful as dev/test aid to reconcile AO aliases/clones and false structure names, not necessarily player-facing. https://www.curseforge.com/minecraft/mc-mods/wits/files/8412915 |
| Full discovery journal | **Explorer's Journals** (KayDev) | NeoForge 1.21.1 `1720282`, initial 1.0.0 release Oct 2026 claims registry-derived biomes, structures, dimensions, mobs, ores, discovery statistics and individual multiplayer data. **Extremely new/low adoption and unverified**; sandbox prototype in a copied test instance only. Investigate data model, total denominator, false positives, structure-only coverage, GUI/FPS/TPS, world safety and save migration. https://www.curseforge.com/minecraft/mc-mods/explorers-journals |
| Fabric journal alternative | **Codex: Discoveries** | Fabric 1.21.1 only, source lists Fabric API, so not an automatic NeoForge addition; may be an inspiration only. https://www.curseforge.com/minecraft/mc-mods/codex-discoveries |
| Existing reliable substrate | **FTB Quests 1.21.1** | Official docs confirm built-in **Visit Biome**, **Find Structure**, and **Advancement** quest tasks: https://docs.feed-the-beast.com/mod-docs/mods/suite/Quests/Developer/Quests/Types/ . Test actual tracking and per-player completion with currently staged FTB Solo Quests; do not assume team settings work until verified. |
| Custom persistence substrate | **Vanilla data-pack advancements** | 1.21.1 official vanilla `minecraft:location` predicate already tracks entering structure IDs (see `minecraft:end/find_end_city`); can make displayless one-time per-player flags and optionally invoke reward functions/scoreboards. Biome predicates analogous. Requires generated fixed IDs, tests, careful version migrations and denominators; not a fully dynamic mod registry scan. https://mcasset.cloud/1.21.1/data/minecraft/advancement/end/find_end_city.json |

**Do not stack two systems displaying identical biome titles or keep multiple progression journals recording the same events without a clear data-owner decision.**

## Proposed information architecture: AO Explorer's Journal

A. **Biomes visited:** unique biome registry type seen in permitted/active dimensions; **current curated roster + actual installed vanilla/modded**. Include biome unique IDs instead of display text for stable saving. Do not equate "40 intended Overworld donor biomes and 2 Nether donors" with total available biome count — these are curated donor counts, not all possible biomes.

B. **Structure discovered:** entering or reaching a registered, *enabled and reachable* major dungeon/landmark structure. Store the **structure registry ID** and, optionally, first-encounter dimension/coordinates/time. Label aliases and AO clones correctly. Structure-type discovery and physical-instance visitation are two DIFFERENT counters. Do not enumerate all 1,219 catalog rows as a denominator by default; many are variants, clones, duplicates, disabled, inaccessible or small decorative structures.

C. **Dungeon cleared:** separately earned by meaningful evidence (boss kill, configured objective, reward-room activation, or curated FTB Quest). Merely entering a boundary is *not* proof of clearing. Many decorative structures have no meaningful clear condition; mark not applicable.

D. **Dimensions entered:** discrete milestones.

E. **Optional categories:** bosses defeated, rare creatures observed, discoveries documented, rare loot/artifacts secured, secrets, research/photo entries.

**Player data:** per-player persistent progression must survive relog and world restarts; retain stable resource IDs and versioned migrations if content categories expand. Multiplayer global discoveries are optional and must NOT silently complete personal exploration. Test backup/restore and 2-player differences. Avoid auto-uploading player UUIDs/location history to a public website.

## Percentage policy

- Show **category-specific percentages** and a *core exploration* total, not a single misleading denominator. Example: `Biomes 47/92`, `Major structures 28/74`, `Dimensions 4/7`. These counts are illustrative only — derive actual denominators from the final frozen registry and verified reachable sets.
- Use a stable **core checklist** (realistically achievable) and a separate optional **rare/legendary discoveries** category. Optional extremely rare variants must not make 100% progress impractical or dynamically lower the score after an unrelated mod change without a version notice.
- Breakdown by dimension/mod and class (ruins, dungeon, village, landmark, ocean), with filter `undiscovered only`, spoiler-safe unknown labels `???` by default.
- Show world vs pack version in the UI; avoid treating the count of registered dungeon templates/pools as structure count.

## Title/UI behavior

- **Dimensions:** large ceremonial title on *first entry*, optional subdued variant on later dimension travel.
- **Biomes:** compact/subtle subtitle; debounce ~15–45 seconds and only alert for meaningful transition, not repeated border crossings. Configurable always / first visit only / off.
- **Major structure / dungeon:** distinct title with optional short sound, **first-time per structure type or discovered instance**; configurable based on user preference. Set title precedence `major structure > dimension > biome` and queue/coalesce overlapping notifications.
- **Minor buildings:** no automatic dramatic title; log if meaningful without pop-up.
- **Accessibility:** scale, opacity, sound, mute, notification duration, hide entirely, shader/HUD overlap test.
- **Discovery toast text:** `New discovery: [Name]`, and optionally category progress (e.g. `23 / 85`). No global chat flood, spoilers or forced automatic Xaero waypoints by default.

## Implementation options (ordered by initial cost)

1. **Minimal prototype using what AO already installs:** FTB Quests with two **Visit Biome** tasks and two **Find Structure** tasks (one vanilla + one modded each), plus staged FTB Solo Quests. Verify tasks complete quietly, survive logout, remain independent between players, and only trigger on actual discoveries. Build a compact optional Explorer chapter, with milestones. Native FTB Quests chapter progress UI may suffice before building our own mod.
2. **Vanilla datapack generated by Python from approved AO registry:** one displayless `data/ambient_odyssey/advancement/explore/...` per selected biome/structure, `minecraft:location` with exact player predicates; optional reward `function` to increment per-player scoreboard only once; test reconnect, re-grant, upgrades and migration. No server mod necessary. Structure IDs must refer to real effective registry, no wishful names. Direct custom UI/per-type counts require commands/FTB integration or a lightweight client mod.
3. **Existing Explorer's Journals prototype:** compare its native discovery engine and UI against FTB/datapack reference in an isolated instance; prefer only if accurate and maintains per-player data at modest overhead.
4. **Purpose-built AO Explorer mod / public site extension (later):** server-authoritative event-driven registry discovery, true per-player history, visit locations, encounter tags, custom journal UI and optional export. Not needed until prototype establishes why datapack/FTB is insufficient. Public atlas could show static coverage and guides; user progress syncing requires explicit opt-in and privacy design.

### Small prototype / objective gates

- Use a **copy** of the Test8.2 working profile; do not edit active Test8.3 until worldgen accepted. Select `minecraft:plains`, one known current modded surface biome, one vanilla structure, and one real modded dungeon from the effective registered IDs. Verify structure IDs using WITS / `/locate` / in-game debug where appropriate; `/locate` alone is *not* natural discovery.
- Two different players, fresh save and previously used world. Walk across short adjacent-biome boundaries, enter structures and move to adjacent jigsaw pieces. Check title spam, first-discovery vs repeated visit, dimension crossings, death/relog, world save and game restart.
- Verify FTB Quest per-player independence with FTB Solo Quests on server; check whether “find” means nearby, inside bounding box or another condition.
- Audit disabled structures, cloned structure IDs, content added later, hidden End/Nether structures, rare ocean structures and nonregistered/code-spawned landmarks.
- Measure title rendering, logger warnings and CPU/tick impact in 5–7-player scenario; make no claim of zero performance overhead.
- If advanced enough, export a compact `exploration-registry.json` to the wiki from the same validated authoring source; do **not** expose player progress by default.

## Additional exploration QoL suggestions (research only)

- **Expedition log / recent discoveries:** location/time of first entrance, with biome/structure note and optionally a single manual screenshot; avoid duplicating Xaero map features.
- **One-click revisit/bookmark:** optional marking of major *already discovered* structures on Xaero; no free unexplored coordinates or globally revealed POIs. Respect server maps and spoilers.
- **Milestone ranks:** Cartographer → Pathfinder → Wayfinder → Explorer → Master Explorer; cosmetic titles for 10/25/50/75/100% in chosen category, not strong combat rewards.
- **Party vs personal exploration:** personal discovery stays personal. Optional private party comparison without shared expedition planning or first-on-server/first-explorer honors; avoid notifications or automatic team completion.
- **Documented rarity:** rare discoveries show small flavor text or lore after discovery; mysterious names hidden until seen.
- **Expedition preparation:** optional travel supplies, biome dangers and waypoint reminders, linking later to gear tier/boss planner without spoilering loot before the first visit.
- **Environmental photo album:** purely opt-in later; no default local screenshot collection/upload.
- **Explore by biome family / dimension:** meaningful grouped checklists rather than hundreds of unfiltered rows.
- **Return route safety:** sensible markers for portals, major waystones and death coordinates if Xaero settings do not already cover them; avoid adding overlapping map mods.
- **Explorer's achievements:** personal/collective milestone panels and curated rare discoveries, but do not turn mundane biome hopping into a required quest grind.

## Decision status

- **User proposed exploration titles + background discovery checklist; concept supported.** Exact mods/datapack/UI **not selected or approved**. Research and test in separate QoL wave. Preserve worldgen freeze priority.
- **Engineering recommendation:** start with **Traveler's Titles + native FTB Quests prototype**, then assess **First Steps** exact compatible JAR and **Explorer's Journals** as a comparator. Only build full bespoke journal if required after functional test.


---

## Approved concept inventory — user confirmation, 10 October 2026

**Decision:** User approved *every feature from the prior exploration conversation* for the upcoming expansion backlog. These are approved **design goals**, not approved exact mods, untested datapacks, or release changes. Do not modify the working Test8.2/Test8.3 pack yet.

| Prior feature | Status | Notes |
|---|---|---|
| Entering biome and dimension titles | Approved concept | Modded names, subtle repeat transitions, dramatic first dimension |
| Named major structure and dungeon titles | Approved concept | First-discovery hero titles, avoid border spam |
| Silent persistent per-player discovery tracking | Approved concept | Biomes, structures and dimensions, across reloads |
| Searchable explorer journal and checklists | Approved concept | Discovered/unknown filters, progress breakdown by dimension/category |
| Biome, structure, dungeon and dimension percentages | Approved concept | Eligible reachable denominator; optional legendary milestones separate |
| Structure found versus dungeon cleared | Approved concept | Avoid equating dungeon discovery with boss defeat |
| Explorer ranks and cosmetic rewards | Approved concept | Cartographer/Pathfinder/Wayfinder etc, not power-gating |
| Expedition diary, first visits, recaps | Approved concept | History of noteworthy discoveries; local/private player data |
| Bookmarks and known-location waypoints | Approved concept | Only previously visited, avoid duplicating Xaero map |
| Rare discoveries, lore and secret entries | Approved concept | Hidden labels until found, optional specials outside mandatory 100% |
| Personal and optional party exploration history | Approved concept, limited | Keep individual saves and optional party comparisons; **exclude world-first leaderboards, memorials, halls of fame, or first-on-server attribution** per latest user choice |
| Grouped biome/dimension/family explorer goals | Approved concept | Practical collections, no impossible completion |
| Environmental screenshot album | Approved concept | Opt-in photo journal, no automated uploads |
| Expedition preparation and safe return reminders | Approved concept | Gear/hazard hints, Waystones, portals and death-route notes |
| Public wiki/Atlas integration | Approved concept | Per-location wiki, boss tier, gear readiness; export opt-in |
| Optional creatures/resources discovery index | Approved concept | Check usefulness and data accuracy against Explorer's Journals |
| Accessible title/sound and notification settings | Approved concept | Toggle, cooldown, scaling, screen overlap, sounds |

**Tracking implementations still undecided:** Native FTB Quests Visit Biome / Find Structure proof of concept, Traveler's Titles, structure titles via compatible First Steps if possible, new Explorer's Journals mod, silent advancement datapack or custom mod if necessary. These must pass a two-player persistence/runtime test and not delay worldgen freeze.

## Next round of exploration ideas — brainstorm candidates, not user-approved installs

| Idea | Estimated effort | Why it might be excellent | Important design or balance constraint |
|---|---|---|---|
| **Explorer's Guild and expedition contracts** | Medium–high | Optional guild board with hints to discover climate zones, ruins, oceans, towers; cosmetic ranks and quest chains | No mandatory grind, quests should not reveal precise coords |
| **Rumors, treasure maps and clue chains** | Medium–high | Books, rumors, cartographers or shipwreck clues guide expeditions to particular region/structure families | Actual reachable structures and clue pool verified against frozen AO generation |
| **Natural wonders / scenic viewpoints** | High | Not every memorable place is a generated structure: enormous mountains, caverns, ocean cliffs and breathtaking views | Terrain features often lack a structure ID; start curated or manually documented, do not pretend fully automatic |
| **Discovered → Conquered → Mastered** | Medium–high | Separate discovery, main encounter completion, and optional secrets for major dungeons | Use boss/quest evidence, not structure-entry alone; don't force mastery |
| **Regional collections and explorer badges** | Medium | Oceanographer, Alpine Surveyor, Cavern Cartographer; discover themed landmark groups | Check 100% feasibility; no artificial per-biome grind |
| **Field guide / ecology encyclopedia** | Medium | Reveal mob habitats, hazards, unique resources and biome lore only after seeing them | Version-accurate facts and discover-only spoilers |
| **Boss danger reconnaissance** | Medium | Once you find a major location, see AO boss tier and broad gear-preparation hints linked to Gear Atlas | Tier is a balancing target, not proof of guaranteed victory; optional spoilers |
| **Group expedition planner** | Medium | Party rendezvous, shared objective list, supplies, and optional one-click route export | Coordinate sharing opt-in; independent discovery progress |
| **Explorer trophy cabinet / museum** | Medium–high | Cosmetic trophies and framed souvenirs from exceptional discoveries, a common hall for 5–7 players | Prefer visual/story rewards over stat power or excessive extra items |
| **Lost-expedition notes / linked lore puzzles** | High | Shipwreck notes and ruin inscriptions hint at bigger mysteries spanning dimensions and regions | Curated actual locations and readable story; avoid nonexistent worlds/links |
| **Conditional Explorer's Compass** | Low–medium | Official 1.21.1 NeoForge structure locator could be a late-game clue/search tool | AO already pins Nature's Compass 252848:7892954 but NOT Explorer's Compass. Official compatible Explorer's Compass 491794:7892943 supports cost/durability and blacklists. Limit boss/rare targets or skip to preserve discovery; https://www.curseforge.com/minecraft/mc-mods/explorers-compass/files/7892943 |
| **Optional personal atlas export** | Medium–high | Portable player checklist for manual import into our website with per-item pages and guides | No automatic upload of UUID, coordinates, seed or other private data |
| **World-first memorial hall** | Medium | Low-noise opt-in plaques and first discoverer record, shared server legends | Do not spam global chat or steal personal achievement independence |
| **Location-tiered return markers** | Medium | Discovered-only journal to Xaero waypoint action, icons by rarity / category | Don't install redundant maps, don't reveal unseen coordinates |
| **Expedition condition report** | Low–medium | Optional party gear, known biome hazards, travel supplies and portal/waystone checklist before trips | Simple manual checklist before any unreliable auto-analysis |

### Suggested sequencing
1. **Discovery baseline:** titles, silent personal tracking, checklists, accessible toasts, bookmarks and ranks.
2. **Meaningful expeditions:** guild board, rumors, tier reconnaissance, journal diary and grouped collections.
3. **Long-term bespoke systems:** scenic wonders, full conquer/master detection and privacy-conscious player atlas export. **No exploration museum, linked lost-expedition narratives, shared expedition planner or world-first records.**

### Already-installed versus candidate location tools
- Nature's Compass: already pinned in the current source release lock, file 252848:7892954 (1.21.1 NeoForge), can find biomes but is not a discovery journal.
- Explorer's Compass: NOT pinned; 1.21.1 NeoForge file 491794:7892943 exists, can locate modded structures. Use only after deciding if searching for undiscovered major dungeons would undermine AO's intended exploration.

**Status:** previous exploration suggestions approved as backlog concepts by user. Newly brainstormed enhancements have been selectively approved: ideas 1–7 and 12 retained; ideas 8–11 declined, see follow-up selection below. No modpack JARs, releases, configs or tests modified in this documentation change.

---

## Follow-up selection — keep ideas 1–7 and 12; reject ideas 8–11 (10 Oct 2026)

**Latest explicit decision supersedes prior broad approval where relevant.** User likes all the numbered ideas from the two brainstorm replies **except #8, #9, #10, #11**. These numbers refer to the most recent numbered list of 5–12 and the preceding numbered list of 1–4.

### Keep — now approved exploration design concepts

1. **Explorer's Guild and Expedition Contracts** — optional exploration prompts, reputation and cosmetic progression.
2. **Rumors, treasure charts and navigational clue chains** — exploration clues and directions; **not** scripted lost-expedition story arcs.
3. **Scenic Wonders and natural landmark documentation** — curated/opt-in natural discovery rather than false auto-generated named features.
4. **Discovered → Conquered → Mastered** — accurate distinct dungeon milestones; optional mastery.
5. **Biome Field Guide** — biome-specific discoveries, ecology, mobs/resources/hazards.
6. **Dungeon Danger Reconnaissance** — show provisional AO boss tier and appropriate gear band after discovering a site.
7. **Regional Exploration Collections** — themed biome/structure badges and achievable sets.
12. **Personal Atlas Export** — optional export to the public AO website without personal information leaking by default.

### Exclude — intentionally not planned

8. **Exploration Museum / trophy cabinet** — no physical museum/trophy-display system.
9. **Lost Expedition Stories** — no extended, linked expedition-narrative/lore-puzzle system. Short location flavor, optional secrets and navigational rumors in #2 are still approved.
10. **Party Expedition Planner** — no bespoke group route planner or shared supply/itinerary UI. Ordinary multiplayer exploration and personal-vs-party progress distinction remain.
11. **World-First Discovery Records** — no first-discoverer leaderboard, global memorial, hall of fame or automatic server-first attribution. Personal first-visit timestamps and discovery history remain.

**Do not reintroduce excluded items automatically during quests, FTB/FTB Teams design, journal GUI, decorative structures or public wiki planning.** Previously proposed `first-on-server` honors are superseded by this exclusion, while the previously approved optional *personal* first-visit journal persists.

**Non-numbered ideas** such as optional Explorer's Compass, safe-return markers and low-friction expedition preparation remain in the audit subject to balancing and technical checks.

**Implementation status:** all kept entries are approved *concepts only*. No exact mods/JARs, commands, datapacks or release changes are approved or installed through this decision.
