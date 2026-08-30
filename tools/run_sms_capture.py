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
p.add_argument("--vdp-wait-pcs", type=str,
               default="0x04E7,0x04EA,0x04EB",
               help="PCs where the bounded diagnostic C008 wait release applies")
p.add_argument("--diagnostic-release-scene-wait", action="store_true",
               help="diagnostic only: also clear C203 at configured wait PCs")
p.add_argument("--irq-every-runs", type=int, default=1,
               help="inject a VBlank-like IM1 IRQ every N native runs; 0 disables")
p.add_argument("--scanline-irq", action="store_true",
               help="schedule VBlank/H-interrupt at SMS scanline boundaries")
p.add_argument("--dega-frame-schedule", action="store_true",
               help="use Dega's frame order: line 192, 193-261, then 0-191")
p.add_argument("--input-value", type=lambda x: int(x, 0), default=0xFF,
               help="value returned by SMS controller ports DC/C0")
p.add_argument("--input-sequence", type=str, default=None,
               help="comma-separated hex/decimal controller values, one per native run")
p.add_argument("--dega-io-semantics", action="store_true",
               help="use Dega-compatible V-counter and active-low controller reads")
p.add_argument("--trace-pc-range", type=str, default="0x3400-0x35A0",
               help="inclusive PC range to trace, for example 0x3400-0x35A0")
p.add_argument("--trace-limit", type=int, default=20000,
               help="maximum number of detailed trace records")
p.add_argument("--trace-every", type=int, default=1,
               help="record one matching event every N trace events")
p.add_argument("--trace-memory-range", type=str, default=None,
               help="inclusive memory range to trace, for example 0xDD00-0xDE37")
p.add_argument("--trace-out", type=Path, default=None,
               help="optional JSON file receiving detailed memory/I/O trace")
p.add_argument("--out", type=Path, required=True)
a = p.parse_args()

def parse_input_sequence(value):
    if not value:
        return []
    try:
        values = [int(item.strip(), 0) & 0xFF
                  for item in value.split(",") if item.strip()]
    except ValueError as exc:
        raise SystemExit(f"invalid --input-sequence: {value!r}") from exc
    if not values:
        raise SystemExit("--input-sequence must contain at least one value")
    return values


input_sequence = parse_input_sequence(a.input_sequence)
try:
    vdp_wait_pcs = {int(item.strip(), 0) for item in a.vdp_wait_pcs.split(",")
                    if item.strip()}
except ValueError as exc:
    raise SystemExit(f"invalid --vdp-wait-pcs: {a.vdp_wait_pcs!r}") from exc
current_input = a.input_value & 0xFF
input_history = []
try:
    trace_start, trace_end = [int(item, 0) for item in a.trace_pc_range.split("-", 1)]
except ValueError as exc:
    raise SystemExit(f"invalid --trace-pc-range: {a.trace_pc_range!r}") from exc
if trace_start > trace_end or not 0 <= trace_start <= 0xFFFF or not 0 <= trace_end <= 0xFFFF:
    raise SystemExit(f"invalid --trace-pc-range: {a.trace_pc_range!r}")
trace_memory_start = trace_memory_end = None
if a.trace_memory_range:
    try:
        trace_memory_start, trace_memory_end = [int(item, 0) for item in
                                                a.trace_memory_range.split("-", 1)]
    except ValueError as exc:
        raise SystemExit(f"invalid --trace-memory-range: {a.trace_memory_range!r}") from exc
    if (trace_memory_start > trace_memory_end or
            not 0 <= trace_memory_start <= 0xFFFF or
            not 0 <= trace_memory_end <= 0xFFFF):
        raise SystemExit(f"invalid --trace-memory-range: {a.trace_memory_range!r}")
trace_records = []
trace_event_count = 0
current_run = 0


def trace_event(kind, address=None, value=None, force=False):
    global trace_event_count
    trace_event_count += 1
    if a.trace_every < 1:
        raise SystemExit("--trace-every must be at least 1")
    if len(trace_records) >= a.trace_limit or "cpu" not in globals():
        return
    if not force and trace_event_count % a.trace_every != 0:
        return
    pc = cpu.pc & 0xFFFF
    if not force and not (trace_start <= pc <= trace_end):
        return
    record = {"run": current_run, "pc": f"0x{pc:04X}", "kind": kind,
              "bank_fffe": mapper[0xFFFE], "bank_ffff": mapper[0xFFFF],
              "a": cpu.a, "b": cpu.b, "c": cpu.c, "d": cpu.d,
              "e": cpu.e, "h": cpu.h, "l": cpu.l}
    if address is not None:
        record["address"] = f"0x{address & 0xFFFF:04X}"
    if value is not None:
        record["value"] = value & 0xFF
    trace_records.append(record)

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
scanline = 192 if a.dega_frame_schedule else 0
hint_counter = 0
pending_irq = False


def ram_index(addr):
    return (addr - 0xC000) & 0x1FFF


def read_mem(addr):
    global vdp_wait_reads
    addr &= 0xFFFF
    # The real SMS clears C008 from a VDP/interrupt path during the call at
    # 04E4. With no VDP timing model, release only this known polling loop
    # after a bounded number of reads; all other RAM remains untouched.
    if addr == 0xC008 and 'cpu' in globals() and cpu.pc in vdp_wait_pcs:
        vdp_wait_reads += 1
        if vdp_wait_reads >= a.vdp_wait_reads:
            ram[ram_index(addr)] = 0
    if (a.diagnostic_release_scene_wait and addr == 0xC203 and
            'cpu' in globals() and cpu.pc in vdp_wait_pcs):
        ram[ram_index(addr)] = 0
    reads[addr] = reads.get(addr, 0) + 1
    if (addr == 0xC008 or 0xC020 <= addr <= 0xC030 or
            0xC200 <= addr <= 0xC251 or addr in mapper or
            (trace_memory_start is not None and trace_memory_start <= addr <= trace_memory_end)):
        read_value = mapper[addr] if addr in mapper else ram[ram_index(addr)]
        trace_event("mem_read", addr, read_value)
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
    if (addr == 0xC008 or 0xC020 <= addr <= 0xC030 or
            0xC200 <= addr <= 0xC251 or addr in mapper or
            (trace_memory_start is not None and trace_memory_start <= addr <= trace_memory_end)):
        trace_event("mem_write", addr, value,
                    force=addr in (0xC008, 0xC203))
    if addr in mapper:
        mapper[addr] = value
    elif 0xC000 <= addr <= 0xFFFF:
        ram[ram_index(addr)] = value


def input_port(port):
    global pending_irq
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
        # Dega clears the Z80 interrupt latch when VDP status is read.
        pending_irq = False
        return value
    if port == 0x7E:
        if a.dega_io_semantics:
            return (scanline - 6) & 0xFF if scanline > 0xDA else scanline & 0xFF
        return 0
    if port == 0x7F:
        return 0x40
    if port in (0xDC, 0xC0):
        value = ((~(current_input & 0x3F)) & 0xFF
                 if a.dega_io_semantics else current_input)
        trace_event("controller_read", port, value, force=True)
        return value
    if port in (0xDD, 0xC1):
        trace_event("region_read", port, 0xFF, force=True)
        # The supplied ROM is Japanese; bit behavior follows Dega's MX_JAPAN.
        return 0xFF
    if port == 0xF2:
        return 0xFF
    return 0xFF


def output_port(port, value):
    global pending_irq
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
            # Dega clears the interrupt latch on VDP control writes.
            pending_irq = False
    # PSG, stereo and FM ports have no bearing on RAM capture.


def request_irq():
    """Latch an SMS interrupt request until the CPU can accept it."""
    global pending_irq
    pending_irq = True
    trace_event("irq_requested", force=True)


def inject_im1_irq():
    """Inject a conservative SMS VBlank IRQ at a native run boundary.

    The Python Z80 binding exposes read-only IFF properties, but its state
    view is writable. IM1 entry is therefore reproduced explicitly: push PC,
    clear IFF1/IFF2, and jump to 0038h. This is deliberately reported as a
    diagnostic approximation until a core with an IRQ latch is used.
    """
    global pending_irq
    if not pending_irq:
        return False
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
    pending_irq = False
    vdp["stat"] |= 0x80
    trace_event("irq_injected", force=True)
    return True


def schedule_scanline_irq():
    """Advance one NTSC scanline and request enabled SMS raster interrupts.

    With ``--dega-frame-schedule``, the order matches MastFrame(): line 192
    first (VBlank status is already visible), then 193..261, then 0..191.
    """
    global scanline, hint_counter
    if a.dega_frame_schedule:
        current = scanline
        scanline = 193 if current == 192 else (0 if current == 261 else current + 1)
    else:
        scanline = (scanline + 1) % 262
        current = scanline

    requested = False
    if current == 193:
        vdp["stat"] |= 0x80
        trace_event("vblank_tick", value=vdp["regs"][1], force=True)
        requested = bool(vdp["regs"][1] & 0x20)
    elif current <= 192:
        if current == 0:
            hint_counter = vdp["regs"][10]
        else:
            hint_counter -= 1
        if hint_counter < 0:
            vdp["stat"] |= 0x40
            requested = bool(vdp["regs"][0] & 0x10)
            hint_counter = vdp["regs"][10]

    if requested:
        request_irq()
    return inject_im1_irq()

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
        current_run = steps + 1
        if input_sequence:
            sequence_index = min(steps, len(input_sequence) - 1)
            current_input = input_sequence[sequence_index]
        input_history.append({"run": steps + 1, "value": current_input})
        event = cpu.run()
        steps += 1
        # run() may stop at the configured tick budget. Re-arm it so the
        # diagnostic runner can continue through multiple frames/events.
        cpu.ticks_to_stop = a.ticks_per_run
        events.append({"event": event, "pc": f"0x{cpu.pc:04X}"})
        if a.scanline_irq:
            if schedule_scanline_irq():
                events[-1]["irq_injected"] = True
        elif a.irq_every_runs and steps % a.irq_every_runs == 0:
            request_irq()
            if inject_im1_irq():
                events[-1]["irq_injected"] = True
        elif pending_irq and inject_im1_irq():
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
    "input": {"default": a.input_value & 0xFF,
              "sequence": input_sequence,
              "dega_io_semantics": a.dega_io_semantics,
              "history_tail": input_history[-64:]},
    "timing": {"vdp_wait_pcs": [f"0x{x:04X}" for x in sorted(vdp_wait_pcs)],
               "scanline_irq": a.scanline_irq,
               "dega_frame_schedule": a.dega_frame_schedule,
               "scanline": scanline, "hint_counter": hint_counter,
               "pending_irq": pending_irq},
    "trace": {"pc_range": [f"0x{trace_start:04X}", f"0x{trace_end:04X}"],
              "memory_range": ([f"0x{trace_memory_start:04X}", f"0x{trace_memory_end:04X}"]
                                if trace_memory_start is not None else None),
              "limit": a.trace_limit, "sample_every": a.trace_every,
              "events_seen": trace_event_count, "records": trace_records},
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
if a.trace_out:
    a.trace_out.write_text(json.dumps({"rom": str(a.rom), "trace": report["trace"]},
                                      indent=2) + "\n", encoding="utf-8")
print(json.dumps({k: report[k] for k in
                  ("result", "steps", "pc", "sp", "mapper", "breakpoint")},
                 indent=2))
