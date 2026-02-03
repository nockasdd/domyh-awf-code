# Java — Advanced Patterns

> DOMYH Awesome Code v5.5 — Tier 3 Reference

## Table of Contents

- [Virtual Threads Deep Dive](#virtual-threads-deep-dive)
- [Modern Pattern Matching](#modern-pattern-matching)
- [Structured Concurrency](#structured-concurrency)
- [Spring Boot 3 Patterns](#spring-boot-3-patterns)
- [Testing Patterns](#testing-patterns)

---

## Virtual Threads Deep Dive

### When to Use Virtual Threads

```java
// ✅ IDEAL: I/O-bound tasks
// - HTTP requests
// - Database queries
// - File I/O
// - Message queue operations

// ❌ AVOID: CPU-bound tasks
// - Complex calculations
// - Image processing
// - Data compression

// ✅ HTTP Server with Virtual Threads
public class VirtualThreadServer {
    public static void main(String[] args) throws IOException {
        var server = HttpServer.create(new InetSocketAddress(8080), 0);
        server.setExecutor(Executors.newVirtualThreadPerTaskExecutor());

        server.createContext("/api", exchange -> {
            // Each request runs on a virtual thread
            var result = fetchDataFromDatabase();
            var response = result.getBytes();
            exchange.sendResponseHeaders(200, response.length);
            exchange.getResponseBody().write(response);
            exchange.close();
        });

        server.start();
    }
}
```

### Avoiding Virtual Thread Pitfalls

```java
// ❌ WRONG: Using synchronized (pins carrier thread)
public class BadExample {
    private final Object lock = new Object();

    public void update() {
        synchronized (lock) {
            // Virtual thread is pinned here!
            databaseCall();
        }
    }
}

// ✅ CORRECT: Use ReentrantLock
public class GoodExample {
    private final ReentrantLock lock = new ReentrantLock();

    public void update() {
        lock.lock();
        try {
            // Virtual thread can unmount during I/O
            databaseCall();
        } finally {
            lock.unlock();
        }
    }
}

// ✅ Resource limiting with Semaphore
public class DatabasePool {
    // Limit concurrent DB connections to 100
    private final Semaphore semaphore = new Semaphore(100);
    private final DataSource dataSource;

    public Connection getConnection() throws SQLException, InterruptedException {
        semaphore.acquire();
        try {
            return dataSource.getConnection();
        } catch (SQLException e) {
            semaphore.release();
            throw e;
        }
    }

    public void returnConnection(Connection conn) throws SQLException {
        try {
            conn.close();
        } finally {
            semaphore.release();
        }
    }
}
```

### ScopedValue (Java 21+)

```java
// ✅ ScopedValue: Preferred over ThreadLocal for virtual threads
public class RequestContext {
    private static final ScopedValue<User> CURRENT_USER = ScopedValue.newInstance();

    public static void handleRequest(User user, Runnable handler) {
        ScopedValue.runWhere(CURRENT_USER, user, handler);
    }

    public static User getCurrentUser() {
        return CURRENT_USER.orElseThrow(
            () -> new IllegalStateException("No user in context")
        );
    }
}

// Usage
RequestContext.handleRequest(user, () -> {
    // CURRENT_USER is available here and in all nested calls
    processOrder();
    sendNotification();
});
```

---

## Modern Pattern Matching

### Exhaustive Pattern Matching

```java
// ✅ Sealed hierarchy with exhaustive matching
public sealed interface Payment
    permits CreditCardPayment, BankTransferPayment, CryptoPayment {}

public record CreditCardPayment(
    String cardNumber,
    String expiry,
    BigDecimal amount
) implements Payment {}

public record BankTransferPayment(
    String iban,
    BigDecimal amount
) implements Payment {}

public record CryptoPayment(
    String walletAddress,
    String currency,
    BigDecimal amount
) implements Payment {}

// ✅ Compiler ensures all cases are handled
public String processPayment(Payment payment) {
    return switch (payment) {
        case CreditCardPayment cc ->
            "Processing card ending in " + cc.cardNumber().substring(12);
        case BankTransferPayment bt ->
            "Transfer to IBAN: " + bt.iban();
        case CryptoPayment crypto ->
            "Crypto payment: " + crypto.amount() + " " + crypto.currency();
    };
}
```

### Guard Patterns

```java
// ✅ Pattern matching with guards
public String categorizeOrder(Order order) {
    return switch (order) {
        case Order o when o.total().compareTo(BigDecimal.valueOf(1000)) > 0
            -> "Premium order: " + o.id();
        case Order o when o.items().isEmpty()
            -> "Empty order: " + o.id();
        case Order o
            -> "Standard order: " + o.id();
    };
}

// ✅ Nested record patterns
public record Address(String street, String city, String country) {}
public record Customer(String name, Address address) {}
public record Order(String id, Customer customer, List<Item> items) {}

public String getShippingZone(Order order) {
    return switch (order) {
        case Order(_, Customer(_, Address(_, _, "USA")), _)
            -> "Domestic";
        case Order(_, Customer(_, Address(_, _, "Canada")), _)
            -> "North America";
        case Order(_, Customer(_, Address(_, _, String country)), _)
            -> "International: " + country;
    };
}
```

---

## Structured Concurrency

### StructuredTaskScope Patterns

```java
import java.util.concurrent.StructuredTaskScope;

// ✅ ShutdownOnFailure: Cancel all if any fails
public record UserProfile(User user, List<Order> orders, List<Review> reviews) {}

public UserProfile loadUserProfile(String userId) throws Exception {
    try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
        Subtask<User> userTask = scope.fork(() -> fetchUser(userId));
        Subtask<List<Order>> ordersTask = scope.fork(() -> fetchOrders(userId));
        Subtask<List<Review>> reviewsTask = scope.fork(() -> fetchReviews(userId));

        scope.join();           // Wait for all
        scope.throwIfFailed();  // Propagate exception if any failed

        return new UserProfile(
            userTask.get(),
            ordersTask.get(),
            reviewsTask.get()
        );
    }
}

// ✅ ShutdownOnSuccess: Return first successful result
public String fetchFromAnyMirror(String resourceId) throws Exception {
    try (var scope = new StructuredTaskScope.ShutdownOnSuccess<String>()) {
        scope.fork(() -> fetchFromMirror1(resourceId));
        scope.fork(() -> fetchFromMirror2(resourceId));
        scope.fork(() -> fetchFromMirror3(resourceId));

        scope.join();
        return scope.result();  // Returns first successful result
    }
}

// ✅ Custom scope for partial results
public class PartialResultScope<T> extends StructuredTaskScope<T> {
    private final List<T> results = new CopyOnWriteArrayList<>();
    private final List<Throwable> errors = new CopyOnWriteArrayList<>();

    @Override
    protected void handleComplete(Subtask<? extends T> subtask) {
        switch (subtask.state()) {
            case SUCCESS -> results.add(subtask.get());
            case FAILED -> errors.add(subtask.exception());
            case UNAVAILABLE -> {}
        }
    }

    public List<T> getResults() { return List.copyOf(results); }
    public List<Throwable> getErrors() { return List.copyOf(errors); }
}
```

---

## Spring Boot 3 Patterns

### Virtual Threads Configuration

```yaml
# application.yml
spring:
  threads:
    virtual:
      enabled: true # Enable virtual threads for MVC

server:
  tomcat:
    threads:
      max: 200 # Still useful for backpressure
```

### Modern REST Controller

```java
@RestController
@RequestMapping("/api/users")
@RequiredArgsConstructor
public class UserController {
    private final UserService userService;

    @GetMapping
    public List<UserDTO> findAll(
        @RequestParam(defaultValue = "0") int page,
        @RequestParam(defaultValue = "20") int size
    ) {
        return userService.findAll(PageRequest.of(page, size))
            .map(UserDTO::from)
            .getContent();
    }

    @GetMapping("/{id}")
    public UserDTO findById(@PathVariable Long id) {
        return userService.findById(id)
            .map(UserDTO::from)
            .orElseThrow(() -> new NotFoundException("User not found: " + id));
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public UserDTO create(@Valid @RequestBody CreateUserRequest request) {
        return UserDTO.from(userService.create(request));
    }

    @PutMapping("/{id}")
    public UserDTO update(
        @PathVariable Long id,
        @Valid @RequestBody UpdateUserRequest request
    ) {
        return UserDTO.from(userService.update(id, request));
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void delete(@PathVariable Long id) {
        userService.delete(id);
    }
}

// ✅ Global exception handler
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(NotFoundException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public ProblemDetail handleNotFound(NotFoundException ex) {
        return ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, ex.getMessage());
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ProblemDetail handleValidation(MethodArgumentNotValidException ex) {
        var detail = ex.getBindingResult().getFieldErrors().stream()
            .map(e -> e.getField() + ": " + e.getDefaultMessage())
            .collect(Collectors.joining(", "));
        return ProblemDetail.forStatusAndDetail(HttpStatus.BAD_REQUEST, detail);
    }
}
```

### Repository Pattern with Spring Data

```java
public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByEmail(String email);

    @Query("SELECT u FROM User u WHERE u.status = :status")
    List<User> findByStatus(@Param("status") UserStatus status);

    @EntityGraph(attributePaths = {"orders", "reviews"})
    Optional<User> findWithDetailsById(Long id);

    @Modifying
    @Query("UPDATE User u SET u.lastLoginAt = :time WHERE u.id = :id")
    void updateLastLogin(@Param("id") Long id, @Param("time") Instant time);
}
```

---

## Testing Patterns

### JUnit 5 with Nested Tests

```java
@SpringBootTest
@AutoConfigureMockMvc
class UserControllerTest {

    @Autowired MockMvc mockMvc;
    @MockBean UserService userService;

    @Nested
    @DisplayName("GET /api/users/{id}")
    class GetUser {

        @Test
        @DisplayName("returns user when found")
        void returnsUser() throws Exception {
            var user = new User(1L, "alice@example.com", "Alice");
            when(userService.findById(1L)).thenReturn(Optional.of(user));

            mockMvc.perform(get("/api/users/1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.email").value("alice@example.com"))
                .andExpect(jsonPath("$.name").value("Alice"));
        }

        @Test
        @DisplayName("returns 404 when not found")
        void returns404() throws Exception {
            when(userService.findById(1L)).thenReturn(Optional.empty());

            mockMvc.perform(get("/api/users/1"))
                .andExpect(status().isNotFound());
        }
    }
}
```

### Testcontainers Integration

```java
@SpringBootTest
@Testcontainers
class UserRepositoryIntegrationTest {

    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16")
        .withDatabaseName("test")
        .withUsername("test")
        .withPassword("test");

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
    }

    @Autowired UserRepository userRepository;

    @Test
    void savesAndRetrievesUser() {
        var user = new User(null, "test@example.com", "Test User");
        var saved = userRepository.save(user);

        assertThat(saved.getId()).isNotNull();
        assertThat(userRepository.findByEmail("test@example.com"))
            .isPresent()
            .hasValueSatisfying(u -> assertThat(u.getName()).isEqualTo("Test User"));
    }
}
```

---

_DOMYH Awesome Code v6.0.0 — Java Advanced Patterns — 2025-2026_
