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
