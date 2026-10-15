# Progression consistency report: native baseline (DRAFT)

**What this is.** How the *native* stats of the Tier 6 to 9 bosses are ordered today. **What it is not.** There is no target model yet (no agreed player-power reference per tier), so it shows ordering and gaps, not whether a tier is right. No value has been changed.

Health is the measured baseline from the AOT run (attribute value 20 ticks after a proper spawn) or, where marked `config`, the value the live config states. Health is **not** difficulty: damage, armor, phases, healing and mechanics matter too (the handoff says so). The hit-count bosses (Chesed, Malkuth, Geburah) are left out of the health statistics.

## Tier summary (health, native)

| Tier | Bosses with health | Min | Median | Max |
|---|---:|---:|---:|---:|
| 6 | 9 | 120 | 300 | 500 |
| 7 | 6 | 250 | 525 | 800 |
| 8 | 10 | 200 | 410 | 750 |
| 9 | 3 | 300 | 390 | 1000 |

**The median native health does not rise with the tier** (it falls after Tier 7), so the native stats do not follow the tier order; this is the expected starting point, not an error in the data.

## Tier 6

| Boss | Health | Attack attribute | Extra layers or notes |
|---|---:|---:|---|
| Dead King | 500 (measured) | 10 |  |
| Underground dragons (fire, ice, lightning) (fire_dragon) | 500 (measured) | 18 | Config values are shared by all three dragon species; measured at 125 days of growth. |
| Underground dragons (fire, ice, lightning) (ice_dragon) | 500 (measured) | 18 | Shared dragon config; measured at 125 days. |
| Underground dragons (fire, ice, lightning) (lightning_dragon) | 500 (measured) | 18 | Shared dragon config; measured at 125 days. |
| Captain Cornelia | 300 (measured) | 14 |  |
| Eternal Starlight: Starlight Golem | 200 (measured) | - | Boss respawn on (30 min cooldown). Interaction-locked in earlier tests. |
| Eternal Starlight: Lunar Monstrosity | 200 (measured) | 5 | Boss respawn on (30 min cooldown). |
| Eternal Starlight: The Gatekeeper | 175 (measured) | 1 | Boss respawn on (30 min cooldown, config/eternal_starlight.json). Interaction-locked in earlier tests. |
| Eternal Starlight: Permafrost | 120 (measured) | 6 | Boss respawn on (30 min cooldown). |
| Ignited Revenant | unmeasured | - |  |
| Coralssus | unmeasured | - |  |
| Kobolediator | unmeasured | - |  |

## Tier 7

| Boss | Health | Attack attribute | Extra layers or notes |
|---|---:|---:|---|
| Malkuth | 1024 (measured) (hit-count) | 140 | Hit-count mechanics; difficulty multipliers in the config. |
| Ossukage | 800 (measured) | 7 | Ritual summon at a crafted altar; no arena; no respawn mechanism found. |
| Kotsukage | 700 (measured) | 12 | Ritual summon; no arena. |
| Netherite Monstrosity | 600 (measured) | 25 |  |
| Ancient Remnant | 450 (measured) | 25 | Owner: needs a special interaction to appear; stats should edit like the other Cataclysm bosses. Health measur |
| Ender Guardian | 333 (measured) | 16 |  |
| Ice and Fire Hydra | 250 (config) | - |  |
| Chesed | 10 (measured) (hit-count) | none (no attack_damage a | Hit-count mechanics (chesedMaxHits) besides health; difficulty multipliers in the config. |
| Ender Golem | unmeasured | - |  |

## Tier 8

| Boss | Health | Attack attribute | Extra layers or notes |
|---|---:|---:|---|
| Umbrakar | 750 (measured) | 14 | Ritual summon; no arena. |
| Last of Deepslate | 600 (measured) | 35 |  |
| Bosses'Rise: Kraken | 500 (measured) | 10 |  |
| Ignis | 453.25 (measured) | 14 |  |
| Maledictus | 420 (measured) | 13 |  |
| The Leviathan | 400 (measured) | 15 |  |
| Bosses'Rise: Underworld Knight | 280 (measured) | 13 |  |
| Bosses'Rise: Yeti | 250 (measured) | 18 |  |
| Bosses'Rise: Infernal Dragon | 250 (measured) | 14 |  |
| Bosses'Rise: Sandworm | 200 (measured) | 10 |  |

## Tier 9

| Boss | Health | Attack attribute | Extra layers or notes |
|---|---:|---:|---|
| Tyros | 1000 (measured) | 20 | Stronger Fire Boss 2.0.0 is installed (config/strongerfireboss-common.toml): soul-mode damage limiter (1% cap  |
| Scylla | 390 (measured) | 18 | Her wave (a constant 9.0 hit every 0.5 s) has no lever; melee scales with the attack attribute, fixed-damage a |
| Obsidilith | 300 (measured) | 16 |  |

## Tier TBD

| Boss | Health | Attack attribute | Extra layers or notes |
|---|---:|---:|---|
| Geburah | 20 (measured) (hit-count) | none (no attack_damage a |  |

## Bosses below the median of the tier immediately under them

- **Ice and Fire Hydra** (Tier 7, health 250) is below the Tier 6 median (300).
- **Ignis** (Tier 8, health 453.25) is below the Tier 7 median (525).
- **Maledictus** (Tier 8, health 420) is below the Tier 7 median (525).
- **The Leviathan** (Tier 8, health 400) is below the Tier 7 median (525).
- **Bosses'Rise: Sandworm** (Tier 8, health 200) is below the Tier 7 median (525).
- **Bosses'Rise: Yeti** (Tier 8, health 250) is below the Tier 7 median (525).
- **Bosses'Rise: Infernal Dragon** (Tier 8, health 250) is below the Tier 7 median (525).
- **Bosses'Rise: Underworld Knight** (Tier 8, health 280) is below the Tier 7 median (525).
- **Bosses'Rise: Kraken** (Tier 8, health 500) is below the Tier 7 median (525).
- **Scylla** (Tier 9, health 390) is below the Tier 8 median (410).
- **Obsidilith** (Tier 9, health 300) is below the Tier 8 median (410).

**At or near the 1024 health cap already:** Tyros. A higher tier cannot get more health from the attribute; armor, resistance or absorption effects, or the later damage-scaling addon, would be needed.

**No health figure at all:** Ignited Revenant, Coralssus, Kobolediator, Ender Golem.

**Bosses whose real difficulty is not in these numbers:** Tyros (Stronger Fire Boss addon: soul-mode damage cap, Rend, Sharpness V), Chesed and Malkuth (hit-count mechanics), Scylla (a wave and fixed-damage abilities that the attribute does not scale).

## Needed before this can become a real report
- A player-power reference per tier (for example measured damage per second and health of a typical kit), or owner-set targets.
- The five never-measured bosses and the four whose damage is interaction-locked (see the ledger).
- Decisions on Geburah (TBD) and the Eternal Starlight family (TBD).
