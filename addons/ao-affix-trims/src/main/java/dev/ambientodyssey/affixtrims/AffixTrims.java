package dev.ambientodyssey.affixtrims;

import dev.shadowsoffire.apotheosis.affix.AffixHelper;
import net.minecraft.core.RegistryAccess;
import net.minecraft.core.component.DataComponents;
import net.minecraft.core.registries.Registries;
import net.minecraft.tags.ItemTags;
import net.minecraft.util.RandomSource;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.armortrim.ArmorTrim;

/** Cosmetic only: preserve existing trims and every other item component. */
public final class AffixTrims {
    private AffixTrims() {}

    public static boolean apply(ItemStack stack, RegistryAccess registries, RandomSource random) {
        if (stack.isEmpty() || !stack.is(ItemTags.TRIMMABLE_ARMOR)
                || stack.has(DataComponents.TRIM) || !AffixHelper.getRarity(stack).isBound()
                || !AffixHelper.hasAffixes(stack)) return false;
        var materials = registries.registryOrThrow(Registries.TRIM_MATERIAL).holders()
                .filter(h -> h.key().location().getNamespace().equals("minecraft")).toList();
        var patterns = registries.registryOrThrow(Registries.TRIM_PATTERN).holders()
                .filter(h -> h.key().location().getNamespace().equals("minecraft")).toList();
        if (materials.isEmpty() || patterns.isEmpty()) return false;
        stack.set(DataComponents.TRIM, new ArmorTrim(
                materials.get(random.nextInt(materials.size())),
                patterns.get(random.nextInt(patterns.size()))));
        return true;
    }

    public static boolean apply(ItemStack stack, RegistryAccess registries) {
        // Cosmetic randomness must not change Apotheosis's affix/loot RNG sequence.
        return apply(stack, registries, RandomSource.create());
    }
}
