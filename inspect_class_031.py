#!/usr/bin/env python3
"""Small dependency-free classfile inspector for audit evidence (not decompilation)."""
import argparse, json, struct, zipfile

class Reader:
    def __init__(self,data): self.data=data;self.p=0
    def u1(self):v=self.data[self.p];self.p+=1;return v
    def u2(self):v=struct.unpack_from('>H',self.data,self.p)[0];self.p+=2;return v
    def u4(self):v=struct.unpack_from('>I',self.data,self.p)[0];self.p+=4;return v
    def take(self,n):v=self.data[self.p:self.p+n];self.p+=n;return v

def inspect(data):
    r=Reader(data);assert r.u4()==0xcafebabe;r.take(4);n=r.u2();cp=[None]*n;i=1
    while i<n:
        t=r.u1()
        if t==1:cp[i]=r.take(r.u2()).decode(errors='replace')
        elif t in (3,4):cp[i]=(t,r.take(4).hex())
        elif t in (5,6):cp[i]=(t,r.take(8).hex());i+=1
        elif t in (7,8,16,19,20):cp[i]=(t,r.u2())
        elif t in (9,10,11,12,17,18):cp[i]=(t,r.u2(),r.u2())
        elif t==15:cp[i]=(t,r.u1(),r.u2())
        else:raise ValueError(t)
        i+=1
    def resolve(i):
        v=cp[i]
        if isinstance(v,str):return v
        if v[0] in (7,8,16,19,20):return resolve(v[1])
        if v[0] in (9,10,11,12):return ' '.join(resolve(x) for x in v[1:])
        return str(v)
    def attrs(reader):
        result={}
        for _ in range(reader.u2()):
            name=resolve(reader.u2());result[name]=reader.take(reader.u4())
        return result
    r.take(6);r.take(r.u2()*2)
    for _ in range(r.u2()):r.take(6);attrs(r)
    methods=[]
    for _ in range(r.u2()):
        access=r.u2();name=resolve(r.u2());descriptor=resolve(r.u2());a=attrs(r);operations=[]
        if 'Code' in a:
            cr=Reader(a['Code']);cr.take(4);code=cr.take(cr.u4());p=0
            fixed={0x10:1,0x11:2,0x12:1,0x13:2,0x14:2,0x84:2,0xa9:1,
                   0xb2:2,0xb3:2,0xb4:2,0xb5:2,0xb6:2,0xb7:2,0xb8:2,0xb9:4,0xba:4,
                   0xbb:2,0xbc:1,0xbd:2,0xc0:2,0xc1:2,0xc5:3,0xc6:2,0xc7:2,0xc8:4,0xc9:4}
            names={0xb2:'getstatic',0xb3:'putstatic',0xb4:'getfield',0xb5:'putfield',0xb6:'invokevirtual',
                   0xb7:'invokespecial',0xb8:'invokestatic',0xb9:'invokeinterface',0xba:'invokedynamic',
                   0x12:'ldc',0x13:'ldc_w',0xbb:'new',0xc0:'checkcast',0x99:'ifeq',0x9a:'ifne',
                   0xa7:'goto',0xac:'ireturn',0xb0:'areturn',0xb1:'return',0x03:'iconst_0',0x04:'iconst_1'}
            while p<len(code):
                start=p;op=code[p];p+=1;nargs=fixed.get(op,1 if 0x15<=op<=0x19 or 0x36<=op<=0x3a else 2 if 0x99<=op<=0xa8 else 0)
                if op in (0xaa,0xab):
                    p += (-p)%4
                    if op==0xaa:
                        _,lo,hi=struct.unpack_from('>iii',code,p);nargs=12+4*(hi-lo+1)
                    else:nargs=8+8*struct.unpack_from('>i',code,p+4)[0]
                elif op==0xc4:nargs=5 if code[p]==0x84 else 3
                args=code[p:p+nargs];p+=nargs
                entry={'offset':start,'op':names.get(op,hex(op))}
                if op in (0xb2,0xb3,0xb4,0xb5,0xb6,0xb7,0xb8,0xb9,0xba,0xbb,0xbd,0xc0,0xc1,0x13,0x14):
                    entry['reference']=resolve(struct.unpack_from('>H',args)[0])
                elif op==0x12:entry['reference']=resolve(args[0])
                elif nargs:entry['args']=args.hex()
                operations.append(entry)
        methods.append({'name':name,'descriptor':descriptor,'operations':operations})
    return {'constants':[v for v in cp if isinstance(v,str)],'methods':methods}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('jar');p.add_argument('class_path');a=p.parse_args()
    with zipfile.ZipFile(a.jar) as z:print(json.dumps(inspect(z.read(a.class_path)),indent=2))
