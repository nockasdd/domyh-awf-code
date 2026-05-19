---
library: java
version: "25"
latest: true
category: language
official_docs: https://docs.oracle.com/en/java/
last_updated: 2026-03-21
last_checked: 2026-03-21
source: ai-enhanced from oracle.com + openjdk.org + web research
---

# Java 25 (LTS)

> Java — A robust, object-oriented, platform-independent programming language.
> Current: Java 25 LTS (Sep 2025) | Previous LTS: Java 21 (Sep 2023)
> Docs: https://docs.oracle.com/en/java/javase/25/

## Version Comparison

| Feature | Java 21 (LTS) | Java 23 | Java 24 | Java 25 (LTS) |
|:--------|:--------------|:--------|:--------|:--------------|
| Support | LTS → Sep 2028 | STS 6mo | STS 6mo | **LTS → Sep 2028** |
| Virtual threads | ✅ Stable | ✅ | ✅ **No pinning** | ✅ No pinning |
| Pattern matching (records) | ✅ | ✅ | ✅ | ✅ |
| Primitive in patterns | ❌ | Preview | 2nd Preview | ✅ Expected |
| Stream Gatherers | ❌ | 2nd Preview | ✅ Stable | ✅ |
| Structured Concurrency | Preview | 3rd Preview | 4th Preview | ✅ Expected |
| Scoped Values | Preview | 3rd Preview | 4th Preview | ✅ Expected |
| Class-File API | ❌ | 2nd Preview | ✅ Stable | ✅ |
| Flexible constructors | ❌ | 2nd Preview | 3rd Preview | ✅ Expected |
| Module import declarations | ❌ | Preview | 2nd Preview | ✅ Expected |
| ZGC generational default | ❌ | ✅ | ✅ (only mode) | ✅ |
| Security Manager | Deprecated | Deprecated | ❌ Disabled | ❌ Removed |
| `sun.misc.Unsafe` | Deprecated | Terminal dep. | ⚠️ Warnings | ❌ Removal path |
| AOT class loading | ❌ | ❌ | ✅ Stable | ✅ |

## Installation

```bash
# SDKMAN (recommended — manages multiple versions)
curl -s "https://get.sdkman.io" | bash
sdk install java 25-open     # OpenJDK
sdk install java 25-graal    # GraalVM

# macOS (Homebrew)
brew install openjdk@25

# Windows (winget)
winget install Oracle.JDK.25

# Docker
docker run -it eclipse-temurin:25-jdk

# Verify
java --version       # openjdk 25 2025-09-16
javac --version
```

## Configuration

```xml
<!-- pom.xml (Maven) -->
<properties>
    <java.version>25</java.version>
    <maven.compiler.source>25</maven.compiler.source>
    <maven.compiler.target>25</maven.compiler.target>
</properties>
```

```groovy
// build.gradle.kts (Gradle)
java {
    toolchain {
        languageVersion.set(JavaLanguageVersion.of(25))
    }
}
```

```properties
# JVM options (common production flags)
-XX:+UseZGC                     # ZGC (generational only since JDK 24)
-XX:MaxRAMPercentage=75.0       # container-aware memory
-XX:+UseCompressedOops
-Xms256m -Xmx2g
--enable-preview                # if using preview features
```

## Core API

### Modern Java Syntax

```java
// Records — immutable data carriers (Java 16+)
public record User(String name, String email, int age) {
    // Compact constructor — validation
    public User {
        if (age < 0) throw new IllegalArgumentException("Age must be >= 0");
        email = email.toLowerCase();
    }
}

var user = new User("Alice", "ALICE@DEV.COM", 30);
System.out.println(user.name());  // "Alice"
System.out.println(user.email()); // "alice@dev.com"

// Sealed classes — restricted inheritance (Java 17+)
public sealed interface Shape permits Circle, Rectangle, Triangle {}
public record Circle(double radius) implements Shape {}
public record Rectangle(double width, double height) implements Shape {}
public record Triangle(double base, double height) implements Shape {}

// Pattern matching (Java 21+)
double area = switch (shape) {
    case Circle c -> Math.PI * c.radius() * c.radius();
    case Rectangle r -> r.width() * r.height();
    case Triangle t -> 0.5 * t.base() * t.height();
};

// Text blocks (Java 15+)
String json = """
        {
            "name": "%s",
            "age": %d
        }
        """.formatted(user.name(), user.age());
```

### Virtual Threads (Java 21+)

```java
// Virtual threads — lightweight, JVM-managed
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    // Spawn 100,000 concurrent tasks — uses ~KB of memory each
    IntStream.range(0, 100_000).forEach(i ->
        executor.submit(() -> {
            Thread.sleep(Duration.ofSeconds(1));
            return fetchFromDb(i);  // blocking I/O is fine!
        })
    );
}

// JDK 24+: synchronized WITHOUT pinning!
// Previously, synchronized blocks pinned virtual threads to platform threads
synchronized (lock) {
    // In JDK 24+, this does NOT pin the virtual thread
    var data = httpClient.send(request, BodyHandlers.ofString());
    processData(data);
}

// Thread.ofVirtual() — explicit creation
Thread.ofVirtual().name("worker-", 0).start(() -> {
    System.out.println("Running on: " + Thread.currentThread());
});

// ⚠️ Gotcha: Don't pool virtual threads — create new ones per task
// ⚠️ Gotcha: Avoid ThreadLocal with virtual threads — use ScopedValue instead
```

### Structured Concurrency (Preview → Expected stable JDK 25)

```java
// Treat concurrent tasks as single unit
try (var scope = StructuredTaskScope.open()) {
    Subtask<User> userTask = scope.fork(() -> findUser(userId));
    Subtask<List<Order>> ordersTask = scope.fork(() -> fetchOrders(userId));

    scope.join();  // wait for all

    // Both results available — errors propagated correctly
    var user = userTask.get();
    var orders = ordersTask.get();
    return new UserProfile(user, orders);
}
// If either fails, the other is cancelled automatically
```

### Stream Gatherers (Java 24+)

```java
import java.util.stream.Gatherers;

// Custom intermediate stream operations
var windowedAvg = numbers.stream()
    .gather(Gatherers.windowSliding(3))  // sliding window of 3
    .map(window -> window.stream().mapToInt(i -> i).average().orElse(0))
    .toList();

// Fixed groups
var groups = items.stream()
    .gather(Gatherers.windowFixed(5))  // groups of 5
    .toList();

// Scan (running accumulation)
var running = numbers.stream()
    .gather(Gatherers.scan(() -> 0, Integer::sum))
    .toList();  // [1, 3, 6, 10, ...]
```

### HTTP Client (Java 11+)

```java
HttpClient client = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_2)
    .connectTimeout(Duration.ofSeconds(10))
    .build();

// GET request
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://api.example.com/users"))
    .header("Accept", "application/json")
    .GET()
    .build();

HttpResponse<String> response = client.send(request,
    HttpResponse.BodyHandlers.ofString());

// POST with JSON
HttpRequest post = HttpRequest.newBuilder()
    .uri(URI.create("https://api.example.com/users"))
    .header("Content-Type", "application/json")
    .POST(HttpRequest.BodyPublishers.ofString(json))
    .build();

// Async
client.sendAsync(request, HttpResponse.BodyHandlers.ofString())
    .thenApply(HttpResponse::body)
    .thenAccept(System.out::println);
```

### Collections & LINQ-style

```java
// Immutable collections (Java 9+)
var list = List.of("a", "b", "c");
var set = Set.of(1, 2, 3);
var map = Map.of("key1", "val1", "key2", "val2");

// Streams — Java's LINQ equivalent
var result = users.stream()
    .filter(u -> u.age() >= 18)
    .sorted(Comparator.comparing(User::name))
    .map(u -> new UserDto(u.name(), u.email()))
    .toList();  // Java 16+

// Collectors
var byCity = users.stream()
    .collect(Collectors.groupingBy(User::city));

var nameList = users.stream()
    .map(User::name)
    .collect(Collectors.joining(", "));

// Optional
Optional<User> user = findUser(id);
String name = user
    .map(User::name)
    .orElse("Unknown");
user.ifPresent(u -> sendEmail(u.email()));
```

## Common Patterns

```java
// 1. Builder pattern (modern — with records)
public record ServerConfig(
    String host, int port, boolean ssl,
    Duration timeout, int maxConnections
) {
    public static Builder builder() { return new Builder(); }

    public static class Builder {
        private String host = "localhost";
        private int port = 8080;
        private boolean ssl = false;
        private Duration timeout = Duration.ofSeconds(30);
        private int maxConnections = 100;

        public Builder host(String h)        { host = h; return this; }
        public Builder port(int p)           { port = p; return this; }
        public Builder ssl(boolean s)        { ssl = s; return this; }
        public Builder timeout(Duration t)   { timeout = t; return this; }
        public Builder maxConnections(int n) { maxConnections = n; return this; }

        public ServerConfig build() {
            return new ServerConfig(host, port, ssl, timeout, maxConnections);
        }
    }
}

var config = ServerConfig.builder()
    .host("api.prod.com")
    .port(443)
    .ssl(true)
    .build();

// 2. Result type (no exceptions for business errors)
public sealed interface Result<T> {
    record Success<T>(T value) implements Result<T> {}
    record Failure<T>(String error) implements Result<T> {}

    static <T> Result<T> success(T value) { return new Success<>(value); }
    static <T> Result<T> failure(String error) { return new Failure<>(error); }
}

// 3. Dependency injection (Spring Boot)
@Service
public class UserService {
    private final UserRepository repo;

    public UserService(UserRepository repo) { // constructor injection
        this.repo = repo;
    }
}

// 4. Spring Boot REST controller
@RestController
@RequestMapping("/api/users")
public class UserController {
    @GetMapping("/{id}")
    public ResponseEntity<User> getUser(@PathVariable Long id) {
        return userService.findById(id)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public User createUser(@Valid @RequestBody CreateUserDto dto) {
        return userService.create(dto);
    }
}
```

## Gotchas & Breaking Changes

### General Gotchas

- ⚠️ **Null everywhere**: Java allows null for any reference type. Use `Optional<T>`, `@NonNull`, or Kotlin's null safety.
- ⚠️ **String `==` vs `.equals()`**: `==` compares references, not values. Always use `.equals()` for strings.
  ```java
  "hello" == new String("hello")      // false!
  "hello".equals(new String("hello")) // true
  ```
- ⚠️ **Checked exceptions**: Must be caught or declared. Can lead to verbose code. Use unchecked `RuntimeException` for business logic.
- ⚠️ **`ConcurrentModificationException`**: Don't modify collection while iterating. Use `Iterator.remove()` or stream `.filter()`.
- ⚠️ **`ThreadLocal` + virtual threads**: ThreadLocal per virtual thread = massive memory usage. Use `ScopedValue` instead.
- ⚠️ **Date/Time API**: Never use `java.util.Date`/`Calendar`. Use `java.time.*` (Java 8+): `LocalDate`, `Instant`, `ZonedDateTime`.
- ⚠️ **Resource leaks**: Always use try-with-resources for `Closeable` objects (streams, connections, etc.).
- ⚠️ **Autoboxing performance**: Boxed types (`Integer`, `Long`) in hot paths cause GC pressure. Use primitives.

### Java 24/25 Breaking Changes

- ⚠️ **Security Manager DISABLED**: If app uses `SecurityManager`, it no longer works. Rearchitect security.
- ⚠️ **`sun.misc.Unsafe` warnings**: Runtime warnings issued. Migrate to `VarHandle` or Foreign Function API.
- ⚠️ **Windows 32-bit x86 REMOVED** (Java 24): No longer supported.
- ⚠️ **JNI warnings**: Prepare for future restrictions. Use Foreign Function & Memory API instead.
- ⚠️ **ZGC non-generational REMOVED** (Java 24): Only generational mode available.
- ⚠️ **Oracle JDK 21 licensing**: Permissive license ends Sep 2026. Upgrade to JDK 25 or switch to OpenJDK/Temurin.

### Java 23 Breaking Changes

- ⚠️ **`sun.misc.Unsafe` terminally deprecated**: Plan migration now.
- ⚠️ **String templates withdrawn**: Feature removed from preview, undergoing redesign.

## Migration

### From Java 21 (LTS) → Java 25 (LTS)
1. Update build tools: Maven/Gradle Java target to 25
2. Remove `SecurityManager` usage — disabled since JDK 24
3. Migrate `sun.misc.Unsafe` → `VarHandle` / Foreign Memory API
4. Review JNI usage — warnings in JDK 24, future restrictions
5. Adopt virtual threads for I/O-bound tasks
6. Use Stream Gatherers for custom stream operations (stable JDK 24)
7. Adopt `ScopedValue` over `ThreadLocal` for virtual threads
8. Test with ZGC (generational only)
9. Update Oracle JDK licensing if applicable
10. Run full test suite with `--enable-preview` for new features

### From Java 17 (LTS) → Java 25 (LTS)
1. All of the above +
2. Adopt records, sealed classes, pattern matching
3. Replace `instanceof` chains with switch pattern matching
4. Use text blocks for multi-line strings
5. Migrate to `java.time.*` if still on Date/Calendar
6. Consider AOT compilation for microservices

<!--
BM25 DESIGN RULES:
- H1 = library name (root search anchor)
- H2 = feature category
- Code:prose ratio ≥ 70:30
- Keep 5-30KB per file
-->
