from pathlib import Path
import gzip, json
raw=gzip.open('/home/ubuntu/work/kujakuou_direct/build/sync_capture/synchronized_state.mc0','rb').read()
patterns={
 'hud_top_left_bytes':bytes([0,1,4,5]),
 'hud_bottom_left_bytes':bytes([2,3,6,7]),
 'hud_top_right_bytes':bytes([8,9,4,5]),
 'hud_bottom_right_bytes':bytes([10,11,6,7]),
 'hud_top_left_words':b''.join(v.to_bytes(2,'little') for v in [0,1,4,5]),
 'hud_bottom_left_words':b''.join(v.to_bytes(2,'little') for v in [2,3,6,7]),
 'hud_top_right_words':b''.join(v.to_bytes(2,'little') for v in [8,9,4,5]),
 'hud_bottom_right_words':b''.join(v.to_bytes(2,'little') for v in [10,11,6,7]),
}
results={}
for name,p in patterns.items():
 hits=[]; start=0
 while True:
  i=raw.find(p,start)
  if i<0: break
  hits.append(i); start=i+1
 results[name]=hits[:500]
# Look for offsets where at least two HUD patterns occur within 0x100 bytes.
allhits=sorted((i,n) for n,hs in results.items() for i in hs)
clusters=[]
for i,n in allhits:
 near=[(j,m) for j,m in allhits if abs(j-i)<=0x100]
 if len({m for j,m in near})>=2: clusters.append({'offset':i,'near':near[:20]})
Path('/home/ubuntu/work/kujakuou_direct/build/name_table_hits.json').write_text(json.dumps({'patterns':{k:len(v) for k,v in results.items()},'clusters':clusters[:200]},indent=2))
print(json.dumps({'patterns':{k:len(v) for k,v in results.items()},'clusters':clusters[:20]},indent=2))
