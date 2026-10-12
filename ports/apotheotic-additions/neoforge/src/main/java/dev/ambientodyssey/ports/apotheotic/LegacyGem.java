package dev.ambientodyssey.ports.apotheotic;
import dev.shadowsoffire.apotheosis.socket.gem.Gem;
import dev.shadowsoffire.apotheosis.socket.gem.Purity;
import net.minecraft.core.component.DataComponents;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.ItemStack;
import java.util.OptionalInt;
import java.util.function.IntPredicate;
/** Nine original tiers use native definitions and an independent component. */
public final class LegacyGem {
 public static final int FIRST_COMPONENT_TIER = 5;
 public static final String[] TIERS = {"common", "uncommon", "rare", "epic", "mythic", "ancient", "artifact", "heirloom", "esoteric"};
 public static ItemStack toLegacyStack(Gem gem, int tier) {
  if (tier < 0 || tier > 8 || gem.getBonuses().stream().anyMatch(b -> !(b instanceof LegacyAttributeBonus legacy) || !legacy.supportsTier(tier)))
   throw new IllegalArgumentException("Unsupported exact legacy tier: " + tier);
  ItemStack stack = gem.toStack(Purity.values()[Math.min(5, tier)]);
  // Tiers 0..4 are exactly represented by native purity; a component there could go stale
  // when stock purity upgrades copy the stack. Only upper tiers (5..8, all backed by PERFECT) carry it.
  if (tier >= FIRST_COMPONENT_TIER) stack.set(ApotheoticPort.LEGACY_GEM_TIER.get(), tier);
  // Same staleness reason: lower tiers keep the stock purity-derived name.
  if (tier >= FIRST_COMPONENT_TIER) stack.set(DataComponents.CUSTOM_NAME, Component.literal(TIERS[tier] + " ").append(Component.translatable("item.apotheosis.gem." + gem.getId())));
  return stack;
 }
 /** @deprecated unvalidated; use {@link #resolveTier}. */
 @Deprecated
 public static int tier(ItemStack stack, Purity fallback) {
  return stack.getOrDefault(ApotheoticPort.LEGACY_GEM_TIER.get(), fallback.ordinal());
 }

 /**
  * Exact tier of a gem stack, or empty when the stack is not valid for this bonus. Never escalates:
  * native purity is the ceiling. A component below 5, or any component on a non-PERFECT stack, is ignored
  * (purity wins). A PERFECT stack with component 5..8 uses it if supported, else resolves to empty.
  * With no component on a PERFECT stack: Ancient if supported, else the lowest supported upper tier.
  */
 public static OptionalInt resolveTier(ItemStack stack, Purity purity, IntPredicate supports) {
  // Native GemView clamps malformed stacks up to a gem's minimum purity. That
  // view must not raise the ceiling represented by the actual item component.
  var storedPurity = dev.shadowsoffire.apotheosis.socket.gem.GemItem.getPurity(stack);
  if (storedPurity.ordinal() < purity.ordinal()) purity = storedPurity;
  if (purity.ordinal() < 5) return supports.test(purity.ordinal()) ? OptionalInt.of(purity.ordinal()) : OptionalInt.empty();
  Integer component = stack.get(ApotheoticPort.LEGACY_GEM_TIER.get());
  if (component != null && component >= FIRST_COMPONENT_TIER && component <= 8)
   return supports.test(component) ? OptionalInt.of(component) : OptionalInt.empty();
  for (int t = 5; t <= 8; t++) if (supports.test(t)) return OptionalInt.of(t);
  return OptionalInt.empty();
 }
 /** True for Artifact/Heirloom/Esoteric stacks (component 6..8), which stock purity-only code cannot represent. Ancient (5) is exactly native PERFECT. */
 public static boolean isNonNativeUpperTier(ItemStack stack) {
  Integer c = stack.get(ApotheoticPort.LEGACY_GEM_TIER.get());
  return c != null && c >= 6 && c <= 8;
 }
}
