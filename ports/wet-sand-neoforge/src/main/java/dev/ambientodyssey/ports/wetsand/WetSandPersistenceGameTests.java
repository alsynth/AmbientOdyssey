package dev.ambientodyssey.ports.wetsand;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.registries.Registries;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.GameType;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.entity.BrushableBlockEntity;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.Vec3;
import net.neoforged.neoforge.common.NeoForge;
import net.neoforged.neoforge.common.util.FakePlayerFactory;
import net.neoforged.neoforge.event.entity.player.PlayerInteractEvent;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import com.mojang.authlib.GameProfile;
import java.util.UUID;

/** Registered only for explicit, separate writer and reader JVM invocations. */
@PrefixGameTestTemplate(false)
public final class WetSandPersistenceGameTests {
    private static final org.slf4j.Logger LOGGER = com.mojang.logging.LogUtils.getLogger();
    private static final BlockPos ANCHOR = new BlockPos(-400, 80, -400);
    private static final long SEED = 876543210L;

    @GameTest(template = "empty", templateNamespace = WetSandPort.ID)
    public static void savedArchaeologySurvivesServerRestart(GameTestHelper helper) {
        var level = helper.getLevel();
        level.getChunkAt(ANCHOR);
        String phase = System.getProperty("ao_wet_sand.persistencePhase");
        if ("write".equals(phase)) {
            level.getEntitiesOfClass(ItemEntity.class, new AABB(ANCHOR).inflate(2)).forEach(ItemEntity::discard);
            level.setBlockAndUpdate(ANCHOR.below(), Blocks.STONE.defaultBlockState());
            level.setBlockAndUpdate(ANCHOR, WetSandPort.SOAKED_SUSPICIOUS_SAND.get().defaultBlockState());
            var entity = (BrushableBlockEntity) level.getBlockEntity(ANCHOR);
            entity.setLootTable(ResourceKey.create(Registries.LOOT_TABLE,
                    ResourceLocation.withDefaultNamespace("archaeology/desert_well")), SEED);
            entity.setChanged();
            level.setBlockAndUpdate(ANCHOR.east().below(), Blocks.STONE.defaultBlockState());
            level.setBlockAndUpdate(ANCHOR.east(), WetSandPort.WET_RED_SAND.get().defaultBlockState());
            LOGGER.info("WETSAND_PERSISTENCE_WRITE: treasure seed and both sand variants staged for server shutdown save");
        } else if ("read".equals(phase)) {
            helper.assertTrue(level.getBlockState(ANCHOR).is(WetSandPort.SOAKED_SUSPICIOUS_SAND.get()), "Saved suspicious stage missing after restart");
            helper.assertTrue(level.getBlockState(ANCHOR.east()).is(WetSandPort.WET_RED_SAND.get()), "Saved red sand stage missing after restart");
            helper.assertTrue(level.getBlockEntity(ANCHOR) instanceof BrushableBlockEntity, "Saved brushable entity missing");
            var entity = (BrushableBlockEntity) level.getBlockEntity(ANCHOR);
            var saved = entity.saveWithoutMetadata(level.registryAccess());
            helper.assertTrue(saved.getLong("LootTableSeed") == SEED && saved.getString("LootTable").equals("minecraft:archaeology/desert_well"),
                    "Saved treasure table/seed changed across process restart");
            var player = FakePlayerFactory.get(level, new GameProfile(UUID.randomUUID(), "sand-restart"));
            player.setGameMode(GameType.SURVIVAL);
            player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(Items.GLASS_BOTTLE));
            NeoForge.EVENT_BUS.post(new PlayerInteractEvent.RightClickBlock(player, InteractionHand.MAIN_HAND, ANCHOR,
                    new BlockHitResult(Vec3.atCenterOf(ANCHOR), Direction.UP, ANCHOR, false)));
            helper.assertTrue(level.getBlockState(ANCHOR).is(WetSandPort.WET_SUSPICIOUS_SAND.get()), "Bottle extraction failed after restart");
            entity = (BrushableBlockEntity) level.getBlockEntity(ANCHOR);
            long time = level.getGameTime();
            entity.brush(time, player, Direction.UP);
            ItemStack treasure = entity.getItem().copy();
            helper.assertFalse(treasure.isEmpty(), "Real desert-well loot did not resolve");
            for (int i = 1; i < 10; i++) entity.brush(time + i * 10, player, Direction.UP);
            helper.assertTrue(level.getBlockState(ANCHOR).is(WetSandPort.WET_SAND.get()), "Brushing left incorrect sand stage");
            var drops = level.getEntitiesOfClass(ItemEntity.class, new AABB(ANCHOR).inflate(2));
            helper.assertTrue(drops.size() == 1 && ItemStack.isSameItemSameComponents(drops.getFirst().getItem(), treasure)
                    && drops.getFirst().getItem().getCount() == treasure.getCount(), "Restarted treasure must drop exactly once");
            player.discard();
            LOGGER.info("WETSAND_PERSISTENCE_READ: saved stages, treasure seed, bottle extraction and real archaeology loot PASS");
        } else helper.fail("Persistence phase must be write or read");
        helper.succeed();
    }
}
