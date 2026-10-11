package dev.ambientodyssey.ports.wetsand;

import com.mojang.authlib.GameProfile;
import java.util.UUID;
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
    public static void hydrationAndDryingPreserveBothSandTypes(GameTestHelper helper) {
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
            for (int stage = 2; stage >= 0; stage--) {
                tick(helper);
                helper.assertBlockPresent(WetSandPort.humidityBlock(red, stage), POS);
            }
        }
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
            for (int stage = 1; stage <= 3; stage++) {
                helper.setBlock(POS, WetSandPort.humidityBlock(red, stage));
                helper.assertTrue(Blocks.SUGAR_CANE.defaultBlockState().canSurvive(helper.getLevel(), helper.absolutePos(POS.above())),
                        "Sugar cane must survive without adjacent water on hydrated sand");
            }
        }
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
}
