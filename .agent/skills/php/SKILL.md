---
name: php
detect: ["composer.json", "*.php", "artisan", "symfony.lock"]
version: "4.3.0"
category: backend
tier: 1
---

# PHP Patterns — DOMYH Agent v4.3

> **Version**: PHP 8.3/8.4 (2025-2026)
> **Frameworks**: Laravel 12, Symfony 8
> **Philosophy**: Modern PHP with strict types, Property Hooks, and async patterns

---

## 🎯 When to Use This Skill

Use for: Web applications, APIs, Laravel/Symfony projects, WordPress plugins.
**NOT for**: CLI tools (→ rust/go), ML/AI (→ python).

---

## 📦 Recommended Stack (2025-2026)

### Frameworks

| Framework      | Use Case                  | PHP Version |
| -------------- | ------------------------- | ----------- |
| **Laravel 12** | Full-stack, APIs, SaaS 🏆 | 8.2+        |
| **Symfony 8**  | Enterprise, modular       | 8.4+        |
| **Slim 5**     | Micro-framework           | 8.2+        |

### Laravel Ecosystem

| Library            | Use Case              | Install                                      |
| ------------------ | --------------------- | -------------------------------------------- |
| **Livewire 3**     | Full-stack without JS | `composer require livewire/livewire`         |
| **Inertia.js**     | SPA with Vue/React    | `composer require inertiajs/inertia-laravel` |
| **Laravel Octane** | High performance      | `composer require laravel/octane`            |
| **Laravel Pulse**  | Real-time monitoring  | `composer require laravel/pulse`             |
| **Pest**           | Modern testing 🏆     | `composer require pestphp/pest --dev`        |

### Quality Tools

| Tool         | Use Case              | Install                                    |
| ------------ | --------------------- | ------------------------------------------ |
| **PHPStan**  | Static analysis 🏆    | `composer require phpstan/phpstan --dev`   |
| **Rector**   | Automated refactoring | `composer require rector/rector --dev`     |
| **Pint**     | Code styling          | `composer require laravel/pint --dev`      |
| **Larastan** | PHPStan for Laravel   | `composer require larastan/larastan --dev` |

### IDE Support

| IDE          | Plugin                      | Features                        |
| ------------ | --------------------------- | ------------------------------- |
| **PhpStorm** | Built-in                    | Full Laravel/Symfony support 🏆 |
| **VS Code**  | Intelephense + Laravel Pint | Code completion, formatting     |

---

## 🆕 PHP 8.4 Features (2025)

### Property Hooks

```php
<?php
declare(strict_types=1);

// ✅ Property Hooks - replace getters/setters
class User
{
    public string $name {
        set => ucfirst(strtolower($value));
        get => $this->name;
    }

    public string $email {
        set {
            if (!filter_var($value, FILTER_VALIDATE_EMAIL)) {
                throw new InvalidArgumentException("Invalid email");
            }
            $this->email = strtolower($value);
        }
    }

    // ✅ Virtual property (no storage)
    public string $displayName {
        get => $this->name;
    }
}
```

### Asymmetric Visibility

```php
<?php
// ✅ Different visibility for read/write
class BankAccount
{
    // Public read, private write
    public private(set) float $balance = 0.0;

    public function deposit(float $amount): void
    {
        $this->balance += $amount;
    }
}

$account = new BankAccount();
$account->deposit(100);
echo $account->balance;  // ✅ Can read
// $account->balance = 0; // ❌ Cannot write
```

### Modern Constructor

```php
<?php
// ✅ Constructor promotion with readonly (PHP 8.1+)
readonly class CreateUserDTO
{
    public function __construct(
        public string $email,
        public string $name,
        public ?string $phone = null,
    ) {}
}

// ✅ Combined with property hooks (PHP 8.4)
class User
{
    public function __construct(
        public string $email {
            set => strtolower($value);
        },
        public readonly string $id,
    ) {}
}
```

---

## 🏗️ Laravel Patterns

### Controller with Dependency Injection

```php
<?php
declare(strict_types=1);

namespace App\Http\Controllers;

use App\Services\UserService;
use App\Http\Requests\CreateUserRequest;
use App\Http\Resources\UserResource;
use Illuminate\Http\JsonResponse;

final class UserController extends Controller
{
    public function __construct(
        private readonly UserService $userService,
    ) {}

    public function index(): JsonResponse
    {
        $users = $this->userService->paginate(
            perPage: request()->integer('per_page', 20)
        );

        return UserResource::collection($users)
            ->response();
    }

    public function store(CreateUserRequest $request): JsonResponse
    {
        $user = $this->userService->create(
            $request->validated()
        );

        return UserResource::make($user)
            ->response()
            ->setStatusCode(201);
    }
}
```

### Service Pattern

```php
<?php
declare(strict_types=1);

namespace App\Services;

use App\Models\User;
use App\DTOs\CreateUserDTO;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;

final class UserService
{
    public function create(CreateUserDTO $dto): User
    {
        return DB::transaction(function () use ($dto) {
            $user = User::create([
                'name' => $dto->name,
                'email' => $dto->email,
                'password' => Hash::make($dto->password),
            ]);

            $user->profile()->create([
                'bio' => $dto->bio,
            ]);

            event(new UserCreated($user));

            return $user;
        });
    }
}
```

### Form Request Validation

```php
<?php
declare(strict_types=1);

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rules\Password;

final class CreateUserRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    /**
     * @return array<string, mixed>
     */
    public function rules(): array
    {
        return [
            'name' => ['required', 'string', 'max:255'],
            'email' => ['required', 'email', 'unique:users,email'],
            'password' => ['required', Password::defaults()],
            'bio' => ['nullable', 'string', 'max:1000'],
        ];
    }
}
```

### Eloquent with Query Scopes

```php
<?php
declare(strict_types=1);

namespace App\Models;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

final class User extends Model
{
    protected $fillable = ['name', 'email', 'password'];

    protected $hidden = ['password', 'remember_token'];

    protected $casts = [
        'email_verified_at' => 'datetime',
        'password' => 'hashed',
    ];

    // ✅ Relationship
    public function posts(): HasMany
    {
        return $this->hasMany(Post::class);
    }

    // ✅ Query Scope
    public function scopeActive(Builder $query): Builder
    {
        return $query->where('is_active', true);
    }

    // ✅ Named Scope
    public function scopeVerified(Builder $query): Builder
    {
        return $query->whereNotNull('email_verified_at');
    }
}

// Usage
$users = User::active()
    ->verified()
    ->with('posts')
    ->latest()
    ->paginate(20);
```

---

## 🎭 Enums (PHP 8.1+)

```php
<?php
declare(strict_types=1);

namespace App\Enums;

enum OrderStatus: string
{
    case Pending = 'pending';
    case Processing = 'processing';
    case Shipped = 'shipped';
    case Delivered = 'delivered';
    case Cancelled = 'cancelled';

    public function label(): string
    {
        return match($this) {
            self::Pending => 'Chờ xử lý',
            self::Processing => 'Đang xử lý',
            self::Shipped => 'Đã gửi',
            self::Delivered => 'Đã giao',
            self::Cancelled => 'Đã hủy',
        };
    }

    public function color(): string
    {
        return match($this) {
            self::Pending => 'yellow',
            self::Processing => 'blue',
            self::Shipped => 'purple',
            self::Delivered => 'green',
            self::Cancelled => 'red',
        };
    }

    public function canTransitionTo(self $status): bool
    {
        return match($this) {
            self::Pending => in_array($status, [self::Processing, self::Cancelled]),
            self::Processing => in_array($status, [self::Shipped, self::Cancelled]),
            self::Shipped => in_array($status, [self::Delivered]),
            default => false,
        };
    }
}
```

---

## 🧪 Testing with Pest

```php
<?php
// tests/Feature/UserTest.php

use App\Models\User;

describe('User Management', function () {
    it('can create a user', function () {
        $response = $this->postJson('/api/users', [
            'name' => 'John Doe',
            'email' => 'john@example.com',
            'password' => 'password123',
        ]);

        $response->assertCreated()
            ->assertJsonPath('data.name', 'John Doe');

        $this->assertDatabaseHas('users', [
            'email' => 'john@example.com',
        ]);
    });

    it('validates required fields', function () {
        $this->postJson('/api/users', [])
            ->assertUnprocessable()
            ->assertJsonValidationErrors(['name', 'email', 'password']);
    });

    it('requires unique email', function () {
        User::factory()->create(['email' => 'john@example.com']);

        $this->postJson('/api/users', [
            'name' => 'John Doe',
            'email' => 'john@example.com',
            'password' => 'password123',
        ])->assertUnprocessable()
            ->assertJsonValidationErrors(['email']);
    });
});

// ✅ Unit test for service
describe('UserService', function () {
    it('creates user with profile', function () {
        $dto = new CreateUserDTO(
            name: 'John',
            email: 'john@example.com',
            password: 'secret',
        );

        $user = app(UserService::class)->create($dto);

        expect($user)
            ->name->toBe('John')
            ->email->toBe('john@example.com');

        expect($user->profile)->not->toBeNull();
    });
});
```

---

## 📊 Static Analysis (PHPStan)

```neon
# phpstan.neon
includes:
    - vendor/larastan/larastan/extension.neon

parameters:
    # ✅ Level 9 or 10 recommended for 2026
    level: 9

    paths:
        - app
        - tests

    excludePaths:
        - app/Providers

    checkMissingIterableValueType: true
    checkGenericClassInNonGenericObjectType: true
```

```bash
# Run analysis
vendor/bin/phpstan analyse --memory-limit=2G
```

---

## ✅ Production Checklist

### Code Quality

- [ ] PHP 8.4+ features used
- [ ] `declare(strict_types=1)` everywhere
- [ ] PHPStan level 9+ passing
- [ ] PSR-12 coding style (Pint)
- [ ] All classes are `final` or `readonly`

### Performance

- [ ] OPcache enabled
- [ ] JIT enabled for CPU tasks
- [ ] Laravel Octane for high traffic
- [ ] Database queries optimized (N+1)

### Security

- [ ] All inputs validated
- [ ] SQL injection prevented (Eloquent)
- [ ] XSS prevented (Blade escaping)
- [ ] CSRF tokens on forms
- [ ] Secrets in .env, not code

### Testing

- [ ] Pest/PHPUnit tests passing
- [ ] Feature tests for API
- [ ] Unit tests for services
- [ ] Test coverage > 80%

---

_DOMYH Agent v4.3 • PHP 8.3/8.4_
