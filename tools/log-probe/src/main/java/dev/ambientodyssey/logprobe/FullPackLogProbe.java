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
 private boolean opening,finished; private int ticks;
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
    mc.createWorldOpenFlows().createFreshLevel("ao-full-pack-log-probe",settings,new WorldOptions(48127,false,false),a->a.registryOrThrow(Registries.WORLD_PRESET).getHolderOrThrow(WorldPresets.FLAT).value().createWorldDimensions(),new TitleScreen());
    return;
   }
   if(mc.player==null||mc.level==null||mc.getSingleplayerServer()==null||++ticks<100)return;
   finished=true;
   var type=Class.forName("dev.shadowsoffire.apotheosis.socket.gem.GemRegistry");
   var registry=type.getField("INSTANCE").get(null);
   var values=(java.util.Collection<?>)type.getMethod("getValues").invoke(registry);
   LOG.info("AO_FULL_PACK_WORLD_JOIN_OBSERVED: disposable integrated player/world ready; {} native gems",values.size());
   if(Boolean.getBoolean("ao.fullpack.campaignChecks")) {
    Class.forName("dev.shadowsoffire.apotheosis.affix.augmenting.AugmentingScreen$FatTexButton");
    mc.getSingleplayerServer().submit(() -> {
     CampaignChecks.run(mc.getSingleplayerServer());
     try { IntegrationChecks.run(mc.getSingleplayerServer()); } catch(Exception e) { throw new IllegalStateException(e); }
    }).get();
   }
   var config=com.google.gson.JsonParser.parseString(java.nio.file.Files.readString(java.nio.file.Path.of("config/dungeon_difficulty/difficulty_v2.json"))).getAsJsonObject();
   mc.getSingleplayerServer().submit(() -> {
    try { OrdinaryRuleProbe.start(mc.getSingleplayerServer(),config,() -> mc.execute(() -> {
     LOG.info("AO_FULL_PACK_WORLD_JOIN_PASS: integrated world and synthetic DD fixtures completed; no natural combat or multiplayer certification");mc.stop();
    })); } catch(Exception e) { LOG.error("AO_FULL_PACK_PROBE_FAIL",e);mc.execute(mc::stop); }
   }).get();
  }catch(Exception|LinkageError e){finished=true;LOG.error("AO_FULL_PACK_PROBE_FAIL",e);mc.stop();}
 }
}
