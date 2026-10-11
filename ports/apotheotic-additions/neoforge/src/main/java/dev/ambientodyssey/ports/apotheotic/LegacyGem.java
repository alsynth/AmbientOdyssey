package dev.ambientodyssey.ports.apotheotic;
import dev.shadowsoffire.apotheosis.socket.gem.Gem;
import dev.shadowsoffire.apotheosis.socket.gem.Purity;
import net.minecraft.core.component.DataComponents;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.ItemStack;
/** Nine original tiers use native definitions and an independent component. */
public final class LegacyGem {
 public static final String[] TIERS = {"common", "uncommon", "rare", "epic", "mythic", "ancient", "artifact", "heirloom", "esoteric"};
 public static ItemStack toLegacyStack(Gem gem, int tier) {
  if (tier < 0 || tier > 8 || gem.getBonuses().stream().anyMatch(b -> !(b instanceof LegacyAttributeBonus legacy) || !legacy.supportsTier(tier)))
   throw new IllegalArgumentException("Unsupported exact legacy tier: " + tier);
  ItemStack stack = gem.toStack(Purity.values()[Math.min(5, tier)]);
  stack.set(ApotheoticPort.LEGACY_GEM_TIER.get(), tier);
  stack.set(DataComponents.CUSTOM_NAME, Component.literal(TIERS[tier] + " ").append(Component.translatable("item.apotheosis.gem." + gem.getId())));
  return stack;
 }
 public static int tier(ItemStack stack, Purity fallback) {
  return stack.getOrDefault(ApotheoticPort.LEGACY_GEM_TIER.get(), fallback.ordinal());
 }
}
