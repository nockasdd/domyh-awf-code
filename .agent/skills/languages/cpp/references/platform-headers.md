## ⚠️ Platform-Specific Headers (CRITICAL)

### Windows Headers Conflicts

> **CRITICAL**: Windows headers have many conflicts. Follow this order exactly!

#### 1. Include Order (winsock2.h BEFORE windows.h)

```cpp
// ✅ CORRECT ORDER - winsock2.h MUST come before windows.h
#define WIN32_LEAN_AND_MEAN  // Exclude rarely-used stuff
#define NOMINMAX             // Prevent min/max macros
#define STRICT               // Enable strict type checking
#define UNICODE              // Use Unicode APIs
#define _UNICODE

#include <winsock2.h>        // 1st - Winsock 2.0
#include <ws2tcpip.h>        // 2nd - TCP/IP extensions
#include <windows.h>         // 3rd - Windows API

// ❌ WRONG - causes redefinition errors!
#include <windows.h>         // includes winsock.h (1.1)
#include <winsock2.h>        // conflicts with winsock.h!
```

#### 2. Essential Macros (Define BEFORE any Windows includes)

```cpp
// pch.h or stdafx.h - Put at TOP of precompiled header
#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN  // Exclude: Cryptography, DDE, RPC, Shell, Winsock 1.1
#endif

#ifndef NOMINMAX
#define NOMINMAX             // Prevent Windows min/max macros
#endif                       // Allows std::min, std::max to work

#ifndef STRICT
#define STRICT               // Strict type checking for handles
#endif

// Now safe to include Windows headers
#include <windows.h>
```

#### 3. min/max Macro Conflicts

```cpp
// ❌ Problem: Windows defines min/max as macros
#include <windows.h>
#include <algorithm>
int x = std::min(a, b);  // ERROR: macro expansion!

// ✅ Solution 1: Use NOMINMAX (recommended)
#define NOMINMAX
#include <windows.h>
#include <algorithm>
int x = std::min(a, b);  // Works!

// ✅ Solution 2: Parentheses workaround
int x = (std::min)(a, b);  // Prevents macro expansion

// ✅ Solution 3: #undef after include
#include <windows.h>
#undef min
#undef max
#include <algorithm>
```

#### 4. WIN32_LEAN_AND_MEAN Exclusions

```cpp
// WIN32_LEAN_AND_MEAN excludes these - include manually if needed:
#define WIN32_LEAN_AND_MEAN
#include <windows.h>

// If you need these, include AFTER windows.h:
#include <shellapi.h>    // Shell API
#include <mmsystem.h>    // Multimedia
#include <wincrypt.h>    // Cryptography
#include <commdlg.h>     // Common dialogs
#include <dde.h>         // DDE
```

### Windows Headers Quick Reference

| Header         | Purpose              | Notes                         |
| -------------- | -------------------- | ----------------------------- |
| `<windows.h>`  | Core Windows API     | Always use with LEAN_AND_MEAN |
| `<winsock2.h>` | Sockets (Winsock 2)  | MUST include BEFORE windows.h |
| `<ws2tcpip.h>` | TCP/IP, getaddrinfo  | Include after winsock2.h      |
| `<windowsx.h>` | Message crackers     | Helper macros                 |
| `<commctrl.h>` | Common controls      | ListView, TreeView, etc.      |
| `<shlobj.h>`   | Shell interface      | Folder browser, etc.          |
| `<shobjidl.h>` | Shell COM interfaces | Modern file dialogs           |
| `<tchar.h>`    | TCHAR portability    | Legacy, prefer wchar_t        |

---

### Linux/POSIX Headers

#### 1. Define \_REENTRANT for Thread-Safe Functions

```cpp
// ✅ Define BEFORE any system headers
#define _REENTRANT          // Thread-safe libc functions
#define _POSIX_C_SOURCE 200809L  // POSIX.1-2008

#include <pthread.h>
#include <unistd.h>
#include <signal.h>
```

#### 2. Signal Handling with Threads (Critical)

```cpp
#include <pthread.h>
#include <signal.h>

// ✅ Block signals in worker threads, handle in dedicated thread
int main() {
    sigset_t set;
    sigemptyset(&set);
    sigaddset(&set, SIGINT);
    sigaddset(&set, SIGTERM);

    // Block signals in main thread (inherited by child threads)
    pthread_sigmask(SIG_BLOCK, &set, NULL);

    // Create worker threads (they inherit blocked signals)
    pthread_t worker;
    pthread_create(&worker, NULL, worker_func, NULL);

    // Handle signals in main thread with sigwait
    int sig;
    while (sigwait(&set, &sig) == 0) {
        if (sig == SIGINT || sig == SIGTERM) {
            // Clean shutdown
            break;
        }
    }

    pthread_join(worker, NULL);
    return 0;
}

// ❌ AVOID: Signal handlers with threads (race conditions!)
// Use sigwait() or signalfd() instead
```

#### 3. Common POSIX Headers

| Header           | Purpose          | Key Functions                       |
| ---------------- | ---------------- | ----------------------------------- |
| `<unistd.h>`     | POSIX API        | read, write, close, fork, exec      |
| `<pthread.h>`    | Threads          | pthread*create, pthread_mutex*\*    |
| `<signal.h>`     | Signals          | sigaction, sigwait, pthread_sigmask |
| `<fcntl.h>`      | File control     | open, fcntl, O\_\* flags            |
| `<sys/types.h>`  | Type definitions | pid_t, size_t, ssize_t              |
| `<sys/socket.h>` | Sockets          | socket, bind, listen, accept        |
| `<netinet/in.h>` | Internet addr    | sockaddr_in, htons, ntohs           |
| `<arpa/inet.h>`  | IP conversion    | inet_pton, inet_ntop                |
| `<sys/stat.h>`   | File status      | stat, fstat, mkdir                  |
| `<sys/mman.h>`   | Memory mapping   | mmap, munmap, mprotect              |
| `<dlfcn.h>`      | Dynamic loading  | dlopen, dlsym, dlclose              |

---

### Cross-Platform Patterns

```cpp
// Platform detection
#if defined(_WIN32) || defined(_WIN64)
    #define PLATFORM_WINDOWS
#elif defined(__linux__)
    #define PLATFORM_LINUX
#elif defined(__APPLE__)
    #define PLATFORM_MACOS
#endif

// Platform-specific includes
#ifdef PLATFORM_WINDOWS
    #define WIN32_LEAN_AND_MEAN
    #define NOMINMAX
    #include <windows.h>
    #include <winsock2.h>
#else
    #include <unistd.h>
    #include <sys/socket.h>
    #include <netinet/in.h>
    #include <pthread.h>
#endif

// Sleep abstraction
inline void sleep_ms(int ms) {
#ifdef PLATFORM_WINDOWS
    Sleep(ms);
#else
    usleep(ms * 1000);
#endif
}
```
