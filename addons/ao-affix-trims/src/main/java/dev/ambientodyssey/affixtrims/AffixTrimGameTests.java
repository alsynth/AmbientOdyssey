package dev.ambientodyssey.affixtrims;

import dev.shadowsoffire.apotheosis.Apoth;
import dev.shadowsoffire.apotheosis.affix.AffixHelper;
import dev.shadowsoffire.apotheosis.affix.ItemAffixes;
import dev.shadowsoffire.apotheosis.loot.LootController;
import dev.shadowsoffire.apotheosis.loot.RarityRegistry;
import dev.shadowsoffire.apotheosis.tiers.GenContext;
import dev.shadowsoffire.apotheosis.tiers.WorldTier;
import net.minecraft.core.BlockPos;
import net.minecraft.core.component.DataComponents;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.RandomSource;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

@GameTestHolder(AffixTrimMod.MODID)
@PrefixGameTestTemplate(false)
public final class AffixTrimGameTests {
    private static ItemStack loot(GameTestHelper helper, net.minecraft.world.item.Item item) {
        var rarity = RarityRegistry.INSTANCE.holder(ResourceLocation.parse("apotheosis:epic")).get();
        var context = GenContext.standalone(RandomSource.create(7531), WorldTier.values()[0], 0,
                helper.getLevel(), helper.absolutePos(BlockPos.ZERO));
        return LootController.createLootItem(new ItemStack(item), rarity, context);
    }

    @GameTest(template = "empty")
    public static void nativeFactoryTrimsAllFourArmorSlots(GameTestHelper helper) {
        for (var item : new net.minecraft.world.item.Item[]{Items.DIAMOND_HELMET, Items.DIAMOND_CHESTPLATE,
                Items.DIAMOND_LEGGINGS, Items.DIAMOND_BOOTS}) {
            var stack = loot(helper, item);
            helper.assertTrue(AffixHelper.hasAffixes(stack), "Native affix generation failed");
            helper.assertTrue(stack.has(DataComponents.TRIM), "Factory return hook missed affixed armor");
            var trim = stack.get(DataComponents.TRIM);
            helper.assertTrue(trim.material().unwrapKey().orElseThrow().location().getNamespace().equals("minecraft")
                    && trim.pattern().unwrapKey().orElseThrow().location().getNamespace().equals("minecraft"),
                    "Only vanilla trim assets are supported");
        }
        helper.succeed();
    }

    @GameTest(template = "empty")
    public static void ordinaryArmorAndAffixedWeaponsStayUntrimmed(GameTestHelper helper) {
        helper.assertFalse(AffixTrims.apply(new ItemStack(Items.DIAMOND_CHESTPLATE), helper.getLevel().registryAccess()), "Plain armor gained a trim");
        var sword = loot(helper, Items.DIAMOND_SWORD);
        helper.assertTrue(AffixHelper.hasAffixes(sword), "Weapon fixture is not affixed");
        helper.assertFalse(sword.has(DataComponents.TRIM), "Sword gained an armor trim");
        helper.assertFalse(AffixTrims.apply(ItemStack.EMPTY, helper.getLevel().registryAccess()), "Empty stack modified");
        helper.succeed();
    }

    @GameTest(template = "empty")
    public static void existingTrimsAndEveryOtherComponentSurvive(GameTestHelper helper) {
        var stack = loot(helper, Items.DIAMOND_CHESTPLATE);
        var before = stack.copy();
        helper.assertFalse(AffixTrims.apply(stack, helper.getLevel().registryAccess()), "Existing trim rerolled");
        helper.assertTrue(ItemStack.isSameItemSameComponents(before, stack), "Existing components changed");
        stack.remove(DataComponents.TRIM);
        before = stack.copy();
        helper.assertTrue(AffixTrims.apply(stack, helper.getLevel().registryAccess()), "Affixed fixture was skipped");
        stack.remove(DataComponents.TRIM);
        helper.assertTrue(ItemStack.isSameItemSameComponents(before, stack), "Affixes/rarity/name changed");
        helper.succeed();
    }

    @GameTest(template = "empty")
    public static void lateAndOldItemEntityDropsGetTrimmed(GameTestHelper helper) {
        var stack = loot(helper, Items.DIAMOND_BOOTS);
        stack.remove(DataComponents.TRIM);
        var pos = helper.absolutePos(BlockPos.ZERO);
        var entity = new ItemEntity(helper.getLevel(), pos.getX(), pos.getY(), pos.getZ(), stack);
        helper.getLevel().addFreshEntity(entity);
        helper.assertTrue(entity.getItem().has(DataComponents.TRIM), "Item spawn fallback did not run");
        entity.discard();
        helper.succeed();
    }

    @GameTest(template = "empty")
    public static void trimSurvivesNativeSerialization(GameTestHelper helper) {
        var stack = loot(helper, Items.DIAMOND_HELMET);
        var restored = ItemStack.parseOptional(helper.getLevel().registryAccess(),
                (net.minecraft.nbt.CompoundTag) stack.save(helper.getLevel().registryAccess()));
        helper.assertTrue(ItemStack.isSameItemSameComponents(stack, restored), "Trim/affixes lost on save/reload");
        helper.succeed();
    }

    @GameTest(template = "empty")
    public static void emptyAffixMarkersAreNotGenuineLoot(GameTestHelper helper) {
        var stack = new ItemStack(Items.DIAMOND_BOOTS);
        AffixHelper.setRarity(stack, RarityRegistry.INSTANCE.holder(ResourceLocation.parse("apotheosis:epic")).get());
        stack.set(Apoth.Components.AFFIXES, ItemAffixes.EMPTY);
        helper.assertFalse(AffixTrims.apply(stack, helper.getLevel().registryAccess()), "Empty affix markers accepted");
        helper.succeed();
    }

    @GameTest(template = "empty")
    public static void openingOldChestTrimsLootAndPreservesOtherSlots(GameTestHelper helper) {
        var player = net.neoforged.neoforge.common.util.FakePlayerFactory.getMinecraft(helper.getLevel());
        var container = new net.minecraft.world.SimpleContainer(27);
        var armor = loot(helper, Items.DIAMOND_CHESTPLATE);
        armor.remove(DataComponents.TRIM);
        container.setItem(0, armor);
        container.setItem(1, new ItemStack(Items.DIAMOND, 17));
        var menu = net.minecraft.world.inventory.ChestMenu.threeRows(1, player.getInventory(), container);
        net.neoforged.neoforge.common.NeoForge.EVENT_BUS.post(
                new net.neoforged.neoforge.event.entity.player.PlayerContainerEvent.Open(player, menu));
        helper.assertTrue(container.getItem(0).has(DataComponents.TRIM), "Old chest loot was not trimmed on open");
        helper.assertTrue(container.getItem(1).is(Items.DIAMOND) && container.getItem(1).getCount() == 17,
                "Chest contents/counts changed");
        helper.succeed();
    }

    @GameTest(template = "empty")
    public static void globalLootFallbackKeepsOrderAndCounts(GameTestHelper helper) {
        var armor = loot(helper, Items.DIAMOND_HELMET);
        armor.remove(DataComponents.TRIM);
        var diamonds = new ItemStack(Items.DIAMOND, 11);
        var generated = new it.unimi.dsi.fastutil.objects.ObjectArrayList<ItemStack>();
        generated.add(diamonds);
        generated.add(armor);
        var params = new net.minecraft.world.level.storage.loot.LootParams.Builder(helper.getLevel())
                .withParameter(net.minecraft.world.level.storage.loot.parameters.LootContextParams.ORIGIN,
                        net.minecraft.world.phys.Vec3.atCenterOf(helper.absolutePos(BlockPos.ZERO)))
                .create(net.minecraft.world.level.storage.loot.parameters.LootContextParamSets.CHEST);
        var context = new net.minecraft.world.level.storage.loot.LootContext.Builder(params).create(java.util.Optional.empty());
        var result = new RandomAffixArmorTrimModifier(new net.minecraft.world.level.storage.loot.predicates.LootItemCondition[0])
                .apply(generated, context);
        helper.assertTrue(result == generated && result.size() == 2 && result.get(0) == diamonds
                && diamonds.getCount() == 11 && result.get(1) == armor, "Loot order/count changed");
        helper.assertTrue(armor.has(DataComponents.TRIM), "Global fallback missed affixed armor");
        helper.succeed();
    }
}
