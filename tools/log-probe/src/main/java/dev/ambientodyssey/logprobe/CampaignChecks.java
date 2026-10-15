package dev.ambientodyssey.logprobe;

import dev.ambientodyssey.campaign.AOCampaign;
import dev.ambientodyssey.campaign.BossRewards;
import dev.ambientodyssey.campaign.GrandTreasure;
import dev.ambientodyssey.augmentingsigils.SigilCosts;
import dev.shadowsoffire.apotheosis.Apoth;
import dev.shadowsoffire.apotheosis.affix.ItemAffixes;
import dev.shadowsoffire.apotheosis.loot.LootController;
import dev.shadowsoffire.apotheosis.loot.RarityRegistry;
import dev.shadowsoffire.apotheosis.tiers.GenContext;
import dev.shadowsoffire.apotheosis.tiers.WorldTier;
import it.unimi.dsi.fastutil.objects.ObjectArrayList;
import java.util.Optional;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.MinecraftServer;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.storage.loot.LootContext;
import net.minecraft.world.level.storage.loot.LootParams;
import net.minecraft.world.level.storage.loot.parameters.LootContextParams;
import net.minecraft.world.level.storage.loot.parameters.LootContextParamSets;
import net.minecraft.world.level.storage.loot.predicates.LootItemCondition;
import net.minecraft.world.phys.Vec3;

/** Synthetic full-pack engine checks. This is not a natural boss fight or multiplayer certification. */
public final class CampaignChecks {
 private static final java.util.List<String> failures=new java.util.ArrayList<>();
 private static void check(boolean pass,String message){if(!pass){failures.add(message);com.mojang.logging.LogUtils.getLogger().error("AO_CAMPAIGN_CHECK_FAIL: {}",message);}}
 public static void run(MinecraftServer server){
  failures.clear();
  var player=server.getPlayerList().getPlayers().getFirst();
  var level=player.serverLevel();
  for(String id:AOCampaign.BOSSES.keySet()) {
   boolean exists=BuiltInRegistries.ENTITY_TYPE.containsKey(ResourceLocation.parse(id));
   if(!exists&&id.startsWith("remnants:"))exists=BuiltInRegistries.ENTITY_TYPE.containsKey(ResourceLocation.parse(id.replace("remnants:","remnant_bosses:")));
   check(exists,"Missing boss registry: "+id);
  }
  com.mojang.logging.LogUtils.getLogger().info("AO_REMNANT_NATIVE_ENTITY_IDS: {}",BuiltInRegistries.ENTITY_TYPE.keySet().stream().filter(id->id.getNamespace().contains("remnant")).sorted().toList());
  var zombie=EntityType.ZOMBIE.create(level);
  for(String id:AOCampaign.DISABLED){
   var effect=BuiltInRegistries.MOB_EFFECT.getHolder(ResourceLocation.parse(id)).orElseThrow();
   check(!zombie.addEffect(new MobEffectInstance(effect,100)),"Disabled effect applied: "+id);
  }
  check(zombie.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SPEED,100)),"Unrelated vanilla effect blocked");
  check(SigilCosts.fromId(ResourceLocation.parse("ao_apotheotic_port:ancient"),1,false)==6,"r19 Ancient alias failed");
  // Native gems remain authoritative: never exercise the obsolete custom gem-grant path.
  var regalia=BossRewards.regaliaIds();var uniques=BossRewards.uniqueIds();
  check(regalia.size()==BossRewards.POLICY.getAsJsonArray("regalia").size(),"A required curated Regalia item is not registered");
  var optional=BossRewards.POLICY.getAsJsonArray("unique_weapons_optional");
  for(var id:BossRewards.POLICY.getAsJsonArray("unique_weapons"))
   if(!optional.contains(id))check(uniques.contains(ResourceLocation.parse(id.getAsString())),"Required native unique absent: "+id);
  check(!uniques.isEmpty(),"No native unique weapon available");
  var samples=new com.google.gson.JsonObject();
  for(int tier:new int[]{4,5,6,7,8,9}){
   var counts=new java.util.TreeMap<String,Integer>();
   for(int i=0;i<100;i++){
    var bonus=BossRewards.createBonus(player,tier,player.getRandom());
    check(bonus.size()>=3,"Missing guaranteed boss bonus at tier "+tier);
    if(bonus.size()<3)continue;
    check(!bonus.getFirst().getOrDefault(Apoth.Components.AFFIXES,ItemAffixes.EMPTY).isEmpty(),"Guaranteed reward is not affixed");
    check(regalia.contains(BuiltInRegistries.ITEM.getKey(bonus.get(1).getItem())),"Reward outside curated Regalia");
    check(uniques.contains(BuiltInRegistries.ITEM.getKey(bonus.get(2).getItem())),"Ordinary/non-unique weapon rewarded");
    for(int n=3;n<bonus.size();n++){
     var stack=bonus.get(n);check(!stack.getOrDefault(Apoth.Components.AFFIXES,ItemAffixes.EMPTY).isEmpty(),"Extra rarity reward has no affixes");
     var rarityId=RarityRegistry.INSTANCE.getKey(stack.get(Apoth.Components.RARITY).get()).toString();
     counts.merge(rarityId,1,Integer::sum);
    }
    if(tier==4||tier==5||tier==9)check(bonus.size()==3,"Unapproved rare extra at tier "+tier);
   }
   samples.add(Integer.toString(tier),new com.google.gson.Gson().toJsonTree(counts));
  }
  var observations=new com.google.gson.JsonObject();observations.add("extra_rarity_counts_per_100",samples);
  observations.add("registered_regalia",new com.google.gson.Gson().toJsonTree(regalia.stream().map(Object::toString).toList()));
  observations.add("registered_uniques",new com.google.gson.Gson().toJsonTree(uniques.stream().map(Object::toString).toList()));
  observations.addProperty("scope","Native factory fixtures only; no natural kill, party credit or Lootr certification");
  try{java.nio.file.Files.writeString(java.nio.file.Path.of("BOSS_REWARD_NATIVE_OBSERVATIONS.json"),new com.google.gson.GsonBuilder().setPrettyPrinting().create().toJson(observations));}catch(java.io.IOException e){throw new IllegalStateException(e);}
  var modifier=new GrandTreasure(new LootItemCondition[0]);
  var params=new LootParams.Builder(level).withParameter(LootContextParams.ORIGIN,Vec3.ZERO).create(LootContextParamSets.CHEST);
  var ctx=new LootContext.Builder(params).create(Optional.empty());ctx.setQueriedLootTableId(ResourceLocation.parse("minecraft:chests/nether_bridge"));
  var loot=new ObjectArrayList<ItemStack>();var diamond=new ItemStack(Items.DIAMOND,3);loot.add(diamond);
  modifier.apply(loot,ctx);check(loot.size()==1&&loot.getFirst()==diamond&&diamond.getCount()==3,"Grand modifier changed unrelated native loot");
  var rarity=RarityRegistry.INSTANCE.getValue(ResourceLocation.parse("apotheosis:mythic"));
  var equipment=LootController.createLootItem(new ItemStack(Items.DIAMOND_SWORD),rarity,
    GenContext.standalone(player.getRandom(),WorldTier.PINNACLE,0,level,player.blockPosition()));
  check(!equipment.getOrDefault(Apoth.Components.AFFIXES,ItemAffixes.EMPTY).isEmpty(),"Native test affix roll failed");
  equipment.setDamageValue(11);player.setItemInHand(InteractionHand.MAIN_HAND,equipment);
  server.getCommands().performPrefixedCommand(player.createCommandSourceStack(),"ao_mastery upgrade");
  check(!player.getPersistentData().getCompound(AOCampaign.STATE).getBoolean("heirloom_claimed"),"Ungated mastery claim allowed");
  var state=player.getPersistentData().getCompound(AOCampaign.STATE);
  state.putBoolean("tier_8",true);state.putBoolean("irons_spellbooks:fire_boss",true);state.putBoolean("cataclysm:scylla",true);
  player.getPersistentData().put(AOCampaign.STATE,state);
  server.getCommands().performPrefixedCommand(player.createCommandSourceStack(),"ao_mastery upgrade");
  check(!player.getPersistentData().getCompound(AOCampaign.STATE).getBoolean("heirloom_claimed"),"Mastery allowed before Obsidilith milestone");
  state.putBoolean("bosses_of_mass_destruction:obsidilith",true);
  player.getPersistentData().put(AOCampaign.STATE,state);
  var affixes=equipment.get(Apoth.Components.AFFIXES);
  server.getCommands().performPrefixedCommand(player.createCommandSourceStack(),"ao_mastery upgrade");
  check(player.getMainHandItem()==equipment&&equipment.getCount()==1&&equipment.getDamageValue()==11,"Mastery replaced/duplicated/reset held item");
  check(equipment.get(Apoth.Components.AFFIXES).equals(affixes),"Mastery rerolled affixes");
  check(RarityRegistry.INSTANCE.getKey(equipment.get(Apoth.Components.RARITY).get()).toString().equals("ao_apotheotic_port:heirloom"),"Mastery rarity not Heirloom");
  check(player.getPersistentData().getCompound(AOCampaign.STATE).getBoolean("heirloom_claimed"),"Mastery claim not persisted");
  player.setItemInHand(InteractionHand.MAIN_HAND,new ItemStack(Items.DIAMOND_SWORD));
  server.getCommands().performPrefixedCommand(player.createCommandSourceStack(),"ao_mastery upgrade");
  check(player.getMainHandItem().get(Apoth.Components.RARITY)==null,"Second mastery claim allowed");
  try{
   Class<?> manager=Class.forName("org.infernalstudios.questlog.core.QuestManager");
   Object quests=manager.getConstructor(net.minecraft.world.entity.player.Player.class).newInstance(player);
   manager.getMethod("createAllQuests").invoke(quests);
   var all=(java.util.List<?>)manager.getMethod("getAllQuests").invoke(quests);
   check(all.size()==153,"Native Questlog loaded "+all.size()+" rather than 153 quests");
  }catch(ReflectiveOperationException e){throw new IllegalStateException("Questlog native parse check failed",e);}
  if(!failures.isEmpty())throw new IllegalStateException(String.join("; ",failures));
  com.mojang.logging.LogUtils.getLogger().info("AO_CAMPAIGN_SYNTHETIC_PASS: boss/effect registries, 600 native boss reward factory samples, unique-only policy, r19 Sigil alias, Grand negative control, guarded held-item preservation/one-claim and 153 native quests");
 }
}
