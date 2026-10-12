package dev.ambientodyssey.ports.apotheotic.mixin;

import dev.ambientodyssey.ports.apotheotic.LegacyGem;
import dev.shadowsoffire.apotheosis.util.GemIngredient;
import net.minecraft.world.item.ItemStack;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/** A native PERFECT-gem ingredient means exactly Ancient; it must not consume Artifact/Heirloom/Esoteric gems. */
@Mixin(GemIngredient.class)
public abstract class GemIngredientMixin {
    @Inject(method = "test(Lnet/minecraft/world/item/ItemStack;)Z", at = @At("HEAD"), cancellable = true)
    private void ao_apotheotic$exactTier(ItemStack stack, CallbackInfoReturnable<Boolean> cir) {
        if (LegacyGem.isNonNativeUpperTier(stack)) cir.setReturnValue(false);
    }
}
