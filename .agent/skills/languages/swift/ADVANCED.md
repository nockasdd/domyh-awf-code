# Swift — Advanced Patterns

# DOMYH Awesome Code v6.1.2 — Tier 3 Reference

## Table of Contents

- [Concurrency](#concurrency)
- [Protocols & Generics](#protocols--generics)
- [Memory Management](#memory-management)
- [SwiftUI Patterns](#swiftui-patterns)

---

## Concurrency

### Async/Await

```swift
func fetchUserData(userId: String) async throws -> UserData {
    async let profile = fetchProfile(userId)
    async let orders = fetchOrders(userId)
    async let settings = fetchSettings(userId)

    return try await UserData(
        profile: profile,
        orders: orders,
        settings: settings
    )
}

// Actor for thread safety
actor OrderCache {
    private var cache: [String: Order] = [:]

    func get(_ id: String) -> Order? {
        return cache[id]
    }

    func set(_ id: String, order: Order) {
        cache[id] = order
    }
}
```

### TaskGroup

```swift
func processAllOrders(_ ids: [String]) async throws -> [Result] {
    try await withThrowingTaskGroup(of: Result.self) { group in
        for id in ids {
            group.addTask {
                try await processOrder(id)
            }
        }

        var results: [Result] = []
        for try await result in group {
            results.append(result)
        }
        return results
    }
}
```

---

## Protocols & Generics

### Protocol with Associated Types

```swift
protocol Repository {
    associatedtype Entity
    associatedtype ID: Hashable

    func find(by id: ID) async throws -> Entity?
    func save(_ entity: Entity) async throws
    func delete(by id: ID) async throws
}

struct UserRepository: Repository {
    typealias Entity = User
    typealias ID = UUID

    func find(by id: UUID) async throws -> User? {
        // Implementation
    }
}
```

### Type Erasure

```swift
// Type-erased wrapper
struct AnyRepository<Entity, ID: Hashable>: Repository {
    private let _find: (ID) async throws -> Entity?
    private let _save: (Entity) async throws -> Void

    init<R: Repository>(_ repository: R) where R.Entity == Entity, R.ID == ID {
        _find = repository.find
        _save = repository.save
    }

    func find(by id: ID) async throws -> Entity? {
        try await _find(id)
    }

    func save(_ entity: Entity) async throws {
        try await _save(entity)
    }
}
```

---

## Memory Management

### Weak References in Closures

```swift
class ViewModel {
    private var cancellables = Set<AnyCancellable>()

    func fetchData() {
        dataService.fetch()
            .receive(on: DispatchQueue.main)
            .sink { [weak self] completion in
                guard let self = self else { return }
                self.handleCompletion(completion)
            } receiveValue: { [weak self] data in
                self?.processData(data)
            }
            .store(in: &cancellables)
    }
}
```

### Unowned for Performance

```swift
class Parent {
    lazy var child: Child = {
        // Guaranteed to outlive child - use unowned
        Child(parent: self)
    }()
}

class Child {
    unowned let parent: Parent

    init(parent: Parent) {
        self.parent = parent
    }
}
```

---

## SwiftUI Patterns

### MVVM with Combine

```swift
@MainActor
class OrderViewModel: ObservableObject {
    @Published private(set) var orders: [Order] = []
    @Published private(set) var isLoading = false
    @Published var error: Error?

    private let repository: OrderRepository

    init(repository: OrderRepository) {
        self.repository = repository
    }

    func loadOrders() async {
        isLoading = true
        defer { isLoading = false }

        do {
            orders = try await repository.fetchAll()
        } catch {
            self.error = error
        }
    }
}

struct OrderListView: View {
    @StateObject private var viewModel: OrderViewModel

    var body: some View {
        List(viewModel.orders) { order in
            OrderRow(order: order)
        }
        .task {
            await viewModel.loadOrders()
        }
    }
}
```

### Environment & Dependency Injection

```swift
// Environment key
struct RepositoryKey: EnvironmentKey {
    static var defaultValue: OrderRepository = MockOrderRepository()
}

extension EnvironmentValues {
    var orderRepository: OrderRepository {
        get { self[RepositoryKey.self] }
        set { self[RepositoryKey.self] = newValue }
    }
}

// Usage
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(\.orderRepository, ProductionOrderRepository())
        }
    }
}
```

---

_DOMYH Awesome Code v6.1.2 — Tier 3 Reference_
