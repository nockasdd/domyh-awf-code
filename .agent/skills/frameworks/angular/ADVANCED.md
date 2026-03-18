# Angular — Advanced Patterns

## Table of Contents

- [Signals & Reactivity](#signals--reactivity)
- [Standalone Components](#standalone-components)
- [Server-Side Rendering](#server-side-rendering)
- [RxJS Advanced](#rxjs-advanced)
- [Performance](#performance)

---

## Signals & Reactivity

### Signal Patterns (Angular 17+)

```typescript
// Computed signals with derived state
@Component({
  template: `
    <input [ngModel]="searchQuery()" (ngModelChange)="searchQuery.set($event)" />
    <ul>
      @for (item of filteredItems(); track item.id) {
        <li>{{ item.name }}</li>
      }
    </ul>
    <p>{{ resultCount() }} results</p>
  `,
})
export class SearchComponent {
  searchQuery = signal('')
  items = signal<Item[]>([])

  filteredItems = computed(() =>
    this.items().filter(item =>
      item.name.toLowerCase().includes(this.searchQuery().toLowerCase())
    )
  )

  resultCount = computed(() => this.filteredItems().length)

  constructor() {
    // Side effect with cleanup
    effect((onCleanup) => {
      const query = this.searchQuery()
      const timeout = setTimeout(() => this.search(query), 300)
      onCleanup(() => clearTimeout(timeout))
    })
  }
}
```

### Signal Store (NgRx Signals)

```typescript
export const TodoStore = signalStore(
  { providedIn: 'root' },
  withState<TodoState>({ todos: [], loading: false, filter: 'all' }),
  withComputed(({ todos, filter }) => ({
    filteredTodos: computed(() => {
      const f = filter()
      return f === 'all' ? todos() : todos().filter(t => t.status === f)
    }),
    stats: computed(() => ({
      total: todos().length,
      completed: todos().filter(t => t.completed).length,
    })),
  })),
  withMethods((store, http = inject(HttpClient)) => ({
    async loadTodos() {
      patchState(store, { loading: true })
      const todos = await firstValueFrom(http.get<Todo[]>('/api/todos'))
      patchState(store, { todos, loading: false })
    },
    toggleTodo(id: string) {
      patchState(store, {
        todos: store.todos().map(t =>
          t.id === id ? { ...t, completed: !t.completed } : t
        ),
      })
    },
  }))
)
```

---

## Standalone Components

### Lazy Loading with Deferrable Views

```typescript
@Component({
  standalone: true,
  imports: [HeavyChartComponent],
  template: `
    @defer (on viewport) {
      <app-heavy-chart [data]="chartData" />
    } @placeholder {
      <div class="skeleton h-64 w-full rounded-lg"></div>
    } @loading (minimum 500ms) {
      <app-spinner />
    } @error {
      <p>Failed to load chart</p>
    }
  `,
})
export class DashboardComponent {}
```

---

## Server-Side Rendering

### SSR with Hydration (Angular 17+)

```typescript
// app.config.ts
export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    provideClientHydration(withEventReplay()),
    provideHttpClient(withFetch()),
  ],
}

// Transfer state for SSR→client
@Component({ ... })
export class DataComponent {
  private transferState = inject(TransferState)
  private http = inject(HttpClient)

  data = signal<Data | null>(null)

  async ngOnInit() {
    const key = makeStateKey<Data>('my-data')
    const cached = this.transferState.get(key, null)

    if (cached) {
      this.data.set(cached)
    } else {
      const data = await firstValueFrom(this.http.get<Data>('/api/data'))
      this.transferState.set(key, data)
      this.data.set(data)
    }
  }
}
```

---

## RxJS Advanced

### Custom Operators

```typescript
// Retry with exponential backoff
function retryWithBackoff<T>(maxRetries = 3, delayMs = 1000): MonoTypeOperatorFunction<T> {
  return (source) =>
    source.pipe(
      retry({
        count: maxRetries,
        delay: (error, retryCount) => timer(delayMs * Math.pow(2, retryCount - 1)),
      })
    )
}

// Debounced search with cancellation
searchResults$ = this.searchInput$.pipe(
  debounceTime(300),
  distinctUntilChanged(),
  filter(q => q.length >= 2),
  switchMap(query =>
    this.http.get<Result[]>(`/api/search?q=${query}`).pipe(
      retryWithBackoff(2),
      catchError(() => of([]))
    )
  ),
  shareReplay(1)
)
```

---

## Performance

### Change Detection Optimization

```typescript
@Component({
  changeDetection: ChangeDetectionStrategy.OnPush,  // Always use
  template: `
    <!-- Track by for *ngFor / @for -->
    @for (item of items(); track item.id) {
      <app-item [item]="item" />
    }
  `,
})
export class ListComponent {
  items = input.required<Item[]>()  // Signal-based input (v17.1+)
}
```

```yaml
performance_checklist:
  - "OnPush change detection on ALL components"
  - "track by id in @for loops"
  - "Lazy load routes: loadComponent/loadChildren"
  - "@defer for below-fold content"
  - "Signal inputs over @Input() decorator"
  - "Avoid subscribe() — use async pipe or toSignal()"
  - "preloadingStrategy: PreloadAllModules for routes"
```

---
