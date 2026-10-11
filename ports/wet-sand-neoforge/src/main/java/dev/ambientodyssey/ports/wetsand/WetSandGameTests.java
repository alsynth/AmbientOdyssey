package dev.ambientodyssey.ports.wetsand;

import com.mojang.authlib.GameProfile;
import java.util.UUID;
import java.util.ArrayList;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.world.item.crafting.CraftingInput;
import net.minecraft.world.item.crafting.RecipeType;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.alchemy.PotionContents;
import net.minecraft.world.item.alchemy.Potions;
import net.minecraft.world.level.GameType;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.entity.BrushableBlockEntity;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.resources.ResourceKey;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.Vec3;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.neoforged.neoforge.common.NeoForge;
import net.neoforged.neoforge.common.util.FakePlayerFactory;
import net.neoforged.neoforge.event.entity.player.PlayerInteractEvent;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

@GameTestHolder(WetSandPort.ID)
@PrefixGameTestTemplate(false)
public final class WetSandGameTests {
    private static final BlockPos POS = new BlockPos(4, 2, 4);

    private static void tick(GameTestHelper helper) {
        BlockPos absolute = helper.absolutePos(POS);
        BlockState state = helper.getLevel().getBlockState(absolute);
        if (state.getBlock() instanceof WetSandPort.MoistureFallingBlock block) {
            block.randomTick(state, helper.getLevel(), absolute, helper.getLevel().getRandom());
        } else if (state.getBlock() instanceof WetSandPort.MoistureBlock block) {
            block.randomTick(state, helper.getLevel(), absolute, helper.getLevel().getRandom());
        } else {
            helper.fail("Expected a moisture block before tick");
        }
    }

    @GameTest(template = "empty")
    public static void hydrationAndBottleDryingPreserveBothSandTypes(GameTestHelper helper) {
        var player = FakePlayerFactory.get(helper.getLevel(), new GameProfile(UUID.randomUUID(), "sand-creative"));
        player.setGameMode(GameType.CREATIVE);
        player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(Items.GLASS_BOTTLE));
        for (boolean red : new boolean[]{false, true}) {
            helper.setBlock(POS.below(), Blocks.STONE);
            helper.setBlock(POS.east(), Blocks.WATER);
            helper.setBlock(POS, WetSandPort.humidityBlock(red, 1));
            for (int stage = 2; stage <= 3; stage++) {
                tick(helper);
                helper.assertBlockPresent(WetSandPort.humidityBlock(red, stage), POS);
            }
            tick(helper);
            helper.assertBlockPresent(WetSandPort.humidityBlock(red, 3), POS);
            helper.setBlock(POS.east(), Blocks.AIR);
            tick(helper);
            helper.assertBlockPresent(WetSandPort.humidityBlock(red, 3), POS);
            for (int stage = 2; stage >= 0; stage--) {
                BlockPos absolute = helper.absolutePos(POS);
                NeoForge.EVENT_BUS.post(new PlayerInteractEvent.RightClickBlock(player, InteractionHand.MAIN_HAND, absolute,
                        new BlockHitResult(Vec3.atCenterOf(absolute), Direction.UP, absolute, false)));
                helper.assertBlockPresent(WetSandPort.humidityBlock(red, stage), POS);
            }
        }
        helper.assertTrue(player.getMainHandItem().getCount() == 1, "Creative bottle must not be consumed");
        player.discard();
        helper.succeed();
    }

    @GameTest(template = "empty")
    public static void sourceWaterRangeIsBounded(GameTestHelper helper) {
        BlockPos absolute = helper.absolutePos(POS);
        helper.setBlock(POS.east(3), Blocks.WATER);
        helper.assertTrue(WetSandPort.hasNearbyWater(helper.getLevel(), absolute), "Source at range 3 must hydrate");
        helper.setBlock(POS.east(3), Blocks.AIR);
        helper.setBlock(POS.east(4), Blocks.WATER);
        helper.assertFalse(WetSandPort.hasNearbyWater(helper.getLevel(), absolute), "Source at range 4 must not hydrate");
        helper.succeed();
    }

    @GameTest(template = "empty")
    public static void caneSurvivesOnAllMoistureStages(GameTestHelper helper) {
        for (boolean red : new boolean[]{false, true}) {
            for (int stage = 2; stage <= 3; stage++) {
                helper.setBlock(POS, WetSandPort.humidityBlock(red, stage));
                helper.assertTrue(Blocks.SUGAR_CANE.defaultBlockState().canSurvive(helper.getLevel(), helper.absolutePos(POS.above())),
                        "Sugar cane must survive without adjacent water on hydrated sand");
            }
        }
        for (int stage = 2; stage <= 3; stage++) {
            helper.setBlock(POS, WetSandPort.archaeologyBlock(stage));
            helper.assertTrue(Blocks.SUGAR_CANE.defaultBlockState().canSurvive(helper.getLevel(), helper.absolutePos(POS.above())),
                    "Cane must survive on wet and soaked suspicious sand");
        }
        helper.setBlock(POS, WetSandPort.MOIST_SAND.get());
        helper.assertFalse(Blocks.SUGAR_CANE.defaultBlockState().canSurvive(helper.getLevel(), helper.absolutePos(POS.above())),
                "Moist sand must still require adjacent water");
        helper.setBlock(POS, Blocks.SAND);
        helper.assertFalse(Blocks.SUGAR_CANE.defaultBlockState().canSurvive(helper.getLevel(), helper.absolutePos(POS.above())),
                "Dry sand must still require vanilla water");
        helper.succeed();
    }

    @GameTest(template = "empty")
    public static void soakedCollisionIsLowered(GameTestHelper helper) {
        for (boolean red : new boolean[]{false, true}) {
            for (int stage = 2; stage <= 3; stage++) {
                BlockState state = WetSandPort.humidityBlock(red, stage).defaultBlockState();
                double height = state.getCollisionShape(helper.getLevel(), helper.absolutePos(POS), CollisionContext.empty()).max(Direction.Axis.Y);
                helper.assertTrue(height == (stage == 3 ? 14.0 / 16.0 : 1.0), "Incorrect wet/soaked collision height");
            }
        }
        helper.succeed();
    }

    @GameTest(template = "empty", timeoutTicks = 60)
    public static void moistFallsButWetAndSoakedStay(GameTestHelper helper) {
        helper.setBlock(new BlockPos(1, 0, 1), Blocks.STONE);
        helper.setBlock(new BlockPos(3, 0, 1), Blocks.STONE);
        helper.setBlock(new BlockPos(5, 0, 1), Blocks.STONE);
        helper.setBlock(new BlockPos(1, 3, 1), WetSandPort.MOIST_SAND.get());
        helper.setBlock(new BlockPos(3, 3, 1), WetSandPort.WET_SAND.get());
        helper.setBlock(new BlockPos(5, 3, 1), WetSandPort.SOAKED_SAND.get());
        helper.runAfterDelay(30, () -> {
            helper.assertBlockPresent(WetSandPort.MOIST_SAND.get(), new BlockPos(1, 1, 1));
            helper.assertBlockPresent(WetSandPort.WET_SAND.get(), new BlockPos(3, 3, 1));
            helper.assertBlockPresent(WetSandPort.SOAKED_SAND.get(), new BlockPos(5, 3, 1));
            helper.succeed();
        });
    }

    @GameTest(template = "empty")
    public static void survivalOffhandBottleConsumesCorrectStack(GameTestHelper helper) {
        var player = FakePlayerFactory.get(helper.getLevel(), new GameProfile(UUID.randomUUID(), "sand-survival"));
        player.setGameMode(GameType.SURVIVAL);
        player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(Items.STICK, 3));
        player.setItemInHand(InteractionHand.OFF_HAND, new ItemStack(Items.GLASS_BOTTLE, 2));
        helper.setBlock(POS, WetSandPort.WET_RED_SAND.get());
        BlockPos absolute = helper.absolutePos(POS);
        var event = new PlayerInteractEvent.RightClickBlock(player, InteractionHand.OFF_HAND, absolute,
                new BlockHitResult(Vec3.atCenterOf(absolute), Direction.UP, absolute, false));
        NeoForge.EVENT_BUS.post(event);
        helper.assertTrue(event.isCanceled(), "Bottle extraction must handle the event");
        helper.assertBlockPresent(WetSandPort.MOIST_RED_SAND.get(), POS);
        helper.assertTrue(player.getOffhandItem().getCount() == 1, "Exactly one offhand bottle must be consumed");
        helper.assertTrue(player.getMainHandItem().getCount() == 3, "Main hand must be untouched");
        helper.assertTrue(player.getInventory().contains(PotionContents.createItemStack(Items.POTION, Potions.WATER)), "Water potion must be delivered");
        player.discard();
        helper.succeed();
    }

    @GameTest(template = "empty")
    public static void spectatorCannotExtractWater(GameTestHelper helper) {
        var player = FakePlayerFactory.get(helper.getLevel(), new GameProfile(UUID.randomUUID(), "sand-spectator"));
        player.setGameMode(GameType.SPECTATOR);
        player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(Items.GLASS_BOTTLE));
        helper.setBlock(POS, WetSandPort.SOAKED_SAND.get());
        BlockPos absolute = helper.absolutePos(POS);
        NeoForge.EVENT_BUS.post(new PlayerInteractEvent.RightClickBlock(player, InteractionHand.MAIN_HAND, absolute,
                new BlockHitResult(Vec3.atCenterOf(absolute), Direction.UP, absolute, false)));
        helper.assertBlockPresent(WetSandPort.SOAKED_SAND.get(), POS);
        helper.assertTrue(player.getMainHandItem().getCount() == 1, "Spectator bottle must not be consumed");
        player.discard();
        helper.succeed();
    }

    @GameTest(template = "empty")
    public static void archaeologyLootSeedSurvivesTransitionsAndReload(GameTestHelper helper) {
        helper.setBlock(POS.below(), Blocks.STONE);
        helper.setBlock(POS, Blocks.SUSPICIOUS_SAND);
        BlockPos absolute = helper.absolutePos(POS);
        var entity = (BrushableBlockEntity) helper.getLevel().getBlockEntity(absolute);
        entity.setLootTable(ResourceKey.create(Registries.LOOT_TABLE, ResourceLocation.withDefaultNamespace("archaeology/desert_well")), 123456789L);
        for (int stage : new int[]{1, 2, 3, 2, 1, 0}) {
            helper.assertTrue(WetSandPort.transitionArchaeology(helper.getLevel(), absolute, stage), "Archaeology transition failed");
            helper.assertBlockPresent(WetSandPort.archaeologyBlock(stage), POS);
            var current = helper.getLevel().getBlockEntity(absolute);
            CompoundTag saved = current.saveWithFullMetadata(helper.getLevel().registryAccess());
            helper.assertTrue(saved.getString("LootTable").equals("minecraft:archaeology/desert_well"), "Loot table was lost");
            helper.assertTrue(saved.getLong("LootTableSeed") == 123456789L, "Treasure seed was lost");
            var reloaded = BlockEntity.loadStatic(absolute, helper.getBlockState(POS), saved, helper.getLevel().registryAccess());
            helper.assertTrue(reloaded instanceof BrushableBlockEntity, "Brushable entity failed saved-NBT reload");
            helper.getLevel().setBlockEntity(reloaded);
        }
        helper.succeed();
    }

    @GameTest(template = "empty")
    public static void realizedTreasureSurvivesAllMoistureChanges(GameTestHelper helper) {
        helper.setBlock(POS.below(), Blocks.STONE);
        helper.setBlock(POS, Blocks.SUSPICIOUS_SAND);
        BlockPos absolute = helper.absolutePos(POS);
        CompoundTag data = new CompoundTag();
        data.put("item", new ItemStack(Items.DIAMOND).save(helper.getLevel().registryAccess()));
        helper.getLevel().getBlockEntity(absolute).loadWithComponents(data, helper.getLevel().registryAccess());
        for (int stage : new int[]{1, 2, 3, 2, 1, 0}) {
            helper.assertTrue(WetSandPort.transitionArchaeology(helper.getLevel(), absolute, stage), "Archaeology transition failed");
            var entity = (BrushableBlockEntity) helper.getLevel().getBlockEntity(absolute);
            helper.assertTrue(entity.getItem().is(Items.DIAMOND) && entity.getItem().getCount() == 1, "Treasure changed or disappeared");
        }
        helper.succeed();
    }

    @GameTest(template = "empty")
    public static void activeBrushingIsNeverReplacedAndCompletesOnce(GameTestHelper helper) {
        helper.setBlock(POS.below(), Blocks.STONE);
        helper.setBlock(POS, WetSandPort.WET_SUSPICIOUS_SAND.get());
        BlockPos absolute = helper.absolutePos(POS);
        var entity = (BrushableBlockEntity) helper.getLevel().getBlockEntity(absolute);
        CompoundTag data = new CompoundTag();
        data.put("item", new ItemStack(Items.DIAMOND).save(helper.getLevel().registryAccess()));
        entity.loadWithComponents(data, helper.getLevel().registryAccess());
        var player = FakePlayerFactory.get(helper.getLevel(), new GameProfile(UUID.randomUUID(), "sand-brusher"));
        player.setGameMode(GameType.SURVIVAL);
        long start = helper.getLevel().getGameTime();
        entity.brush(start, player, Direction.UP);
        helper.assertTrue(helper.getBlockState(POS).getValue(BlockStateProperties.DUSTED) > 0, "Brushing did not start");
        helper.assertFalse(WetSandPort.transitionArchaeology(helper.getLevel(), absolute, 3), "Active brushing must prevent replacement");
        helper.assertTrue(helper.getLevel().getBlockEntity(absolute) == entity, "Active brush entity must stay identical");
        for (int brush = 1; brush < 10; brush++) entity.brush(start + brush * 10, player, Direction.UP);
        helper.assertBlockPresent(WetSandPort.WET_SAND.get(), POS);
        helper.assertItemEntityCountIs(Items.DIAMOND, POS, 2, 1);
        player.discard();
        helper.succeed();
    }

    @GameTest(template = "empty")
    public static void allSixteenConcreteRecipesCraftWithMixedMoisture(GameTestHelper helper) {
        String[] colors = {"white", "orange", "magenta", "light_blue", "yellow", "lime", "pink", "gray",
                "light_gray", "cyan", "purple", "blue", "brown", "green", "red", "black"};
        for (String color : colors) {
            var slots = new ArrayList<ItemStack>();
            slots.add(new ItemStack(BuiltInRegistries.ITEM.get(ResourceLocation.withDefaultNamespace(color + "_dye"))));
            for (int i = 0; i < 4; i++) slots.add(new ItemStack(Items.GRAVEL));
            for (int stage : new int[]{1, 2, 3, 1}) slots.add(new ItemStack(WetSandPort.humidityBlock(false, stage)));
            var input = CraftingInput.of(3, 3, slots);
            var match = helper.getLevel().getRecipeManager().getRecipeFor(RecipeType.CRAFTING, input, helper.getLevel());
            helper.assertTrue(match.isPresent(), "Missing concrete recipe for " + color);
            ItemStack result = match.orElseThrow().value().assemble(input, helper.getLevel().registryAccess());
            helper.assertTrue(result.is(BuiltInRegistries.ITEM.get(ResourceLocation.withDefaultNamespace(color + "_concrete")))
                    && result.getCount() == 8, "Wrong concrete result for " + color);
        }
        helper.succeed();
    }

    @GameTest(template = "empty")
    public static void allOrdinarySandVariantsDropExactlyOnce(GameTestHelper helper) {
        for (boolean red : new boolean[]{false, true}) {
            for (int stage = 1; stage <= 3; stage++) {
                Block block = WetSandPort.humidityBlock(red, stage);
                helper.setBlock(POS.below(), Blocks.STONE);
                helper.setBlock(POS, block);
                var drops = Block.getDrops(block.defaultBlockState(), helper.getLevel(), helper.absolutePos(POS), null);
                helper.assertTrue(drops.size() == 1 && drops.getFirst().is(block.asItem()) && drops.getFirst().getCount() == 1,
                        "Ordinary moisture sand must drop exactly one matching block item");
            }
        }
        helper.succeed();
    }

    @GameTest(template = "empty")
    public static void hydrationPropagatesAndStopsAtDistanceCeiling(GameTestHelper helper) {
        helper.setBlock(POS.east(3), Blocks.WATER);
        helper.setBlock(POS.east(2), WetSandPort.SOAKED_SAND.get());
        helper.setBlock(POS.east(), WetSandPort.WET_SAND.get());
        helper.assertTrue(WetSandPort.nextMoistureStage(helper.getLevel(), helper.absolutePos(POS), 0) == 1,
                "Dry sand at water distance 3 must receive moisture from wetter neighbor");
        helper.assertTrue(WetSandPort.nextMoistureStage(helper.getLevel(), helper.absolutePos(POS), 1) == 1,
                "Distance 3 must cap humidity at moist");
        helper.setBlock(POS.east(), Blocks.AIR);
        helper.assertTrue(WetSandPort.nextMoistureStage(helper.getLevel(), helper.absolutePos(POS), 0) == 0,
                "Distant water without adjacent wet sand must not skip propagation");
        helper.succeed();
    }

    @GameTest(template = "empty")
    public static void verticalFlowingWaterHydrates(GameTestHelper helper) {
        helper.setBlock(POS.above(), Blocks.WATER.defaultBlockState().setValue(net.minecraft.world.level.block.LiquidBlock.LEVEL, 4));
        helper.assertTrue(WetSandPort.nextMoistureStage(helper.getLevel(), helper.absolutePos(POS), 1) == 2,
                "Flowing water directly above must hydrate sand");
        helper.succeed();
    }
}
