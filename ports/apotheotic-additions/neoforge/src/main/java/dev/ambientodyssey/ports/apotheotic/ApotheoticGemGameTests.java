package dev.ambientodyssey.ports.apotheotic;

import com.google.gson.JsonParser;
import dev.shadowsoffire.apotheosis.socket.SocketHelper;
import dev.shadowsoffire.apotheosis.socket.gem.GemRegistry;
import dev.shadowsoffire.apotheosis.socket.gem.UnsocketedGem;
import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;

@GameTestHolder(ApotheoticPort.ID)
@PrefixGameTestTemplate(false)
public final class ApotheoticGemGameTests {
    @GameTest(template = "empty")
    public static void allFiveGemsPreserveEveryOriginalTierAndSerialization(GameTestHelper helper) {
        var input = ApotheoticGemGameTests.class.getResourceAsStream("/assets/ao_apotheotic_port/core-gem-port-manifest.json");
        var rows = JsonParser.parseReader(new InputStreamReader(input, StandardCharsets.UTF_8)).getAsJsonObject().getAsJsonArray("gems");
        int count = 0;
        for (var entry : rows) {
            var row = entry.getAsJsonObject();
            if (!row.get("status").getAsString().equals("ported_attribute_gem")) continue;
            var holder = GemRegistry.INSTANCE.holder(ResourceLocation.parse(row.get("ported_id").getAsString()));
            helper.assertTrue(holder.isBound(), "Native gem codec failed to bind");
            var gem = holder.get();
            var values = row.getAsJsonObject("original").getAsJsonArray("bonuses").get(0).getAsJsonObject().getAsJsonObject("values");
            var bonus = (LegacyAttributeBonus) gem.getBonuses().get(0);
            for (var value : values.entrySet()) {
                String key = value.getKey().substring(value.getKey().lastIndexOf(':') + 1);
                int tier = java.util.List.of(LegacyGem.TIERS).indexOf(key);
                var stack = LegacyGem.toLegacyStack(gem, tier);
                var restored = ItemStack.parse(helper.getLevel().registryAccess(), stack.save(helper.getLevel().registryAccess())).orElseThrow();
                if (tier >= LegacyGem.FIRST_COMPONENT_TIER)
                    helper.assertTrue(restored.get(ApotheoticPort.LEGACY_GEM_TIER.get()) == tier, "Lost exact legacy tier in item serialization");
                else
                    helper.assertFalse(restored.has(ApotheoticPort.LEGACY_GEM_TIER.get()), "Lower tiers must rely on native purity only");
                var buffer = new net.minecraft.network.RegistryFriendlyByteBuf(io.netty.buffer.Unpooled.buffer(), helper.getLevel().registryAccess());
                try {
                    ApotheoticPort.LEGACY_GEM_TIER.get().streamCodec().encode(buffer, tier);
                    helper.assertTrue(ApotheoticPort.LEGACY_GEM_TIER.get().streamCodec().decode(buffer) == tier,
                            "Network codec lost exact legacy gem tier");
                } finally { buffer.release(); }
                double amount = bonus.createModifier(UnsocketedGem.of(restored)).amount();
                helper.assertTrue(Math.abs(amount - value.getValue().getAsDouble()) < 0.000001, "Original gem tier value changed");
            }
            count++;
        }
        helper.assertTrue(count == 5, "Gem batch count changed");
        helper.succeed();
    }

    @GameTest(template = "empty", timeoutTicks = 80)
    public static void esotericGemSocketsAndChangesRealEquippedHealth(GameTestHelper helper) {
        var gem = GemRegistry.INSTANCE.holder(ResourceLocation.fromNamespaceAndPath(ApotheoticPort.ID, "modded/hearty")).get();
        var chest = new ItemStack(Items.DIAMOND_CHESTPLATE);
        SocketHelper.setSockets(chest, 1);
        var socketed = SocketHelper.socketGemInItem(chest, LegacyGem.toLegacyStack(gem, 8));
        helper.assertFalse(socketed.isEmpty(), "Native socketing rejected Esoteric gem");
        var restored = ItemStack.parse(helper.getLevel().registryAccess(), socketed.save(helper.getLevel().registryAccess())).orElseThrow();
        var inst = SocketHelper.getGems(restored).get(0);
        helper.assertTrue(inst.isValid() && inst.gemStack().get(ApotheoticPort.LEGACY_GEM_TIER.get()) == 8, "Socket serialization lost Esoteric tier");
        var unique = GemRegistry.INSTANCE.holder(ResourceLocation.fromNamespaceAndPath(ApotheoticPort.ID, "crafted/warden")).get();
        var twoSockets = new ItemStack(Items.DIAMOND_CHESTPLATE);
        SocketHelper.setSockets(twoSockets, 2);
        var first = SocketHelper.socketGemInItem(twoSockets, LegacyGem.toLegacyStack(unique, 6));
        helper.assertFalse(first.isEmpty(), "Native socketing rejected first unique gem");
        helper.assertTrue(SocketHelper.socketGemInItem(first, LegacyGem.toLegacyStack(unique, 8)).isEmpty(),
                "Distinct legacy tiers bypassed native unique gem restriction");
        var golem = helper.spawn(EntityType.IRON_GOLEM, new BlockPos(2, 1, 2));
        double base = golem.getAttributeBaseValue(Attributes.MAX_HEALTH);
        golem.setItemSlot(EquipmentSlot.CHEST, restored);
        helper.runAfterDelay(5, () -> {
            helper.assertTrue(Math.abs(golem.getAttributeValue(Attributes.MAX_HEALTH) - base - 5) < 0.0001,
                    "Esoteric health bonus flattened to Ancient/Perfect value");
            golem.discard();
            helper.succeed();
        });
    }

    /** Exercise tier resolution through actual native item views and recipes. */
    @GameTest(template = "empty")
    public static void tierResolutionFailsClosedAndNeverEscalates(GameTestHelper helper) {
        var gem = GemRegistry.INSTANCE.holder(ResourceLocation.fromNamespaceAndPath(ApotheoticPort.ID, "modded/hearty")).get();
        var bonus = (LegacyAttributeBonus) gem.getBonuses().get(0);
        // Component on a non-PERFECT stack is ignored: purity is the ceiling.
        var flawless = gem.toStack(dev.shadowsoffire.apotheosis.socket.gem.Purity.FLAWLESS);
        flawless.set(ApotheoticPort.LEGACY_GEM_TIER.get(), 8);
        var r = LegacyGem.resolveTier(flawless, dev.shadowsoffire.apotheosis.socket.gem.Purity.FLAWLESS, bonus::supportsTier);
        helper.assertTrue(r.isPresent() && r.getAsInt() == 4, "Component changed a supported FLAWLESS tier");
        helper.assertTrue(Math.abs(bonus.createModifier(UnsocketedGem.of(flawless)).amount() - 2.5) < 0.000001,
                "Component escalated actual FLAWLESS modifier");
        // Stale lower component on PERFECT (as after a stock purity upgrade) is ignored.
        var perfect = gem.toStack(dev.shadowsoffire.apotheosis.socket.gem.Purity.PERFECT);
        perfect.set(ApotheoticPort.LEGACY_GEM_TIER.get(), 4);
        var p = LegacyGem.resolveTier(perfect, dev.shadowsoffire.apotheosis.socket.gem.Purity.PERFECT, t -> t == 5 || t == 8);
        helper.assertTrue(p.isPresent() && p.getAsInt() == 5, "Stale lower component not ignored");
        // Unsupported exact upper tier resolves empty and createModifier yields a zero modifier, no exception.
        var unsupported = gem.toStack(dev.shadowsoffire.apotheosis.socket.gem.Purity.PERFECT);
        unsupported.set(ApotheoticPort.LEGACY_GEM_TIER.get(), 7);
        helper.assertTrue(LegacyGem.resolveTier(unsupported, dev.shadowsoffire.apotheosis.socket.gem.Purity.PERFECT, t -> t == 5 || t == 8).isEmpty(), "Unsupported tier resolved");
        var restrictedBonus = new LegacyAttributeBonus(bonus.getGemClass(), Attributes.MAX_HEALTH,
                net.minecraft.world.entity.ai.attributes.AttributeModifier.Operation.ADD_VALUE,
                java.util.Map.of("ancient", 3.0, "esoteric", 5.0));
        helper.assertTrue(restrictedBonus.createModifier(UnsocketedGem.of(unsupported)).amount() == 0.0,
                "Unsupported exact tier must produce zero rather than a fallback or exception");
        // A native view clamps this upper-only gem up to PERFECT; raw stored purity still wins.
        var crafted = GemRegistry.INSTANCE.holder(ResourceLocation.fromNamespaceAndPath(ApotheoticPort.ID, "crafted/warden")).get();
        var malformed = LegacyGem.toLegacyStack(crafted, 8);
        dev.shadowsoffire.apotheosis.socket.gem.GemItem.setPurity(malformed, dev.shadowsoffire.apotheosis.socket.gem.Purity.FLAWLESS);
        var craftedBonus = (LegacyAttributeBonus) crafted.getBonuses().get(0);
        helper.assertTrue(craftedBonus.createModifier(UnsocketedGem.of(malformed)).amount() == 0.0,
                "Native minimum-purity clamp escalated malformed upper-only gem");
        var lower = LegacyGem.toLegacyStack(gem, 4);
        var inventory = new net.neoforged.neoforge.items.ItemStackHandler(4);
        inventory.setStackInSlot(0, lower);
        var input = new dev.shadowsoffire.apotheosis.socket.gem.cutting.GemCuttingRecipe.CuttingRecipeInput(inventory);
        var upgrade = new dev.shadowsoffire.apotheosis.socket.gem.cutting.PurityUpgradeRecipe(
                dev.shadowsoffire.apotheosis.socket.gem.Purity.FLAWLESS, java.util.List.of(), java.util.List.of());
        helper.assertTrue(upgrade.isValidBaseItem(input, lower), "Native upgrade rejects valid lower-tier base");
        var upgraded = upgrade.assemble(input, helper.getLevel().registryAccess());
        helper.assertFalse(upgraded.has(ApotheoticPort.LEGACY_GEM_TIER.get()) ||
                upgraded.has(net.minecraft.core.component.DataComponents.CUSTOM_NAME), "Stock upgrade retained a stale tier/name");
        helper.assertTrue(Math.abs(bonus.createModifier(UnsocketedGem.of(upgraded)).amount() - 3.0) < 0.000001,
                "Stock FLAWLESS-to-PERFECT upgrade retained Mythic instead of Ancient value");
        helper.assertFalse(upgrade.isValidBaseItem(input, LegacyGem.toLegacyStack(gem, 8)),
                "Stock cutting accepts an upper-tier gem as upgrade base");
        helper.succeed();
    }

    /** Characterization of stock behavior the port must not rely on: UnsocketedGem.equals ignores the tier component. */
    @GameTest(template = "empty")
    public static void stockUnsocketedEqualityIgnoresUpperTierComponent(GameTestHelper helper) {
        var gem = GemRegistry.INSTANCE.holder(ResourceLocation.fromNamespaceAndPath(ApotheoticPort.ID, "modded/hearty")).get();
        var a = LegacyGem.toLegacyStack(gem, 6);
        var b = LegacyGem.toLegacyStack(gem, 8);
        helper.assertTrue(UnsocketedGem.of(a).equals(UnsocketedGem.of(b)), "Stock equality now distinguishes tiers: revisit cutting/ingredient guards");
        helper.assertFalse(ItemStack.isSameItemSameComponents(a, b), "Distinct tiers must not stack");
        helper.succeed();
    }

    /** Characterizes unresolved data-loss/ingredient hazards; passing does not make them safe. */
    @GameTest(template = "empty")
    public static void stockGemCaseAndPerfectIngredientLoseUpperTierIdentity(GameTestHelper helper) {
        var holder = GemRegistry.INSTANCE.holder(ResourceLocation.fromNamespaceAndPath(ApotheoticPort.ID, "modded/hearty"));
        var esoteric = LegacyGem.toLegacyStack(holder.get(), 8);
        var ingredient = new dev.shadowsoffire.apotheosis.util.GemIngredient(dev.shadowsoffire.apotheosis.socket.gem.Purity.PERFECT);
        helper.assertTrue(ingredient.test(esoteric), "Perfect ingredient behavior changed; review upper-tier recipe guard");
        var pos = new BlockPos(1, 1, 1);
        helper.setBlock(pos, dev.shadowsoffire.apotheosis.Apoth.Blocks.GEM_CASE.value().defaultBlockState());
        var blockEntity = helper.getLevel().getBlockEntity(helper.absolutePos(pos));
        helper.assertTrue(blockEntity instanceof dev.shadowsoffire.apotheosis.socket.gem.storage.GemCaseTile,
                "Native Gem Case fixture did not initialize");
        var gemCase = (dev.shadowsoffire.apotheosis.socket.gem.storage.GemCaseTile) blockEntity;
        gemCase.depositGem(esoteric);
        var extracted = gemCase.extractGem(holder, dev.shadowsoffire.apotheosis.socket.gem.Purity.PERFECT, 1);
        helper.assertFalse(extracted.isEmpty(), "Gem Case did not return stored gem");
        helper.assertFalse(extracted.has(ApotheoticPort.LEGACY_GEM_TIER.get()), "Case behavior changed: review preservation fix");
        var bonus = (LegacyAttributeBonus) holder.get().getBonuses().get(0);
        helper.assertTrue(Math.abs(bonus.createModifier(UnsocketedGem.of(extracted)).amount() - 3.0) < 0.000001,
                "Expected known Esoteric-to-Ancient data-loss hazard not reproduced");
        helper.succeed();
    }
}
