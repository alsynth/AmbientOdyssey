# Ambient Odyssey — 0.4f historical audit addendum

**Experimental; no client/server gameplay certification.** Seven new native NeoForge 1.21.1 project pins added to the successful 302-ref predecessor; expected **309 CF refs**, native 273 worldgen repairs retained. Sources below are exact official CF file pages, NOT loose redistributed JARs.

| Addition | CF project:file | Risk/acceptance |
|---|---|---|
| Armor Trim Item Fix | [895603:5924310](https://www.curseforge.com/minecraft/mc-mods/armor-trim-item-fix/files/5924310) | client cosmetic, explicitly requested |
| Shulker Box Tooltip | [315811:6530833](https://www.curseforge.com/minecraft/mc-mods/shulkerboxtooltip/files/6530833) | storage previews; check Better Inventory overlap |
| Crafting Tweaks | [233071:8697050](https://www.curseforge.com/minecraft/mc-mods/crafting-tweaks/files/8697050) | rotate/clear/balance crafting grid; keybind conflicts later |
| Chat Heads | [407206:7057837](https://www.curseforge.com/minecraft/mc-mods/chat-heads/files/7057837) | client chat identity |
| Sound Physics Remastered | [535489:7032247](https://www.curseforge.com/minecraft/mc-mods/sound-physics-remastered/files/7032247) | reverb and occlusion; verify Atmosfera/Waves overlap |
| Polymorph | [388800:6794589](https://www.curseforge.com/minecraft/mc-mods/polymorph/files/6794589) | recipe collision selector; ensure UI works with JEI |
| Brewin' And Chewin' | [637808:8309583](https://www.curseforge.com/minecraft/mc-mods/brewin-and-chewin/files/8309583) | Farmer's Delight fermentation and serving gameplay |

Sound Physics and Atmosfera are different types of audio mods, but water echoes, rain/shore ambience and overhead birds must be listened to before defaulting aggressive reverb. Polymorph and Shulker previews need JEI/Better Inventory integration tests; Crafting Tweaks adds binds pending keybind overhaul. Brewin's 4.5.0 requires Farmer's Delight 1.3.2 or newer, and baseline already contains FD 1.3.4 in the previously verified client log. No unapproved Fabric/CTM/LOD/skill tree substitutions.

**Inherited duplicate closure:** Clumps 256717:5623731 was already present in the historical Test4 manifest (237 CF projects) and in the current baseline, so it is deliberately **not** an additional CF reference. Current source keeps baseline Clumps unchanged; it was never a newly added mod in this wave. Total 302 + seven new = **309 CF refs**.
