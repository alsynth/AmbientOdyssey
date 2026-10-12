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
        // Fail closed: an invalid or unsupported exact tier yields a zero-effect modifier, never an exception
        // (this runs in attribute recalculation and tooltips) and never a higher tier than native purity allows.
        var tier = LegacyGem.resolveTier(gem.gemStack(), gem.purity(), this::supportsTier);
        double amount = tier.isPresent() ? legacyValues.get(LegacyGem.TIERS[tier.getAsInt()]) : 0.0;
        return new AttributeModifier(makeUniqueId(gem), amount, operation);
    }

    public boolean supportsTier(int tier) {
        return tier >= 0 && tier <= 8 && legacyValues.containsKey(LegacyGem.TIERS[tier]);
    }

    @Override public Codec<? extends GemBonus> getCodec() { return CODEC; }
}
