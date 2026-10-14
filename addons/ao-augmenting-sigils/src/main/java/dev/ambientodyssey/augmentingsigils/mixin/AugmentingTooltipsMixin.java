package dev.ambientodyssey.augmentingsigils.mixin;

import dev.ambientodyssey.augmentingsigils.SigilCosts;
import dev.shadowsoffire.apotheosis.affix.augmenting.AugmentingScreen;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Redirect;

/** Keep displayed tooltip prices in sync with the authority on the server. */
@Mixin(targets = "dev.shadowsoffire.apotheosis.affix.augmenting.AugmentingScreen$FatTexButton", remap = false)
public abstract class AugmentingTooltipsMixin {
    @Shadow private AugmentingScreen this$0;

    @Redirect(method = "renderToolTip",
        at = @At(value = "FIELD",
            target = "Ldev/shadowsoffire/apotheosis/AdventureConfig;rerollSigilCost:I"),
        remap = false)
    private int ao$rerollTooltip() { return SigilCosts.reroll(this$0.getMenu().getMainItem()); }

    @Redirect(method = "renderToolTip",
        at = @At(value = "FIELD",
            target = "Ldev/shadowsoffire/apotheosis/AdventureConfig;upgradeSigilCost:I"),
        remap = false)
    private int ao$upgradeTooltip() { return SigilCosts.upgrade(this$0.getMenu().getMainItem()); }
}
