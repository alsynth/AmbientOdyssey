# Experimental native Apotheotic Additions port

This prototype is isolated from the v0.4.5 release. The current native milestone
retains Artifact, Heirloom and Esoteric, 25 core attribute affixes, and five
attribute-only gems with their nine original tier values. Natural custom rarity
and gem drop weights remain zero. It is not a complete or playable pack release.

Twelve native GameTests verify rarity binding, native rolls and item serialization,
real server resource reload, original stepped affix ranges and actual equipped
damage, gem values/item/network serialization, native unique restrictions, and
socketed Esoteric health applied to an equipped entity, tier resolution and stock
upgrade behavior. A characterization test also reproduces unresolved Gem Case
tier loss and Perfect-ingredient acceptance of upper tiers. Passing that test
confirms the hazards, not compatibility. Tests must emit twelve
fresh passing results; successful compilation or launcher exit is insufficient.

Use docs/ports/V046_RESUME.md for current evidence, remaining systems and exact
continuation requirements. Core converters keep complete source inventories:
118 attribute affixes (25 active, 93 pending) and 71 gems (5 active, 66 pending).
All 146 other affixes and bosses, loot, recipes/reforging/trades remain pending.
Native gem cutting does not support the three upper tiers and compares gems
without their legacy component; dedicated upgrade checks must precede release.
Full-pack gameplay and multiplayer verification also remain outstanding.

Ported data is attributed under AFL-3.0; see neoforge/NOTICE.md and LICENSE.AFL-3.0.
