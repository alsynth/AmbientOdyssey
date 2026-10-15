"""Author additive experimental quests from the 101-beat design; preserve all 52 existing quests."""
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OVERLAY = ROOT / 'release_030/experimental_overlays/v050/overrides'
CHAPTERS = {
 'The First Pages': ('first_pages', 'minecraft:book'), 'The Open Road': ('open_road', 'minecraft:compass'),
 'Trial by Steel': ('trial_steel', 'minecraft:iron_sword'), 'The Wider World': ('v050_wider_world', 'minecraft:bow'),
 'The Threshold': ('v050_threshold', 'minecraft:blaze_rod'), 'Old Powers': ('v050_old_powers', 'minecraft:diamond_sword'),
 'The Legendary Hunt': ('v050_legendary_hunt', 'minecraft:nether_star'), 'The Breaking Point': ('v050_breaking_point', 'minecraft:totem_of_undying'),
 'Beyond the Known': ('v050_beyond_known', 'minecraft:dragon_breath'), 'The Final Horizon': ('v050_final_horizon', 'minecraft:dragon_egg')}
NOTES = {
 0: 'Keep a safe place to sleep, a return route and enough food for an unexpected delay. Your first expedition can stay close to home.',
 1: 'Choose a landmark that interests you and leave a waypoint before going underground. A sensible route home matters more than travelling far.',
 2: 'A complete defensive kit and two useful combat supports are a better foundation than one impressive weapon. Test your recovery before entering a dungeon.',
 3: 'Explore a style that suits you: shield and steel, a mobile bow, or spells with reliable recovery. Demi\'s Sky and Ice Arenas have been removed from this test version.',
 4: 'The Nether, a Trial Chamber or a Mine Cells expedition can be your next challenge. Leave early Mine Cells loot as you find it; prepare a safe retreat.',
 5: 'The Night Lich and Void Blossom offer alternative Overworld milestones. A Bastion is a Tier 5 structure; a Nether Fortress is Tier 4.',
 6: 'The Dead King is the primary experimental Pinnacle route. Kobolediator is a provisional alternate whose combat equivalence still needs testing. Winning grants access without changing your active difficulty.',
 7: 'Choose one legendary threat and learn its telegraphs. Ancient Remnant and Ender Guardian are Tier 7; Maledictus and Leviathan are Tier 8, Scylla is Tier 9. A party is optional.',
 8: 'The Last of Deepslate is the first verified registry route for this experimental mastery milestone. Other Tier 8 encounters remain in the field dossiers until their triggers are confirmed.',
 9: 'Tyros, Scylla and Obsidilith are optional superboss challenges. After a Tier 8 milestone and all three victories, hold one affixed equipment item below Heirloom and use /ao_mastery upgrade. This changes the held item once; it does not give a second item. Chesed, Malkuth and Geburah are exempt Tier 5 bosses.'}

def write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

def advancement(name):
    return {'type':'questlog:advancement', 'advancement':'ao_campaign:milestones/' + name,
            'required_amount':1, 'name':'Complete the ' + name.replace('_', ' ') + ' milestone'}

def compile_campaign():
    rows = list(csv.DictReader((ROOT / 'docs/questing/V050_QUEST_BEATS_PROVISIONAL.csv').open(encoding='utf-8-sig', newline='')))
    assert len(rows) == 101
    source = ROOT / 'release_030/overrides/config/questlog/quests'
    original = {p.stem for p in source.glob('*.json')}
    assert len(original) == 52
    mapping, previous = [], None
    chapter_entries = {}
    # Only a chapter's opening note gates its optional objectives. Actual boss milestones
    # gate subsequent chapters, rather than demanding every side entry or rare site.
    tier_gate = {6:'ao_v050_old_powers_07',7:'ao_v050_legendary_hunt_05',
                 8:'ao_v050_breaking_point_05',9:'ao_v050_beyond_known_04'}
    for row in rows:
        tier, seq = int(row['ao_tier']), int(row['sequence'])
        if (tier,seq) == (9,3):
            row['quest_beat'] = 'Defeat Obsidilith in the End'
            row['validation_status'] = 'OWNER_SELECTED_T9_20261014; native kill milestone, combat acceptance pending'
        chapter, icon = CHAPTERS[row['chapter']]
        slug = 'ao_v050_' + row['design_seed_id'].removeprefix('design_')
        assert slug not in original
        obj = {'type':'questlog:read', 'name':'Read and acknowledge this expedition note'}
        status = 'READ_ACKNOWLEDGEMENT_ONLY'
        # Real vanilla preparations and milestones; never pretend to detect equipment quality or tactics.
        item_rules = {(0,4):('minecraft:cooked_beef',8), (0,6):('minecraft:shield',1),
                      (1,2):('minecraft:torch',32), (4,7):('minecraft:golden_apple',1)}
        if (tier,seq) in item_rules:
            item, amount = item_rules[tier,seq]
            obj = {'type':'questlog:item_obtain', 'item':item, 'required_amount':amount, 'name':'Carry ' + str(amount) + ' ' + item.split(':')[1].replace('_',' ')}
            status = 'NATIVE_ITEM_OBJECTIVE'
        milestone_rules = {(5,7):'tier_5', (6,5):'tier_6', (6,6):'artifact_reward', (6,7):'tier_6',
                           (7,5):'tier_7', (7,6):'heirloom_reward', (8,4):'tier_8', (8,5):'esoteric_reward',
                           (9,1):'tyros', (9,2):'scylla', (9,3):'obsidilith', (9,4):'heirloom_upgrade'}
        if (tier,seq) in milestone_rules:
            obj = advancement(milestone_rules[tier,seq]); status = 'SERVER_BOSS_OR_TRANSACTION_MILESTONE'
        if (tier,seq) == (4,2):
            obj = {'type':'questlog:visit_dimension','dimension':'minecraft:the_nether','required_amount':1,'name':'Enter the Nether'}
            status = 'NATIVE_DIMENSION_OBJECTIVE'
        if (tier,seq) == (4,4):
            obj = {'type':'questlog:or','name':'Enter a Trial Chamber or Nether Fortress', 'objectives':[
                {'type':'questlog:visit_structure','structure':s,'required_amount':1} for s in ('minecraft:trial_chambers','minecraft:fortress')]}
            status = 'NATIVE_STRUCTURE_OBJECTIVE'
        reserved = False
        if reserved:
            obj = {'type':'questlog:unobtainable','name':'Reserved: third End superboss remains unselected'}
            status = 'RESERVED_UNASSIGNED';
        description = NOTES[tier] + '\n\n' + row['quest_beat'] + '.'
        if status == 'READ_ACKNOWLEDGEMENT_ONLY':
            description += '\n\nThis entry records that you read the advice. It does not detect a fight, gear quality, a completed expedition or a claimed reward.'
        if reserved:
            description += '\n\nThis reserved encounter has no selected boss and does not block the final mastery upgrade.'
        quest = {'title':row['quest_beat'][:80], 'description':description, 'chapter':'questlog:'+chapter,
                 'sort_order':100+seq, 'icon':{'item':icon}, 'objectives':[obj], 'rewards':[],
                 'toast_on_unlock':False,'toast_on_complete':False,'show_popup_on_unlock':False,
                 'hide_when_completed':False,'repeatable':False,'global':False}
        if seq == 1:
            gate = tier_gate.get(tier, chapter_entries.get(tier-1))
            chapter_entries[tier] = slug
        else:
            gate = chapter_entries[tier]
        if gate and not reserved:
            quest['prerequisites'] = [{'type':'questlog:quest_complete','quest':'questlog:'+gate}]
        if not reserved: previous = slug
        write(OVERLAY / 'config/questlog/quests' / (slug+'.json'), quest)
        mapping.append({**row,'engine_quest_id':'questlog:'+slug,'implemented_objective':status})
    for order,(name,(slug,icon)) in enumerate(CHAPTERS.items(),13):
        if slug.startswith('v050_'):
            write(OVERLAY/'config/questlog/chapters'/(slug+'.json'),
                  {'name':name, 'translatable':False,'icon':{'item':icon},'order':order,'default_chapter':False,'hidden':False})
    for name in ['tier_5','tier_6','tier_7','tier_8','tier_9','tyros','scylla','obsidilith','heirloom_upgrade','artifact_reward','heirloom_reward','esoteric_reward']:
        write(ROOT/'addons/ao-campaign/src/main/resources/data/ao_campaign/advancement/milestones'/(name+'.json'),
              {'criteria':{'completed':{'trigger':'minecraft:impossible'}}})
    out = ROOT/'docs/questing/V050_IMPLEMENTED_QUEST_MAPPING.csv'
    with out.open('w',encoding='utf-8',newline='') as f:
        writer = csv.DictWriter(f,fieldnames=list(mapping[0]));writer.writeheader();writer.writerows(mapping)
    print(json.dumps({'design_beats':len(rows),'new_quests':len(mapping),'original_quests_preserved':52,
                      'read_acknowledgements':sum(r['implemented_objective']=='READ_ACKNOWLEDGEMENT_ONLY' for r in mapping),
                      'reserved_unassigned':0,'runtime_tested':False}))

if __name__ == '__main__': compile_campaign()
