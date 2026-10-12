package dev.ambientodyssey.affixtrims;

import com.mojang.serialization.MapCodec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import it.unimi.dsi.fastutil.objects.ObjectArrayList;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.storage.loot.LootContext;
import net.minecraft.world.level.storage.loot.predicates.LootItemCondition;
import net.neoforged.neoforge.common.loot.IGlobalLootModifier;
import net.neoforged.neoforge.common.loot.LootModifier;

public final class RandomAffixArmorTrimModifier extends LootModifier {
    public static final MapCodec<RandomAffixArmorTrimModifier> CODEC = RecordCodecBuilder.mapCodec(
            inst -> LootModifier.codecStart(inst).apply(inst, RandomAffixArmorTrimModifier::new));

    public RandomAffixArmorTrimModifier(LootItemCondition[] conditions) {
        super(conditions);
    }

    @Override public MapCodec<? extends IGlobalLootModifier> codec() { return CODEC; }

    @Override protected ObjectArrayList<ItemStack> doApply(ObjectArrayList<ItemStack> generated, LootContext context) {
        for (ItemStack item : generated) {
            AffixTrims.apply(item, context.getLevel().registryAccess());
        }
        return generated;
    }
}
