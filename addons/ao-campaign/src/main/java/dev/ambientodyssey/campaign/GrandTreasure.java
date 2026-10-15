package dev.ambientodyssey.campaign;

import com.google.gson.*;
import com.mojang.serialization.MapCodec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import it.unimi.dsi.fastutil.objects.ObjectArrayList;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.util.*;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.*;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.storage.loot.*;
import net.minecraft.world.level.storage.loot.parameters.LootContextParams;
import net.minecraft.world.level.storage.loot.predicates.LootItemCondition;
import net.neoforged.neoforge.common.loot.*;

/** Appends one exact native-pool draw; never regenerates a full native table or rewrites its odds. */
public final class GrandTreasure extends LootModifier {
 public static final MapCodec<GrandTreasure> CODEC=RecordCodecBuilder.mapCodec(i->LootModifier.codecStart(i).apply(i,GrandTreasure::new));
 private static final ThreadLocal<Boolean> ACTIVE=ThreadLocal.withInitial(()->false);
 private final Set<LootContext> handled=Collections.newSetFromMap(new WeakHashMap<>());
 private final Map<String,LootTable> cache=new HashMap<>();
 private final Set<String> rejected=new HashSet<>();
 public GrandTreasure(LootItemCondition[] conditions){super(conditions);}
 public MapCodec<? extends IGlobalLootModifier> codec(){return CODEC;}
 public JsonObject matching(LootContext ctx){
  var origin=ctx.getParamOrNull(LootContextParams.ORIGIN);if(origin==null||!ctx.getLevel().dimension().equals(Level.OVERWORLD))return null;
  String table=ctx.getQueriedLootTableId().toString();
  if(table.startsWith("minecraft:")||table.startsWith("minecells:"))return null;
  var registry=ctx.getLevel().registryAccess().registryOrThrow(Registries.STRUCTURE);
  for(var v:BossRewards.POLICY.getAsJsonArray("grand_treasure")){
   var row=v.getAsJsonObject();if(!table.equals(row.get("table").getAsString()))continue;
   var structure=registry.get(ResourceLocation.parse(row.get("structure").getAsString()));
   if(structure!=null&&ctx.getLevel().structureManager().getStructureAt(BlockPos.containing(origin),structure).isValid())return row;
  }
  return null;
 }
 private LootTable nativeSinglePool(LootContext ctx,JsonObject row){
  String source=row.get("source_resource").getAsString();String key=source+"#"+row.get("pool_index").getAsInt();
  if(rejected.contains(key))return null;
  // A resource reload changes the resource manager; cache per server resource identity.
  String cached=System.identityHashCode(ctx.getLevel().getServer().getResourceManager())+":"+key;
  if(cache.containsKey(cached))return cache.get(cached);
  try{
   String[] path=source.substring(5).split("/",2);var resource=ResourceLocation.fromNamespaceAndPath(path[0],path[1]);
   byte[] bytes;
   try(var in=ctx.getLevel().getServer().getResourceManager().getResourceOrThrow(resource).open()){bytes=in.readAllBytes();}
   String digest=HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(bytes));
   if(!digest.equals(row.get("source_sha256").getAsString()))throw new IllegalStateException("Effective source hash changed");
   var original=JsonParser.parseString(new String(bytes,StandardCharsets.UTF_8)).getAsJsonObject();
   var pool=original.getAsJsonArray("pools").get(row.get("pool_index").getAsInt()).getAsJsonObject().deepCopy();
   pool.addProperty("rolls",1);pool.addProperty("bonus_rolls",0);
   var one=new JsonObject();one.addProperty("type","minecraft:chest");var pools=new JsonArray();pools.add(pool);one.add("pools",pools);
   if(original.has("functions"))one.add("functions",original.get("functions").deepCopy());
   var ops=RegistryOps.create(com.mojang.serialization.JsonOps.INSTANCE,ctx.getLevel().registryAccess());
   LootTable table=LootTable.DIRECT_CODEC.parse(ops,one).getOrThrow();cache.put(cached,table);return table;
  }catch(Exception e){rejected.add(key);com.mojang.logging.LogUtils.getLogger().error("AO_GRAND_SOURCE_BLOCKED: {}: {}",source,e.toString());return null;}
 }
 protected ObjectArrayList<ItemStack> doApply(ObjectArrayList<ItemStack> nativeLoot,LootContext ctx){
  if(ACTIVE.get()||handled.contains(ctx))return nativeLoot;
  var row=matching(ctx);if(row==null)return nativeLoot;handled.add(ctx);
  var single=nativeSinglePool(ctx,row);if(single==null||ctx.getRandom().nextFloat()>=.05F)return nativeLoot;
  var additions=new ObjectArrayList<ItemStack>();
  ACTIVE.set(true);
  try{single.getRandomItemsRaw(ctx,additions::add);}finally{ACTIVE.set(false);}
  nativeLoot.addAll(additions);return nativeLoot;
 }
}
