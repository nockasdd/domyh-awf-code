## 📄 Program Structure Templates

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

- [ ] **Avoid inline ASM if possible** Use intrinsics, compiler optimizations
- [ ] **Profile before optimizing** Don't guess, measure
- [ ] **Keep ASM sections minimal** Maintain only critical paths
- [ ] **Use runtime CPU detection** Support multiple instruction sets
- [ ] **Align data properly** 16/32/64-byte for SIMD operations
- [ ] **Follow calling conventions** Preserve callee-saved registers
- [ ] **Document thoroughly** ASM is harder to understand
- [ ] **Test on target hardware** SIMD behavior varies

---
