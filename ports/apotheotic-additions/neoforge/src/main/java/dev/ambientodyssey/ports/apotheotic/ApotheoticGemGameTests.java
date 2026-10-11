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
                helper.assertTrue(restored.get(ApotheoticPort.LEGACY_GEM_TIER.get()) == tier, "Lost exact legacy tier in item serialization");
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
}
