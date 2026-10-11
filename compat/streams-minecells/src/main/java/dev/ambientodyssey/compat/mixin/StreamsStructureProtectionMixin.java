package dev.ambientodyssey.compat.mixin;

import net.minecraft.world.level.levelgen.structure.Structure;
import net.minecraft.world.level.levelgen.structure.StructureStart;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/**
 * Streams Reflowing's StructureMixin can turn valid structures into
 * StructureStart.INVALID_START to protect rivers. Mine Cells' grid structures
 * are mandatory gameplay geometry; they must never be vetoed by Streams.
 *
 * Match only Mine Cells' own structure implementations. Never change Overworld
 * or other modded structures. Targets verified from 2.14.4 NeoForge bytecode.
 */
@Mixin(targets = "dev.streamsreflowing.worldgen.StreamsWorldgen", remap = false)
public abstract class StreamsStructureProtectionMixin {
    private static boolean ao$isMineCellsStructure(Structure structure) {
        return structure != null
            && structure.getClass().getName().startsWith("com.github.mim1q.minecells.");
    }

    @Inject(
        method = "structureAlwaysGenerates(Lnet/minecraft/world/level/levelgen/structure/Structure;)Z",
        at = @At("HEAD"), cancellable = true, remap = false
    )
    private static void ao$keepMineCellsStructures(Structure structure, CallbackInfoReturnable<Boolean> callback) {
        if (ao$isMineCellsStructure(structure)) {
            callback.setReturnValue(true);
        }
    }

    @Inject(
        method = "structureFootprintOnStream(Lnet/minecraft/world/level/levelgen/structure/StructureStart;)Z",
        at = @At("HEAD"), cancellable = true, remap = false
    )
    private static void ao$avoidMineCellsFootprintVeto(StructureStart start, CallbackInfoReturnable<Boolean> callback) {
        if (start != null && ao$isMineCellsStructure(start.getStructure())) {
            callback.setReturnValue(false);
        }
    }

    @Inject(
        method = "generationPointOnWater(IIILjava/lang/String;)Z",
        at = @At("HEAD"), cancellable = true, remap = false
    )
    private static void ao$avoidMineCellsStartVeto(int x, int y, int z, String structureId, CallbackInfoReturnable<Boolean> callback) {
        if (structureId != null && structureId.startsWith("minecells:")) {
            callback.setReturnValue(false);
        }
    }
}
