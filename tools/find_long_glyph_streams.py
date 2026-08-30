#!/usr/bin/env python3
from pathlib import Path
import argparse
p=argparse.ArgumentParser(description='Find long FF-terminated glyph-like streams')
p.add_argument('rom');p.add_argument('--out',required=True);p.add_argument('--min',type=int,default=12);p.add_argument('--max',type=int,default=180)
a=p.parse_args();rom=Path(a.rom).read_bytes(); rows=[]
controls={0xfb,0xfc,0xfd,0xfe,0xff,0xee}
for bank in range(len(rom)//0x4000):
 data=rom[bank*0x4000:(bank+1)*0x4000]
 for start in range(len(data)):
  if data[start]==0xff: continue
  end=data.find(b'\xff',start+1)
  if end<0 or end-start<a.min or end-start>a.max: continue
  seg=data[start:end]
  # avoid arbitrary binary: require mostly small nonzero values and few high bytes
  small=sum(1 for x in seg if x<0x80 and x not in controls)
  zeros=seg.count(0)
  if small/max(1,len(seg))>=0.70 and zeros<=len(seg)*0.35:
   cpu=0x8000+(start if start<0x4000 else start-0x4000)
   rows.append((len(seg),bank,start,seg))
rows.sort(reverse=True)
out=['# Long FF-terminated glyph-like candidates','',f'candidates={len(rows)}','']
for n,bank,start,seg in rows[:500]: out.append(f'bank={bank} file=0x{bank*0x4000+start:06X} off=0x{start:04X} len={n} hex={seg[:160].hex()}')
Path(a.out).write_text('\n'.join(out)+'\n',encoding='utf-8');print(f'wrote {len(rows)} candidates to {a.out}')
