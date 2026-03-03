---
name: asm
description: "Assembly language patterns for x86/ARM systems. Use when working with .asm/.s files."
detect: ["*.asm", "*.s", "*.S", "__asm", "asm volatile"]
category: language
tier: 2
---

# Assembly Language Patterns DOMYH Awesome Code

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
| **x86 (32-bit)** | NASM, MASM, GAS | Intel/AT&T | MSVC, GCC, Clang | ✅ Yes        |
| **x64 (64-bit)** | NASM, MASM, GAS | Intel/AT&T | GCC, Clang       | ✅ Yes        |
| **x64 (64-bit)** | MASM (ml64.exe) | Intel      | MSVC             | ❌ No inline\* |
| **ARM64**        | GAS             | UAL        | GCC, Clang       | ✅ Yes        |
| **ARM32**        | GAS             | UAL        | GCC, Clang       | ✅ Yes        |
| **RISC-V**       | GAS             | Standard   | GCC              | ✅ Yes        |

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
| **cdecl**    | Stack R→L    | Caller  | EAX    | EAX,ECX,EDX  | Default C   |
| **stdcall**  | Stack R→L    | Callee  | EAX    | EAX,ECX,EDX  | Windows API |
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

### MSVC x64 Use Intrinsics Instead

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

### External ASM File (MASM Windows x64)

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

## 📚 Deep-Dive References

- **SIMD Programming** — SSE, AVX, NEON intrinsics and patterns
  → See [references/simd-programming.md](references/simd-programming.md)

- **Build Commands & Program Structure** — NASM/MASM/GAS templates, Makefile patterns
  → See [references/build-structure.md](references/build-structure.md)

- **Advanced Architectures** — Legacy DOS, RISC-V, Intel AVX10/AMX, modern IDE tools
  → See [references/advanced-architectures.md](references/advanced-architectures.md)

## ✅ Best Practices Checklist

- [ ] **Avoid inline ASM if possible** Use intrinsics, compiler optimizations
- [ ] **Profile before optimizing** Don't guess, measure
- [ ] **Keep ASM sections minimal** Maintain only critical paths
- [ ] **Use runtime CPU detection** Support multiple instruction sets
- [ ] **Align data properly** 16/32/64-byte for SIMD operations
- [ ] **Follow calling conventions** Preserve callee-saved registers
- [ ] **Document thoroughly** ASM is harder to understand
- [ ] **Test on target hardware** SIMD behavior varies

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
