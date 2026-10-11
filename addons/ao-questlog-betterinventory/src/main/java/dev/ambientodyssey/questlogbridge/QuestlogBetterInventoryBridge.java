package dev.ambientodyssey.questlogbridge;

import com.mojang.logging.LogUtils;
import java.lang.reflect.Constructor;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.components.Tooltip;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.network.chat.Component;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.ModList;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.client.event.ScreenEvent;
import net.neoforged.neoforge.common.NeoForge;
import org.slf4j.Logger;

/**
 * Optional *client-only* bridge. No Questlog or Better Inventory classes are
 * statically referenced: the addon can be installed on an instance without
 * either mod and never changes their menus, packets or inventories.
 *
 * Depends on tested AO targets: Minecraft 1.21.1, NeoForge 21.1.252,
 * Better Inventory 1.3.2 and Questlog 3.4.1.
 */
@Mod(value = QuestlogBetterInventoryBridge.MODID, dist = Dist.CLIENT)
public final class QuestlogBetterInventoryBridge {
    public static final String MODID = "aoquestlogbridge";
    private static final String BETTER_INVENTORY_SCREEN =
            "dev.fallingcloud.betterinventory.client.screen.BetterInventoryScreen";
    private static final String QUESTLOG_SCREEN =
            "org.infernalstudios.questlog.client.gui.screen.QuestlogScreen";
    private static final Logger LOG = LogUtils.getLogger();

    private static long lastBadgeTick = Long.MIN_VALUE;
    private static boolean cachedBadge;

    public QuestlogBetterInventoryBridge(IEventBus modEventBus) {
        NeoForge.EVENT_BUS.addListener(QuestlogBetterInventoryBridge::onInit);
        NeoForge.EVENT_BUS.addListener(QuestlogBetterInventoryBridge::onRender);
    }

    private static boolean isTarget(Screen screen) {
        return screen.getClass().getName().equals(BETTER_INVENTORY_SCREEN)
                && ModList.get().isLoaded("questlog")
                && ModList.get().isLoaded("betterinventory");
    }

    private static int buttonX(Screen screen) {
        // Anchored to display edge, not the vanilla 176px InventoryScreen.
        // Avoids Better Inventory's backpack, crafting and Curios panels.
        return Math.max(4, screen.width - 26);
    }

    private static int buttonY(Screen screen) {
        return 6;
    }

    private static void onInit(ScreenEvent.Init.Post event) {
        final Screen screen = event.getScreen();
        if (!isTarget(screen)) return;

        Button button = Button.builder(Component.literal("Q"), unused -> openQuestlog(screen))
                .bounds(buttonX(screen), buttonY(screen), 20, 20)
                .tooltip(Tooltip.create(Component.translatable("questlog.gui.open")))
                .build();
        event.addListener(button);
        lastBadgeTick = Long.MIN_VALUE;
        LOG.debug("Attached Questlog access button to BetterInventoryScreen");
    }

    private static void openQuestlog(Screen parent) {
        Minecraft minecraft = Minecraft.getInstance();
        if (minecraft.screen != parent || minecraft.player == null) return;

        try {
            Class<?> type = Class.forName(QUESTLOG_SCREEN);
            Constructor<?> constructor = type.getConstructor(Screen.class);
            Screen journal = (Screen) constructor.newInstance(parent);
            minecraft.setScreen(journal);
        } catch (ReflectiveOperationException | LinkageError e) {
            LOG.error("Failed to open Questlog from Better Inventory. Check Questlog 3.4.1 compatibility", e);
            minecraft.player.displayClientMessage(
                    Component.literal("Could not open Questlog — see latest.log"), true);
        }
    }

    private static void onRender(ScreenEvent.Render.Post event) {
        Screen screen = event.getScreen();
        if (!isTarget(screen) || !showsBadge()) return;
        Minecraft minecraft = Minecraft.getInstance();
        if (minecraft.level == null) return;

        // Check unclaimed rewards once per second, but show immediate Questlog
        // notifications as soon as received, matching its own button's rules.
        long tick = minecraft.level.getGameTime();
        if (tick < lastBadgeTick || tick - lastBadgeTick >= 20) {
            cachedBadge = hasQuestlogNotification();
            lastBadgeTick = tick;
        } else if (!cachedBadge) {
            cachedBadge = hasRecentNotification();
        }
        if (!cachedBadge) return;

        GuiGraphics graphics = event.getGuiGraphics();
        int x = buttonX(screen) + 14;
        int y = buttonY(screen) - 3;
        graphics.fill(x, y, x + 8, y + 9, 0xFF5B270E);
        graphics.fill(x + 1, y + 1, x + 7, y + 8, 0xFFFFC65B);
        graphics.drawString(minecraft.font, "!", x + 2, y, 0xFF2A1400, false);
    }

    private static boolean showsBadge() {
        try {
            Class<?> configHost = Class.forName("org.infernalstudios.questlog.Questlog");
            Object config = configHost.getMethod("getConfig").invoke(null);
            Field button = config.getClass().getField("button");
            Object settings = button.get(config);
            return settings.getClass().getField("showBadge").getBoolean(settings);
        } catch (ReflectiveOperationException | LinkageError ignored) {
            return true; // Prefer a notification over silently hiding it.
        }
    }

    private static boolean hasRecentNotification() {
        try {
            Class<?> events = Class.forName("org.infernalstudios.questlog.QuestlogClientEvents");
            return events.getField("mostRecentNotificationQuest").get(null) != null;
        } catch (ReflectiveOperationException | LinkageError ignored) {
            return false;
        }
    }

    private static boolean hasQuestlogNotification() {
        if (hasRecentNotification()) return true;
        try {
            Class<?> client = Class.forName("org.infernalstudios.questlog.QuestlogClient");
            Object manager = client.getMethod("getLocal").invoke(null);
            if (manager == null) return false;
            Object quests = manager.getClass().getMethod("getAllQuests").invoke(manager);
            if (!(quests instanceof Iterable<?> entries)) return false;

            for (Object quest : entries) {
                Class<?> type = quest.getClass();
                Method completed = type.getMethod("isCompleted");
                Method rewarded = type.getMethod("isRewarded");
                if (Boolean.TRUE.equals(completed.invoke(quest))
                        && Boolean.FALSE.equals(rewarded.invoke(quest))) {
                    return true;
                }
            }
        } catch (ReflectiveOperationException | LinkageError e) {
            LOG.debug("Questlog badge-state lookup unavailable", e);
        }
        return false;
    }
}
