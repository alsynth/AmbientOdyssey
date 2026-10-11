package dev.ambientodyssey.worldgensafety;

import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;

/**
 * Experimental, minimal world-generation safety shim. Does not alter
 * vanilla generation or other mod's spawning and preserves Hominid
 * replacement on the main server thread.
 */
@Mod("ao_worldgen_safety")
public final class WorldgenSafety {
    public WorldgenSafety(IEventBus modBus) {
    }
}
