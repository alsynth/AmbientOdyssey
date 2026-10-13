"""CRC, candidate identity and byte-exact rollback validation for the config kit."""
import argparse,hashlib,json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def validate(kit, repeat=None):
    with zipfile.ZipFile(kit) as z:
        assert z.testzip() is None,'ZIP CRC error'
        assert 'manifest.json' not in z.namelist(),'Kit must not masquerade as full import'
        assert not any(n.endswith('.jar') or '..' in Path(n).parts for n in z.namelist())
        for side in ('candidate','rollback'):
            path=side+'/config/dungeon_difficulty/difficulty_v2.json'
            assert z.read(path)==(ROOT/'experiments/structure-difficulty-v3'/path).read_bytes(),side+' bytes differ'
        c=json.loads(z.read('candidate/config/dungeon_difficulty/difficulty_v2.json'))
        summary=json.loads(z.read('evidence/SUMMARY.json'))
        assert sum(len(d['zones']) for d in c['dimensions'])==summary['zones']
        assert summary['runtime_tested'] is False
        assert hashlib.sha256(z.read('rollback/config/dungeon_difficulty/difficulty_v2.json')).hexdigest()==summary['rollback_sha256']
    if repeat:assert kit.read_bytes()==repeat.read_bytes(),'Rebuild is not byte-identical'
    return {'status':'PASS_STATIC_KIT_ONLY','sha256':hashlib.sha256(kit.read_bytes()).hexdigest(),'zip_crc':'PASS','candidate_and_rollback_identity':'PASS','byte_identical_rebuild':'PASS' if repeat else 'NOT_RUN','runtime_tested':False}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('kit',type=Path);p.add_argument('--repeat',type=Path);p.add_argument('--report',type=Path);a=p.parse_args();result=validate(a.kit,a.repeat)
    if a.report:a.report.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))
