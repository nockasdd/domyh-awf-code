## 🧠 Memory Management

### Smart Pointers

```cpp
#include <memory>

// 📦 unique_ptr (exclusive ownership)
auto widget = std::make_unique<Widget>(config);

// 📦 shared_ptr (shared ownership)
auto resource = std::make_shared<Resource>();
auto copy = resource;  // Reference count = 2

// 📦 weak_ptr (non-owning reference)
std::weak_ptr<Resource> weak = resource;
if (auto locked = weak.lock()) {
    // Use locked safely
}

// 📦 Custom deleter
auto file = std::unique_ptr<FILE, decltype(&fclose)>(
    fopen("data.txt", "r"), fclose
);
```

### Move Semantics

```cpp
class Buffer {
    std::unique_ptr<uint8_t[]> data_;
    size_t size_;

public:
    // Move constructor
    Buffer(Buffer&& other) noexcept
        : data_(std::move(other.data_))
        , size_(std::exchange(other.size_, 0)) {}

    // Move assignment
    Buffer& operator=(Buffer&& other) noexcept {
        if (this != &other) {
            data_ = std::move(other.data_);
            size_ = std::exchange(other.size_, 0);
        }
        return *this;
    }
};
```

---

## � Concurrency

### std::jthread (C++20)

```cpp
#include <thread>
#include <stop_token>

std::jthread worker([](std::stop_token stoken) {
    while (!stoken.stop_requested()) {
        // Do work
    }
});

// Automatic join on destruction
// Can request stop: worker.request_stop();
```

### std::atomic

```cpp
#include <atomic>

std::atomic<int> counter{0};

void increment() {
    counter.fetch_add(1, std::memory_order_relaxed);
}

int get() {
    return counter.load(std::memory_order_acquire);
}
```
