package dev.ambientodyssey.worldgensafety.mixin;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.MinecraftServer;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.phys.Vec3;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/** Exact pinned Tan Huge Trees 1.8.0 beta: only adjust asynchronous
 * worldgen marker spawns, not tree construction or natural mob spawning.
 */
@Mixin(targets="tannyjung.tanshugetrees_core.game.GameUtils$Mob", remap=false)
public abstract class TansWorldgenMarkerSchedulingMixin {
    @Shadow(remap=false)
    public static Entity summon(ServerLevel level, Vec3 at, String entityId,
                                String name, String tags, String customData) {
        throw new AssertionError("Mixin shadow not transformed");
    }

    @Inject(
        method="summonWorldGen(Lnet/minecraft/server/level/ServerLevel;Lnet/minecraft/world/phys/Vec3;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V",
        at=@At("HEAD"),
        cancellable=true,
        remap=false
    )
    private static void ao$enqueueMarkerToServerThread(
            ServerLevel level, Vec3 at, String entityId, String name,
            String tags, String customData, CallbackInfo ci) {
        MinecraftServer server = level.getServer();
        if (server != null && !server.isSameThread()) {
            server.tell(() -> summon(level, at, entityId, name, tags, customData));
            ci.cancel();
        }
    }
}
