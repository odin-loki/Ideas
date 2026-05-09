# CPU — hardware OS acceleration in SystemVerilog (early experiment)

> **One Verilog source file plus the conversation that produced it.** The Verilog isn't a general-purpose CPU core — it's a hardware-side accelerator for OS primitives: a hardware BIOS state machine, a syscall dispatch interface, a process table, and context-switch primitives, packaged as `os_accelerator` (and an inner `hardware_bios`).

---

## ⚙️ What this folder is

A two-file research artefact: a long SystemVerilog source describing a hardware-OS-acceleration block, paired with the design-discussion log that produced it. The Verilog file is itself the canonical specification — there is no formal paper here.

| File | Role |
|---|---|
| [`CPU Verilog.txt`](CPU%20Verilog.txt) | SystemVerilog source. Top module `os_accelerator` (parameterised `PROCESS_TABLE_SIZE` / `CONTEXT_SIZE`), inner `hardware_bios` with a six-state machine (`POWER_ON_SELF_TEST`, `HARDWARE_INIT`, `MEMORY_TEST`, `BOOT_SEQUENCE`, `SYSTEM_INIT`, `OS_HANDOFF`), 64-bit syscall interface (`syscall_number`, four-arg `syscall_args`, `syscall_result`, `syscall_complete`). |
| [`CPU Convo Log.txt`](CPU%20Convo%20Log.txt) | Design-discussion transcript that produced the Verilog. |

---

## 🚧 Honest framing

- This is **not a complete CPU core** in the conventional ALU/decoder/pipeline sense — earlier README copy described "CPU specification and architecture" stages (specification → Verilog → simulation → archive) that are not realised in the source file. The actual scope is OS acceleration: hardware BIOS, syscall dispatch, context save/restore, process-table management.
- The Verilog uses `module` declarations nested inside other `module`s (a non-standard SystemVerilog idiom) and is best read as a structural sketch rather than a synthesisable design.
- "Archaeology" is a fair description: this is preserved early experimentation, not a product.

---

## 🔗 Related work in this repo

- [`../100W Wideband Noise Generator/`](../100W%20Wideband%20Noise%20Generator/) — the other Verilog artefact in the repo (Chua-circuit RF noise generator with FPGA supervision)
- [`../Future C++/`](../Future%20C++/) — managed-language design conversation (a software counterpart to this hardware experiment)
- [`../New Classes of Electrical Components/`](../New%20Classes%20of%20Electrical%20Components/) — hybrid discrete-continuous device classes
- [`../Neural Decompiler/`](../Neural%20Decompiler/) — the inverse problem: recovering source from instruction streams

---

[← Back to main README](../README.md)
