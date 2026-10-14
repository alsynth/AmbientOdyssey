package dev.ambientodyssey.campaign;

import java.util.ArrayList;
import dev.shadowsoffire.apotheosis.socket.gem.Gem;
import dev.shadowsoffire.apotheosis.socket.gem.GemRegistry;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.item.ItemStack;

/** Uses the supplied r19 port's real support check and stack factory, never cosmetic gem tags. */
public final class BossGems {
    private BossGems() {}
    public static ItemStack create(ServerPlayer player, String grade) {
        try {
            Class<?> legacy = Class.forName("dev.ambientodyssey.ports.apotheotic.LegacyGem");
            String[] tiers = (String[]) legacy.getField("TIERS").get(null);
            int tier = -1;
            for (int i = 0; i < tiers.length; i++) if (grade.equalsIgnoreCase(tiers[i])) tier = i;
            if (tier < 0) return ItemStack.EMPTY;
            var supports = legacy.getMethod("supportsTier", Gem.class, int.class);
            var make = legacy.getMethod("toLegacyStack", Gem.class, int.class);
            var candidates = new ArrayList<Gem>();
            for (Gem gem : GemRegistry.INSTANCE.getValues())
                if ((boolean) supports.invoke(null, gem, tier)) candidates.add(gem);
            if (candidates.isEmpty()) return ItemStack.EMPTY;
            return (ItemStack) make.invoke(null, candidates.get(player.getRandom().nextInt(candidates.size())), tier);
        } catch (ReflectiveOperationException | LinkageError e) {
            return ItemStack.EMPTY; // No counterfeit grade or fallback duplicate equipment.
        }
    }
}
