#!/usr/bin/env python3
"""Map regional dialogue handlers from current-format Z80 disassembly."""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

LINE = re.compile(r"^([0-9A-Fa-f]{4}):\s+([0-9A-Fa-f]+)\s+(.*)$")
LD_PTR = re.compile(r"ld\s+(hl|de),\s+0x([0-9a-f]+)", re.I)
CALL = re.compile(r"call\s+0x([0-9a-f]+)", re.I)

def parse(path):
    out=[]
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        m=LINE.match(line)
        if not m: continue
        raw=m.group(2); text=m.group(3)
        out.append({"pc":int(m.group(1),16), "raw":raw, "opcode":int(raw[:2],16),
                    "size":len(raw)//2, "text":text})
    return out

def resolver_calls(items, resolver):
    return [i for i,x in enumerate(items) if (m:=CALL.search(x["text"])) and int(m.group(1),16)==resolver]

def signature(items, start, width):
    return tuple((x["opcode"],x["size"]) for x in items[start:start+width])

def pointers(items, index, radius=10):
    result=[]
    for x in items[max(0,index-radius):index]:
        if m:=LD_PTR.search(x["text"]):
            result.append({"register":m.group(1).upper(),"value":int(m.group(2),16),"pc":x["pc"]})
    return result

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("reference",type=Path); ap.add_argument("target",type=Path)
    ap.add_argument("--reference-resolver",type=lambda x:int(x,0),required=True)
    ap.add_argument("--target-resolver",type=lambda x:int(x,0),required=True)
    ap.add_argument("--window",type=int,default=12); ap.add_argument("--out",type=Path,required=True)
    a=ap.parse_args(); ref=parse(a.reference); tar=parse(a.target)
    rc=resolver_calls(ref,a.reference_resolver); tc=resolver_calls(tar,a.target_resolver)
    rows=[]
    for ri in rc:
        sig=signature(ref,ri,a.window); hits=[ti for ti in tc if signature(tar,ti,a.window)==sig]
        rows.append({"reference_pc":ref[ri]["pc"],"target_hits":[tar[x]["pc"] for x in hits],
                     "unique":len(hits)==1,"reference_pointers":pointers(ref,ri),
                     "target_pointers":[pointers(tar,x) for x in hits],"window":a.window,
                     "signature":[list(x) for x in sig]})
    report={"reference":str(a.reference),"target":str(a.target),
            "reference_resolver":hex(a.reference_resolver),"target_resolver":hex(a.target_resolver),
            "reference_calls":len(rc),"target_calls":len(tc),"matches":rows}
    a.out.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"reference_calls":len(rc),"target_calls":len(tc),"matched":sum(bool(x["target_hits"]) for x in rows),"unique":sum(x["unique"] for x in rows),"report":str(a.out)},indent=2))

if __name__=="__main__": main()
