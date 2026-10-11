# Luki's Woodland Mansions + Dungeons & Taverns key appearance

**11 October 2026 — implemented in the Mine Cells WORKING control branch derivative; no new mods required.**

The pack already installs official Luki's Woodland Mansions `mr_lukis_woodlandmansions` (CurseForge project 1385782, file 7227735) and Dungeons & Taverns `mr_dungeons_andtaverns` (project 853794, file 5768823) as NeoForge mod JARs. The client log `latest(20261010-232036).log` explicitly shows both mod IDs in `Reloading ResourceManager`, meaning NeoForge already makes their `assets/` available through `Mod Resources`. The original author's suggestion to put a **datapack** in both datapacks and resourcepacks is not applicable to this already-installed **mod** packaging. Do not install a second duplicate JAR/resourcepack: it can worsen key-model priority conflicts and risks redistributing author-owned assets.

### Actual collision (reproduced from upstream exact versions)
- Luki mod v1.0+mod, official upstream Modrinth `RZN5D3zs/1fEmTmPi` SHA256 `61c477cbe76847a204157c92b944438edc610abd91c71aff1ab7e58aca3a1e65`: `assets/minecraft/models/item/trial_key.json` and `ominous_trial_key.json` define models for mansion (6161), ravager (6162), stronghold (6767), dragon (6768).
- Dungeons & Taverns v4.4.4+mod (NeoForge), official Modrinth `tpehi7ww/BYUUUeZA` SHA256 `1db28e89e0cb76aebe9e40955d1866e8ac1779575d15c2a1e250ac804a762d05` defines its own 15 custom trial/ominous key models with IDs 711–723, *using the exact same two base model JSON paths*.
- Minecraft resource-pack precedence overwrites files instead of combining model overrides. Without a merged model, whichever mod's `trial_key.json` wins hides custom textures from the other. This affects visuals, not key functionality.

### Fix
Add two **JSON-only** routing files to AO's independent Paxi key-compat resource pack at:
`config/paxi/resourcepacks/ao_lukis_dnt_key_compat/assets/minecraft/models/item/trial_key.json`
and `ominous_trial_key.json`.

Merge and sort all source authors' `custom_model_data` override values, keep Dungeons & Taverns' parent, default textures and display transformations. All 19 custom key model entries reference the original mods' `assets/minecraft/models/item/keys/*.json` and their already-loaded textures. **No author-owned .png, .jar, or .nbt is embedded or duplicated**, and worldgen/loot/gameplay are untouched.

### Tests / limitations
- This independent pack cannot be erased by the AO resource-repair compiler. The merged model IDs and exact source project versions are statically validated in `tools/validate_v041_lukis_dnt_keys.py`; ZIP validator confirms they reach final CurseForge import package.
- The `Mine Cells Structure Control` branch remains our proven gameplay baseline with **Streams Reflowing, Noisiumed and Structure Essentials** absent; the derived key-compatible test ZIP maintains these exclusions and retains working Mine Cells. No Streams reintroduction in this change.
- Client rendering cannot be tested in Actions. In-game confirm both Luki Mansion/Ravager Keys and some Dungeons & Taverns trial/ominous keys retain distinct custom textures. Confirm `ao_lukis_dnt_key_compat` appears active.
- If another mod defines the same exact vanilla key models, it may need inclusion in AO's merged JSON as well; do not claim a global complete key override audit without binary evidence.
- User reports **both `fastChunkLoading = false` and `streamBiomeBlacklist` failed to resolve Streams Reflowing/Mine Cells conflict**. Mark config-only hypothesis FAILED. A proper dimension-aware source patch or leaving Streams removed is required; no further guesswork with blacklists. 

Sources:
- https://www.curseforge.com/minecraft/mc-mods/lukis-woodland-mansions
- https://modrinth.com/datapack/lukis-woodland-mansions/version/1fEmTmPi
- https://modrinth.com/datapack/dungeons-and-taverns/version/BYUUUeZA
