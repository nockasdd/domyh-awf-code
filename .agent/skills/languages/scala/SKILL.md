---
name: scala
detect: ["*.scala", "*.sc", "build.sbt", "project/*.scala"]
version: "6.2.1"
category: functional
tier: 2
---

# Scala 3 Patterns — DOMYH Awesome Code

> **Version**: Scala 3.4+ (2025-2026)
> **Frameworks**: ZIO 2, Cats Effect 3, Akka
> **Philosophy**: Functional-first, type-safe, JVM power

---

## 🎯 When to Use This Skill

Use for: Data pipelines, distributed systems, type-safe APIs.
**NOT for**: Simple scripts (→ python), frontend (→ typescript).

---

## 📦 Recommended Stack

| Library    | Use Case         | Add to build.sbt                        |
| ---------- | ---------------- | --------------------------------------- |
| **ZIO 2**  | Effect system 🏆 | `"dev.zio" %% "zio" % "2.0"`            |
| **http4s** | HTTP server      | `"org.http4s" %% "http4s-ember-server"` |
| **Circe**  | JSON             | `"io.circe" %% "circe-generic"`         |
| **Doobie** | Database         | `"org.tpolecat" %% "doobie-core"`       |

---

## 🔄 Scala 3 Essentials

### Enums and ADTs

```scala
// ✅ Enum (Scala 3)
enum Status:
  case Active, Inactive, Pending

// ✅ ADT with data
enum Result[+E, +A]:
  case Success(value: A)
  case Failure(error: E)

// ✅ Pattern matching
def handle[E, A](result: Result[E, A]): String = result match
  case Result.Success(value) => s"Got: $value"
  case Result.Failure(error) => s"Error: $error"
```

### Extension Methods

```scala
extension (s: String)
  def toSlug: String =
    s.toLowerCase.replaceAll("\\s+", "-")

  def truncate(maxLen: Int): String =
    if s.length <= maxLen then s else s.take(maxLen) + "..."

// Usage
"Hello World".toSlug      // "hello-world"
"Long text here".truncate(8)  // "Long tex..."
```

### Given/Using (Context Parameters)

```scala
// ✅ Define given instance
trait JsonEncoder[A]:
  def encode(a: A): String

given JsonEncoder[Int] with
  def encode(a: Int): String = a.toString

given JsonEncoder[String] with
  def encode(a: String): String = s"\"$a\""

// ✅ Use with using clause
def toJson[A](value: A)(using encoder: JsonEncoder[A]): String =
  encoder.encode(value)

// Auto-derived
toJson(42)        // "42"
toJson("hello")   // "\"hello\""
```

---

## ⚡ ZIO Patterns

```scala
import zio.*

// ✅ Effect composition
def program: ZIO[Any, Throwable, Unit] = for
  _    <- Console.printLine("Enter name:")
  name <- Console.readLine
  _    <- Console.printLine(s"Hello, $name!")
yield ()

// ✅ Error handling
def divide(a: Int, b: Int): ZIO[Any, String, Int] =
  if b == 0 then ZIO.fail("Division by zero")
  else ZIO.succeed(a / b)

// ✅ Resource management
def withFile[A](path: String)(use: BufferedReader => Task[A]): Task[A] =
  ZIO.acquireReleaseWith(
    ZIO.attempt(new BufferedReader(new FileReader(path)))
  )(reader => ZIO.succeed(reader.close()))(use)

// ✅ Parallel execution
def fetchAll: ZIO[Any, Throwable, (User, Posts, Comments)] =
  (fetchUser <&> fetchPosts <&> fetchComments)

// Run
object Main extends ZIOAppDefault:
  def run = program
```

---

## 🌐 HTTP4s Server

```scala
import org.http4s.*
import org.http4s.dsl.io.*
import org.http4s.ember.server.EmberServerBuilder
import cats.effect.{IO, IOApp}

object Main extends IOApp.Simple:
  val routes = HttpRoutes.of[IO] {
    case GET -> Root / "users" =>
      Ok("""{"users": []}""")

    case GET -> Root / "users" / IntVar(id) =>
      Ok(s"""{"id": $id}""")

    case req @ POST -> Root / "users" =>
      for
        body   <- req.as[String]
        result <- Ok(s"Created: $body")
      yield result
  }

  val app = routes.orNotFound

  def run: IO[Unit] =
    EmberServerBuilder
      .default[IO]
      .withHost(host"0.0.0.0")
      .withPort(port"8080")
      .withHttpApp(app)
      .build
      .useForever
```

---

## 🗃️ Database with Doobie

```scala
import doobie.*
import doobie.implicits.*
import cats.effect.IO

case class User(id: Long, name: String, email: String)

object UserRepo:
  def findById(id: Long): ConnectionIO[Option[User]] =
    sql"SELECT id, name, email FROM users WHERE id = $id"
      .query[User]
      .option

  def create(name: String, email: String): ConnectionIO[Long] =
    sql"INSERT INTO users (name, email) VALUES ($name, $email)"
      .update
      .withUniqueGeneratedKeys[Long]("id")

  def all: ConnectionIO[List[User]] =
    sql"SELECT id, name, email FROM users"
      .query[User]
      .to[List]
```

---

## ✅ Production Checklist

- [ ] Scala 3 syntax used
- [ ] Effects are explicit (ZIO/Cats)
- [ ] Tests with ZIO Test or MUnit
- [ ] Scalafmt formatting

---

_DOMYH Awesome Code • Scala 3.4+_
