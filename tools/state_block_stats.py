from pathlib import Path
import gzip, math
from collections import Counter
p=Path('/home/ubuntu/work/kujakuou_direct/build/sync_capture/synchronized_state.mc0')
b=gzip.open(p,'rb').read()
for size in (0x100,0x400,0x1000,0x2000,0x4000):
 rows=[]
 for off in range(0,len(b)-size+1,size):
  c=b[off:off+size]; n=len(c); q=Counter(c)
  e=-sum((v/n)*math.log2(v/n) for v in q.values())
  rows.append((e,len(q),c.count(0),c.count(255),off))
 print(f'\nSIZE {size:#x}')
 for r in sorted(rows)[:25]: print(f'ent={r[0]:.3f} uniq={r[1]:3d} zero={r[2]:5d} ff={r[3]:5d} off={r[4]:#08x}')
