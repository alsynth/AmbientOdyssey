package dev.ambientodyssey.starterchest;

import java.util.function.Supplier;
import com.mojang.serialization.MapCodec;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.registries.DeferredRegister;
import net.neoforged.neoforge.registries.NeoForgeRegistries;
import net.neoforged.neoforge.common.loot.IGlobalLootModifier;

@Mod(AOStarterChestMod.MOD_ID)
public final class AOStarterChestMod {
    public static final String MOD_ID = "ao_starter_chest";
    public static final DeferredRegister<MapCodec<? extends IGlobalLootModifier>> MODIFIERS =
            DeferredRegister.create(NeoForgeRegistries.Keys.GLOBAL_LOOT_MODIFIER_SERIALIZERS, MOD_ID);
    public static final Supplier<MapCodec<StarterAffixModifier>> STARTER_AFFIX =
            MODIFIERS.register("starter_affix", () -> StarterAffixModifier.CODEC);

    public AOStarterChestMod(IEventBus bus) {
        MODIFIERS.register(bus);
    }
}
