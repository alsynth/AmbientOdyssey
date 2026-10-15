# The Annihilator and Regalia: proposal (not approved, not implemented)

**Status:** Approved: acquisition native-only (15 Oct); tier still a proposal (T6 starting point, see section C). Implemented: no; nothing was added to Regalia, now or earlier. Statically verified: the facts in section A (installed `L_Ender's Cataclysm 1.21.1-3.33.jar`, R4 config and R4 campaign policy). In-game tested: no. Multiplayer tested: no.

## A. Already specified or verified

### The item
- ID `cataclysm:the_annihilator`. Tagged `minecraft:swords` and `cataclysm:explosion_immune_item`. Enchantability 16. Can disable shields.
- **Stats (R4 `cataclysm-common.toml`, `[tools_and_abilities.annihilator.tool_config]`):** `attack_damage = 8.5`, `attack_speed = 1.6` (mod defaults, unchanged in R4). For scale, a vanilla netherite sword is 8 damage at 1.6 speed.
- **Critical hits:** lang text "Higher Critical Damage". Cataclysm's `ServerEventHandler.onCriticalAttack` adds the player's `cataclysm:additional_critical_damage` attribute ÷ 100 to the crit multiplier, and plays a parry sound on Annihilator crits. **The Annihilator's own attribute amount is not decoded.**
- **Charged AoE:** lang text "If you hold it in both hands, you can charge it for 2 seconds for AOE damage". In bytecode: hold-to-use (72000 max), threshold constants 40 ticks (= 2 s) and 100. The AoE code uses a 6.0 constant (likely the radius) and damage from the holder's `ATTACK_DAMAGE` attribute via a `mobAttack(player)` damage source. Exact AoE formula not decoded.

### Acquisition and native progression
- Recipe (shaped): **2 × `cataclysm:cursium_ingot` + 1 × `cataclysm:black_steel_ingot`**.
- **Cursium** comes from **Maledictus** (3–4 ingots in its loot table) or from Cursium blocks. Maledictus is **T8** in the R4 boss policy.
- **Black steel** comes from e.g. `frosted_prison_treasure` (5–9 ingots, weight 10) and other Cataclysm chests.
- Upgrade: `cataclysm:weapon_fusion` of Annihilator + `ignitium_ingot` gives **The Immolator**. Ignitium comes from Ignis (also T8).

### Owner decisions that apply
- Cursium items are **native-only** for Regalia (decision 5.7 / E4).
- The Annihilator is "unapproved / owner decision outstanding" (`LOOT_OVERHAUL_OWNER_DECISIONS_20261015.md:62`; canonical handoff line 84).
- Owner remark, input only: "eligible for the Regalia bonus from T6 because of its critical damage and charged AoE".

### How Regalia works today (R4)
- `ao_loot_policy.json` `regalia` is a **flat list of 13 IDs**. `BossRewards.java:72` picks one **uniformly** on every credited boss kill, **T2–T9 alike, with no tier gating**.
- The reward is a plain `new ItemStack(id)`, with no affixes or enchantments.

## B. Proposal (mine, for your decision)

### Fit with AO progression
- Natively, the Annihilator is a **T8** weapon: it needs a Maledictus kill for Cursium, and its upgrade needs Ignis. Granting it at T6 skips two boss tiers and works around the "Cursium native-only" rule.
- Its power (netherite-level damage + crit bonus + 6-block charged AoE + shield break) fits the T6 "endgame-ready" gear band. It would beat most T6-reachable weapons.

### Combat interactions
- The AoE uses a player-attributed `mobAttack` source, so it **counts for kill credit** and **isn't blocked by Cornelia's filter** (she ignores arrows, tridents and explosions, not mob attacks).
- AoE hits several mobs at once, which compounds with DD T6 zones (+300% HP) and Brutal Bosses (×4 HP).
- A Regalia copy arrives plain; Apotheosis affixes only come through native routes.

### Options

| Option | What changes | Chance per credited kill | Chance after 5 T6 kills |
|---|---|---|---|
| **1. Native-only (recommended)** | nothing | 0 | 0 |
| 2. Tier-gated Regalia from T7 | new `min_tier` per Regalia entry, separate low-weight roll | 3% | — (T7+) |
| 3. Tier-gated from T6 (your remark) | as option 2, `min_tier: 6` | 2% | 9.6% |
| (not recommended) Plain list entry | add to the flat list | 1/14 ≈ 7.1% **at every tier from T2** | 31% |

The percentages are uniform-roll arithmetic, not measured drop rates. Five T6 kills: 1 − 0.98⁵ = 9.6%; 1 − (13/14)⁵ = 31%.

**Why I recommend option 1:** it keeps the Maledictus → Cursium → Annihilator → Ignis → Immolator chain and the Cursium native-only rule. Option 2 or 3 would need a code and schema change (tier gating doesn't exist today).

**If you choose option 3:** a 2% separate roll gated at `min_tier >= 6`, excluded from T2–T5. Keep the native recipe as is. Don't apply the same to The Immolator.

### Risks
- Skipping the T8 progression route.
- Weakening the Cursium native-only rule.
- AoE inflating farm speed in T6 DD zones.
- A plain-list entry would leak it to T2 bosses.

### Open questions for you
1. Native-only, T7, or T6?
2. If gated: a separate roll (as above), or part of the single Regalia pick?
3. Does "Cursium native-only" also cover items crafted from Cursium?
4. Should I measure the crit attribute amount and the AoE formula in an engine test before you decide?

## C. Owner direction (15 Oct, second round): native-only acquisition, T6 starting point

**Decided:** acquisition is native-only. No Regalia entry, no AO grant, no AO recipe change. **Proposal input:** T6 is the starting point.

### What native-only means in practice (statically verified)
- The recipe needs 2 Cursium ingots. I scanned every installed JAR's loot tables, recipes and structure NBT. **The only native Cursium source is Maledictus** (3–4 ingots per kill). Cursium blocks only come from ingots. Other mods (Cataclysm Spellbooks, MEED, the AO gem port) only *consume* Cursium.
- Maledictus is **T8** in R4's boss policy. So with native-only acquisition, **the earliest a player can craft the Annihilator is after a T8 kill**, whatever tier label AO gives it.

### T6 vs T7 as the design tier (if you keep a tier label for balance and quest text)

| | T6 | T7 |
|---|---|---|
| Gear band (V050 rubric) | "Endgame-ready … T6 boss reward unlocks further gear" | "Pinnacle-aware Ancient access, Artifact/Heirloom path" |
| Weapon fit | 8.5 dmg / 1.6 speed ≈ netherite sword + crit bonus + 6-block charged AoE. Strong but not beyond T6 expectations | Below typical T7 Artifact/Heirloom gear, so it'd be a sidegrade there |
| Boss content it helps with | T6 bosses (Ignited Revenant, Coralssus, Kobolediator, Dead King, Cornelia) and T6 DD zones (+300% HP), where AoE matters most | T7 bosses (Netherite Monstrosity, Ender Guardian, Hydra …) |
| Conflict with native route | Native gate is T8, two tiers later | Native gate is T8, one tier later |

**Justification for T6 (your starting point):** its stats and AoE match the T6 gear band, and its value is highest against T6 DD crowds. At T7 it's already outclassed by Artifact/Heirloom routes. **Gap:** native-only acquisition delays it to T8. So T6 can only be the *design* tier (tooltips, quest hints, balance tables). It can't be the *availability* tier unless one of these changes:
1. Maledictus is re-tiered to T6 (a boss-policy change, your call); or
2. a native Cursium source appears in another installed mod (none found).

I recommend option 1 **not** be done just for this item. Treat T6 as the design tier and T8 as the real availability tier, and say so in quest text.

### Open questions
1. Is a "design tier T6, available at T8" split acceptable, or should the Annihilator just be labeled T8?
2. Still to decode by engine test: the crit attribute amount and the AoE damage formula.
