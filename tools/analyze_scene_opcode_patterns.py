#!/usr/bin/env python3
from pathlib import Path
from collections import Counter, defaultdict
import argparse

p=argparse.ArgumentParser(description='Analyze command-byte patterns in banked scene bytecode')
p.add_argument('rom'); p.add_argument('--bank',type=int,default=22); p.add_argument('--start',type=lambda x:int(x,16),default=0x9d08); p.add_argument('--end',type=lambda x:int(x,16),default=0x9fc8); p.add_argument('--out',required=True)
a=p.parse_args()
rom=Path(a.rom).read_bytes(); base=a.bank*0x4000; data=rom[base+(a.start-0x8000):base+(a.end-0x8000)+1]
cmds=(0xfb,0xfc,0xfd,0xfe,0xff,0xee)
count=Counter(); contexts=defaultdict(list)
for i,v in enumerate(data):
 if v in cmds:
  count[v]+=1
  contexts[v].append(data[max(0,i-3):i+8].hex())
out=['# Scene opcode pattern analysis','',f'bank={a.bank} range=0x{a.start:04X}-0x{a.end:04X}','', 'opcode,count']
for v,n in sorted(count.items()): out.append(f'0x{v:02X},{n}')
out += ['', '## contexts']
for v in sorted(contexts):
 out.append(f'### 0x{v:02X}')
 for s in contexts[v][:40]: out.append(s)
 out.append('')
Path(a.out).write_text('\n'.join(out)+'\n',encoding='utf-8')
print(f'wrote opcode analysis to {a.out}')
