#!/usr/bin/env python3
"""Extract byte-packed VDP data stored as 32-bit words in a save state."""
from pathlib import Path
import argparse, gzip, json

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('state',type=Path); ap.add_argument('offset',type=lambda x:int(x,0)); ap.add_argument('-o','--out',type=Path,default=Path('vdp_bytes.bin')); ap.add_argument('--count',type=lambda x:int(x,0),default=0x4000); ap.add_argument('--stride',type=int,default=4); ap.add_argument('--byte',type=int,default=0); args=ap.parse_args()
 raw=gzip.open(args.state,'rb').read(); vals=[]
 for i in range(args.count):
  p=args.offset+i*args.stride+args.byte
  if p>=len(raw): break
  vals.append(raw[p])
 args.out.write_bytes(bytes(vals))
 info={'state_offset':args.offset,'count':len(vals),'stride':args.stride,'byte':args.byte,'out':str(args.out.resolve())}
 print(json.dumps(info,indent=2))
if __name__=='__main__': main()
