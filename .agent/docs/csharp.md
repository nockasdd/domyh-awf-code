---
library: csharp
version: "14"
latest: true
category: language
official_docs: https://learn.microsoft.com/en-us/dotnet/csharp/
last_updated: 2026-03-21
last_checked: 2026-03-21
source: ai-enhanced from learn.microsoft.com + web research
---

# C# 14 (.NET 10)

> C# — A modern, object-oriented, type-safe programming language for the .NET platform.
> Current: C# 14 / .NET 10.0 LTS (Nov 2025) | Previous: C# 13 / .NET 9 STS
> Docs: https://learn.microsoft.com/en-us/dotnet/csharp/

## Version Comparison

| Feature | C# 12 / .NET 8 | C# 13 / .NET 9 | C# 14 / .NET 10 |
|:--------|:---------------|:---------------|:----------------|
| Support | LTS (Nov 2026) | STS (May 2026) | **LTS (Nov 2028)** |
| `params` collections (Span, etc.) | ❌ | ✅ | ✅ |
| `System.Threading.Lock` | ❌ | ✅ | ✅ |
| `field` keyword (property backing) | ❌ | Preview | ✅ Stable |
| Extension members (methods+props) | ❌ | ❌ | ✅ New |
| Null-conditional assignment (`?.=`) | ❌ | ❌ | ✅ |
| Partial constructors & events | ❌ | ❌ | ✅ |
| `ref struct` in generics | ❌ | ✅ | ✅ |
| `\e` escape sequence | ❌ | ✅ | ✅ |
| AI Agent Framework | ❌ | ❌ | ✅ |
| EF Core vector search | ❌ | ❌ | ✅ |
| NativeAOT improvements | Basic | Better | ✅ Best |
| Post-quantum crypto | ❌ | ❌ | ✅ |
| `BinaryFormatter` | ⚠️ Deprecated | ❌ Removed (WinForms) | ❌ |

## Installation

```bash
# .NET SDK (includes C# compiler)
# Windows (winget)
winget install Microsoft.DotNet.SDK.10

# macOS (Homebrew)
brew install dotnet-sdk

# Linux (Ubuntu/Debian)
sudo apt-get install -y dotnet-sdk-10.0

# Docker
docker run -it mcr.microsoft.com/dotnet/sdk:10.0

# Verify
dotnet --version    # 10.0.xxx
dotnet --list-sdks
```

## Configuration

```xml
<!-- project.csproj — SDK-style project -->
<Project Sdk="Microsoft.NET.Sdk.Web">
  <PropertyGroup>
    <TargetFramework>net10.0</TargetFramework>
    <LangVersion>14</LangVersion>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Microsoft.EntityFrameworkCore" Version="10.0.0" />
    <PackageReference Include="Microsoft.Extensions.AI" Version="10.0.0" />
  </ItemGroup>
</Project>
```

```json
// appsettings.json
{
  "ConnectionStrings": {
    "Default": "Server=.;Database=MyApp;Trusted_Connection=true"
  },
  "Logging": {
    "LogLevel": { "Default": "Information" }
  }
}
```

## Core API

### Types & Variables

```csharp
// Value types
int count = 42;
double pi = 3.14159;
bool isActive = true;
char grade = 'A';
decimal price = 19.99m;

// Reference types
string name = "C#";
int[] numbers = [1, 2, 3, 4, 5];  // C# 12: collection expressions
List<string> names = ["Alice", "Bob"];

// Nullable reference types (enable in .csproj)
string? nullable = null;       // OK — explicitly nullable
string nonNull = "hello";      // Warning if assigned null

// Records (C# 9+) — immutable value objects
public record Point(double X, double Y);
public record struct Vector(double X, double Y);  // value type record

// Tuples
var (name, age) = ("Alice", 30);
(string Name, int Age) person = ("Bob", 25);

// Pattern matching
var result = shape switch
{
    Circle { Radius: > 0 } c => Math.PI * c.Radius * c.Radius,
    Rectangle { Width: var w, Height: var h } => w * h,
    null => 0,
    _ => throw new ArgumentException("Unknown shape")
};
```

### C# 13 Features

```csharp
// params collections — no longer limited to arrays
public void Log(params ReadOnlySpan<string> messages)
{
    foreach (var msg in messages)
        Console.WriteLine(msg);
}
Log("info", "warning", "error");  // ← zero allocation with Span

// System.Threading.Lock — better than Monitor
private readonly Lock _lock = new();

public void ThreadSafeMethod()
{
    lock (_lock)  // compiler uses Lock.EnterScope() automatically
    {
        // critical section — more efficient than lock(object)
    }
}

// Escape sequence \e
string escapeCode = "\e[31m";  // ANSI red text

// ref struct in generics
public T Process<T>(T value) where T : allows ref struct
{
    // can now accept Span<T>, ReadOnlySpan<T> etc.
    return value;
}

// Implicit index in object initializers
var countdown = new int[5]
{
    [^1] = 1,  // last element
    [^2] = 2,
    [^3] = 3,
};
```

### C# 14 Features

```csharp
// Extension members — methods, properties, and events
public static extension UserExtensions for User
{
    public string FullName => $"{this.FirstName} {this.LastName}";

    public bool IsAdult => this.Age >= 18;

    public void Greet() => Console.WriteLine($"Hello, {this.FullName}!");
}

User user = new("Alice", "Smith", 30);
Console.WriteLine(user.FullName);  // "Alice Smith"
user.Greet();

// field keyword — access backing field in properties
public class Temperature
{
    public double Celsius
    {
        get => field;
        set => field = value < -273.15
            ? throw new ArgumentException("Below absolute zero")
            : value;
    }
    // No need for: private double _celsius;
}

// Null-conditional assignment
user?.Address?.City = "New York";  // only assigns if path is not null

// Partial constructors
public partial class DataProcessor
{
    public partial DataProcessor(string connectionString);
}

// Implementation (e.g., source generator)
public partial class DataProcessor
{
    public partial DataProcessor(string connectionString)
    {
        _connection = new SqlConnection(connectionString);
    }
}

// nameof with unbound generics
string name = nameof(List<>);   // "List"
string name2 = nameof(Dictionary<,>);  // "Dictionary"

// Implicit Span conversions
void Process(ReadOnlySpan<byte> data) { }
byte[] buffer = new byte[1024];
Process(buffer);  // implicit conversion — no .AsSpan() needed
```

### LINQ

```csharp
// Essential LINQ operations
var users = dbContext.Users
    .Where(u => u.IsActive)
    .OrderBy(u => u.LastName)
    .Select(u => new { u.FullName, u.Email })
    .ToList();

// .NET 9: CountBy, AggregateBy
var countByCity = users.CountBy(u => u.City);
var totalByDept = employees.AggregateBy(
    e => e.Department,
    seed: 0m,
    (total, e) => total + e.Salary
);

// .NET 10: LeftJoin, RightJoin (EF Core)
var result = users
    .LeftJoin(orders,
        u => u.Id,
        o => o.UserId,
        (user, order) => new { user.Name, order?.Total });

// Async LINQ
await foreach (var item in GetDataAsync())
{
    Process(item);
}
```

### Async/Await

```csharp
// Basic async pattern
public async Task<User> GetUserAsync(int id)
{
    var user = await _repository.FindByIdAsync(id);
    return user ?? throw new NotFoundException($"User {id} not found");
}

// Parallel async
var tasks = userIds.Select(id => GetUserAsync(id));
User[] users = await Task.WhenAll(tasks);

// Cancellation
public async Task ProcessAsync(CancellationToken ct = default)
{
    while (!ct.IsCancellationRequested)
    {
        await Task.Delay(1000, ct);
        await DoWorkAsync(ct);
    }
}

// IAsyncEnumerable — streaming
public async IAsyncEnumerable<int> GenerateAsync(
    [EnumeratorCancellation] CancellationToken ct = default)
{
    for (int i = 0; i < 100; i++)
    {
        ct.ThrowIfCancellationRequested();
        yield return await ComputeAsync(i);
    }
}
```

### Dependency Injection

```csharp
// Program.cs — Minimal API (.NET 6+)
var builder = WebApplication.CreateBuilder(args);

// Register services
builder.Services.AddScoped<IUserService, UserService>();
builder.Services.AddSingleton<ICacheService, RedisCacheService>();
builder.Services.AddTransient<IEmailService, SmtpEmailService>();

// Named/Keyed services (.NET 8+)
builder.Services.AddKeyedSingleton<ICache>("redis", new RedisCache());
builder.Services.AddKeyedSingleton<ICache>("memory", new MemoryCache());

var app = builder.Build();

// Minimal API endpoints
app.MapGet("/users/{id}", async (int id, IUserService svc) =>
    await svc.GetByIdAsync(id) is { } user
        ? Results.Ok(user)
        : Results.NotFound());

app.MapPost("/users", async (CreateUserDto dto, IUserService svc) =>
{
    var user = await svc.CreateAsync(dto);
    return Results.Created($"/users/{user.Id}", user);
});

app.Run();
```

### Entity Framework Core

```csharp
// DbContext
public class AppDbContext : DbContext
{
    public DbSet<User> Users => Set<User>();
    public DbSet<Order> Orders => Set<Order>();

    protected override void OnModelCreating(ModelBuilder builder)
    {
        builder.Entity<User>(e =>
        {
            e.HasIndex(u => u.Email).IsUnique();
            e.HasMany(u => u.Orders).WithOne(o => o.User);
        });
    }
}

// Migrations
// dotnet ef migrations add InitialCreate
// dotnet ef database update

// Queries
var activeUsers = await dbContext.Users
    .Include(u => u.Orders)
    .Where(u => u.IsActive)
    .AsNoTracking()
    .ToListAsync();
```

## Common Patterns

```csharp
// 1. Result pattern (no exceptions for business logic)
public record Result<T>
{
    public T? Value { get; init; }
    public string? Error { get; init; }
    public bool IsSuccess => Error is null;

    public static Result<T> Success(T value) => new() { Value = value };
    public static Result<T> Failure(string error) => new() { Error = error };
}

// 2. Options pattern (strongly typed config)
public class SmtpOptions
{
    public const string Section = "Smtp";
    public string Host { get; set; } = "";
    public int Port { get; set; } = 587;
}
builder.Services.Configure<SmtpOptions>(config.GetSection(SmtpOptions.Section));

// 3. Middleware pattern (ASP.NET Core)
public class RequestTimingMiddleware(RequestDelegate next)
{
    public async Task InvokeAsync(HttpContext context)
    {
        var sw = Stopwatch.StartNew();
        await next(context);
        context.Response.Headers["X-Response-Time"] = $"{sw.ElapsedMilliseconds}ms";
    }
}
app.UseMiddleware<RequestTimingMiddleware>();

// 4. MediatR / CQRS
public record GetUserQuery(int Id) : IRequest<User>;

public class GetUserHandler(AppDbContext db) : IRequestHandler<GetUserQuery, User>
{
    public async Task<User> Handle(GetUserQuery request, CancellationToken ct)
        => await db.Users.FindAsync(request.Id, ct)
           ?? throw new NotFoundException();
}
```

## Gotchas & Breaking Changes

### General Gotchas

- ⚠️ **Nullable reference types**: Enabling `<Nullable>enable</Nullable>` generates warnings for ALL existing code. Migrate gradually.
- ⚠️ **`async void`**: Only use for event handlers. Exceptions in `async void` crash the app — use `async Task` instead.
- ⚠️ **`ConfigureAwait(false)`**: In library code, always use `.ConfigureAwait(false)` to avoid deadlocks. In ASP.NET Core, it's not needed (no SynchronizationContext).
- ⚠️ **EF Core lazy loading**: Disabled by default. `Include()` is eager loading. Lazy loading requires `Microsoft.EntityFrameworkCore.Proxies`.
- ⚠️ **`IDisposable` leaks**: Always use `using` or DI for disposable resources. `HttpClient` should be singleton via `IHttpClientFactory`.
- ⚠️ **String comparison**: `==` does ordinal comparison. For culture-aware: `string.Compare(a, b, StringComparison.CurrentCulture)`.
- ⚠️ **`Task.Result` / `.Wait()`**: Blocks thread and can deadlock. Always `await` instead.
- ⚠️ **LINQ deferred execution**: `Where()`, `Select()` don't execute until `.ToList()` / `.FirstOrDefault()` etc. Database queries may fail late.

### C# 14 / .NET 10 Breaking Changes

- ⚠️ **`field` keyword naming conflict**: If your class has a member named `field`, it conflicts with the new keyword. Rename it.
- ⚠️ **.NET 10 is LTS**: Migrate from .NET 9 (STS, EOL May 2026) to .NET 10 for long-term support.
- ⚠️ **Keyed services strict (since .NET 9)**: Resolving unregistered keyed service throws `InvalidOperationException` (was silent in .NET 8).

### C# 13 / .NET 9 Breaking Changes

- ⚠️ **`BinaryFormatter` removed** in Windows Forms — use `System.Text.Json` or protobuf.
- ⚠️ **`ToString()` on nullable LINQ properties**: Returns empty string instead of null.
- ⚠️ **`Environment.SetEnvironmentVariable("", string.Empty)`**: Now sets empty value (was delete in .NET 8).

## Migration

### From .NET 8 (C# 12) → .NET 10 (C# 14)
1. Update `<TargetFramework>net10.0</TargetFramework>` and `<LangVersion>14</LangVersion>`
2. Update all NuGet packages to 10.x versions
3. Check for `field` naming conflicts with new keyword
4. Replace `BinaryFormatter` usage if any
5. Adopt `System.Threading.Lock` over `lock(object)`
6. Migrate `tools.json` / Windows Forms themes
7. Test keyed service resolution (strict since .NET 9)
8. Run `dotnet format` to clean up
9. Run full test suite — check nullable warnings

### From .NET 9 (C# 13) → .NET 10 (C# 14)
1. Update `<TargetFramework>net10.0</TargetFramework>`
2. Adopt extension members for cleaner code
3. Enable `field` keyword (was preview, now stable)
4. Use null-conditional assignment (`?.=`)
5. Review breaking changes list from Microsoft

<!--
BM25 DESIGN RULES:
- H1 = library name (root search anchor)
- H2 = feature category, add (vN) suffix for version matching
- Code:prose ratio ≥ 70:30
- Use ⚠️ diff notes for version disambiguation
- Keep 5-30KB per file, H2 sections ~50 lines each
-->
