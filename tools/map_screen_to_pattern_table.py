#!/usr/bin/env python3
from pathlib import Path
import json
from PIL import Image

def tile_mask_bytes(d):
 if len(d)<32:return 0
 m=0
 for y in range(8):
  for x in range(8):
   b=7-x; v=sum(((d[y*4+p]>>b)&1)<<p for p in range(4))
   if v:m|=1<<(y*8+x)
 return m

def main():
 import argparse
 ap=argparse.ArgumentParser(); ap.add_argument('patterns',type=Path); ap.add_argument('screen',type=Path); ap.add_argument('-o','--out',type=Path,default=Path('screen_pattern_map.json')); ap.add_argument('--count',type=int,default=256); args=ap.parse_args()
 raw=args.patterns.read_bytes(); im=Image.open(args.screen).convert('RGB')
 if im.size==(1024,960): im=im.crop((0,96,1024,864)).resize((256,192),Image.Resampling.NEAREST)
 else: im=im.resize((256,192),Image.Resampling.NEAREST)
 pats=[tile_mask_bytes(raw[i*32:i*32+32]) for i in range(min(args.count,len(raw)//32))]
 cells=[]
 for ty in range(24):
  for tx in range(32):
   target=0
   for y in range(8):
    for x in range(8):
     r,g,b=im.getpixel((tx*8+x,ty*8+y))
     if max(r,g,b)>45: target|=1<<(y*8+x)
   ranked=sorted(((target^p).bit_count(),i) for i,p in enumerate(pats))[:8]
   cells.append({'x':tx,'y':ty,'target_bits':target.bit_count(),'best':ranked})
 args.out.write_text(json.dumps(cells,indent=2)); print(json.dumps({'cells':len(cells),'patterns':len(pats),'out':str(args.out.resolve())},indent=2))
if __name__=='__main__': main()
