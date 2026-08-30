#!/usr/bin/env python3
from pathlib import Path
import gzip, argparse, json

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('state',type=Path); ap.add_argument('-o','--out',type=Path,default=Path('deinterleaved')); ap.add_argument('--start',type=lambda x:int(x,0),default=0); ap.add_argument('--end',type=lambda x:int(x,0)); args=ap.parse_args()
 raw=gzip.open(args.state,'rb').read(); end=args.end or len(raw); args.out.mkdir(parents=True,exist_ok=True)
 rows=[]
 # Every candidate is a 32 KiB state span deinterleaved into a 16 KiB stream.
 for s in range(args.start,end-0x8000+1,0x100):
  block=raw[s:s+0x8000]
  for parity in (0,1):
   out=block[parity::2][:0x4000]
   p=args.out/f'candidate_{s:06x}_{parity}.vram'; p.write_bytes(out)
   rows.append({'state_offset':s,'parity':parity,'path':str(p.resolve()),'nonzero':sum(x!=0 for x in out),'unique':len(set(out))})
 json.dump({'state_size':len(raw),'candidates':rows},open(args.out/'report.json','w'),indent=2)
 print(json.dumps({'state_size':len(raw),'candidates':len(rows),'out':str(args.out.resolve())},indent=2))
if __name__=='__main__': main()
