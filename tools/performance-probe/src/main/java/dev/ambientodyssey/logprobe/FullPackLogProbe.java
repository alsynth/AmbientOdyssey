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
 public FullPackLogProbe(){NeoForge.EVENT_BUS.addListener(this::tick);NeoForge.EVENT_BUS.addListener(this::frame);NeoForge.EVENT_BUS.addListener(this::renderTooltip);}
 private void tick(ClientTickEvent.Post event){
  if(!Boolean.getBoolean("ao.fullpack.logProbe")||finished)return;
  var mc=Minecraft.getInstance();
  try{
   if(benchmark){benchTick(mc);return;}
   if(System.nanoTime()-start>1500_000_000_000L)throw new IllegalStateException("World load timed out; screen="+(mc.screen==null?"none":mc.screen.getClass().getName()));
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
   if(!tooltipTest){
    var stack=new net.minecraft.world.item.ItemStack(net.minecraft.world.item.Items.NETHERITE_SWORD);
    var lore=new java.util.ArrayList<net.minecraft.network.chat.Component>();for(int i=1;i<=32;i++)lore.add(net.minecraft.network.chat.Component.literal("Full-pack tooltip regression line "+i));
    stack.set(net.minecraft.core.component.DataComponents.LORE,new net.minecraft.world.item.component.ItemLore(lore));mc.player.getInventory().setItem(0,stack);mc.player.getInventory().selected=1;
    inventory=openInventory(mc,3);var slot=inventory.getMenu().slots.stream().filter(v->v.hasItem()&&v.getItem().is(net.minecraft.world.item.Items.NETHERITE_SWORD)).findFirst().orElseThrow();
    hoverX=inventory.getGuiLeft()+slot.x+8;hoverY=inventory.getGuiTop()+slot.y+8;tooltipTest=true;ticks=0;return;
   }
   if(ticks==110){
    check((Boolean)Class.forName("net.sweenus.simplytooltips.client.render.ScrollState").getMethod("isScrollableActive").invoke(null),"long tooltip scrolling not active");
    var scroll=net.minecraft.client.MouseHandler.class.getDeclaredMethod("onScroll",long.class,double.class,double.class);scroll.setAccessible(true);scroll.invoke(mc.mouseHandler,mc.getWindow().getWindow(),0d,-8d);return;
   }
   if(ticks<135)return;
   check((Integer)Class.forName("net.sweenus.simplytooltips.client.render.ScrollState").getMethod("get").invoke(null)>0,"tooltip content did not scroll");
   try(var shot=net.minecraft.client.Screenshot.takeScreenshot(mc.getMainRenderTarget())){shot.writeToFile(mc.gameDirectory.toPath().resolve("tooltip-removal-regression.png"));}
   tooltipTest=false;LOG.info("AO_PERF_UI_PASS: Q/E equip/click/return and native tooltip scrolling after removal passed");
   mc.setScreen(null);beginBench(mc);return;
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
 private boolean tooltipTest;private int hoverX,hoverY;
 private void renderTooltip(net.neoforged.neoforge.client.event.ScreenEvent.Render.Pre event){
  if(tooltipTest&&event.getScreen()==inventory){inventory.renderWithTooltip(event.getGuiGraphics(),hoverX,hoverY,event.getPartialTick());event.setCanceled(true);}
 }
 private boolean benchmark;
 private int variant,trial;
 private long periodStart,lastFrame;
 private boolean sampling;
 private final java.util.ArrayList<Double> frameMs=new java.util.ArrayList<>();
 private final java.util.ArrayList<java.util.Map<String,Object>> results=new java.util.ArrayList<>();
 private static final String[] MODES={"OFF","AO Performance","AO Balanced","AO Quality","AO Balanced Culling OFF","AO Balanced Streams Original"};
 private void frame(net.neoforged.neoforge.client.event.RenderFrameEvent.Post event){
  if(!sampling)return;var mc=Minecraft.getInstance();long now=System.nanoTime();
  if(mc.getOverlay()==null&&mc.screen==null&&lastFrame!=0)frameMs.add((now-lastFrame)/1_000_000d);
  lastFrame=now;
 }
 private void beginBench(Minecraft mc)throws Exception {
  var server=mc.getSingleplayerServer();var sp=server.getPlayerList().getPlayers().getFirst();
  var origin=sp.blockPosition();
  server.submit(()->{
   var level=server.overworld();level.setDayTime(6000);level.getGameRules().getBoolean(net.minecraft.world.level.GameRules.RULE_DAYLIGHT);level.getGameRules().getRule(net.minecraft.world.level.GameRules.RULE_DAYLIGHT).set(false,server);
   for(int x=-20;x<=20;x++)for(int z=0;z<=40;z++)level.setBlock(origin.offset(x,-1,z),net.minecraft.world.level.block.Blocks.GRASS_BLOCK.defaultBlockState(),3);
   for(int x=-14;x<=14;x++)for(int y=0;y<7;y++)level.setBlock(origin.offset(x,y,18),net.minecraft.world.level.block.Blocks.STONE_BRICKS.defaultBlockState(),3);
   for(int x=-16;x<=16;x+=8){
    for(int y=0;y<9;y++)level.setBlock(origin.offset(x,y,9),net.minecraft.world.level.block.Blocks.OAK_LOG.defaultBlockState(),3);
    for(int a=-3;a<=3;a++)for(int b=-3;b<=3;b++)for(int y=6;y<10;y++)level.setBlock(origin.offset(x+a,y,9+b),net.minecraft.world.level.block.Blocks.OAK_LEAVES.defaultBlockState().setValue(net.minecraft.world.level.block.LeavesBlock.PERSISTENT,true),3);
   }
   for(int x=-8;x<=8;x+=4){level.setBlock(origin.offset(x,9,15),net.minecraft.world.level.block.Blocks.WATER.defaultBlockState(),3);level.setBlock(origin.offset(x,9,16),net.minecraft.world.level.block.Blocks.STONE.defaultBlockState(),3);}
   for(int i=0;i<32;i++){
    var cow=net.minecraft.world.entity.EntityType.COW.create(level);cow.setNoAi(true);cow.setPersistenceRequired();cow.moveTo(origin.getX()-12+(i%8)*3,origin.getY(),origin.getZ()+22+(i/8)*2,0,0);level.addFreshEntity(cow);
    level.setBlock(origin.offset(-12+(i%8)*3,0,24+(i/8)*2),net.minecraft.world.level.block.Blocks.CHEST.defaultBlockState(),3);
   }
   sp.teleportTo(origin.getX()+0.5,origin.getY()+3,origin.getZ()-5+0.5);return null;
  }).get();
  mc.player.setYRot(0);mc.player.setXRot(12);mc.options.renderDistance().set(12);mc.options.simulationDistance().set(6);mc.options.framerateLimit().set(160);mc.options.enableVsync().set(false);
  benchmark=true;selectMode(mc);LOG.info("AO_PERF_SCENE_READY: controlled flat trees/waterfalls/occluded cows/chests; 1440p,12/6,cap160; not survival benchmark");
 }
 private void selectMode(Minecraft mc)throws Exception {
  sampling=false;frameMs.clear();lastFrame=0;
  var c=Class.forName("dev.tr7zw.entityculling.EntityCullingModBase");var inst=c.getField("instance").get(null);var cfg=c.getField("config").get(inst);
  check(!cfg.getClass().getField("tickCulling").getBoolean(cfg),"tick culling unexpectedly enabled");
  Class.forName("dev.tr7zw.entityculling.versionless.EntityCullingVersionlessBase").getField("enabled").setBoolean(null,variant!=4);
  var streams=Class.forName("dev.streamsreflowing.neoforge.StreamsConfigNeo");
  String[] keys={"STREAM_BUBBLES","STREAM_DEBRIS","PARTICLE_RATE","MAX_STREAM_PARTICLES","STREAM_PARTICLE_SCAN_RADIUS"};
  Object[] values=variant==5?new Object[]{2,true,1.0,1000,256}:new Object[]{1,false,0.5,250,64};
  for(int i=0;i<keys.length;i++){Object v=streams.getField(keys[i]).get(null);v.getClass().getMethod("set",Object.class).invoke(v,values[i]);}
  var clear=net.minecraft.client.particle.ParticleEngine.class.getDeclaredMethod("clearParticles");clear.setAccessible(true);clear.invoke(mc.particleEngine);
  var iris=Class.forName("net.irisshaders.iris.Iris");var config=iris.getMethod("getIrisConfig").invoke(null);
  String pack=variant==0?"AO Balanced":variant>=4?"AO Balanced":MODES[variant];
  config.getClass().getMethod("setShaderPackName",String.class).invoke(config,pack);
  config.getClass().getMethod("setShadersEnabled",boolean.class).invoke(config,variant!=0);
  iris.getMethod("reload").invoke(null);
  check(((java.util.Optional<?>)iris.getMethod("getStoredError").invoke(null)).isEmpty(),"shader compilation stored an error");
  if(variant!=0)check(((java.util.Optional<?>)iris.getMethod("getCurrentPack").invoke(null)).isPresent(),"shader pack missing");
  LOG.info("AO_PERF_MODE_READY: {} trial={}",MODES[variant],trial+1);periodStart=System.nanoTime();
 }
 private void benchTick(Minecraft mc)throws Exception {
  double elapsed=(System.nanoTime()-periodStart)/1_000_000_000d;
  if(!sampling&&elapsed>=20){sampling=true;frameMs.clear();lastFrame=0;periodStart=System.nanoTime();return;}
  if(!sampling||elapsed<30)return;
  if(variant!=0)check((Boolean)Class.forName("net.irisshaders.iris.Iris").getMethod("isPackInUseQuick").invoke(null),"shader renderer fell back to vanilla");
  sampling=false;check(frameMs.size()>50,"not enough frame samples");
  double total=frameMs.stream().mapToDouble(Double::doubleValue).sum();var sorted=new java.util.ArrayList<>(frameMs);sorted.sort(java.util.Comparator.reverseOrder());int n=Math.max(1,sorted.size()/100);
  double slow=sorted.subList(0,n).stream().mapToDouble(Double::doubleValue).average().orElseThrow();
  var row=new java.util.LinkedHashMap<String,Object>();row.put("mode",MODES[variant]);row.put("trial",trial+1);row.put("frames",frameMs.size());row.put("avg_fps",frameMs.size()*1000d/total);row.put("fps_1pct_low",1000d/slow);row.put("particles_at_end",mc.particleEngine.countParticles());row.put("scene","synthetic flat, 2560x1440, 12/6, cap160, 30 seconds after20s warmup");results.add(row);
  var gson=new com.google.gson.GsonBuilder().setPrettyPrinting().create();java.nio.file.Files.writeString(mc.gameDirectory.toPath().resolve("performance-results.json"),gson.toJson(results),java.nio.charset.StandardCharsets.UTF_8);
  LOG.info("AO_PERF_TRIAL: {}",gson.toJson(row));
  if(trial==0)try(var shot=net.minecraft.client.Screenshot.takeScreenshot(mc.getMainRenderTarget())){shot.writeToFile(mc.gameDirectory.toPath().resolve("performance-mode-"+variant+".png"));}
  if(++trial<3){selectMode(mc);return;}trial=0;
  if(++variant<MODES.length){selectMode(mc);return;}
  LOG.info("AO_FULL_PACK_WORLD_JOIN_PASS: candidate UI/shader compilation and 18 controlled client trials passed; not full survival/multiplayer certification");finished=true;benchmark=false;mc.stop();
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
