package dev.ambientodyssey.compat;

import net.neoforged.fml.common.Mod;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Mod(StreamsMineCellsCompat.MODID)
public final class StreamsMineCellsCompat {
    public static final String MODID = "ao_streams_minecells";
    public static final Logger LOGGER = LoggerFactory.getLogger(MODID);

    public StreamsMineCellsCompat() {
        LOGGER.info("Ambient Odyssey: protecting Mine Cells dungeon generation from Streams Reflowing worldgen hooks");
    }
}
