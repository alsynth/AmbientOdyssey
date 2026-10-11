"""Check the actual development JAR's model/texture graph and distribution notices."""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import zipfile


def validate(jar: Path):
    with zipfile.ZipFile(jar) as archive:
        files = set(archive.namelist())
        assert archive.testzip() is None, "Corrupt JAR entry"
        assert 'LICENSE' in files and 'NOTICE.md' in files, "Distribution notices missing"
        metadata = archive.read('META-INF/neoforge.mods.toml').decode()
        assert 'license="GPL-3.0-only"' in metadata, "Incorrect distribution license"
        assert not any(name.startswith('data/minecraft/worldgen/') for name in files), "Vanilla worldgen replacement is forbidden"
        models = [name for name in files if name.startswith('assets/ao_wet_sand/models/') and name.endswith('.json')]
        for name in models:
            model = json.loads(archive.read(name))
            parent = model.get('parent', '')
            if parent.startswith('ao_wet_sand:'):
                assert f"assets/ao_wet_sand/models/{parent.split(':', 1)[1]}.json" in files, f"Missing parent in {name}"
            for texture in model.get('textures', {}).values():
                if texture.startswith('ao_wet_sand:'):
                    path = f"assets/ao_wet_sand/textures/{texture.split(':', 1)[1]}.png"
                    assert path in files, f"Missing texture for {name}"
                    png = archive.read(path)
                    assert png[:8] == b'\x89PNG\r\n\x1a\n' and struct.unpack('>II', png[16:24]) == (16, 16), f"Invalid block texture {path}"
        blockstates = [name for name in files if name.startswith('assets/ao_wet_sand/blockstates/') and name.endswith('.json')]
        assert len(blockstates) == 9, "Expected nine moisture block states"
        for name in blockstates:
            for variant in json.loads(archive.read(name))['variants'].values():
                path = f"assets/ao_wet_sand/models/{variant['model'].split(':', 1)[1]}.json"
                assert path in files, f"Unresolved blockstate model in {name}"
            block = Path(name).stem
            assert f'assets/ao_wet_sand/models/item/{block}.json' in files, f"Missing item model for {block}"
            assert f'data/ao_wet_sand/loot_table/blocks/{block}.json' in files, f"Missing loot table for {block}"
        provenance = json.loads(archive.read('assets/ao_wet_sand/texture-provenance.json'))
        for name, expected in provenance['sha256'].items():
            actual = hashlib.sha256(archive.read('assets/ao_wet_sand/textures/block/' + name)).hexdigest()
            assert actual == expected, f"Upstream texture altered without provenance update: {name}"
        return {'status': 'PASS', 'blockstates': len(blockstates), 'models': len(models), 'upstream_textures': len(provenance['sha256']),
                'runtime_client_verified': False, 'jar_sha256': hashlib.sha256(jar.read_bytes()).hexdigest()}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('jar', type=Path)
    print(json.dumps(validate(parser.parse_args().jar), indent=2))
