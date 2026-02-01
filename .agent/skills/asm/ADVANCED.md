# Assembly — Advanced Patterns

# DOMYH Agent v4.3 — Tier 3 Reference

## Table of Contents

- [Windows x64 Deep Dive](#windows-x64-deep-dive)
- [Linux System Programming](#linux-system-programming)
- [SIMD Advanced Patterns](#simd-advanced-patterns)
- [Security & Exploit Development](#security--exploit-development)
- [Performance Optimization](#performance-optimization)
- [Reverse Engineering Patterns](#reverse-engineering-patterns)

---

## Windows x64 Deep Dive

### Microsoft x64 ABI Complete Reference

```yaml
registers:
  volatile: [RAX, RCX, RDX, R8, R9, R10, R11, XMM0-XMM5]
  nonvolatile: [RBX, RBP, RDI, RSI, RSP, R12-R15, XMM6-XMM15]

arguments:
  integer: [RCX, RDX, R8, R9] # Then stack
  float: [XMM0, XMM1, XMM2, XMM3]

shadow_space: 32 # bytes, ALWAYS allocated by caller
stack_alignment: 16 # bytes, before CALL instruction

return:
  integer: RAX # up to 64 bits
  float: XMM0 # or ST(0) for x87
  large: # >64 bits or non-trivial
    caller_allocates_memory: true
    address_in: RCX # shifts other args right
```

### SEH (Structured Exception Handling)

```asm
; Function with exception handling
MyFunction PROC FRAME
    ; Prolog with unwind codes
    push rbp
    .pushreg rbp

    mov rbp, rsp
    .setframe rbp, 0

    sub rsp, 32
    .allocstack 32

    .endprolog

    ; Function body...

    ; Epilog
    add rsp, 32
    pop rbp
    ret
MyFunction ENDP
```

### Windows API Calling Example

```asm
.data
    caption db "Title", 0
    message db "Hello from ASM!", 0

.code
    externdef MessageBoxA:proc
    externdef ExitProcess:proc

main PROC
    sub rsp, 40          ; Shadow space + alignment

    xor r9d, r9d         ; uType = MB_OK
    lea r8, caption      ; lpCaption
    lea rdx, message     ; lpText
    xor ecx, ecx         ; hWnd = NULL
    call MessageBoxA

    xor ecx, ecx         ; exit code
    call ExitProcess
main ENDP

END
```

---

## Linux System Programming

### Syscall Table (x64) — Common Operations

```asm
; System call convention:
; RAX = syscall number
; Args: RDI, RSI, RDX, R10, R8, R9
; Return: RAX (-errno on error)
; Clobbered: RCX, R11

; File operations
; 0 = read(fd, buf, count)
; 1 = write(fd, buf, count)
; 2 = open(path, flags, mode)
; 3 = close(fd)

; Memory operations
; 9 = mmap(addr, len, prot, flags, fd, off)
; 11 = munmap(addr, len)
; 12 = brk(addr)

; Process operations
; 57 = fork()
; 59 = execve(path, argv, envp)
; 60 = exit(status)
; 62 = kill(pid, sig)

; Socket operations
; 41 = socket(domain, type, protocol)
; 42 = connect(fd, addr, len)
; 43 = accept(fd, addr, len)
; 44 = sendto(fd, buf, len, flags, addr, len)
; 45 = recvfrom(fd, buf, len, flags, addr, len)
```

### mmap Example — Executable Memory

```asm
section .text
global allocate_executable

; void* allocate_executable(size_t size)
allocate_executable:
    push rbp
    mov rbp, rsp

    ; mmap(NULL, size, PROT_READ|PROT_WRITE|PROT_EXEC,
    ;      MAP_PRIVATE|MAP_ANONYMOUS, -1, 0)
    mov rax, 9           ; sys_mmap
    xor rdi, rdi         ; addr = NULL
    mov rsi, rdi         ; size from arg (already in rsi)
    mov rdx, 7           ; PROT_READ|PROT_WRITE|PROT_EXEC
    mov r10, 0x22        ; MAP_PRIVATE|MAP_ANONYMOUS
    mov r8, -1           ; fd = -1
    xor r9, r9           ; offset = 0
    syscall

    pop rbp
    ret
```

### Fork/Exec Pattern

```asm
section .data
    path db "/bin/sh", 0
    argv dq path, 0

section .text
global spawn_shell

spawn_shell:
    ; fork()
    mov rax, 57
    syscall

    test rax, rax
    jnz .parent          ; Parent: rax = child PID

    ; Child process
    ; execve("/bin/sh", ["/bin/sh", NULL], NULL)
    mov rax, 59
    lea rdi, [rel path]
    lea rsi, [rel argv]
    xor rdx, rdx         ; envp = NULL
    syscall

    ; execve doesn't return on success
    mov rax, 60
    xor rdi, rdi
    syscall

.parent:
    ; Parent continues here
    ret
```

---

## SIMD Advanced Patterns

### AVX-512 Programming

```asm
; AVX-512 requires EVEX prefix
; New features: masking, embedded broadcast, rounding control

section .data
    align 64
    vec_a: times 16 dd 1.0
    vec_b: times 16 dd 2.0
    result: times 16 dd 0.0

section .text
global avx512_add

; void avx512_add(float* result, float* a, float* b)
avx512_add:
    vmovaps zmm0, [rsi]           ; Load 16 floats
    vaddps zmm0, zmm0, [rdx]      ; Add 16 floats
    vmovaps [rdi], zmm0           ; Store result
    ret

; Masked operation
avx512_conditional_add:
    ; k1 = mask register
    vmovaps zmm0, [rsi]
    vaddps zmm0 {k1}, zmm0, [rdx] ; Only add where mask bit = 1
    vmovaps [rdi], zmm0
    ret
```

### Horizontal Operations

```asm
; Sum all elements in YMM register (8 floats)
horizontal_sum_avx:
    ; ymm0 = [a, b, c, d, e, f, g, h]
    vextractf128 xmm1, ymm0, 1     ; xmm1 = [e, f, g, h]
    vaddps xmm0, xmm0, xmm1        ; xmm0 = [a+e, b+f, c+g, d+h]
    vhaddps xmm0, xmm0, xmm0       ; xmm0 = [a+e+b+f, c+g+d+h, ...]
    vhaddps xmm0, xmm0, xmm0       ; xmm0 = [sum, ...]
    ; Result in xmm0[0]
    ret

; Maximum element in YMM
horizontal_max_avx:
    vextractf128 xmm1, ymm0, 1
    vmaxps xmm0, xmm0, xmm1
    vshufps xmm1, xmm0, xmm0, 0x0E  ; Swap high/low pairs
    vmaxps xmm0, xmm0, xmm1
    vshufps xmm1, xmm0, xmm0, 0x01  ; Swap adjacent
    vmaxps xmm0, xmm0, xmm1
    ret
```

### String Operations with SSE4.2

```asm
; Fast strlen using PCMPISTRI
sse42_strlen:
    mov rax, rdi
    pxor xmm0, xmm0              ; Zero for comparison

.loop:
    pcmpistri xmm0, [rax], 0x08  ; Find null terminator
    jnz .not_found
    add rax, rcx                  ; RCX = position of null
    sub rax, rdi                  ; Calculate length
    ret

.not_found:
    add rax, 16
    jmp .loop
```

---

## Security & Exploit Development

### Shellcode Writing

```asm
; Position-independent execve("/bin/sh")
; Size: 27 bytes

bits 64

global _start

_start:
    xor rsi, rsi         ; argv = NULL
    push rsi             ; Push null terminator
    mov rdi, 0x68732f2f6e69622f  ; "/bin//sh" in little endian
    push rdi
    mov rdi, rsp         ; rdi = pointer to "/bin//sh"
    xor rdx, rdx         ; envp = NULL
    push 59              ; execve syscall number
    pop rax
    syscall
```

### Return-Oriented Programming (ROP) Gadgets

```asm
; Common useful gadgets
pop_rdi_ret:
    pop rdi
    ret

pop_rsi_ret:
    pop rsi
    ret

pop_rdx_ret:
    pop rdx
    ret

; Stack pivot
xchg_rax_rsp_ret:
    xchg rax, rsp
    ret

; Write-what-where
mov_ptr_rdi_rax_ret:
    mov [rdi], rax
    ret
```

### Anti-Analysis Techniques

```asm
; Timing-based anti-debug
check_debugger:
    rdtsc
    mov r8, rax          ; Save first timestamp

    ; Some operations
    xor eax, eax
    cpuid                ; Serialize

    rdtsc
    sub rax, r8          ; Time difference

    cmp rax, 1000        ; Threshold (adjust as needed)
    ja .debugger_detected

    xor eax, eax
    ret

.debugger_detected:
    mov eax, 1
    ret
```

---

## Performance Optimization

### Cache-Friendly Data Access

```asm
; Prefetch for performance
prefetch_loop:
    mov rcx, rdi         ; data pointer
    mov rdx, rsi         ; count

.loop:
    prefetcht0 [rcx + 256]  ; Prefetch ahead

    ; Process 64 bytes (cache line)
    vmovaps ymm0, [rcx]
    vmovaps ymm1, [rcx + 32]
    ; ... processing ...
    vmovaps [rcx], ymm0
    vmovaps [rcx + 32], ymm1

    add rcx, 64
    sub rdx, 16          ; 16 floats per iteration
    jnz .loop

    ret
```

### Branch Prediction Hints

```asm
; Use cold/hot section hints
section .text.hot

hot_path:
    cmp eax, 0
    jne .unlikely        ; Predict taken

    ; Hot path code here
    ret

section .text.cold
.unlikely:
    ; Cold path code here
    ret
```

### Memory Barrier Examples

```asm
; Full fence
full_barrier:
    mfence
    ret

; Load fence
load_barrier:
    lfence
    ret

; Store fence
store_barrier:
    sfence
    ret

; Acquire semantics (load-acquire)
load_acquire:
    mov rax, [rdi]
    lfence               ; Prevent loads from reordering after
    ret

; Release semantics (store-release)
store_release:
    sfence               ; Prevent stores from reordering before
    mov [rdi], rsi
    ret
```

---

## Reverse Engineering Patterns

### Common Compiler Patterns

```asm
; Switch-case jump table (optimized)
; Usually generated for dense cases
switch_example:
    cmp eax, 5           ; Check bounds
    ja .default

    lea rcx, [rel jump_table]
    movsxd rax, dword [rcx + rax*4]
    add rax, rcx
    jmp rax

jump_table:
    dd case_0 - jump_table
    dd case_1 - jump_table
    dd case_2 - jump_table
    ; ...

; C++ virtual call
; mov rax, [rdi]        ; Load vtable pointer
; call [rax + 0x10]     ; Call vtable[2]

; Stack canary check
; mov rax, fs:[0x28]    ; Get canary from TLS
; mov [rsp + N], rax    ; Store on stack
; ...function body...
; xor rax, [rsp + N]    ; Check canary
; jne __stack_chk_fail
```

### Identifying Constructs

```asm
; Heap allocation pattern
; call malloc
; or
; mov edi, size
; call operator new
; Result in rax

; Object constructor call pattern
; lea rdi, [rax]        ; this pointer
; call Constructor

; Exception handling (C++)
; Look for:
; - _Unwind_Resume
; - __cxa_throw
; - landing pads in .eh_frame

; std::string (libstdc++)
; SSO: string data inline if len <= 15
; Large: ptr to heap at offset 0
```

### Deobfuscation Hints

```asm
; Opaque predicate (always true)
; mov eax, 5
; imul eax, eax         ; eax = 25
; and eax, 1            ; LSB of 25 = 1
; jnz .actual_code      ; Always taken

; Dead code after unconditional jump
; jmp next
; db 0xE8               ; Fake call opcode
; next:

; Anti-disassembly with overlapping instructions
; Be aware of:
; - Instruction misalignment
; - Jump into middle of instruction
```

---

## ARM64 Advanced Topics

### SVE (Scalable Vector Extension)

```asm
// SVE uses predicate registers (p0-p15)
// Vector length is implementation-defined (128-2048 bits)

sve_add:
    whilelo p0.s, xzr, x2    // Create predicate mask
    ld1w z0.s, p0/z, [x0]    // Load with predicate
    ld1w z1.s, p0/z, [x1]    // Load with predicate
    fadd z0.s, z0.s, z1.s    // Vector add
    st1w z0.s, p0, [x0]      // Store with predicate
    ret
```

### Apple Silicon Specifics

```asm
// Apple M-series uses custom calling convention
// x18 is reserved for OS
// Thread-local storage via tpidrro_el0

apple_tls_access:
    mrs x0, tpidrro_el0      // Read TLS base
    ldr x0, [x0, #OFFSET]    // Load TLS variable
    ret
```

---

_DOMYH Agent v4.3 — Advanced Assembly Reference_
