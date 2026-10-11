package dev.ambientodyssey.worldgensafety.mixin;

import net.minecraft.server.MinecraftServer;
import net.minecraft.server.TickTask;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Redirect;

/**
 * Native Tan Huge Trees 1.8.0 beta:
 * GameUtils$Mob.summonWorldGen invokes MinecraftServer.execute(Runnable)
 * for a marker-entity spawn lambda. The original execute occasionally runs
 * it inline on Worker-Main during worldgen (actual Cupboard stack trace).
 *
 * Redirect EXACTLY that call site. On offthread workers, enqueue the author's
 * *original* Runnable as a later TickTask; on server thread, behave as before.
 * Unlike a shadowed summon override, this preserves the entire original
 * entity-creation lambda and its custom marker data without reimplementing it.
 */
@Mixin(targets="tannyjung.tanshugetrees_core.game.GameUtils$Mob", remap=false)
public abstract class TansWorldgenMarkerSchedulingMixin {
    @Redirect(
        method="summonWorldGen(Lnet/minecraft/server/level/ServerLevel;Lnet/minecraft/world/phys/Vec3;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V",
        at=@At(
            value="INVOKE",
            target="Lnet/minecraft/server/MinecraftServer;execute(Ljava/lang/Runnable;)V",
            remap=false
        ),
        remap=false
    )
    private static void ao$enqueueWorldgenMarker(MinecraftServer server, Runnable nativeSummon) {
        if (server.isSameThread()) {
            server.execute(nativeSummon);
        } else {
            server.tell(new TickTask(server.getTickCount() + 1, nativeSummon));
        }
    }
}
