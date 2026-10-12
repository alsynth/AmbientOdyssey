package dev.ambientodyssey.questlogbridge;

import java.nio.file.Files;
import net.minecraft.client.Minecraft;
import net.minecraft.client.Screenshot;
import net.minecraft.client.gui.components.AbstractButton;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.client.gui.screens.TitleScreen;
import net.minecraft.client.gui.screens.AccessibilityOnboardingScreen;
import net.minecraft.client.gui.screens.inventory.AbstractContainerScreen;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.world.Difficulty;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.level.GameRules;
import net.minecraft.world.level.GameType;
import net.minecraft.world.level.LevelSettings;
import net.minecraft.world.level.WorldDataConfiguration;
import net.minecraft.world.level.levelgen.WorldOptions;
import net.minecraft.world.level.levelgen.presets.WorldPresets;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.ClientTickEvent;

/** Opt-in isolated native-client QA; dormant in ordinary installations. */
@EventBusSubscriber(modid = QuestlogBetterInventoryBridge.MODID, value = Dist.CLIENT)
public final class QuestlogPlacementQA {
    private static final org.slf4j.Logger LOG = com.mojang.logging.LogUtils.getLogger();
    private static final long START = System.nanoTime();
    private static boolean opening;
    private static boolean finished;
    private static int scale = 2;
    private static int waitTicks;
    private static AbstractContainerScreen<?> inventory;

    @SubscribeEvent
    public static void tick(ClientTickEvent.Post event) {
        if (!Boolean.getBoolean("aoquestlogbridge.clientQA") || finished) return;
        var mc = Minecraft.getInstance();
        try {
            if (System.nanoTime() - START > 240_000_000_000L) throw new IllegalStateException("QA timed out");
            if (mc.screen instanceof AccessibilityOnboardingScreen && mc.getOverlay() == null) {
                mc.setScreen(new TitleScreen());
                return;
            }
            if (!opening && mc.screen instanceof TitleScreen && mc.getOverlay() == null) {
                opening = true;
                mc.options.onboardAccessibility = false;
                mc.options.renderDistance().set(2);
                mc.options.simulationDistance().set(2);
                var settings = new LevelSettings("Questlog placement QA", GameType.CREATIVE, false,
                        Difficulty.PEACEFUL, true, new GameRules(), WorldDataConfiguration.DEFAULT);
                if (Files.exists(mc.gameDirectory.toPath().resolve("saves/questlog-placement-qa/level.dat"))) {
                    mc.createWorldOpenFlows().openWorld("questlog-placement-qa", () -> mc.setScreen(new TitleScreen()));
                } else {
                    mc.createWorldOpenFlows().createFreshLevel("questlog-placement-qa", settings,
                            new WorldOptions(7531, false, false), access -> access.registryOrThrow(Registries.WORLD_PRESET)
                                    .getHolderOrThrow(WorldPresets.FLAT).value().createWorldDimensions(), new TitleScreen());
                }
                return;
            }
            if (mc.player == null || mc.level == null || mc.getOverlay() != null) return;
            if (inventory == null) {
                if (++waitTicks < 60) return;
                mc.options.guiScale().set(scale);
                mc.resizeDisplay();
                var menuClass = Class.forName("dev.fallingcloud.betterinventory.menu.BetterInventoryMenu");
                var menu = menuClass.getConstructor(int.class, Inventory.class).newInstance(0, mc.player.getInventory());
                var screenClass = Class.forName("dev.fallingcloud.betterinventory.client.screen.BetterInventoryScreen");
                inventory = (AbstractContainerScreen<?>) screenClass
                        .getConstructor(menuClass, Inventory.class, Component.class)
                        .newInstance(menu, mc.player.getInventory(), Component.literal("Inventory QA"));
                mc.setScreen(inventory);
                waitTicks = 0;
                return;
            }
            if (++waitTicks < 40) return; // Allow native render and widget repositioning.
            var tabs = inventory.children().stream().filter(c -> c instanceof AbstractButton b
                    && b.getMessage().getString().equals("Q")).toList();
            if (tabs.size() != 1) throw new IllegalStateException("Expected one Q tab, found " + tabs.size());
            var q = (AbstractButton) tabs.getFirst();
            var layout = Class.forName("dev.fallingcloud.betterinventory.BetterInventoryLayout");
            int settingsX = layout.getField("SETTINGS_X").getInt(null);
            int settingsWidth = layout.getField("SETTINGS_SIZE").getInt(null);
            int expectedX = inventory.getGuiLeft() + layout.getField("RIGHT_A_X").getInt(null) + 10;
            if (q.getX() != expectedX || q.getY() != inventory.getGuiTop())
                throw new IllegalStateException("Q is not centered above the right armor panel: " + q.getX() + "," + q.getY());
            if (q.getX() + q.getWidth() > inventory.width || q.getY() < 0)
                throw new IllegalStateException("Q is off-screen");
            var path = mc.gameDirectory.toPath().resolve("questlog-scale-" + scale + ".png");
            try (var screenshot = Screenshot.takeScreenshot(mc.getMainRenderTarget())) { screenshot.writeToFile(path); }
            if (!inventory.mouseClicked(q.getX() + 12, q.getY() + 10, 0)
                    || !mc.screen.getClass().getName().equals("org.infernalstudios.questlog.client.gui.screen.QuestlogScreen"))
                throw new IllegalStateException("Q click did not open Questlog");
            mc.screen.keyPressed(256, 0, 0); // Native Questlog handles Escape in keyPressed.
            if (mc.screen != inventory) throw new IllegalStateException("Questlog did not return to the parent inventory");
            LOG.info("QUESTLOG_PLACEMENT_SCALE_PASS: scale={}, gear={}..{}, Q={},{}; native click/return passed",
                    scale, inventory.getGuiLeft() + settingsX, inventory.getGuiLeft() + settingsX + settingsWidth,
                    q.getX(), q.getY());
            if (++scale > 4) {
                finished = true;
                LOG.info("QUESTLOG_PLACEMENT_QA_PASS: scales 2/3/4 rendered, Q hitbox opens journal and returns");
                mc.stop();
            } else {
                inventory = null;
                waitTicks = 0;
                mc.setScreen(null);
            }
        } catch (Exception | LinkageError failure) {
            finished = true;
            LOG.error("QUESTLOG_PLACEMENT_QA_FAIL", failure);
            mc.stop();
        }
    }
}
