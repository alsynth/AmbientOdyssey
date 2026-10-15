# Master integration — private experimental candidate, 15 October 2026

This branch assembles the exact PR50 import with compatible PR51/53/54/57 content, PR59 Brutal Bosses, the verified-scope portion of PR62, and the latest owner decisions. It does not merge into main or install into an existing player profile. Worldgen is **NOT frozen**. The full request is **partially completed**: several native routes and the broader loot/DD rollout remain gated below.

## Source and package changes

- Remove Demi's Sky Arena from the final manifest, copied runtime inventory, four configs and density compiler inputs. Keep unrelated Sky Whale Ship content.
- Brutal Bosses: 70 eligible-chest chance, distance 30, HP ×4, damage ×3. Individual boss JSONs, spawn tables and dummyboss unchanged.
- DD: 23 scoped Overworld zones; T2–6 budgets +100/150/200/250/300% HP, +40/60/80/100/200% attack, +3/5/8/11/15 armor. Foundry T6; Dungeon Crawl T3. Philip's level-three ruins follows owner category-default T2. No Tier0/1 zones, Mechanical Nest blanket zone, Pasterdream or dimension-wide buffs. Frosted Prison/Sunken City held because their separate structure tiers remain provisional. Existing Catacombs T4 retained from pilot; its individual review is not newly approved.
- 51 native boss config field changes across Cataclysm, BOMD, Block Factory/Bosses'Rise, Remnant, Iron's and Ice & Fire Hydra. Native HP cap accepted, uncapped targets retained in the field ledger. No promise that ordinary attack keys change fixed abilities. Shared dragon species settings, FD hit counts/abilities, participant scaling, soul mode and respawn settings preserved.
- Dead King remains T6 for rewards, with native T7 combat targets. Cornelia remains T6 for rewards and has the same T7 combat target, **but no verified native route implements it**. No competing generic scaler was added.
- Chesed/Malkuth/Geburah: T5 milestone classification; their stats are entirely untouched. Ignis/Maledictus/Leviathan T8; Obsidilith/Tyros/Scylla T9. R3/R4 namespace and Obsidilith corrections recovered from the earlier local checkout; current source is committed separately.
- Starter addon 0.2.0 uses the PR51 owner correction: bonuses append to vanilla loot; no replacement Bonus Chest table. One of five genuine installed spellstones, real Common55/Uncommon30/Rare15 affixed item, torches and cooked meat. Lootr whitelist and exact-table Apotheosis exemptions retained. Two-player conversion/independence is still manual.
- Sigils 0.1.1 retain 6/18/24/32 reroll and 12/36/48/64 upgrade costs; native low rarities and gem gates unchanged. Goblin costs and Flight Ring recipes retained. Campaign 0.2.0 retains original 52 quests/13 chapters plus 101 journal entries/7 chapters and 32 manual pages. 83 additions are reading acknowledgements, not fight objectives.
- Unapproved Rage Glove 10% Monstrosity route is unregistered; native acquisition remains. Its research class is retained but inactive. No new elite gatekeeper subset.

## Evidence and provenance

`pr-audit.json` and `pr-metadata.json` identify the exact 20 significant draft heads plus the older drafts required by the handoff. Research data is not automatically gameplay configuration. `native-balance-ledger.json` records each changed field; `dd-effective-zones.json` records scope and holds. Final package receipt records every member SHA256, custom JAR SHA256 and complete changes from exact PR50.

The original `NEXT_AGENT_PACKAGE.zip` was found in Downloads: archive SHA256 `4ec40d32b9d919d5bec5c6d505f5efadd674197171a33f6248546f742a32c550`. All 00–21 documents/tools and 39 rollback configs are imported under `docs/research/next-agent-package-20261014`. All 39 supplied checksums verify; 35 match repository-original content after newline normalization, three DD metadata files are absent from the original source and the DD config differs. The original snapshot is preserved byte-for-byte. Its old Geburah, Brutal Bosses and roster text is superseded by the master handoff.

Local historical R4 exists but is unpublished; GitHub release has R1–R3. Neither proves the owner's active install. No live profile, server or save was modified. Optional Wet Sand and Apotheotic port artifacts are inherited byte-exact from the hash-pinned base, not rebuilt or claimed newly compatible.

## Remaining blockers

1. Cornelia/Last of Deepslate and other bosses without native stat routes need the separate owner addon or a verified per-boss native hook. Hydra has only a health key; ordinary damage remains unimplemented. Lich exposes missile damage rather than an ordinary attack key. Coralssus lacks a mapped combat section. Harbinger/Mechanical Nest exact tier/identity remain unresolved. Do not assign unnamed bosses or blanket-buff species/minions.
2. Eternal Starlight family selection is still TBD in the imported owner package: preserve its native stats and respawn. T2–4 boss targets remain planned where no exact approved entity/route is established. T5 ordinary BOMD config work is implemented; FD exceptions preserved.
3. The 497-row DD plan is a review queue. Registry existence alone does not prove dimension eligibility, natural reachability, owner approval or Paxi precedence for every candidate. No mass injection was made.
4. Five-class structure/container mapping and encounter-specific rare affix distributions remain planned. The imported package explicitly leaves reward pacing/expected kills undecided. No invented drop percentages, universal vanilla-table replacement or broad high-rarity injection was shipped. Existing first-clear grade rewards remain experimental; farm fairness, party contribution and retry after failed reward delivery need follow-up.
5. Real normal-FTF natural arenas, generation-placed spawners/loot/Lootr, dedicated server, 2-player persistence/credit, special damage, capped HP after real encounter setup, respawn/summoning, shaders/performance and staged Chunky acceptance remain open. Synthetic flat-world tests do not close these gates.
6. Quest Atlas, custom main menu, optional realm campaigns and player build benchmarks remain deferred as authorized. Origins, Ocean Loot, MCA Reborn, Big Globe and Mob Plaque are not introduced.

## Verification labels

Use the final accompanying verification report for exact tested ZIP/hash. Native addon GameTests, integrated startup, actual-registry queries and synthetic entity fixtures are distinct evidence. None establishes a natural boss fight, dedicated multiplayer acceptance, OWNER ACCEPTED or LIVE INSTALLED. Initial RC2 observations are historical once the final additive starter/Tyros/Hydra/DD corrections are packaged.

## Rollback

Import as a NEW CurseForge profile. Preserve the working client/server folders and make a cold backup of the entire save, including serverconfig, playerdata, advancements and quest/team data. Keep exact PR50 and the currently installed known-good ZIP untouched.

For full rollback, stop the experimental client/server and return to the original profile plus its **pre-test save backup**. Never load a world generated with removed content in an older profile as a substitute for restoration. The generated rollback ZIP contains byte-exact PR50 payloads for every replaced/removed member and a receipt listing added paths to remove; it is not a modpack to import and must not be blindly extracted over a live profile. The separate 39-config research baseline may describe an older local profile and is not a universal rollback for the current experiment. SERVER configs in existing worlds must be restored in the world's serverconfig as well as defaultconfigs. Never overwrite historical releases, rollback branches or Tan's locked archive.
