package dev.ambientodyssey.augmentingsigils;

import dev.shadowsoffire.apotheosis.AdventureConfig;
import dev.shadowsoffire.apotheosis.Apoth;
import dev.shadowsoffire.apotheosis.loot.RarityRegistry;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.ItemStack;

/** Cost by the item's actual Apotheosis rarity data component, not its affix's name. */
public final class SigilCosts {
    private SigilCosts() {}

    public static int reroll(ItemStack stack) {
        return calculate(stack, AdventureConfig.rerollSigilCost, false);
    }

    public static int upgrade(ItemStack stack) {
        return calculate(stack, AdventureConfig.upgradeSigilCost, true);
    }

    public static int calculate(ItemStack stack, int vanillaCost, boolean upgrade) {
        if (stack.isEmpty()) return vanillaCost;
        var holder = stack.get(Apoth.Components.RARITY);
        if (holder == null || !holder.isBound()) return vanillaCost;
        var rarity = RarityRegistry.INSTANCE.getKey(holder.get());
        return fromId(rarity, vanillaCost, upgrade);
    }

    /**
     * AO port may use the original Apotheotic Additions IDs or its own namespace.
     * Never mistake a rarity with a different namespace for Ancient/Artifact/etc.
     */
    public static int fromId(ResourceLocation rarity, int vanillaCost, boolean upgrade) {
        if (rarity == null) return vanillaCost;
        String ns = rarity.getNamespace(), path = rarity.getPath();
        int reroll = switch (path) {
            case "ancient" -> "apotheosis".equals(ns) || approvedPortNamespace(ns) ? 6 : 0;
            case "artifact" -> approvedPortNamespace(ns) ? 18 : 0;
            case "heirloom" -> approvedPortNamespace(ns) ? 24 : 0;
            case "esoteric" -> approvedPortNamespace(ns) ? 32 : 0;
            default -> 0;
        };
        if (reroll <= 0) return vanillaCost;
        return upgrade ? reroll * 2 : reroll;
    }

    private static boolean approvedPortNamespace(String ns) {
        return "apotheotic_additions".equals(ns) || "ao_apotheotic_port".equals(ns);
    }
}
