#!/usr/bin/env python3
"""Read structure NBT without third-party dependencies, retaining every tag type."""
import gzip, io, struct

FORMATS={1:'b',2:'h',3:'i',4:'q',5:'f',6:'d'}

class NbtReader:
    def __init__(self,raw):self.f=io.BytesIO(gzip.decompress(raw) if raw[:2]==b'\x1f\x8b' else raw)
    def take(self,n):
        b=self.f.read(n)
        if len(b)!=n:raise ValueError('Truncated NBT')
        return b
    def number(self,fmt):return struct.unpack('>'+fmt,self.take(struct.calcsize(fmt)))[0]
    def string(self):return self.take(self.number('H')).decode('utf-8')
    def payload(self,t):
        if t in FORMATS:return self.number(FORMATS[t])
        if t==7:return self.take(self.number('i'))
        if t==8:return self.string()
        if t==9:
            subtype=self.number('B');return (subtype,[self.payload(subtype) for _ in range(self.number('i'))])
        if t==10:
            values=[]
            while True:
                subtype=self.number('B')
                if subtype==0:break
                name=self.string();values.append((name,subtype,self.payload(subtype)))
            return values
        if t in (11,12):return [self.number('i' if t==11 else 'q') for _ in range(self.number('i'))]
        raise ValueError(t)
    def read(self):
        t=self.number('B');name=self.string();value=self.payload(t)
        assert not self.f.read(1), 'Trailing NBT data'
        return (name,t,value)

def plain(t,v):
    if t==10:return {k:plain(st,sv) for k,st,sv in v}
    if t==9:return [plain(v[0],sv) for sv in v[1]]
    if t==7:return list(v)
    return v

def encode_nbt(name, t, value, compressed=True):
    """Write a typed NBT tree, preserving order and types of unedited tags."""
    def string(s):
        raw=s.encode('utf-8');return struct.pack('>H',len(raw))+raw
    def payload(kind,v):
        if kind in FORMATS:return struct.pack('>'+FORMATS[kind],v)
        if kind==7:return struct.pack('>i',len(v))+bytes(v)
        if kind==8:return string(v)
        if kind==9:return bytes([v[0]])+struct.pack('>i',len(v[1]))+b''.join(payload(v[0],x) for x in v[1])
        if kind==10:return b''.join(bytes([st])+string(k)+payload(st,sv) for k,st,sv in v)+b'\x00'
        if kind in (11,12):return struct.pack('>i',len(v))+b''.join(struct.pack('>i' if kind==11 else '>q',x) for x in v)
        raise ValueError(kind)
    raw=bytes([t])+string(name)+payload(t,value)
    return gzip.compress(raw,mtime=0) if compressed else raw

def migrate_waystone_jigsaw(raw):
    """Modernize the supplied Waystones desert template's legacy connector NBT."""
    name,t,tree=NbtReader(raw).read()
    fields={k:(st,sv) for k,st,sv in tree}
    palette=fields['palette'][1][1]
    states=[]
    for i,block in enumerate(palette):
        d={k:(st,sv) for k,st,sv in block}
        if d['Name'][1]!='minecraft:jigsaw':continue
        states.append(i)
        facing=dict((k,sv) for k,st,sv in d.get('Properties',(10,[]))[1]).get('facing','north')
        orientation=facing+'_up' if facing in {'north','south','east','west'} else 'north_up'
        block[:]=[(k,st,sv) for k,st,sv in block if k!='Properties']+[
            ('Properties',10,[('orientation',8,orientation)])]
    for block in fields['blocks'][1][1]:
        d={k:(st,sv) for k,st,sv in block}
        if d['state'][1] not in states:continue
        block[:]=[(k,st,sv) for k,st,sv in block if k!='nbt']+[
            ('nbt',10,[(key,8,v) for key,v in {
                'id':'minecraft:jigsaw','name':'minecraft:building_entrance',
                'target':'minecraft:empty','pool':'minecraft:empty',
                'joint':'aligned','final_state':'minecraft:air'}.items()])]
    assert states,'No native jigsaw states'
    return encode_nbt(name,t,tree)

def template_details(raw):
    name,t,value=NbtReader(raw).read();d=plain(t,value)
    palettes=d.get('palettes',[d.get('palette',[])])
    jigsaw_states={i for palette in palettes for i,x in enumerate(palette) if x['Name']=='minecraft:jigsaw'}
    jigs=[b for b in d.get('blocks',[]) if b['state'] in jigsaw_states]
    return {'size':d.get('size'),'jigsaws':jigs,'palette_ids':sorted({x['Name'] for palette in palettes for x in palette}),
            'entities':d.get('entities',[])}

if __name__=='__main__':
    import argparse,json,zipfile
    p=argparse.ArgumentParser();p.add_argument('jar');p.add_argument('path');a=p.parse_args()
    with zipfile.ZipFile(a.jar) as z:print(json.dumps(template_details(z.read(a.path)),indent=2))
