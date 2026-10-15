package dev.ambientodyssey.campaign;

import java.util.Map;
import java.util.Set;
import com.mojang.serialization.MapCodec;
import dev.shadowsoffire.apotheosis.Apoth;
import dev.shadowsoffire.apotheosis.affix.AffixHelper;
import dev.shadowsoffire.apotheosis.affix.ItemAffixes;
import dev.shadowsoffire.apotheosis.loot.RarityRegistry;
import dev.shadowsoffire.apotheosis.tiers.WorldTier;
import net.minecraft.commands.Commands;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.item.ItemStack;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.bus.api.EventPriority;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.common.NeoForge;
import net.neoforged.neoforge.common.loot.IGlobalLootModifier;
import net.neoforged.neoforge.event.RegisterCommandsEvent;
import net.neoforged.neoforge.event.entity.living.LivingDeathEvent;
import net.neoforged.neoforge.event.entity.living.MobEffectEvent;
import net.neoforged.neoforge.event.entity.player.PlayerEvent;
import net.neoforged.neoforge.registries.DeferredRegister;
import net.neoforged.neoforge.registries.NeoForgeRegistries;

@Mod("ao_campaign")
public final class AOCampaign {
    public static final String STATE = "ao_campaign_v1";
    public static final Set<String> DISABLED = Set.of("simplymore:stun", "simplymore:implicit_stun", "simplymore:dazzled");
    // Provisional second T6 route; solo equivalence still requires a real fight comparison.
    public static final Map<String, Integer> BOSSES = Map.ofEntries(
        Map.entry("bosses_of_mass_destruction:lich", 5), Map.entry("bosses_of_mass_destruction:void_blossom", 5),
        Map.entry("irons_spellbooks:dead_king", 6), Map.entry("cataclysm:kobolediator", 6),
        Map.entry("cataclysm:netherite_monstrosity", 7), Map.entry("cataclysm:ignis", 8),
        Map.entry("cataclysm:the_leviathan", 8), Map.entry("cataclysm:maledictus", 8),
        Map.entry("cataclysm:ender_guardian", 7), Map.entry("cataclysm:ancient_remnant", 7),
        Map.entry("fdbosses:chesed", 5), Map.entry("fdbosses:malkuth", 5), Map.entry("fdbosses:geburah", 5),
        Map.entry("aquamirae:captain_cornelia", 6),
        Map.entry("remnants:ossukage", 7), Map.entry("remnants:kotsukage", 7),
        Map.entry("remnants:umbrakar", 8),
        Map.entry("archaion:last_of_deepslate", 8),
        Map.entry("bosses_of_mass_destruction:obsidilith", 9),
        Map.entry("irons_spellbooks:fire_boss", 9), Map.entry("cataclysm:scylla", 9));
    private static final DeferredRegister<MapCodec<? extends IGlobalLootModifier>> LOOT =
        DeferredRegister.create(NeoForgeRegistries.Keys.GLOBAL_LOOT_MODIFIER_SERIALIZERS, "ao_campaign");
    static { LOOT.register("rage_glove_gate", () -> RageGloveGate.CODEC); }

    public AOCampaign(IEventBus bus) {
        LOOT.register(bus);
        NeoForge.EVENT_BUS.addListener(EventPriority.LOWEST, this::effect);
        NeoForge.EVENT_BUS.addListener(this::death);
        NeoForge.EVENT_BUS.addListener(this::onClone);
        NeoForge.EVENT_BUS.addListener(this::commands);
    }
    private void effect(MobEffectEvent.Applicable event) {
        var id = BuiltInRegistries.MOB_EFFECT.getKey(event.getEffectInstance().getEffect().value());
        if (id != null && DISABLED.contains(id.toString())) event.setResult(MobEffectEvent.Applicable.Result.DO_NOT_APPLY);
    }
    private void onClone(PlayerEvent.Clone event) {
        if (event.getOriginal().getPersistentData().contains(STATE))
            event.getEntity().getPersistentData().put(STATE, event.getOriginal().getPersistentData().getCompound(STATE).copy());
    }
    private void death(LivingDeathEvent event) {
        if (event.getEntity().level().isClientSide() || !(event.getSource().getEntity() instanceof ServerPlayer player)) return;
        String id = BuiltInRegistries.ENTITY_TYPE.getKey(event.getEntity().getType()).toString();
        if (id.equals("bosses_of_mass_destruction:obsidilith") && !event.getEntity().level().dimension().equals(net.minecraft.world.level.Level.END)) return;
        Integer tier = BOSSES.get(id);
        // The archive contains both legacy holder and platform-specific namespaces.
        // Accept only these three audited Remnant paths in either native namespace.
        if (tier == null && id.startsWith("remnant_bosses:")) tier = BOSSES.get("remnants:" + id.substring(id.indexOf(':') + 1));
        if (tier == null) return;
        var state = player.getPersistentData().getCompound(STATE);
        if (!state.getBoolean(id)) {
            state.putBoolean(id, true);
            state.putBoolean("tier_" + tier, true);
            player.getPersistentData().put(STATE, state);
            grant(player, "ao_campaign:milestones/tier_" + tier);
            if (tier == 6) {
                // Grant access, never force the player's active difficulty higher.
                var advancement = player.server.getAdvancements().get(WorldTier.PINNACLE.getUnlockAdvancement());
                if (advancement != null) for (String criterion : player.getAdvancements().getOrStartProgress(advancement).getRemainingCriteria())
                    player.getAdvancements().award(advancement, criterion);
            }
            String grade = tier == 6 ? "artifact" : tier == 7 ? "heirloom" : tier == 8 ? "esoteric" : null;
            // One gem per player per grade milestone, not one for every farmed kill.
            if (grade != null && !state.getBoolean(grade + "_reward")) {
                ItemStack gem = BossGems.create(player, grade);
                if (!gem.isEmpty()) {
                    if (!player.addItem(gem)) player.drop(gem, false);
                    state.putBoolean(grade + "_reward", true);
                    player.getPersistentData().put(STATE, state);
                    grant(player, "ao_campaign:milestones/" + grade + "_reward");
                } else player.sendSystemMessage(Component.literal("The " + grade + " reward could not resolve. It remains unclaimed."));
            }
            if (id.equals("irons_spellbooks:fire_boss")) grant(player, "ao_campaign:milestones/tyros");
            if (id.equals("cataclysm:scylla")) grant(player, "ao_campaign:milestones/scylla");
            if (id.equals("bosses_of_mass_destruction:obsidilith")) grant(player, "ao_campaign:milestones/obsidilith");
            player.sendSystemMessage(Component.literal("Journal milestone recorded: Tier " + tier + "."));
        }
    }
    public static void grant(ServerPlayer player, String id) {
        var advancement = player.server.getAdvancements().get(ResourceLocation.parse(id));
        if (advancement != null) for (String c : player.getAdvancements().getOrStartProgress(advancement).getRemainingCriteria())
            player.getAdvancements().award(advancement, c);
    }
    private void commands(RegisterCommandsEvent event) {
        event.getDispatcher().register(Commands.literal("ao_mastery").then(Commands.literal("upgrade").executes(ctx -> {
            var player = ctx.getSource().getPlayerOrException();
            var state = player.getPersistentData().getCompound(STATE);
            ItemStack held = player.getMainHandItem();
            if (!state.getBoolean("tier_8") || !state.getBoolean("irons_spellbooks:fire_boss") || !state.getBoolean("cataclysm:scylla") || !state.getBoolean("bosses_of_mass_destruction:obsidilith")) {
                ctx.getSource().sendFailure(Component.literal("Defeat a Tier 8 encounter, Tyros, Scylla and Obsidilith first.")); return 0;
            }
            if (state.getBoolean("heirloom_claimed")) { ctx.getSource().sendFailure(Component.literal("Your mastery upgrade has already been used.")); return 0; }
            var target = RarityRegistry.INSTANCE.getValue(ResourceLocation.parse("ao_apotheotic_port:heirloom"));
            var current = held.get(Apoth.Components.RARITY);
            if (held.getCount() != 1 || target == null || current == null || !current.isBound()
                || held.getOrDefault(Apoth.Components.AFFIXES, ItemAffixes.EMPTY).isEmpty()
                || current.get().sortIndex() >= target.sortIndex()) {
                ctx.getSource().sendFailure(Component.literal("Hold one affixed equipment item below Heirloom rarity.")); return 0;
            }
            // One synchronous server transaction: no /give, no replacement item and no reroll.
            AffixHelper.setRarity(held, target);
            state.putBoolean("heirloom_claimed", true);
            player.getPersistentData().put(STATE, state);
            player.containerMenu.broadcastChanges();
            grant(player, "ao_campaign:milestones/heirloom_upgrade");
            ctx.getSource().sendSuccess(() -> Component.literal("Your held item is now Heirloom. Its existing components are preserved."), false);
            return 1;
        })));
    }
}
