package dev.ambientodyssey.campaign;

import com.google.gson.*;
import dev.shadowsoffire.apotheosis.Apoth;
import dev.shadowsoffire.apotheosis.affix.ItemAffixes;
import dev.shadowsoffire.apotheosis.loot.*;
import dev.shadowsoffire.apotheosis.tiers.GenContext;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.*;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.util.RandomSource;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.item.*;
import net.neoforged.neoforge.event.entity.living.LivingDropsEvent;

/** Only appends new drops after native loot generation. Never alters native loot or gem progression. */
public final class BossRewards {
 public static final JsonObject POLICY=load();
 private static final Map<net.minecraft.world.entity.LivingEntity,Long> HANDLED=new WeakHashMap<>();
 private static final org.slf4j.Logger LOG=com.mojang.logging.LogUtils.getLogger();
 private static JsonObject load(){
  try(var in=BossRewards.class.getResourceAsStream("/ao_loot_policy.json")){
   if(in==null)throw new IllegalStateException("Missing reviewed boss loot policy");
   return JsonParser.parseReader(new InputStreamReader(in,StandardCharsets.UTF_8)).getAsJsonObject();
  }catch(java.io.IOException e){throw new IllegalStateException(e);}
 }
 public static Integer tier(String id){
  var bosses=POLICY.getAsJsonObject("bosses");var v=bosses.get(id);
  // Remnant bosses exist under legacy holder and platform namespaces; accept both, as AOCampaign does.
  if(v==null&&id.startsWith("remnant_bosses:"))v=bosses.get("remnants:"+id.substring(id.indexOf(':')+1));
  return v==null?null:v.getAsInt();
 }
 private static final Set<String> WARNED=new HashSet<>();
 private static void warnOnce(String key,String message,Object... args){if(WARNED.add(key))LOG.warn(message,args);}
 public static List<ResourceLocation> regaliaIds(){
  var ids=new ArrayList<ResourceLocation>();
  for(var v:POLICY.getAsJsonArray("regalia")){
   var id=ResourceLocation.parse(v.getAsString());
   if(Set.of("enigmaticlegacy","enigmaticlegacyplus","pasterdream","neopasterdream","simplyswords").contains(id.getNamespace()))continue;
   if(BuiltInRegistries.ITEM.containsKey(id)&&BuiltInRegistries.ITEM.get(id)!=Items.AIR)ids.add(id);
   else warnOnce("regalia:"+id,"AO_REGALIA_SKIPPED: {} is not a registered item",id);
  }
  return ids;
 }
 public static List<ResourceLocation> uniqueIds(){
  var ids=new ArrayList<ResourceLocation>();
  var tag=net.minecraft.tags.TagKey.create(net.minecraft.core.registries.Registries.ITEM,ResourceLocation.parse("simplyswords:uniques"));
  for(var v:POLICY.getAsJsonArray("unique_weapons")){
   var id=ResourceLocation.parse(v.getAsString());
   boolean ok=id.getNamespace().equals("simplyswords")&&BuiltInRegistries.ITEM.containsKey(id)&&BuiltInRegistries.ITEM.getHolder(id).map(h->h.is(tag)).orElse(false);
   if(ok)ids.add(id);
   else warnOnce("unique:"+id,"AO_UNIQUE_SKIPPED: {} is absent or not in simplyswords:uniques (optional={})",id,POLICY.getAsJsonArray("unique_weapons_optional").contains(v));
  }
  return ids;
 }
 private static ItemStack affix(GenContext context,LootRarity rarity){
  if(rarity==null)return ItemStack.EMPTY;
  for(int i=0;i<8;i++){
   var item=LootController.createRandomLootItem(context,rarity);
   if(!item.isEmpty()&&!item.getOrDefault(Apoth.Components.AFFIXES,ItemAffixes.EMPTY).isEmpty())return item;
  }
  LOG.error("AO_BOSS_BONUS_BLOCKED: native equipment factory produced no affixed item for {}",rarity);
  return ItemStack.EMPTY;
 }
 public static List<ItemStack> createBonus(ServerPlayer player,int tier,RandomSource random){
  var nativeContext=GenContext.forPlayerAtPos(random,player,player.blockPosition());
  var result=new ArrayList<ItemStack>();
  var item=affix(nativeContext,LootRarity.random(nativeContext));if(!item.isEmpty())result.add(item);
  var regalia=regaliaIds();if(!regalia.isEmpty())result.add(new ItemStack(BuiltInRegistries.ITEM.get(regalia.get(random.nextInt(regalia.size())))));
  else LOG.error("AO_BOSS_BONUS_BLOCKED: no validated Regalia IDs");
  var weapons=uniqueIds();if(!weapons.isEmpty())result.add(new ItemStack(BuiltInRegistries.ITEM.get(weapons.get(random.nextInt(weapons.size())))));
  else LOG.error("AO_BOSS_BONUS_BLOCKED: no validated Simply Swords unique IDs");
  var rates=POLICY.getAsJsonObject("rare_affix_rates").getAsJsonObject(Integer.toString(tier));
  if(rates!=null)for(var entry:rates.entrySet())if(random.nextDouble()<entry.getValue().getAsDouble()){
   var rarity=RarityRegistry.INSTANCE.getValue(ResourceLocation.parse("ao_apotheotic_port:"+entry.getKey()));
   var extra=affix(nativeContext,rarity);if(!extra.isEmpty())result.add(extra);
  }
  return result;
 }
 public void drops(LivingDropsEvent event){
  var boss=event.getEntity();if(boss.level().isClientSide())return;
  var player=event.getSource().getEntity() instanceof ServerPlayer p?p:boss.getLastHurtByPlayer() instanceof ServerPlayer p?p:null;
  if(player==null||player.level()!=boss.level())return;
  String id=BuiltInRegistries.ENTITY_TYPE.getKey(boss.getType()).toString();var tier=tier(id);if(tier==null)return;
  long tick=boss.level().getGameTime();if(Objects.equals(HANDLED.get(boss),tick))return;HANDLED.put(boss,tick);
  for(var stack:createBonus(player,tier,player.getRandom())){
   var drop=new ItemEntity(boss.level(),boss.getX(),boss.getY(),boss.getZ(),stack);drop.setTarget(player.getUUID());drop.setDefaultPickUpDelay();event.getDrops().add(drop);
  }
 }
}
