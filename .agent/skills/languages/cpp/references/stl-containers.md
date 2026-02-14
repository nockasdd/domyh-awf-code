## 📚 STL Containers Reference

### Sequence Containers

| Container              | Access | Insert/Delete      | Use Case            |
| ---------------------- | ------ | ------------------ | ------------------- |
| `std::vector<T>`       | O(1)   | O(1) amortized end | Dynamic array       |
| `std::deque<T>`        | O(1)   | O(1) both ends     | Double-ended queue  |
| `std::list<T>`         | O(n)   | O(1) anywhere      | Frequent insertions |
| `std::array<T,N>`      | O(1)   | Fixed              | Compile-time size   |
| `std::forward_list<T>` | O(n)   | O(1)               | Singly linked       |

### Associative Containers

| Container                 | Access   | Insert   | Ordered | Use Case         |
| ------------------------- | -------- | -------- | ------- | ---------------- |
| `std::map<K,V>`           | O(log n) | O(log n) | Yes     | Key-value sorted |
| `std::set<T>`             | O(log n) | O(log n) | Yes     | Unique sorted    |
| `std::multimap<K,V>`      | O(log n) | O(log n) | Yes     | Multiple values  |
| `std::unordered_map<K,V>` | O(1) avg | O(1) avg | No      | Fast lookups     |
| `std::unordered_set<T>`   | O(1) avg | O(1) avg | No      | Fast membership  |

### Container Usage

```cpp
#include <vector>
#include <map>
#include <unordered_map>
#include <array>

// 📦 Vector with reserve
std::vector<int> nums;
nums.reserve(1000);  // Pre-allocate
nums.push_back(42);
nums.emplace_back(100);

// 📦 Range-based for
for (const auto& num : nums) {
    std::cout << num << '\n';
}

// 📦 Map with structured bindings
std::map<std::string, int> scores{{"Alice", 100}, {"Bob", 85}};
for (const auto& [name, score] : scores) {
    std::cout << name << ": " << score << '\n';
}

// 📦 Unordered map for O(1) lookups
std::unordered_map<int, std::string> idToName;
idToName[1] = "John";
if (auto it = idToName.find(1); it != idToName.end()) {
    std::cout << it->second << '\n';
}

// 📦 Fixed-size array
std::array<int, 5> arr{1, 2, 3, 4, 5};
```
