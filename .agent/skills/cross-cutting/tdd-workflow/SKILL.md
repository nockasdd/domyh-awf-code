---
name: tdd-workflow
version: "7.0.0"
category: cross-cutting
---

# Test-Driven Development (TDD)

> 🧪 **Complete TDD methodology for production-quality code**
> **Patterns**: 180+ | **Languages**: 12 | **Categories**: 6

---

## Quick Reference

| What You Need                        | Data File                  | Patterns |
| ------------------------------------ | -------------------------- | -------- |
| Core TDD cycle (Red-Green-Refactor)  | `core-tdd-cycle.yaml`      | 35       |
| Test doubles (mock, stub, spy, fake) | `test-doubles.yaml`        | 30       |
| Coverage strategies                  | `coverage-strategies.yaml` | 25       |
| BDD/ATDD patterns (Given-When-Then)  | `bdd-atdd-patterns.yaml`   | 30       |
| Language-specific TDD patterns       | `language-patterns.yaml`   | 45       |
| TDD anti-patterns to avoid           | `anti-patterns.yaml`       | 15       |

---

## TDD Cycle

```
┌─────────────────────────────────────────────┐
│  1. RED    → Write a failing test           │
│  2. GREEN  → Write minimal code to pass     │
│  3. REFACTOR → Improve without breaking     │
│  4. REPEAT → Next requirement               │
└─────────────────────────────────────────────┘
```

### Phase Details

| Phase        | Goal                     | Rules                                                    |
| ------------ | ------------------------ | -------------------------------------------------------- |
| **RED**      | Define expected behavior | Test MUST fail first. No production code yet             |
| **GREEN**    | Make it work             | Write the SIMPLEST code that passes. No optimization     |
| **REFACTOR** | Make it clean            | Remove duplication. Improve naming. All tests still pass |

---

## Test Naming Conventions

| Pattern                                        | Example                                     |
| ---------------------------------------------- | ------------------------------------------- |
| `should_[behavior]_when_[condition]`           | `should_throw_when_email_invalid`           |
| `[method]_[scenario]_[expected]`               | `withdraw_insufficientFunds_throwsError`    |
| `given_[context]_when_[action]_then_[outcome]` | `given_empty_cart_when_checkout_then_error` |
| `it [behavior description]`                    | `it returns 404 for missing user`           |

---

## Test Structure (AAA Pattern)

```
Arrange → Set up test data, dependencies, system state
Act     → Execute the behavior under test
Assert  → Verify the expected outcome
```

---

## Test Doubles

| Type      | Purpose                     | When to Use                     |
| --------- | --------------------------- | ------------------------------- |
| **Dummy** | Fill parameter lists        | Satisfy required args, not used |
| **Stub**  | Return canned answers       | Isolate from dependencies       |
| **Spy**   | Record interactions         | Verify side-effects             |
| **Mock**  | Pre-programmed expectations | Behavior verification           |
| **Fake**  | Simplified implementation   | In-memory DB, fake API          |

---

## Coverage Strategy

| Level           | Target         | Method                |
| --------------- | -------------- | --------------------- |
| **Unit**        | 80%+           | TDD cycle             |
| **Integration** | 60%+           | API/DB boundary tests |
| **E2E**         | Critical paths | Smoke + regression    |
| **Mutation**    | 70%+           | Kill mutant score     |

---

## BDD Format

```gherkin
Feature: User Registration
  Scenario: Valid registration
    Given a new user with valid email
    When they submit the registration form
    Then account is created
    And welcome email is sent
```

---

## Language-Specific TDD

| Language       | Framework   | Runner          | Assert                          |
| -------------- | ----------- | --------------- | ------------------------------- |
| **TypeScript** | Jest/Vitest | `npx vitest`    | `expect().toBe()`               |
| **Python**     | pytest      | `pytest -v`     | `assert`, `pytest.raises`       |
| **Go**         | testing     | `go test ./...` | `t.Fatal`, testify              |
| **Rust**       | built-in    | `cargo test`    | `assert_eq!`, `#[should_panic]` |
| **Java**       | JUnit 5     | `mvn test`      | `assertEquals`, Mockito         |
| **C#**         | xUnit/NUnit | `dotnet test`   | `Assert.Equal`, Moq             |
| **C++**        | Google Test | `ctest`         | `EXPECT_EQ`, GMock              |
| **Swift**      | XCTest      | `swift test`    | `XCTAssertEqual`                |
| **Kotlin**     | JUnit 5     | `gradle test`   | MockK, kotest                   |
| **PHP**        | PHPUnit     | `phpunit`       | `$this->assertEquals()`         |
| **Ruby**       | RSpec       | `rspec`         | `expect().to eq()`              |
| **Elixir**     | ExUnit      | `mix test`      | `assert`                        |

---

## HSA Integration

Data powered by HSA BM25 search engine. Query YAML data via skill search:

| Domain        | Query Examples                       |
| ------------- | ------------------------------------ |
| TDD Cycle     | "red green refactor minimal code"    |
| Test Doubles  | "mock stub spy fake dummy"           |
| BDD           | "given when then scenario feature"   |
| Coverage      | "mutation testing kill score branch" |
| Anti-patterns | "test coupling brittle flaky slow"   |
