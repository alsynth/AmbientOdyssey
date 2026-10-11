package dev.ambientodyssey.ports.wetsand;

import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.screens.TitleScreen;
import net.minecraft.client.gui.screens.AccessibilityOnboardingScreen;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.inventory.InventoryMenu;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.ClientTickEvent;

/** Opt-in test hook; never exits an ordinary player session. */
@EventBusSubscriber(modid = WetSandPort.ID, value = Dist.CLIENT)
public final class WetSandClientSmoke {
    private static final org.slf4j.Logger LOGGER = com.mojang.logging.LogUtils.getLogger();
    private static int readyTicks;
    private static boolean finished;

    @SubscribeEvent
    public static void onTick(ClientTickEvent.Post event) {
        if (!Boolean.getBoolean("ao_wet_sand.clientSmoke") || finished) return;
        Minecraft minecraft = Minecraft.getInstance();
        if (minecraft.screen instanceof AccessibilityOnboardingScreen && minecraft.getOverlay() == null) {
            minecraft.setScreen(new TitleScreen());
            return;
        }
        if (!(minecraft.screen instanceof TitleScreen) || minecraft.getOverlay() != null || ++readyTicks < 40) return;
        finished = true;
        try {
            int models = 0;
            for (boolean red : new boolean[]{false, true}) {
                for (int stage = 1; stage <= 3; stage++) {
                    Block block = WetSandPort.humidityBlock(red, stage);
                    String name = (stage == 1 ? "moist" : stage == 2 ? "wet" : "soaked") + (red ? "_red" : "") + "_sand";
                    checkSprite(minecraft, name);
                    var model = minecraft.getBlockRenderer().getBlockModel(block.defaultBlockState());
                    if (!model.getParticleIcon().contents().name().equals(ResourceLocation.fromNamespaceAndPath(WetSandPort.ID, "block/" + name))) {
                        throw new IllegalStateException("Incorrect baked particle sprite for " + name);
                    }
                    models++;
                }
            }
            for (int stage = 1; stage <= 3; stage++) {
                String name = (stage == 1 ? "moist" : stage == 2 ? "wet" : "soaked") + "_suspicious_sand";
                for (int dusted = 0; dusted < 4; dusted++) {
                    checkSprite(minecraft, name + "_" + dusted);
                    var state = WetSandPort.archaeologyBlock(stage).defaultBlockState().setValue(BlockStateProperties.DUSTED, dusted);
                    var model = minecraft.getBlockRenderer().getBlockModel(state);
                    if (!model.getParticleIcon().contents().name().equals(ResourceLocation.fromNamespaceAndPath(WetSandPort.ID, "block/" + name + "_" + dusted))) {
                        throw new IllegalStateException("Incorrect baked brush model for " + name + " dusted=" + dusted);
                    }
                    models++;
                }
            }
            LOGGER.info("WETSAND_CLIENT_SMOKE_PASS: title screen rendered, 18 native baked block models and texture atlas sprites resolved");
        } catch (Exception failure) {
            LOGGER.error("WETSAND_CLIENT_SMOKE_FAIL", failure);
        } finally {
            minecraft.stop();
        }
    }

    private static void checkSprite(Minecraft minecraft, String name) {
        ResourceLocation expected = ResourceLocation.fromNamespaceAndPath(WetSandPort.ID, "block/" + name);
        var sprite = minecraft.getTextureAtlas(InventoryMenu.BLOCK_ATLAS).apply(expected);
        if (!sprite.contents().name().equals(expected)) throw new IllegalStateException("Missing atlas sprite " + expected);
    }
}
