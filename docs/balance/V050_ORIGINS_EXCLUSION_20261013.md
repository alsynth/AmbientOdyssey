# Ambient Odyssey — Origins removal / exclusion decision
**Binding user decision · 13 October 2026**  
**Status:** Design and future-content exclusion recorded. **No runtime mod-removal operation claimed.**

## Decision
Ambient Odyssey **will not use Origins**. Treat this as a full exclusion, not merely "Origins are optional" and not a request to add a new alternative race/class engine.

- No **Origins (NeoForge)** or **NeoOrigins**, their extensions, race/species selection, background systems, player Origin powers, Origin passive/weakness modifiers, Origins selection prompts, or Origin respec/Orb of Origin quest paths.
- No Origins-themed quest lines, FTB manual pages, achievement/advancement gates, Origin-only recipes, Origins progression triggers, Origins balance targets or Origin-dependent gear recommendations.
- Retain gear, affix, Apotheosis, Artifacts, Relics, Curios/accessories and native **Iron's Spells / Ars Nouveau** progression; player expression comes from actual available equipment, weapons, magic and personal experimentation, not racial perks.
- No unsolicited replacement class/MMO stat overhaul just because Origins is removed. Independent skill systems can be considered later only if user requests.

## Evidence and removal status
Checked `docs/performance/v049-prep/MOD_DEPENDENCY_AUDIT.json` and `docs/testing/v04-evidence/dependency-audit.json`, a historical consolidated native-JAR scan: **neither contains an Origins/NeoOrigins/Apoli named JAR or dependency entry**. Checked `release_030/release-lock.json` on the v0.5 research branch: **no Origins/Apoli additions are pinned**. The source tree exposes no direct `release_030/overrides` Origins-specific path.

**These checks do not by themselves prove the exact player's newest installed JAR set.** Before issuing `remove_projects` in `release-lock.json`, inspect the effective current CurseForge manifest and native `mods` directory, including the inherited `Ambient-Odyssey-v0.2.10.zip`. If Origins or any *dedicated Origins addon* does exist, remove its exact project/file pin and only dependencies that become truly orphaned; do **not** strip shared libraries required by unrelated mods.

**No pack binary, manifest project count, game config, Questlog JSON, release ZIP, mod JAR or rollback has been changed by this decision.** The correction currently affects authored game-design documentation and agent instructions.

## Superseded history
The prior study `docs/audits/RPG_CHARACTER_IDENTITY_PRIVATE_MMO_PROPOSAL_2026-10-10.md` contains 8–12 proposed Origins, addon candidates and attribute/race research; that entire Origins section is **historical only, rejected for AO**. Do not use its old "preferred backend" recommendations. The existing `docs/questing/QUEST_CAMPAIGN_ARCHITECTURE.md` must not recreate Origins quests or FTB pages.

## Work mode / implementation checklist
1. Reconcile latest full packaged mod roster against this prohibition.
2. If an Origins backend/addon is actually present, remove it safely on a separate development branch and run dependency closure checks (and full client/game tests before release).
3. Scan installed Questlog/FTB/advancement assets, keybind overrides and onboarding UIs for Origin references; remove source-confirmed unused entries without changing unrelated quests or save progress.
4. Eliminate stale Origins assumptions in the RPG progression design, boss balance and gear readiness rubrics.
5. Report exact changes vs pre-existing absence; never report "removed Origins from playable pack" if it was only a historical design proposal.

**Authority:** user explicitly stated "We won't be playing with Origins so you can take those out at least." This supersedes earlier planning recommendations.
