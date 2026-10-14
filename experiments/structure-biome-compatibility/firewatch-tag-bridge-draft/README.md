# SUPERSEDED — DO NOT INSTALL OR DEPLOY

This **older experimental shared-tag bridge** is intentionally retained for historical comparison only. The pinned **Dungeons & Taverns v4.4.4 NeoForge JAR** source audit proved its additions to `nova_structures:collections/birch_forests`, `cherry_forests`, and `savannas` would affect **22**, **19**, and **20** structure IDs respectively through the nested `collections/land` tag, not only firewatch towers.

Use the newer **[source-faithful four-tower draft](../firewatch-structure-only-draft/README.md)** for review instead; it changes only each targeted tower's `biomes` field to a private AO-specific biome tag and preserves all native structural fields. **Neither draft is active in Paxi, in the modpack release, or on the server.** Actual natural generation and current profile resources still require testing.

Pinned-JAR evidence: `docs/balance/DD_DNT_PINNED_444_NATIVE_CONSUMERS_20261014.json`.
