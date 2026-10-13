import com.google.gson.Gson;
import net.dungeon_difficulty.config.Config;
import java.nio.file.Files;
import java.nio.file.Path;

/** Uses the exact installed config classes; no Minecraft execution or sanitization. */
public class DDV3SchemaProbe {
    public static void main(String[] args) throws Exception {
        Config config = new Gson().fromJson(Files.readString(Path.of(args[0])), Config.class);
        if (config.dimensions.length == 0 || config.difficulty_types.size() != 7)
            throw new IllegalStateException("Missing dimension/type data");
        int zones = 0;
        for (var dimension : config.dimensions) {
            zones += dimension.zones.size();
            for (var zone : dimension.zones) {
                if (zone.difficulty.level != 1 || zone.zone_matches.structure == null)
                    throw new IllegalStateException("Invalid structure rule");
            }
        }
        if (config.per_player_difficulty.enabled || config.player_effects.enabled)
            throw new IllegalStateException("Unexpected global effects");
        System.out.println("PASS exact installed DD 3.9.2 Gson schema: " + zones + " zones, 7 types; not a Minecraft runtime test");
    }
}
