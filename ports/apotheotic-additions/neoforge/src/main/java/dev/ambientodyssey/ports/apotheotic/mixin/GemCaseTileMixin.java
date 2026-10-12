package dev.ambientodyssey.ports.apotheotic.mixin;

import dev.ambientodyssey.ports.apotheotic.LegacyGem;
import dev.shadowsoffire.apotheosis.socket.gem.storage.GemCaseTile;
import net.minecraft.world.Containers;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.entity.BlockEntity;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * Backstop only. The Gem Case stores gems by native purity, which would flatten Artifact/Heirloom/Esoteric to
 * Ancient. Entry points refuse such stacks first; if one still reaches here (another mod), drop it unchanged
 * rather than void or downgrade it.
 */
@Mixin(GemCaseTile.class)
public abstract class GemCaseTileMixin {
    @Inject(method = "depositGem(Lnet/minecraft/world/item/ItemStack;)V", at = @At("HEAD"), cancellable = true)
    private void ao_apotheotic$refuseUpperTier(ItemStack stack, CallbackInfo ci) {
        if (!LegacyGem.isNonNativeUpperTier(stack)) return;
        BlockEntity self = (BlockEntity) (Object) this;
        if (self.getLevel() != null && !self.getLevel().isClientSide()) {
            var pos = self.getBlockPos();
            Containers.dropItemStack(self.getLevel(), pos.getX() + 0.5, pos.getY() + 1.0, pos.getZ() + 0.5, stack.copy());
        }
        ci.cancel();
    }
}
