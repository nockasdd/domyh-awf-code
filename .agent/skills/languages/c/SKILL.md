---
name: c
detect: ["*.c", "*.h", "Makefile", "CMakeLists.txt"]
version: "6.3.1"
category: language
tier: 1
---

# C Language Patterns DOMYH Awesome Code

> Pure C (ISO C23) development patterns NOT C++

## 🔍 Language Identification

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

## 🆕 C23 New Features

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

## 📚 Deep-Dive References

- **Memory Management** — malloc/free patterns, arena allocators, memory pools
  → See [references/memory-management.md](references/memory-management.md)

- **Data Structures** — Linked lists, hash maps, ring buffers in C
  → See [references/data-structures.md](references/data-structures.md)

- **Platform Headers** — Windows/POSIX specifics, \_REENTRANT, signal handling
  → See [references/platform-headers.md](references/platform-headers.md)

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
