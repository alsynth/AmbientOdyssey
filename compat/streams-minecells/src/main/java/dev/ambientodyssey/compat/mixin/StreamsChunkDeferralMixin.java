package dev.ambientodyssey.compat.mixin;

import java.util.concurrent.CompletableFuture;
import net.minecraft.server.level.GenerationChunkHolder;
import net.minecraft.util.StaticCache2D;
import net.minecraft.world.level.chunk.ChunkAccess;
import net.minecraft.world.level.chunk.status.ChunkStep;
import net.minecraft.world.level.chunk.status.WorldGenContext;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/**
 * Keep the normal vanilla chunk pipeline for Mine Cells' specially generated
 * dimensions. Streams' ChunkStepMixin calls this method and only intercepts
 * ChunkStep.apply if defer() returns a non-null future. Null means: proceed
 * with the original Minecraft chunk step.
 *
 * Narrowly matched to Streams Reflowing NeoForge 2.14.4.
 */
@Mixin(targets = "dev.streamsreflowing.worldgen.ChunkStepDefer", remap = false)
public abstract class StreamsChunkDeferralMixin {
    @Inject(
        method = "defer(Lnet/minecraft/world/level/chunk/status/ChunkStep;Lnet/minecraft/world/level/chunk/status/WorldGenContext;Lnet/minecraft/util/StaticCache2D;Lnet/minecraft/world/level/chunk/ChunkAccess;)Ljava/util/concurrent/CompletableFuture;",
        at = @At("HEAD"),
        cancellable = true,
        remap = false
    )
    private static void ao$doNotDeferMineCells(
        ChunkStep step,
        WorldGenContext context,
        StaticCache2D<GenerationChunkHolder> cache,
        ChunkAccess chunk,
        CallbackInfoReturnable<CompletableFuture<ChunkAccess>> callback
    ) {
        if (context != null
                && context.level() != null
                && "minecells".equals(context.level().dimension().location().getNamespace())) {
            callback.setReturnValue(null);
        }
    }
}
