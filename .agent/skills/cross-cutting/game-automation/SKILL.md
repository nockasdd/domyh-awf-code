---
name: game-automation
description: "Game automation and low-level runtime tooling for memory, hooking, injection, input, networking, bot AI, kernel, hypervisor, and WebView2. Use when working with C++ game automation projects, DLL injection, or emulator automation."
detect: ["*.cpp", "*.h", "*.hpp", "*.cxx", "scripts/**/*.lua", "CMakeLists.txt", "*.vcxproj", "*.sln"]
category: cross-cutting
tier: 1
---

# Game Automation Systems

> C++20 game automation: memory, hooking, injection, networking, bot AI, kernel, hypervisor, DirectX overlay, WebView2

## 📦 Data Files

| File | Content | Records |
| ---- | ------- | ------- |
| `memory-patterns.yaml` | RPM/WPM, pointer chains, AOB scanner, module base, RAII | ~25 |
| `hooking-patterns.yaml` | 6 libraries + 5 hook types (VMT, IAT, VEH, inline, trampoline) | ~20 |
| `injection-methods.yaml` | CRT, manual mapping, reflective, APC, thread hijack, sideload | ~12 |
| `concurrency-patterns.yaml` | jthread, coroutines, thread pool, SPSC queue, frame budget | ~25 |
| `networking-patterns.yaml` | WSASend/WSARecv hooks, packet parsing, encryption bypass, IPC | ~15 |
| `input-vision-patterns.yaml` | 5-level input, OpenCV, Tesseract, BitBlt, DX overlay | ~15 |
| `bot-architecture.yaml` | FSM, HFSM, BT, GOAP, task scheduler, emulator CLIs | ~15 |
| `kernel-mode-patterns.yaml` | KMDF/WDM, MmCopyVirtualMemory, CR3, MDL, kdmapper, IOCTL | ~15 |
| `hypervisor-patterns.yaml` | VT-x/AMD-V, EPT hooking, DMA FPGA, PCILeech, firmware | ~12 |
| `game-engine-re.yaml` | UE4/5 SDK (Dumper-7), Unity IL2CPP, ReClass, VTable recon | ~15 |
| `webview2-single-binary.yaml` | Static build, .rc embed, WebResourceRequested, Tailwind v4 | ~10 |

## 🎯 Core Problem

```
❌ Without: Agent generates naive WinAPI code, misses RAII, wrong hook library, no thread safety
✅ With: Agent uses safe patterns, correct hook libs, lock-free queues, proper injection methods
```

## 📋 Quick Reference

| Topic | Pattern |
| ----- | ------- |
| Safe memory read | `std::optional<T> Read(HANDLE, uintptr_t)` with RPM |
| Pointer chain | `ReadChain(handle, base, std::span<offsets>)` |
| AOB scan | IDA-style pattern `"E8 ? ? ? ? 48 8B"` with wildcards |
| Best hook lib 2025 | SafetyHook (stealth) or PolyHook2 (versatile) |
| DLL inject (stealth) | Manual mapping + PE header erasure |
| Async automation | `co_await MoveToTarget()` → coroutine chains |
| Thread safety | SPSC lock-free queue between bot↔game threads |
| Packet intercept | Hook `ws2_32!WSASend` trước encrypt function |
| Input (stealth) | Hardware emulation (Arduino HID) or driver-level |
| Bot AI (complex) | Behavior Tree > FSM khi >10 states |
| Kernel memory | CR3 physical read (tránh API hooks) |
| Hypervisor | EPT hooking (invisible inline hook) |
| UE SDK dump | Dumper-7 hoặc UEDumper cho UE4/5 |
| Single exe | /MT + vcpkg static + .rc embed resources |

## ⚠️ Anti-Patterns

| ❌ Don't | ✅ Do |
| -------- | ----- |
| Raw `ReadProcessMemory` without check | Use `std::optional<T>` wrapper |
| Hardcode addresses `0x12345678` | Use AOB pattern scanner |
| `CreateRemoteThread` for serious inject | Manual mapping with PE erasure |
| `std::thread` without join | `std::jthread` with stop_token |
| `std::mutex` in hot path | SPSC lock-free ring buffer |
| MinHook in 2025 (dated) | SafetyHook or PolyHook2 |
| Inline hook on integrity-checked fn | VEH hook or EPT hook |
| `Sleep(100)` fixed delay | `std::normal_distribution` human timing |
| `/MD` dynamic CRT | `/MT` static CRT for single-exe |
| External .css/.html files | Embed via .rc resource compiler |

## 📋 Checklist

- [ ] Memory read/write wrapped with error handling?
- [ ] Addresses resolved via pattern scan, not hardcoded?
- [ ] RAII wrappers for all HANDLEs?
- [ ] Hook library chosen appropriately for threat model?
- [ ] Injection method matches stealth requirement?
- [ ] Bot logic on separate thread with message queue?
- [ ] Frame budget ≤ 2ms for bot logic per tick?
- [ ] Packets intercepted before/after encryption?
- [ ] Human-like input timing with randomization?
- [ ] Build output is single .exe or .dll?

---
