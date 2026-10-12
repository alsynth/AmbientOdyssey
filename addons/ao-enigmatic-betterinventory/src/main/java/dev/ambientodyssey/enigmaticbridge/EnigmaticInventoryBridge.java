package dev.ambientodyssey.enigmaticbridge;

import com.mojang.logging.LogUtils;
import java.lang.reflect.Method;
import java.util.List;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.components.AbstractButton;
import net.minecraft.client.gui.components.AbstractWidget;
import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.components.Tooltip;
import net.minecraft.client.gui.narration.NarrationElementOutput;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.client.gui.screens.inventory.AbstractContainerScreen;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.level.ItemLike;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.ModList;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.client.event.ScreenEvent;
import net.neoforged.neoforge.common.NeoForge;

/** Client-only, optional, no replaced menus or custom packets. Exact target: EL+ 1.1.2 / BI 1.3.2. */
@Mod(value="aoenigmaticbridge", dist=Dist.CLIENT)
public final class EnigmaticInventoryBridge {
    private static final String BASE="auviotre.enigmatic.legacy.";
    private static final ResourceLocation ATLAS=ResourceLocation.fromNamespaceAndPath("betterinventory","textures/gui/inventory.png");
    private static Method hasCurio, configGet;
    private static ItemLike ring;
    private static Object enabled;
    private static boolean failed;

    public EnigmaticInventoryBridge(IEventBus bus) {
        NeoForge.EVENT_BUS.addListener(EnigmaticInventoryBridge::init);
        NeoForge.EVENT_BUS.addListener(EnigmaticInventoryBridge::beforeRender);
        NeoForge.EVENT_BUS.addListener(EnigmaticInventoryBridge::beforeClick);
    }
    private static boolean target(Screen screen) {
        return screen.getClass().getName().equals("dev.fallingcloud.betterinventory.client.screen.BetterInventoryScreen")
            && ModList.get().isLoaded("enigmaticlegacyplus");
    }
    private static void init(ScreenEvent.Init.Post event) {
        if (!target(event.getScreen()) || failed) return;
        try {
            if (hasCurio==null) {
                hasCurio=Class.forName(BASE+"handlers.EnigmaticHandler").getMethod("hasCurio",LivingEntity.class,ItemLike.class);
                ring=(ItemLike)Class.forName(BASE+"registries.EnigmaticItems").getField("CURSED_RING").get(null);
                enabled=Class.forName(BASE+"contents.item.rings.CursedRing").getField("enableEnderRing").get(null);
                configGet=enabled.getClass().getMethod("get");
            }
            var parent=(AbstractContainerScreen<?>)event.getScreen();
            // Original action handles the carried stack and sends EL+'s server-validated packet.
            Button original=(Button)Class.forName(BASE+"client.screen.button.EnderChestInventoryButton")
                .getMethod("getInstance",AbstractContainerScreen.class,boolean.class).invoke(null,parent,false);
            var tab=new EnderTab(parent,original);
            tab.refresh();
            event.addListener(tab);
        } catch (ReflectiveOperationException | LinkageError e) {
            failed=true;
            LogUtils.getLogger().error("AO Enigmatic bridge incompatible with installed EL+; button disabled",e);
        }
    }
    private static boolean allowed() {
        var player=Minecraft.getInstance().player;
        if (player==null || hasCurio==null || failed) return false;
        try { return Boolean.TRUE.equals(configGet.invoke(enabled)) && Boolean.TRUE.equals(hasCurio.invoke(null,player,ring)); }
        catch (ReflectiveOperationException | LinkageError e) {
            if (!failed) LogUtils.getLogger().error("AO Enigmatic equip lookup failed; button disabled",e);
            failed=true; return false;
        }
    }
    private static void beforeRender(ScreenEvent.Render.Pre event) {
        if (!target(event.getScreen())) return;
        for (var child:event.getScreen().children()) if(child instanceof EnderTab tab) tab.refresh();
    }
    private static void beforeClick(ScreenEvent.MouseButtonPressed.Pre event) {
        if (!target(event.getScreen()) || event.getButton()!=0) return;
        for (var child:event.getScreen().children()) if (child instanceof EnderTab tab) {
            tab.refresh();
            // BI's container click handling can consume this lower slot region before widgets.
            // Only route our own visible hitbox; all native controls retain their input path.
            if (tab.mouseClicked(event.getMouseX(),event.getMouseY(),event.getButton())) {
                event.setCanceled(true); return;
            }
        }
    }
    public static final class EnderTab extends AbstractButton {
        private final AbstractContainerScreen<?> parent;
        private final Button original;
        private EnderTab(AbstractContainerScreen<?> parent,Button original) {
            super(0,0,24,20,Component.translatable("container.enderchest"));
            this.parent=parent; this.original=original;
            setTooltip(Tooltip.create(getMessage()));
        }
        private void refresh() {
            active=visible=allowed();
            if (!visible) return;
            // User-selected space below the left tool panel; preserve any active toolbox slot.
            int left=parent.getGuiLeft(), top=parent.getGuiTop();
            int[][] candidates={{left+92,top+192},{left+63,top+192},
                {left+280,top-22},{left-26,top}};
            for (int[] p:candidates) {
                if(p[0]<2 || p[1]<2 || p[0]+24>parent.width-2 || p[1]+20>parent.height-2) continue;
                boolean overlaps=false;
                for (var child:parent.children()) if(child instanceof AbstractWidget w && w!=this && w.visible
                    && p[0]<w.getX()+w.getWidth() && p[0]+24>w.getX()
                    && p[1]<w.getY()+w.getHeight() && p[1]+20>w.getY()) { overlaps=true; break; }
                for (var slot:parent.getMenu().slots) if (slot.isActive()
                    && p[0]<left+slot.x+16 && p[0]+24>left+slot.x
                    && p[1]<top+slot.y+16 && p[1]+20>top+slot.y) { overlaps=true; break; }
                if (!overlaps) { setPosition(p[0],p[1]); return; }
            }
            active=visible=false; // Never cover a native control when no safe position exists.
        }
        @Override protected void renderWidget(GuiGraphics graphics,int x,int y,float partial) {
            graphics.blit(ATLAS,getX(),getY(),220,isHoveredOrFocused()?21:0,24,20,512,256);
            var font=Minecraft.getInstance().font;
            graphics.drawString(font,"E",getX()+(24-font.width("E"))/2,getY()+6,0xFFEADFC9,true);
        }
        @Override public void onPress() {
            if (Minecraft.getInstance().screen==parent && allowed()) original.onPress();
        }
        @Override protected void updateWidgetNarration(NarrationElementOutput output) { defaultButtonNarrationText(output); }
    }
}
