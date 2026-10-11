package dev.ambientodyssey.ports.wetsand;

import net.minecraft.core.BlockPos;
import com.mojang.serialization.MapCodec;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.util.RandomSource;
import net.minecraft.tags.FluidTags;
import net.minecraft.world.level.Level;
import net.neoforged.neoforge.common.NeoForge;
import net.neoforged.neoforge.event.tick.ServerTickEvent;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.FallingBlock;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.registries.DeferredBlock;
import net.neoforged.neoforge.registries.DeferredItem;
import net.neoforged.neoforge.registries.DeferredRegister;

/**
 * Native NeoForge PORT PROTOTYPE, not the original Wet Sand mod.
 *
 * This first iteration establishes six item/block registries and moisture
 * transitions for the new blocks. It intentionally does not inject into
 * vanilla sand or worldgen, or tamper with suspicious-sand block entities.
 * That requires a separate source-backed, TPS-bounded implementation.
 */
@Mod(WetSandPort.ID)
public final class WetSandPort {
    public static final String ID = "ao_wet_sand";
    private static final DeferredRegister.Blocks BLOCKS = DeferredRegister.createBlocks(ID);
    private static final DeferredRegister.Items ITEMS = DeferredRegister.createItems(ID);
    public static final DeferredBlock<Block> MOIST_SAND = stage("moist_sand", false, 1);
    public static final DeferredBlock<Block> WET_SAND = stage("wet_sand", false, 2);
    public static final DeferredBlock<Block> SOAKED_SAND = stage("soaked_sand", false, 3);
    public static final DeferredBlock<Block> MOIST_RED_SAND = stage("moist_red_sand", true, 1);
    public static final DeferredBlock<Block> WET_RED_SAND = stage("wet_red_sand", true, 2);
    public static final DeferredBlock<Block> SOAKED_RED_SAND = stage("soaked_red_sand", true, 3);

    private static DeferredBlock<Block> stage(String name, boolean red, int stage) {
        DeferredBlock<Block> block = BLOCKS.register(name,
                () -> stage == 1
                        ? new MoistureFallingBlock(red, stage, BlockBehaviour.Properties.ofFullCopy(red ? Blocks.RED_SAND : Blocks.SAND).randomTicks())
                        : new MoistureBlock(red, stage, BlockBehaviour.Properties.ofFullCopy(red ? Blocks.RED_SAND : Blocks.SAND).randomTicks()));
        ITEMS.register(name, () -> new BlockItem(block.get(), new Item.Properties()));
        return block;
    }

    public WetSandPort(IEventBus modBus) {
        BLOCKS.register(modBus);
        ITEMS.register(modBus);
        NeoForge.EVENT_BUS.addListener(WetSandPort::updateNearbyShorelines);
    }

    /** No worldgen hooks or chunk-wide scans: at most eight checks per player per second. */
    private static void updateNearbyShorelines(ServerTickEvent.Post event) {
        if (event.getServer().getTickCount() % 20 != 0) return;
        for (var player : event.getServer().getPlayerList().getPlayers()) {
            ServerLevel level = player.serverLevel();
            if (!level.dimension().equals(Level.OVERWORLD)) continue;
            RandomSource random = level.getRandom();
            for (int attempt = 0; attempt < 8; attempt++) {
                BlockPos center = player.blockPosition();
                BlockPos pos = center.offset(random.nextInt(17)-8, -1-random.nextInt(3), random.nextInt(17)-8);
                if (!level.hasChunkAt(pos)) continue;
                Block old = level.getBlockState(pos).getBlock();
                if (old != Blocks.SAND && old != Blocks.RED_SAND) continue;
                boolean nearWater = false;
                for (int dx=-3; dx<=3 && !nearWater; dx++) {
                    for (int dz=-3; dz<=3 && !nearWater; dz++) {
                        if (Math.abs(dx)+Math.abs(dz)>3) continue;
                        BlockPos nearby=pos.offset(dx,0,dz);
                        if (!level.hasChunkAt(nearby)) continue;
                        var fluid=level.getFluidState(nearby);
                        nearWater=fluid.is(FluidTags.WATER) && fluid.isSource();
                    }
                }
                if (nearWater) level.setBlock(pos,(old==Blocks.SAND ? MOIST_SAND : MOIST_RED_SAND).get().defaultBlockState(),3);
            }
        }
    }

    private static void advance(BlockState state, ServerLevel level, BlockPos pos, boolean red, int stage) {
        boolean hydrated = false;
        for (int dx = -3; dx <= 3 && !hydrated; dx++) {
            for (int dz = -3; dz <= 3 && !hydrated; dz++) {
                if (Math.abs(dx) + Math.abs(dz) > 3) continue;
                var fluid = level.getFluidState(pos.offset(dx, 0, dz));
                hydrated = fluid.is(FluidTags.WATER) && fluid.isSource();
            }
        }
        int target = Math.min(3, Math.max(0, stage + (hydrated ? 1 : -1)));
        if (target == stage) return;
        Block next = switch (target) {
            case 0 -> red ? Blocks.RED_SAND : Blocks.SAND;
            case 1 -> red ? MOIST_RED_SAND.get() : MOIST_SAND.get();
            case 2 -> red ? WET_RED_SAND.get() : WET_SAND.get();
            default -> red ? SOAKED_RED_SAND.get() : SOAKED_SAND.get();
        };
        level.setBlock(pos, next.defaultBlockState(), 3);
    }

    /** Moist sand inherits vanilla gravity; wet and soaked stages are stable. */
    public static final class MoistureFallingBlock extends FallingBlock {
        public static final MapCodec<MoistureFallingBlock> CODEC = simpleCodec(properties -> new MoistureFallingBlock(false, 1, properties));
        @Override public MapCodec<? extends FallingBlock> codec() { return CODEC; }
        private final boolean red;
        private final int stage;
        public MoistureFallingBlock(boolean red, int stage, Properties properties) {
            super(properties);
            this.red = red;
            this.stage = stage;
        }
        @Override
        public int getDustColor(BlockState state, BlockGetter level, BlockPos pos) {
            return red ? 0xA04A2A : 0xDBD3A0;
        }
        @Override
        protected void randomTick(BlockState state, ServerLevel level, BlockPos pos, RandomSource random) {
            advance(state, level, pos, red, stage);
        }
    }

    public static final class MoistureBlock extends Block {
        private final boolean red;
        private final int stage;
        public MoistureBlock(boolean red, int stage, Properties properties) {
            super(properties);
            this.red = red;
            this.stage = stage;
        }
        @Override
        protected void randomTick(BlockState state, ServerLevel level, BlockPos pos, RandomSource random) {
            advance(state, level, pos, red, stage);
        }
    }
}
