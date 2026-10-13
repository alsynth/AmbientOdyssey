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
   LOG.info("AO_FULL_PACK_WORLD_JOIN_PASS: player joined disposable flat integrated world; {} native gems loaded; content errors remain diagnostic, no gameplay certification",values.size());
   mc.getSingleplayerServer().execute(()->{
    try {
     export(mc.getSingleplayerServer()); LOG.info("AO_PR45_RUNTIME_REGISTRY_EXPORT_PASS");
     var input=new com.google.gson.Gson().fromJson(java.nio.file.Files.readString(java.nio.file.Path.of("PR45_CHECK_INPUT.json")),com.google.gson.JsonObject.class);
     if(input.has("run_ordinary_tests")&&input.get("run_ordinary_tests").getAsBoolean()) {
      var data=new com.google.gson.Gson().fromJson(java.nio.file.Files.readString(java.nio.file.Path.of("PR45_RUNTIME_REGISTRIES.json")),com.google.gson.JsonObject.class);
      OrdinaryRuleProbe.start(mc.getSingleplayerServer(),data.getAsJsonObject("loaded_dd_config"),()->mc.execute(mc::stop));return;
     }
    }
    catch(Exception e) { LOG.error("AO_FULL_PACK_PROBE_FAIL",e); }
    mc.execute(mc::stop);
   });
  }catch(Exception|LinkageError e){finished=true;LOG.error("AO_FULL_PACK_PROBE_FAIL",e);mc.stop();}
 }
 private static void export(net.minecraft.server.MinecraftServer server) throws Exception {
  var gson=new com.google.gson.GsonBuilder().setPrettyPrinting().create();
  var input=gson.fromJson(java.nio.file.Files.readString(java.nio.file.Path.of("PR45_CHECK_INPUT.json")),com.google.gson.JsonObject.class);
  var output=new com.google.gson.JsonObject();
  var manager=Class.forName("net.dungeon_difficulty.DungeonDifficulty").getField("config").get(null);
  output.add("loaded_dd_config",gson.toJsonTree(manager.getClass().getField("value").get(manager)));
  var structures=server.registryAccess().registryOrThrow(Registries.STRUCTURE);
  var registered=new com.google.gson.JsonObject();
  for(var id:input.getAsJsonArray("structure_ids"))registered.addProperty(id.getAsString(),structures.containsKey(net.minecraft.resources.ResourceLocation.parse(id.getAsString())));
  output.add("structure_registry_membership",registered);
  var entities=new com.google.gson.JsonObject();
  for(var id:input.getAsJsonArray("arena_entity_ids"))entities.addProperty(id.getAsString(),net.minecraft.core.registries.BuiltInRegistries.ENTITY_TYPE.containsKey(net.minecraft.resources.ResourceLocation.parse(id.getAsString())));
  output.add("arena_entity_registry_membership",entities);
  var winners=new com.google.gson.JsonArray();
  for(var check:input.getAsJsonArray("resource_checks")) {
   var row=check.getAsJsonObject();var id=net.minecraft.resources.ResourceLocation.parse(row.get("id").getAsString());
   var path=net.minecraft.resources.ResourceLocation.fromNamespaceAndPath(id.getNamespace(),row.get("kind").getAsString()+"/"+id.getPath()+".json");
   var result=new com.google.gson.JsonObject();result.addProperty("id",id.toString());result.addProperty("kind",row.get("kind").getAsString());
   var resource=server.getResourceManager().getResource(path);result.addProperty("present",resource.isPresent());
   if(resource.isPresent()) {
    result.addProperty("source_pack",resource.get().sourcePackId());
    try(var stream=resource.get().open()) {
     String hash=java.util.HexFormat.of().formatHex(java.security.MessageDigest.getInstance("SHA-256").digest(stream.readAllBytes()));
     result.addProperty("sha256",hash);var matches=new com.google.gson.JsonArray();
     for(var provider:row.getAsJsonArray("providers"))if(provider.getAsJsonObject().get("sha256").getAsString().equals(hash))matches.add(provider.getAsJsonObject().get("provider").getAsString());
     result.add("matching_audited_providers",matches);
    }
   }
   winners.add(result);
  }
  output.add("effective_resource_winners",winners);output.addProperty("encounter_gameplay_tested",false);output.addProperty("dedicated_server_tested",false);output.addProperty("multiplayer_tested",false);
  java.nio.file.Files.writeString(java.nio.file.Path.of("PR45_RUNTIME_REGISTRIES.json"),gson.toJson(output));
 }
}
