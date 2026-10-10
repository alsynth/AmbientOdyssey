# Ambient Odyssey — Roadmap & Quest Atlas

This is the next iteration of the **8 October 2026 offline Ambient Odyssey Development Roadmap**. The original roadmap's phases, retrospective notes, and browser-local checkmarks are preserved in `index.html`. `quests.html` adds the first Quest Atlas.

## Open offline

1. Extract **all files** from the website ZIP to one folder, preserving `assets/`.
2. Double-click `index.html` for the original roadmap or `quests.html` for questlines. Both pages work without a server or network connection.
3. Choose a chapter, search quests, and click an entry to read objectives, prerequisites, rewards, and original field notes.
4. To send someone a particular quest link, use the optional `?quest=<quest-id>` query string **on an actual web host**; local file links may behave differently between browsers.

**Not a player progress dashboard.** It does not read saves or contact a Minecraft server. The roadmap's checkboxes only save on that browser/device. Quest Atlas tracks **authored definitions**, not runtime completion or whether a boss was actually defeated. Chapter intros and read objectives are intentionally labelled as experiments.

## One source of truth

All quest text, task definitions, rewards and prerequisites come from the pack itself:

```
release_030/overrides/config/questlog/quests/*.json
release_030/overrides/config/questlog/chapters/*.json
```

Regenerate after **any** quest edits (with Python 3.10+):

```bash
python tools/export_quest_atlas.py
python tools/export_quest_atlas.py --check
python tools/build_quest_atlas_site.py
```

`site/quest-data.js` is generated specifically for `file://` compatibility; using `fetch("quest-data.json")` would break opening HTML directly from a local disk in some browsers. The companion `quest-data.json` is a public/static machine-readable export. These files **do not contain player data** and must not be edited manually.

## Roadmap for adding content

- **Q1:** 50 existing Questlog quests in 13 chapters, fully browseable online/offline, search and filter.
- **Q2:** Native modded gameplay chains for Mine Cells, Twilight Forest, Aether, Cataclysm and equipment once actual item/advancement/entity registry identifiers are verified.
- **Guide expansion:** Add separate pages for the 32 existing in-game FTB Manual reference articles, boss dossiers, keybinds and gear; keep their source text authoritative.
- **Optional future:** If the website gets hosted, add stable quest URLs and maybe spoiler toggles. Do not imply cross-player progression sync without actual server integration.

## Hosting status

No live Ambient Odyssey domain, GitHub Pages publication or deployed server is configured by these files. This folder is **static site source** and the CI artifact is an offline website ZIP. Site deployment should be set up separately, with public/private content rules reviewed first.

## Tests

`python -m unittest discover -s tests -p test_quest_atlas_site.py` and `node --check site/assets/quest-atlas.js`. The GitHub workflow checks the exported site against the live modpack's source definitions and publishes a ZIP. Browser/UX testing on actual devices is still pending.
