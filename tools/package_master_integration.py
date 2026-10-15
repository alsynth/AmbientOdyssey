"""Build the private integration from the exact PR50 base and freshly compiled addons."""
import argparse, contextlib, hashlib, io, json, subprocess, tempfile, zipfile
from pathlib import Path
import package_ao_full_pr54 as prior
from ao_pregen_remove_skyarena import omit_demis_sky_arena

ROOT=Path(__file__).resolve().parents[1]
def digest(data):return hashlib.sha256(data).hexdigest()
def build(base,output):
    base,output=Path(base),Path(output)
    if output.exists():raise ValueError('Never overwrite an existing candidate')
    libs=ROOT/'addons'
    starter=libs/'ao-starter-chest/build/libs/ao-starter-chest-0.2.0-experimental.jar'
    sigils=libs/'ao-augmenting-sigils/build/libs/ao-augmenting-sigils-0.1.1-experimental.jar'
    campaign=libs/'ao-campaign/build/libs/ao-campaign-0.2.0-experimental.jar'
    (ROOT/'build').mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(dir=ROOT/'build') as tmp:
        with contextlib.redirect_stdout(io.StringIO()):prior.build(base,starter,sigils,Path(tmp)/'prior.zip',campaign)
        with zipfile.ZipFile(Path(tmp)/'prior.zip') as z:payload={n:z.read(n) for n in z.namelist() if not n.endswith('/')}
    baseline=dict(payload)
    report_root=ROOT/'docs/handoffs/integration-20261015'
    ledger=json.loads((report_root/'native-balance-ledger.json').read_text())
    paths={r['path'] for r in ledger}|{'config/brutalbosses.json','config/dungeon_difficulty/difficulty_v2.json',
      'defaultconfigs/irons_spellbooks-server.toml','defaultconfigs/block_factorys_bosses-server.toml'}
    for rel in paths:payload['overrides/'+rel]=(ROOT/'release_030/overrides'/rel).read_bytes()
    for rel in json.loads((report_root/'removed-source-paths.json').read_text()):payload.pop('overrides/'+rel,None)
    manifest=json.loads(payload['manifest.json']);manifest['files'],removed=omit_demis_sky_arena(manifest['files']);assert removed==1
    manifest['name']='Ambient Odyssey - Master Integration PRIVATE TEST'
    manifest['version']='0.5.1-master-integration-20261015'
    payload['manifest.json']=(json.dumps(manifest,indent=2)+'\n').encode()
    # Correct the runtime inventory as well as the importer manifest.
    name='overrides/AO_TEST_NOTES/FULL_IMPORT_INPUTS.json'
    inputs=json.loads(payload[name]);inputs['roster']=[r for r in inputs['roster'] if r['name']!='SkyArena-1.3.6-1.21.1.jar']
    inputs['integration_note']='SkyArena removed by owner issue 58; historical counts below may describe PR50'
    payload[name]=(json.dumps(inputs,indent=2)+'\n').encode()
    # Remove misleading prototype notes from inherited package; keep their hashes in the change receipt.
    for name in ['overrides/AO_TEST_NOTES/FULL_PR54.txt']:
        payload.pop(name,None)
    notes=('PRIVATE TEST ONLY. New CurseForge profile, Minecraft 1.21.1 / NeoForge 21.1.252.\n'
      '337 CurseForge references, 10 custom JARs, expected 340 physical mod JARs.\n'
      '23 scoped DD zones; exact 497-row expansion remains gated. Brutal Bosses 70/30/x4 HP/x3 damage.\n'
      '51 native boss config fields changed; HP cap accepted, scripted abilities not promised scaled.\n'
      'T5 Chesed/Malkuth/Geburah exempt; Dead King/Cornelia T6 category and T7 combat targets.\n'
      'Cornelia combat has no verified native config and remains BLOCKED, no competing scaler.\n'
      'Rage Glove experimental gate disabled; native acquisition retained pending owner selection.\n'
      'Preserves PR51 starter, trade and ring integrations, Sigils and world-tier rarity candidate.\n'
      'Mastery retains campaign gates; natural fights, Lootr two-player rolls and pregen remain manual.\n'
      'This ZIP is not a worldgen freeze or live install. See supplied verification and test guide.\n')
    payload['overrides/AO_TEST_NOTES/MASTER_INTEGRATION.txt']=notes.encode()
    payload['overrides/AO_TEST_NOTES/NATIVE_BALANCE_LEDGER.json']=(report_root/'native-balance-ledger.json').read_bytes()
    # Package rollback is byte-exact for every replaced/removed payload, never a full-version overwrite.
    changed={n:{'before_sha256':digest(baseline[n]) if n in baseline else None,'after_sha256':digest(payload[n]) if n in payload else None}
      for n in sorted(set(payload)|set(baseline)) if baseline.get(n)!=payload.get(n)}
    output.parent.mkdir(parents=True,exist_ok=True)
    def write(path,entries):
        with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
            for n,b in sorted(entries.items()):
                info=zipfile.ZipInfo(n,(2026,10,15,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16;z.writestr(info,b)
    write(output,payload)
    rollback=output.with_name(output.stem+'-Rollback.zip')
    if rollback.exists():raise ValueError('Rollback already exists; never overwrite')
    with zipfile.ZipFile(output) as z:
        assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))
        assert not any('probe' in n.lower() and n.endswith('.jar') for n in z.namelist())
    with zipfile.ZipFile(base) as z:original={n:z.read(n) for n in z.namelist() if not n.endswith('/')}
    full_changes={n:{'before_sha256':digest(original[n]) if n in original else None,'after_sha256':digest(payload[n]) if n in payload else None}
      for n in sorted(set(payload)|set(original)) if original.get(n)!=payload.get(n)}
    rollback_payload={n:original[n] for n in full_changes if n in original}
    rollback_payload['ROLLBACK-RECEIPT.json']=json.dumps({'remove_added_paths':[n for n in full_changes if n not in original],
      'restore_basis':'Exact PR50 ZIP payload; restore a separate PR50 profile and its PRE-test save backup. Never apply rollback over a world already generated with different content.','paths':full_changes},indent=2).encode()
    write(rollback,rollback_payload)
    receipt={'base_sha256':digest(base.read_bytes()),'source_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip(),
      'source_tree_has_uncommitted_changes':bool(subprocess.check_output(['git','status','--porcelain'],cwd=ROOT)),
      'zip_sha256':digest(output.read_bytes()),'rollback_sha256':digest(rollback.read_bytes()),'cf_references':len(manifest['files']),
      'custom_jars':{n:digest(b) for n,b in payload.items() if n.startswith('overrides/mods/') and n.endswith('.jar')},
      'all_members_sha256':{n:digest(b) for n,b in payload.items()},'changed_from_pr50':full_changes,
      'changed_from_intermediate':changed,'runtime_status':'NOT_TESTED_AT_PACKAGING'}
    Path(str(output)+'.report.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({k:v for k,v in receipt.items() if k not in ['changed_from_pr50','changed_from_intermediate','all_members_sha256','custom_jars']},indent=2))
    return receipt
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--base',required=True,type=Path);p.add_argument('--output',required=True,type=Path);a=p.parse_args();build(a.base,a.output)
