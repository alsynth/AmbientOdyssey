package dev.ambientodyssey.affixtrims;

import com.mojang.serialization.MapCodec;
import java.util.function.Supplier;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.registries.DeferredRegister;
import net.neoforged.neoforge.registries.NeoForgeRegistries;
import net.neoforged.neoforge.common.loot.IGlobalLootModifier;
import net.neoforged.neoforge.common.NeoForge;
import net.neoforged.neoforge.event.entity.EntityJoinLevelEvent;
import net.neoforged.neoforge.event.entity.player.PlayerContainerEvent;
import net.minecraft.world.entity.item.ItemEntity;

@Mod(AffixTrimMod.MODID)
public final class AffixTrimMod {
    public static final String MODID = "ao_affix_trims";
    public static final DeferredRegister<MapCodec<? extends IGlobalLootModifier>> MODIFIERS =
            DeferredRegister.create(NeoForgeRegistries.Keys.GLOBAL_LOOT_MODIFIER_SERIALIZERS, MODID);
    public static final Supplier<MapCodec<RandomAffixArmorTrimModifier>> RANDOM_ARMOR_TRIM =
            MODIFIERS.register("random_affix_armor_trim", () -> RandomAffixArmorTrimModifier.CODEC);

    public AffixTrimMod(IEventBus bus) {
        MODIFIERS.register(bus);
        NeoForge.EVENT_BUS.addListener(AffixTrimMod::onItemSpawn);
        NeoForge.EVENT_BUS.addListener(AffixTrimMod::onContainerOpen);
    }

    private static void onItemSpawn(EntityJoinLevelEvent event) {
        if (!event.getLevel().isClientSide && event.getEntity() instanceof ItemEntity item) {
            // Also catches old affixed drops and additions after global loot modifiers.
            var stack = item.getItem().copy();
            if (AffixTrims.apply(stack, event.getLevel().registryAccess())) item.setItem(stack);
        }
    }

    private static void onContainerOpen(PlayerContainerEvent.Open event) {
        if (event.getEntity().level().isClientSide) return;
        // One bounded pass on open, no per-tick inventory/world scans. Handles old chests.
        for (var slot : event.getContainer().slots) {
            if (AffixTrims.apply(slot.getItem(), event.getEntity().registryAccess())) slot.setChanged();
        }
        event.getContainer().broadcastChanges();
    }
}
