package dev.ambientodyssey.ports.apotheotic.mixin;

import dev.ambientodyssey.ports.apotheotic.LegacyGem;
import net.minecraft.world.item.ItemStack;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/** Hoppers/pipes: report non-native upper-tier gems as not inserted, exactly as stock does for invalid stacks. */
@Mixin(targets = "dev.shadowsoffire.apotheosis.socket.gem.storage.GemCaseTile$GemCaseItemHandler")
public abstract class GemCaseItemHandlerMixin {
    @Inject(method = "insertItem(ILnet/minecraft/world/item/ItemStack;Z)Lnet/minecraft/world/item/ItemStack;", at = @At("HEAD"), cancellable = true)
    private void ao_apotheotic$refuseUpperTier(int slot, ItemStack stack, boolean simulate, CallbackInfoReturnable<ItemStack> cir) {
        if (LegacyGem.isNonNativeUpperTier(stack)) cir.setReturnValue(stack);
    }
}
