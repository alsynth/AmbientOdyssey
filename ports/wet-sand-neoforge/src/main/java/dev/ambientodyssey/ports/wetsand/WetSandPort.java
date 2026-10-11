package dev.ambientodyssey.ports.wetsand;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.level.block.BrushableBlock;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.entity.BrushableBlockEntity;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.neoforged.neoforge.event.BlockEntityTypeAddBlocksEvent;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.VoxelShape;
import net.neoforged.neoforge.common.util.TriState;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.alchemy.PotionContents;
import net.minecraft.world.item.alchemy.Potions;
import net.neoforged.neoforge.event.entity.player.PlayerInteractEvent;
import com.mojang.serialization.MapCodec;
import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
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
import net.neoforged.bus.api.EventPriority;
import net.neoforged.neoforge.event.RegisterGameTestsEvent;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.registries.DeferredBlock;
import net.neoforged.neoforge.registries.DeferredItem;
import net.neoforged.neoforge.registries.DeferredRegister;

/**
 * Native NeoForge PORT PROTOTYPE, not the original Wet Sand mod.
 *
 * Six moisture variants, bounded conversion of loaded ordinary sand, and
 * bottle extraction with treasure-preserving archaeology transitions.
 * Upstream worldgen replacement remains excluded for AO terrain compatibility.
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
    public static final DeferredBlock<Block> MOIST_SUSPICIOUS_SAND = archaeologyStage("moist_suspicious_sand", 1);
    public static final DeferredBlock<Block> WET_SUSPICIOUS_SAND = archaeologyStage("wet_suspicious_sand", 2);
    public static final DeferredBlock<Block> SOAKED_SUSPICIOUS_SAND = archaeologyStage("soaked_suspicious_sand", 3);

    private static DeferredBlock<Block> archaeologyStage(String name, int stage) {
        DeferredBlock<Block> block = BLOCKS.register(name, () -> new MoistureBrushableBlock(stage,
                BlockBehaviour.Properties.ofFullCopy(Blocks.SUSPICIOUS_SAND).randomTicks()));
        ITEMS.register(name, () -> new BlockItem(block.get(), new Item.Properties()));
        return block;
    }

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
        modBus.addListener((BlockEntityTypeAddBlocksEvent event) -> event.modify(BlockEntityType.BRUSHABLE_BLOCK,
                MOIST_SUSPICIOUS_SAND.get(), WET_SUSPICIOUS_SAND.get(), SOAKED_SUSPICIOUS_SAND.get()));
        NeoForge.EVENT_BUS.addListener(WetSandPort::updateNearbyShorelines);
        NeoForge.EVENT_BUS.addListener(EventPriority.LOWEST, WetSandPort::dehydrateWithBottle);
        if (System.getProperty("ao_wet_sand.persistencePhase") != null) {
            modBus.addListener((RegisterGameTestsEvent event) -> event.register(WetSandPersistenceGameTests.class));
        }
    }

    /** Use a glass bottle to remove one moisture stage and receive a water bottle. */
    private static void dehydrateWithBottle(PlayerInteractEvent.RightClickBlock event) {
        if (!(event.getLevel() instanceof ServerLevel level)) return;
        if (event.getEntity().isSpectator() || !event.getEntity().mayBuild()
                || !level.mayInteract(event.getEntity(), event.getPos())) return;
        if (!event.getItemStack().is(Items.GLASS_BOTTLE)) return;
        BlockPos pos = event.getPos();
        Block block = level.getBlockState(pos).getBlock();
        boolean red;
        int stage;
        if (block instanceof MoistureFallingBlock moist) {
            red = moist.red;
            stage = moist.stage;
        } else if (block instanceof MoistureBlock moist) {
            red = moist.red;
            stage = moist.stage;
        } else if (block instanceof MoistureBrushableBlock moist) {
            if (!transitionArchaeology(level, pos, moist.stage - 1)) return;
            deliverWaterBottle(event);
            return;
        } else return;
        if (stage <= 0) return;
        if (!level.setBlock(pos, humidityBlock(red, stage-1).defaultBlockState(), 3)) return;
        deliverWaterBottle(event);
    }

    private static void deliverWaterBottle(PlayerInteractEvent.RightClickBlock event) {
        var player = event.getEntity();
        if (!player.getAbilities().instabuild) {
            event.getItemStack().shrink(1);
            ItemStack result = PotionContents.createItemStack(Items.POTION, Potions.WATER);
            if (!player.addItem(result)) player.drop(result, false);
        }
        event.setCancellationResult(InteractionResult.SUCCESS);
        event.setCanceled(true);
    }

    static Block humidityBlock(boolean red,int stage) {
        return switch (stage) {
            case 0 -> red ? Blocks.RED_SAND : Blocks.SAND;
            case 1 -> red ? MOIST_RED_SAND.get() : MOIST_SAND.get();
            case 2 -> red ? WET_RED_SAND.get() : WET_SAND.get();
            default -> red ? SOAKED_RED_SAND.get() : SOAKED_SAND.get();
        };
    }

    static Block archaeologyBlock(int stage) {
        return switch (stage) {
            case 0 -> Blocks.SUSPICIOUS_SAND;
            case 1 -> MOIST_SUSPICIOUS_SAND.get();
            case 2 -> WET_SUSPICIOUS_SAND.get();
            default -> SOAKED_SUSPICIOUS_SAND.get();
        };
    }

    /** Never replace an actively brushed block. Transfer full saved treasure data before notifying clients. */
    static boolean transitionArchaeology(ServerLevel level, BlockPos pos, int target) {
        BlockState previous = level.getBlockState(pos);
        if (!(previous.getBlock() instanceof BrushableBlock)
                || previous.getValue(BlockStateProperties.DUSTED) != 0
                || !(level.getBlockEntity(pos) instanceof BrushableBlockEntity entity)) return false;
        CompoundTag data = entity.saveWithoutMetadata(level.registryAccess());
        BlockState next = archaeologyBlock(target).defaultBlockState();
        if (!level.setBlock(pos, next, 2)) return false;
        if (!(level.getBlockEntity(pos) instanceof BrushableBlockEntity replacement)) {
            // Fail closed if another mod prevented the expected block entity creation.
            level.setBlock(pos, previous, 2);
            if (level.getBlockEntity(pos) instanceof BrushableBlockEntity restored) {
                restored.loadWithComponents(data, level.registryAccess());
                restored.setChanged();
            }
            return false;
        }
        replacement.loadWithComponents(data, level.registryAccess());
        replacement.setChanged();
        level.sendBlockUpdated(pos, previous, next, 3);
        level.updateNeighborsAt(pos, next.getBlock());
        return true;
    }

    /** Eight candidates/player/second; each visits at most 343 loaded positions and six neighbors. */
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
                if (old == Blocks.SUSPICIOUS_SAND) {
                    if (nextMoistureStage(level, pos, 0) > 0) transitionArchaeology(level, pos, 1);
                    continue;
                }
                if (old != Blocks.SAND && old != Blocks.RED_SAND) continue;
                if (nextMoistureStage(level, pos, 0) > 0) level.setBlock(pos,(old==Blocks.SAND ? MOIST_SAND : MOIST_RED_SAND).get().defaultBlockState(),3);
            }
        }
    }

    static boolean hasNearbyWater(ServerLevel level, BlockPos pos) {
        return waterMoistureCeiling(level, pos) > 0;
    }

    /** Source and flowing water influence a loaded-only three-dimensional radius. */
    private static int waterMoistureCeiling(ServerLevel level, BlockPos pos) {
        int ceiling = 0;
        for (int dx = -3; dx <= 3; dx++) {
            for (int dy = -3; dy <= 3; dy++) {
                for (int dz = -3; dz <= 3; dz++) {
                    BlockPos nearby = pos.offset(dx, dy, dz);
                    if (!level.hasChunkAt(nearby)) continue;
                    if (level.getFluidState(nearby).is(FluidTags.WATER)) {
                        int distance = Math.max(Math.abs(dx), Math.max(Math.abs(dy), Math.abs(dz)));
                        ceiling = Math.max(ceiling, Math.min(3, 4 - distance));
                        if (ceiling == 3) return ceiling;
                    }
                }
            }
        }
        return ceiling;
    }

    static int nextMoistureStage(ServerLevel level, BlockPos pos, int current) {
        if (current >= 3 || current >= waterMoistureCeiling(level, pos)) return current;
        for (Direction direction : Direction.values()) {
            BlockPos adjacent = pos.relative(direction);
            if (!level.hasChunkAt(adjacent)) continue;
            if (level.getFluidState(adjacent).is(FluidTags.WATER)) return current + 1;
            Block neighbor = level.getBlockState(adjacent).getBlock();
            int stage = neighbor instanceof MoistureFallingBlock moist ? moist.stage
                    : neighbor instanceof MoistureBlock moist ? moist.stage
                    : neighbor instanceof MoistureBrushableBlock moist ? moist.stage : 0;
            if (stage > current) return current + 1;
        }
        return current;
    }

    private static void advance(BlockState state, ServerLevel level, BlockPos pos, boolean red, int stage) {
        int target = nextMoistureStage(level, pos, stage);
        if (target == stage) return;
        Block next = humidityBlock(red, target);
        level.setBlock(pos, next.defaultBlockState(), 3);
    }

    /** Moist sand inherits vanilla gravity; wet and soaked stages are stable. */
    public static final class MoistureFallingBlock extends FallingBlock {
        public static final MapCodec<MoistureFallingBlock> CODEC = RecordCodecBuilder.mapCodec(
                instance -> instance.group(
                        Codec.BOOL.fieldOf("red").forGetter(block -> block.red),
                        propertiesCodec()
                ).apply(instance, (red, properties) -> new MoistureFallingBlock(red, 1, properties)));
        @Override public MapCodec<? extends FallingBlock> codec() { return CODEC; }
        private final boolean red;
        private final int stage;
        public MoistureFallingBlock(boolean red, int stage, Properties properties) {
            super(properties);
            this.red = red;
            this.stage = stage;
        }
        @Override
        public TriState canSustainPlant(BlockState state, BlockGetter level, BlockPos pos,
                Direction facing, BlockState plant) {
            return TriState.DEFAULT;
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
        public static final MapCodec<MoistureBlock> CODEC = RecordCodecBuilder.mapCodec(
                instance -> instance.group(
                        Codec.BOOL.fieldOf("red").forGetter(block -> block.red),
                        Codec.intRange(2, 3).fieldOf("stage").forGetter(block -> block.stage),
                        propertiesCodec()
                ).apply(instance, MoistureBlock::new));
        private static final VoxelShape SOAKED_COLLISION = Block.box(0, 0, 0, 16, 14, 16);
        @Override public MapCodec<? extends Block> codec() { return CODEC; }
        private final boolean red;
        private final int stage;
        public MoistureBlock(boolean red, int stage, Properties properties) {
            super(properties);
            this.red = red;
            this.stage = stage;
        }
        @Override
        public TriState canSustainPlant(BlockState state, BlockGetter level, BlockPos pos,
                Direction facing, BlockState plant) {
            return facing == Direction.UP && plant.is(Blocks.SUGAR_CANE) ? TriState.TRUE : TriState.DEFAULT;
        }
        @Override
        protected VoxelShape getCollisionShape(BlockState state, BlockGetter level, BlockPos pos,
                CollisionContext context) {
            return stage == 3 ? SOAKED_COLLISION : super.getCollisionShape(state, level, pos, context);
        }
        @Override
        protected void randomTick(BlockState state, ServerLevel level, BlockPos pos, RandomSource random) {
            advance(state, level, pos, red, stage);
        }
    }

    public static final class MoistureBrushableBlock extends BrushableBlock {
        public static final MapCodec<BrushableBlock> MOISTURE_CODEC = RecordCodecBuilder.mapCodec(
                instance -> instance.group(
                        Codec.intRange(1, 3).fieldOf("stage").forGetter(block -> ((MoistureBrushableBlock) block).stage),
                        propertiesCodec()
                ).apply(instance, MoistureBrushableBlock::new));
        private final int stage;

        public MoistureBrushableBlock(int stage, Properties properties) {
            super(humidityBlock(false, stage), SoundEvents.BRUSH_SAND, SoundEvents.BRUSH_SAND_COMPLETED, properties);
            this.stage = stage;
        }

        @Override public MapCodec<BrushableBlock> codec() { return MOISTURE_CODEC; }

        @Override
        public TriState canSustainPlant(BlockState state, BlockGetter level, BlockPos pos,
                Direction facing, BlockState plant) {
            return stage >= 2 && facing == Direction.UP && plant.is(Blocks.SUGAR_CANE) ? TriState.TRUE : TriState.DEFAULT;
        }

        @Override
        public void tick(BlockState state, ServerLevel level, BlockPos pos, RandomSource random) {
            if (stage == 1) super.tick(state, level, pos, random);
            else if (level.getBlockEntity(pos) instanceof BrushableBlockEntity entity) entity.checkReset();
        }

        @Override
        protected void randomTick(BlockState state, ServerLevel level, BlockPos pos, RandomSource random) {
            int target = nextMoistureStage(level, pos, stage);
            if (target != stage) transitionArchaeology(level, pos, target);
        }

        @Override
        protected VoxelShape getCollisionShape(BlockState state, BlockGetter level, BlockPos pos, CollisionContext context) {
            return stage == 3 ? MoistureBlock.SOAKED_COLLISION : super.getCollisionShape(state, level, pos, context);
        }
    }
}
