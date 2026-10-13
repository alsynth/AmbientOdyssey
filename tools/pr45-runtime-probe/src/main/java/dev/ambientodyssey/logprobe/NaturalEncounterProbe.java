package dev.ambientodyssey.logprobe;

import com.google.gson.*;
import net.minecraft.core.HolderSet;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.level.ChunkPos;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.chunk.status.ChunkStatus;
import net.minecraft.world.level.levelgen.structure.Structure;
import net.minecraft.world.phys.AABB;
import net.neoforged.neoforge.common.NeoForge;
import net.neoforged.neoforge.event.tick.ServerTickEvent;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

/** Observes natural structure placement in an isolated normal-terrain Nether. */
final class NaturalEncounterProbe {
 private static final String[] IDS={"eternalnether:catacomb","eternalnether:citadel","eternalnether:piglin_manor"};
 private static MinecraftServer server;
 private static int finishAt;
 private static Runnable done;
 private static JsonArray results;

 static void start(MinecraftServer active,Runnable completion) {
  server=active;done=completion;results=new JsonArray();
  try {
   ServerLevel nether=server.getLevel(Level.NETHER);
   if(nether==null)throw new IllegalStateException("Nether dimension is unavailable");
   var registry=server.registryAccess().registryOrThrow(Registries.STRUCTURE);
   for(String id:IDS) {
    var row=new JsonObject();row.addProperty("structure",id);
    var holder=registry.getHolder(ResourceLocation.parse(id));
    if(holder.isEmpty()){row.addProperty("status","NOT_REGISTERED");results.add(row);continue;}
    var target=nether.getChunkSource().getGenerator().findNearestMapStructure(nether,HolderSet.direct(holder.get()),net.minecraft.core.BlockPos.ZERO,32,false);
    if(target==null){row.addProperty("status","NO_NATURAL_START_FOUND_WITHIN_RADIUS_32_CHUNKS");results.add(row);continue;}
    var origin=target.getFirst();var structure=target.getSecond().value();
    row.addProperty("located_x",origin.getX());row.addProperty("located_z",origin.getZ());row.addProperty("located_structure",target.getSecond().unwrapKey().map(k->k.location().toString()).orElse("unknown"));
    var startChunk=nether.getChunkSource().getChunk(origin.getX()>>4,origin.getZ()>>4,ChunkStatus.FULL,true);
    var start=startChunk.getStartForStructure(structure);
    if(start==null||!start.isValid()){row.addProperty("status","LOCATED_BUT_NO_GENERATED_START_AFTER_FULL_CHUNK");results.add(row);continue;}
    var bounds=start.getBoundingBox();row.addProperty("status","NATURAL_STRUCTURE_START_GENERATED");
    row.addProperty("start_chunk_x",startChunk.getPos().x);row.addProperty("start_chunk_z",startChunk.getPos().z);row.addProperty("piece_count",start.getPieces().size());
    var bb=new AABB(bounds.minX(),bounds.minY(),bounds.minZ(),bounds.maxX()+1,bounds.maxY()+1,bounds.maxZ()+1);
    int minX=bounds.minX()>>4,maxX=bounds.maxX()>>4,minZ=bounds.minZ()>>4,maxZ=bounds.maxZ()>>4;
    List<net.minecraft.world.level.chunk.LevelChunk> chunks=new ArrayList<>();
    for(int cx=minX;cx<=maxX;cx++)for(int cz=minZ;cz<=maxZ;cz++)chunks.add(nether.getChunk(cx,cz));
    var mobs=new JsonArray();
    for(var entity:nether.getEntities((net.minecraft.world.entity.Entity)null,bb,e->e.isAlive()))if(entity instanceof Mob mob) {
     var m=new JsonObject();m.addProperty("type",net.minecraft.core.registries.BuiltInRegistries.ENTITY_TYPE.getKey(mob.getType()).toString());
     m.addProperty("x",mob.getX());m.addProperty("y",mob.getY());m.addProperty("z",mob.getZ());m.addProperty("health",mob.getHealth());
     m.addProperty("max_health",mob.getAttributeValue(Attributes.MAX_HEALTH));
     m.addProperty("attack_damage",mob.getAttribute(Attributes.ATTACK_DAMAGE)==null?0:mob.getAttributeValue(Attributes.ATTACK_DAMAGE));
     m.addProperty("armor",mob.getAttributeValue(Attributes.ARMOR));
     m.addProperty("persistent",mob.isPersistenceRequired());m.addProperty("custom_name",mob.hasCustomName());mobs.add(m);
    }
    row.add("mobs_in_generated_bounds",mobs);
    var spawners=new JsonArray();
    for(var chunk:chunks)for(var pos:chunk.getBlockEntitiesPos())if(chunk.getBlockState(pos).is(Blocks.SPAWNER)&&bounds.isInside(pos)) {
     var s=new JsonObject();s.addProperty("x",pos.getX());s.addProperty("y",pos.getY());s.addProperty("z",pos.getZ());
     var be=chunk.getBlockEntity(pos);if(be!=null)s.addProperty("block_entity_nbt",be.saveWithoutMetadata(nether.registryAccess()).toString());
     spawners.add(s);
    }
    row.addProperty("ordinary_spawner_count_in_generated_bounds",spawners.size());row.add("spawners",spawners);results.add(row);
   }
   finishAt=server.getTickCount()+40;NeoForge.EVENT_BUS.addListener(NaturalEncounterProbe::tick);
  }catch(Exception|LinkageError e){cleanup(e);}
 }

 private static void tick(ServerTickEvent.Post event) {
  if(server==null||event.getServer()!=server||server.getTickCount()<finishAt)return;
  var report=new JsonObject();report.addProperty("world_seed",48127);report.addProperty("world_preset","minecraft:normal");report.addProperty("dimension","minecraft:the_nether");report.addProperty("difficulty","normal");report.addProperty("scope","naturally located structures forced to FULL chunks in disposable normal-terrain world; observed mob/spawner state in generated piece bounding boxes");report.add("structures",results);
  try{Files.writeString(Path.of("PR45_NATURAL_ENCOUNTERS.json"),new GsonBuilder().setPrettyPrinting().create().toJson(report));}
  catch(Exception e){com.mojang.logging.LogUtils.getLogger().error("AO_FULL_PACK_PROBE_FAIL",e);}
  boolean found=results.asList().stream().anyMatch(r->r.getAsJsonObject().get("status").getAsString().equals("NATURAL_STRUCTURE_START_GENERATED"));
  com.mojang.logging.LogUtils.getLogger().info("AO_NATURAL_STRUCTURE_PROBE_{}: generated_starts={}/{}",found?"PASS":"NO_STARTS",results.asList().stream().filter(r->r.getAsJsonObject().get("status").getAsString().equals("NATURAL_STRUCTURE_START_GENERATED")).count(),IDS.length);
  cleanup(null);
 }
 private static void cleanup(Throwable e){if(e!=null)com.mojang.logging.LogUtils.getLogger().error("AO_FULL_PACK_PROBE_FAIL",e);if(server!=null){var mc=net.minecraft.client.Minecraft.getInstance();mc.execute(mc::stop);}server=null;}
}
