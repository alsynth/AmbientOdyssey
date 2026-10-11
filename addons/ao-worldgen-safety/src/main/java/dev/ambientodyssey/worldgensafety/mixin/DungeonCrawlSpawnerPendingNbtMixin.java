package dev.ambientodyssey.worldgensafety.mixin;

import net.minecraft.core.BlockPos;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.server.level.WorldGenRegion;
import net.minecraft.world.level.LevelAccessor;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.entity.SpawnerBlockEntity;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Unique;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.Redirect;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.block.state.BlockState;
import xiroc.dungeoncrawl.theme.Theme;
import xiroc.dungeoncrawl.theme.SecondaryTheme;

/**
 * Exact Dungeon Crawl 2.3.17 spawner-worldgen repair.
 *
 * Dungeon Crawl places Blocks.SPAWNER and immediately calls LevelAccessor
 * .getBlockEntity(pos). In WorldGenRegion the block entity may still be a
 * DUMMY pending NBT rather than a live SpawnerBlockEntity. Returning a temporary
 * spawner to Dungeon Crawl preserves the author's original random monster,
 * inventory, potion, weighted spawn, player range and delay calculations.
 * At return, serialize the fully configured temporary block entity into
 * ChunkAccess's native pending block-entity NBT map. Chunk promotion then loads
 * the authoritative NBT; never schedule setBlock/addFreshEntity asynchronously.
 *
 * No behavior change for live LevelAccessor with an existing block entity.
 * Runtime testing must prove spawner mobs after save/rejoin in new chunks.
 */
@Mixin(targets = "xiroc.dungeoncrawl.dungeon.block.Spawner", remap = false)
public abstract class DungeonCrawlSpawnerPendingNbtMixin {
    @Unique
    private static final ThreadLocal<SpawnerBlockEntity> AO_PENDING_SPAWNER = new ThreadLocal<>();

    @Inject(method = "place", at = @At("HEAD"), remap = false)
    private void ao$clearPendingAtEntry(LevelAccessor world, BlockState state,
            BlockPos pos, RandomSource random, Theme theme,
            SecondaryTheme secondaryTheme, int stage, CallbackInfo ci) {
        AO_PENDING_SPAWNER.remove();
    }

    @Redirect(method = "place",
            at = @At(value = "INVOKE",
                    target = "Lnet/minecraft/world/level/LevelAccessor;getBlockEntity(Lnet/minecraft/core/BlockPos;)Lnet/minecraft/world/level/block/entity/BlockEntity;"),
            remap = false)
    private BlockEntity ao$getOrCreateWorldgenSpawner(LevelAccessor world, BlockPos pos) {
        BlockEntity existing = world.getBlockEntity(pos);
        if (existing != null) return existing;
        // Do not fabricate a spawner unless worldgen accepted the block placement.
        if (!(world instanceof WorldGenRegion) || !world.getBlockState(pos).is(Blocks.SPAWNER)) {
            return null;
        }
        SpawnerBlockEntity pending = new SpawnerBlockEntity(pos, Blocks.SPAWNER.defaultBlockState());
        AO_PENDING_SPAWNER.set(pending);
        return pending;
    }

    @Inject(method = "place", at = @At("RETURN"), remap = false)
    private void ao$storeConfiguredWorldgenSpawner(LevelAccessor world, BlockState state,
            BlockPos pos, RandomSource random, Theme theme,
            SecondaryTheme secondaryTheme, int stage, CallbackInfo ci) {
        SpawnerBlockEntity configured = AO_PENDING_SPAWNER.get();
        AO_PENDING_SPAWNER.remove();
        if (configured == null || !(world instanceof WorldGenRegion region)
                || !world.getBlockState(pos).is(Blocks.SPAWNER)) {
            return;
        }
        // Existing WorldGenRegion pending DUMMY NBT is replaced, not a second BE
        // spawned. ChunkAccess persists this exact BlockEntity's id, x/y/z and
        // BaseSpawner SpawnData/SpawnPotentials through the normal chunk pipeline.
        CompoundTag nbt = configured.saveWithFullMetadata(world.registryAccess());
        region.getChunk(pos.getX() >> 4, pos.getZ() >> 4).setBlockEntityNbt(nbt);
    }
}
