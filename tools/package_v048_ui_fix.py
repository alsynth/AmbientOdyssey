"""Package a config-only UI update, preserving the exact consolidated v048 payload."""
import argparse
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

BASE_SHA = 'b0f506a1192d4e2e66a577872e78af68e8383c7df2c03d9d16b578c059cc2ebe'
CONFIGS = ['legendarytooltips.toml', 'equipmentcompare.toml',
           'simplytooltips/config.toml', 'wover/client.json']
README = '''Close Minecraft before installing.

For your existing v048 profile: extract this kit, double-click INSTALL.cmd,
then select the profile folder. The updater backs up existing settings and
changes only the specified UI settings. Mods, worlds and gem content stay intact.

BetterEnd/WorldWeaver welcome and update popups are skipped.
SimplyTooltips handles vanilla and modded item descriptions, with a bounded
body and mouse-wheel scrolling. Tabs are disabled so affix details share one view.
Legendary Tooltips borders/item previews and
Equipment Compare panels are temporarily disabled to avoid competing renderers.
Their mods stay installed. No key bindings are changed.

Apotheotic Additions log errors are recorded but deferred to its ongoing work.
'''


def archive(path, members):
    path.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(path, 'w', compression=ZIP_DEFLATED) as z:
        for name, data in sorted(members.items()):
            info = ZipInfo(name, (2026, 10, 12, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            z.writestr(info, data)
    with ZipFile(path) as z:
        assert z.testzip() is None and len(z.namelist()) == len(members)
        for name, data in members.items():
            assert z.read(name) == data, name
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(a):
    root = Path(__file__).resolve().parents[1]
    assert hashlib.sha256(a.base.read_bytes()).hexdigest() == BASE_SHA
    configs = {name: (root/'release_030/overrides/config'/name).read_bytes() for name in CONFIGS}
    kit = {'config/'+name: data for name, data in configs.items()}
    kit['INSTALL.ps1'] = (root/'tools/install_tooltip_startup_fix.ps1').read_bytes()
    kit['INSTALL.cmd'] = b'@echo off\r\npowershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0INSTALL.ps1"\r\npause\r\n'
    kit['READ_FIRST.txt'] = README.encode('utf-8')
    kit_sha = archive(a.output/'Ambient-Odyssey-v048-UI-FIX-KIT.zip', kit)
    with ZipFile(a.base) as z:
        original = {n: z.read(n) for n in z.namelist()}
    full = dict(original)
    manifest = json.loads(full['manifest.json'])
    manifest['name'] = 'Ambient Odyssey v0.4.8.1 - Tooltip and Startup Fix TEST'
    manifest['version'] = '0.4.8.1-tooltip-startup-fix-test'
    full['manifest.json'] = (json.dumps(manifest, indent=2)+'\n').encode('utf-8')
    full.update({'overrides/config/'+name: data for name, data in configs.items()})
    full['overrides/AO_TEST_NOTES/UI_FIX.txt'] = README.encode('utf-8')
    changed = {'manifest.json'} | {'overrides/config/'+name for name in CONFIGS}
    for name, data in original.items():
        if name not in changed:
            assert full[name] == data, name
    assert manifest['files'] == json.loads(original['manifest.json'])['files']
    full_sha = archive(a.output/'Ambient-Odyssey-v0.4.8.1-FULL-UI-FIX-TEST.zip', full)
    report = {'base_sha256': BASE_SHA, 'kit_sha256': kit_sha, 'full_sha256': full_sha,
              'unchanged_mod_pins': len(manifest['files']), 'prototype_jar_unchanged': True}
    (a.output/'V048_UI_FIX_INPUTS.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--base', type=Path, required=True)
    p.add_argument('--output', type=Path, default=Path('build'))
    main(p.parse_args())
