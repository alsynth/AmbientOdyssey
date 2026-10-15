package dev.ambientodyssey.starterchest;

import java.util.List;
import com.mojang.serialization.MapCodec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import dev.shadowsoffire.apotheosis.Apoth;
import dev.shadowsoffire.apotheosis.affix.ItemAffixes;
import dev.shadowsoffire.apotheosis.loot.LootController;
import dev.shadowsoffire.apotheosis.loot.LootRarity;
import dev.shadowsoffire.apotheosis.loot.RarityRegistry;
import dev.shadowsoffire.apotheosis.tiers.GenContext;
import dev.shadowsoffire.apotheosis.tiers.WorldTier;
import it.unimi.dsi.fastutil.objects.ObjectArrayList;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.storage.loot.LootContext;
import net.minecraft.world.level.storage.loot.parameters.LootContextParams;
import net.minecraft.world.level.storage.loot.predicates.LootItemCondition;
import net.minecraft.world.phys.Vec3;
import net.neoforged.neoforge.common.loot.IGlobalLootModifier;
import net.neoforged.neoforge.common.loot.LootModifier;

/**
 * Adds one genuine Apotheosis affix item to the optional world-creation Bonus Chest.
 * Uses Apotheosis's own rarity rule engine; it never writes decorative fake components.
 * Must run after Apotheosis's generic affix injection to guarantee *exactly* one such item.
 * Packaging is gated on a native, 2-player Lootr test for execution order.
 */
public final class StarterAffixModifier extends LootModifier {
    public static final MapCodec<StarterAffixModifier> CODEC = RecordCodecBuilder.mapCodec(
            inst -> LootModifier.codecStart(inst).apply(inst, StarterAffixModifier::new));
    private static final ResourceLocation BONUS = ResourceLocation.parse("minecraft:chests/spawn_bonus_chest");
    private static final Item[] BASE_ITEMS = {
            Items.IRON_SWORD, Items.IRON_PICKAXE, Items.IRON_CHESTPLATE,
            Items.IRON_HELMET, Items.IRON_BOOTS, Items.BOW, Items.SHIELD
    };

    private static final String[] SPELLSTONES = {
            "enigmaticlegacyplus:blazing_core", "enigmaticlegacyplus:golem_heart",
            "enigmaticlegacyplus:ocean_stone", "enigmaticlegacyplus:angel_blessing",
            "enigmaticlegacyplus:lost_engine"
    };
    private static final Item[] COOKED_MEATS = {
            Items.COOKED_BEEF, Items.COOKED_PORKCHOP, Items.COOKED_CHICKEN, Items.COOKED_MUTTON
    };

    public StarterAffixModifier(LootItemCondition[] conditions) {
        super(conditions);
    }

    @Override
    public MapCodec<? extends IGlobalLootModifier> codec() { return CODEC; }

    @Override
    protected ObjectArrayList<ItemStack> doApply(ObjectArrayList<ItemStack> loot, LootContext ctx) {
        if (!BONUS.equals(ctx.getQueriedLootTableId())) return loot;
        final List<LootRarity> selectedPool = RarityRegistry.getSortedRarities().stream()
                .filter(r -> {
                    ResourceLocation key = RarityRegistry.INSTANCE.getKey(r);
                    return key != null && ("common".equals(key.getPath())
                            || "uncommon".equals(key.getPath()) || "rare".equals(key.getPath()));
                }).toList();
        if (selectedPool.size() != 3) return loot; // No fake item if registry is incomplete.
        int roll = ctx.getRandom().nextInt(100);
        String target = roll < 55 ? "common" : roll < 85 ? "uncommon" : "rare";
        LootRarity rarity = selectedPool.stream()
                .filter(r -> target.equals(RarityRegistry.INSTANCE.getKey(r).getPath()))
                .findFirst().orElse(null);
        if (rarity == null) return loot;
        GenContext context = GenContext.forLoot(ctx);
        if (context == null) {
            Vec3 origin = ctx.getParamOrNull(LootContextParams.ORIGIN);
            BlockPos pos = origin == null ? ctx.getLevel().getSharedSpawnPos() : BlockPos.containing(origin);
            context = GenContext.standalone(ctx.getRandom(), WorldTier.HAVEN, ctx.getLuck(), ctx.getLevel(), pos);
        }
        final int start = ctx.getRandom().nextInt(BASE_ITEMS.length);
        ItemStack affixed = ItemStack.EMPTY;
        for (int i = 0; i < BASE_ITEMS.length; ++i) {
            ItemStack candidate = LootController.createLootItem(
                    new ItemStack(BASE_ITEMS[(start + i) % BASE_ITEMS.length]), rarity, context);
            if (!candidate.getOrDefault(Apoth.Components.AFFIXES, ItemAffixes.EMPTY).isEmpty()) {
                affixed = candidate;
                break;
            }
        }
        if (affixed.isEmpty()) return loot; // Avoid handing out an un-affixed impostor.
        // Ensures one, not the ordinary Apotheosis chest bonus plus another, provided this
        // modifier is ordered AFTER other mod-wide loot injection.
        loot.removeIf(stack -> !stack.getOrDefault(Apoth.Components.AFFIXES, ItemAffixes.EMPTY).isEmpty());
        affixed.set(Apoth.Components.FROM_CHEST, true);
        loot.add(affixed);
        // Crucial: append our extras to the already-generated vanilla Bonus Chest loot.
        // This module must NOT override minecraft:chests/spawn_bonus_chest.
        ResourceLocation spellstoneId = ResourceLocation.parse(
                SPELLSTONES[ctx.getRandom().nextInt(SPELLSTONES.length)]);
        Item spellstone = BuiltInRegistries.ITEM.get(spellstoneId);
        if (spellstone != null && spellstone != Items.AIR) {
            loot.add(new ItemStack(spellstone));
        }
        loot.add(new ItemStack(Items.TORCH, 32 + ctx.getRandom().nextInt(17)));
        loot.add(new ItemStack(
                COOKED_MEATS[ctx.getRandom().nextInt(COOKED_MEATS.length)],
                16 + ctx.getRandom().nextInt(33)));
        return loot;
    }
}
