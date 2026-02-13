---
name: c
detect: ["*.c", "*.h", "Makefile", "CMakeLists.txt"]
version: "6.2.5"
category: language
tier: 1
---

# C Language Patterns — DOMYH Awesome Code

> Pure C (ISO C23) development patterns — NOT C++

## � Language Identification

```yaml
# C vs C++ distinction (CRITICAL)
c_only:
  - ".c files"
  - "No classes, namespaces, templates"
  - "No std::string, std::vector"
  - "No new/delete operators"
  - "Uses stdio.h, stdlib.h, string.h"

cpp_indicators: # Switch to C++ skill if detected
  - ".cpp, .cxx, .cc files"
  - "class, namespace, template"
  - "#include <iostream>, <vector>, <string>"
  - "new/delete operators"
  - "std:: prefix"
```

---

## 📊 Standard Headers Reference

### Core Headers (C23)

| Header        | Purpose              | Key Functions                               |
| ------------- | -------------------- | ------------------------------------------- |
| `<stdio.h>`   | I/O operations       | printf, scanf, fopen, fclose, fread, fwrite |
| `<stdlib.h>`  | General utilities    | malloc, calloc, realloc, free, exit, atoi   |
| `<string.h>`  | String operations    | strlen, strcpy, strncpy, strcmp, memcpy     |
| `<stdint.h>`  | Fixed-width integers | int8_t, uint32_t, int64_t, size_t           |
| `<stdbool.h>` | Boolean type         | bool, true, false                           |
| `<stddef.h>`  | Common definitions   | NULL, size_t, ptrdiff_t, offsetof           |
| `<math.h>`    | Math functions       | sin, cos, sqrt, pow, fabs, ceil, floor      |
| `<time.h>`    | Time/date            | time, clock, difftime, strftime             |
| `<errno.h>`   | Error handling       | errno, ENOMEM, EINVAL, ENOENT               |
| `<assert.h>`  | Assertions           | assert, static_assert (C23)                 |
| `<ctype.h>`   | Character handling   | isalpha, isdigit, toupper, tolower          |
| `<limits.h>`  | Type limits          | INT_MAX, INT_MIN, UINT_MAX, CHAR_BIT        |

### C23 New Headers

| Header          | Purpose              | Key Functions/Types               |
| --------------- | -------------------- | --------------------------------- |
| `<stdckdint.h>` | Checked integer math | ckd_add, ckd_sub, ckd_mul         |
| `<stdbit.h>`    | Bit manipulation     | stdc_popcount, stdc_leading_zeros |
| `<uchar.h>`     | UTF-8 support        | char8_t, mbrtoc32, c32rtomb       |

---

## 🔧 C23 New Features

### nullptr (replaces NULL)

```c
// ✅ C23 - Type-safe null pointer
#include <stddef.h>  // nullptr_t

void process(int *ptr) {
    if (ptr == nullptr) {  // C23
        return;
    }
    // ...
}

int *p = nullptr;  // Preferred in C23
```

### constexpr (Compile-time Constants)

```c
// ✅ C23 constexpr
constexpr int MAX_SIZE = 1024;
constexpr double PI = 3.14159265359;

// Can be used in array sizes
int buffer[MAX_SIZE];
```

### Binary Literals & Digit Separators

```c
// ✅ C23 binary literals
int mask = 0b1111'0000;    // Binary with separators
int big = 1'000'000;       // Million with separators
```

### Checked Integer Arithmetic

```c
// ✅ C23 - Prevent integer overflow
#include <stdckdint.h>

int a = INT_MAX;
int b = 1;
int result;

if (ckd_add(&result, a, b)) {
    // Overflow detected
    printf("Integer overflow!\n");
} else {
    printf("Result: %d\n", result);
}
```

### C23 Attributes

```c
// ✅ C23 attributes for better static analysis
[[nodiscard]] int compute(int x);     // Warn if return value ignored
[[deprecated("Use new_func")]] void old_func(void);
[[fallthrough]]                       // Intentional fallthrough in switch
[[maybe_unused]] int debug_flag;      // Suppress unused warnings
[[noreturn]] void fatal_error(void);  // Never returns
```

---

## 📦 Standard Library APIs

### stdio.h - File I/O

```c
#include <stdio.h>

// ✅ File operations
FILE *fp = fopen("data.txt", "r");
if (fp == NULL) {
    perror("fopen");  // Print error with context
    return -1;
}

char line[256];
while (fgets(line, sizeof(line), fp) != NULL) {
    printf("%s", line);
}

fclose(fp);

// ✅ Binary file I/O
FILE *bin = fopen("data.bin", "rb");
uint8_t buffer[1024];
size_t bytes_read = fread(buffer, 1, sizeof(buffer), bin);

// ✅ Formatted output
printf("Int: %d, Hex: 0x%08X, Float: %.2f\n", 42, 255, 3.14);
fprintf(stderr, "Error: %s\n", strerror(errno));

// ✅ Safe string formatting
char buf[64];
int n = snprintf(buf, sizeof(buf), "User: %s", username);
if (n >= (int)sizeof(buf)) {
    // Truncation occurred
}
```

### stdlib.h - Memory & Utilities

```c
#include <stdlib.h>

// ✅ Memory allocation (ALWAYS check for NULL)
void *ptr = malloc(size);
if (ptr == NULL) {
    return -ENOMEM;
}

// ✅ Zero-initialized memory
int *arr = calloc(count, sizeof(int));
if (arr == NULL) {
    return -ENOMEM;
}

// ✅ Resize memory (handle NULL case)
void *new_ptr = realloc(ptr, new_size);
if (new_ptr == NULL) {
    free(ptr);  // Original still valid
    return -ENOMEM;
}
ptr = new_ptr;

// ✅ Free memory and prevent use-after-free
free(ptr);
ptr = NULL;  // ALWAYS nullify after free

// ✅ String conversions
int val = atoi("42");       // No error checking
long lval = strtol("42", NULL, 10);  // Preferred - with base

// ✅ Environment
char *home = getenv("HOME");
if (home != NULL) {
    printf("Home: %s\n", home);
}

// ✅ Random numbers
srand((unsigned)time(NULL));
int r = rand() % 100;  // 0-99

// ✅ Sorting and searching
qsort(array, count, sizeof(array[0]), compare_func);
void *found = bsearch(&key, array, count, sizeof(array[0]), compare_func);
```

### string.h - String Operations

```c
#include <string.h>

// ❌ DANGEROUS - Buffer overflow
char buf[10];
strcpy(buf, user_input);  // NEVER do this

// ✅ SAFE alternatives
strncpy(buf, user_input, sizeof(buf) - 1);
buf[sizeof(buf) - 1] = '\0';  // Ensure null termination

// ✅ Or use snprintf (recommended)
snprintf(buf, sizeof(buf), "%s", user_input);

// ✅ String length
size_t len = strlen(str);

// ✅ String comparison
if (strcmp(str1, str2) == 0) {
    // Strings are equal
}

// ✅ Case-insensitive (POSIX, not standard C)
// Use strcasecmp on POSIX systems

// ✅ Memory operations
memcpy(dest, src, n);      // Copy (no overlap)
memmove(dest, src, n);     // Copy (overlap safe)
memset(buf, 0, sizeof(buf));  // Zero memory

// ✅ C23 - Clear sensitive data (not optimized away)
#include <string.h>
memset_explicit(password, 0, sizeof(password));

// ✅ C23 - strdup (now standard)
char *copy = strdup(original);  // malloc + strcpy
if (copy == NULL) {
    return -ENOMEM;
}
// ... use copy ...
free(copy);
```

---

## 🧠 Memory Management Patterns

### RAII Pattern (Resource Acquisition Is Initialization)

```c
// ✅ Cleanup attribute (GCC/Clang extension, common in Linux kernel)
#define AUTO_FREE __attribute__((cleanup(cleanup_free)))

static void cleanup_free(void *p) {
    free(*(void **)p);
}

void process_data(void) {
    AUTO_FREE char *buf = malloc(1024);
    if (!buf) return;

    // buf automatically freed when function returns
    // No need for explicit free()
}
```

### Error Handling with goto (Linux Kernel Style)

```c
// ✅ Standard C pattern for resource cleanup
int process_file(const char *path) {
    int ret = 0;
    FILE *fp = NULL;
    char *buf = NULL;

    fp = fopen(path, "r");
    if (!fp) {
        ret = -errno;
        goto out;
    }

    buf = malloc(BUFFER_SIZE);
    if (!buf) {
        ret = -ENOMEM;
        goto out_close;
    }

    // Do processing...
    if (some_error) {
        ret = -EINVAL;
        goto out_free;
    }

    // Success path
    ret = 0;

out_free:
    free(buf);
out_close:
    fclose(fp);
out:
    return ret;
}
```

### Memory Debugging

```bash
# Valgrind (memory leak detection)
valgrind --leak-check=full ./program

# AddressSanitizer (compile-time)
gcc -fsanitize=address -g program.c -o program

# UndefinedBehaviorSanitizer
gcc -fsanitize=undefined -g program.c -o program
```

---

## 🏗️ Data Structures

### Struct Patterns

```c
// ✅ Opaque pointer pattern (information hiding)
// In header file (user.h)
typedef struct User User;
User *user_create(const char *name);
void user_destroy(User *user);
const char *user_get_name(const User *user);

// In implementation file (user.c)
struct User {
    char *name;
    int id;
    // Private implementation details
};

User *user_create(const char *name) {
    User *u = malloc(sizeof(*u));
    if (!u) return NULL;

    u->name = strdup(name);
    if (!u->name) {
        free(u);
        return NULL;
    }
    u->id = generate_id();
    return u;
}

void user_destroy(User *user) {
    if (user) {
        free(user->name);
        free(user);
    }
}
```

### Flexible Array Member (FAM)

```c
// ✅ C99+ pattern for variable-length data
struct Message {
    size_t length;
    uint32_t type;
    char data[];  // Flexible array member (MUST be last)
};

struct Message *create_message(const char *text) {
    size_t len = strlen(text) + 1;
    struct Message *msg = malloc(sizeof(*msg) + len);
    if (!msg) return NULL;

    msg->length = len;
    msg->type = MSG_TYPE_TEXT;
    memcpy(msg->data, text, len);
    return msg;
}
```

---

## 🔒 Security Best Practices

### Input Validation

```c
// ✅ Validate all user input
int parse_int(const char *str, int *out) {
    if (str == NULL || out == NULL) {
        return -EINVAL;
    }

    char *endptr;
    errno = 0;
    long val = strtol(str, &endptr, 10);

    if (errno == ERANGE || val > INT_MAX || val < INT_MIN) {
        return -ERANGE;
    }
    if (endptr == str || *endptr != '\0') {
        return -EINVAL;  // No valid digits or trailing garbage
    }

    *out = (int)val;
    return 0;
}
```

### Buffer Safety

```c
// ✅ Always use bounded operations
#define SAFE_COPY(dst, src) \
    do { \
        strncpy(dst, src, sizeof(dst) - 1); \
        dst[sizeof(dst) - 1] = '\0'; \
    } while (0)

// ✅ Prefer snprintf for formatting
char buf[256];
if (snprintf(buf, sizeof(buf), "%s:%d", host, port) >= (int)sizeof(buf)) {
    // Handle truncation
    return -E2BIG;
}
```

---

## 🔧 Build & Tools

### Compiler Flags

```bash
# ✅ Recommended GCC/Clang flags
CFLAGS = -std=c23 -Wall -Wextra -Werror -pedantic

# Debug build
CFLAGS += -g -O0 -fsanitize=address,undefined

# Release build
CFLAGS += -O2 -DNDEBUG -flto

# Security hardening
CFLAGS += -fstack-protector-strong -D_FORTIFY_SOURCE=2
LDFLAGS += -Wl,-z,relro,-z,now
```

### Makefile Template

```makefile
CC = gcc
CFLAGS = -std=c23 -Wall -Wextra -Werror -pedantic
LDFLAGS =

SRC = $(wildcard src/*.c)
OBJ = $(SRC:.c=.o)
TARGET = program

.PHONY: all clean

all: $(TARGET)

$(TARGET): $(OBJ)
	$(CC) $(LDFLAGS) -o $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -c -o $@ $<

clean:
	rm -f $(OBJ) $(TARGET)
```

### CMake Template

```cmake
cmake_minimum_required(VERSION 3.20)
project(MyProject C)

set(CMAKE_C_STANDARD 23)
set(CMAKE_C_STANDARD_REQUIRED ON)

add_compile_options(-Wall -Wextra -Werror -pedantic)

add_executable(program
    src/main.c
    src/utils.c
)

# Debug/Release configurations
if(CMAKE_BUILD_TYPE STREQUAL "Debug")
    add_compile_options(-g -O0 -fsanitize=address,undefined)
    add_link_options(-fsanitize=address,undefined)
endif()
```

---

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

_DOMYH Awesome Code • C Language (ISO C23) • 2025-2026_
