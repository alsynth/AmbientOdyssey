package dev.ambientodyssey.ports.apotheotic;

import java.util.Map;
import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import dev.shadowsoffire.apotheosis.socket.gem.GemClass;
import dev.shadowsoffire.apotheosis.socket.gem.GemView;
import dev.shadowsoffire.apotheosis.socket.gem.Purity;
import dev.shadowsoffire.apotheosis.socket.gem.bonus.AttributeBonus;
import dev.shadowsoffire.apotheosis.socket.gem.bonus.GemBonus;
import dev.shadowsoffire.placebo.codec.PlaceboCodecs;
import net.minecraft.core.Holder;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.world.entity.ai.attributes.Attribute;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;

public final class LegacyAttributeBonus extends AttributeBonus {
    public static final Codec<LegacyAttributeBonus> CODEC = RecordCodecBuilder.create(i -> i.group(
        GemClass.CODEC.fieldOf("gem_class").forGetter(b -> b.gemClass),
        BuiltInRegistries.ATTRIBUTE.holderByNameCodec().fieldOf("attribute").forGetter(b -> b.attribute),
        PlaceboCodecs.enumCodec(AttributeModifier.Operation.class).fieldOf("operation").forGetter(b -> b.operation),
        Codec.unboundedMap(Codec.STRING, Codec.DOUBLE).fieldOf("legacy_values").forGetter(b -> b.legacyValues)
    ).apply(i, LegacyAttributeBonus::new));
    private final Map<String, Double> legacyValues;

    public LegacyAttributeBonus(GemClass gemClass, Holder<Attribute> attr, AttributeModifier.Operation op, Map<String, Double> values) {
        super(gemClass, attr, op, Map.of());
        if (values.isEmpty() || values.keySet().stream().anyMatch(k -> !java.util.List.of(LegacyGem.TIERS).contains(k)))
            throw new IllegalArgumentException("Unknown or empty legacy tier values");
        legacyValues = Map.copyOf(values);
    }

    @Override public boolean supports(Purity purity) {
        if (purity.ordinal() < 5) return legacyValues.containsKey(LegacyGem.TIERS[purity.ordinal()]);
        return java.util.stream.IntStream.rangeClosed(5, 8).anyMatch(t -> legacyValues.containsKey(LegacyGem.TIERS[t]));
    }

    @Override public AttributeModifier createModifier(GemView gem) {
        int tier = LegacyGem.tier(gem.gemStack(), gem.purity());
        if (!gem.gemStack().has(ApotheoticPort.LEGACY_GEM_TIER.get()) && tier == 5 && !supportsTier(tier))
            tier = java.util.stream.IntStream.rangeClosed(6, 8).filter(this::supportsTier).findFirst().orElse(5);
        if (tier < 0 || tier > 8 || !legacyValues.containsKey(LegacyGem.TIERS[tier]))
            throw new IllegalArgumentException("Gem has no bonus at its exact legacy tier");
        return new AttributeModifier(makeUniqueId(gem), legacyValues.get(LegacyGem.TIERS[tier]), operation);
    }

    public boolean supportsTier(int tier) {
        return tier >= 0 && tier <= 8 && legacyValues.containsKey(LegacyGem.TIERS[tier]);
    }

    @Override public Codec<? extends GemBonus> getCodec() { return CODEC; }
}
