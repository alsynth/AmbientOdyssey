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
    public static final DeferredItem<Item> ARTIFACT_MATERIAL =
            ITEMS.registerSimpleItem("artifact_material", new Item.Properties());
    public static final DeferredItem<Item> HEIRLOOM_MATERIAL =
            ITEMS.registerSimpleItem("heirloom_material", new Item.Properties());
    public static final DeferredItem<Item> ESOTERIC_MATERIAL =
            ITEMS.registerSimpleItem("esoteric_material", new Item.Properties());

    public ApotheoticPort(IEventBus bus) {
        ITEMS.register(bus);
        bus.addListener((BuildCreativeModeTabContentsEvent event) -> {
            if (event.getTabKey() == CreativeModeTabs.INGREDIENTS) {
                event.accept(ARTIFACT_MATERIAL.get());
                event.accept(HEIRLOOM_MATERIAL.get());
                event.accept(ESOTERIC_MATERIAL.get());
            }
        });
    }
}
