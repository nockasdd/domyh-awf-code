---
name: flutter
detect: ["pubspec.yaml", "*.dart", "lib/main.dart", "analysis_options.yaml"]
version: "6.4.5"
category: mobile
tier: 1
---

# Flutter/Dart Patterns — DOMYH Awesome Code

> Flutter 3.29+ & Dart 3.7 — 2025-2026

## 🔍 Language Detection

```yaml
flutter_indicators:  # Flutter/Dart skill activates
  - "pubspec.yaml"
  - "*.dart files"
  - "lib/main.dart"
  - "import 'package:flutter/"
  - "StatelessWidget, StatefulWidget"
  - "MaterialApp, Scaffold"
  - "Riverpod, BLoC, Provider"

not_flutter:  # Other frameworks
  - "package.json, *.tsx" → React Native
  - "build.gradle.kts, @Composable" → Kotlin/Android
  - "*.swift, SwiftUI" → iOS Native
```

---

## 📊 Flutter & Dart Versions (2025-2026)

| Version          | Release | Key Features                           |
| ---------------- | ------- | -------------------------------------- |
| **Dart 3.6**     | 2024-12 | Pub workspaces, improved analyzer      |
| **Dart 3.7**     | 2025-Q1 | Wildcard variables, improved formatter |
| **Flutter 3.27** | 2024-12 | Material 3 default, Impeller stable    |
| **Flutter 3.29** | 2025-Q1 | Impeller iOS default, main thread Dart |

### Dart 3.7 Features

```dart
// ✅ Digit separators (readability)
const billion = 1_000_000_000;
const hex = 0xFF_EC_DE_5D;

// ✅ Wildcard variables - elegant callback handling
future.then((_) => print('Done!')); // Underscore as wildcard

// ✅ Improved formatter - auto trailing commas
// Formatter now adds/removes trailing commas based on line length
```

### Flutter 3.29 New Features

```dart
// ✅ Impeller is now DEFAULT on iOS (Skia removed)
// No configuration needed - automatic performance boost

// ✅ Main Thread Dart Execution (Android/iOS)
// Eliminates separate UI thread - better platform interop
// Allows synchronous calls to/from native platform

// ✅ BackdropGroup for optimized blur effects
import 'package:flutter/widgets.dart';

BackdropGroup(
  children: [
    BackdropFilter.grouped(
      filter: ImageFilter.blur(sigmaX: 10, sigmaY: 10),
      child: Container(color: Colors.white.withOpacity(0.5)),
    ),
    BackdropFilter.grouped(
      filter: ImageFilter.blur(sigmaX: 5, sigmaY: 5),
      child: Container(color: Colors.blue.withOpacity(0.3)),
    ),
  ],
)

// ✅ ImageFilter.shader - Custom shaders on child widgets
ImageFilter.shader(
  fragmentShader: myFragmentShader,
  child: Image.asset('assets/photo.png'),
)
```

### Material 3 Updates (3.29)

```dart
// ✅ FadeForwardsPageTransitionsBuilder - new default transition
MaterialApp(
  theme: ThemeData(
    pageTransitionsTheme: PageTransitionsTheme(
      builders: {
        TargetPlatform.android: FadeForwardsPageTransitionsBuilder(),
        TargetPlatform.iOS: CupertinoPageTransitionsBuilder(),
      },
    ),
  ),
)
```

---

## 🛠️ IDE & Toolchain Support

### VS Code (Recommended)

```yaml
extensions_required:
  - "Dart" (dart-code.dart-code)
  - "Flutter" (dart-code.flutter)
optional:
  - "Flutter Widget Snippets"
  - "Awesome Flutter Snippets"
  - "Dart Data Class Generator"
features:
  - Hot Reload (ctrl+s)
  - Widget Inspector
  - Dart DevTools integration
  - Debugging with breakpoints
  - Code formatting (dart format)
notes:
  - Lightweight, fast startup
  - Cross-platform (Windows, macOS, Linux)
  - Best for most developers
```

### Android Studio / IntelliJ IDEA

```yaml
plugins_required:
  - "Flutter" plugin
  - "Dart" plugin
features:
  - Full IDE features
  - Integrated emulator
  - Flutter Inspector
  - Performance profiler
  - Built-in device manager
notes:
  - Heavier resource usage
  - Better for Android-focused development
  - Excellent refactoring tools
```

---

## 📦 State Management (2025)

### Comparison

| Solution         | Use Case     | Complexity | Performance |
| ---------------- | ------------ | ---------- | ----------- |
| **Riverpod 3.0** | Most apps 🏆 | Medium     | Excellent   |
| **BLoC/Cubit**   | Enterprise   | High       | Excellent   |
| **Provider**     | Simple apps  | Low        | Good        |
| **GetX**         | Rapid dev    | Low        | Good        |

### Riverpod 3.0 Best Practices

```dart
import 'package:riverpod/riverpod.dart';

// ✅ FutureProvider for async data
final userProvider = FutureProvider.autoDispose<User>((ref) async {
  final api = ref.watch(apiClientProvider);
  return api.fetchUser();
});

// ✅ Notifier for complex state
class CounterNotifier extends Notifier<int> {
  @override
  int build() => 0;  // Initial state

  void increment() => state++;
  void decrement() => state--;
}

final counterProvider = NotifierProvider<CounterNotifier, int>(
  CounterNotifier.new,
);

// ✅ In widgets: use watch() in build, read() in callbacks
class CounterWidget extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final count = ref.watch(counterProvider);  // ✅ watch in build

    return Column(
      children: [
        Text('Count: $count'),
        ElevatedButton(
          onPressed: () => ref.read(counterProvider.notifier).increment(),  // ✅ read in callback
          child: Text('Increment'),
        ),
      ],
    );
  }
}

// ✅ Use ref.select() to reduce rebuilds
final userName = ref.watch(userProvider.select((u) => u.name));
```

### BLoC Pattern Best Practices

```dart
import 'package:flutter_bloc/flutter_bloc.dart';

// ✅ Events
sealed class AuthEvent {}
class LoginRequested extends AuthEvent {
  final String email;
  final String password;
  LoginRequested(this.email, this.password);
}
class LogoutRequested extends AuthEvent {}

// ✅ States
sealed class AuthState {}
class AuthInitial extends AuthState {}
class AuthLoading extends AuthState {}
class AuthAuthenticated extends AuthState {
  final User user;
  AuthAuthenticated(this.user);
}
class AuthError extends AuthState {
  final String message;
  AuthError(this.message);
}

// ✅ BLoC
class AuthBloc extends Bloc<AuthEvent, AuthState> {
  final AuthRepository _repository;

  AuthBloc(this._repository) : super(AuthInitial()) {
    on<LoginRequested>(_onLoginRequested);
    on<LogoutRequested>(_onLogoutRequested);
  }

  Future<void> _onLoginRequested(
    LoginRequested event,
    Emitter<AuthState> emit,
  ) async {
    emit(AuthLoading());
    try {
      final user = await _repository.login(event.email, event.password);
      emit(AuthAuthenticated(user));
    } catch (e) {
      emit(AuthError(e.toString()));
    }
  }

  Future<void> _onLogoutRequested(
    LogoutRequested event,
    Emitter<AuthState> emit,
  ) async {
    await _repository.logout();
    emit(AuthInitial());
  }
}

// ✅ Use BlocBuilder efficiently
BlocBuilder<AuthBloc, AuthState>(
  buildWhen: (previous, current) => current is! AuthLoading,  // Optimize rebuilds
  builder: (context, state) {
    return switch (state) {
      AuthInitial() => LoginScreen(),
      AuthLoading() => LoadingIndicator(),
      AuthAuthenticated(user: final u) => HomeScreen(user: u),
      AuthError(message: final m) => ErrorScreen(message: m),
    };
  },
)
```

---

## 📦 Essential Packages (2025)

### Networking & Data

| Package               | Version | Use Case                      |
| --------------------- | ------- | ----------------------------- |
| **dio**               | 5.x     | HTTP client with interceptors |
| **retrofit**          | 4.x     | Type-safe REST client         |
| **freezed**           | 2.x     | Immutable data classes        |
| **json_serializable** | 6.x     | JSON parsing                  |
| **isar**              | 3.x     | Local NoSQL database          |
| **drift**             | 2.x     | Local SQL database            |

### UI & Design

| Package                  | Use Case             |
| ------------------------ | -------------------- |
| **flutter_hooks**        | React-style hooks    |
| **auto_route**           | Type-safe navigation |
| **go_router**            | Official navigation  |
| **flutter_screenutil**   | Responsive sizing    |
| **cached_network_image** | Image caching        |
| **shimmer**              | Loading effects      |

### Code Generation

```yaml
# pubspec.yaml
dev_dependencies:
  build_runner: ^2.4.0
  freezed: ^2.5.0
  json_serializable: ^6.8.0
  retrofit_generator: ^8.0.0
```

```bash
# Run code generation
dart run build_runner build --delete-conflicting-outputs
```

---

## ✨ Dart 3 Language Features

### Sealed Classes & Pattern Matching

```dart
// ✅ Sealed class for exhaustive pattern matching
sealed class Result<T> {
  const Result();
}

class Success<T> extends Result<T> {
  final T value;
  const Success(this.value);
}

class Failure<T> extends Result<T> {
  final Exception error;
  const Failure(this.error);
}

// ✅ Pattern matching in switch
String handleResult(Result<User> result) {
  return switch (result) {
    Success(value: final user) => 'Hello, ${user.name}!',
    Failure(error: final e) => 'Error: ${e.toString()}',
  };
}

// ✅ if-case pattern matching
if (result case Success(value: final user)) {
  print('User: ${user.name}');
}
```

### Records & Destructuring

```dart
// ✅ Records (anonymous tuples)
(String, int) getUserInfo() => ('Alice', 25);

final (name, age) = getUserInfo();
print('$name is $age years old');

// ✅ Named fields in records
({String name, int age}) getUser() => (name: 'Alice', age: 25);

final (:name, :age) = getUser();
```

### Freezed for Immutable Models

```dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'user.freezed.dart';
part 'user.g.dart';

// ✅ Immutable data class with freezed
@freezed
class User with _$User {
  const factory User({
    required String id,
    required String email,
    required String name,
    @Default(false) bool isActive,
    DateTime? lastLoginAt,
  }) = _User;

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
}

// Usage
final user = User(id: '1', email: 'a@b.com', name: 'Alice');
final updated = user.copyWith(isActive: true);  // Immutable update
```

---

## 📂 Project Structure (Feature-First)

```
lib/
├── main.dart
├── app/
│   ├── app.dart                    # MaterialApp setup
│   └── router.dart                 # Navigation
├── core/
│   ├── constants/
│   │   ├── colors.dart
│   │   └── strings.dart
│   ├── network/
│   │   ├── api_client.dart
│   │   └── interceptors.dart
│   ├── theme/
│   │   └── app_theme.dart
│   └── utils/
│       └── extensions.dart
├── features/
│   ├── auth/
│   │   ├── data/
│   │   │   ├── datasources/
│   │   │   ├── models/
│   │   │   └── repositories/
│   │   ├── domain/
│   │   │   ├── entities/
│   │   │   └── usecases/
│   │   └── presentation/
│   │       ├── pages/
│   │       ├── widgets/
│   │       └── providers/
│   └── home/
│       └── ...
└── shared/
    └── widgets/
        ├── buttons/
        └── loading/
```

---

## ⚡ Performance Optimization

### Reduce Rebuilds

```dart
// ✅ Use const constructors
const SizedBox(height: 16);
const Text('Hello');

// ✅ Extract widgets to avoid rebuilds
class UserList extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      itemCount: users.length,
      itemBuilder: (context, index) => UserListItem(user: users[index]),
    );
  }
}

// ✅ Use keys for list items
ListView.builder(
  itemBuilder: (context, index) => UserCard(
    key: ValueKey(users[index].id),  // Important!
    user: users[index],
  ),
)

// ✅ RepaintBoundary for complex widgets
RepaintBoundary(
  child: ComplexAnimatedWidget(),
)
```

### Heavy Computation in Isolates

```dart
import 'dart:isolate';

// ✅ Offload CPU-heavy work to isolate
Future<List<ProcessedItem>> processDataInIsolate(List<RawItem> items) async {
  return await Isolate.run(() {
    return items.map((item) => processItem(item)).toList();
  });
}
```

---

## 🎨 Naming Conventions (Effective Dart)

| Element    | Convention           | Example                    |
| ---------- | -------------------- | -------------------------- |
| Classes    | PascalCase           | `UserProfileScreen`        |
| Extensions | PascalCase           | `StringExtensions`         |
| Functions  | camelCase            | `getUserData()`            |
| Variables  | camelCase            | `userName`, `isLoading`    |
| Constants  | camelCase            | `defaultTimeout`           |
| Private    | \_camelCase          | `_internalState`           |
| Files      | snake_case           | `user_profile_screen.dart` |
| Packages   | snake_case           | `my_awesome_package`       |
| Enums      | PascalCase.camelCase | `LoadingState.loading`     |
| Libraries  | snake_case           | `library user_utils;`      |

---

## ✅ Production Checklist

### Code Quality

- [ ] `dart format` applied
- [ ] `dart analyze` clean (no warnings)
- [ ] Const constructors used where possible
- [ ] Keys added to list items
- [ ] dispose() implemented for controllers

### State Management

- [ ] Riverpod/BLoC properly configured
- [ ] No setState in large widgets
- [ ] State properly disposed

### Performance

- [ ] RepaintBoundary for complex widgets
- [ ] Isolates for heavy computation
- [ ] Images optimized and cached
- [ ] LazyLoading for large lists

### Testing

- [ ] Unit tests for business logic
- [ ] Widget tests for UI
- [ ] Integration tests for flows

---

_DOMYH Awesome Code • Flutter 3.29+ / Dart 3.7+ • Impeller Default_
