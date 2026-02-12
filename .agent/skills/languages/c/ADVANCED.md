# C Language — Advanced Patterns

# DOMYH Awesome Code — Tier 3 Reference

## Table of Contents

- [Advanced Memory Patterns](#advanced-memory-patterns)
- [Data Structure Implementations](#data-structure-implementations)
- [Concurrency Patterns](#concurrency-patterns)
- [Low-Level I/O](#low-level-io)
- [Performance Optimization](#performance-optimization)
- [Embedding & FFI](#embedding--ffi)

---

## Advanced Memory Patterns

### Custom Memory Allocator

```c
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

// Simple arena allocator
typedef struct Arena {
    uint8_t *data;
    size_t size;
    size_t offset;
} Arena;

Arena *arena_create(size_t size) {
    Arena *arena = malloc(sizeof(Arena));
    if (!arena) return NULL;

    arena->data = malloc(size);
    if (!arena->data) {
        free(arena);
        return NULL;
    }

    arena->size = size;
    arena->offset = 0;
    return arena;
}

void *arena_alloc(Arena *arena, size_t size) {
    // Align to 8 bytes
    size_t aligned = (size + 7) & ~7;

    if (arena->offset + aligned > arena->size) {
        return NULL;  // Out of memory
    }

    void *ptr = arena->data + arena->offset;
    arena->offset += aligned;
    return ptr;
}

void arena_reset(Arena *arena) {
    arena->offset = 0;  // All allocations freed at once
}

void arena_destroy(Arena *arena) {
    if (arena) {
        free(arena->data);
        free(arena);
    }
}
```

### Memory Pool (Fixed-size Block Allocator)

```c
typedef struct MemoryPool {
    void *blocks;       // Block storage
    void *free_list;    // Free block linked list
    size_t block_size;
    size_t block_count;
} MemoryPool;

MemoryPool *pool_create(size_t block_size, size_t block_count) {
    // Ensure minimum size for free list pointer
    if (block_size < sizeof(void *)) {
        block_size = sizeof(void *);
    }

    MemoryPool *pool = malloc(sizeof(MemoryPool));
    if (!pool) return NULL;

    pool->blocks = malloc(block_size * block_count);
    if (!pool->blocks) {
        free(pool);
        return NULL;
    }

    pool->block_size = block_size;
    pool->block_count = block_count;

    // Initialize free list
    pool->free_list = pool->blocks;
    uint8_t *current = pool->blocks;
    for (size_t i = 0; i < block_count - 1; i++) {
        void **next = (void **)current;
        *next = current + block_size;
        current += block_size;
    }
    *(void **)current = NULL;  // Last block

    return pool;
}

void *pool_alloc(MemoryPool *pool) {
    if (!pool->free_list) return NULL;

    void *block = pool->free_list;
    pool->free_list = *(void **)block;
    return block;
}

void pool_free(MemoryPool *pool, void *block) {
    if (!block) return;

    *(void **)block = pool->free_list;
    pool->free_list = block;
}
```

---

## Data Structure Implementations

### Dynamic Array (Vector)

```c
typedef struct Vector {
    void **items;
    size_t size;
    size_t capacity;
} Vector;

#define VECTOR_INIT_CAP 8

Vector *vector_create(void) {
    Vector *v = malloc(sizeof(Vector));
    if (!v) return NULL;

    v->items = malloc(sizeof(void *) * VECTOR_INIT_CAP);
    if (!v->items) {
        free(v);
        return NULL;
    }

    v->size = 0;
    v->capacity = VECTOR_INIT_CAP;
    return v;
}

int vector_push(Vector *v, void *item) {
    if (v->size >= v->capacity) {
        size_t new_cap = v->capacity * 2;
        void **new_items = realloc(v->items, sizeof(void *) * new_cap);
        if (!new_items) return -ENOMEM;

        v->items = new_items;
        v->capacity = new_cap;
    }

    v->items[v->size++] = item;
    return 0;
}

void *vector_pop(Vector *v) {
    if (v->size == 0) return NULL;
    return v->items[--v->size];
}

void *vector_get(Vector *v, size_t index) {
    if (index >= v->size) return NULL;
    return v->items[index];
}
```

### Hash Table

```c
#include <stdint.h>

typedef struct HashEntry {
    char *key;
    void *value;
    struct HashEntry *next;
} HashEntry;

typedef struct HashMap {
    HashEntry **buckets;
    size_t bucket_count;
    size_t size;
} HashMap;

// FNV-1a hash
static uint64_t hash_string(const char *str) {
    uint64_t hash = 0xcbf29ce484222325ULL;  // FNV offset basis
    while (*str) {
        hash ^= (uint8_t)*str++;
        hash *= 0x100000001b3ULL;  // FNV prime
    }
    return hash;
}

HashMap *hashmap_create(size_t bucket_count) {
    HashMap *map = malloc(sizeof(HashMap));
    if (!map) return NULL;

    map->buckets = calloc(bucket_count, sizeof(HashEntry *));
    if (!map->buckets) {
        free(map);
        return NULL;
    }

    map->bucket_count = bucket_count;
    map->size = 0;
    return map;
}

int hashmap_put(HashMap *map, const char *key, void *value) {
    size_t idx = hash_string(key) % map->bucket_count;

    // Check for existing key
    for (HashEntry *e = map->buckets[idx]; e; e = e->next) {
        if (strcmp(e->key, key) == 0) {
            e->value = value;  // Update
            return 0;
        }
    }

    // Insert new entry
    HashEntry *entry = malloc(sizeof(HashEntry));
    if (!entry) return -ENOMEM;

    entry->key = strdup(key);
    if (!entry->key) {
        free(entry);
        return -ENOMEM;
    }

    entry->value = value;
    entry->next = map->buckets[idx];
    map->buckets[idx] = entry;
    map->size++;
    return 0;
}

void *hashmap_get(HashMap *map, const char *key) {
    size_t idx = hash_string(key) % map->bucket_count;

    for (HashEntry *e = map->buckets[idx]; e; e = e->next) {
        if (strcmp(e->key, key) == 0) {
            return e->value;
        }
    }
    return NULL;
}
```

---

## Concurrency Patterns

### POSIX Threads Basics

```c
#include <pthread.h>

typedef struct ThreadData {
    int id;
    int *result;
} ThreadData;

static void *worker_thread(void *arg) {
    ThreadData *data = (ThreadData *)arg;

    // Do work...
    *data->result = data->id * 10;

    return NULL;
}

int run_parallel(void) {
    pthread_t threads[4];
    ThreadData data[4];
    int results[4];

    for (int i = 0; i < 4; i++) {
        data[i].id = i;
        data[i].result = &results[i];

        if (pthread_create(&threads[i], NULL, worker_thread, &data[i]) != 0) {
            return -errno;
        }
    }

    for (int i = 0; i < 4; i++) {
        pthread_join(threads[i], NULL);
        printf("Result %d: %d\n", i, results[i]);
    }

    return 0;
}
```

### Mutex and Condition Variables

```c
#include <pthread.h>

typedef struct ThreadSafeQueue {
    void **items;
    size_t capacity;
    size_t head, tail, count;
    pthread_mutex_t lock;
    pthread_cond_t not_empty;
    pthread_cond_t not_full;
} ThreadSafeQueue;

ThreadSafeQueue *queue_create(size_t capacity) {
    ThreadSafeQueue *q = malloc(sizeof(ThreadSafeQueue));
    if (!q) return NULL;

    q->items = malloc(sizeof(void *) * capacity);
    if (!q->items) {
        free(q);
        return NULL;
    }

    q->capacity = capacity;
    q->head = q->tail = q->count = 0;

    pthread_mutex_init(&q->lock, NULL);
    pthread_cond_init(&q->not_empty, NULL);
    pthread_cond_init(&q->not_full, NULL);

    return q;
}

void queue_push(ThreadSafeQueue *q, void *item) {
    pthread_mutex_lock(&q->lock);

    while (q->count == q->capacity) {
        pthread_cond_wait(&q->not_full, &q->lock);
    }

    q->items[q->tail] = item;
    q->tail = (q->tail + 1) % q->capacity;
    q->count++;

    pthread_cond_signal(&q->not_empty);
    pthread_mutex_unlock(&q->lock);
}

void *queue_pop(ThreadSafeQueue *q) {
    pthread_mutex_lock(&q->lock);

    while (q->count == 0) {
        pthread_cond_wait(&q->not_empty, &q->lock);
    }

    void *item = q->items[q->head];
    q->head = (q->head + 1) % q->capacity;
    q->count--;

    pthread_cond_signal(&q->not_full);
    pthread_mutex_unlock(&q->lock);

    return item;
}
```

### C11 Atomics

```c
#include <stdatomic.h>

typedef struct AtomicCounter {
    atomic_int value;
} AtomicCounter;

void counter_init(AtomicCounter *c) {
    atomic_init(&c->value, 0);
}

int counter_increment(AtomicCounter *c) {
    return atomic_fetch_add(&c->value, 1);
}

int counter_get(AtomicCounter *c) {
    return atomic_load(&c->value);
}

// Compare-and-swap pattern
_Bool counter_cas(AtomicCounter *c, int expected, int desired) {
    return atomic_compare_exchange_strong(&c->value, &expected, desired);
}
```

---

## Low-Level I/O

### Memory-Mapped Files

```c
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

typedef struct MappedFile {
    void *data;
    size_t size;
    int fd;
} MappedFile;

MappedFile *mmap_file(const char *path) {
    MappedFile *mf = malloc(sizeof(MappedFile));
    if (!mf) return NULL;

    mf->fd = open(path, O_RDONLY);
    if (mf->fd < 0) {
        free(mf);
        return NULL;
    }

    struct stat sb;
    if (fstat(mf->fd, &sb) < 0) {
        close(mf->fd);
        free(mf);
        return NULL;
    }

    mf->size = sb.st_size;
    mf->data = mmap(NULL, mf->size, PROT_READ, MAP_PRIVATE, mf->fd, 0);

    if (mf->data == MAP_FAILED) {
        close(mf->fd);
        free(mf);
        return NULL;
    }

    return mf;
}

void mmap_close(MappedFile *mf) {
    if (mf) {
        munmap(mf->data, mf->size);
        close(mf->fd);
        free(mf);
    }
}
```

### Non-blocking I/O

```c
#include <fcntl.h>
#include <unistd.h>
#include <errno.h>

int set_nonblocking(int fd) {
    int flags = fcntl(fd, F_GETFL, 0);
    if (flags < 0) return -errno;

    if (fcntl(fd, F_SETFL, flags | O_NONBLOCK) < 0) {
        return -errno;
    }
    return 0;
}

// Non-blocking read
ssize_t read_nonblocking(int fd, void *buf, size_t size) {
    ssize_t n = read(fd, buf, size);

    if (n < 0) {
        if (errno == EAGAIN || errno == EWOULDBLOCK) {
            return 0;  // Would block, try again later
        }
        return -errno;  // Real error
    }

    return n;  // Bytes read
}
```

---

## Performance Optimization

### SIMD with Intrinsics

```c
#include <immintrin.h>  // SSE/AVX
#include <stdint.h>

// Sum array using AVX2
float sum_array_avx(const float *arr, size_t n) {
    __m256 sum_vec = _mm256_setzero_ps();

    size_t i = 0;
    for (; i + 8 <= n; i += 8) {
        __m256 v = _mm256_loadu_ps(&arr[i]);
        sum_vec = _mm256_add_ps(sum_vec, v);
    }

    // Horizontal sum
    float result[8];
    _mm256_storeu_ps(result, sum_vec);

    float sum = 0.0f;
    for (int j = 0; j < 8; j++) {
        sum += result[j];
    }

    // Handle remainder
    for (; i < n; i++) {
        sum += arr[i];
    }

    return sum;
}
```

### Cache Optimization

```c
// ✅ Cache-friendly: Row-major access
void matrix_multiply_optimized(
    const float *A, const float *B, float *C,
    int M, int N, int K
) {
    // Block size for cache
    const int BLOCK = 32;

    for (int i0 = 0; i0 < M; i0 += BLOCK) {
        for (int j0 = 0; j0 < N; j0 += BLOCK) {
            for (int k0 = 0; k0 < K; k0 += BLOCK) {
                // Process block
                int i_end = (i0 + BLOCK < M) ? i0 + BLOCK : M;
                int j_end = (j0 + BLOCK < N) ? j0 + BLOCK : N;
                int k_end = (k0 + BLOCK < K) ? k0 + BLOCK : K;

                for (int i = i0; i < i_end; i++) {
                    for (int k = k0; k < k_end; k++) {
                        float a_ik = A[i * K + k];
                        for (int j = j0; j < j_end; j++) {
                            C[i * N + j] += a_ik * B[k * N + j];
                        }
                    }
                }
            }
        }
    }
}
```

---

## Embedding & FFI

### Calling C from Python (ctypes)

```c
// my_math.c - compile as shared library
#include <stdint.h>

__attribute__((visibility("default")))
int32_t add_numbers(int32_t a, int32_t b) {
    return a + b;
}

__attribute__((visibility("default")))
void process_array(int32_t *arr, size_t len, int32_t multiplier) {
    for (size_t i = 0; i < len; i++) {
        arr[i] *= multiplier;
    }
}
```

```python
# Python usage
import ctypes

lib = ctypes.CDLL('./libmy_math.so')

# Define signatures
lib.add_numbers.argtypes = [ctypes.c_int32, ctypes.c_int32]
lib.add_numbers.restype = ctypes.c_int32

result = lib.add_numbers(10, 20)
print(f"Result: {result}")

# Array processing
lib.process_array.argtypes = [ctypes.POINTER(ctypes.c_int32), ctypes.c_size_t, ctypes.c_int32]
lib.process_array.restype = None

arr = (ctypes.c_int32 * 5)(1, 2, 3, 4, 5)
lib.process_array(arr, 5, 10)
print(list(arr))  # [10, 20, 30, 40, 50]
```

### Compile as Shared Library

```bash
# Linux
gcc -shared -fPIC -o libmy_math.so my_math.c

# macOS
gcc -shared -fPIC -o libmy_math.dylib my_math.c

# Windows
gcc -shared -o my_math.dll my_math.c
```

---

_DOMYH Awesome Code — C Language Advanced Patterns_
