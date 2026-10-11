package dev.ambientodyssey.worldgensafety;

import net.minecraft.server.MinecraftServer;
import net.minecraft.server.TickTask;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.MobCategory;
import net.neoforged.neoforge.common.NeoForge;
import net.neoforged.neoforge.event.entity.EntityJoinLevelEvent;
import org.slf4j.Logger;
import com.mojang.logging.LogUtils;

import java.lang.reflect.Method;

/**
 * Narrow, additive late-retry for Dungeon Difficulty 3.9.2 (1.21.1).
 *
 * Native Dungeon Difficulty runs EntityScaling.scale() at the HEAD of
 * ServerEntityManager.addEntity and calls markEvaluated(dimension) even
 * when no zone could be resolved. If a structure is still being generated,
 * its structure references/bounding boxes may not yet be available. The mob
 * will then forever be skipped by Dungeon Difficulty's "already evaluated"
 * guard -- including after a move into a now-complete dungeon.
 *
 * This compatibility shim makes at most two RETRIES, only for server-thread
 * newly added hostile mobs that are not already scaled and have not changed
 * dimension. It clears only Dungeon Difficulty's "evaluated in" marker,
 * never native attributes or its saved "dd_scaled" level. It calls the
 * original mod's own EntityScaling.scale(), retaining all native math,
 * health proportions, effect types and per-zone settings.
 *
 * Does NOT heal/raise mobs that have 2 health. That symptom needs a new
 * user log and entity-specific attribute evidence to diagnose safely.
 */
public final class DungeonDifficultyDeferredEvaluation {
    private static final Logger LOG = LogUtils.getLogger();
    private static final String CLASS = "net.dungeon_difficulty.logic.EntityDifficultyScalable";
    private static final String SCALER = "net.dungeon_difficulty.logic.EntityScaling";
    private static volatile boolean warnedReflection;

    private DungeonDifficultyDeferredEvaluation() {}

    public static void register() {
        NeoForge.EVENT_BUS.addListener(DungeonDifficultyDeferredEvaluation::onJoin);
        LOG.info("AO: enabled guarded late location-evaluation retries for Dungeon Difficulty");
    }

    private static void onJoin(EntityJoinLevelEvent event) {
        if (!(event.getLevel() instanceof ServerLevel level)
                || !(event.getEntity() instanceof Mob mob)
                || mob.getType().getCategory() != MobCategory.MONSTER) {
            return;
        }
        MinecraftServer server = level.getServer();
        if (server == null || !server.isSameThread()) {
            return; // Never touch a worldgen worker's entity state.
        }
        retryAfter(server, level, mob, 10);
    }

    private static void retryAfter(MinecraftServer server, ServerLevel level,
                                   Mob mob, int deltaTicks) {
        server.tell(new TickTask(server.getTickCount() + deltaTicks, () -> {
            if (!server.isSameThread()
                    || mob.isRemoved()
                    || !mob.isAlive()
                    || mob.level() != level
                    || !level.hasChunkAt(mob.blockPosition())) {
                return;
            }
            try {
                Class<?> iface = Class.forName(CLASS);
                if (!iface.isInstance(mob)) return;
                Method scaled = iface.getMethod("isAlreadyScaled");
                if (Boolean.TRUE.equals(scaled.invoke(mob))) return;

                // If structure lookup ran too early, undo JUST the no-zone
                // evaluation sentinel, then let the original scaler retry.
                String dimension = level.dimension().location().toString();
                Method getEvaluated = iface.getMethod("getEvaluatedDimension");
                String evaluated = (String) getEvaluated.invoke(mob);
                if (evaluated != null && !evaluated.equals(dimension)) {
                    return;
                }
                iface.getMethod("markEvaluated", String.class)
                     .invoke(mob, new Object[]{null});
                Class<?> scaler = Class.forName(SCALER);
                scaler.getMethod("scale", Entity.class, ServerLevel.class)
                      .invoke(null, mob, level);

                // Retry only once more if the first delayed evaluation still
                // cannot see the full structure location. Never reapply
                // successful attribute modifiers or persist fake scaling.
                if (deltaTicks == 10
                        && !Boolean.TRUE.equals(scaled.invoke(mob))) {
                    retryAfter(server, level, mob, 40);
                }
            } catch (ReflectiveOperationException | LinkageError ex) {
                if (!warnedReflection) {
                    warnedReflection = true;
                    LOG.warn("AO: Dungeon Difficulty native API changed; deferred "
                            + "retry disabled (not a fatal error): {}", ex.toString());
                }
            }
        }));
    }
}
