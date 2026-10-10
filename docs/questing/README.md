# Questing in Ambient Odyssey

**Working source:** [Q1 50 Questlog quest definitions](QUESTLOG_Q1_INSTALLED_INDEX.json), with the separate [FTB Manual 32-page index](FTB_MANUAL_IMPLEMENTED_INDEX.json). Current source baseline is `experimental/v0.4h-q1-ftb-field-manual-20261010`. Static packaging validated; actual game/runtime UI still pending.

Browse the [offline Quest Atlas website](../../site/quests.html) or [website documentation](../../site/README.md) to inspect the same 50 Questlog definitions outside Minecraft. The site is source-generated and does not track actual player progression.

## The two books

- **Questlog Adventure Journal (3.4.1):** 50 initial, mostly optional exploration and instructional entries across 13 chapters. Exact JSON source under `release_030/overrides/config/questlog/`. See [implementation](QUESTLOG_Q1_IMPLEMENTATION.md), [admin editing](QUESTLOG_ADMIN_GUIDE.md), [runtime test matrix](QUESTLOG_Q1_RUNTIME_TESTS.md).
- **FTB Field Manual:** 32 reward-free, task-free reference pages across three chapters (Systems, Tips & Tricks, Controls). Existing **When Dungeons Arise** FTB questline remains intact. See [FTB manual implementation](FTB_MANUAL_Q1_IMPLEMENTATION.md).
- **Q2 and beyond:** planned progression and adventures use [Campaign Architecture](QUEST_CAMPAIGN_ARCHITECTURE.md), [quest content seeds](QUEST_CONTENT_SEEDS.csv) and [verified/future mod coverage](MOD_QUEST_COVERAGE_MATRIX.csv). These are **backlogs**, not hidden installed quest files.

## Authoring and testing

```bash
python tools/validate_v04_quest_campaign.py
python tools/validate_v04_ftb_manual.py
python tools/validate_v04_questlog.py
```

Source-backed vanilla triggers only in Q1; deeper boss and dimension adventures need real installed registry IDs, progression checks and testing. Don't force one Origin, cursed ring, RNG landmark, weapon category or modded class. Only one quest engine pays each milestone reward.

Previous research, depth reports, 50 original prose drafts, tips and long-form field notes remain in this folder. The previous README is preserved at [historical questing README](../archive/history/QUESTING_README_pre_organization_2026-10-10.md).
