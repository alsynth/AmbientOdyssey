package dev.ambientodyssey.worldgensafety.mixin;

import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.TickTask;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.monster.Zombie;
import net.neoforged.neoforge.event.entity.living.FinalizeSpawnEvent;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

import java.util.Optional;

/**
 * Replace Hominid 1.3.4's invalid FinalizeSpawnEvent flow for exact vanilla
 * zombies. The native event callback discards the original zombie and inserts
 * a replacement inside FinalizeSpawnEvent. It can lead to "marked as removed
 * already" on the main thread and illegal off-thread insertion in worldgen.
 *
 * NeoForge 1.21.1 FinalizeSpawnEvent#setSpawnCancelled(true) is the official
 * way to prevent the original mob from being added; simply cancelling this
 * event would only skip initialization and does not prevent the actual spawn.
 *
 * Preserve original Hominid encounter chance: 10% Juggernaut, otherwise 10%
 * Bellman. Other mobs (including illager avoidance logic) are unchanged.
 * Only convert on main server thread; async worldgen retains vanilla zombies.
 *
 * Even on main server thread, defer insertion until a later server TickTask
 * rather than adding an entity synchronously inside a spawn event.
 *
 * This remains a private RUNTIME-UNTESTED experiment.
 */
@Mixin(targets = "com.alganaut.hominid.registry.event.HominidClientEvents", remap = false)
public abstract class HominidFinalizeSpawnMixin {
    private static final ResourceLocation JUGGERNAUT =
            ResourceLocation.fromNamespaceAndPath("hominid", "juggernaut");
    private static final ResourceLocation BELLMAN =
            ResourceLocation.fromNamespaceAndPath("hominid", "bellman");

    @Inject(
        method = "onEntityJoinWorld(Lnet/neoforged/neoforge/event/entity/living/FinalizeSpawnEvent;)V",
        at = @At("HEAD"),
        cancellable = true,
        remap = false
    )
    private static void ao$deferSafeHominidReplacement(FinalizeSpawnEvent event, CallbackInfo ci) {
        if (event.getEntity() == null || event.getEntity().getClass() != Zombie.class) {
            return; // native Hominid other-entity handling remains untouched
        }

        // Never run the native zombie-discard path, even on the server thread.
        ci.cancel();

        if (!(event.getEntity().level() instanceof ServerLevel level)
                || level.getServer() == null || !level.getServer().isSameThread()
                || event.isSpawnCancelled()) {
            return; // async/worldgen vanilla zombie remains unmodified
        }

        ResourceLocation target;
        if (level.getRandom().nextFloat() < 0.1F) {
            target = JUGGERNAUT;
        } else if (level.getRandom().nextFloat() < 0.1F) {
            target = BELLMAN;
        } else {
            return; // normally spawn the original zombie
        }

        Optional<EntityType<?>> replacementType = BuiltInRegistries.ENTITY_TYPE.getOptional(target);
        if (replacementType.isEmpty()) {
            return; // fail-open to original zombie if pinned Hominid registry changes
        }

        Entity original = event.getEntity();
        final double x = original.getX(), y = original.getY(), z = original.getZ();
        final float yaw = original.getYRot(), pitch = original.getXRot();
        final BlockPos originalPos = original.blockPosition();
        final EntityType<?> type = replacementType.get();
        final MinecraftServer server = level.getServer();

        // Only after the replacement type is verified may the vanilla spawn be suppressed.
        event.setSpawnCancelled(true);
        server.tell(new TickTask(server.getTickCount() + 1, () -> {
            // Async structure placement may still be constructing this chunk.
            // Avoid any synchronous load or worldgen recursion when it isn't ready.
            if (!level.hasChunkAt(originalPos)) {
                return;
            }
            Entity replacement = type.create(level);
            if (replacement == null) {
                return;
            }
            replacement.moveTo(x, y, z, yaw, pitch);
            level.addFreshEntity(replacement);
        }));
    }
}
