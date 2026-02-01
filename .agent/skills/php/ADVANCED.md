# PHP — Advanced Patterns

# DOMYH Agent v4.2 — Tier 3 Reference

## Table of Contents

- [Modern PHP Features](#modern-php-features)
- [Design Patterns](#design-patterns)
- [Performance](#performance)
- [Testing](#testing)

---

## Modern PHP Features

### Attributes (PHP 8)

```php
#[Attribute(Attribute::TARGET_METHOD)]
class Route {
    public function __construct(
        public string $path,
        public string $method = 'GET'
    ) {}
}

class UserController {
    #[Route('/users', 'GET')]
    public function index(): Response {
        return new JsonResponse($this->users->all());
    }

    #[Route('/users/{id}', 'GET')]
    public function show(int $id): Response {
        return new JsonResponse($this->users->find($id));
    }
}

// Route discovery
$routes = [];
$reflection = new ReflectionClass(UserController::class);
foreach ($reflection->getMethods() as $method) {
    $attributes = $method->getAttributes(Route::class);
    foreach ($attributes as $attr) {
        $route = $attr->newInstance();
        $routes[$route->path] = [$route->method, $method->getName()];
    }
}
```

### Enums & Match

```php
enum Status: string {
    case Pending = 'pending';
    case Approved = 'approved';
    case Rejected = 'rejected';

    public function label(): string {
        return match($this) {
            self::Pending => 'Đang chờ',
            self::Approved => 'Đã duyệt',
            self::Rejected => 'Từ chối',
        };
    }
}

// Match expression
$result = match($status) {
    Status::Pending => $this->handlePending(),
    Status::Approved => $this->handleApproved(),
    default => throw new InvalidStatusException(),
};
```

---

## Design Patterns

### Repository Pattern

```php
interface UserRepositoryInterface {
    public function find(int $id): ?User;
    public function findByEmail(string $email): ?User;
    public function save(User $user): void;
}

class EloquentUserRepository implements UserRepositoryInterface {
    public function find(int $id): ?User {
        return User::find($id);
    }

    public function findByEmail(string $email): ?User {
        return User::where('email', $email)->first();
    }

    public function save(User $user): void {
        $user->save();
    }
}
```

### Service Container

```php
class Container {
    private array $bindings = [];
    private array $instances = [];

    public function bind(string $abstract, Closure $concrete): void {
        $this->bindings[$abstract] = $concrete;
    }

    public function singleton(string $abstract, Closure $concrete): void {
        $this->bind($abstract, function($c) use ($abstract, $concrete) {
            if (!isset($this->instances[$abstract])) {
                $this->instances[$abstract] = $concrete($c);
            }
            return $this->instances[$abstract];
        });
    }

    public function make(string $abstract): mixed {
        if (isset($this->bindings[$abstract])) {
            return $this->bindings[$abstract]($this);
        }
        return new $abstract();
    }
}
```

---

## Performance

### Opcache Preloading

```php
// preload.php
$files = [
    __DIR__ . '/src/Core/Container.php',
    __DIR__ . '/src/Http/Request.php',
    __DIR__ . '/src/Http/Response.php',
];

foreach ($files as $file) {
    opcache_compile_file($file);
}

// php.ini
// opcache.preload=/path/to/preload.php
// opcache.preload_user=www-data
```

### Generators for Memory Efficiency

```php
// Instead of loading entire file into memory
function readLargeFile(string $path): Generator {
    $handle = fopen($path, 'r');
    while (!feof($handle)) {
        yield fgets($handle);
    }
    fclose($handle);
}

// Process line by line with constant memory
foreach (readLargeFile('huge.log') as $line) {
    processLine($line);
}
```

---

## Testing

### Mocking with PHPUnit

```php
class OrderServiceTest extends TestCase {
    public function test_creates_order_with_payment(): void {
        $paymentGateway = $this->createMock(PaymentGateway::class);
        $paymentGateway->expects($this->once())
            ->method('charge')
            ->with(1000)
            ->willReturn(new PaymentResult(success: true));

        $service = new OrderService($paymentGateway);
        $order = $service->create(['amount' => 1000]);

        $this->assertEquals('paid', $order->status);
    }
}
```

---

_DOMYH Agent v4.2 — Tier 3 Reference_
