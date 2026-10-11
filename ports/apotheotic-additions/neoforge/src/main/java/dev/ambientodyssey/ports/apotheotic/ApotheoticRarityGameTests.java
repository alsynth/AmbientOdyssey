package dev.ambientodyssey.ports.apotheotic;

import dev.shadowsoffire.apotheosis.affix.AffixHelper;
import dev.shadowsoffire.apotheosis.loot.LootRarity;
import dev.shadowsoffire.apotheosis.loot.RarityRegistry;
import dev.shadowsoffire.apotheosis.tiers.GenContext;
import dev.shadowsoffire.apotheosis.tiers.WorldTier;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.Registries;
import net.minecraft.tags.TagKey;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.RandomSource;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

@GameTestHolder(ApotheoticPort.ID)
@PrefixGameTestTemplate(false)
public final class ApotheoticRarityGameTests {
    private static final String[] NAMES = {"artifact", "heirloom", "esoteric"};

    private static LootRarity rarity(GameTestHelper helper, String name) {
        var holder = RarityRegistry.INSTANCE.holder(ResourceLocation.fromNamespaceAndPath(ApotheoticPort.ID, name));
        helper.assertTrue(holder.isBound(), "Native Apotheosis did not load rarity " + name);
        return holder.get();
    }

    @GameTest(template = "empty")
    public static void allThreeNativeRaritiesAndMaterialsBind(GameTestHelper helper) {
        Item[] materials = {ApotheoticPort.ARTIFACT_MATERIAL.get(), ApotheoticPort.HEIRLOOM_MATERIAL.get(), ApotheoticPort.ESOTERIC_MATERIAL.get()};
        int[] counts = {8, 4, 16};
        for (int i = 0; i < NAMES.length; i++) {
            LootRarity value = rarity(helper, NAMES[i]);
            helper.assertTrue(value.getMaterial() == materials[i], "Incorrect rarity material binding");
            helper.assertTrue(new ItemStack(materials[i]).is(TagKey.create(Registries.ITEM,
                    ResourceLocation.fromNamespaceAndPath("apotheosis", "rarity_materials"))), "Material missing from reforge ingredient tag");
            var reverse = RarityRegistry.getMaterialRarity(materials[i]);
            helper.assertTrue(reverse.isBound() && reverse.get() == value, "Material reverse lookup did not bind");
            helper.assertTrue(value.rules().size() == counts[i], "Original rarity rule count changed");
        }
        var mythic = RarityRegistry.INSTANCE.holder(ResourceLocation.fromNamespaceAndPath("apotheosis", "mythic"));
        helper.assertTrue(mythic.isBound(), "Built-in Mythic rarity must remain present");
        helper.assertTrue(rarity(helper, "artifact").sortIndex() > mythic.get().sortIndex(), "Artifact must sort above Mythic");
        helper.assertTrue(rarity(helper, "heirloom").sortIndex() > rarity(helper, "artifact").sortIndex(), "Heirloom ordering changed");
        helper.assertTrue(rarity(helper, "esoteric").sortIndex() > rarity(helper, "heirloom").sortIndex(), "Esoteric ordering changed");
        helper.succeed();
    }

    @GameTest(template = "empty")
    public static void customRaritiesRemainAbsentFromNaturalRolls(GameTestHelper helper) {
        for (String name : NAMES) {
            LootRarity value = rarity(helper, name);
            for (WorldTier tier : WorldTier.values()) {
                for (float luck : new float[]{0, 10, 100}) {
                    helper.assertTrue(value.weights().getWeight(tier, luck) == 0, "Incomplete rarity became obtainable: " + name);
                }
            }
        }
        for (WorldTier tier : WorldTier.values()) {
            var context = GenContext.standalone(RandomSource.create(987654321L), tier, 100,
                    helper.getLevel(), helper.absolutePos(new BlockPos(1, 1, 1)));
            for (int roll = 0; roll < 100; roll++) {
                LootRarity result = LootRarity.random(context);
                helper.assertTrue(result != null, "Built-in rarity rolls must remain usable");
                helper.assertFalse(RarityRegistry.INSTANCE.getKey(result).getNamespace().equals(ApotheoticPort.ID), "A prototype leaked into natural drops");
            }
        }
        helper.succeed();
    }

    @GameTest(template = "empty")
    public static void allThreeRarityComponentsSurviveItemSerialization(GameTestHelper helper) {
        for (String name : NAMES) {
            LootRarity value = rarity(helper, name);
            ItemStack item = new ItemStack(Items.DIAMOND_SWORD);
            AffixHelper.setRarity(item, value);
            var saved = item.save(helper.getLevel().registryAccess());
            ItemStack reloaded = ItemStack.parse(helper.getLevel().registryAccess(), saved).orElseThrow();
            helper.assertTrue(AffixHelper.getRarity(reloaded).get() == value, "Native component serialization lost rarity " + name);
        }
        helper.succeed();
    }

    @GameTest(template = "empty", batch = "rarity_reload", timeoutTicks = 400)
    public static void allThreeRaritiesRebindAfterRealDataReload(GameTestHelper helper) {
        var server = helper.getLevel().getServer();
        var reload = server.reloadResources(server.getPackRepository().getSelectedIds());
        helper.onEachTick(() -> {
            if (!reload.isDone()) return;
            helper.succeedIf(() -> {
                reload.join();
                for (String name : NAMES) {
                    LootRarity value = rarity(helper, name);
                    helper.assertTrue(RarityRegistry.getMaterialRarity(value.getMaterial()).get() == value,
                            "Rarity material map did not rebuild after reload");
                    ItemStack item = new ItemStack(Items.DIAMOND_SWORD);
                    AffixHelper.setRarity(item, value);
                    helper.assertTrue(AffixHelper.getRarity(item).get() == value, "Rarity component failed after reload");
                }
            });
        });
    }
}
