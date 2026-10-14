package dev.ambientodyssey.starterchest;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;
import dev.shadowsoffire.apotheosis.Apoth;
import dev.shadowsoffire.apotheosis.affix.ItemAffixes;
import dev.shadowsoffire.apotheosis.loot.RarityRegistry;
import it.unimi.dsi.fastutil.objects.ObjectArrayList;
import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.storage.loot.LootContext;
import net.minecraft.world.level.storage.loot.LootParams;
import net.minecraft.world.level.storage.loot.parameters.LootContextParamSets;
import net.minecraft.world.level.storage.loot.parameters.LootContextParams;
import net.minecraft.world.phys.Vec3;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

/**
 * Native GameTests. This class is deliberately excluded from production JARs.
 * Tests real Apotheosis reload registries, affix generation, and modifier targeting.
 * Does not test Lootr per-player world-creation Bonus Chest conversion.
 */
@GameTestHolder(AOStarterChestMod.MOD_ID)
@PrefixGameTestTemplate(false)
public final class StarterAffixGameTests {
    private static final ResourceLocation BONUS = ResourceLocation.parse("minecraft:chests/spawn_bonus_chest");
    private static LootContext context(GameTestHelper h, ResourceLocation id) {
        var params = new LootParams.Builder(h.getLevel())
                .withParameter(LootContextParams.ORIGIN, Vec3.atCenterOf(h.absolutePos(BlockPos.ZERO)))
                .create(LootContextParamSets.CHEST);
        var ctx = new LootContext.Builder(params).create(Optional.empty());
        ctx.setQueriedLootTableId(id); // NeoForge sets this when a real loot table is evaluated.
        return ctx;
    }

    @GameTest(template = "empty")
    public static void everyStarterRollIsRealAndRespectsRarityMix(GameTestHelper h) {
        var generator = new StarterAffixModifier(new net.minecraft.world.level.storage.loot.predicates.LootItemCondition[0]);
        Map<String, Integer> counts = new HashMap<>();
        for (int i=0; i<600; i++) {
            var items = new ObjectArrayList<ItemStack>();
            items.add(new ItemStack(Items.TORCH, 40));
            var queriedCtx = context(h, BONUS);
            generator.apply(items, queriedCtx);
            long affixCount = items.stream()
                .filter(s -> !s.getOrDefault(Apoth.Components.AFFIXES, ItemAffixes.EMPTY).isEmpty()).count();
            h.assertTrue(affixCount == 1, "Missing or duplicate affix item at iteration " + i
                    + " queried=" + queriedCtx.getQueriedLootTableId()
                    + " rarities=" + RarityRegistry.getSortedRarities().stream()
                          .map(r -> RarityRegistry.INSTANCE.getKey(r).toString()).toList()
                    + " items=" + items);
            h.assertTrue(items.size() == 2 && items.get(0).is(Items.TORCH) && items.get(0).getCount() == 40,
                    "Normal starter supplies were replaced or damaged");
            ItemStack reward = items.get(1);
            var rarity = reward.get(Apoth.Components.RARITY);
            h.assertTrue(rarity != null && rarity.isBound(), "Rolled equipment has no bound rarity");
            String key = RarityRegistry.INSTANCE.getKey(rarity.get()).getPath();
            h.assertTrue(key.equals("common") || key.equals("uncommon") || key.equals("rare"),
                    "Unexpected starter rarity " + key);
            counts.merge(key, 1, Integer::sum);
        }
        // Broad bounds catch inverted/incorrect rarity tables without flaky exact-count tests.
        h.assertTrue(counts.getOrDefault("common",0) >= 270 && counts.getOrDefault("common",0) <= 390,
                "Common share unexpectedly far from 55%: " + counts);
        h.assertTrue(counts.getOrDefault("uncommon",0) >= 120 && counts.getOrDefault("uncommon",0) <= 240,
                "Uncommon share unexpectedly far from 30%: " + counts);
        h.assertTrue(counts.getOrDefault("rare",0) >= 45 && counts.getOrDefault("rare",0) <= 135,
                "Rare share unexpectedly far from 15%: " + counts);
        h.succeed();
    }

    @GameTest(template = "empty")
    public static void nonBonusLootUnchanged(GameTestHelper h) {
        var generator = new StarterAffixModifier(new net.minecraft.world.level.storage.loot.predicates.LootItemCondition[0]);
        var loot = new ObjectArrayList<ItemStack>();
        var diamond = new ItemStack(Items.DIAMOND, 4);
        loot.add(diamond);
        var result = generator.apply(loot, context(h, ResourceLocation.parse("minecraft:chests/simple_dungeon")));
        h.assertTrue(result == loot && loot.size() == 1 && loot.get(0) == diamond && diamond.getCount() == 4,
                "Unrelated dungeon loot was altered");
        h.succeed();
    }
}
