#!/usr/bin/env python3
"""Run a minimal SMS memory/mapper model and capture a Z80 breakpoint.

This is a diagnostic runner, not a complete SMS emulator. It maps the fixed
16 KiB ROM window, the two switchable ROM windows selected by FFFE/FFFF, and
SMS RAM at C000-DFFF (mirrored at E000-FFFF except mapper registers). I/O is
stubbed conservatively. It is intended to determine whether the ROM reaches
the C280 initialization breakpoint without requiring a graphical emulator.
"""
from pathlib import Path
import argparse
import json
import z80

p = argparse.ArgumentParser(description=__doc__)
p.add_argument("rom", type=Path)
p.add_argument("--breakpoint", type=lambda x: int(x, 0), default=0x4A8D)
p.add_argument("--max-steps", type=int, default=5_000_000)
p.add_argument("--ticks-per-run", type=int, default=100_000,
               help="CPU ticks budget for each native run() call")
p.add_argument("--vdp-wait-reads", type=int, default=2,
               help="reads of C008 before the diagnostic VDP wait is released")
p.add_argument("--out", type=Path, required=True)
a = p.parse_args()

rom = a.rom.read_bytes()
if len(rom) % 0x4000:
    raise SystemExit(f"ROM size must be a multiple of 0x4000, got {len(rom):#x}")
banks = [rom[i:i + 0x4000] for i in range(0, len(rom), 0x4000)]
ram = bytearray(0x2000)
mapper = {0xFFFC: 0, 0xFFFD: 0, 0xFFFE: 1, 0xFFFF: 0x82}
reads = {}
writes = {}
last_pc = None
vdp_wait_reads = 0


def ram_index(addr):
    return (addr - 0xC000) & 0x1FFF


def read_mem(addr):
    global vdp_wait_reads
    addr &= 0xFFFF
    # The real SMS clears C008 from a VDP/interrupt path during the call at
    # 04E4. With no VDP timing model, release only this known polling loop
    # after a bounded number of reads; all other RAM remains untouched.
    if addr == 0xC008 and 'cpu' in globals() and cpu.pc in (0x04E7, 0x04EA, 0x04EB):
        vdp_wait_reads += 1
        if vdp_wait_reads >= a.vdp_wait_reads:
            ram[ram_index(addr)] = 0
    reads[addr] = reads.get(addr, 0) + 1
    if addr < 0x4000:
        return banks[0][addr]
    if addr < 0x8000:
        bank = mapper[0xFFFE] & 0x1F
        return banks[bank % len(banks)][addr - 0x4000]
    if addr < 0xC000:
        bank = mapper[0xFFFF] & 0x1F
        return banks[bank % len(banks)][addr - 0x8000]
    if addr in mapper:
        return mapper[addr]
    return ram[ram_index(addr)]


def write_mem(addr, value):
    addr &= 0xFFFF
    value &= 0xFF
    writes[addr] = writes.get(addr, 0) + 1
    if addr in mapper:
        mapper[addr] = value
    elif 0xC000 <= addr <= 0xFFFF:
        ram[ram_index(addr)] = value


def input_port(port):
    # No controller/VDP timing is modeled. Open-bus zero is explicit.
    return 0


def output_port(port, value):
    # VDP/PSG writes are intentionally ignored in this diagnostic runner.
    return None

cpu = z80.Z80Machine()
cpu.set_read_callback(read_mem)
cpu.set_write_callback(write_mem)
cpu.set_input_callback(input_port)
cpu.set_output_callback(output_port)
cpu.set_breakpoint(a.breakpoint)

# Reset-compatible values used by the game's fixed boot code.
cpu.pc = 0
cpu.sp = 0xDFF0
cpu.ticks_to_stop = a.ticks_per_run
steps = 0
result = "breakpoint"
events = []
try:
    while steps < a.max_steps:
        event = cpu.run()
        steps += 1
        # run() may stop at the configured tick budget. Re-arm it so the
        # diagnostic runner can continue through multiple frames/events.
        cpu.ticks_to_stop = a.ticks_per_run
        events.append({"event": event, "pc": f"0x{cpu.pc:04X}"})
        if cpu.pc == a.breakpoint:
            break
    else:
        result = "step_limit"
except Exception as exc:
    result = "error"
    error = repr(exc)
else:
    error = None

if result == "breakpoint" and cpu.pc != a.breakpoint:
    result = "step_limit"

snapshot = {f"0x{0xC000 + i:04X}": ram[i] for i in range(len(ram)) if ram[i]}
interesting = {f"0x{x:04X}": read_mem(x) for x in
               list(range(0xD100, 0xD140)) +
               [0xC020, 0xC021, 0xC022, 0xC025, 0xC026, 0xC027,
                0xC028, 0xC030, 0xC032, 0xC205, 0xC215, 0xC238,
                0xC251, 0xC280, 0xC281]}
report = {
    "rom_size": len(rom),
    "banks": len(banks),
    "breakpoint": f"0x{a.breakpoint:04X}",
    "result": result,
    "steps": steps,
    "events": events[-32:],
    "pc": f"0x{cpu.pc:04X}",
    "sp": f"0x{cpu.sp:04X}",
    "mapper": {f"0x{k:04X}": v for k, v in mapper.items()},
    "interesting_ram": interesting,
    "nonzero_ram": snapshot,
    "read_counts": {f"0x{k:04X}": v for k, v in sorted(reads.items())
                     if 0xC000 <= k <= 0xDFFF},
    "write_counts": {f"0x{k:04X}": v for k, v in sorted(writes.items())
                      if 0xC000 <= k <= 0xDFFF},
}
if error:
    report["error"] = error
a.out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps({k: report[k] for k in
                  ("result", "steps", "pc", "sp", "mapper", "breakpoint")},
                 indent=2))
