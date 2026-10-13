import com.google.gson.GsonBuilder;
import java.util.Map;
import java.util.TreeMap;
/** Read constant maps only. Does not invoke config bootstrap or write game files. */
public class RemnantV270DefaultsProbe {
    public static void main(String[] args) throws Exception {
        Map<String,Object> maps = new TreeMap<>();
        for (String name : new String[]{"BoneMonsterConfig", "SovereignConfig"}) {
            Class<?> type = Class.forName("com.nightbeam.remnants.config." + name);
            maps.put(name, type.getField("DEFAULTS").get(null));
        }
        System.out.println(new GsonBuilder().setPrettyPrinting().create().toJson(maps));
    }
}
