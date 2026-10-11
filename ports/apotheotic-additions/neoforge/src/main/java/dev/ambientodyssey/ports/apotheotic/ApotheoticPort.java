package dev.ambientodyssey.ports.apotheotic;

import net.minecraft.world.item.Item;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.registries.DeferredItem;
import net.neoforged.neoforge.registries.DeferredRegister;

/** Port milestone 1: register the three crafting materials used by the original rarities.
 *  This has no loot distribution, bosses, gems or rarity loading until verified.
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
    }
}
