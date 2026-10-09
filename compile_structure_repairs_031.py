#!/usr/bin/env python3
"""Compile only evidence-backed template-pool repairs from editable inputs."""
import json,shutil,hashlib
from pathlib import Path
from nbt_audit_031 import migrate_waystone_jigsaw
ROOT=Path(__file__).resolve().parent
RELEASE=ROOT/'release_030'
PACK=RELEASE/'overrides/config/paxi/datapacks/ao_structure_repairs'

def compile_repairs():
 plan=json.loads((RELEASE/'structure-repairs.json').read_text())
 if (PACK/'data').exists():shutil.rmtree(PACK/'data')
 PACK.mkdir(parents=True,exist_ok=True)
 (PACK/'pack.mcmeta').write_text(json.dumps({'pack':{'pack_format':48,'description':'Ambient Odyssey: verified native template-pool repairs'}},indent=2)+'\n', newline='\n')
 for id,payload in plan['template_pools'].items():
  assert payload['elements'],id
  assert any(e['element']['element_type']!='minecraft:empty_pool_element' for e in payload['elements']),id
  ns,name=id.split(':',1);path=PACK/'data'/ns/'worldgen/template_pool'/(name+'.json')
  path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(payload,indent=2)+'\n', newline='\n')
 for id,payload in plan.get('recipes',{}).items():
  ns,name=id.split(':',1);path=PACK/'data'/ns/'recipe'/(name+'.json')
  path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(payload,indent=2)+'\n', newline='\n')
 for category,rows in plan.get('additional_resources',{}).items():
  assert category in {'tags/entity_type','tags/item','loot_modifiers','loot_table'}
  for id,payload in rows.items():
   ns,name=id.split(':',1);path=PACK/'data'/ns/category/(name+'.json')
   path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(payload,indent=2)+'\n', newline='\n')
 for id,entry in plan.get('template_migrations',{}).items():
  raw=(RELEASE/entry['source']).read_bytes()
  assert hashlib.sha256(raw).hexdigest()==entry['source_sha256'],id
  assert entry['operation']=='waystone_jigsaw_1_21_1'
  ns,name=id.split(':',1);path=PACK/'data'/ns/'structure'/(name+'.nbt')
  path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(migrate_waystone_jigsaw(raw))
 resource_pack=RELEASE/'overrides/config/paxi/resourcepacks/ao_resource_repairs'
 if (resource_pack/'assets').exists():shutil.rmtree(resource_pack/'assets')
 resource_pack.mkdir(parents=True,exist_ok=True)
 (resource_pack/'pack.mcmeta').write_text(json.dumps({'pack':{'pack_format':34,'description':'Ambient Odyssey: native Traveloptics resource repairs'}},indent=2)+'\n', newline='\n')
 for name,payload in plan.get('client_models',{}).items():
  assert name.startswith('assets/traveloptics/models/') and name.endswith('.json') and '..' not in Path(name).parts
  path=resource_pack/name;path.parent.mkdir(parents=True,exist_ok=True)
  path.write_text(json.dumps(payload,indent=2)+'\n', newline='\n')
 print('Structure assembly:',len(plan['template_pools']),'nonempty native-asset pool repairs')

if __name__=='__main__':compile_repairs()
