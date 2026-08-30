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
p.add_argument("--irq-every-runs", type=int, default=1,
               help="inject a VBlank-like IM1 IRQ every N native runs; 0 disables")
p.add_argument("--out", type=Path, required=True)
a = p.parse_args()

rom = a.rom.read_bytes()
if len(rom) % 0x4000:
    raise SystemExit(f"ROM size must be a multiple of 0x4000, got {len(rom):#x}")
banks = [rom[i:i + 0x4000] for i in range(0, len(rom), 0x4000)]
ram = bytearray(0x2000)
vram = bytearray(0x4000)
cram = bytearray(0x40)
vdp = {"low": 0, "wait": 0, "addr": 0, "mode": 0, "stat": 0,
       "regs": bytearray(0x10)}
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
    port &= 0xFF
    if port == 0xBE:
        value = vram[vdp["addr"] & 0x3FFF]
        vdp["addr"] = (vdp["addr"] + 1) & 0x3FFF
        vdp["wait"] = 0
        return value
    if port == 0xBF:
        value = vdp["stat"] | 0x20
        vdp["stat"] &= 0x3F
        vdp["wait"] = 0
        return value
    if port == 0x7E:
        return 0
    if port == 0x7F:
        return 0x40
    if port in (0xDC, 0xC0):
        return 0xFF
    if port in (0xDD, 0xC1):
        # The supplied ROM is Japanese; bit behavior follows Dega's MX_JAPAN.
        return 0xFF
    if port == 0xF2:
        return 0xFF
    return 0xFF


def output_port(port, value):
    port &= 0xFF
    value &= 0xFF
    if port == 0xBE:
        if vdp["mode"] == 3:
            cram[vdp["addr"] & 0x3F] = value
        else:
            vram[vdp["addr"] & 0x3FFF] = value
        vdp["addr"] = (vdp["addr"] + 1) & 0x3FFF
        vdp["wait"] = 0
    elif port == 0xBF:
        if not vdp["wait"]:
            vdp["low"] = value
            vdp["wait"] = 1
        else:
            command = (value << 8) | vdp["low"]
            vdp["addr"] = command & 0x3FFF
            vdp["mode"] = (command >> 14) & 3
            if (command & 0xF000) == 0x8000:
                index = (command >> 8) & 0x3F
                if index < 0x10:
                    vdp["regs"][index] = command & 0xFF
            vdp["wait"] = 0
            vdp["stat"] &= 0x3F
    # PSG, stereo and FM ports have no bearing on RAM capture.


def inject_im1_irq():
    """Inject a conservative SMS VBlank IRQ at a native run boundary.

    The Python Z80 binding exposes read-only IFF properties, but its state
    view is writable. IM1 entry is therefore reproduced explicitly: push PC,
    clear IFF1/IFF2, and jump to 0038h. This is deliberately reported as a
    diagnostic approximation until a core with an IRQ latch is used.
    """
    state = cpu.get_state_view()
    if not state[34] or cpu.int_disabled:
        return False
    sp = (cpu.sp - 2) & 0xFFFF
    write_mem(sp, cpu.pc & 0xFF)
    write_mem((sp + 1) & 0xFFFF, cpu.pc >> 8)
    cpu.sp = sp
    state[34] = 0
    state[35] = 0
    cpu.pc = 0x0038
    vdp["stat"] |= 0x80
    return True

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
        if a.irq_every_runs and steps % a.irq_every_runs == 0:
            if inject_im1_irq():
                events[-1]["irq_injected"] = True
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
    "vdp": {"addr": vdp["addr"], "mode": vdp["mode"], "stat": vdp["stat"],
            "regs": list(vdp["regs"]), "vram_nonzero": sum(x != 0 for x in vram),
            "cram_nonzero": sum(x != 0 for x in cram)},
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
