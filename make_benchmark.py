"""Create a manual 180-locate survey matching the completed V3 log roster."""
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parent
STRUCTURES = [
 'dungeons_arise:infested_temple', 'integrated_villages:tavern_village',
 'towns_and_towers:village_forest', 'philipsruins:ancient_towers',
 'graveyard:large_graveyard', 'graveyard:medium_graveyard',
 'idas:pillager_fortress', 'idas:ars_nouveau/archmages_tower', 'idas:ruined_fort',
 'idas:haunted_manor', 'illagerwarship:warship', 'skyarena:ice_arena',
 'dungeons_arise:coliseum', 'dungeons_arise:heavenly_challenger',
 'dungeons_arise:kisegi_sanctuary', 'dungeons_arise:keep_kayra',
 'block_factorys_bosses:sandworm_nest', 'bosses_of_mass_destruction:lich_tower',
 'cataclysm:frosted_prison', 'cataclysm:acropolis']
POINTS = [(0,0),(20000,20000),(20000,-20000),(-20000,20000),(-20000,-20000),
          (40000,0),(-40000,0),(0,40000),(0,-40000)]

def build():
    files = {'pack.mcmeta': json.dumps({'pack': {'pack_format':48,
             'description':'AO manual 9-point / 20-structure survey'}})}
    prefix = 'data/ao_benchmark/function/'
    files[prefix+'start.mcfunction'] = '\n'.join([
        'scoreboard objectives add ao_bench dummy',
        *[f'schedule clear ao_benchmark:step_{i:03}' for i in range(1,181)],
        'scoreboard players set #running ao_bench 1',
        'tellraw @a {"text":"[AO BENCHMARK] 180 locates starting. Record seed/preset/settings; locate results do not measure clipping or density."}',
        'schedule function ao_benchmark:step_001 1s replace'])+'\n'
    files[prefix+'stop.mcfunction'] = 'scoreboard players set #running ao_bench 0\ntellraw @a {"text":"[AO BENCHMARK] Stopped after the current command."}\n'
    number = 0
    for point,(x,z) in enumerate(POINTS,1):
        for step,structure in enumerate(STRUCTURES,1):
            number += 1
            name = f'{number:03}'
            files[prefix+f'step_{name}.mcfunction'] = f'execute if score #running ao_bench matches 1 run function ao_benchmark:work_{name}\n'
            message = [{'text':f'[AO RESULT] point={point} step={step}/20 structure={structure} success='},
                       {'score':{'name':'#success','objective':'ao_bench'}},
                       {'text':' distance='},{'score':{'name':'#distance','objective':'ao_bench'}},
                       {'text':' blocks'}]
            commands = ['scoreboard players set #distance ao_bench -1',
                        'scoreboard players set #success ao_bench 0',
                        f'execute in minecraft:overworld positioned {x} 100 {z} store result score #distance ao_bench store success score #success ao_bench run locate structure {structure}',
                        'tellraw @a '+json.dumps(message,separators=(',',':'))]
            if number < 180:
                commands.append(f'execute if score #running ao_bench matches 1 run schedule function ao_benchmark:step_{number+1:03} 2s replace')
            else:
                commands += ['scoreboard players set #running ao_bench 0',
                             'tellraw @a {"text":"[AO BENCHMARK] Complete: 180 locates."}']
            files[prefix+f'work_{name}.mcfunction'] = '\n'.join(commands)+'\n'
    assert number == 180
    output = ROOT/'build/AO-Benchmark-0.3.0.zip'
    output.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED) as archive:
        for name,content in sorted(files.items()): archive.writestr(name,content)
    print(output)
    return output

if __name__ == '__main__': build()
