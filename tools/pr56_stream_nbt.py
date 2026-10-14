"""Bounded, streaming source-NBT palette/block scan for oversized AO structures.

A two-pass scan keeps only palette states and interesting spawner/jigsaw/entity
records, never a full decompressed NBT blob or all block compounds in memory.
This is NOT a live generated-world placement or spawner-activation check.
"""
import gzip
import io
import struct

MAX_UNCOMPRESSED = 256 * 1024 * 1024
MAX_STRING = 1 << 20
MAX_DEPTH = 80
MAX_LIST = 3_000_000
MAX_ARRAY = 64_000_000

class LimitedReader:
    def __init__(self, source, limit=MAX_UNCOMPRESSED):
        self.src, self.limit, self.count = source, limit, 0
    def read(self, size):
        if size < 0 or self.count + size > self.limit:
            raise ValueError("STREAM_LIMIT_EXCEEDED")
        result = self.src.read(size)
        self.count += len(result)
        if len(result) != size:
            raise ValueError("TRUNCATED_NBT_STREAM")
        return result
    def skip(self, size):
        if size < 0 or self.count + size > self.limit:
            raise ValueError("STREAM_LIMIT_EXCEEDED")
        while size:
            step=min(size,65536)
            chunk=self.read(step)
            size-=len(chunk)

class SelectiveNBT:
    def __init__(self, src):
        self.r=src
    def unpack(self, kind):
        return struct.unpack(">"+kind,self.r.read(struct.calcsize(">"+kind)))[0]
    def string(self):
        count=self.unpack("H")
        if count>MAX_STRING:raise ValueError("STRING_LIMIT_EXCEEDED")
        return self.r.read(count).decode("utf-8",errors="replace")
    def length(self, typ, max_count=MAX_LIST):
        count=self.unpack("i")
        if count<0 or count>max_count:raise ValueError("BAD_NBT_LENGTH")
        return count
    def read_payload(self, typ, depth=0, store=True):
        if depth>MAX_DEPTH:raise ValueError("NBT_DEPTH_LIMIT")
        if typ==0:return None
        if typ in (1,2,3,4,5,6):
            size={1:1,2:2,3:4,4:8,5:4,6:8}[typ]
            if not store:self.r.skip(size);return None
            return self.unpack({1:"b",2:"h",3:"i",4:"q",5:"f",6:"d"}[typ])
        if typ==7:
            n=self.length(typ,MAX_ARRAY)
            self.r.skip(n)
            return None
        if typ==8:
            count=self.unpack("H")
            if count>MAX_STRING:raise ValueError("STRING_LIMIT_EXCEEDED")
            if not store:self.r.skip(count);return None
            return self.r.read(count).decode("utf-8",errors="replace")
        if typ==9:
            item=self.unpack("B")
            n=self.length(typ)
            if n and item==0:raise ValueError("INVALID_END_LIST")
            if not store:
                for _ in range(n):self.read_payload(item,depth+1,False)
                return None
            return [self.read_payload(item,depth+1,True) for _ in range(n)]
        if typ==10:
            result={} if store else None
            while True:
                t=self.unpack("B")
                if not t:break
                key=self.string()
                v=self.read_payload(t,depth+1,store)
                if store:result[key]=v
            return result
        if typ in (11,12):
            n=self.length(typ,MAX_ARRAY//(4 if typ==11 else 8))
            self.r.skip(n*(4 if typ==11 else 8))
            return None
        raise ValueError("UNSUPPORTED_NBT_TYPE_"+str(typ))
    def root_fields(self, wanted, callback):
        if self.unpack("B")!=10:
            raise ValueError("EXPECTED_NAMED_ROOT_COMPOUND")
        self.string()
        seen=[]
        while True:
            tag=self.unpack("B")
            if tag==0:break
            name=self.string()
            seen.append(name)
            if name in wanted:
                callback(self, name, tag)
            else:
                self.read_payload(tag,store=False)
        return seen
    def each_list_compound(self, tag, visit):
        if tag!=9:raise ValueError("EXPECTED_NBT_LIST")
        typ=self.unpack("B")
        if typ!=10:raise ValueError("EXPECTED_COMPOUND_LIST")
        count=self.length(9)
        for _ in range(count):
            visit(self.read_payload(10))

def open_nbt(zf, name, max_bytes):
    # ZipExtFile itself decompresses the outer JAR's ZIP member. We then
    # consume the NBT gzip layer as a STREAM, not gzip.decompress(all_bytes).
    raw=io.BufferedReader(zf.open(name))
    header=raw.peek(2)[:2]
    if header==b"\x1f\x8b":
        source=gzip.GzipFile(fileobj=raw,mode="rb")
    elif header[:1]==b"\x0a":
        source=raw
    else:
        raw.close()
        raise ValueError("UNSUPPORTED_NBT_STREAM_COMPRESSION")
    return source, LimitedReader(source,max_bytes)

def extract_selected(zf, name, max_bytes=MAX_UNCOMPRESSED):
    palettes=[]
    def palette_visit(parser,key,tag):
        nonlocal palettes
        if key=="palette":
            palettes=parser.read_payload(tag)
        elif key=="palettes":
            multi=parser.read_payload(tag)
            palettes=multi[0] if multi else []
    source,limited=open_nbt(zf,name,max_bytes)
    try:
        parser=SelectiveNBT(limited)
        parser.root_fields({"palette","palettes"},palette_visit)
        pass1=limited.count
    finally:
        source.close()
    if not isinstance(palettes,list) or not palettes:
        raise ValueError("MISSING_NBT_PALETTE")
    valid={"minecraft:spawner","minecraft:trial_spawner","minecraft:jigsaw"}
    interesting=[]
    ids=[]
    def second_pass(parser,key,tag):
        if key=="blocks":
            def block_visit(b):
                if not isinstance(b,dict):return
                index=b.get("state",-1)
                if not isinstance(index,int) or not 0<=index<len(palettes):return
                p=palettes[index]
                if isinstance(p,dict) and p.get("Name") in valid:
                    interesting.append({"state":index,"nbt":b.get("nbt",{})})
            parser.each_list_compound(tag,block_visit)
        elif key=="entities":
            def entity_visit(e):
                n=e.get("nbt",{}) if isinstance(e,dict) else {}
                if isinstance(n,dict) and isinstance(n.get("id"),str):
                    ids.append({"nbt":{"id":n["id"]}})
            parser.each_list_compound(tag,entity_visit)
    source,limited=open_nbt(zf,name,max_bytes)
    try:
        parser=SelectiveNBT(limited)
        parser.root_fields({"blocks","entities"},second_pass)
        pass2=limited.count
    finally:
        source.close()
    return ({"palette":palettes,"blocks":interesting,"entities":ids},
            {"streaming_mode":"TWO_PASS_LIMITED_NBT",
             "first_pass_bytes":pass1,"second_pass_bytes":pass2,
             "palette_states":len(palettes),
             "interesting_block_records":len(interesting),
             "entity_records":len(ids),
             "max_bytes_per_pass":max_bytes})
