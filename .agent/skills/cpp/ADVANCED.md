# C++ — Advanced Patterns

# DOMYH Awesome Code v4.3 — Tier 3 Reference

## Table of Contents

- [C++26 Features Preview](#c26-features-preview)
- [Advanced Templates](#advanced-templates)
- [Metaprogramming](#metaprogramming)
- [Concurrency Advanced](#concurrency-advanced)
- [Performance Optimization](#performance-optimization)
- [Design Patterns](#design-patterns)

---

## C++26 Features Preview

### Static Reflection

```cpp
// C++26 reflection (expected syntax)
#include <meta>

consteval auto get_member_names(auto type_info) {
    std::vector<std::string_view> names;
    for (auto member : type_info.members()) {
        names.push_back(member.name());
    }
    return names;
}

struct User {
    int id;
    std::string name;
    float score;
};

// Usage: auto names = get_member_names(^User);
// Result: {"id", "name", "score"}
```

### Contracts

```cpp
// C++26 contracts
int divide(int a, int b)
    pre(b != 0)         // Precondition
    post(r: r * b == a) // Postcondition
{
    return a / b;
}

class BoundedQueue {
    void push(int value)
        pre(!full())     // Queue not full
        post(!empty())   // Queue not empty after push
    {
        // Implementation
    }
};
```

### std::execution (Senders/Receivers)

```cpp
#include <execution>

// Async task composition with senders
auto work = std::execution::schedule(scheduler)
    | std::execution::then([](){ return compute(); })
    | std::execution::then([](auto result){ return process(result); })
    | std::execution::on(io_scheduler);

std::this_thread::sync_wait(work);
```

---

## Advanced Templates

### Variadic Templates

```cpp
// Fold expressions (C++17)
template<typename... Args>
auto sum(Args... args) {
    return (... + args);  // Unary left fold
}

// Parameter pack expansion
template<typename... Ts>
void print_all(const Ts&... args) {
    ((std::cout << args << ' '), ...);
    std::cout << '\n';
}

// Perfect forwarding with pack
template<typename Fn, typename... Args>
decltype(auto) invoke_with_logging(Fn&& fn, Args&&... args) {
    std::cout << "Calling function\n";
    return std::invoke(std::forward<Fn>(fn), std::forward<Args>(args)...);
}
```

### CRTP (Curiously Recurring Template Pattern)

```cpp
template<typename Derived>
class Counter {
    static inline int count = 0;
public:
    Counter() { ++count; }
    ~Counter() { --count; }
    static int getCount() { return count; }
};

class Widget : public Counter<Widget> {
    // Each Widget type has its own counter
};

class Gadget : public Counter<Gadget> {
    // Gadget has separate counter from Widget
};
```

### Expression Templates

```cpp
// Lazy evaluation for math expressions
template<typename L, typename R>
struct Add {
    const L& left;
    const R& right;

    auto operator[](size_t i) const {
        return left[i] + right[i];
    }
};

template<typename L, typename R>
Add<L, R> operator+(const L& l, const R& r) {
    return {l, r};
}

// Usage: auto result = a + b + c;  // No temporaries created
```

---

## Metaprogramming

### Type Traits

```cpp
#include <type_traits>

template<typename T>
void process(T&& value) {
    if constexpr (std::is_pointer_v<std::decay_t<T>>) {
        // Pointer handling
        if (value) process(*value);
    } else if constexpr (std::is_arithmetic_v<T>) {
        // Numeric handling
        std::cout << "Numeric: " << value << '\n';
    } else if constexpr (std::is_same_v<std::decay_t<T>, std::string>) {
        // String handling
        std::cout << "String: " << value << '\n';
    } else {
        // Generic handling
        static_assert(std::is_copy_constructible_v<T>);
    }
}
```

### Compile-Time Programming

```cpp
// consteval (immediate function - C++20)
consteval int square(int n) {
    return n * n;
}

// constexpr lambda (C++17)
constexpr auto factorial = [](int n) {
    int result = 1;
    for (int i = 2; i <= n; ++i) {
        result *= i;
    }
    return result;
};

static_assert(factorial(5) == 120);

// std::array at compile time
consteval auto make_squares() {
    std::array<int, 10> arr{};
    for (int i = 0; i < 10; ++i) {
        arr[i] = i * i;
    }
    return arr;
}

constexpr auto squares = make_squares();
```

---

## Concurrency Advanced

### Lock-Free Data Structures

```cpp
#include <atomic>

template<typename T>
class LockFreeStack {
    struct Node {
        T data;
        std::atomic<Node*> next;
        Node(T value) : data(std::move(value)), next(nullptr) {}
    };

    std::atomic<Node*> head{nullptr};

public:
    void push(T value) {
        Node* new_node = new Node(std::move(value));
        new_node->next = head.load(std::memory_order_relaxed);
        while (!head.compare_exchange_weak(
            new_node->next, new_node,
            std::memory_order_release,
            std::memory_order_relaxed));
    }

    std::optional<T> pop() {
        Node* old_head = head.load(std::memory_order_relaxed);
        while (old_head && !head.compare_exchange_weak(
            old_head, old_head->next.load(std::memory_order_relaxed),
            std::memory_order_acquire,
            std::memory_order_relaxed));

        if (!old_head) return std::nullopt;
        T result = std::move(old_head->data);
        delete old_head;
        return result;
    }
};
```

### Coroutines (C++20)

```cpp
#include <coroutine>
#include <optional>

template<typename T>
struct Generator {
    struct promise_type {
        T current_value;

        Generator get_return_object() {
            return Generator{std::coroutine_handle<promise_type>::from_promise(*this)};
        }
        std::suspend_always initial_suspend() { return {}; }
        std::suspend_always final_suspend() noexcept { return {}; }
        std::suspend_always yield_value(T value) {
            current_value = std::move(value);
            return {};
        }
        void return_void() {}
        void unhandled_exception() { std::terminate(); }
    };

    std::coroutine_handle<promise_type> handle;

    ~Generator() { if (handle) handle.destroy(); }

    std::optional<T> next() {
        if (handle.done()) return std::nullopt;
        handle.resume();
        if (handle.done()) return std::nullopt;
        return handle.promise().current_value;
    }
};

Generator<int> range(int start, int end) {
    for (int i = start; i < end; ++i) {
        co_yield i;
    }
}

// Usage
auto gen = range(0, 10);
while (auto value = gen.next()) {
    std::cout << *value << ' ';
}
```

---

## Performance Optimization

### Memory Layout Optimization

```cpp
// Cache-friendly data layout
struct alignas(64) CacheLine {
    std::array<float, 16> data;
};

// Avoid false sharing in multithreaded code
struct alignas(64) ThreadData {
    std::atomic<int> counter{0};
    char padding[60];  // Pad to cache line boundary
};

// SOA (Structure of Arrays) vs AOS (Array of Structures)
// AOS (cache unfriendly for specific field access)
struct ParticleAOS {
    float x, y, z;
    float vx, vy, vz;
};
std::vector<ParticleAOS> particles_aos;

// SOA (cache friendly for batch processing)
struct ParticlesSOA {
    std::vector<float> x, y, z;
    std::vector<float> vx, vy, vz;
};
ParticlesSOA particles_soa;
```

### SIMD with Intrinsics

```cpp
#include <immintrin.h>

void add_vectors_avx(float* a, float* b, float* result, size_t n) {
    size_t i = 0;
    for (; i + 8 <= n; i += 8) {
        __m256 va = _mm256_loadu_ps(&a[i]);
        __m256 vb = _mm256_loadu_ps(&b[i]);
        __m256 vr = _mm256_add_ps(va, vb);
        _mm256_storeu_ps(&result[i], vr);
    }
    // Handle remainder
    for (; i < n; ++i) {
        result[i] = a[i] + b[i];
    }
}
```

### Small Buffer Optimization

```cpp
template<typename T, size_t BufferSize = 32>
class SmallVector {
    alignas(T) std::byte buffer_[BufferSize];
    T* data_;
    size_t size_;
    size_t capacity_;

    bool is_small() const { return data_ == reinterpret_cast<const T*>(buffer_); }

public:
    SmallVector() : data_(reinterpret_cast<T*>(buffer_)),
                    size_(0), capacity_(BufferSize / sizeof(T)) {}

    void push_back(const T& value) {
        if (size_ == capacity_) {
            grow();
        }
        new (&data_[size_++]) T(value);
    }

private:
    void grow() {
        size_t new_capacity = capacity_ * 2;
        T* new_data = static_cast<T*>(::operator new(new_capacity * sizeof(T)));
        std::uninitialized_move_n(data_, size_, new_data);
        if (!is_small()) {
            ::operator delete(data_);
        }
        data_ = new_data;
        capacity_ = new_capacity;
    }
};
```

---

## Design Patterns

### Type Erasure

```cpp
class AnyCallable {
    struct Concept {
        virtual ~Concept() = default;
        virtual void call() = 0;
    };

    template<typename F>
    struct Model : Concept {
        F func;
        Model(F f) : func(std::move(f)) {}
        void call() override { func(); }
    };

    std::unique_ptr<Concept> impl_;

public:
    template<typename F>
    AnyCallable(F f) : impl_(std::make_unique<Model<F>>(std::move(f))) {}

    void operator()() { impl_->call(); }
};

// Usage
AnyCallable fn1 = []{ std::cout << "Lambda\n"; };
AnyCallable fn2 = std::bind(&SomeClass::method, &obj);
fn1();
fn2();
```

### Policy-Based Design

```cpp
// Policies
struct LoggingPolicy {
    static void log(const std::string& msg) {
        std::cout << "[LOG] " << msg << '\n';
    }
};

struct NoLoggingPolicy {
    static void log(const std::string&) {}
};

// Policy-based class
template<typename LogPolicy = NoLoggingPolicy>
class Repository {
public:
    void save(const Entity& entity) {
        LogPolicy::log("Saving entity");
        // Save implementation
    }
};

// Usage
Repository<LoggingPolicy> debugRepo;     // With logging
Repository<> prodRepo;                    // Without logging
```

---

_DOMYH Awesome Code v4.3 — C++ Advanced Patterns_
