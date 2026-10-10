#!/usr/bin/env python3
"""Static v0.4.1 regression checks; not client or gameplay validation."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
L=json.loads((R/'release_030/release-lock.json').read_text())
assert L['version']=='0.4.1-experimental-six-fix-test'
assert L['remove_projects']['rarcompat']==1100379
C=L['additions']['content-041-cardinal-components-api']
assert (C['projectId'],C['id'],C['fileName'],set(C['gameVersions']))==(318449,5845879,'cardinal-components-api-6.1.2.jar',{'1.21.1','Fabric'})
P=R/'release_030/overrides/config/paxi/datapacks/ao_v041_runtime_fixes'
assert json.loads((P/'pack.mcmeta').read_text())['pack']['pack_format']==48
files=list(P.glob('data/*/recipe/**/*.json'))
assert len(files)==19,len(files)
assert all(json.loads(f.read_text())=={'neoforge:conditions':[{'type':'neoforge:false'}]} for f in files)
t=json.loads((R/'release_030/overrides/config/paxi/datapacks/ao_technical_fixes/data/traveloptics/tags/entity_type/element_fire.json').read_text())
assert t['replace'] is True and 'old_netherite_monstrosity' not in json.dumps(t)
assert 'prevent-moving-into-unloaded-chunks: true' in (R/'release_030/overrides/config/servercore/config.yml').read_text()
assert 'double_cake = false' in (R/'release_030/overrides/config/amendments-common.toml').read_text()
assert len(list((R/'release_030/overrides/config/questlog/quests').glob('*.json')))==50
print('PASS v0.4.1 static: CCA/rarcompat, 19 recipe guards, tag, ServerCore, Amendments, Questlog')
