#!/usr/bin/env python3
"""Generate an exact Goblin Traders 1.21.1 epic-trade datapack override.

Reads the ACTUAL pinned Goblin Traders JAR; copies its generated trade JSON,
modifying only two payment fields for the four Goblin-Tuned chainmail offers.
Fails closed on a missing/mismatched trade format or output item components.
Does not redistribute a mod JAR or overwrite existing releases.
"""
import argparse
import json
import pathlib
import zipfile

NATIVE = "data/goblintraders/goblin_trades/goblin_trader/epic.json"
ARMOR = {
    "minecraft:chainmail_helmet", "minecraft:chainmail_chestplate",
    "minecraft:chainmail_leggings", "minecraft:chainmail_boots",
}

def transform(trades):
    if not isinstance(trades, dict) or not isinstance(trades.get("trades"), list):
        raise ValueError("Unrecognized native JSON structure: expected object with trades list")
    changed = set()
    for t in trades["trades"]:
        if not isinstance(t, dict):
            continue
        output = t.get("offer_item", {})
        if not isinstance(output, dict):
            continue
        item = output.get("id")
        if item not in ARMOR:
            continue
        if item in changed:
            raise ValueError(f"Duplicate tuned offer: {item}")
        components = output.get("components", {})
        if not isinstance(components, dict) or not {"minecraft:attribute_modifiers", "minecraft:max_damage"} <= set(components):
            raise ValueError(f"Expected original Goblin-Tuned attribute and durability components missing for {item}")
        if t.get("max_trades") != 1:
            raise ValueError(f"Unexpected max_trades for {item}")
        if not isinstance(t.get("payment_item"), dict) or not isinstance(t.get("secondary_payment_item"), dict):
            raise ValueError(f"Unexpected original price schema for {item}")
        t["payment_item"] = {"id": "minecraft:diamond", "count": 32}
        t["secondary_payment_item"] = {"id": "irons_spellbooks:cinder_essence", "count": 4}
        changed.add(item)
    if changed != ARMOR:
        raise ValueError(f"Only matched {sorted(changed)}; expected {sorted(ARMOR)}")
    return trades

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("jar", help="Installed official Goblin Traders JAR, pinned for AO (1.21.1 / 1.11.2)")
    parser.add_argument("--output", default="build/ao-goblin-trade-overrides")
    args = parser.parse_args()
    with zipfile.ZipFile(args.jar) as z:
        if NATIVE not in z.namelist():
            raise ValueError(f"Native trade JSON not found: {NATIVE}")
        native = json.loads(z.read(NATIVE))
    altered = transform(native)
    folder = pathlib.Path(args.output)
    dest = folder / NATIVE
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(altered, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (folder / "pack.mcmeta").write_text(json.dumps(
        {"pack": {"pack_format": 48, "description": "AO: tuned chainmail 32 diamonds + 4 Cinder Essence"}},
        indent=2) + "\n", encoding="utf-8")
    print(f"Validated 4 chainmail Goblin-Tuned trade overrides: {dest}")
    print("Copy generated files to a Paxi datapack only AFTER registry/runtime tests. Original trades preserved.")

if __name__ == "__main__":
    main()
