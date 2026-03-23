---
name: kotlin
description: "Kotlin development patterns for Android, JVM, and multiplatform. Use when working with .kt/.kts files."
detect: ["build.gradle.kts", "settings.gradle.kts", "*.kt", "*.kts"]
category: languages
tier: 1
---

# Kotlin Patterns — DOMYH Awesome Code

> Kotlin 2.0/2.1 • KMP • Compose — 2025-2026

## 🌳 Decision Tree

```
Task → What Kotlin pattern?
  ├─ Platform
  │   ├─ Android → Jetpack Compose 🏆
  │   ├─ Backend → Ktor / Spring Boot
  │   ├─ Multiplatform → KMP (shared logic)
  │   └─ Desktop → Compose Multiplatform
  ├─ Architecture (Android)
  │   ├─ UI → MVVM + Compose
  │   ├─ DI → Hilt / Koin
  │   └─ Navigation → Navigation Compose
  ├─ Concurrency
  │   ├─ Async → Coroutines + Flow
  │   └─ Structured → CoroutineScope
  └─ Testing
      ├─ Unit → JUnit 5 + MockK
      └─ UI → Compose Testing
```

---

## 🔍 Language Detection

```yaml
kotlin_indicators:  # Kotlin skill activates
  - "build.gradle.kts, settings.gradle.kts"
  - "*.kt, *.kts files"
  - "fun main(), fun keyword"
  - "data class, sealed class"
  - "val, var declarations"
  - "import kotlinx.*, androidx.*"
  - "@Composable, @Serializable"

not_kotlin:  # Similar languages
  - "build.gradle (Groovy)" → Java/Groovy
  - "*.java, public class" → Java
  - "*.swift, SwiftUI" → Swift
  - "pubspec.yaml" → Flutter/Dart
```

---

## 📊 Kotlin Versions (2025-2026)

| Version        | Release | Key Features                     |
| -------------- | ------- | -------------------------------- |
| **Kotlin 2.0** | 2024-05 | K2 compiler stable, Enum.entries |
| **Kotlin 2.1** | 2024-11 | Compiler improvements, bug fixes |
| **Kotlin 2.2** | 2025-H1 | ~40% faster compilation          |
| **KMP Stable** | 2024-05 | Production-ready multiplatform   |

### K2 Compiler Benefits

```kotlin
// ✅ K2 compiler is now default (2x faster)
// build.gradle.kts
kotlin {
    compilerOptions {
        // K2 is now stable and default
        freeCompilerArgs.add("-opt-in=kotlin.ExperimentalStdlibApi")
    }
}

// ✅ Enum.entries replaces Enum.values()
enum class Color { RED, GREEN, BLUE }

// ❌ OLD: Color.values() - creates new array each time
// ✅ NEW: Color.entries - returns immutable list
Color.entries.forEach { println(it) }
```

---

## 🛠️ IDE & Toolchain

> See `data/core.yaml` for IDE comparison details (IntelliJ, Android Studio, Fleet/VS Code).

**Recommended**: IntelliJ IDEA (server/desktop) · Android Studio (mobile) · Both support K2 compiler + KMP

---

## 📦 Kotlin Ecosystem

> See `data/android.yaml` for full Jetpack library catalog and `data/core.yaml` for networking/testing.

**Android Jetpack**: Compose 1.7+ · Room 2.6+ · Hilt 2.51+ · Navigation 2.8+
**Networking**: Ktor Client · kotlinx.serialization
**Async**: Coroutines + Flow + StateFlow
**Testing**: JUnit 5 · MockK · Turbine · Kotest

---

## 🌍 Kotlin Multiplatform (KMP)

### Project Structure

```
shared/
├── src/
│   ├── commonMain/       # Shared code
│   │   └── kotlin/
│   │       ├── data/
│   │       ├── domain/
│   │       └── presentation/
│   ├── androidMain/      # Android-specific
│   │   └── kotlin/
│   ├── iosMain/          # iOS-specific
│   │   └── kotlin/
│   ├── commonTest/       # Shared tests
│   ├── androidUnitTest/
│   └── iosTest/
└── build.gradle.kts

composeApp/               # Compose Multiplatform UI
├── src/
│   ├── commonMain/
│   ├── androidMain/
│   ├── iosMain/
│   └── desktopMain/
└── build.gradle.kts

androidApp/               # Android entry point
iosApp/                   # iOS entry point (Swift)
```

### expect/actual Mechanism

```kotlin
// commonMain - Expect declaration
expect class PlatformContext

expect fun getPlatformName(): String

expect suspend fun getDeviceId(context: PlatformContext): String

// androidMain - Actual implementation
actual class PlatformContext(val context: Context)

actual fun getPlatformName(): String = "Android ${Build.VERSION.SDK_INT}"

actual suspend fun getDeviceId(context: PlatformContext): String {
    return Settings.Secure.getString(
        context.context.contentResolver,
        Settings.Secure.ANDROID_ID
    )
}

// iosMain - Actual implementation
actual class PlatformContext  // No-op on iOS

actual fun getPlatformName(): String = "iOS ${UIDevice.currentDevice.systemVersion}"

actual suspend fun getDeviceId(context: PlatformContext): String {
    return UIDevice.currentDevice.identifierForVendor?.UUIDString ?: ""
}
```

### Compose Multiplatform

```kotlin
// commonMain - Shared UI
@Composable
fun App() {
    MaterialTheme {
        var count by remember { mutableStateOf(0) }

        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            Text("Count: $count")
            Button(onClick = { count++ }) {
                Text("Increment")
            }
        }
    }
}

// build.gradle.kts
kotlin {
    androidTarget()
    iosX64()
    iosArm64()
    iosSimulatorArm64()

    sourceSets {
        commonMain.dependencies {
            implementation(compose.runtime)
            implementation(compose.foundation)
            implementation(compose.material3)
        }
    }
}
```

---

## 🎨 Jetpack Compose Best Practices

### Performance Optimization

```kotlin
// ✅ Use remember for expensive calculations
@Composable
fun ExpensiveList(items: List<Item>) {
    val sortedItems = remember(items) {
        items.sortedBy { it.name }  // Only recalculated when items changes
    }

    LazyColumn {
        items(sortedItems, key = { it.id }) { item ->
            ItemRow(item)
        }
    }
}

// ✅ derivedStateOf to reduce recompositions
@Composable
fun SearchResults(items: List<Item>, query: String) {
    val filteredItems by remember(items) {
        derivedStateOf {
            if (query.isEmpty()) items
            else items.filter { it.name.contains(query, ignoreCase = true) }
        }
    }

    LazyColumn {
        items(filteredItems) { item -> ItemRow(item) }
    }
}

// ✅ Use Stable/Immutable types
@Immutable
data class User(
    val id: String,
    val name: String,
    val email: String
)

// ✅ State hoisting pattern
@Composable
fun UserCard(
    user: User,
    onEditClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    Card(modifier = modifier) {
        Text(user.name)
        Button(onClick = onEditClick) { Text("Edit") }
    }
}

// ✅ collectAsStateWithLifecycle for production
@Composable
fun UserScreen(viewModel: UserViewModel) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    when (val state = uiState) {
        is UiState.Loading -> LoadingIndicator()
        is UiState.Success -> UserContent(state.user)
        is UiState.Error -> ErrorMessage(state.message)
    }
}
```

### Composable Previews

```kotlin
@Preview(showBackground = true)
@Preview(showBackground = true, uiMode = UI_MODE_NIGHT_YES)
@Composable
fun UserCardPreview() {
    MaterialTheme {
        UserCard(
            user = User("1", "Alice", "alice@example.com"),
            onEditClick = {}
        )
    }
}
```

---

## 🔒 Null Safety

```kotlin
// ✅ Prefer non-nullable types
val name: String = "Alice"  // Cannot be null

// ✅ Use nullable when necessary
val middleName: String? = null

// ✅ Safe call operator ?.
val length = middleName?.length  // Returns Int?

// ✅ Elvis operator ?: for defaults
val length = middleName?.length ?: 0

// ✅ let for null checks
middleName?.let { name ->
    println("Middle name: $name")
}

// ❌ AVOID: !! not-null assertion (can throw NPE)
val length = middleName!!.length  // Dangerous!

// ✅ Use require/check for validation
fun createUser(email: String): User {
    require(email.contains("@")) { "Invalid email" }
    return User(email)
}
```

---

## ⚡ Coroutines Best Practices

```kotlin
// ✅ Structured concurrency with viewModelScope
class UserViewModel : ViewModel() {
    private val _uiState = MutableStateFlow<UiState>(UiState.Loading)
    val uiState: StateFlow<UiState> = _uiState.asStateFlow()

    fun loadUser(id: String) {
        viewModelScope.launch {
            _uiState.value = UiState.Loading
            try {
                val user = repository.fetchUser(id)
                _uiState.value = UiState.Success(user)
            } catch (e: Exception) {
                _uiState.value = UiState.Error(e.message ?: "Unknown error")
            }
        }
    }
}

// ✅ Parallel execution with async
suspend fun loadUserData(id: String): UserData {
    return coroutineScope {
        val userDeferred = async { fetchUser(id) }
        val ordersDeferred = async { fetchOrders(id) }

        UserData(
            user = userDeferred.await(),
            orders = ordersDeferred.await()
        )
    }
}

// ✅ Error handling with Result type
sealed class Result<out T> {
    data class Success<T>(val data: T) : Result<T>()
    data class Failure(val error: Throwable) : Result<Nothing>()
}

suspend fun <T> safeCall(block: suspend () -> T): Result<T> {
    return try {
        Result.Success(block())
    } catch (e: Exception) {
        Result.Failure(e)
    }
}

// ✅ Flow with flowWithLifecycle
repository.users
    .flowWithLifecycle(lifecycle, Lifecycle.State.STARTED)
    .collect { users -> updateUI(users) }
```

---

## 🎨 Naming Conventions

| Element             | Convention    | Example                 |
| ------------------- | ------------- | ----------------------- |
| Classes             | PascalCase    | `UserRepository`        |
| Interfaces          | PascalCase    | `UserService`           |
| Functions           | camelCase     | `getUserById()`         |
| Properties          | camelCase     | `userName`              |
| Constants           | UPPER_SNAKE   | `MAX_RETRY_COUNT`       |
| Backing properties  | \_camelCase   | `_uiState`              |
| Extension functions | camelCase     | `String.isValidEmail()` |
| Type parameters     | Single letter | `T`, `K`, `V`           |
| Packages            | lowercase     | `com.example.user`      |

---

## 📂 Project Structure (Clean Architecture)

```
app/
├── data/
│   ├── local/
│   │   ├── dao/
│   │   └── entity/
│   ├── remote/
│   │   ├── api/
│   │   └── dto/
│   └── repository/
├── domain/
│   ├── model/
│   ├── repository/
│   └── usecase/
├── presentation/
│   ├── navigation/
│   ├── theme/
│   └── screens/
│       └── home/
│           ├── HomeScreen.kt
│           ├── HomeViewModel.kt
│           └── components/
└── di/
    └── AppModule.kt
```

---

## ✅ Production Checklist

### Code Quality

- [ ] Null safety enforced (no !! operator)
- [ ] val preferred over var
- [ ] data class for models
- [ ] sealed class for state/events

### Coroutines

- [ ] viewModelScope used
- [ ] Proper exception handling
- [ ] Flow with lifecycle awareness

### Compose

- [ ] remember for expensive operations
- [ ] Keys in LazyColumn/LazyRow
- [ ] Stable/Immutable data classes
- [ ] Previews for components

### KMP (if applicable)

- [ ] expect/actual properly implemented
- [ ] Platform-specific code isolated
- [ ] Common tests passing

### DI

- [ ] Hilt configured
- [ ] Proper scoping (@Singleton, @ViewModelScoped)

---
