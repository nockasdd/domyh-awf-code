# C# — Advanced Patterns

> DOMYH Awesome Code — Tier 3 Reference

## Table of Contents

- [Async Advanced Patterns](#async-advanced-patterns)
- [LINQ Expression Trees](#linq-expression-trees)
- [Source Generators](#source-generators)
- [Dependency Injection Advanced](#dependency-injection-advanced)
- [Performance Optimization](#performance-optimization)
- [Domain-Driven Design](#domain-driven-design)

---

## Async Advanced Patterns

### ValueTask for Hot Paths

```csharp
// ValueTask avoids allocation when result is cached
private int? _cachedValue;

public ValueTask<int> GetValueAsync()
{
    if (_cachedValue.HasValue)
    {
        return ValueTask.FromResult(_cachedValue.Value);
    }
    return new ValueTask<int>(FetchValueAsync());
}

private async Task<int> FetchValueAsync()
{
    var value = await _repository.GetAsync();
    _cachedValue = value;
    return value;
}
```

### Channel for Producer-Consumer

```csharp
using System.Threading.Channels;

public class EventProcessor
{
    private readonly Channel<Event> _channel = Channel.CreateBounded<Event>(
        new BoundedChannelOptions(1000)
        {
            FullMode = BoundedChannelFullMode.Wait
        });

    public async Task StartAsync(CancellationToken ct)
    {
        await foreach (var evt in _channel.Reader.ReadAllAsync(ct))
        {
            await ProcessEventAsync(evt);
        }
    }

    public async ValueTask EnqueueAsync(Event evt)
    {
        await _channel.Writer.WriteAsync(evt);
    }
}
```

### TaskCompletionSource for Manual Control

```csharp
public class AsyncOperation
{
    private readonly TaskCompletionSource<Result> _tcs = new();

    public Task<Result> WaitForCompletionAsync() => _tcs.Task;

    public void Complete(Result result) => _tcs.TrySetResult(result);
    public void Fail(Exception ex) => _tcs.TrySetException(ex);
    public void Cancel() => _tcs.TrySetCanceled();
}
```

### IAsyncEnumerable Streaming

```csharp
public async IAsyncEnumerable<User> GetUsersStreamAsync(
    [EnumeratorCancellation] CancellationToken ct = default)
{
    await foreach (var batch in _repository.GetBatchesAsync(ct))
    {
        foreach (var user in batch)
        {
            yield return user;
        }
    }
}

// Consuming
await foreach (var user in GetUsersStreamAsync(cancellationToken))
{
    await ProcessUserAsync(user);
}
```

---

## LINQ Expression Trees

### Dynamic Filter Builder

```csharp
public static Expression<Func<T, bool>> BuildFilter<T>(string property, object value)
{
    var param = Expression.Parameter(typeof(T), "x");
    var prop = Expression.Property(param, property);
    var constant = Expression.Constant(value);
    var equal = Expression.Equal(prop, constant);
    return Expression.Lambda<Func<T, bool>>(equal, param);
}

// Usage
var filter = BuildFilter<User>("Age", 25);
var adults = _context.Users.Where(filter).ToList();
```

### Combining Expressions

```csharp
public static class ExpressionExtensions
{
    public static Expression<Func<T, bool>> And<T>(
        this Expression<Func<T, bool>> left,
        Expression<Func<T, bool>> right)
    {
        var param = Expression.Parameter(typeof(T));
        var body = Expression.AndAlso(
            Expression.Invoke(left, param),
            Expression.Invoke(right, param));
        return Expression.Lambda<Func<T, bool>>(body, param);
    }

    public static Expression<Func<T, bool>> Or<T>(
        this Expression<Func<T, bool>> left,
        Expression<Func<T, bool>> right)
    {
        var param = Expression.Parameter(typeof(T));
        var body = Expression.OrElse(
            Expression.Invoke(left, param),
            Expression.Invoke(right, param));
        return Expression.Lambda<Func<T, bool>>(body, param);
    }
}

// Usage
Expression<Func<User, bool>> isAdult = u => u.Age >= 18;
Expression<Func<User, bool>> isActive = u => u.IsActive;
var combined = isAdult.And(isActive);
```

### Custom LINQ Extensions

```csharp
public static class LinqExtensions
{
    public static IEnumerable<IEnumerable<T>> Batch<T>(
        this IEnumerable<T> source, int size)
    {
        var batch = new List<T>(size);
        foreach (var item in source)
        {
            batch.Add(item);
            if (batch.Count >= size)
            {
                yield return batch;
                batch = new List<T>(size);
            }
        }
        if (batch.Count > 0)
            yield return batch;
    }

    public static async IAsyncEnumerable<List<T>> BatchAsync<T>(
        this IAsyncEnumerable<T> source,
        int size,
        [EnumeratorCancellation] CancellationToken ct = default)
    {
        var batch = new List<T>(size);
        await foreach (var item in source.WithCancellation(ct))
        {
            batch.Add(item);
            if (batch.Count >= size)
            {
                yield return batch;
                batch = new List<T>(size);
            }
        }
        if (batch.Count > 0)
            yield return batch;
    }
}
```

---

## Source Generators

### Incremental Generator (Modern Pattern)

```csharp
[Generator]
public class DtoGenerator : IIncrementalGenerator
{
    public void Initialize(IncrementalGeneratorInitializationContext context)
    {
        // Find all classes with [GenerateDto] attribute
        var provider = context.SyntaxProvider
            .ForAttributeWithMetadataName(
                "MyApp.GenerateDtoAttribute",
                predicate: (node, _) => node is ClassDeclarationSyntax,
                transform: (ctx, _) => GetDtoInfo(ctx))
            .Where(info => info is not null);

        context.RegisterSourceOutput(provider, Execute!);
    }

    private static DtoInfo? GetDtoInfo(GeneratorAttributeSyntaxContext ctx)
    {
        var classSymbol = ctx.TargetSymbol as INamedTypeSymbol;
        if (classSymbol is null) return null;

        return new DtoInfo(
            classSymbol.Name,
            classSymbol.ContainingNamespace.ToDisplayString(),
            GetProperties(classSymbol));
    }

    private static void Execute(SourceProductionContext context, DtoInfo info)
    {
        var source = GenerateDtoSource(info);
        context.AddSource($"{info.Name}Dto.g.cs", source);
    }
}
```

### System.Text.Json Source Generator

```csharp
// Define serialization context (AOT-friendly)
[JsonSerializable(typeof(User))]
[JsonSerializable(typeof(List<User>))]
[JsonSerializable(typeof(CreateUserRequest))]
[JsonSourceGenerationOptions(
    PropertyNamingPolicy = JsonKnownNamingPolicy.CamelCase,
    WriteIndented = false)]
public partial class AppJsonContext : JsonSerializerContext { }

// Usage
var json = JsonSerializer.Serialize(user, AppJsonContext.Default.User);
var users = JsonSerializer.Deserialize(data, AppJsonContext.Default.ListUser);
```

---

## Dependency Injection Advanced

### Keyed Services (.NET 8+)

```csharp
// Registration
builder.Services.AddKeyedScoped<IPaymentProcessor, StripeProcessor>("stripe");
builder.Services.AddKeyedScoped<IPaymentProcessor, PayPalProcessor>("paypal");
builder.Services.AddKeyedScoped<IPaymentProcessor, VNPayProcessor>("vnpay");

// Resolution via attribute
public class PaymentService(
    [FromKeyedServices("stripe")] IPaymentProcessor stripe,
    [FromKeyedServices("paypal")] IPaymentProcessor paypal)
{
    public async Task ProcessAsync(string provider, Payment payment)
    {
        var processor = provider switch
        {
            "stripe" => stripe,
            "paypal" => paypal,
            _ => throw new ArgumentException($"Unknown provider: {provider}")
        };
        await processor.ProcessAsync(payment);
    }
}
```

### Decorator Pattern with DI

```csharp
public static IServiceCollection Decorate<TInterface, TDecorator>(
    this IServiceCollection services)
    where TDecorator : TInterface
{
    var descriptor = services.SingleOrDefault(d => d.ServiceType == typeof(TInterface));
    if (descriptor is null)
        throw new InvalidOperationException($"{typeof(TInterface).Name} not registered");

    services.Remove(descriptor);
    services.Add(new ServiceDescriptor(
        typeof(TInterface),
        sp =>
        {
            var inner = descriptor.ImplementationFactory?.Invoke(sp)
                ?? ActivatorUtilities.CreateInstance(sp, descriptor.ImplementationType!);
            return ActivatorUtilities.CreateInstance<TDecorator>(sp, inner);
        },
        descriptor.Lifetime));

    return services;
}

// Usage
builder.Services.AddScoped<IUserRepository, UserRepository>();
builder.Services.Decorate<IUserRepository, CachedUserRepository>();
builder.Services.Decorate<IUserRepository, LoggingUserRepository>();
```

### Factory Pattern with DI

```csharp
public interface INotificationSenderFactory
{
    INotificationSender Create(NotificationType type);
}

public class NotificationSenderFactory(IServiceProvider sp) : INotificationSenderFactory
{
    public INotificationSender Create(NotificationType type) => type switch
    {
        NotificationType.Email => sp.GetRequiredService<EmailSender>(),
        NotificationType.Sms => sp.GetRequiredService<SmsSender>(),
        NotificationType.Push => sp.GetRequiredService<PushSender>(),
        _ => throw new ArgumentOutOfRangeException(nameof(type))
    };
}
```

---

## Performance Optimization

### Span<T> and Memory<T>

```csharp
public static class StringHelper
{
    // Zero-allocation parsing
    public static bool TryParseKeyValue(
        ReadOnlySpan<char> input,
        out ReadOnlySpan<char> key,
        out ReadOnlySpan<char> value)
    {
        var index = input.IndexOf('=');
        if (index < 0)
        {
            key = default;
            value = default;
            return false;
        }

        key = input[..index].Trim();
        value = input[(index + 1)..].Trim();
        return true;
    }
}
```

### ArrayPool for Buffer Reuse

```csharp
public async Task ProcessLargeFileAsync(string path)
{
    var buffer = ArrayPool<byte>.Shared.Rent(81920);
    try
    {
        await using var stream = File.OpenRead(path);
        int bytesRead;
        while ((bytesRead = await stream.ReadAsync(buffer)) > 0)
        {
            ProcessChunk(buffer.AsSpan(0, bytesRead));
        }
    }
    finally
    {
        ArrayPool<byte>.Shared.Return(buffer);
    }
}
```

### ObjectPool for Expensive Objects

```csharp
public class ExpensiveProcessorPool
{
    private readonly ObjectPool<ExpensiveProcessor> _pool;

    public ExpensiveProcessorPool()
    {
        var policy = new DefaultPooledObjectPolicy<ExpensiveProcessor>();
        _pool = new DefaultObjectPool<ExpensiveProcessor>(policy, maximumRetained: 10);
    }

    public async Task<Result> ProcessAsync(Input input)
    {
        var processor = _pool.Get();
        try
        {
            return await processor.ProcessAsync(input);
        }
        finally
        {
            _pool.Return(processor);
        }
    }
}
```

### StringBuilder for String Building

```csharp
public static string BuildReport(IEnumerable<Transaction> transactions)
{
    var sb = new StringBuilder(capacity: 4096);
    sb.AppendLine("Transaction Report");
    sb.AppendLine("==================");

    foreach (var tx in transactions)
    {
        sb.AppendLine($"{tx.Date:yyyy-MM-dd} | {tx.Amount:C} | {tx.Description}");
    }

    return sb.ToString();
}
```

---

## Domain-Driven Design

### Entity Base

```csharp
public abstract class Entity<TId> : IEquatable<Entity<TId>>
    where TId : notnull
{
    public TId Id { get; protected init; } = default!;

    private readonly List<IDomainEvent> _domainEvents = [];
    public IReadOnlyList<IDomainEvent> DomainEvents => _domainEvents.AsReadOnly();

    protected void AddDomainEvent(IDomainEvent domainEvent) =>
        _domainEvents.Add(domainEvent);

    public void ClearDomainEvents() => _domainEvents.Clear();

    public bool Equals(Entity<TId>? other) =>
        other is not null && Id.Equals(other.Id);

    public override bool Equals(object? obj) =>
        obj is Entity<TId> other && Equals(other);

    public override int GetHashCode() => Id.GetHashCode();
}
```

### Value Object Base

```csharp
public abstract record ValueObject
{
    protected abstract IEnumerable<object?> GetEqualityComponents();
}

public record Money(decimal Amount, string Currency) : ValueObject
{
    protected override IEnumerable<object?> GetEqualityComponents()
    {
        yield return Amount;
        yield return Currency;
    }

    public static Money operator +(Money left, Money right)
    {
        if (left.Currency != right.Currency)
            throw new InvalidOperationException("Cannot add different currencies");
        return left with { Amount = left.Amount + right.Amount };
    }
}
```

### Result Pattern

```csharp
public class Result<T>
{
    public bool IsSuccess { get; }
    public T? Value { get; }
    public Error? Error { get; }

    private Result(bool isSuccess, T? value, Error? error)
    {
        IsSuccess = isSuccess;
        Value = value;
        Error = error;
    }

    public static Result<T> Success(T value) => new(true, value, null);
    public static Result<T> Failure(Error error) => new(false, default, error);

    public TResult Match<TResult>(
        Func<T, TResult> onSuccess,
        Func<Error, TResult> onFailure) =>
        IsSuccess ? onSuccess(Value!) : onFailure(Error!);
}

public record Error(string Code, string Message);

// Usage
public async Task<Result<User>> GetUserAsync(int id)
{
    var user = await _repository.FindAsync(id);
    return user is null
        ? Result<User>.Failure(new Error("USER_NOT_FOUND", $"User {id} not found"))
        : Result<User>.Success(user);
}
```

### Aggregate Root

```csharp
public class Order : Entity<OrderId>, IAggregateRoot
{
    private readonly List<OrderItem> _items = [];
    public IReadOnlyList<OrderItem> Items => _items.AsReadOnly();

    public CustomerId CustomerId { get; private init; }
    public OrderStatus Status { get; private set; }
    public Money TotalAmount { get; private set; }

    private Order() { } // EF Core

    public static Order Create(CustomerId customerId)
    {
        var order = new Order
        {
            Id = OrderId.Create(),
            CustomerId = customerId,
            Status = OrderStatus.Draft,
            TotalAmount = Money.Zero("USD")
        };

        order.AddDomainEvent(new OrderCreatedEvent(order.Id));
        return order;
    }

    public void AddItem(ProductId productId, int quantity, Money price)
    {
        if (Status != OrderStatus.Draft)
            throw new InvalidOperationException("Cannot modify completed order");

        var item = new OrderItem(productId, quantity, price);
        _items.Add(item);
        RecalculateTotal();
    }

    public void Submit()
    {
        if (_items.Count == 0)
            throw new InvalidOperationException("Cannot submit empty order");

        Status = OrderStatus.Submitted;
        AddDomainEvent(new OrderSubmittedEvent(Id, TotalAmount));
    }

    private void RecalculateTotal()
    {
        TotalAmount = _items.Aggregate(
            Money.Zero("USD"),
            (sum, item) => sum + item.LineTotal);
    }
}
```

---

_DOMYH Awesome Code — C# Advanced Patterns — 2025-2026_
