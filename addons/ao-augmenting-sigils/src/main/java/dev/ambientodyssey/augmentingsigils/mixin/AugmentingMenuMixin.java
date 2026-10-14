package dev.ambientodyssey.augmentingsigils.mixin;

import dev.ambientodyssey.augmentingsigils.SigilCosts;
import dev.shadowsoffire.apotheosis.affix.augmenting.AugmentingMenu;
import net.minecraft.world.item.ItemStack;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Redirect;

/**
 * A single source of truth for affordability and payment:
 * replacements are applied both to hasCost() and the actual server charge.
 */
@Mixin(value = AugmentingMenu.class, remap = false)
public abstract class AugmentingMenuMixin {
    @Shadow public abstract ItemStack getMainItem();

    @Redirect(method = {"hasUpgradeCost", "clickMenuButton"},
        at = @At(value = "FIELD",
           target = "Ldev/shadowsoffire/apotheosis/AdventureConfig;upgradeSigilCost:I"),
        remap = false)
    private int ao$upgradeCost() { return SigilCosts.upgrade(getMainItem()); }

    @Redirect(method = {"hasRerollCost", "clickMenuButton"},
        at = @At(value = "FIELD",
           target = "Ldev/shadowsoffire/apotheosis/AdventureConfig;rerollSigilCost:I"),
        remap = false)
    private int ao$rerollCost() { return SigilCosts.reroll(getMainItem()); }
}
