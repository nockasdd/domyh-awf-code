---
name: fsharp
detect: ["*.fs", "*.fsx", "*.fsproj"]
version: "6.0.0"
category: functional
tier: 3
---

# F# Patterns — DOMYH Awesome Code v5.3

> **Version**: F# 8+ (.NET 8)
> **Framework**: Giraffe, Saturn, Fable
> **Philosophy**: Functional-first, type-safe, .NET ecosystem

---

## 🎯 When to Use

Use for: Data processing, .NET APIs, type-safe systems.
**NOT for**: Pure OOP projects (→ C#).

---

## 🔧 Project Setup

```bash
dotnet new console -lang F# -o MyApp
cd MyApp
dotnet add package Giraffe
dotnet run
```

---

## 🔄 Core Patterns

### Discriminated Unions

```fsharp
type Result<'T, 'E> =
    | Ok of 'T
    | Error of 'E

type UserError =
    | NotFound of int
    | ValidationError of string
    | Unauthorized

let findUser id : Result<User, UserError> =
    match Database.find id with
    | Some user -> Ok user
    | None -> Error (NotFound id)

// Pattern matching
match findUser 123 with
| Ok user -> printfn "Found: %s" user.Name
| Error (NotFound id) -> printfn "User %d not found" id
| Error (ValidationError msg) -> printfn "Invalid: %s" msg
| Error Unauthorized -> printfn "Access denied"
```

### Railway-Oriented Programming

```fsharp
let (>>=) result f =
    match result with
    | Ok x -> f x
    | Error e -> Error e

let validateEmail email =
    if email.Contains("@") then Ok email
    else Error "Invalid email"

let validateName name =
    if String.length name >= 2 then Ok name
    else Error "Name too short"

let createUser name email =
    validateName name >>= fun validName ->
    validateEmail email >>= fun validEmail ->
    Ok { Name = validName; Email = validEmail }
```

### HTTP with Giraffe

```fsharp
open Giraffe

let webApp =
    choose [
        GET >=> route "/" >=> text "Hello World"
        GET >=> routef "/users/%i" (fun id ->
            json { Id = id; Name = "User" })
        POST >=> route "/users" >=> bindJson<CreateUser> (fun dto ->
            json { Success = true })
    ]

let configureApp (app : IApplicationBuilder) =
    app.UseGiraffe(webApp)
```

---

## ✅ Production Checklist

- [ ] `dotnet build` passing
- [ ] Tests with `Expecto` or `xUnit`
- [ ] `fantomas` formatting
- [ ] Type annotations on public API

---

_DOMYH Awesome Code v6.0.0 • F# 8+_
