#!/usr/bin/env python3
from pathlib import Path
import gzip, json
from collections import defaultdict
from PIL import Image

def tile_bytes(im,tx,ty,perm):
    d=bytearray()
    for y in range(8):
        rows=[0,0,0,0]
        for x in range(8):
            v=im.getpixel((tx*8+x,ty*8+y)) & 15
            for p in range(4): rows[p] |= ((v>>perm[p])&1) << (7-x)
        d.extend(rows)
    return bytes(d)

def main():
    import argparse
    ap=argparse.ArgumentParser(); ap.add_argument('state',type=Path); ap.add_argument('screen',type=Path); ap.add_argument('-o','--out',type=Path,default=Path('tile_hits.json')); args=ap.parse_args()
    raw=gzip.open(args.state,'rb').read(); im=Image.open(args.screen)
    if im.mode!='P': im=im.convert('P',palette=Image.Palette.ADAPTIVE,colors=16)
    if im.size==(1024,960): im=im.crop((0,96,1024,864)).resize((256,192),Image.Resampling.NEAREST)
    else: im=im.resize((256,192),Image.Resampling.NEAREST)
    # Ignore nearly empty cells; keep rare/structured screen tiles.
    hits=[]
    perms=[(0,1,2,3),(3,2,1,0),(1,0,3,2),(2,3,0,1)]
    for perm in perms:
        by=defaultdict(list)
        for ty in range(24):
            for tx in range(32):
                b=tile_bytes(im,tx,ty,perm)
                if any(b) and b not in by: by[b].append((tx,ty))
                elif any(b): by[b].append((tx,ty))
        found=0; locations=[]
        for b,poss in by.items():
            pos=raw.find(b)
            if pos>=0:
                found+=1; locations.append({'screen':poss[:8],'state_offset':pos,'tile_hex':b.hex()})
        hits.append({'perm':perm,'distinct_screen_tiles':len(by),'exact_tiles_found':found,'locations':locations[:200]})
    args.out.write_text(json.dumps({'state_size':len(raw),'results':hits},indent=2))
    print(json.dumps({'state_size':len(raw),'results':[(x['perm'],x['exact_tiles_found']) for x in hits],'out':str(args.out.resolve())},indent=2))
if __name__=='__main__': main()
