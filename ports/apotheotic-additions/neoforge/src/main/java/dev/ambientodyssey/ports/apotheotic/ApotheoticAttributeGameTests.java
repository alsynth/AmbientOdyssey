package dev.ambientodyssey.ports.apotheotic;

import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import com.mojang.serialization.JsonOps;
import dev.shadowsoffire.apotheosis.affix.AffixHelper;
import dev.shadowsoffire.apotheosis.affix.AffixRegistry;
import dev.shadowsoffire.apotheosis.affix.AttributeAffix;
import dev.shadowsoffire.apotheosis.affix.ItemAffixes;
import dev.shadowsoffire.apotheosis.loot.LootCategory;
import dev.shadowsoffire.apotheosis.loot.RarityRegistry;
import dev.shadowsoffire.placebo.util.StepFunction;
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
public final class ApotheoticAttributeGameTests {
    private static JsonObject manifest() {
        var input = ApotheoticAttributeGameTests.class.getResourceAsStream("/assets/ao_apotheotic_port/core-attribute-port-manifest.json");
        if (input == null) throw new IllegalStateException("Missing migration manifest");
        try (var reader = new InputStreamReader(input, StandardCharsets.UTF_8)) {
            return JsonParser.parseReader(reader).getAsJsonObject();
        } catch (java.io.IOException failure) { throw new IllegalStateException(failure); }
    }

    @GameTest(template = "empty")
    public static void allTwentyFiveCoreAffixesLoadAndAvoidStockRarities(GameTestHelper helper) {
        int count = 0;
        var mythic = RarityRegistry.INSTANCE.holder(ResourceLocation.fromNamespaceAndPath("apotheosis", "mythic")).get();
        for (var entry : manifest().getAsJsonArray("attribute_affixes")) {
            var row = entry.getAsJsonObject();
            if (!row.get("status").getAsString().equals("ported_core_attribute")) continue;
            var holder = AffixRegistry.INSTANCE.holder(ResourceLocation.parse(row.get("ported_id").getAsString()));
            helper.assertTrue(holder.isBound() && holder.get() instanceof AttributeAffix, "Native attribute affix failed to bind");
            for (var categoryId : row.getAsJsonArray("categories")) {
                ItemStack sample = sample(categoryId.getAsString());
                var category = LootCategory.forItem(sample);
                helper.assertTrue(category.getKey().toString().equals(categoryId.getAsString()), "Wrong native item category");
                helper.assertFalse(holder.get().canApplyTo(sample, category, mythic), "Custom-only affix leaked into stock rarity pool");
                for (String rarityId : row.getAsJsonObject("values").keySet()) {
                    var rarity = RarityRegistry.INSTANCE.holder(ResourceLocation.parse(rarityId)).get();
                    helper.assertTrue(holder.get().canApplyTo(sample, category, rarity), "Ported affix cannot apply to its original rarity/category");
                }
            }
            count++;
        }
        helper.assertTrue(count == 25, "Core affix inventory changed");
        helper.succeed();
    }

    @GameTest(template = "empty")
    public static void everyNativeCurvePreservesOriginalDiscreteRolls(GameTestHelper helper) {
        for (var entry : manifest().getAsJsonArray("attribute_affixes")) {
            var row = entry.getAsJsonObject();
            if (!row.get("status").getAsString().equals("ported_core_attribute")) continue;
            var holder = AffixRegistry.INSTANCE.holder(ResourceLocation.parse(row.get("ported_id").getAsString()));
            helper.assertTrue(holder.isBound(), "Affix missing before curve check");
            var encoded = AttributeAffix.CODEC.encodeStart(JsonOps.INSTANCE, (AttributeAffix) holder.get()).getOrThrow().getAsJsonObject();
            for (var pair : row.getAsJsonObject("values").entrySet()) {
                var expected = pair.getValue().getAsJsonObject();
                var curve = StepFunction.CODEC.parse(JsonOps.INSTANCE, encoded.getAsJsonObject("values").get(pair.getKey())).getOrThrow();
                float min = expected.get("min").getAsFloat();
                float step = expected.get("step").getAsFloat();
                int steps = expected.get("steps").getAsInt();
                helper.assertTrue(Math.abs(curve.min() - min) < 0.0001 && Math.abs(curve.step() - step) < 0.0001,
                        "Original curve bounds/increment changed");
                if (step != 0) helper.assertTrue(curve.steps() == steps, "Original discrete step count changed");
                helper.assertTrue(Math.abs(curve.get(0) - min) < 0.0001 && Math.abs(curve.get(1) - (min + steps * step)) < 0.0001,
                        "Original minimum/maximum roll changed");
            }
        }
        helper.succeed();
    }

    @GameTest(template = "empty", timeoutTicks = 80)
    public static void artifactDamageAffectsEquippedEntityAndPersists(GameTestHelper helper) {
        var rarity = RarityRegistry.INSTANCE.holder(ResourceLocation.fromNamespaceAndPath(ApotheoticPort.ID, "artifact"));
        var affix = AffixRegistry.INSTANCE.holder(ResourceLocation.fromNamespaceAndPath(ApotheoticPort.ID, "sword/attribute/artifact_damage"));
        helper.assertTrue(rarity.isBound() && affix.isBound(), "Damage test inputs did not bind");
        ItemStack sword = new ItemStack(Items.DIAMOND_SWORD);
        AffixHelper.setRarity(sword, rarity.get());
        AffixHelper.setAffixes(sword, ItemAffixes.EMPTY.toBuilder().put(affix, 1).build());
        var golem = helper.spawn(EntityType.IRON_GOLEM, new BlockPos(2, 1, 2));
        double base = golem.getAttributeBaseValue(Attributes.ATTACK_DAMAGE);
        golem.setItemSlot(EquipmentSlot.MAINHAND, sword);
        helper.runAfterDelay(5, () -> {
            helper.assertTrue(Math.abs(golem.getAttributeValue(Attributes.ATTACK_DAMAGE) - (base + 6 + 20)) < 0.0001,
                    "Original maximum Artifact damage bonus did not affect a real equipped entity");
            ItemStack restored = ItemStack.parse(helper.getLevel().registryAccess(), sword.save(helper.getLevel().registryAccess())).orElseThrow();
            golem.setItemSlot(EquipmentSlot.MAINHAND, restored);
            helper.runAfterDelay(5, () -> {
                helper.assertTrue(Math.abs(golem.getAttributeValue(Attributes.ATTACK_DAMAGE) - (base + 6 + 20)) < 0.0001,
                        "Reloaded affix lost or duplicated its equipped damage modifier");
                golem.discard();
                helper.succeed();
            });
        });
    }

    private static ItemStack sample(String category) {
        return new ItemStack(switch (category) {
            case "apotheosis:melee_weapon" -> Items.DIAMOND_SWORD;
            case "apotheosis:trident" -> Items.TRIDENT;
            case "apotheosis:bow" -> Items.BOW;
            case "apotheosis:breaker" -> Items.DIAMOND_PICKAXE;
            case "apotheosis:helmet" -> Items.DIAMOND_HELMET;
            case "apotheosis:chestplate" -> Items.DIAMOND_CHESTPLATE;
            case "apotheosis:leggings" -> Items.DIAMOND_LEGGINGS;
            case "apotheosis:boots" -> Items.DIAMOND_BOOTS;
            case "apotheosis:shield" -> Items.SHIELD;
            default -> throw new IllegalArgumentException("Unverified category " + category);
        });
    }
}
