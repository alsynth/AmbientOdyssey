package dev.ambientodyssey.logprobe;

import com.google.gson.*;
import java.nio.file.*;
import net.minecraft.core.registries.*;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.MinecraftServer;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.Attributes;

/** Diagnostic observations in an actual integrated engine, not natural combat acceptance. */
final class IntegrationChecks {
 static void run(MinecraftServer server) throws Exception {
  var report=new JsonObject();var zones=new JsonArray();var bosses=new JsonArray();
  var structures=server.registryAccess().registryOrThrow(Registries.STRUCTURE);
  var config=JsonParser.parseString(Files.readString(Path.of("config/dungeon_difficulty/difficulty_v2.json"))).getAsJsonObject();
  for(var d:config.getAsJsonArray("dimensions"))for(var z:d.getAsJsonObject().getAsJsonArray("zones")){
   String id=z.getAsJsonObject().getAsJsonObject("zone_matches").get("structure").getAsString();
   var row=new JsonObject();row.addProperty("id",id);row.addProperty("registered",structures.containsKey(ResourceLocation.parse(id)));
   var key=ResourceLocation.parse(id);var resource=ResourceLocation.fromNamespaceAndPath(key.getNamespace(),"worldgen/structure/"+key.getPath()+".json");
   var winner=server.getResourceManager().getResource(resource);row.addProperty("effective_resource_pack",winner.map(r->r.sourcePackId()).orElse("registry/code source"));zones.add(row);
   if(!structures.containsKey(ResourceLocation.parse(id)))throw new IllegalStateException("DD structure missing: "+id);
  }
  if(structures.keySet().stream().anyMatch(id->id.getNamespace().equals("skyarena")))throw new IllegalStateException("Removed Sky Arena structure registered");
  for(String id:new String[]{"irons_spellbooks:dead_king","cataclysm:kobolediator","cataclysm:ignited_revenant","cataclysm:ender_guardian","cataclysm:ignis","cataclysm:the_leviathan","cataclysm:maledictus","cataclysm:scylla","bosses_of_mass_destruction:lich","bosses_of_mass_destruction:void_blossom","bosses_of_mass_destruction:gauntlet","bosses_of_mass_destruction:obsidilith","aquamirae:captain_cornelia","fdbosses:chesed","fdbosses:malkuth","fdbosses:geburah"}){
   var key=ResourceLocation.parse(id);var row=new JsonObject();row.addProperty("id",id);row.addProperty("registered",BuiltInRegistries.ENTITY_TYPE.containsKey(key));
   if(BuiltInRegistries.ENTITY_TYPE.containsKey(key)){
    var entity=BuiltInRegistries.ENTITY_TYPE.get(key).create(server.overworld());
    if(entity instanceof LivingEntity living){
     row.addProperty("created_max_hp",living.getMaxHealth());row.addProperty("created_attack",living.getAttribute(Attributes.ATTACK_DAMAGE)==null?null:living.getAttributeValue(Attributes.ATTACK_DAMAGE));
     if(entity instanceof net.minecraft.world.entity.Mob mob){
      mob.finalizeSpawn(server.overworld(),server.overworld().getCurrentDifficultyAt(mob.blockPosition()),net.minecraft.world.entity.MobSpawnType.COMMAND,null);
      row.addProperty("finalized_max_hp",living.getMaxHealth());row.addProperty("finalized_attack",living.getAttribute(Attributes.ATTACK_DAMAGE)==null?null:living.getAttributeValue(Attributes.ATTACK_DAMAGE));
     }
    }
    if(entity!=null)entity.discard();
   }
   bosses.add(row);
  }
  var packs=new JsonArray();server.getPackRepository().getSelectedIds().forEach(packs::add);
  report.add("enabled_datapacks",packs);report.add("dd_registry_checks",zones);report.add("created_boss_attributes",bosses);
  var stones=java.util.Set.of("enigmaticlegacyplus:blazing_core","enigmaticlegacyplus:golem_heart","enigmaticlegacyplus:ocean_stone","enigmaticlegacyplus:angel_blessing","enigmaticlegacyplus:lost_engine");
  for(String id:stones)if(!BuiltInRegistries.ITEM.containsKey(ResourceLocation.parse(id)))throw new IllegalStateException("Starter stone missing: "+id);
  var table=server.reloadableRegistries().getLootTable(net.minecraft.resources.ResourceKey.create(Registries.LOOT_TABLE,ResourceLocation.parse("minecraft:chests/spawn_bonus_chest")));
  var rolls=new JsonObject();var stoneCounts=new java.util.TreeMap<String,Integer>();var rarities=new java.util.TreeMap<String,Integer>();
  for(int i=0;i<600;i++){
   var params=new net.minecraft.world.level.storage.loot.LootParams.Builder(server.overworld()).withParameter(net.minecraft.world.level.storage.loot.parameters.LootContextParams.ORIGIN,net.minecraft.world.phys.Vec3.ZERO).create(net.minecraft.world.level.storage.loot.parameters.LootContextParamSets.CHEST);
   var loot=table.getRandomItems(params);int stone=0,affixed=0;
   for(var stack:loot){
    String id=BuiltInRegistries.ITEM.getKey(stack.getItem()).toString();if(stones.contains(id)){stone+=stack.getCount();stoneCounts.merge(id,1,Integer::sum);}
    if(!stack.getOrDefault(dev.shadowsoffire.apotheosis.Apoth.Components.AFFIXES,dev.shadowsoffire.apotheosis.affix.ItemAffixes.EMPTY).isEmpty()){
     affixed++;var r=stack.get(dev.shadowsoffire.apotheosis.Apoth.Components.RARITY);String rarity=dev.shadowsoffire.apotheosis.loot.RarityRegistry.INSTANCE.getKey(r.get()).getPath();rarities.merge(rarity,1,Integer::sum);
    }
   }
   if(stone!=1||affixed!=1)throw new IllegalStateException("Starter integrated roll "+i+" has stones="+stone+" affixed="+affixed);
  }
  rolls.addProperty("rolls",600);rolls.add("stone_counts",new Gson().toJsonTree(stoneCounts));rolls.add("rarity_counts",new Gson().toJsonTree(rarities));report.add("native_bonus_table_samples",rolls);
  report.addProperty("scope","Engine creation observations only; not spawned/finalized fights, respawn, ability damage, natural worldgen or multiplayer");
  Files.writeString(Path.of("MASTER_NATIVE_OBSERVATIONS.json"),new GsonBuilder().setPrettyPrinting().create().toJson(report));
  com.mojang.logging.LogUtils.getLogger().info("AO_MASTER_REGISTRY_PASS: {} scoped DD structures registered; Sky Arena absent",zones.size());
 }
}
