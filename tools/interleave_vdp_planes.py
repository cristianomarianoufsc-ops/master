#!/usr/bin/env python3
from pathlib import Path
import argparse, json

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('passes',nargs=4,type=Path); ap.add_argument('-o','--out',type=Path,required=True); args=ap.parse_args()
 blobs=[p.read_bytes() for p in args.passes]; n=min(len(x) for x in blobs); n-=n%8
 out=bytearray()
 # Each decompressed stream is one bitplane: 8 bytes per tile, 8 rows.
 for tile in range(n//8):
  for row in range(8):
   for plane in range(4): out.append(blobs[plane][tile*8+row])
 args.out.write_bytes(out)
 print(json.dumps({'planes':[len(x) for x in blobs],'tiles':n//8,'output_bytes':len(out),'out':str(args.out.resolve())},indent=2))
if __name__=='__main__': main()
