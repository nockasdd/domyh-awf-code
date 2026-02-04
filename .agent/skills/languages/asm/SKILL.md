---
name: asm
detect: ["*.asm", "*.s", "*.S", "__asm", "asm volatile"]
version: "6.1.2"
category: language
tier: 2
---

# Assembly Language Patterns — DOMYH Awesome Code v6.1.2

> Comprehensive guide for x86/x64, ARM64 assembly with C++ integration

## 🔍 Detection Patterns

```yaml
file_extensions:
  - "*.asm" # MASM/NASM
  - "*.s" # GAS (lowercase)
  - "*.S" # GAS with preprocessor

code_patterns:
  # Inline ASM (GCC/Clang)
  - "__asm__"
  - "asm volatile"
  - "__asm"

  # MASM directives
  - ".code"
  - ".data"
  - "PROC"
  - "ENDP"

  # NASM directives
  - "section .text"
  - "section .data"
  - "global _start"

  # GAS directives
  - ".global"
  - ".text"
  - ".data"
```

---

## 🏗️ Architecture Support Matrix

| Arch             | Assembler       | Syntax     | Compiler         | Inline Support |
| ---------------- | --------------- | ---------- | ---------------- | -------------- |
| **x86 (32-bit)** | NASM, MASM, GAS | Intel/AT&T | MSVC, GCC, Clang | ✅ Yes         |
| **x64 (64-bit)** | NASM, MASM, GAS | Intel/AT&T | GCC, Clang       | ✅ Yes         |
| **x64 (64-bit)** | MASM (ml64.exe) | Intel      | MSVC             | ❌ No inline\* |
| **ARM64**        | GAS             | UAL        | GCC, Clang       | ✅ Yes         |
| **ARM32**        | GAS             | UAL        | GCC, Clang       | ✅ Yes         |
| **RISC-V**       | GAS             | Standard   | GCC              | ✅ Yes         |

> \*MSVC x64 does NOT support inline assembly. Use external .asm files or intrinsics.

---

## 🖥️ IDE Setup Guide

### Visual Studio (MASM x64)

```yaml
setup_steps: 1. Install "Desktop development with C++" workload
  2. Right-click project → Build Dependencies → Build Customizations
  3. Check "masm(.targets, .props)" → OK
  4. Add new item → Name with .asm extension
  5. Right-click .asm file → Properties → Item Type → Microsoft Macro Assembler
  6. Configure for x64 platform in Configuration Manager

linker_settings:
  - Entry Point: main (if ASM contains entry)
  - Additional Dependencies: (optional C runtime)
```

### VS Code / Cursor

```json
{
  "extensions": [
    "ms-vscode.cpptools",
    "dan-c-underwood.arm",
    "maziac.asm-code-lens"
  ],
  "settings": {
    "files.associations": {
      "*.asm": "asm",
      "*.s": "asm",
      "*.S": "asm"
    }
  }
}
```

### JetBrains CLion

```yaml
setup:
  - Install "Assembly Language Support" plugin
  - Configure custom build targets for nasm/ml64
  - Use CMake with enable_language(ASM_NASM) or enable_language(ASM_MASM)
```

---

## 📊 Calling Conventions Reference

### x86 (32-bit) Conventions

| Convention   | Args           | Cleanup | Return | Caller-saved | Use Case    |
| ------------ | -------------- | ------- | ------ | ------------ | ----------- |
| **cdecl**    | Stack R→L      | Caller  | EAX    | EAX,ECX,EDX  | Default C   |
| **stdcall**  | Stack R→L      | Callee  | EAX    | EAX,ECX,EDX  | Windows API |
| **fastcall** | ECX,EDX,Stack  | Callee  | EAX    | EAX,ECX,EDX  | Performance |
| **thiscall** | ECX=this,Stack | Callee  | EAX    | EAX,ECX,EDX  | C++ methods |

### x64 Conventions

| Platform             | Integer Args          | Float Args | Return  | Shadow Space |
| -------------------- | --------------------- | ---------- | ------- | ------------ |
| **Windows x64**      | RCX,RDX,R8,R9         | XMM0-3     | RAX     | 32 bytes     |
| **System V (Linux)** | RDI,RSI,RDX,RCX,R8,R9 | XMM0-7     | RAX,RDX | None         |

#### Windows x64 Detail

```asm
; First 4 args: RCX, RDX, R8, R9
; Float args: XMM0, XMM1, XMM2, XMM3
; Caller allocates 32-byte shadow space
; Stack must be 16-byte aligned before CALL

; Example: int func(int a, int b, int c, int d)
mov ecx, a       ; arg1
mov edx, b       ; arg2
mov r8d, c       ; arg3
mov r9d, d       ; arg4
sub rsp, 32      ; shadow space
call func
add rsp, 32      ; cleanup
```

#### System V AMD64 Detail (Linux/macOS)

```asm
; First 6 integer args: RDI, RSI, RDX, RCX, R8, R9
; First 8 float args: XMM0-XMM7
; No shadow space, 128-byte red zone for leaf functions

; Example: int func(int a, int b, int c, int d)
mov edi, a       ; arg1
mov esi, b       ; arg2
mov edx, c       ; arg3
mov ecx, d       ; arg4
call func
```

### ARM64 Convention (AAPCS64)

```asm
; Integer args: X0-X7
; Float args: V0-V7 (D0-D7 for doubles)
; Return: X0 (or X0+X1 for 128-bit)
; Callee-saved: X19-X28, X29 (FP), X30 (LR)
; Stack: 16-byte aligned

; Example function
my_func:
    stp x29, x30, [sp, #-16]!  ; Save FP and LR
    mov x29, sp                  ; Setup frame pointer
    ; ... function body ...
    ldp x29, x30, [sp], #16     ; Restore FP and LR
    ret
```

---

## 🔧 Function Prologue/Epilogue

### x64 Standard Prologue

```asm
my_function:
    ; Prologue
    push rbp                    ; Save caller's base pointer
    mov rbp, rsp                ; Set new base pointer
    sub rsp, 32                 ; Reserve space for locals + shadow

    ; Save non-volatile registers if needed
    push rbx
    push r12
    push r13

    ; ... function body ...

    ; Epilogue
    pop r13
    pop r12
    pop rbx
    leave                       ; mov rsp, rbp; pop rbp
    ret
```

### Leaf Function (No Calls)

```asm
; Leaf functions can skip prologue/epilogue
; Linux: Can use 128-byte red zone below RSP
leaf_add:
    add rdi, rsi                ; a + b
    mov rax, rdi                ; return result
    ret
```

---

## 💻 Inline Assembly

### GCC Extended Syntax

```c
// Syntax: asm volatile ("template" : outputs : inputs : clobbers)

// Read timestamp counter
static inline uint64_t rdtsc(void) {
    uint32_t lo, hi;
    __asm__ volatile (
        "rdtsc"
        : "=a" (lo), "=d" (hi)  // Outputs: eax → lo, edx → hi
        :                         // No inputs
        :                         // No clobbers
    );
    return ((uint64_t)hi << 32) | lo;
}

// Atomic compare-and-swap
static inline bool cas(uint64_t *ptr, uint64_t old, uint64_t new_val) {
    uint64_t prev;
    __asm__ volatile (
        "lock cmpxchgq %2, %1"
        : "=a" (prev), "+m" (*ptr)   // Output: rax → prev, memory update
        : "r" (new_val), "0" (old)   // Input: register, old in rax
        : "memory"                    // Clobber: memory barrier
    );
    return prev == old;
}

// CPUID
static inline void cpuid(uint32_t level, uint32_t *eax, uint32_t *ebx,
                          uint32_t *ecx, uint32_t *edx) {
    __asm__ volatile (
        "cpuid"
        : "=a" (*eax), "=b" (*ebx), "=c" (*ecx), "=d" (*edx)
        : "a" (level), "c" (0)
    );
}
```

### MSVC x64 — Use Intrinsics Instead

```c
// MSVC x64 does NOT support inline asm
// Use intrinsics from <intrin.h>

#include <intrin.h>

uint64_t rdtsc_msvc(void) {
    return __rdtsc();
}

// Or link external .asm file
extern "C" uint64_t custom_asm_function(uint64_t arg);
```

### External ASM File (MASM — Windows x64)

```asm
; custom_asm.asm
.code

; Export for C/C++
public custom_asm_function

; int64_t custom_asm_function(int64_t arg)
custom_asm_function PROC
    ; RCX = first arg (Windows x64)
    mov rax, rcx
    shl rax, 1          ; multiply by 2
    ret
custom_asm_function ENDP

END
```

```cpp
// In C++ code
extern "C" int64_t custom_asm_function(int64_t arg);

int main() {
    int64_t result = custom_asm_function(42);  // Returns 84
    return 0;
}
```

---

## ⚡ SIMD Programming

### Intrinsics vs Inline ASM Decision

```yaml
recommendation:
  use_intrinsics:
    - Portable across compilers
    - Compiler can optimize around them
    - Easier to maintain
    - Better for SSE/AVX/AVX-512

  use_inline_asm:
    - CPU-specific features not in intrinsics
    - Precise instruction control needed
    - Very small, critical code paths
```

### SSE/AVX Intrinsics Example

```c
#include <immintrin.h>

// Add 8 floats using AVX
void vector_add_avx(float* result, const float* a, const float* b) {
    __m256 va = _mm256_load_ps(a);    // Load 8 floats from a
    __m256 vb = _mm256_load_ps(b);    // Load 8 floats from b
    __m256 vr = _mm256_add_ps(va, vb); // Add
    _mm256_store_ps(result, vr);       // Store result
}

// Dot product using SSE
float dot_product_sse(const float* a, const float* b, int n) {
    __m128 sum = _mm_setzero_ps();
    for (int i = 0; i < n; i += 4) {
        __m128 va = _mm_load_ps(&a[i]);
        __m128 vb = _mm_load_ps(&b[i]);
        sum = _mm_add_ps(sum, _mm_mul_ps(va, vb));
    }
    // Horizontal add
    sum = _mm_hadd_ps(sum, sum);
    sum = _mm_hadd_ps(sum, sum);
    return _mm_cvtss_f32(sum);
}
```

### Runtime CPU Feature Detection

```c
#include <cpuid.h>  // GCC/Clang

bool has_avx2(void) {
    unsigned int eax, ebx, ecx, edx;
    __cpuid(7, eax, ebx, ecx, edx);
    return (ebx & (1 << 5)) != 0;  // AVX2 bit
}

// Dispatch based on CPU features
void process_data(float* data, int n) {
    if (has_avx2()) {
        process_avx2(data, n);
    } else if (has_sse4()) {
        process_sse4(data, n);
    } else {
        process_scalar(data, n);
    }
}
```

### ARM64 NEON Intrinsics

```c
#include <arm_neon.h>

// Add 4 floats using NEON
void vector_add_neon(float* result, const float* a, const float* b) {
    float32x4_t va = vld1q_f32(a);     // Load 4 floats
    float32x4_t vb = vld1q_f32(b);     // Load 4 floats
    float32x4_t vr = vaddq_f32(va, vb); // Add
    vst1q_f32(result, vr);              // Store
}

// Horizontal sum
float horizontal_sum_neon(float32x4_t v) {
    float32x2_t sum = vadd_f32(vget_low_f32(v), vget_high_f32(v));
    sum = vpadd_f32(sum, sum);
    return vget_lane_f32(sum, 0);
}
```

---

## 📁 Program Structure Templates

### NASM (Linux x64)

```asm
; program.asm
section .data
    msg db "Hello, World!", 10
    len equ $ - msg

section .bss
    buffer resb 256

section .text
    global _start

_start:
    ; sys_write(1, msg, len)
    mov rax, 1          ; syscall: write
    mov rdi, 1          ; fd: stdout
    mov rsi, msg        ; buffer
    mov rdx, len        ; count
    syscall

    ; sys_exit(0)
    mov rax, 60         ; syscall: exit
    xor rdi, rdi        ; status: 0
    syscall
```

### MASM (Windows x64)

```asm
; program.asm
.data
    msg db "Hello, World!", 0

.code
    externdef printf:proc

main PROC
    sub rsp, 40         ; Shadow space + alignment
    lea rcx, msg        ; First arg
    call printf
    add rsp, 40
    xor eax, eax        ; Return 0
    ret
main ENDP

END
```

### GAS (ARM64)

```asm
// program.s
.data
msg:    .ascii "Hello, World!\n"
len = . - msg

.text
.global _start

_start:
    mov x8, #64         // sys_write
    mov x0, #1          // fd: stdout
    ldr x1, =msg        // buffer
    mov x2, #len        // count
    svc #0

    mov x8, #93         // sys_exit
    mov x0, #0          // status
    svc #0
```

---

## 🔨 Build Commands

### NASM + LD (Linux)

```bash
# Compile
nasm -f elf64 program.asm -o program.o

# Link
ld program.o -o program

# Or with C runtime
nasm -f elf64 program.asm -o program.o
gcc program.o -o program -no-pie
```

### MASM + MSVC (Windows)

```powershell
# Compile ASM
ml64 /c program.asm /Fo program.obj

# Link with C++ code
cl /c main.cpp
link main.obj program.obj /OUT:main.exe

# Or combined in Visual Studio project
# Just add .asm file after enabling MASM build customization
```

### GAS + GCC (Cross-platform)

```bash
# Compile
as program.s -o program.o

# Link
ld program.o -o program

# Or with GCC
gcc -c program.s -o program.o
gcc main.c program.o -o main
```

### CMake Integration

```cmake
# Enable ASM
enable_language(ASM_NASM)
# or
enable_language(ASM_MASM)

# Add ASM sources
add_executable(myprogram
    main.cpp
    asm_routines.asm
)
```

---

## ✅ Best Practices Checklist

- [ ] **Avoid inline ASM if possible** — Use intrinsics, compiler optimizations
- [ ] **Profile before optimizing** — Don't guess, measure
- [ ] **Keep ASM sections minimal** — Maintain only critical paths
- [ ] **Use runtime CPU detection** — Support multiple instruction sets
- [ ] **Align data properly** — 16/32/64-byte for SIMD operations
- [ ] **Follow calling conventions** — Preserve callee-saved registers
- [ ] **Document thoroughly** — ASM is harder to understand
- [ ] **Test on target hardware** — SIMD behavior varies

---

## 🔍 Common Issues & Solutions

| Issue                     | Cause                     | Solution                          |
| ------------------------- | ------------------------- | --------------------------------- |
| MSVC x64 inline ASM error | Not supported             | Use external .asm or intrinsics   |
| Segfault in SIMD          | Misaligned data           | Use `alignas(32)` or `_mm_malloc` |
| Function not found        | Name mangling             | Use `extern "C"` in C++           |
| Stack corruption          | Wrong calling convention  | Check shadow space, register save |
| Performance worse than C  | Compiler optimizes better | Profile, let compiler do its job  |

---

## 🏛️ Legacy Assemblers & DOS

### Assembler Comparison

| Assembler | Syntax    | Linker | 16-bit | Direct .COM | Best For              |
| --------- | --------- | ------ | ------ | ----------- | --------------------- |
| **NASM**  | Intel     | LD/GCC | ✅     | ✅          | Cross-platform        |
| **MASM**  | Intel     | LINK   | ✅     | ❌          | Windows/Visual Studio |
| **GAS**   | AT&T      | LD     | ✅     | ❌          | GCC/Linux ecosystem   |
| **TASM**  | Intel     | TLINK  | ✅     | ✅          | DOS + Turbo Debugger  |
| **FASM**  | Intel     | None   | ✅     | ✅          | Self-contained, fast  |
| **A86**   | Custom    | None   | ✅     | ✅          | Simple DOS programs   |
| **YASM**  | NASM-like | LD     | ✅     | ✅          | NASM alternative      |
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
  max_size: 16 rows × 64 bytes

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
    _tile_dpbf16ps(2, 0, 1); // C += A × B (BF16)
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

_DOMYH Awesome Code v6.1.2 • Assembly Language Skill • Comprehensive Guide_
