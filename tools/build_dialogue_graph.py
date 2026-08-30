#!/usr/bin/env python3
from pathlib import Path
files={
 'handlers':'build/dialog_handler_candidates.md',
 'chains':'build/chain_5c02_finals.txt',
 'primary':'build/dialog_pointer_af55_bank22.md',
 'external':'build/bd55_external_ref_targets.txt',
 'findings':'build/static_script_findings.md',
}
out=['# Consolidated dialogue-resolution graph','',
      'This report separates executable handlers from pointer tables and scene bytecode.','']
for name,path in files.items():
 p=Path(path)
 out.append(f'## {name}: {path}')
 out.append(p.read_text(errors='replace') if p.exists() else '[missing]')
 out.append('')
Path('build/dialogue_resolution_graph.md').write_text('\n'.join(out),encoding='utf-8')
print('wrote build/dialogue_resolution_graph.md')
