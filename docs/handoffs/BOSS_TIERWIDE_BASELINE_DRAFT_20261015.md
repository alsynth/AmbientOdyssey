# T6–T9 boss tier-wide baseline — first owner playtest proposal (15 Oct 2026)

**Status: proposal only — not patched, not deployed, no gameplay tests.** Based on 35-row file 17 boss ledger, and 18–21 companion evidence. A separate per-boss CSV is delivered in the chat artifact. The tier changes are *new proposed playtest values*, not measured targets or prior owner-approved numbers.

| Boss tier | HP scale from native/config baseline | Ordinary attack scale | Use |
|---|---:|---:|---|
| T6 | 1.50× | 1.25× | First playtest baseline |
| T7 | 1.75× | 1.40× | First playtest baseline |
| T8 | 2.00× | 1.60× | First playtest baseline |
| T9 | 2.50× | 1.80× | First playtest baseline; mostly requires cap/mechanic solution |

## Review gates and exceptions
- **Hit-count fights (Chesed, Malkuth, and Geburah TBD)**: do not apply ordinary HP multiplier without analyzing hit counts and vulnerability windows. Geburah unassigned.
- **1024 HP cap**: large bosses hit observed cap with 1.75–2.5× HP. Don't apply an unachievable number and call it effective; armor, phase design, absorption or user's future addon needs analysis. The target HP in the companion CSV is *indicative and capped*, not proof of effective implementation.
- **Scripted damage vs attack attribute**: Scylla wave and fixed skills, Iron's spell power, boss ranged spells, hit-count damage, and several special boss skills require separate ability tuning. General attack multiplier may leave much of their damage unchanged.
- **Tyros** already has Stronger Fire Boss addon and is near cap at 1000 HP; preserve its soul-mode rules and do not force naïve HP scaling.
- **Bosses'Rise/Block Factory's Bosses**: current SERVER config path and effect per-world unresolved; preserve distinct per-boss health, armor and attack fields. Yeti interaction-locked.
- **Brutal Bosses** are a separate global design: HP×4, damage×3 as last explicit owner values. Do not mix into T6–9 boss baseline automatically; reconcile newer handoff's mistaken ×4 damage assumption before deployment.
- **Missing measurements**: Ignited Revenant, Coralssus, Kobolediator, Ender Golem, Ice and Fire Hydra must be measured; HP computed for these is intentionally blank.
- **No live addon**: Aquamirae Captain Cornelia and Archaion Last of Deepslate have no native config; require datapack/addon or other measured hook. Authoritative high-tier addon development belongs to owner's separate developer.
- **Do not change player-count scaling automatically.** No reliable native scaling was established.
- **No loot changes yet.** Lootr/chest table edits and boss rewards will follow baseline mechanical validation; boss-drop and chest-loot economy should remain separate.

## Implementation plan
1. Verify config source files against the exact installed pack, including world/serverconfig copies; capture byte-identical rollback and hashes.
2. Apply **per-mod, per-boss** native HP and ordinary-attack modifiers where verified, **not a global entity attribute override that stacks unexpectedly with DD**. Distinguish a mod's current multiplier from resulting total.
3. Isolate bosses with special scripted damage or 1024 HP cap in an addon follow-up, with stable entity IDs and interaction mechanic tests.
4. Test T6 first against actual player equipment/Apotheosis gear. Record time to kill, incoming damage by ability, phase handling and party size. Recalibrate T7–T9 after owner review.
5. Ensure DD vanilla mob matcher doesn't silently double-scale tested boss entity IDs; Brutal Bosses stacked modifiers are intentionally separate.
6. Record all changed keys, before/after values, hashes, and rollback commands before releasing a test build.

**This document deliberately does not claim an effective playable patch:** tier multipliers alone are not safe to transcribe into incompatible mod config schemas, and the owner will test tiers before approving final difficulty.

## Owner superseding multipliers — 15 October 2026

**This section supersedes all earlier tier-wide proposals in this document.** Owner-selected targets: **T6 HP x10, ordinary attack x3; T7 HP x10, attack x6; T8 HP x10, attack x10; T9 HP x10, attack x10**. They are playtest targets, not implemented native config values or in-game validated.

**Critical implementation gate:** the documented effective max-health cap at 1024 prevents native attribute-based x10 HP on bosses with baseline HP greater than 102.4. Do not silently clamp the target and describe it as x10; retain both the uncapped x10 target and achieved actual health separately. Before implementation, verify a reliable workaround using boss addon mechanics or multi-phase/health replacement rather than blindly writing values above cap. For hit-count bosses (Chesed, Malkuth, and Geburah pending tier), do NOT multiply visible HP by x10 as if it represented survival time; handle hit-count gates separately. Fixed-damage attacks and special abilities need distinct treatment from vanilla attack attributes; actual T6/7/8/9 damage will not necessarily become x3/x6/x10/x10 without source-specific changes. Health caps and special-mechanic blocks are owner review checkpoints. Preserve Brutal Bosses independent 4x HP/3x damage decision, not these tier-wide boss targets.

**Status:** planning only. No native boss config, datapack, addon or production file changed by this update.

## Owner approval — full Tier 2–9 multiplier schedule (15 October 2026)

This is the current approved schedule and **supersedes the older T6 x3 attack proposal**. T2 HP x2 / ordinary attack x1.5; T3 x3 / x2; T4 x5 / x3; T5 x7 / x4; **T6 x10 / x5**; T7 x10 / x6; T8 x10 / x10; T9 x10 / x10.

Apply available native config/attribute multipliers to ordinary bosses, accepting observed vanilla HP ceiling ~1024 and as-yet unconfirmed attack caps. Modded ability damage may exceed vanilla attribute caps; do not claim ordinary attack scalar alters spells or scripted attacks. Future post-worldgen addon will reinforce high-end bosses as a separate layer. Do not block baseline on exceptional mechanics; mark exceptions for follow-up. Preserve Chesed, Malkuth, Geburah hit-count mechanics; avoid blanket Ice & Fire settings that affect unrelated low-tier surface dragons. Dungeon Difficulty is separate from boss native stats. **Approval is for balance targets, not proof they have been implemented or runtime-tested.**
