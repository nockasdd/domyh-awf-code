# Kotlin — Advanced Patterns

> DOMYH Awesome Code — Tier 3 Reference

## Table of Contents

- [Advanced Coroutines](#advanced-coroutines)
- [Flow Patterns](#flow-patterns)
- [KMP Advanced Patterns](#kmp-advanced-patterns)
- [Compose Optimization](#compose-optimization)
- [Testing Patterns](#testing-patterns)

---

## Advanced Coroutines

### Structured Concurrency

```kotlin
// ✅ CoroutineScope that propagates cancellation
class UserRepository(
    private val api: UserApi,
    private val cache: UserCache,
) {
    // Parallel fetch with structured cancellation
    suspend fun getUserWithDetails(id: String): UserDetails = coroutineScope {
        val userDeferred = async { api.getUser(id) }
        val ordersDeferred = async { api.getOrders(id) }
        val reviewsDeferred = async { api.getReviews(id) }

        // If any fails, all are cancelled
        UserDetails(
            user = userDeferred.await(),
            orders = ordersDeferred.await(),
            reviews = reviewsDeferred.await()
        )
    }

    // SupervisorScope: siblings don't cancel each other
    suspend fun fetchOptionalData(id: String): OptionalData = supervisorScope {
        val primary = async { api.getPrimaryData(id) }
        val secondary = async {
            try { api.getSecondaryData(id) }
            catch (e: Exception) { null }  // Can fail without affecting primary
        }

        OptionalData(
            primary = primary.await(),
            secondary = secondary.await()
        )
    }
}
```

### Custom CoroutineScope

```kotlin
// ✅ Lifecycle-aware scope
class AppContainer : LifecycleOwner {
    private val job = SupervisorJob()
    private val scope = CoroutineScope(Dispatchers.Main + job)

    override fun onDestroy() {
        job.cancel()  // Cancels all children
    }

    fun launchInScope(block: suspend CoroutineScope.() -> Unit) {
        scope.launch { block() }
    }
}

// ✅ Exception handler
private val errorHandler = CoroutineExceptionHandler { _, throwable ->
    Log.e("AppScope", "Uncaught exception", throwable)
    analytics.logError(throwable)
}

val safeScope = CoroutineScope(Dispatchers.Main + job + errorHandler)
```

### Retry with Backoff

```kotlin
// ✅ Exponential backoff retry
suspend fun <T> retry(
    times: Int = 3,
    initialDelay: Long = 100,
    maxDelay: Long = 5000,
    factor: Double = 2.0,
    block: suspend () -> T
): T {
    var currentDelay = initialDelay
    repeat(times - 1) { attempt ->
        try {
            return block()
        } catch (e: Exception) {
            Log.w("Retry", "Attempt $attempt failed, retrying in ${currentDelay}ms")
        }
        delay(currentDelay)
        currentDelay = (currentDelay * factor).toLong().coerceAtMost(maxDelay)
    }
    return block()  // Last attempt
}

// Usage
suspend fun fetchUser(id: String): User = retry {
    api.getUser(id)
}
```

---

## Flow Patterns

### StateFlow for UI State

```kotlin
// ✅ UI State pattern
sealed interface UiState<out T> {
    data object Loading : UiState<Nothing>
    data class Success<T>(val data: T) : UiState<T>
    data class Error(val message: String, val retry: () -> Unit) : UiState<Nothing>
}

class UserViewModel(
    private val repository: UserRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow<UiState<User>>(UiState.Loading)
    val uiState: StateFlow<UiState<User>> = _uiState.asStateFlow()

    init {
        loadUser()
    }

    fun loadUser() {
        viewModelScope.launch {
            _uiState.value = UiState.Loading
            try {
                val user = repository.getUser()
                _uiState.value = UiState.Success(user)
            } catch (e: Exception) {
                _uiState.value = UiState.Error(
                    message = e.message ?: "Unknown error",
                    retry = ::loadUser
                )
            }
        }
    }
}

// ✅ In Composable
@Composable
fun UserScreen(viewModel: UserViewModel) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    when (val state = uiState) {
        is UiState.Loading -> LoadingIndicator()
        is UiState.Success -> UserContent(state.data)
        is UiState.Error -> ErrorMessage(
            message = state.message,
            onRetry = state.retry
        )
    }
}
```

### SharedFlow for Events

```kotlin
// ✅ One-time events (navigation, snackbar)
class UserViewModel : ViewModel() {
    private val _events = MutableSharedFlow<UiEvent>()
    val events: SharedFlow<UiEvent> = _events.asSharedFlow()

    sealed interface UiEvent {
        data class ShowSnackbar(val message: String) : UiEvent
        data class Navigate(val route: String) : UiEvent
    }

    fun onSaveClicked() {
        viewModelScope.launch {
            try {
                repository.saveUser()
                _events.emit(UiEvent.ShowSnackbar("Saved successfully"))
                _events.emit(UiEvent.Navigate("home"))
            } catch (e: Exception) {
                _events.emit(UiEvent.ShowSnackbar("Failed to save"))
            }
        }
    }
}

// ✅ Collect events
@Composable
fun UserScreen(viewModel: UserViewModel) {
    val snackbarHostState = remember { SnackbarHostState() }

    LaunchedEffect(Unit) {
        viewModel.events.collect { event ->
            when (event) {
                is UiEvent.ShowSnackbar -> snackbarHostState.showSnackbar(event.message)
                is UiEvent.Navigate -> navController.navigate(event.route)
            }
        }
    }
}
```

### Flow Operators

```kotlin
// ✅ Debounce for search
fun observeSearch(query: StateFlow<String>): Flow<List<SearchResult>> =
    query
        .debounce(300)  // Wait 300ms after last keystroke
        .filter { it.length >= 2 }  // Min 2 characters
        .distinctUntilChanged()  // Ignore duplicates
        .flatMapLatest { q -> searchRepository.search(q) }  // Cancel previous

// ✅ Combine multiple flows
val combinedState: StateFlow<CombinedState> = combine(
    userFlow,
    settingsFlow,
    networkStatusFlow
) { user, settings, network ->
    CombinedState(user, settings, network)
}.stateIn(
    scope = viewModelScope,
    started = SharingStarted.WhileSubscribed(5000),
    initialValue = CombinedState.EMPTY
)
```

---

## KMP Advanced Patterns

### Dependency Injection in KMP

```kotlin
// ✅ Koin for KMP
// commonMain
val commonModule = module {
    single<UserRepository> { UserRepositoryImpl(get()) }
    single<SettingsRepository> { SettingsRepositoryImpl(get()) }
}

// androidMain
val androidModule = module {
    single<HttpClient> {
        HttpClient(OkHttp) {
            install(ContentNegotiation) { json() }
        }
    }
    single<DataStore<Preferences>> { context.dataStore }
}

// iosMain
val iosModule = module {
    single<HttpClient> {
        HttpClient(Darwin) {
            install(ContentNegotiation) { json() }
        }
    }
    single { NSUserDefaults.standardUserDefaults }
}

// Initialize
fun initKoin(appDeclaration: KoinAppDeclaration = {}) = startKoin {
    appDeclaration()
    modules(commonModule, platformModule())
}
```

### Platform-Specific Implementations

```kotlin
// ✅ File handling across platforms
// commonMain
expect class FileHandler() {
    suspend fun readFile(path: String): String
    suspend fun writeFile(path: String, content: String)
}

// androidMain
actual class FileHandler {
    private val context: Context = ApplicationContext.get()

    actual suspend fun readFile(path: String): String = withContext(Dispatchers.IO) {
        context.openFileInput(path).bufferedReader().useLines { it.joinToString("\n") }
    }

    actual suspend fun writeFile(path: String, content: String) = withContext(Dispatchers.IO) {
        context.openFileOutput(path, Context.MODE_PRIVATE).bufferedWriter().use {
            it.write(content)
        }
    }
}

// iosMain
actual class FileHandler {
    private val fileManager = NSFileManager.defaultManager

    actual suspend fun readFile(path: String): String {
        val url = getDocumentsDirectory().URLByAppendingPathComponent(path)
        return NSString.stringWithContentsOfURL(url, NSUTF8StringEncoding, null) as String
    }

    actual suspend fun writeFile(path: String, content: String) {
        val url = getDocumentsDirectory().URLByAppendingPathComponent(path)
        (content as NSString).writeToURL(url, true, NSUTF8StringEncoding, null)
    }

    private fun getDocumentsDirectory(): NSURL {
        return NSFileManager.defaultManager.URLsForDirectory(
            NSDocumentDirectory,
            NSUserDomainMask
        ).first() as NSURL
    }
}
```

---

## Compose Optimization

### Stability and Immutability

```kotlin
// ✅ Mark as stable for Compose compiler
@Immutable
data class User(
    val id: String,
    val name: String,
    val email: String
)

// ✅ Use stable collections
import kotlinx.collections.immutable.*

@Immutable
data class UserListState(
    val users: ImmutableList<User>,  // from kotlinx.collections.immutable
    val isLoading: Boolean
)

// ❌ AVOID: Mutable or unstable types
data class BadState(
    val users: List<User>,  // Not guaranteed stable
    val metadata: Map<String, Any>  // Any is not stable
)
```

### remember and derivedStateOf

```kotlin
@Composable
fun UserList(
    users: ImmutableList<User>,
    searchQuery: String
) {
    // ✅ remember expensive computation
    val filteredUsers = remember(users, searchQuery) {
        if (searchQuery.isEmpty()) users
        else users.filter { it.name.contains(searchQuery, ignoreCase = true) }
    }

    // ✅ derivedStateOf for derived state that changes less often
    val hasResults by remember {
        derivedStateOf { filteredUsers.isNotEmpty() }
    }

    // ✅ rememberSaveable for configuration changes
    var selectedIndex by rememberSaveable { mutableIntStateOf(-1) }

    LazyColumn {
        items(filteredUsers, key = { it.id }) { user ->
            UserItem(user)
        }
    }
}
```

### Lambda Stability

```kotlin
// ❌ AVOID: Lambda capturing state
@Composable
fun UserItem(user: User, viewModel: UserViewModel) {
    Button(onClick = { viewModel.selectUser(user.id) }) {  // Unstable lambda
        Text("Select")
    }
}

// ✅ Use remember for lambdas
@Composable
fun UserItem(
    user: User,
    onSelect: (String) -> Unit
) {
    val onClick = remember(user.id) { { onSelect(user.id) } }

    Button(onClick = onClick) {
        Text("Select")
    }
}

// ✅ Or use method reference
class UserItemState(
    private val userId: String,
    private val onSelect: (String) -> Unit
) {
    fun handleClick() = onSelect(userId)
}
```

---

## Testing Patterns

### ViewModel Testing with Turbine

```kotlin
import app.cash.turbine.test
import kotlinx.coroutines.test.runTest

@OptIn(ExperimentalCoroutinesApi::class)
class UserViewModelTest {

    @Test
    fun `loadUser emits loading then success`() = runTest {
        val mockRepo = mockk<UserRepository> {
            coEvery { getUser() } returns User("1", "Alice")
        }
        val viewModel = UserViewModel(mockRepo)

        viewModel.uiState.test {
            assertEquals(UiState.Loading, awaitItem())

            val success = awaitItem() as UiState.Success
            assertEquals("Alice", success.data.name)

            cancelAndIgnoreRemainingEvents()
        }
    }

    @Test
    fun `loadUser emits error on failure`() = runTest {
        val mockRepo = mockk<UserRepository> {
            coEvery { getUser() } throws Exception("Network error")
        }
        val viewModel = UserViewModel(mockRepo)

        viewModel.uiState.test {
            assertEquals(UiState.Loading, awaitItem())

            val error = awaitItem() as UiState.Error
            assertEquals("Network error", error.message)

            cancelAndIgnoreRemainingEvents()
        }
    }
}
```

### Compose UI Testing

```kotlin
@OptIn(ExperimentalTestApi::class)
class UserScreenTest {

    @get:Rule
    val composeTestRule = createComposeRule()

    @Test
    fun displaysUserName() {
        val user = User("1", "Alice", "alice@example.com")

        composeTestRule.setContent {
            UserCard(user = user, onEdit = {})
        }

        composeTestRule.onNodeWithText("Alice").assertIsDisplayed()
        composeTestRule.onNodeWithText("alice@example.com").assertIsDisplayed()
    }

    @Test
    fun clickEditButtonTriggersCallback() {
        var editClicked = false
        val user = User("1", "Alice", "alice@example.com")

        composeTestRule.setContent {
            UserCard(user = user, onEdit = { editClicked = true })
        }

        composeTestRule.onNodeWithText("Edit").performClick()

        assertTrue(editClicked)
    }
}
```

### KMP Testing

```kotlin
// commonTest
class UserRepositoryTest {

    private val mockApi = FakeUserApi()
    private val repository = UserRepositoryImpl(mockApi)

    @Test
    fun getUserReturnsUser() = runTest {
        mockApi.setUser(User("1", "Alice"))

        val user = repository.getUser("1")

        assertEquals("Alice", user.name)
    }
}

// Fake implementation for testing
class FakeUserApi : UserApi {
    private var user: User? = null

    fun setUser(user: User) {
        this.user = user
    }

    override suspend fun getUser(id: String): User {
        return user ?: throw Exception("User not found")
    }
}
```

---
