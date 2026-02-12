---
name: swift
detect: ["Package.swift", "*.swift", "*.xcodeproj", "*.xcworkspace"]
version: "6.2.2"
category: mobile
tier: 1
---

# Swift Patterns — DOMYH Awesome Code

> **Version**: Swift 6/6.1 (2025-2026)
> **Frameworks**: SwiftUI, UIKit
> **Philosophy**: Protocol-oriented, type-safe, actor-based concurrency

---

## 🎯 When to Use This Skill

Use for: iOS/macOS/watchOS/tvOS apps, SwiftUI, server-side Swift.
**NOT for**: Android (→ kotlin), cross-platform (→ flutter).

---

## 📦 Recommended Stack (2025-2026)

### UI Frameworks

| Library     | Use Case             | iOS Version |
| ----------- | -------------------- | ----------- |
| **SwiftUI** | Declarative UI 🏆    | iOS 17+     |
| **UIKit**   | Legacy, fine control | iOS 13+     |

### Networking

| Library        | Use Case              |
| -------------- | --------------------- |
| **URLSession** | Native async/await 🏆 |
| **Alamofire**  | HTTP client           |

### State & Data

| Library         | Use Case             | iOS     |
| --------------- | -------------------- | ------- |
| **@Observable** | Observation macro 🏆 | iOS 17+ |
| **SwiftData**   | Persistence          | iOS 17+ |
| **Core Data**   | Legacy persistence   | iOS 13+ |
| **Combine**     | Reactive streams     | iOS 13+ |

### Architecture

| Library  | Use Case                |
| -------- | ----------------------- |
| **TCA**  | Composable Architecture |
| **MVVM** | ViewModels pattern      |

### IDE Support

| IDE          | Features                           |
| ------------ | ---------------------------------- |
| **Xcode 17** | Full Swift 6 support, AI assist 🏆 |
| **VS Code**  | Swift extension, debugging         |

---

## 🆕 Swift 6 Features (2025)

### Strict Concurrency (Data Race Safety)

```swift
// ✅ Swift 6 enforces data race safety at compile time
// All sendable violations are now errors, not warnings

actor UserCache {
    private var cache: [Int: User] = [:]

    func get(_ id: Int) -> User? {
        cache[id]
    }

    func set(_ id: Int, user: User) {
        cache[id] = user
    }
}

// ✅ Sendable types can cross actor boundaries
struct User: Sendable, Codable, Identifiable {
    let id: Int
    let name: String
    let email: String
}
```

### Async/Await Best Practices

```swift
// ✅ Structured concurrency with TaskGroup
func fetchAllUsers(ids: [Int]) async throws -> [User] {
    try await withThrowingTaskGroup(of: User?.self) { group in
        for id in ids {
            group.addTask {
                try? await fetchUser(id: id)
            }
        }

        var users: [User] = []
        for try await user in group {
            if let user { users.append(user) }
        }
        return users
    }
}

// ✅ MainActor for UI updates
@MainActor
class UserViewModel: ObservableObject {
    @Published var users: [User] = []
    @Published var isLoading = false

    func loadUsers() async {
        isLoading = true
        defer { isLoading = false }

        do {
            users = try await api.fetchUsers()
        } catch {
            // Handle error
        }
    }
}
```

### @Observable Macro (iOS 17+)

```swift
import Observation

// ✅ Modern observation - replaces ObservableObject
@Observable
class UserStore {
    var users: [User] = []
    var selectedUser: User?
    var isLoading = false

    func load() async {
        isLoading = true
        users = await api.fetchUsers()
        isLoading = false
    }
}

// ✅ Usage in SwiftUI
struct UserListView: View {
    @State private var store = UserStore()

    var body: some View {
        List(store.users) { user in
            UserRow(user: user)
        }
        .task { await store.load() }
    }
}
```

---

## 🎨 SwiftUI Best Practices

### View Composition

```swift
// ✅ Small, focused components
struct UserRow: View {
    let user: User

    var body: some View {
        HStack {
            AsyncImage(url: user.avatarURL) { image in
                image.resizable()
            } placeholder: {
                ProgressView()
            }
            .frame(width: 40, height: 40)
            .clipShape(Circle())

            VStack(alignment: .leading) {
                Text(user.name).font(.headline)
                Text(user.email).font(.caption).foregroundStyle(.secondary)
            }
        }
    }
}
```

### Navigation (iOS 16+)

```swift
// ✅ Type-safe navigation with NavigationStack
struct ContentView: View {
    @State private var path = NavigationPath()

    var body: some View {
        NavigationStack(path: $path) {
            UserListView(path: $path)
                .navigationDestination(for: User.self) { user in
                    UserDetailView(user: user)
                }
        }
    }
}
```

### State Management

```swift
// ✅ @State for local, @Binding for passing down
struct ToggleView: View {
    @Binding var isOn: Bool

    var body: some View {
        Toggle("Enable", isOn: $isOn)
    }
}

// ✅ @Environment for dependency injection
@Observable
class AuthManager {
    var currentUser: User?
}

struct ProfileView: View {
    @Environment(AuthManager.self) private var auth

    var body: some View {
        if let user = auth.currentUser {
            Text(user.name)
        }
    }
}
```

---

## 🔧 SwiftData (iOS 17+)

```swift
import SwiftData

// ✅ Model definition
@Model
class Task {
    var title: String
    var isCompleted: Bool
    var createdAt: Date

    init(title: String) {
        self.title = title
        self.isCompleted = false
        self.createdAt = .now
    }
}

// ✅ Usage in SwiftUI
struct TaskListView: View {
    @Environment(\.modelContext) private var context
    @Query(sort: \Task.createdAt, order: .reverse) private var tasks: [Task]

    var body: some View {
        List(tasks) { task in
            TaskRow(task: task)
        }
    }

    func addTask(_ title: String) {
        let task = Task(title: title)
        context.insert(task)
    }
}
```

---

## 🛡️ Error Handling

```swift
// ✅ Typed throws (Swift 6)
enum NetworkError: Error, LocalizedError {
    case invalidURL
    case noData
    case decodingFailed

    var errorDescription: String? {
        switch self {
        case .invalidURL: "Invalid URL"
        case .noData: "No data received"
        case .decodingFailed: "Failed to decode response"
        }
    }
}

func fetchUser(id: Int) async throws(NetworkError) -> User {
    guard let url = URL(string: "\(baseURL)/users/\(id)") else {
        throw .invalidURL
    }

    let (data, _) = try await URLSession.shared.data(from: url)

    do {
        return try JSONDecoder().decode(User.self, from: data)
    } catch {
        throw .decodingFailed
    }
}
```

---

## ✅ Best Practices Checklist

### Code Quality

- [ ] Swift 6 language mode enabled
- [ ] Strict concurrency checking
- [ ] SwiftLint configured
- [ ] All types Sendable where needed

### Architecture

- [ ] @Observable for iOS 17+
- [ ] MVVM or TCA pattern
- [ ] Small, composable views
- [ ] @MainActor for UI

### Performance

- [ ] Lazy loading for lists
- [ ] AsyncImage for remote images
- [ ] Proper task cancellation
- [ ] EquatableView for complex views

---

_DOMYH Awesome Code • Swift 6/6.1_
