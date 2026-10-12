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
 private boolean opening,finished; private int ticks, stage; private net.minecraft.client.gui.screens.inventory.AbstractContainerScreen<?> inventory;
 public FullPackLogProbe(){NeoForge.EVENT_BUS.addListener(this::tick);}
 private void tick(ClientTickEvent.Post event){
  if(!Boolean.getBoolean("ao.fullpack.logProbe")||finished)return;
  var mc=Minecraft.getInstance();
  try{
   if(System.nanoTime()-start>420_000_000_000L)throw new IllegalStateException("World load timed out; screen="+(mc.screen==null?"none":mc.screen.getClass().getName()));
   if(mc.screen instanceof AccessibilityOnboardingScreen&&mc.getOverlay()==null){mc.setScreen(new TitleScreen());return;}
   if(!opening&&mc.screen instanceof TitleScreen&&mc.getOverlay()==null){
    opening=true; mc.options.onboardAccessibility=false;mc.options.renderDistance().set(2);mc.options.simulationDistance().set(2);
    LOG.info("AO_FULL_PACK_TITLE_PASS: creating disposable flat world for full-registry diagnosis");
    var settings=new LevelSettings("AO full-pack log probe",GameType.CREATIVE,false,Difficulty.PEACEFUL,true,new GameRules(),WorldDataConfiguration.DEFAULT);
    mc.createWorldOpenFlows().createFreshLevel("ao-ring-position-"+System.currentTimeMillis(),settings,new WorldOptions(48127,false,false),a->a.registryOrThrow(Registries.WORLD_PRESET).getHolderOrThrow(WorldPresets.FLAT).value().createWorldDimensions(),new TitleScreen());
    return;
   }
   if(mc.player==null||mc.level==null||mc.getSingleplayerServer()==null||++ticks<100)return;
   var server=mc.getSingleplayerServer();
   var sp=server.getPlayerList().getPlayers().getFirst();
   if(stage==0){
    inventory=openInventory(mc,2);
    check(!tab().visible,"unequipped ring must hide tab");
    server.submit(()->{try{equip(sp,true);}catch(Exception e){throw new RuntimeException(e);}}).get();
    stage=1;ticks=0;return;
   }
   if(stage>=1&&stage<=3){
    check(tab().visible&&tab().active,"equipped ring must show tab");
    check(tab().getY()==inventory.getGuiTop()+192,"tab must sit below left tool panel");
    check(tab().getX()==inventory.getGuiLeft()+92 || tab().getX()==inventory.getGuiLeft()+63,"tab must stay in requested left area");
    for(var slot:inventory.getMenu().slots)if(slot.isActive())
      check(!(tab().getX()<inventory.getGuiLeft()+slot.x+16&&tab().getX()+24>inventory.getGuiLeft()+slot.x&&tab().getY()<inventory.getGuiTop()+slot.y+16&&tab().getY()+20>inventory.getGuiTop()+slot.y),"active slot overlap");
    var q=(net.minecraft.client.gui.components.AbstractButton)inventory.children().stream().filter(v->v.getClass().getName().endsWith("QuestlogBetterInventoryBridge$QuestlogTab")).findFirst().orElseThrow();
    check(q.getX()==inventory.getGuiLeft()+318&&q.getY()==inventory.getGuiTop(),"Q must be above right armor");
    click(mc,q);
    check(mc.screen!=null&&mc.screen.getClass().getName().endsWith("QuestlogScreen"),"Q did not open Questlog");
    mc.screen.keyPressed(256,0,0);check(mc.screen==inventory,"Q did not return to Better Inventory");
    LOG.info("AO_QUESTLOG_POSITION_CLICK_PASS: scale={}, x={}, y={}",stage+1,q.getX(),q.getY());
    for(var child:inventory.children())if(child instanceof net.minecraft.client.gui.components.AbstractWidget w&&w!=tab()&&w.visible)
      check(!(tab().getX()<w.getX()+w.getWidth()&&tab().getX()+24>w.getX()&&tab().getY()<w.getY()+w.getHeight()&&tab().getY()+20>w.getY()),"widget overlap");
    try(var shot=net.minecraft.client.Screenshot.takeScreenshot(mc.getMainRenderTarget())){shot.writeToFile(mc.gameDirectory.toPath().resolve("ring-scale-"+(stage+1)+".png"));}
    LOG.info("AO_RING_LAYOUT_PASS: scale={}, x={}, y={}",stage+1,tab().getX(),tab().getY());
    if(stage<3){stage++;inventory=openInventory(mc,stage+1);ticks=0;return;}
    click(mc,tab());
    stage=4;ticks=0;return;
   }
   if(stage==4){
    check(mc.player.containerMenu instanceof net.minecraft.world.inventory.ChestMenu,"original packet did not open chest");
    LOG.info("AO_RING_ORIGINAL_PACKET_PASS: real server opened chest menu");
    mc.player.closeContainer();
    server.submit(()->{try{equip(sp,false);}catch(Exception e){throw new RuntimeException(e);}}).get();
    inventory=openInventory(mc,3);stage=5;ticks=0;return;
   }
   check(!tab().visible,"unequipped ring left a visible button");
   LOG.info("AO_RING_UNEQUIP_PASS: original cursed state does not keep tab visible");
   finished=true;
   LOG.info("AO_FULL_PACK_WORLD_JOIN_PASS: full roster loaded; ring native layout/equip/click/unequip checks passed");
   mc.stop();
  }catch(Exception|LinkageError e){finished=true;LOG.error("AO_FULL_PACK_PROBE_FAIL",e);mc.stop();}
 }
 private static void click(Minecraft mc,net.minecraft.client.gui.components.AbstractButton button)throws Exception {
    var move=net.minecraft.client.MouseHandler.class.getDeclaredMethod("onMove",long.class,double.class,double.class);
    move.setAccessible(true);move.invoke(mc.mouseHandler,mc.getWindow().getWindow(),
      (button.getX()+12d)*mc.getWindow().getScreenWidth()/mc.getWindow().getGuiScaledWidth(),
      (button.getY()+10d)*mc.getWindow().getScreenHeight()/mc.getWindow().getGuiScaledHeight());
    var press=net.minecraft.client.MouseHandler.class.getDeclaredMethod("onPress",long.class,int.class,int.class,int.class);
    press.setAccessible(true);press.invoke(mc.mouseHandler,mc.getWindow().getWindow(),0,1,0);
    press.invoke(mc.mouseHandler,mc.getWindow().getWindow(),0,0,0);
 }
 private static void check(boolean value,String message){if(!value)throw new IllegalStateException(message);}
 private net.minecraft.client.gui.components.AbstractButton tab(){return (net.minecraft.client.gui.components.AbstractButton)inventory.children().stream().filter(v->v.getClass().getName().endsWith("EnigmaticInventoryBridge$EnderTab")).findFirst().orElseThrow();}
 private static void equip(net.minecraft.world.entity.LivingEntity player,boolean on)throws Exception {
  var api=Class.forName("top.theillusivec4.curios.api.CuriosApi");
  var opt=(java.util.Optional<?>)api.getMethod("getCuriosInventory",net.minecraft.world.entity.LivingEntity.class).invoke(null,player);
  var handler=Class.forName("top.theillusivec4.curios.api.type.capability.ICuriosItemHandler");
  var curios=(java.util.Map<?,?>)handler.getMethod("getCurios").invoke(opt.orElseThrow());
  var ring=curios.get("ring");check(ring!=null,"no ring Curios slot");
  var stacks=Class.forName("top.theillusivec4.curios.api.type.inventory.ICurioStacksHandler").getMethod("getStacks").invoke(ring);
  var item=net.minecraft.core.registries.BuiltInRegistries.ITEM.get(net.minecraft.resources.ResourceLocation.parse("enigmaticlegacyplus:cursed_ring"));
  check(item!=net.minecraft.world.item.Items.AIR,"missing native cursed ring item");
  ((net.neoforged.neoforge.items.IItemHandlerModifiable)stacks).setStackInSlot(0,on?new net.minecraft.world.item.ItemStack(item):net.minecraft.world.item.ItemStack.EMPTY);
 }
 private static net.minecraft.client.gui.screens.inventory.AbstractContainerScreen<?> openInventory(Minecraft mc,int scale)throws Exception{
  mc.options.guiScale().set(scale);mc.resizeDisplay();
  var m=Class.forName("dev.fallingcloud.betterinventory.menu.BetterInventoryMenu");
  var menu=m.getConstructor(int.class,net.minecraft.world.entity.player.Inventory.class).newInstance(0,mc.player.getInventory());
  var screen=(net.minecraft.client.gui.screens.inventory.AbstractContainerScreen<?>)Class.forName("dev.fallingcloud.betterinventory.client.screen.BetterInventoryScreen").getConstructor(m,net.minecraft.world.entity.player.Inventory.class,net.minecraft.network.chat.Component.class).newInstance(menu,mc.player.getInventory(),net.minecraft.network.chat.Component.literal("Ring compatibility QA"));
  mc.setScreen(screen);return screen;
 }
}
