## 🏛️ Legacy Assemblers & DOS

### Assembler Comparison

| Assembler | Syntax    | Linker | 16-bit | Direct .COM | Best For              |
| --------- | --------- | ------ | ------ | ----------- | --------------------- |
| **NASM**  | Intel     | LD/GCC | ✅    | ✅         | Cross-platform        |
| **MASM**  | Intel     | LINK   | ✅    | ❌          | Windows/Visual Studio |
| **GAS**   | AT&T      | LD     | ✅    | ❌          | GCC/Linux ecosystem   |
| **TASM**  | Intel     | TLINK  | ✅    | ✅         | DOS + Turbo Debugger  |
| **FASM**  | Intel     | None   | ✅    | ✅         | Self-contained, fast  |
| **A86**   | Custom    | None   | ✅    | ✅         | Simple DOS programs   |
| **YASM**  | NASM-like | LD     | ✅    | ✅         | NASM alternative      |
| **HLA**   | High-lvl  | Link   | ❌     | ❌          | Learning ASM          |

### 16-bit Real Mode (8086/8088)

```asm
; NASM 16-bit DOS .COM program
org 0x100              ; .COM files load at 100h

section .text
start:
    mov ah, 09h        ; DOS print string
    mov dx, message
    int 21h

    mov ah, 4Ch        ; DOS exit
    int 21h

section .data
message db "Hello, DOS!", 13, 10, "$"
```

### DOSBox Development Setup

```yaml
setup:
  1. Install DOSBox/DOSBox-X
  2. Mount work directory: mount c c:\asm
  3. Install assembler (TASM/MASM/NASM)
  4. Use DEBUG.EXE or Turbo Debugger

debuggers:
  DEBUG.EXE: "Built-in DOS debugger (line-oriented)"
  Turbo Debugger: "Full-screen, source-level debugging"
  D86: "A86's companion debugger"
```

### CPU Evolution (16 → 32 → 64-bit)

| CPU     | Year | Bits | Address | Mode         | Memory |
| ------- | ---- | ---- | ------- | ------------ | ------ |
| 8086    | 1978 | 16   | 20-bit  | Real         | 1 MB   |
| 8088    | 1979 | 16   | 20-bit  | Real         | 1 MB   |
| 80286   | 1982 | 16   | 24-bit  | Real/Prot    | 16 MB  |
| 80386   | 1985 | 32   | 32-bit  | Real/Prot/V8 | 4 GB   |
| 80486   | 1989 | 32   | 32-bit  | Real/Prot/V8 | 4 GB   |
| Pentium | 1993 | 32   | 32-bit  | Real/Prot/V8 | 4 GB   |
| x64     | 2003 | 64   | 48-bit  | Long         | 256 TB |

---

## 🆕 RISC-V Assembly

### Register Map (RV64I)

| ABI Name | Reg    | Role            | Preserved |
| -------- | ------ | --------------- | --------- |
| zero     | x0     | Hard-wired zero | N/A       |
| ra       | x1     | Return address  | No        |
| sp       | x2     | Stack pointer   | Yes       |
| gp       | x3     | Global pointer  | N/A       |
| tp       | x4     | Thread pointer  | N/A       |
| t0-t2    | x5-7   | Temporaries     | No        |
| s0/fp    | x8     | Saved/Frame ptr | Yes       |
| s1       | x9     | Saved register  | Yes       |
| a0-a7    | x10-17 | Args / Return   | No        |
| s2-s11   | x18-27 | Saved registers | Yes       |
| t3-t6    | x28-31 | Temporaries     | No        |

### Calling Convention

```asm
# RISC-V function example
my_function:
    addi sp, sp, -16     # Allocate stack
    sd ra, 8(sp)         # Save return address
    sd s0, 0(sp)         # Save s0

    # ... function body ...
    # Args in a0-a7, return in a0/a1

    ld s0, 0(sp)         # Restore s0
    ld ra, 8(sp)         # Restore ra
    addi sp, sp, 16      # Deallocate
    ret
```

### Common Extensions

| Ext | Description         |
| --- | ------------------- |
| M   | Multiply/Divide     |
| A   | Atomics             |
| F   | Single-precision FP |
| D   | Double-precision FP |
| C   | Compressed (16-bit) |
| V   | Vector extension    |

---

## 🆕 Intel AVX10 & AMX (2025-2026)

### AVX10.2 (June 2025)

```yaml
features:
  - Mixed-precision: FP16, BF16 operations
  - IEEE-754-2019 NaN propagation
  - Unified P-core/E-core support
  - Embedded rounding in 256-bit mode
  - 32 vector registers (ZMM0-31)

detection:
  CPUID: Check AVX10 version via CPUID.07H
```

### Intel AMX (Sapphire Rapids+)

```yaml
description: "Accelerate matrix operations for AI/ML"

tiles:
  count: 8 (TMM0-TMM7)
  max_size: 16 rows Ã— 64 bytes

data_types:
  - BF16 (Brain Float 16)
  - INT8 (8-bit integer)
  - FP16 (Half precision)

speedup: "Up to 10x for deep learning"
```

### AMX Intrinsics Example

```c
#include <immintrin.h>

void amx_matmul_bf16(void* c, void* a, void* b) {
    _tile_loadd(0, a, 64);   // Load A → TMM0
    _tile_loadd(1, b, 64);   // Load B → TMM1
    _tile_dpbf16ps(2, 0, 1); // C += A Ã— B (BF16)
    _tile_stored(2, c, 64);  // Store result
}
```

---

## 🛠️ Modern IDE Tools (2025-2026)

### VS Code Extensions

| Extension                 | Purpose                |
| ------------------------- | ---------------------- |
| `ms-vscode.cpptools`      | C/C++ IntelliSense     |
| `maziac.asm-code-lens`    | ASM syntax + debugging |
| `dan-c-underwood.arm`     | ARM assembly support   |
| `13xforever.language-x86` | x86/x64 syntax         |
| `Cortex-Debug`            | ARM embedded debugging |

### ARM-Specific Tools

| Tool           | Description                     |
| -------------- | ------------------------------- |
| ArmLS          | ARM64 language server (LSP)     |
| Arm Dev Studio | Full IDE + Performance Analyzer |
| QEMU           | ARM64/RISC-V emulation          |

### Online Assembly Tools

| Tool               | URL                      |
| ------------------ | ------------------------ |
| Compiler Explorer  | godbolt.org              |
| ASM Editor (specy) | asm-editor.specy.app     |
| onlinegdb          | onlinegdb.com/online_asm |

---

_DOMYH Awesome Code Assembly Language Skill Comprehensive Guide_
