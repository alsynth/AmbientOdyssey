package dev.ambientodyssey.affixtrims.mixin;

import dev.ambientodyssey.affixtrims.AffixTrims;
import dev.shadowsoffire.apotheosis.loot.LootCategory;
import dev.shadowsoffire.apotheosis.loot.LootRarity;
import dev.shadowsoffire.apotheosis.tiers.GenContext;
import net.minecraft.world.item.ItemStack;
import net.neoforged.neoforge.server.ServerLifecycleHooks;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/** Exact Apotheosis 8.9.0 common factory: chest conversion, elite gear and rewards. */
@Mixin(targets = "dev.shadowsoffire.apotheosis.loot.LootController", remap = false)
public abstract class AffixLootCreationMixin {
    @Inject(method = "createLootItem(Lnet/minecraft/world/item/ItemStack;Ldev/shadowsoffire/apotheosis/loot/LootCategory;Ldev/shadowsoffire/apotheosis/loot/LootRarity;Ldev/shadowsoffire/apotheosis/tiers/GenContext;)Lnet/minecraft/world/item/ItemStack;",
            at = @At("RETURN"), remap = false)
    private static void ao$trimFinishedLoot(ItemStack stack, LootCategory category,
            LootRarity rarity, GenContext context, CallbackInfoReturnable<ItemStack> result) {
        var server = ServerLifecycleHooks.getCurrentServer();
        if (server != null) AffixTrims.apply(result.getReturnValue(), server.registryAccess());
    }
}
