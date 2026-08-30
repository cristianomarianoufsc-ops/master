from pathlib import Path
import json
state=Path('/home/ubuntu/work/kujakuou_direct/build/sync_capture/synchronized_state.raw').read_bytes()
rom=Path('/home/ubuntu/work/kujakuou_direct/work/kujaku_ou_jp_original.sms').read_bytes()
base=234662
out=[]
for i in range(12):
 b=state[base+i*32:base+(i+1)*32]
 hits=[]; p=rom.find(b)
 while p>=0 and len(hits)<50:
  hits.append(p); p=rom.find(b,p+1)
 out.append({'pattern_index':i,'state_offset':base+i*32,'rom_offsets':hits,'tile_hex':b.hex()})
Path('/home/ubuntu/work/kujakuou_direct/build/confirmed_tiles_rom.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
