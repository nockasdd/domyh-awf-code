## 📦  Memory Management Patterns

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
