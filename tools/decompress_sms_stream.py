#!/usr/bin/env python3
"""Decode the simple RLE stream used by Kujaku Ou's Z80 VDP loader."""
from pathlib import Path
import argparse, json

def decode_one(data, pos, limit=0x10000):
 out=bytearray(); start=pos
 while pos<len(data) and len(out)<limit:
  ctl=data[pos]; pos+=1
  if ctl==0: break
  if ctl&0x80:
   n=ctl&0x7f; out.extend(data[pos:pos+n]); pos+=n
  else:
   if pos>=len(data): break
   out.extend(bytes([data[pos]])*ctl); pos+=1
 return bytes(out),pos,start

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('rom',type=Path); ap.add_argument('offset',type=lambda x:int(x,0)); ap.add_argument('-o','--out',type=Path,default=Path('stream.bin')); ap.add_argument('--passes',type=int,default=4); args=ap.parse_args()
 data=args.rom.read_bytes(); pos=args.offset; info=[]; allout=bytearray()
 for i in range(args.passes):
  out,end,start=decode_one(data,pos); args.out.parent.mkdir(parents=True,exist_ok=True)
  (args.out.parent/f'{args.out.stem}_pass{i}{args.out.suffix}').write_bytes(out)
  info.append({'pass':i,'source_offset':start,'source_end':end,'decoded_size':len(out),'first_bytes':out[:16].hex()}); allout.extend(out); pos=end
 args.out.write_bytes(allout); print(json.dumps({'offset':args.offset,'passes':info,'combined_size':len(allout),'out':str(args.out.resolve())},indent=2))
if __name__=='__main__': main()
