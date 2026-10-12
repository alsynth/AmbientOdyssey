package dev.ambientodyssey.questlogbridge;

import com.mojang.logging.LogUtils;
import java.lang.reflect.Constructor;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.components.AbstractButton;
import net.minecraft.client.gui.components.Tooltip;
import net.minecraft.client.gui.narration.NarrationElementOutput;
import net.minecraft.client.gui.screens.inventory.AbstractContainerScreen;
import net.minecraft.resources.ResourceLocation;
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

    // Source-verified Better Inventory 1.3.2 atlas:
    // BetterInventoryLayout.SPR_TAB_X=220, SPR_TAB_Y=0, TAB_W=24,
    // TAB_H=20, alternate/selected row at v=21; atlas 512x256.
    // We reference the installed mod's pixels; do not duplicate its art.
    private static final ResourceLocation BETTER_INVENTORY_ATLAS =
            ResourceLocation.fromNamespaceAndPath("betterinventory", "textures/gui/inventory.png");
    private static final int TAB_U = 220;
    private static final int TAB_NORMAL_V = 0;
    private static final int TAB_SELECTED_V = 21;
    private static final int TAB_WIDTH = 24;
    private static final int TAB_HEIGHT = 20;
    private static final int ATLAS_WIDTH = 512;
    private static final int ATLAS_HEIGHT = 256;
    // Verified against the installed Better Inventory 1.3.2 JAR:
    // backpack tabs = left+134,158,182,206,230; crafting=254;
    // settings gear = left+280, width 20 (not the tab's width 24).
    // User-preferred Q tab: centered ABOVE the right armor panel (RIGHT_A_X=308, width=44).
    // Fall back to the previously verified above-gear slot on narrow screens.
    private static final int SETTINGS_X = 280;
    private static final int SETTINGS_WIDTH = 20;
    private static final int TAB_MARGIN = 2;

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

    private record Anchor(int x, int y) {}

    private static Anchor anchor(Screen screen) {
        if (!(screen instanceof AbstractContainerScreen<?> inventory)) {
            return new Anchor(Math.max(2, screen.width - TAB_WIDTH - 2), 2);
        }
        int left = inventory.getGuiLeft();
        int top = inventory.getGuiTop();
        int aboveArmor = left + 318;
        if (aboveArmor >= 2 && aboveArmor + TAB_WIDTH <= screen.width - 2 && top >= 2) {
            return new Anchor(aboveArmor, top);
        }
        int rightOfSettings = left + SETTINGS_X + SETTINGS_WIDTH + TAB_MARGIN;
        // Align with native settings on the same row without covering it.
        if (rightOfSettings + TAB_WIDTH <= screen.width - 2) {
            return new Anchor(rightOfSettings, top);
        }
        int above = top - TAB_HEIGHT - TAB_MARGIN;
        if (above >= 2) {
            return new Anchor(left + SETTINGS_X, above);
        }
        // Very tall GUI scale / short display: place Q BELOW the entire GUI
        // instead of overlapping backpack/crafting/gear at y=top.
        int below = top + inventory.getYSize() + TAB_MARGIN;
        if (below + TAB_HEIGHT <= screen.height - 2) {
            return new Anchor(left + SETTINGS_X, below);
        }
        // Last-resort side placement outside the native image bounds.
        int right = left + inventory.getXSize() + TAB_MARGIN;
        if (right + TAB_WIDTH <= screen.width - 2) {
            return new Anchor(right, Math.max(2, top));
        }
        return new Anchor(Math.max(2, left - TAB_WIDTH - TAB_MARGIN), Math.max(2, top));
    }

    private static int buttonX(Screen screen) {
        return anchor(screen).x();
    }

    private static int buttonY(Screen screen) {
        return anchor(screen).y();
    }

    /**
     * A Better Inventory tab, not a vanilla gray Minecraft button.
     * Exact source atlas and 24x20 sprite sizes are reused to match the
     * mod's native backpack/crafting tabs. Only the Q letter is original.
     */
    private static final class QuestlogTab extends AbstractButton {
        private final Screen parent;

        private QuestlogTab(Screen parent) {
            super(buttonX(parent), buttonY(parent), TAB_WIDTH, TAB_HEIGHT,
                    Component.literal("Q"));
            this.parent = parent;
            this.setTooltip(Tooltip.create(Component.translatable("questlog.gui.open")));
        }

        @Override
        protected void renderWidget(GuiGraphics graphics, int mouseX, int mouseY, float partialTick) {
            // Fix v0.1.1 position drift seen at GUI scale 3: screen layout may
            // recenter after this widget's initial bounds were assigned.
            // Update hitbox together with visual position, so buttons match.
            this.setX(buttonX(this.parent));
            this.setY(buttonY(this.parent));
            int v = this.isHoveredOrFocused() ? TAB_SELECTED_V : TAB_NORMAL_V;
            graphics.blit(BETTER_INVENTORY_ATLAS, this.getX(), this.getY(),
                    TAB_U, v, TAB_WIDTH, TAB_HEIGHT, ATLAS_WIDTH, ATLAS_HEIGHT);

            Minecraft minecraft = Minecraft.getInstance();
            String label = "Q";
            int x = this.getX() + (TAB_WIDTH - minecraft.font.width(label)) / 2;
            int y = this.getY() + 6;
            graphics.drawString(minecraft.font, label, x, y, 0xFFEADFC9, true);
        }

        @Override
        public void onPress() {
            openQuestlog(parent);
        }

        @Override
        protected void updateWidgetNarration(NarrationElementOutput output) {
            this.defaultButtonNarrationText(output);
        }
    }

    private static void onInit(ScreenEvent.Init.Post event) {
        final Screen screen = event.getScreen();
        if (!isTarget(screen)) return;

        event.addListener(new QuestlogTab(screen));
        lastBadgeTick = Long.MIN_VALUE;
        LOG.info("AO Questlog bridge 0.1.6: armor-top primary, safe fallbacks at {},{} (gui left={}, top={})",
                buttonX(screen), buttonY(screen),
                ((AbstractContainerScreen<?>) screen).getGuiLeft(),
                ((AbstractContainerScreen<?>) screen).getGuiTop());
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
        // Gold exclamation badge, offset over the native tab's upper-right.
        // Draw at render-post so it remains visible over widgets and tooltips.
        int x = buttonX(screen) + 16;
        int y = buttonY(screen) - 3;
        graphics.pose().pushPose();
        graphics.pose().translate(0, 0, 400);
        graphics.fill(x - 1, y - 1, x + 10, y + 12, 0xFF261D18);
        graphics.fill(x, y, x + 9, y + 11, 0xFFB75B22);
        graphics.fill(x + 1, y + 1, x + 8, y + 10, 0xFFF3C05C);
        graphics.drawString(minecraft.font, "!", x + 3, y + 1, 0xFF352318, false);
        graphics.pose().popPose();
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
