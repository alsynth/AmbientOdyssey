package dev.ambientodyssey.worldgensafety.mixin;

import net.minecraft.nbt.CompoundTag;
import net.minecraft.nbt.ListTag;
import org.spongepowered.asm.mixin.Final;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * Dungeon Crawl 2.3.17 native RandomMonster.<clinit> explicitly creates one
 * villager offer second payment as "minecraft:air" with Count=0.
 * A missing optional second payment is represented by omitting 'buyB', not an
 * invalid ItemStack; Minecraft's registry loader otherwise complains.
 *
 * Constrained to precisely ONE known-empty native trade field. Never replaces
 * legitimate positive-count items in structure NBT or any other mod.
 */
@Mixin(targets = "xiroc.dungeoncrawl.dungeon.monster.RandomMonster", remap = false)
public abstract class DungeonCrawlOptionalTradeAirMixin {
    @Shadow @Final
    private static CompoundTag VILLAGER_OFFERS;

    @Inject(method = "<clinit>", at = @At("TAIL"), remap = false)
    private static void ao$removeNativeOptionalAirPayment(CallbackInfo ci) {
        if (VILLAGER_OFFERS == null) return;
        ListTag offers = VILLAGER_OFFERS.getList("Recipes", 10);
        for (int i = 0; i < offers.size(); i++) {
            CompoundTag trade = offers.getCompound(i);
            if (!trade.contains("buyB", 10)) continue;
            CompoundTag second = trade.getCompound("buyB");
            if ("minecraft:air".equals(second.getString("id"))
                    && second.getByte("Count") == 0) {
                trade.remove("buyB");
            }
        }
    }
}
