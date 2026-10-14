package dev.ambientodyssey.augmentingsigils;

import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.ItemStack;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;
import dev.shadowsoffire.apotheosis.Apoth;
import dev.shadowsoffire.apotheosis.AdventureConfig;
import dev.shadowsoffire.apotheosis.affix.augmenting.AugmentingMenu;

@GameTestHolder(AOAugmentingSigils.MOD_ID)
@PrefixGameTestTemplate(false)
public final class AOAugmentingGameTests {
    @GameTest(template = "empty")
    public static void costMapPreservesVanillaAndLatePrices(GameTestHelper h) throws Exception {
        final String[] rarities = { "ancient", "artifact", "heirloom", "esoteric" };
        final int[] rerolls = { 6, 18, 24, 32 };
        for (int i = 0; i < rarities.length; i++) {
            String namespace = i == 0 ? "apotheosis" : "apotheotic_additions";
            ResourceLocation key = ResourceLocation.fromNamespaceAndPath(namespace, rarities[i]);
            int reroll = SigilCosts.fromId(key, 1, false);
            int upgrade = SigilCosts.fromId(key, 2, true);
            h.assertTrue(reroll == rerolls[i] && upgrade == rerolls[i] * 2,
                    "Wrong "+key+": "+reroll+"/"+upgrade);
            {
                var alt = ResourceLocation.fromNamespaceAndPath("ao_apotheotic_port", rarities[i]);
                h.assertTrue(SigilCosts.fromId(alt, 1, false) == rerolls[i],
                        "AO prototype alias must match");
            }
        }
        h.assertTrue(SigilCosts.fromId(ResourceLocation.parse("apotheosis:mythic"),1,false)==1, "Mythic reroll changed");
        h.assertTrue(SigilCosts.fromId(ResourceLocation.parse("apotheosis:mythic"),2,true)==2, "Mythic upgrade changed");
        h.assertTrue(SigilCosts.fromId(ResourceLocation.parse("foreign:esoteric"),1,false)==1, "Non-AO rarity changed");
        h.assertTrue(SigilCosts.fromId(null,1,false)==1, "Null rarity changed");
        // Force server-side Mixin target class loading.
        Class.forName(AugmentingMenu.class.getName());
        h.succeed();
    }
    @GameTest(template = "empty")
    public static void maxPriceFitsSigilSlotStack(GameTestHelper h) {
        ItemStack sigils = new ItemStack(Apoth.Items.SIGIL_OF_ENHANCEMENT.value(),64);
        h.assertTrue(sigils.getMaxStackSize() >= 64 && sigils.getCount()==64,
                "64-sigil Esoteric upgrade cannot fit in one payment slot");
        h.assertTrue(AdventureConfig.rerollSigilCost==1 && AdventureConfig.upgradeSigilCost==2,
                "Existing default Sigil costs changed");
        h.assertTrue(AdventureConfig.rerollLevelCost==175 && AdventureConfig.upgradeLevelCost==225,
                "Existing experience-level costs changed");
        h.succeed();
    }
}
