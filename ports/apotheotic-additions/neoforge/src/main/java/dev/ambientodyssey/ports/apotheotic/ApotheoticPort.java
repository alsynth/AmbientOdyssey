package dev.ambientodyssey.ports.apotheotic;

import net.minecraft.world.item.Item;
import net.minecraft.world.item.CreativeModeTabs;
import net.neoforged.neoforge.event.BuildCreativeModeTabContentsEvent;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.registries.DeferredItem;
import net.neoforged.neoforge.registries.DeferredRegister;

/** Three native rarity materials and data-driven tiers, with natural rolls disabled
 *  until their affix/gem/loot subsystems are ported and verified.
 */
@Mod(ApotheoticPort.ID)
public final class ApotheoticPort {
    public static final String ID = "ao_apotheotic_port";
    public static final DeferredRegister.Items ITEMS = DeferredRegister.createItems(ID);
    public static final DeferredRegister<net.minecraft.core.component.DataComponentType<?>> COMPONENTS =
            DeferredRegister.create(net.minecraft.core.registries.Registries.DATA_COMPONENT_TYPE, ID);
    public static final java.util.function.Supplier<net.minecraft.core.component.DataComponentType<Integer>> LEGACY_GEM_TIER =
            COMPONENTS.register("legacy_gem_tier", () -> net.minecraft.core.component.DataComponentType.<Integer>builder()
                    .persistent(com.mojang.serialization.Codec.intRange(0, 8))
                    .networkSynchronized(net.minecraft.network.codec.ByteBufCodecs.VAR_INT).build());
    public static final DeferredItem<Item> ARTIFACT_MATERIAL =
            ITEMS.registerSimpleItem("artifact_material", new Item.Properties());
    public static final DeferredItem<Item> HEIRLOOM_MATERIAL =
            ITEMS.registerSimpleItem("heirloom_material", new Item.Properties());
    public static final DeferredItem<Item> ESOTERIC_MATERIAL =
            ITEMS.registerSimpleItem("esoteric_material", new Item.Properties());

    public ApotheoticPort(IEventBus bus) {
        ITEMS.register(bus);
        COMPONENTS.register(bus);
        dev.shadowsoffire.apotheosis.socket.gem.bonus.GemBonus.CODEC.register(
                net.minecraft.resources.ResourceLocation.fromNamespaceAndPath(ID, "legacy_attribute"), LegacyAttributeBonus.CODEC);
        bus.addListener((BuildCreativeModeTabContentsEvent event) -> {
            if (event.getTabKey() == CreativeModeTabs.INGREDIENTS) {
                event.accept(ARTIFACT_MATERIAL.get());
                event.accept(HEIRLOOM_MATERIAL.get());
                event.accept(ESOTERIC_MATERIAL.get());
            }
        });
    }
}
