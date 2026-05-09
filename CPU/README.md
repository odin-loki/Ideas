# CPU

> **A dual-artefact folder: a sprawling Power-ISA-inspired heterogeneous many-core CPU design *conversation* (16 big OOO cores at 4 GHz with 8-stage pipelines, alongside `4 096` small cores, MOESI cache coherence, DDR5 at `7800 MT/s`, hardware-accelerated virtualisation), paired with a SystemVerilog *sketch* of an `os_accelerator` block whose inner `hardware_bios` state machine moves through `POWER_ON_SELF_TEST → HARDWARE_INIT → MEMORY_TEST → BOOT_SEQUENCE → SYSTEM_INIT → OS_HANDOFF` while the outer block accelerates syscalls, context switches (32 × 64-bit registers + PC/SP/flags), and memory-management (PAGE_FAULT / TLB_MISS / MEMORY_MAP) in hardware.** The unusual move here is putting OS primitives — fork, syscalls, page faults — into RTL rather than software, and pairing the HDL with the architecture-level design discussion that motivates them.

---

## What this folder is

Most CPU-design folders on the open web are either (a) educational toy cores in a few hundred lines of Verilog, or (b) architecture-spec PDFs from major vendors. The "design-conversation + HDL-sketch" pairing is rare, and it is what this folder offers. The conversation log establishes the design *targets* — heterogeneous big.LITTLE-style with 16 large OOO cores plus thousands of small cores, MOESI coherence, four-level cache hierarchy ending in 4 GiB shared L4, DDR5 7800 MT/s, hardware virtualisation, Power-ISA-inspired (not exact-clone) instruction encoding — and the HDL sketch shows what RTL-level OS acceleration might look like at the periphery: an `os_accelerator` module that the OS hands off privileged operations to, with an inner `hardware_bios` that runs the boot state machine.

The design and the sketch are explicitly *not* a buildable CPU. The HDL pattern (nested `module` inside `module`) is not synthesisable as written and would need restructuring. The conversation is a transcript, not a spec. This folder is best read as architecture-fiction with HDL scaffolding — the kind of artefact that pre-dates building anything.

---

## 📑 Source documents

| File | Role |
|---|---|
| [`CPU Verilog.txt`](CPU%20Verilog.txt) | SystemVerilog sketch. `os_accelerator` parameters: `PROCESS_TABLE_SIZE = 1024`, `CONTEXT_SIZE = 512`, syscall args `[4]`. Inner `hardware_bios` enum: `POWER_ON_SELF_TEST`, `HARDWARE_INIT`, `MEMORY_TEST`, `BOOT_SEQUENCE`, `SYSTEM_INIT`, `OS_HANDOFF`. Nested modules: `syscall_accelerator`, `context_switch_accelerator` (`context_t` = 32 × 64-bit + PC/SP/flags), `memory_management_accelerator` (PAGE_FAULT / TLB_MISS / MEMORY_MAP cases). |
| [`CPU Convo Log.txt`](CPU%20Convo%20Log.txt) | Architecture-design conversation log. **L1i / L1d 64 KiB**, **L2 512 KiB**, **L3 4 MiB**, **L4 4 GiB shared**, **MOESI** coherence, **Power ISA v3.1 inspired**, **8-stage OOO** big cores, **4 GHz**, **4 096 small cores**, **DDR5 7800 MT/s**, hardware memory virtualisation. |

---

## 🧠 The architecture (from the conversation log)

| Layer | Spec |
|---|---|
| **Big cores** | 16 × 4 GHz, 8-stage out-of-order, Power-ISA-inspired |
| **Small cores** | 4 096 |
| **Cache hierarchy** | L1i 64 KiB / L1d 64 KiB / L2 512 KiB / L3 4 MiB / L4 4 GiB shared |
| **Coherence** | MOESI |
| **Memory** | DDR5 7800 MT/s |
| **Virtualisation** | Yes (hardware-accelerated) |

## 🧠 The HDL sketch (`CPU Verilog.txt`)

```
os_accelerator
├─ hardware_bios (FSM)
│   POWER_ON_SELF_TEST → HARDWARE_INIT → MEMORY_TEST
│   → BOOT_SEQUENCE → SYSTEM_INIT → OS_HANDOFF
├─ syscall_accelerator (4-argument bundle, dispatches syscall classes)
├─ context_switch_accelerator (32×64-bit regs + PC/SP/flags)
└─ memory_management_accelerator (PAGE_FAULT / TLB_MISS / MEMORY_MAP)
```

The `os_accelerator` is parameterised with `PROCESS_TABLE_SIZE = 1024` and `CONTEXT_SIZE = 512`. Privileged OS operations that traditionally live entirely in kernel software get hardware-accelerated entry paths.

---

## 🚧 Honest caveats

- **Not a buildable CPU.** No silicon, no PPA (power-performance-area) numbers, no synthesis reports, no test bench.
- **Verilog uses nested `module` inside `module`** which is not the conventional synthesisable HDL pattern. Refactoring to instantiated child modules is required before any tools will accept it.
- **Placeholder tasks** (`handle_fork()`, etc.) are stubs.
- **"Power ISA"** is used loosely — sometimes "IBM Power" sometimes "Power ISA inspiration." The design borrows ideas, it doesn't claim to be a Power-ISA-compliant implementation.
- **Conversation is not a specification.** It captures a thought process, not a normative architecture document.

---

## 🎯 What is interesting about this even if it doesn't build

| Thing | Why it's interesting |
|---|---|
| OS primitives in RTL | Inversion of the usual "software handles this" division |
| `hardware_bios` as an FSM | Boot-state-machine as silicon, not BIOS code |
| Syscall bundle `[4]` args | Hardware ABI as an architectural choice, not a software convention |
| Big.LITTLE at 16 + 4 096 | Extreme asymmetry — beyond ARM's typical 8 + 4 |
| Single-folder pairing | Architecture intent + HDL gesture in one place |

---

## 🔗 Related work in this repo

- [`../100W Wideband Noise Generator/`](../100W%20Wideband%20Noise%20Generator/) — sister single-file HDL design (RF rather than CPU)
- [`../Future C++/`](../Future%20C++/) — language-design conversation that complements this hardware design
- [`../New Classes of Electrical Components/`](../New%20Classes%20of%20Electrical%20Components/) — alternative passive devices that might feed silicon-design pipelines
- [`../Cypha/`](../Cypha/) — HRNA inference stack that this CPU might run

---

[← Back to main README](../README.md)
