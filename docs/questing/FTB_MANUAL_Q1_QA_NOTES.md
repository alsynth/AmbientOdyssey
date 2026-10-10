# FTB Manual Q1 CI preflight notes

- First CI found that generic SNBT parsers require comma separators, unlike FTB's export; normalizer only affects in-memory validation.
- Next CI found that all control pages lacked the standard disclaimer about non-reward reference material. Their introductory text was corrected.
- Neither outcome reflects an actual Minecraft/Fabric/NeoForge runtime test; real client testing remains pending.
