#!/usr/bin/env python3
"""Differential tracer for Mednafen SMS save states.

It does not modify ROMs. Given two or more gzip save states, it compares the
uncompressed state bytes, ranks 16 KiB windows by activity/entropy, and emits
candidate regions for VRAM/name-table analysis. This is useful when a scene is
captured before and after a dialogue or menu transition.
"""
from __future__ import annotations
import argparse, gzip, hashlib, json, math
from pathlib import Path

def load(p: Path) -> bytes:
    b=p.read_bytes()
    try: return gzip.decompress(b)
    except Exception: return b

def entropy(b: bytes) -> float:
    if not b: return 0.0
    c=[0]*256
    for x in b:c[x]+=1
    n=len(b); return -sum((v/n)*math.log2(v/n) for v in c if v)

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument('states',nargs='+',type=Path)
 ap.add_argument('-o','--out',type=Path,required=True)
 ap.add_argument('--window',type=lambda x:int(x,0),default=0x4000)
 ap.add_argument('--step',type=lambda x:int(x,0),default=0x20)
 args=ap.parse_args(); args.out.mkdir(parents=True,exist_ok=True)
 raw=[load(p) for p in args.states]; n=min(map(len,raw)); records=[]
 for k in range(len(raw)-1):
  a,b=raw[k][:n],raw[k+1][:n]
  changed=sum(x!=y for x,y in zip(a,b))
  for off in range(0,n-args.window+1,args.step):
   x=a[off:off+args.window]; y=b[off:off+args.window]
   diff=sum(u!=v for u,v in zip(x,y));
   if diff==0: continue
   # Active windows with moderate diversity are better than all-zero noise.
   score=(diff/max(1,args.window))*2.0 + min(entropy(y),8.0)/16.0
   records.append({'pair':k,'offset':off,'end':off+args.window,'changed':diff,'ratio':diff/args.window,'entropy_after':entropy(y),'score':score})
 records.sort(key=lambda r:r['score'],reverse=True)
 report={'states':[{'path':str(p),'raw_size':len(x),'sha256':hashlib.sha256(x).hexdigest()} for p,x in zip(args.states,raw)],'pairs':len(raw)-1,'top_windows':records[:200]}
 (args.out/'report.json').write_text(json.dumps(report,indent=2))
 for i,r in enumerate(records[:32]):
  (args.out/f'candidate_{i:02d}_p{r["pair"]}_{r["offset"]:08x}.bin').write_bytes(raw[r['pair']+1][r['offset']:r['end']])
 print(json.dumps({'states':len(raw),'raw_size':n,'pairs':len(raw)-1,'top_candidates':len(records[:32]),'report':str((args.out/'report.json').resolve())},indent=2))
if __name__=='__main__': main()
