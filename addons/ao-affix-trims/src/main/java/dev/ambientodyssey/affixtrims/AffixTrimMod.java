package dev.ambientodyssey.affixtrims;

import com.mojang.serialization.MapCodec;
import java.util.function.Supplier;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.common.NeoForgeMod;
import net.neoforged.neoforge.registries.DeferredRegister;
import net.neoforged.neoforge.registries.NeoForgeRegistries;
import net.neoforged.neoforge.common.loot.IGlobalLootModifier;

@Mod(AffixTrimMod.MODID)
public final class AffixTrimMod {
    public static final String MODID = "ao_affix_trims";
    public static final DeferredRegister<MapCodec<? extends IGlobalLootModifier>> MODIFIERS =
            DeferredRegister.create(NeoForgeRegistries.Keys.GLOBAL_LOOT_MODIFIER_SERIALIZERS, MODID);
    public static final Supplier<MapCodec<RandomAffixArmorTrimModifier>> RANDOM_ARMOR_TRIM =
            MODIFIERS.register("random_affix_armor_trim", () -> RandomAffixArmorTrimModifier.CODEC);

    public AffixTrimMod(IEventBus bus) {
        MODIFIERS.register(bus);
    }
}
