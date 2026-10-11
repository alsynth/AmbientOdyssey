package dev.ambientodyssey.affixtrims;

import com.mojang.serialization.MapCodec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import it.unimi.dsi.fastutil.objects.ObjectArrayList;
import java.util.List;
import net.minecraft.core.Holder;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.core.component.DataComponents;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.tags.ItemTags;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.armortrim.ArmorTrim;
import net.minecraft.world.item.armortrim.TrimMaterial;
import net.minecraft.world.item.armortrim.TrimPattern;
import net.minecraft.world.level.storage.loot.LootContext;
import net.minecraft.world.level.storage.loot.predicates.LootItemCondition;
import net.neoforged.neoforge.common.loot.IGlobalLootModifier;
import net.neoforged.neoforge.common.loot.LootModifier;

public final class RandomAffixArmorTrimModifier extends LootModifier {
    public static final MapCodec<RandomAffixArmorTrimModifier> CODEC = RecordCodecBuilder.mapCodec(
            inst -> LootModifier.codecStart(inst).apply(inst, RandomAffixArmorTrimModifier::new));
    private static final ResourceLocation RARITY = ResourceLocation.fromNamespaceAndPath("apotheosis", "rarity");
    private static final ResourceLocation AFFIXES = ResourceLocation.fromNamespaceAndPath("apotheosis", "affixes");

    public RandomAffixArmorTrimModifier(LootItemCondition[] conditions) {
        super(conditions);
    }

    @Override public MapCodec<? extends IGlobalLootModifier> codec() { return CODEC; }

    @Override protected ObjectArrayList<ItemStack> doApply(ObjectArrayList<ItemStack> generated, LootContext context) {
        var rarity = BuiltInRegistries.DATA_COMPONENT_TYPE.getOptional(RARITY);
        var affixes = BuiltInRegistries.DATA_COMPONENT_TYPE.getOptional(AFFIXES);
        if (rarity.isEmpty() || affixes.isEmpty()) return generated;
        Registry<TrimMaterial> materials = context.getLevel().registryAccess().registryOrThrow(Registries.TRIM_MATERIAL);
        Registry<TrimPattern> patterns = context.getLevel().registryAccess().registryOrThrow(Registries.TRIM_PATTERN);
        List<Holder.Reference<TrimMaterial>> vanillaMaterials = materials.holders()
                .filter(h -> h.key().location().getNamespace().equals("minecraft")).toList();
        List<Holder.Reference<TrimPattern>> vanillaPatterns = patterns.holders()
                .filter(h -> h.key().location().getNamespace().equals("minecraft")).toList();
        if (vanillaMaterials.isEmpty() || vanillaPatterns.isEmpty()) return generated;
        for (ItemStack item : generated) {
            if (item.isEmpty() || !item.is(ItemTags.TRIMMABLE_ARMOR)
                    || item.has(DataComponents.TRIM)
                    || !item.has(rarity.get()) || !item.has(affixes.get())) continue;
            var material = vanillaMaterials.get(context.getRandom().nextInt(vanillaMaterials.size()));
            var pattern = vanillaPatterns.get(context.getRandom().nextInt(vanillaPatterns.size()));
            item.set(DataComponents.TRIM, new ArmorTrim(material, pattern));
        }
        return generated;
    }
}
