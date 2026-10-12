# Storage guard handoff and manual tests — 12 October 2026

## Resume point

Repo: https://github.com/alsynth/AmbientOdyssey
Branch: experimental/v046-gem-tier-local-verification-20261012
Start from its latest head. Base before this patch was 76d36b3.
Applied Claude patch 5512a0da7d243d4cc99ac302149de8302e25845c using git am;
local imported commit 1dac9c3. The patch's original UNBUILT notes are historical.
Read AGENTS.md, docs/ports/V046_RESUME.md and the source-review follow-up.
Preserve main, v0.4.5, the original port branch and live profiles/saves.

## Verified now

Apotheotic compilation and ALL 12 required native GameTests PASS against actual
Apotheosis 8.9.0 / Placebo 9.9.2 / Apothic Attributes 2.11.0 / NeoForge 21.1.252.
Evidence: docs/testing/v046-evidence/apotheotic-twelve-storage-guard-gametests.log.
Server-tested development JAR SHA-256:
c888eda867524c6d84914dae88207cf601e4c6a5771a5297ac2d29937cc9f723.

Required mixins loaded in the native server tests and an isolated native client.
Tests verify refusal through case item-handler insertion, intact backstop drop,
no upper-tier case storage, Ancient positive-control storage, and native Perfect
ingredient rejecting Esoteric while accepting Ancient. They do NOT simulate the
actual shift-click gesture, drag interaction, a ticking hopper or a complete
crafting recipe. The required count remains 12; log freshness checks remain strict.

Added a reproducible clientQA run in the module's build.gradle, using a new
build/client-qa-runtime folder. Launched it and created a disposable creative
Superflat world named New World. Seven-mod native context, not the full 327-mod
pack. Client reached a real world and opened the Gem Case. A drag from hotbar
to the case input was attempted. Before observing the completed result, physical
Escape stopped Computer Use. Do not mark that drag PASS. Shift-click, actual
hopper and crafting-result checks are still UNVERIFIED. Leave the user's game
window under their control; do not kill Java or interact after that interruption.

## Newly observed presentation problems

User reports Hearty and Armored jewels have missing textures. Hearty's missing
texture was also visible in this isolated client. This is an unfinished asset/model
integration, not intended finished behavior. Original gem art has not been ported.

Creative inventory shows no gems above Perfect. Current native creative population
enumerates six Purity values, so it cannot expose separate Artifact/Heirloom/Esoteric
stacks. Their legacy values and serialization exist, but creative entries for them
have not been implemented. They remain accessible via exact tier components/helper;
absence from creative is NOT proof those tiers were removed. Add explicit upper-tier
entries and correct names/textures; preserve stock gems and all nine original tiers.

## What the user should test now

Use ONLY the disposable client/world above. Tests below are manual and pending.
The live v0.4.5 profile is not an appropriate test target. Record PASS/FAIL separately.

1. Shift-click ONE Esoteric Hearty gem into the Gem Case input. Expect exactly one
   dropped gem with legacy_gem_tier 8, no case storage, no duplication/loss. Pick it
   up and confirm its bonus remains +5 max health; Ancient's value is +3.
2. Drag ONE Esoteric gem into the same input and release. Same expected intact
   drop and zero storage. A gem briefly visible on the cursor/input is not a final
   result. Confirm server state after several ticks, then pick up the drop.
3. Put a hopper above a separate empty Gem Case, pointing into it. Put ONE Esoteric
   gem in the hopper. After several seconds it must remain in the hopper; the case
   must stay empty and no dropped duplicate should appear. Repeat with Ancient
   tier 5 as a positive control: Ancient should enter the case. Ensure the hopper
   is powered off only when arranging it, and unpowered when checking transfer.
4. Test a recipe using the native apotheosis:gem ingredient at purity perfect.
   All other inputs and any gem-specific ID restriction must match. Esoteric must
   yield no output and remain unconsumed. The SAME gem at Ancient tier 5 must yield
   the expected output. If both fail, the test is inconclusive, not PASS.
5. Repeat storage/recipe rejection for Artifact (6) and Heirloom (7), and verify
   ordinary stock gems/Ancient still work. Save/rejoin and check returned upper
   gems still retain their exact tiers. Report texture/name problems separately.

A disposable shapeless crafting fixture has been supplied at:
build/client-qa-runtime/saves/New World/datapacks/aoqa/data/qa/recipe/perfect_gem_guard.json
It accepts any native Perfect gem and produces one diamond. This fixture is NOT
production pack content. In this world run /reload, then put one gem in the player's
2x2 crafting grid. Esoteric must have no result; Ancient must show a diamond.
This gives a meaningful positive control without stock recipe ID restrictions.
The fixture is newly written and NOT yet loaded or verified. If /reload reports a
recipe parse error, record it and fix the fixture before drawing any conclusion.

Command to give one Esoteric Hearty test gem (user may paste into Minecraft chat):
/give @s apotheosis:gem[apotheosis:gem="ao_apotheotic_port:modded/hearty",apotheosis:purity="perfect",ao_apotheotic_port:legacy_gem_tier=8] 1

For Ancient use the identical command with the last value =5; Artifact =6,
Heirloom =7. These command-created stacks currently display a stock Perfect name;
the component and bonus identify the actual legacy tier. This is another pending
presentation issue, not a successful upper-tier naming implementation.

## Local paths / commands

Repository:
C:/Users/headq/Documents/Codex/2026-10-11/i-d-use-the-existing-v0/work/AmbientOdyssey
Disposable world:
ports/apotheotic-additions/neoforge/build/client-qa-runtime/saves/New World
Test JAR:
ports/apotheotic-additions/neoforge/build/libs/ao-apotheotic-port-prototype-0.0.1-source-prototype.jar

From repo root, PowerShell:
$env:GRADLE_USER_HOME='C:/Users/headq/Documents/Codex/ao-gradle-cache'
$env:CI='true'
& ../gradle-runtime/gradle-9.2.1/bin/gradle.bat -p ports/apotheotic-additions/neoforge build runGameTestServer --console=plain
& ../gradle-runtime/gradle-9.2.1/bin/gradle.bat -p ports/apotheotic-additions/neoforge runClientQA --console=plain

Do not launch a second client if this disposable client is already running.
Network permission is needed even for the local Gradle daemon connection here.
Some direct Unicode text injection was ignored by Minecraft; physical key input
worked. The computer-use API lacks a documented held-Shift mouse-click operation,
so do not claim a literal automated shift-click was performed.

## Next agent work

First collect the user's manual results and investigate any duplication/drop or
insertion failure. The depositGem mixin drops a COPY and cancels; callers other
than the tested menu/handler may still retain their source stack. Review ownership
and exactly-once behavior before claiming it is safe against all mod callers.

Implement original gem models/textures with source attribution/license, upper-tier
creative entries and localized tier names. Do not enable natural drops to hide
missing creative entries. Then complete dedicated upper-tier crafting/upgrading,
storage parity and other open gem systems. The refusal guard prevents some loss;
it does not provide tier-aware Gem Case storage or complete the port.

Remaining broader scope stays open: 93 attribute affixes, 146 other affixes,
66 gems, bosses/gear/loot, recipes/reforging/trades and full-pack/multiplayer checks.
Keep Artifact, Heirloom AND Esoteric. Wet Sand full-pack/natural-terrain checks
remain open. No complete CurseForge build has been made. Continue frequent GitHub
checkpoints with exact evidence; compilation, native tests and this narrow client
are not certification of the complete pack. Latest remote CI must be checked
separately after this handoff push.
