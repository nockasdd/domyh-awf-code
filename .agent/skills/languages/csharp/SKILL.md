---
name: csharp
detect: ["*.csproj", "*.sln", "*.cs", "global.json"]
version: "6.2.7"
category: language
tier: 1
---

# C# Development Patterns — DOMYH Awesome Code

> Modern C# (C# 12/13/14) with .NET 9/10 — 2025-2026

## 🔍 Language Detection

```yaml
csharp_indicators:  # C# skill activates
  - ".cs files"
  - "*.csproj, *.sln"
  - "namespace, class, interface, record, struct"
  - "using System;"
  - "async Task, await"
  - "var, dynamic"
  - "LINQ: .Select(), .Where(), .OrderBy()"
  - "[Attribute] decorators"
  - "ASP.NET Core, Blazor, MAUI"

not_csharp:  # Other languages
  - ".cpp, .hpp" → C++
  - ".java" → Java
  - ".ts, .js" → TypeScript/JavaScript
  - ".py" → Python
```

---

## 📊 C# Standards Comparison (2025-2026)

| C# Version | .NET Version | Year | Key Features                                                     |
| ---------- | ------------ | ---- | ---------------------------------------------------------------- |
| **C# 11**  | .NET 7       | 2022 | raw strings, list patterns, required members                     |
| **C# 12**  | .NET 8 LTS   | 2023 | primary constructors, collection expressions, alias any type     |
| **C# 13**  | .NET 9       | 2024 | params collections, Lock type, field keyword, partial properties |
| **C# 14**  | .NET 10 LTS  | 2025 | extension members, null-conditional assignment, implicit span    |

---

## 🛠️ IDE & Toolchain Support (2025-2026)

### Visual Studio 2026

```yaml
version: VS 2026
features:
  - C# 14 / .NET 10 LTS full support
  - GitHub Copilot built-in (AI code generation)
  - Third-party AI assistants support
  - Enhanced debugging with AI insights
  - Faster startup, improved responsiveness
  - ASP.NET Core / Blazor / MAUI tooling
  - Azure integration
notes:
  - Windows primary (limited macOS via VS for Mac)
  - Resource intensive
```

### JetBrains Rider 2025.3+

```yaml
version: Rider 2025.3
features:
  - Day-one .NET 10 / C# 14 support
  - Extension members and operators
  - Cross-platform (Windows, macOS, Linux)
  - Unity, Unreal, Godot game dev support
  - AI Agent Protocol (ACP) integration
  - Fast startup, solution loading
notes:
  - Paid (free for students/educators)
  - IntelliJ-based refactoring
```

### VS Code + C# Dev Kit

```yaml
extensions_required:
  - "C# Dev Kit" (Microsoft)
  - "C#" (OmniSharp/Roslyn)
  - "NuGet Package Manager"
features:
  - Project/solution management
  - Roslyn-powered IntelliSense
  - Integrated testing (xUnit, NUnit, MSTest)
  - Debugging, refactoring
  - Cross-platform
notes:
  - Free, lightweight
  - Requires extension setup
  - Less integrated than full IDEs
```

---

## 📦 .NET Project Configuration

### SDK-Style .csproj (Recommended)

```xml
<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <TargetFramework>net10.0</TargetFramework>
    <LangVersion>14</LangVersion>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
    <EnforceCodeStyleInBuild>true</EnforceCodeStyleInBuild>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Microsoft.Extensions.DependencyInjection" Version="10.0.0" />
    <PackageReference Include="Serilog" Version="4.0.0" />
  </ItemGroup>

</Project>
```

### global.json (Lock SDK Version)

```json
{
  "sdk": {
    "version": "10.0.100",
    "rollForward": "latestPatch"
  }
}
```

---

## ✨ C# 12/13/14 Features

### C# 12: Primary Constructors

```csharp
// ✅ C# 12 - Primary constructor for classes
public class UserService(IUserRepository repo, ILogger<UserService> logger)
{
    public async Task<User?> GetAsync(int id)
    {
        logger.LogInformation("Fetching user {Id}", id);
        return await repo.FindAsync(id);
    }
}

// ✅ Primary constructor captures parameters as fields/properties
public class Point(int x, int y)
{
    public int X => x;
    public int Y => y;
    public double Distance => Math.Sqrt(x * x + y * y);
}
```

### C# 12: Collection Expressions

```csharp
// ✅ C# 12 - Concise collection initialization
int[] numbers = [1, 2, 3, 4, 5];
List<string> names = ["Alice", "Bob", "Charlie"];
Span<int> span = [1, 2, 3];

// ✅ Spread operator
int[] first = [1, 2, 3];
int[] second = [4, 5, 6];
int[] combined = [..first, ..second];  // [1, 2, 3, 4, 5, 6]

// ✅ With LINQ-like operations
int[] evens = [..numbers.Where(n => n % 2 == 0)];
```

### C# 12: Alias Any Type

```csharp
// ✅ C# 12 - Alias for any type (not just namespaces)
using Point = (int X, int Y);
using UserId = System.Int32;
using JsonDict = System.Collections.Generic.Dictionary<string, object>;

Point origin = (0, 0);
UserId userId = 42;
JsonDict data = new() { ["name"] = "Alice" };
```

### C# 13: params Collections

```csharp
// ✅ C# 13 - params works with any collection type
public void LogMessages(params List<string> messages)
{
    foreach (var msg in messages)
        Console.WriteLine(msg);
}

public void ProcessItems(params Span<int> items)
{
    // High-performance stack allocation
}

// Usage
LogMessages(["Error", "Warning", "Info"]);
ProcessItems([1, 2, 3, 4, 5]);
```

### C# 13: New Lock Type

```csharp
// ✅ C# 13 - Dedicated Lock type (better performance)
using System.Threading;

public class ThreadSafeCounter
{
    private readonly Lock _lock = new();  // New Lock type!
    private int _count;

    public void Increment()
    {
        lock (_lock)  // Optimized locking
        {
            _count++;
        }
    }

    // Old way (still works but less optimal)
    // private readonly object _syncRoot = new();
}
```

### C# 13: Partial Properties

```csharp
// ✅ C# 13 - Partial properties and indexers
public partial class GeneratedEntity
{
    public partial string Name { get; set; }
    public partial int this[string key] { get; }
}

// In generated code:
public partial class GeneratedEntity
{
    private string _name = "";
    private Dictionary<string, int> _data = new();

    public partial string Name
    {
        get => _name;
        set => _name = value ?? throw new ArgumentNullException();
    }

    public partial int this[string key] => _data[key];
}
```

### C# 13: field Keyword

```csharp
// ✅ C# 13 - Access backing field directly
public class Product
{
    public decimal Price
    {
        get => field;  // Access backing field
        set => field = value >= 0 ? value : throw new ArgumentException();
    }

    public string Name
    {
        get => field ?? "Unknown";
        set => field = value?.Trim();
    }
}
```

### C# 14: Extension Members (Preview)

```csharp
// ✅ C# 14 - Extension types with properties and operators
public extension StringExtensions for string
{
    public bool IsNullOrEmpty => string.IsNullOrEmpty(this);
    public string Reversed => new(this.Reverse().ToArray());

    public static implicit operator int(string s) => int.Parse(s);
}

// Usage
string name = "Hello";
bool empty = name.IsNullOrEmpty;  // false
string rev = name.Reversed;       // "olleH"
```

---

## 📚 BCL APIs Reference

### System.Text.Json (Preferred for JSON)

```csharp
using System.Text.Json;

// ✅ Serialize/Deserialize
var user = new User("Alice", 30);
string json = JsonSerializer.Serialize(user);
User? parsed = JsonSerializer.Deserialize<User>(json);

// ✅ Configure options (REUSE this instance!)
var options = new JsonSerializerOptions
{
    PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
    WriteIndented = true,
    DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull
};

// ✅ .NET 10 Strict mode
var strictOptions = JsonSerializerOptions.Strict;  // Rejects ambiguous JSON

// ✅ Async streaming
await using var stream = File.OpenRead("data.json");
var items = await JsonSerializer.DeserializeAsync<List<Item>>(stream);

// ✅ Source generators (AOT-friendly)
[JsonSerializable(typeof(User))]
public partial class AppJsonContext : JsonSerializerContext { }
```

### LINQ (Language Integrated Query)

```csharp
using System.Linq;

// ✅ Query syntax
var adults = from u in users
             where u.Age >= 18
             orderby u.Name
             select u;

// ✅ Method syntax (preferred for chaining)
var result = users
    .Where(u => u.IsActive)
    .OrderByDescending(u => u.CreatedAt)
    .Select(u => new { u.Id, u.Name })
    .Take(10)
    .ToList();

// ✅ .NET 9 new methods
var countByCategory = products.CountBy(p => p.Category);
var sumByCategory = products.AggregateBy(
    p => p.Category,
    0m,
    (sum, p) => sum + p.Price
);

// ⚠️ Best Practices
// - Use Any() instead of Count() > 0
// - Project early: .Select() before .ToList()
// - Understand deferred vs immediate execution
```

### Entity Framework Core 10

```csharp
using Microsoft.EntityFrameworkCore;

// ✅ DbContext setup
public class AppDbContext(DbContextOptions<AppDbContext> options)
    : DbContext(options)
{
    public DbSet<User> Users => Set<User>();
    public DbSet<Order> Orders => Set<Order>();
}

// ✅ Async all the way
public async Task<User?> GetUserAsync(int id) =>
    await _context.Users.FindAsync(id);

// ✅ AsNoTracking for read-only
var users = await _context.Users
    .AsNoTracking()
    .Where(u => u.IsActive)
    .ToListAsync();

// ✅ Projection (avoid SELECT *)
var dtos = await _context.Users
    .Select(u => new UserDto(u.Id, u.Name, u.Email))
    .ToListAsync();

// ✅ Eager loading (avoid N+1)
var ordersWithItems = await _context.Orders
    .Include(o => o.Items)
    .Include(o => o.Customer)
    .ToListAsync();

// ✅ Compiled queries (high-performance)
private static readonly Func<AppDbContext, int, Task<User?>> GetUserById =
    EF.CompileAsyncQuery((AppDbContext ctx, int id) =>
        ctx.Users.FirstOrDefault(u => u.Id == id));

// ✅ Batch operations (EF Core 7+)
await _context.Users
    .Where(u => u.LastLoginAt < cutoff)
    .ExecuteDeleteAsync();

await _context.Products
    .Where(p => p.CategoryId == oldCategoryId)
    .ExecuteUpdateAsync(p => p.SetProperty(x => x.CategoryId, newCategoryId));
```

---

## 🌐 ASP.NET Core Patterns

### Minimal API (.NET 9+)

```csharp
var builder = WebApplication.CreateBuilder(args);

// Services
builder.Services.AddScoped<IUserService, UserService>();
builder.Services.AddDbContext<AppDbContext>();

var app = builder.Build();

// Endpoints
app.MapGet("/users/{id:int}", async (int id, IUserService service) =>
    await service.GetAsync(id) is User user
        ? Results.Ok(user)
        : Results.NotFound());

app.MapPost("/users", async (CreateUserDto dto, IUserService service) =>
{
    var user = await service.CreateAsync(dto);
    return Results.Created($"/users/{user.Id}", user);
});

// Endpoint groups
var api = app.MapGroup("/api/v1");
api.MapGet("/health", () => Results.Ok(new { Status = "Healthy" }));

app.Run();
```

### Controller-Based API

```csharp
[ApiController]
[Route("api/[controller]")]
public class UsersController(IUserService userService) : ControllerBase
{
    [HttpGet("{id:int}")]
    [ProducesResponseType<User>(StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> Get(int id)
    {
        var user = await userService.GetAsync(id);
        return user is null ? NotFound() : Ok(user);
    }

    [HttpPost]
    [ProducesResponseType<User>(StatusCodes.Status201Created)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    public async Task<IActionResult> Create([FromBody] CreateUserDto dto)
    {
        var user = await userService.CreateAsync(dto);
        return CreatedAtAction(nameof(Get), new { id = user.Id }, user);
    }
}
```

### Dependency Injection

```csharp
// ✅ Registration
builder.Services.AddScoped<IUserRepository, UserRepository>();
builder.Services.AddSingleton<ICacheService, RedisCacheService>();
builder.Services.AddTransient<IEmailSender, SmtpEmailSender>();

// ✅ Options pattern
builder.Services.Configure<EmailOptions>(
    builder.Configuration.GetSection("Email"));

// ✅ HttpClientFactory
builder.Services.AddHttpClient<IPaymentClient, PaymentClient>(client =>
{
    client.BaseAddress = new Uri("https://api.payment.com/");
    client.Timeout = TimeSpan.FromSeconds(30);
});
```

---

## 📦 Essential Libraries (2025-2026)

### Core Frameworks

| Library          | Purpose                       | NuGet      |
| ---------------- | ----------------------------- | ---------- |
| **ASP.NET Core** | Web APIs, MVC, Razor          | Built-in   |
| **Blazor**       | Full-stack C# web             | Built-in   |
| **MAUI**         | Cross-platform mobile/desktop | Built-in   |
| **.NET Aspire**  | Cloud-native orchestration    | `Aspire.*` |

### Database & ORM

| Library            | Purpose           | When to Use            |
| ------------------ | ----------------- | ---------------------- |
| **EF Core 10**     | Full ORM          | Complex domain models  |
| **Dapper**         | Micro-ORM         | Raw SQL, performance   |
| **Npgsql**         | PostgreSQL driver | Direct Postgres access |
| **MongoDB.Driver** | MongoDB           | Document databases     |

### Logging & Diagnostics

| Library                  | Purpose             |
| ------------------------ | ------------------- |
| **Serilog**              | Structured logging  |
| **OpenTelemetry**        | Distributed tracing |
| **Application Insights** | Azure monitoring    |

### Communication

| Library         | Purpose                          |
| --------------- | -------------------------------- |
| **MassTransit** | Message bus (RabbitMQ, Azure SB) |
| **gRPC**        | High-performance RPC             |
| **SignalR**     | Real-time WebSocket              |

### Utilities

| Library              | Purpose                             |
| -------------------- | ----------------------------------- |
| **FluentValidation** | Validation rules                    |
| **AutoMapper**       | Object mapping                      |
| **MediatR**          | CQRS/Mediator pattern               |
| **Polly**            | Resilience (retry, circuit breaker) |
| **Hangfire**         | Background jobs                     |
| **Quartz.NET**       | Job scheduling                      |

### Testing

| Library              | Purpose                         |
| -------------------- | ------------------------------- |
| **xUnit**            | Testing framework (recommended) |
| **NUnit**            | Testing framework               |
| **Moq**              | Mocking framework               |
| **NSubstitute**      | Mocking framework               |
| **FluentAssertions** | Assertion library               |
| **Testcontainers**   | Integration testing             |

### Blazor UI

| Library               | Purpose                    |
| --------------------- | -------------------------- |
| **MudBlazor**         | Material Design components |
| **Blazorise**         | Multi-framework components |
| **Radzen**            | Business components        |
| **Syncfusion Blazor** | Enterprise components      |

---

## ✅ Production Checklist

### Code Quality

- [ ] .NET 10 LTS / C# 14 used
- [ ] Nullable reference types enabled (`<Nullable>enable</Nullable>`)
- [ ] TreatWarningsAsErrors enabled
- [ ] Static code analysis (SonarQube, Qodana)
- [ ] EditorConfig enforced

### Architecture

- [ ] Dependency Injection used
- [ ] async/await throughout
- [ ] Records for DTOs
- [ ] Result pattern for error handling
- [ ] Minimal APIs or clean controllers

### Performance

- [ ] AsNoTracking for read-only queries
- [ ] Projection before materialization
- [ ] JsonSerializerOptions reused
- [ ] HttpClientFactory used
- [ ] Caching implemented (MemoryCache, Redis)

### Testing

- [ ] Unit tests (xUnit/NUnit)
- [ ] Integration tests (Testcontainers)
- [ ] Architecture tests (NetArchTest)
- [ ] Code coverage ≥80%

### Security

- [ ] HTTPS enforced
- [ ] Authentication/Authorization configured
- [ ] Secrets in Azure Key Vault / User Secrets
- [ ] Input validation (FluentValidation)
- [ ] Rate limiting enabled

### Observability

- [ ] Structured logging (Serilog)
- [ ] OpenTelemetry traces
- [ ] Health checks configured
- [ ] Metrics exposed

---

_DOMYH Awesome Code • C# Development (C# 12/13/14 • .NET 9/10) • 2025-2026_
