package dev.ambientodyssey.worldgensafety.mixin;

import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.monster.Zombie;
import net.neoforged.neoforge.event.entity.living.FinalizeSpawnEvent;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * Hominid 1.3.4 replaces zombies with Juggernauts/Bellmen from
 * FinalizeSpawnEvent by discarding the original zombie and calling
 * ServerLevel.addFreshEntity immediately. StructureTemplate may fire this
 * event on a worldgen worker. Prevent ONLY the unsafe off-thread conversion:
 * vanilla template zombies remain available, normal-thread Hominid behavior
 * is untouched. Verified against published Hominid source and client stack.
 */
@Mixin(targets="com.alganaut.hominid.registry.event.HominidClientEvents", remap=false)
public abstract class HominidFinalizeSpawnMixin {
    @Inject(
        method="onEntityJoinWorld(Lnet/neoforged/neoforge/event/entity/living/FinalizeSpawnEvent;)V",
        at=@At("HEAD"),
        cancellable=true,
        remap=false
    )
    private static void ao$skipUnsafeWorldgenReplacement(FinalizeSpawnEvent event, CallbackInfo ci) {
        if (event.getEntity() == null || event.getEntity().getClass() != Zombie.class) {
            return;
        }
        if (event.getEntity().level() instanceof ServerLevel level
                && level.getServer() != null
                && !level.getServer().isSameThread()) {
            ci.cancel();
        }
    }
}
