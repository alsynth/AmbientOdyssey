package dev.ambientodyssey.logprobe;

import com.google.gson.*;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.Difficulty;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.level.ChunkPos;
import net.minecraft.world.level.GameRules;
import net.minecraft.world.level.WorldGenLevel;
import net.minecraft.world.level.StructureManager;
import net.minecraft.world.level.chunk.ChunkGenerator;
import net.minecraft.world.level.levelgen.structure.*;
import net.minecraft.world.level.levelgen.structure.pieces.*;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.util.RandomSource;
import net.neoforged.neoforge.common.NeoForge;
import net.neoforged.neoforge.event.tick.ServerTickEvent;
import java.nio.file.*;
import java.util.*;

/** Test-only spatial fixtures. Never installed into a real profile or save. */
final class OrdinaryRuleProbe {
 private record Case(String id,String structure,int tier,Mob mob,JsonObject before,JsonObject expected) {}
 private record Fixture(net.minecraft.world.level.chunk.LevelChunk chunk,Structure structure) {}
 private static final List<Case> cases=new ArrayList<>();
 private static final List<Fixture> fixtures=new ArrayList<>();
 private static final Set<ChunkPos> forcedChunks=new HashSet<>();
 private static MinecraftServer server;
 private static int finishAt;
 private static Runnable done;
 private static Difficulty oldDifficulty;
 private static boolean oldSpawning;
 static void start(MinecraftServer active,JsonObject config,Runnable completion) throws Exception {
  server=active;done=completion;var level=server.overworld();oldDifficulty=server.getWorldData().getDifficulty();
  oldSpawning=level.getGameRules().getBoolean(GameRules.RULE_DOMOBSPAWNING);
  server.setDifficulty(Difficulty.NORMAL,true);level.getGameRules().getRule(GameRules.RULE_DOMOBSPAWNING).set(false,server);
  var selected=new TreeMap<Integer,String>();
  for(var d:config.getAsJsonArray("dimensions")) {
   var dim=d.getAsJsonObject();if(!dim.getAsJsonObject("world_matches").get("dimension").getAsString().equals("minecraft:overworld"))continue;
   for(var z:dim.getAsJsonArray("zones")) {var zone=z.getAsJsonObject();int tier=Integer.parseInt(zone.getAsJsonObject("difficulty").get("name").getAsString().replace("ao_tier_",""));selected.putIfAbsent(tier,zone.getAsJsonObject("zone_matches").get("structure").getAsString());}
  }
  try {
   for(var entry:selected.entrySet()) {
    int tier=entry.getKey();var pos=new BlockPos(tier*16,80,0);index(level,entry.getValue(),pos);
    Mob mob=EntityType.ZOMBIE.create(level);mob.setNoAi(true);mob.setInvulnerable(true);mob.setPersistenceRequired();mob.moveTo(pos.getX()+.5,80,pos.getZ()+.5,0,0);
    var before=attributes(mob);var expected=before.deepCopy();
    if(tier>=2)for(var type:config.getAsJsonArray("difficulty_types")) {
     var t=type.getAsJsonObject();if(!t.get("name").getAsString().equals("ao_tier_"+tier))continue;
     for(var a:t.getAsJsonArray("entities").get(0).getAsJsonObject().getAsJsonArray("attributes")) {
      var attr=a.getAsJsonObject();String key=switch(attr.get("attribute").getAsString()){case "minecraft:generic.max_health"->"max_health";case "minecraft:generic.attack_damage"->"attack_damage";default->"armor";};
      double value=attr.get("value").getAsDouble();expected.addProperty(key,attr.get("operation").getAsString().equals("ADDITION")?before.get(key).getAsDouble()+value:before.get(key).getAsDouble()*(1+value));
     }
    }
    level.addFreshEntity(mob);cases.add(new Case("ordinary_t"+tier,entry.getValue(),tier,mob,before,expected));
   }
   if(selected.containsKey(6)) {
    for(var type:List.of(EntityType.PIG,EntityType.WITHER)) {
     var excluded=(Mob)type.create(level);excluded.setNoAi(true);excluded.setInvulnerable(true);excluded.setPersistenceRequired();excluded.moveTo(96.5,80,.5,0,0);var before=attributes(excluded);
     level.addFreshEntity(excluded);cases.add(new Case(type==EntityType.PIG?"passive_in_t6":"named_wither_type_in_t6",selected.get(6),6,excluded,before,before.deepCopy()));
    }
   }
   force(level,new ChunkPos(9,0));var outside=EntityType.ZOMBIE.create(level);outside.setNoAi(true);outside.setInvulnerable(true);outside.setPersistenceRequired();outside.moveTo(144,80,0,0,0);var before=attributes(outside);level.addFreshEntity(outside);cases.add(new Case("ordinary_outside","none",-1,outside,before,before.deepCopy()));
   // An unsupported T7 structure location must not receive an ordinary tier rule.
   var pos=new BlockPos(176,80,0);index(level,"cataclysm:frosted_prison",pos);var t7=EntityType.ZOMBIE.create(level);t7.setNoAi(true);t7.setInvulnerable(true);t7.setPersistenceRequired();t7.moveTo(176,80,0,0,0);before=attributes(t7);level.addFreshEntity(t7);cases.add(new Case("ordinary_t7_site","cataclysm:frosted_prison",7,t7,before,before.deepCopy()));
   finishAt=server.getTickCount()+50;NeoForge.EVENT_BUS.addListener(OrdinaryRuleProbe::tick);
  } catch(Exception e) {cleanup();throw e;}
 }
 private static void index(ServerLevel level,String id,BlockPos pos) {
  var structure=level.registryAccess().registryOrThrow(Registries.STRUCTURE).get(ResourceLocation.parse(id));
  if(structure==null)throw new IllegalStateException("Unregistered structure fixture: "+id);
  var chunk=level.getChunk(pos.getX()>>4,pos.getZ()>>4);var cp=chunk.getPos();
  force(level,cp);
  if(chunk.getStartForStructure(structure)!=null)throw new IllegalStateException("Refusing to replace a real structure start");
  chunk.setStartForStructure(structure,new StructureStart(structure,cp,0,new PiecesContainer(List.of(new Box(pos)))));
  chunk.addReferenceForStructure(structure,cp.toLong());fixtures.add(new Fixture(chunk,structure));
 }
 private static void force(ServerLevel level,ChunkPos pos) {
  if(!level.getForcedChunks().contains(pos.toLong())){level.setChunkForced(pos.x,pos.z,true);forcedChunks.add(pos);}
 }
 private static JsonObject attributes(Mob mob) {
  var row=new JsonObject();row.addProperty("max_health",mob.getAttributeValue(Attributes.MAX_HEALTH));row.addProperty("attack_damage",mob.getAttribute(Attributes.ATTACK_DAMAGE)==null?null:mob.getAttributeValue(Attributes.ATTACK_DAMAGE));row.addProperty("armor",mob.getAttributeValue(Attributes.ARMOR));row.addProperty("current_health",mob.getHealth());return row;
 }
 private static void tick(ServerTickEvent.Post event) {
  if(server==null||event.getServer()!=server||server.getTickCount()<finishAt)return;
  var report=new JsonObject();report.addProperty("scope","ACTUAL MINECRAFT ENTITY SPAWN EVENTS IN SYNTHETIC STRUCTURE BOUNDING BOXES; not natural generation or combat");var rows=new JsonArray();boolean all=true;
  for(var c:cases) {
   var row=new JsonObject();row.addProperty("case",c.id());row.addProperty("structure",c.structure());row.addProperty("tier",c.tier());row.add("before",c.before());row.add("expected_attributes",c.expected());var after=attributes(c.mob());row.add("after_50_ticks",after);row.addProperty("entity_removed",c.mob().isRemoved());boolean pass=!c.mob().isRemoved();
   for(String key:List.of("max_health","attack_damage","armor")) {
    if(c.expected().get(key).isJsonNull())pass&=after.get(key).isJsonNull();
    else pass&=Math.abs(after.get(key).getAsDouble()-c.expected().get(key).getAsDouble())<.001;
   }
   row.addProperty("status",pass?"CLIENT_RUNTIME_PASS_SYNTHETIC_RULE":"CLIENT_RUNTIME_FAIL_SYNTHETIC_RULE");all&=pass;rows.add(row);
  }
  report.add("cases",rows);report.addProperty("all_pass",all);report.addProperty("elite_stacking_tested",false);report.addProperty("natural_structures_tested",false);report.addProperty("combat_tested",false);
  if(!all)com.mojang.logging.LogUtils.getLogger().error("AO_FULL_PACK_PROBE_FAIL: synthetic rule expectations failed; inspect PR45_ORDINARY_RULE_TESTS.json");
  try{Files.writeString(Path.of("PR45_ORDINARY_RULE_TESTS.json"),new GsonBuilder().setPrettyPrinting().create().toJson(report));}
  catch(Exception e){com.mojang.logging.LogUtils.getLogger().error("AO_FULL_PACK_PROBE_FAIL",e);}
  finally{cleanup();server=null;done.run();}
 }
 private static void cleanup() {
  for(var c:cases)c.mob().discard();
  for(var f:fixtures){
   var starts=new java.util.HashMap<>(f.chunk().getAllStarts());starts.remove(f.structure());f.chunk().setAllStarts(starts);
   var refs=new java.util.HashMap<>(f.chunk().getAllReferences());refs.remove(f.structure());f.chunk().setAllReferences(refs);
  }
  if(server!=null){server.setDifficulty(oldDifficulty,true);server.overworld().getGameRules().getRule(GameRules.RULE_DOMOBSPAWNING).set(oldSpawning,server);}
  if(server!=null)for(var pos:forcedChunks)server.overworld().setChunkForced(pos.x,pos.z,false);
  forcedChunks.clear();
 }
 private static final class Box extends StructurePiece {
  Box(BlockPos p){super(StructurePieceType.MINE_SHAFT_ROOM,0,new BoundingBox(p.getX(),72,0,p.getX()+8,88,8));}
  protected void addAdditionalSaveData(StructurePieceSerializationContext context,CompoundTag tag){}
  public void postProcess(WorldGenLevel level,StructureManager manager,ChunkGenerator generator,RandomSource random,BoundingBox box,ChunkPos chunk,BlockPos pos){}
 }
}
