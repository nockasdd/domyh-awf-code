# Flutter/Dart — Advanced Patterns

> DOMYH Awesome Code v6.1.2 — Tier 3 Reference

## Table of Contents

- [Advanced Riverpod Patterns](#advanced-riverpod-patterns)
- [BLoC Advanced Patterns](#bloc-advanced-patterns)
- [Performance Deep Dive](#performance-deep-dive)
- [Testing Patterns](#testing-patterns)
- [Architecture Patterns](#architecture-patterns)

---

## Advanced Riverpod Patterns

### AsyncNotifier with Caching

```dart
import 'package:riverpod/riverpod.dart';

// ✅ AsyncNotifier with cache invalidation
class UsersNotifier extends AsyncNotifier<List<User>> {
  @override
  Future<List<User>> build() async {
    // Auto-refresh every 5 minutes
    final timer = Timer.periodic(Duration(minutes: 5), (_) => refresh());
    ref.onDispose(() => timer.cancel());

    return _fetchUsers();
  }

  Future<List<User>> _fetchUsers() async {
    final api = ref.read(apiClientProvider);
    return api.fetchUsers();
  }

  Future<void> refresh() async {
    state = const AsyncLoading();
    state = await AsyncValue.guard(_fetchUsers);
  }

  Future<void> addUser(User user) async {
    final previousState = state;

    // Optimistic update
    state = AsyncData([...state.value ?? [], user]);

    try {
      await ref.read(apiClientProvider).createUser(user);
    } catch (e) {
      state = previousState;  // Rollback on error
      rethrow;
    }
  }
}

final usersProvider = AsyncNotifierProvider<UsersNotifier, List<User>>(
  UsersNotifier.new,
);

// ✅ Family providers with cache
final userDetailProvider = FutureProvider.autoDispose.family<User, String>(
  (ref, userId) async {
    // Keep alive for 30 seconds after last listener
    final link = ref.keepAlive();
    Timer(Duration(seconds: 30), link.close);

    return ref.read(apiClientProvider).fetchUser(userId);
  },
);
```

### Dependency Injection with Riverpod

```dart
// ✅ Abstract repository with implementation override
abstract class UserRepository {
  Future<List<User>> getUsers();
  Future<User> getUser(String id);
}

class UserRepositoryImpl implements UserRepository {
  final ApiClient _api;

  UserRepositoryImpl(this._api);

  @override
  Future<List<User>> getUsers() => _api.fetchUsers();

  @override
  Future<User> getUser(String id) => _api.fetchUser(id);
}

final userRepositoryProvider = Provider<UserRepository>((ref) {
  return UserRepositoryImpl(ref.read(apiClientProvider));
});

// ✅ Override in tests
void main() {
  testWidgets('shows users', (tester) async {
    await tester.pumpWidget(
      ProviderScope(
        overrides: [
          userRepositoryProvider.overrideWithValue(MockUserRepository()),
        ],
        child: MyApp(),
      ),
    );
  });
}
```

---

## BLoC Advanced Patterns

### Multi-BLoC Communication

```dart
// ✅ BLoC-to-BLoC communication via stream subscription
class OrderBloc extends Bloc<OrderEvent, OrderState> {
  final AuthBloc _authBloc;
  late StreamSubscription<AuthState> _authSubscription;

  OrderBloc(this._authBloc) : super(OrderInitial()) {
    _authSubscription = _authBloc.stream.listen((authState) {
      if (authState is AuthUnauthenticated) {
        add(ClearOrdersEvent());
      }
    });

    on<LoadOrdersEvent>(_onLoadOrders);
    on<ClearOrdersEvent>(_onClearOrders);
  }

  Future<void> _onLoadOrders(
    LoadOrdersEvent event,
    Emitter<OrderState> emit,
  ) async {
    final authState = _authBloc.state;
    if (authState is! AuthAuthenticated) {
      emit(OrderError('Not authenticated'));
      return;
    }

    emit(OrderLoading());
    try {
      final orders = await repository.fetchOrders(authState.user.id);
      emit(OrderLoaded(orders));
    } catch (e) {
      emit(OrderError(e.toString()));
    }
  }

  @override
  Future<void> close() {
    _authSubscription.cancel();
    return super.close();
  }
}
```

### Transformers for Debounce/Throttle

```dart
import 'package:bloc_concurrency/bloc_concurrency.dart';

class SearchBloc extends Bloc<SearchEvent, SearchState> {
  SearchBloc() : super(SearchInitial()) {
    on<SearchQueryChanged>(
      _onSearchQueryChanged,
      transformer: debounce(Duration(milliseconds: 300)),  // Debounce
    );

    on<LoadMoreResults>(
      _onLoadMoreResults,
      transformer: droppable(),  // Drop if already processing
    );
  }

  EventTransformer<T> debounce<T>(Duration duration) {
    return (events, mapper) {
      return events.debounceTime(duration).asyncExpand(mapper);
    };
  }
}
```

---

## Performance Deep Dive

### Widget Tree Optimization

```dart
// ✅ Break large widgets into smaller const widgets
class OptimizedList extends StatelessWidget {
  const OptimizedList({super.key, required this.items});
  final List<Item> items;

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      itemCount: items.length,
      itemBuilder: (context, index) => _OptimizedListItem(
        key: ValueKey(items[index].id),
        item: items[index],
      ),
    );
  }
}

// Separate stateless widget with const constructor
class _OptimizedListItem extends StatelessWidget {
  const _OptimizedListItem({super.key, required this.item});
  final Item item;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(8.0),  // const!
      child: Row(
        children: [
          const Icon(Icons.item),  // const!
          const SizedBox(width: 8),  // const!
          Text(item.name),
        ],
      ),
    );
  }
}
```

### Isolates for Heavy Computation

```dart
import 'dart:isolate';

// ✅ Parse large JSON in isolate
class DataProcessor {
  static Future<List<User>> parseUsersJson(String json) async {
    return await Isolate.run(() {
      final List<dynamic> decoded = jsonDecode(json);
      return decoded.map((e) => User.fromJson(e)).toList();
    });
  }

  // ✅ Complex computation with progress reporting
  static Stream<ProcessingProgress> processDataWithProgress(
    List<RawData> input,
  ) async* {
    final total = input.length;
    final batchSize = 100;

    for (var i = 0; i < total; i += batchSize) {
      final batch = input.skip(i).take(batchSize).toList();
      final processed = await Isolate.run(() {
        return batch.map((e) => _processItem(e)).toList();
      });

      yield ProcessingProgress(
        processed: processed,
        progress: (i + batch.length) / total,
      );
    }
  }
}
```

### Image Optimization

```dart
// ✅ Cached network images with placeholder
CachedNetworkImage(
  imageUrl: user.avatarUrl,
  placeholder: (context, url) => const ShimmerPlaceholder(),
  errorWidget: (context, url, error) => const Icon(Icons.error),
  memCacheWidth: 200,  // Cache at needed resolution
  memCacheHeight: 200,
)

// ✅ Precache images
class _MyScreenState extends State<MyScreen> {
  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    precacheImage(AssetImage('assets/hero.png'), context);
  }
}
```

---

## Testing Patterns

### Widget Testing with Riverpod

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

void main() {
  group('UserList', () {
    testWidgets('displays loading state', (tester) async {
      await tester.pumpWidget(
        ProviderScope(
          overrides: [
            usersProvider.overrideWith(
              (ref) => const AsyncValue.loading(),
            ),
          ],
          child: MaterialApp(home: UserListScreen()),
        ),
      );

      expect(find.byType(CircularProgressIndicator), findsOneWidget);
    });

    testWidgets('displays users', (tester) async {
      final users = [
        User(id: '1', name: 'Alice'),
        User(id: '2', name: 'Bob'),
      ];

      await tester.pumpWidget(
        ProviderScope(
          overrides: [
            usersProvider.overrideWith(
              (ref) => AsyncValue.data(users),
            ),
          ],
          child: MaterialApp(home: UserListScreen()),
        ),
      );

      expect(find.text('Alice'), findsOneWidget);
      expect(find.text('Bob'), findsOneWidget);
    });
  });
}
```

### BLoC Testing

```dart
import 'package:bloc_test/bloc_test.dart';
import 'package:mocktail/mocktail.dart';

class MockUserRepository extends Mock implements UserRepository {}

void main() {
  late MockUserRepository mockRepo;

  setUp(() {
    mockRepo = MockUserRepository();
  });

  group('UserBloc', () {
    blocTest<UserBloc, UserState>(
      'emits [Loading, Loaded] when LoadUsers is successful',
      setUp: () {
        when(() => mockRepo.getUsers())
            .thenAnswer((_) async => [User(id: '1', name: 'Alice')]);
      },
      build: () => UserBloc(mockRepo),
      act: (bloc) => bloc.add(LoadUsersEvent()),
      expect: () => [
        UserLoading(),
        UserLoaded([User(id: '1', name: 'Alice')]),
      ],
    );

    blocTest<UserBloc, UserState>(
      'emits [Loading, Error] when LoadUsers fails',
      setUp: () {
        when(() => mockRepo.getUsers()).thenThrow(Exception('Network error'));
      },
      build: () => UserBloc(mockRepo),
      act: (bloc) => bloc.add(LoadUsersEvent()),
      expect: () => [
        UserLoading(),
        isA<UserError>(),
      ],
    );
  });
}
```

### Integration Testing

```dart
import 'package:integration_test/integration_test.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('full login flow', (tester) async {
    // Given: App is running
    await tester.pumpWidget(MyApp());
    await tester.pumpAndSettle();

    // When: User enters credentials
    await tester.enterText(
      find.byKey(Key('email-field')),
      'test@example.com',
    );
    await tester.enterText(
      find.byKey(Key('password-field')),
      'password123',
    );
    await tester.tap(find.byKey(Key('login-button')));
    await tester.pumpAndSettle();

    // Then: Home screen is displayed
    expect(find.text('Welcome'), findsOneWidget);
  });
}
```

---

## Architecture Patterns

### Clean Architecture with DDD

```dart
// Domain Layer - Pure Dart
abstract class UserRepository {
  Future<Either<Failure, List<User>>> getUsers();
  Future<Either<Failure, User>> getUser(String id);
}

class GetUsersUseCase {
  final UserRepository _repository;

  const GetUsersUseCase(this._repository);

  Future<Either<Failure, List<User>>> call() => _repository.getUsers();
}

// Data Layer
class UserRepositoryImpl implements UserRepository {
  final UserRemoteDataSource _remote;
  final UserLocalDataSource _local;
  final NetworkInfo _networkInfo;

  UserRepositoryImpl(this._remote, this._local, this._networkInfo);

  @override
  Future<Either<Failure, List<User>>> getUsers() async {
    if (await _networkInfo.isConnected) {
      try {
        final users = await _remote.fetchUsers();
        await _local.cacheUsers(users);
        return Right(users);
      } catch (e) {
        return Left(ServerFailure());
      }
    } else {
      try {
        final users = await _local.getCachedUsers();
        return Right(users);
      } catch (e) {
        return Left(CacheFailure());
      }
    }
  }
}

// Presentation Layer
class UserViewModel extends StateNotifier<UserState> {
  final GetUsersUseCase _getUsersUseCase;

  UserViewModel(this._getUsersUseCase) : super(UserInitial());

  Future<void> loadUsers() async {
    state = UserLoading();
    final result = await _getUsersUseCase();
    state = result.fold(
      (failure) => UserError(failure.message),
      (users) => UserLoaded(users),
    );
  }
}
```

---

_DOMYH Awesome Code v6.1.2 — Flutter/Dart Advanced Patterns — 2025-2026_
