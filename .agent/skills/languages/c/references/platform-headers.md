## ⚠️ Platform-Specific Headers (CRITICAL)

### Windows Headers Conflicts

> **CRITICAL**: Windows headers have many conflicts. Follow this order exactly!

#### 1. Include Order (winsock2.h BEFORE windows.h)

```c
// ✅ CORRECT ORDER - winsock2.h MUST come before windows.h
#define WIN32_LEAN_AND_MEAN  // Exclude rarely-used stuff
#define NOMINMAX             // Prevent min/max macros (for C++ compat)
#define STRICT               // Enable strict type checking
#define UNICODE              // Use Unicode APIs
#define _UNICODE

#include <winsock2.h>        // 1st - Winsock 2.0
#include <ws2tcpip.h>        // 2nd - TCP/IP extensions
#include <windows.h>         // 3rd - Windows API

#pragma comment(lib, "ws2_32.lib")  // Link Winsock library

// ❌ WRONG - causes redefinition errors!
#include <windows.h>         // includes winsock.h (1.1)
#include <winsock2.h>        // conflicts with winsock.h!
```

#### 2. Essential Macros

```c
// Define BEFORE any Windows includes (in pch.h or first in source)
#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN  // Excludes: Cryptography, DDE, RPC, Shell, Winsock 1.1
#endif

#ifndef STRICT
#define STRICT               // Strict type checking for HANDLE types
#endif

#include <windows.h>
```

#### 3. Windows Socket Initialization

```c
#include <winsock2.h>
#include <ws2tcpip.h>

int init_winsock(void) {
    WSADATA wsaData;
    int result = WSAStartup(MAKEWORD(2, 2), &wsaData);
    if (result != 0) {
        fprintf(stderr, "WSAStartup failed: %d\n", result);
        return -1;
    }
    return 0;
}

void cleanup_winsock(void) {
    WSACleanup();
}
```

### Windows Headers Quick Reference

| Header         | Purpose             | Notes                            |
| -------------- | ------------------- | -------------------------------- |
| `<windows.h>`  | Core Windows API    | Use with WIN32_LEAN_AND_MEAN     |
| `<winsock2.h>` | Sockets (Winsock 2) | MUST include BEFORE windows.h    |
| `<ws2tcpip.h>` | TCP/IP, getaddrinfo | Include after winsock2.h         |
| `<process.h>`  | Process control     | \_beginthreadex, \_getpid        |
| `<io.h>`       | Low-level I/O       | \_open, \_read, \_write, \_close |
| `<direct.h>`   | Directory           | \_mkdir, \_rmdir, \_getcwd       |
| `<conio.h>`    | Console I/O         | \_getch, \_kbhit                 |

---

### Linux/POSIX Headers

#### 1. Feature Test Macros (Define FIRST)

```c
// Define BEFORE any system headers!
#define _GNU_SOURCE          // GNU extensions (Linux-specific)
#define _POSIX_C_SOURCE 200809L  // POSIX.1-2008 compliance
#define _REENTRANT           // Thread-safe libc functions
#define _XOPEN_SOURCE 700    // X/Open SUSv4 + POSIX 2008

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>
```

#### 2. Signal Handling with Threads (Critical)

```c
#include <pthread.h>
#include <signal.h>
#include <stdio.h>

volatile sig_atomic_t shutdown_flag = 0;

// ✅ Block signals in worker threads, handle in dedicated thread
int main(void) {
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
            shutdown_flag = 1;
            break;
        }
    }

    pthread_join(worker, NULL);
    return 0;
}

// ❌ AVOID: Signal handlers with threads (race conditions!)
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
| `<errno.h>`      | Error codes      | errno, ENOENT, EINVAL               |
| `<dirent.h>`     | Directory ops    | opendir, readdir, closedir          |

---

### Cross-Platform C Code

```c
// Platform detection
#if defined(_WIN32) || defined(_WIN64)
    #define PLATFORM_WINDOWS 1
#elif defined(__linux__)
    #define PLATFORM_LINUX 1
#elif defined(__APPLE__)
    #define PLATFORM_MACOS 1
#else
    #define PLATFORM_UNIX 1
#endif

// Platform-specific includes
#ifdef PLATFORM_WINDOWS
    #define WIN32_LEAN_AND_MEAN
    #include <windows.h>
    #include <winsock2.h>
    #include <ws2tcpip.h>
    #pragma comment(lib, "ws2_32.lib")
#else
    #include <unistd.h>
    #include <sys/socket.h>
    #include <netinet/in.h>
    #include <pthread.h>
    #include <errno.h>
#endif

// Cross-platform sleep
static inline void sleep_ms(unsigned int ms) {
#ifdef PLATFORM_WINDOWS
    Sleep(ms);
#else
    usleep(ms * 1000);
#endif
}

// Cross-platform thread type
#ifdef PLATFORM_WINDOWS
    typedef HANDLE thread_t;
    typedef DWORD thread_ret_t;
#else
    typedef pthread_t thread_t;
    typedef void* thread_ret_t;
#endif

// Cross-platform socket type
#ifdef PLATFORM_WINDOWS
    typedef SOCKET socket_t;
    #define INVALID_SOCKET_VAL INVALID_SOCKET
    #define close_socket(s) closesocket(s)
#else
    typedef int socket_t;
    #define INVALID_SOCKET_VAL (-1)
    #define close_socket(s) close(s)
#endif
```

---

## ✅ Production Checklist

- [ ] No memory leaks (Valgrind clean)
- [ ] All malloc/calloc checked for NULL
- [ ] All resources freed on error paths
- [ ] No buffer overflows (use bounded ops)
- [ ] No use-after-free (nullify pointers)
- [ ] Static analyzer clean (clang-tidy, cppcheck)
- [ ] Const correctness applied
- [ ] Error handling with proper codes
- [ ] Security hardening flags enabled
- [ ] C23 or latest supported standard used

---

_DOMYH Awesome Code C Language (ISO C23) 2025-2026_
