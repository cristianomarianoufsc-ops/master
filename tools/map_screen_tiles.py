from pathlib import Path
import json
base=234662
p=json.load(open('/home/ubuntu/work/kujakuou_direct/build/exact_vram_tile_hits.json'))
out=[]
for r in p['results'][:1]:
 for x in r['locations']:
  off=x['state_offset']
  if off>=base and (off-base)%32==0:
   out.append({'screen_cells':x['screen'],'pattern_index':(off-base)//32,'state_offset':off,'tile_hex':x['tile_hex']})
Path('/home/ubuntu/work/kujakuou_direct/build/screen_tile_map.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
