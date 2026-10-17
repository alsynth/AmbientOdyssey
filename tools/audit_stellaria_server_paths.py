#!/usr/bin/env python3
"""Static server-boundary audit for the checked Stellaria source tree.

This is source triage only. It does not prove runtime behavior or loader compatibility.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

def props_line(text: str, key: str) -> str | None:
    for line in text.splitlines():
        if line.strip().startswith(key + "="):
            return line.split("=", 1)[1].strip()
    return None

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("stellaria_root", type=Path)
    root = parser.parse_args().stellaria_root
    src = root / "src/main/java/com/keko/stellaria"

    def read(relative: str) -> str:
        return (src / relative).read_text(encoding="utf-8")

    entry = read("Stellaria.java")
    glide = read("logic/movement/StellarGlide.java")
    server_net = read("packet/networking/ModMessagesServer.java")
    artha = read("stellarEvent/artha/ArthaDimensionHandler.java")
    zregos = read("entity/boss/zregos/Zregos.java")
    einfarbig = read("entity/boss/einfarbig/Einfarbig.java")
    meta = json.loads((root / "src/main/resources/fabric.mod.json").read_text(encoding="utf-8"))
    props = (root / "gradle.properties").read_text(encoding="utf-8")

    checks = [
        {
            "id": "glide_calls_client_animation_from_server_payload",
            "severity": "blocker_candidate",
            "evidence": "ModMessagesServer registers an Artha movement C2S receiver that calls StellarGlide.glidePLayer; StellarGlide directly references HandleAnimICANTTAKEITANYMORE.",
            "present": "StellarGlide.glidePLayer" in server_net and "HandleAnimICANTTAKEITANYMORE" in glide,
        },
        {
            "id": "server_tick_calls_veil_client_easing",
            "severity": "blocker_candidate",
            "evidence": "Stellaria registers ArthaDimensionHandler.tick on START_SERVER_TICK; that method invokes foundry.veil.api.client.util.Easing.",
            "present": "ArthaDimensionHandler.tick(level_artha)" in entry and "Easing.EASE_OUT_CUBIC.ease" in artha,
        },
        {
            "id": "boss_entity_has_client_render_calls",
            "severity": "blocker_candidate",
            "evidence": "Zregos serverTick calls its particle path; spawnParticle directly uses VeilRenderSystem renderer APIs.",
            "present": "handleThoseFuckingParticlesThatIHate();" in zregos and "VeilRenderSystem.renderer()" in zregos,
        },
        {
            "id": "common_boss_class_references_client_api",
            "severity": "needs_side_split_review",
            "evidence": "Einfarbig is a common entity class with Veil client-render fields/calls and Minecraft references; clientTick is guarded by level().isClientSide, but class loading still needs dedicated-server validation.",
            "present": "private void clientTick()" in einfarbig and "foundry.veil.api.client" in einfarbig and "net.minecraft.client.Minecraft" in einfarbig,
        },
    ]
    result = {
        "scope": "static source inspection only",
        "mod_id": meta.get("id"),
        "source_version": props_line(props, "mod_version") if meta.get("version") == "${version}" else meta.get("version"),
        "minecraft": meta.get("depends", {}).get("minecraft"),
        "loader": props_line(props, "loader_version"),
        "mod_version": props_line(props, "mod_version"),
        "checks": checks,
        "runtime_verified": False,
    }
    print(json.dumps(result, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
