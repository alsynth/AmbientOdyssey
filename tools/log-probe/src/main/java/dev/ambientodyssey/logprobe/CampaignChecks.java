package dev.ambientodyssey.logprobe;

import dev.ambientodyssey.campaign.AOCampaign;
import dev.ambientodyssey.campaign.BossGems;
import dev.ambientodyssey.campaign.RageGloveGate;
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
  for(String id:AOCampaign.BOSSES.keySet()) check(BuiltInRegistries.ENTITY_TYPE.containsKey(ResourceLocation.parse(id)),"Missing boss registry: "+id);
  var zombie=EntityType.ZOMBIE.create(level);
  for(String id:AOCampaign.DISABLED){
   var effect=BuiltInRegistries.MOB_EFFECT.getHolder(ResourceLocation.parse(id)).orElseThrow();
   check(!zombie.addEffect(new MobEffectInstance(effect,100)),"Disabled effect applied: "+id);
  }
  check(zombie.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SPEED,100)),"Unrelated vanilla effect blocked");
  check(SigilCosts.fromId(ResourceLocation.parse("ao_apotheotic_port:ancient"),1,false)==6,"r19 Ancient alias failed");
  for(String grade:new String[]{"artifact","heirloom","esoteric"}){
   var gem=BossGems.create(player,grade);check(!gem.isEmpty(),"Missing native "+grade+" gem reward");
  }
  var modifier=new RageGloveGate(new LootItemCondition[0]);
  var params=new LootParams.Builder(level).withParameter(LootContextParams.ORIGIN,Vec3.ZERO).create(LootContextParamSets.CHEST);
  var ctx=new LootContext.Builder(params).create(Optional.empty());ctx.setQueriedLootTableId(ResourceLocation.parse("minecraft:chests/nether_bridge"));
  var loot=new ObjectArrayList<ItemStack>();loot.add(new ItemStack(BuiltInRegistries.ITEM.get(RageGloveGate.GLOVE)));loot.add(new ItemStack(Items.DIAMOND,3));
  modifier.apply(loot,ctx);check(loot.size()==1&&loot.getFirst().is(Items.DIAMOND)&&loot.getFirst().getCount()==3,"Rage filter touched unrelated loot");
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
  com.mojang.logging.LogUtils.getLogger().info("AO_CAMPAIGN_SYNTHETIC_PASS: boss/effect registries, native gem grades, r19 Sigil alias, loot filter, guarded held-item preservation/one-claim and 153 native quests");
 }
}
