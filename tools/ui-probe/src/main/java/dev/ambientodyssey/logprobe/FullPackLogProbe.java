package dev.ambientodyssey.logprobe;
import com.mojang.logging.LogUtils;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.screens.TitleScreen;
import net.minecraft.client.gui.screens.AccessibilityOnboardingScreen;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.Difficulty;
import net.minecraft.world.level.GameRules;
import net.minecraft.world.level.GameType;
import net.minecraft.world.level.LevelSettings;
import net.minecraft.world.level.WorldDataConfiguration;
import net.minecraft.world.level.levelgen.WorldOptions;
import net.minecraft.world.level.levelgen.presets.WorldPresets;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.common.NeoForge;
import net.neoforged.neoforge.client.event.ClientTickEvent;
@Mod(value="ao_fullpack_probe",dist=Dist.CLIENT)
public final class FullPackLogProbe {
 private static final org.slf4j.Logger LOG=LogUtils.getLogger();
 private final long start=System.nanoTime();
 private int hoverX,hoverY; private String lastScreen=""; private boolean opening,finished; private int ticks, stage; private net.minecraft.client.gui.screens.inventory.AbstractContainerScreen<?> inventory;
 public FullPackLogProbe(){NeoForge.EVENT_BUS.addListener(this::tick);NeoForge.EVENT_BUS.addListener(this::render);}
 private void render(net.neoforged.neoforge.client.event.ScreenEvent.Render.Pre event){
  if(!Boolean.getBoolean("ao.fullpack.logProbe")||inventory==null||event.getScreen()!=inventory)return;
  inventory.renderWithTooltip(event.getGuiGraphics(),hoverX,hoverY,event.getPartialTick());
  event.setCanceled(true);
 }
 private void tick(ClientTickEvent.Post event){
  if(!Boolean.getBoolean("ao.fullpack.logProbe")||finished)return;
  var mc=Minecraft.getInstance();
  try{
   String current=mc.screen==null?"none":mc.screen.getClass().getName();
   if(!current.equals(lastScreen)){LOG.info("AO_UI_SCREEN: {}",current);lastScreen=current;}
   if(!opening&&current.equals("org.betterx.wover.ui.impl.client.WelcomeScreen")){
    try(var shot=net.minecraft.client.Screenshot.takeScreenshot(mc.getMainRenderTarget())){shot.writeToFile(mc.gameDirectory.toPath().resolve("startup-welcome.png"));}
    LOG.info("AO_UI_WELCOME_PRESENT: dismissing only in baseline QA");mc.screen.onClose();return;
   }
   if(System.nanoTime()-start>420_000_000_000L)throw new IllegalStateException("World load timed out; screen="+(mc.screen==null?"none":mc.screen.getClass().getName()));
   if(mc.screen instanceof AccessibilityOnboardingScreen&&mc.getOverlay()==null){mc.setScreen(new TitleScreen());return;}
   if(!opening&&mc.screen instanceof TitleScreen&&mc.getOverlay()==null){
    opening=true; mc.options.onboardAccessibility=false;mc.options.renderDistance().set(2);mc.options.simulationDistance().set(2);
    LOG.info("AO_FULL_PACK_TITLE_PASS: creating disposable flat world for full-registry diagnosis");
    var settings=new LevelSettings("AO full-pack log probe",GameType.CREATIVE,false,Difficulty.PEACEFUL,true,new GameRules(),WorldDataConfiguration.DEFAULT);
mc.createWorldOpenFlows().createFreshLevel("ao-ui-probe-"+System.currentTimeMillis(),settings,new WorldOptions(48127,false,false),a->a.registryOrThrow(Registries.WORLD_PRESET).getHolderOrThrow(WorldPresets.FLAT).value().createWorldDimensions(),new TitleScreen());
    return;
   }
   if(mc.player==null||mc.level==null||mc.getSingleplayerServer()==null||++ticks<100)return;
   if(inventory==null){
    mc.options.guiScale().set(stage<2?2:stage==2?3:4);mc.resizeDisplay();
    var player=mc.player;
    dev.shadowsoffire.apotheosis.tiers.WorldTier.setTier(player,dev.shadowsoffire.apotheosis.tiers.WorldTier.PINNACLE);
    var rarity=dev.shadowsoffire.apotheosis.loot.RarityRegistry.INSTANCE.holder(net.minecraft.resources.ResourceLocation.parse("apotheosis:mythic")).get();
    var server=mc.getSingleplayerServer();
    var level=server.overworld();
    var future=server.submit(()->{
     var ctx=dev.shadowsoffire.apotheosis.tiers.GenContext.standalone(net.minecraft.util.RandomSource.create(74512),dev.shadowsoffire.apotheosis.tiers.WorldTier.values()[0],0,level,net.minecraft.core.BlockPos.ZERO);
     return dev.shadowsoffire.apotheosis.loot.LootController.createLootItem(new net.minecraft.world.item.ItemStack(net.minecraft.world.item.Items.NETHERITE_SWORD),rarity,ctx);
    });
    var loot=future.get();
    if(stage==3){
     var lines=new java.util.ArrayList<net.minecraft.network.chat.Component>();
     for(int i=1;i<=30;i++)lines.add(net.minecraft.network.chat.Component.literal("Long description test line "+i));
     loot.set(net.minecraft.core.component.DataComponents.LORE,new net.minecraft.world.item.component.ItemLore(lines));
    }
    if(stage>0&&!dev.shadowsoffire.apotheosis.affix.AffixHelper.hasAffixes(loot))throw new IllegalStateException("QA sword has no affixes");
    player.getInventory().selected=1;
    player.getInventory().setItem(0,stage==0?new net.minecraft.world.item.ItemStack(net.minecraft.world.item.Items.DIAMOND_SWORD):loot.copy());player.getInventory().setItem(1,loot.copy());player.setItemSlot(net.minecraft.world.entity.EquipmentSlot.OFFHAND,loot.copy());
    player.getInventory().setItem(9,stage==0?new net.minecraft.world.item.ItemStack(net.minecraft.world.item.Items.DIAMOND_SWORD):loot.copy());
    var menuClass=Class.forName("dev.fallingcloud.betterinventory.menu.BetterInventoryMenu");
    var menu=menuClass.getConstructor(int.class,net.minecraft.world.entity.player.Inventory.class).newInstance(0,player.getInventory());
    var screenClass=Class.forName("dev.fallingcloud.betterinventory.client.screen.BetterInventoryScreen");
    inventory=(net.minecraft.client.gui.screens.inventory.AbstractContainerScreen<?>)screenClass.getConstructor(menuClass,net.minecraft.world.entity.player.Inventory.class,net.minecraft.network.chat.Component.class).newInstance(menu,player.getInventory(),net.minecraft.network.chat.Component.literal("Tooltip QA"));
    mc.setScreen(inventory);
    var slot=inventory.getMenu().slots.stream().filter(v->v.hasItem()&&v.getItem().is(stage==0?net.minecraft.world.item.Items.DIAMOND_SWORD:net.minecraft.world.item.Items.NETHERITE_SWORD)).findFirst().orElseThrow();
    hoverX=inventory.getGuiLeft()+slot.x+8;hoverY=inventory.getGuiTop()+slot.y+8;
    var compare=Class.forName("com.anthonyhilyard.equipmentcompare.EquipmentCompare");
    compare.getField("comparisonsActive").setBoolean(null,stage>0);
    ticks=0; return;
   }
   if(stage==3&&ticks==100){
    try(var shot=net.minecraft.client.Screenshot.takeScreenshot(mc.getMainRenderTarget())){shot.writeToFile(mc.gameDirectory.toPath().resolve("tooltip-before-scroll.png"));}
   }
   if(stage==3&&ticks==110){
    var active=(Boolean)Class.forName("net.sweenus.simplytooltips.client.render.ScrollState").getMethod("isScrollableActive").invoke(null);
    if(!active)throw new IllegalStateException("Oversized tooltip has no active scrolling");
    var scroll=net.minecraft.client.MouseHandler.class.getDeclaredMethod("onScroll",long.class,double.class,double.class);
    scroll.setAccessible(true);scroll.invoke(mc.mouseHandler,mc.getWindow().getWindow(),0d,-8d);
    LOG.info("AO_TOOLTIP_NATIVE_WHEEL_PASS: scrollable tooltip active; native mouse wheel callback delivered");
   }
   if(stage==3&&ticks==130){
    int offset=(Integer)Class.forName("net.sweenus.simplytooltips.client.render.ScrollState").getMethod("get").invoke(null);
    if(offset<=0)throw new IllegalStateException("Native wheel callback did not move tooltip content");
    LOG.info("AO_TOOLTIP_SCROLL_OFFSET_PASS: offset={}",offset);
   }
   if(ticks<140)return;
   var path=mc.gameDirectory.toPath().resolve("tooltip-stage-"+stage+".png");
   try(var shot=net.minecraft.client.Screenshot.takeScreenshot(mc.getMainRenderTarget())){shot.writeToFile(path);}
   LOG.info("AO_TOOLTIP_FRAME: stage={}, scale={}, screenshot={}",stage,mc.options.guiScale().get(),path);
   inventory=null;ticks=0;mc.setScreen(null);
   if(++stage<4)return;
   finished=true;
   LOG.info("AO_FULL_PACK_WORLD_JOIN_PASS: UI probe rendered plain and actual affixed comparison tooltips at scales 2/3/4");
   mc.stop();
  }catch(Exception|LinkageError e){finished=true;LOG.error("AO_FULL_PACK_PROBE_FAIL",e);mc.stop();}
 }
}
