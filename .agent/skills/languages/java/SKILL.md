---
name: java
detect:
  ["pom.xml", "build.gradle", "build.gradle.kts", "*.java", "settings.gradle"]
version: "6.2.4"
category: backend
tier: 1
---

# Java Patterns — DOMYH Awesome Code

> Java 21/22/23 LTS — 2025-2026

## 🔍 Language Detection

```yaml
java_indicators:  # Java skill activates
  - "pom.xml" or "build.gradle"
  - "*.java files"
  - "public class, interface, record"
  - "package com.*, org.*"
  - "@SpringBootApplication"
  - "import java.*, javax.*"

not_java:  # JVM alternatives
  - "*.kt, fun main()" → Kotlin
  - "*.scala, object App" → Scala
  - "*.groovy" → Groovy
```

---

## 📊 Java Versions (2025-2026)

| Version     | Type   | Release | Support Until |
| ----------- | ------ | ------- | ------------- |
| **Java 17** | LTS    | 2021-09 | 2029          |
| **Java 21** | LTS 🏆 | 2023-09 | 2031          |
| **Java 22** | STS    | 2024-03 | 2024-09       |
| **Java 23** | STS    | 2024-09 | 2025-03       |
| **Java 25** | LTS    | 2025-09 | 2033+         |

> **Recommendation**: Use Java 21 LTS for production. Java 25 LTS (Sept 2025) will be next major LTS.

### Java 21 Key Features

```java
// ✅ Virtual Threads (Project Loom) - Production Ready
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    IntStream.range(0, 10_000).forEach(i -> {
        executor.submit(() -> {
            Thread.sleep(Duration.ofMillis(100));
            return processRequest(i);
        });
    });
}

// ✅ Records - Immutable Data Classes
public record User(Long id, String email, String name) {}

// ✅ Pattern Matching for switch
static String formatValue(Object obj) {
    return switch (obj) {
        case Integer i -> String.format("int: %d", i);
        case Long l    -> String.format("long: %d", l);
        case Double d  -> String.format("double: %.2f", d);
        case String s  -> String.format("String: %s", s);
        case null      -> "null";
        default        -> obj.toString();
    };
}

// ✅ Record Patterns (Destructuring)
record Point(int x, int y) {}

static int sumCoordinates(Object obj) {
    if (obj instanceof Point(int x, int y)) {
        return x + y;
    }
    return 0;
}

// ✅ Sealed Classes
public sealed interface Shape
    permits Circle, Rectangle, Triangle {}

public record Circle(double radius) implements Shape {}
public record Rectangle(double w, double h) implements Shape {}
public record Triangle(double a, double b, double c) implements Shape {}

// ✅ Pattern Matching with Guards
static String describeShape(Shape shape) {
    return switch (shape) {
        case Circle c when c.radius() > 10 -> "Large circle";
        case Circle c -> "Circle with radius " + c.radius();
        case Rectangle r -> "Rectangle " + r.w() + "x" + r.h();
        case Triangle t -> "Triangle";
    };
}
```

### Java 22/23 Features Preview

```java
// ✅ Unnamed Variables (Java 22)
try (var _ = ScopedValue.where(CURRENT_USER, user)) {
    // _ is unnamed, unused variable
}

// ✅ String Templates (Preview → Stable in future)
String name = "Alice";
int age = 25;
String message = STR."Hello \{name}, you are \{age} years old";

// ✅ Gatherers (Stream API enhancement - Java 22)
List<Integer> result = numbers.stream()
    .gather(Gatherers.windowFixed(3))
    .toList();
```

---

## 🛠️ IDE & Toolchain Support

### IntelliJ IDEA (Recommended)

```yaml
version: 2025.x+
features:
  - Full Java 21/22/23/25 support from release day
  - AI-assisted code completion
  - Advanced refactoring
  - Built-in profiler
  - Maven/Gradle integration
  - Spring Boot support
plugins:
  - "Spring Boot Assistant"
  - "Lombok"
  - "JPA Buddy"
  - "SonarLint"
notes:
  - Community Edition free
  - Ultimate for enterprise features
```

### Eclipse IDE

```yaml
version: 2025-03+
features:
  - Java 25 support via Eclipse JDT
  - JUnit 6.0.1 support
  - Multi-Release JAR support
  - Maven/Gradle integration
plugins:
  - "Spring Tools 4"
  - "Eclipse Wild Web Developer"
notes:
  - Open source
  - Lighter than IntelliJ
```

### VS Code

```yaml
extensions:
  - "Extension Pack for Java" (Microsoft)
  - "Spring Boot Extension Pack"
  - "Debugger for Java"
features:
  - Lightweight option
  - Good for microservices
  - Cross-platform
```

---

## 📦 Frameworks & Libraries (2025)

### Frameworks Comparison

| Framework            | Use Case        | Startup | Memory |
| -------------------- | --------------- | ------- | ------ |
| **Spring Boot 3.3+** | Enterprise 🏆   | 1-3s    | 200MB+ |
| **Quarkus 3.x**      | Cloud-native    | 0.1s    | 50MB   |
| **Micronaut 4.x**    | Compile-time DI | 0.2s    | 60MB   |
| **Jakarta EE 11**    | Standards-based | 2-5s    | 300MB+ |

### Spring Boot 3.3+ (Most Common)

```java
// ✅ Modern Spring Boot with Virtual Threads
@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}

// application.yml - Enable Virtual Threads
spring:
  threads:
    virtual:
      enabled: true

// ✅ REST Controller
@RestController
@RequestMapping("/api/users")
public class UserController {
    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping
    public List<User> findAll() {
        return userService.findAll();
    }

    @GetMapping("/{id}")
    public ResponseEntity<User> findById(@PathVariable Long id) {
        return userService.findById(id)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public User create(@Valid @RequestBody UserCreateRequest request) {
        return userService.create(request);
    }
}
```

### Database Libraries

| Library              | Use Case           |
| -------------------- | ------------------ |
| **Hibernate 6.x**    | JPA implementation |
| **Spring Data JPA**  | Repository pattern |
| **jOOQ**             | Type-safe SQL      |
| **Flyway/Liquibase** | Migrations         |
| **HikariCP**         | Connection pooling |

### Utilities

| Library               | Use Case           |
| --------------------- | ------------------ |
| **Jackson**           | JSON processing    |
| **Lombok**            | Reduce boilerplate |
| **MapStruct**         | Object mapping     |
| **JUnit 5 + Mockito** | Testing            |
| **Testcontainers**    | Integration tests  |
| **Guava**             | Google utilities   |
| **LangChain4j**       | AI/LLM integration |

---

## ⚡ Virtual Threads Best Practices

```java
// ✅ Use for I/O-bound tasks
ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor();

// ✅ DON'T pool virtual threads (they're lightweight)
// ❌ WRONG: VirtualThread pool = new VirtualThreadPool(100);

// ✅ Use Semaphore to limit concurrent resources
private final Semaphore dbConnectionSemaphore = new Semaphore(100);

public Data fetchData() throws InterruptedException {
    dbConnectionSemaphore.acquire();
    try {
        return database.query();
    } finally {
        dbConnectionSemaphore.release();
    }
}

// ✅ Prefer ReentrantLock over synchronized (avoids pinning)
private final ReentrantLock lock = new ReentrantLock();

public void update() {
    lock.lock();
    try {
        // Critical section
    } finally {
        lock.unlock();
    }
}

// ❌ AVOID synchronized (pins virtual thread)
public synchronized void update() {
    // This pins the carrier thread!
}

// ✅ Structured Concurrency (Java 21+)
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    Subtask<User> userTask = scope.fork(() -> fetchUser(id));
    Subtask<Order> orderTask = scope.fork(() -> fetchOrders(id));

    scope.join();           // Wait for all
    scope.throwIfFailed();  // Throw if any failed

    return new UserWithOrders(userTask.get(), orderTask.get());
}
```

---

## 🎯 Records Best Practices

```java
// ✅ Use records for DTOs, API responses, events
public record UserDTO(Long id, String email, String name) {}

public record CreateUserRequest(
    @NotBlank String email,
    @NotBlank @Size(min = 2, max = 100) String name
) {}

// ✅ Compact constructor for validation
public record Point(int x, int y) {
    public Point {
        if (x < 0 || y < 0) {
            throw new IllegalArgumentException("Coordinates must be non-negative");
        }
    }
}

// ✅ Records with additional methods
public record Money(BigDecimal amount, Currency currency) {
    public Money add(Money other) {
        if (!currency.equals(other.currency)) {
            throw new IllegalArgumentException("Currency mismatch");
        }
        return new Money(amount.add(other.amount), currency);
    }

    public static Money zero(Currency currency) {
        return new Money(BigDecimal.ZERO, currency);
    }
}

// ❌ AVOID: Complex business logic in records
// Records should be simple data carriers
```

---

## 📂 Project Structure (Hexagonal/Clean)

```
src/main/java/com/example/myapp/
├── Application.java
├── domain/
│   ├── model/
│   │   ├── User.java
│   │   └── Order.java
│   ├── repository/
│   │   └── UserRepository.java
│   └── service/
│       └── UserService.java
├── application/
│   ├── usecase/
│   │   └── CreateUserUseCase.java
│   └── dto/
│       └── UserDTO.java
├── infrastructure/
│   ├── persistence/
│   │   ├── entity/
│   │   └── repository/
│   ├── config/
│   │   └── AppConfig.java
│   └── external/
│       └── PaymentGateway.java
└── presentation/
    ├── controller/
    │   └── UserController.java
    └── exception/
        └── GlobalExceptionHandler.java
```

---

## 🔧 Build Tools

### Gradle (Kotlin DSL - Recommended)

```kotlin
// build.gradle.kts
plugins {
    java
    id("org.springframework.boot") version "3.3.0"
    id("io.spring.dependency-management") version "1.1.5"
}

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}

dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("org.springframework.boot:spring-boot-starter-data-jpa")

    compileOnly("org.projectlombok:lombok")
    annotationProcessor("org.projectlombok:lombok")

    testImplementation("org.springframework.boot:spring-boot-starter-test")
    testImplementation("org.testcontainers:postgresql")
}

tasks.withType<Test> {
    useJUnitPlatform()
}
```

### Maven

```xml
<project>
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.3.0</version>
    </parent>

    <properties>
        <java.version>21</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
    </dependencies>
</project>
```

---

## 🎨 Naming Conventions

| Element    | Convention    | Example            |
| ---------- | ------------- | ------------------ |
| Classes    | PascalCase    | `UserService`      |
| Interfaces | PascalCase    | `UserRepository`   |
| Methods    | camelCase     | `findByEmail()`    |
| Variables  | camelCase     | `userName`         |
| Constants  | UPPER_SNAKE   | `MAX_RETRIES`      |
| Packages   | lowercase     | `com.example.user` |
| Enums      | PascalCase    | `OrderStatus`      |
| Generics   | Single letter | `T`, `E`, `K`, `V` |

---

## ✅ Production Checklist

### Java Version

- [ ] Using Java 21 LTS or newer
- [ ] Virtual threads enabled for I/O workloads
- [ ] Records used for DTOs

### Code Quality

- [ ] Pattern matching used where applicable
- [ ] No raw types (use generics)
- [ ] Proper exception handling
- [ ] Resources closed with try-with-resources

### Performance

- [ ] Connection pooling configured (HikariCP)
- [ ] Appropriate caching strategy
- [ ] Pagination for large datasets

### Security

- [ ] Input validation (@Valid)
- [ ] SQL injection prevented (parameterized queries)
- [ ] Sensitive data not logged

### Testing

- [ ] Unit tests with JUnit 5
- [ ] Integration tests with Testcontainers
- [ ] Mock external services

---

_DOMYH Awesome Code • Java Development • 2025-2026_
