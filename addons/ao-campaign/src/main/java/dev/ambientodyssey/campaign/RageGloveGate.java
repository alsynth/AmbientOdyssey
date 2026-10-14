package dev.ambientodyssey.campaign;

import com.mojang.serialization.MapCodec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import it.unimi.dsi.fastutil.objects.ObjectArrayList;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.storage.loot.LootContext;
import net.minecraft.world.level.storage.loot.parameters.LootContextParams;
import net.minecraft.world.level.storage.loot.predicates.LootItemCondition;
import net.neoforged.neoforge.common.loot.IGlobalLootModifier;
import net.neoforged.neoforge.common.loot.LootModifier;

/** The native Relics Nether/Nether-like injection is filtered, then one boss roll is added. */
public final class RageGloveGate extends LootModifier {
    public static final ResourceLocation GLOVE = ResourceLocation.parse("relics:rage_glove");
    public static final ResourceLocation BOSS = ResourceLocation.parse("cataclysm:netherite_monstrosity");
    public static final MapCodec<RageGloveGate> CODEC = RecordCodecBuilder.mapCodec(
        i -> LootModifier.codecStart(i).apply(i, RageGloveGate::new));
    public RageGloveGate(LootItemCondition[] conditions) { super(conditions); }
    public MapCodec<? extends IGlobalLootModifier> codec() { return CODEC; }
    protected ObjectArrayList<ItemStack> doApply(ObjectArrayList<ItemStack> loot, LootContext ctx) {
        loot.removeIf(stack -> GLOVE.equals(BuiltInRegistries.ITEM.getKey(stack.getItem())));
        var entity = ctx.getParamOrNull(LootContextParams.THIS_ENTITY);
        if (entity != null && BOSS.equals(BuiltInRegistries.ENTITY_TYPE.getKey(entity.getType()))
            && ctx.getLevel().dimension().equals(Level.NETHER)
            && ctx.hasParam(LootContextParams.LAST_DAMAGE_PLAYER)
            && ctx.getQueriedLootTableId().equals(ResourceLocation.parse("cataclysm:entities/netherite_monstrosity"))
            && BuiltInRegistries.ITEM.containsKey(GLOVE) && ctx.getRandom().nextFloat() < 0.10F) {
            loot.add(new ItemStack(BuiltInRegistries.ITEM.get(GLOVE)));
        }
        return loot;
    }
}
