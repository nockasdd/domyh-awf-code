# React — Advanced Patterns


# Load only when explicitly referenced

## Table of Contents

- [Advanced Hooks](#advanced-hooks)
- [Performance Patterns](#performance-patterns)
- [State Architecture](#state-architecture)
- [Testing Strategies](#testing-strategies)

---

## Advanced Hooks

### useReducer with Context

```tsx
interface State {
  user: User | null;
  loading: boolean;
  error: string | null;
}

type Action =
  | { type: "FETCH_START" }
  | { type: "FETCH_SUCCESS"; payload: User }
  | { type: "FETCH_ERROR"; payload: string };

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case "FETCH_START":
      return { ...state, loading: true, error: null };
    case "FETCH_SUCCESS":
      return { ...state, loading: false, user: action.payload };
    case "FETCH_ERROR":
      return { ...state, loading: false, error: action.payload };
  }
}

const UserContext = createContext<{
  state: State;
  dispatch: Dispatch<Action>;
} | null>(null);

export function UserProvider({ children }: PropsWithChildren) {
  const [state, dispatch] = useReducer(reducer, initialState);
  return (
    <UserContext.Provider value={{ state, dispatch }}>
      {children}
    </UserContext.Provider>
  );
}
```

### Custom Hook: useFetch

```tsx
function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const controller = new AbortController();

    async function fetchData() {
      try {
        const res = await fetch(url, { signal: controller.signal });
        const json = await res.json();
        setData(json);
      } catch (err) {
        if (err instanceof Error && err.name !== "AbortError") {
          setError(err);
        }
      } finally {
        setLoading(false);
      }
    }

    fetchData();
    return () => controller.abort();
  }, [url]);

  return { data, loading, error };
}
```

---

## Performance Patterns

### React.memo with Custom Comparison

```tsx
interface Props {
  items: Item[];
  onSelect: (id: string) => void;
}

const ItemList = memo(
  function ItemList({ items, onSelect }: Props) {
    return (
      <ul>
        {items.map((item) => (
          <li key={item.id} onClick={() => onSelect(item.id)}>
            {item.name}
          </li>
        ))}
      </ul>
    );
  },
  (prevProps, nextProps) => {
    // Custom comparison - only re-render if items changed
    return prevProps.items === nextProps.items;
  },
);
```

### useDeferredValue for Heavy Updates

```tsx
function SearchResults({ query }: { query: string }) {
  const deferredQuery = useDeferredValue(query);
  const isStale = query !== deferredQuery;

  const results = useMemo(() => searchItems(deferredQuery), [deferredQuery]);

  return (
    <div style={{ opacity: isStale ? 0.5 : 1 }}>
      {results.map((item) => (
        <ResultItem key={item.id} item={item} />
      ))}
    </div>
  );
}
```

### Virtual List Pattern

```tsx
function VirtualList<T>({
  items,
  itemHeight,
  containerHeight,
  renderItem,
}: VirtualListProps<T>) {
  const [scrollTop, setScrollTop] = useState(0);

  const startIndex = Math.floor(scrollTop / itemHeight);
  const endIndex = Math.min(
    startIndex + Math.ceil(containerHeight / itemHeight) + 1,
    items.length,
  );

  const visibleItems = items.slice(startIndex, endIndex);
  const offsetY = startIndex * itemHeight;

  return (
    <div
      style={{ height: containerHeight, overflow: "auto" }}
      onScroll={(e) => setScrollTop(e.currentTarget.scrollTop)}
    >
      <div style={{ height: items.length * itemHeight, position: "relative" }}>
        <div style={{ transform: `translateY(${offsetY}px)` }}>
          {visibleItems.map((item, i) => renderItem(item, startIndex + i))}
        </div>
      </div>
    </div>
  );
}
```

---

## State Architecture

### Zustand Store Pattern

```tsx
import { create } from "zustand";
import { immer } from "zustand/middleware/immer";

interface CartStore {
  items: CartItem[];
  addItem: (item: CartItem) => void;
  removeItem: (id: string) => void;
  total: () => number;
}

const useCartStore = create<CartStore>()(
  immer((set, get) => ({
    items: [],
    addItem: (item) =>
      set((state) => {
        state.items.push(item);
      }),
    removeItem: (id) =>
      set((state) => {
        state.items = state.items.filter((i) => i.id !== id);
      }),
    total: () => get().items.reduce((sum, i) => sum + i.price, 0),
  })),
);
```

### Server State with TanStack Query

```tsx
function useUserQuery(userId: string) {
  return useQuery({
    queryKey: ["user", userId],
    queryFn: () => fetchUser(userId),
    staleTime: 5 * 60 * 1000, // 5 minutes
    gcTime: 30 * 60 * 1000, // 30 minutes
  });
}

function useMutateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: updateUser,
    onSuccess: (data) => {
      queryClient.setQueryData(["user", data.id], data);
    },
    onError: () => {
      // Handle error
    },
  });
}
```

---

## Testing Strategies

### Testing Hooks

```tsx
import { renderHook, act } from "@testing-library/react";

test("useCounter increments", () => {
  const { result } = renderHook(() => useCounter(0));

  act(() => {
    result.current.increment();
  });

  expect(result.current.count).toBe(1);
});
```

### Component Testing with MSW

```tsx
import { server } from "./mocks/server";
import { rest } from "msw";

test("loads user data", async () => {
  server.use(
    rest.get("/api/user", (req, res, ctx) => {
      return res(ctx.json({ id: "1", name: "Test" }));
    }),
  );

  render(<UserProfile />);

  expect(await screen.findByText("Test")).toBeInTheDocument();
});
```

---

## Vercel Performance Rules — Full Reference

> **Source**: Vercel React Best Practices
> **Total**: 57 rules across 8 categories
> **Impact**: 2-10× performance improvement when applied

---

### Category 1: Async Patterns (CRITICAL)

#### `async-parallel`: Promise.all() for Independent Operations

When async operations have no interdependencies, execute concurrently.

```tsx
// ❌ Sequential (3 round trips)
const user = await fetchUser();
const posts = await fetchPosts();
const comments = await fetchComments();

// ✅ Parallel (1 round trip, 2-10× faster)
const [user, posts, comments] = await Promise.all([
  fetchUser(),
  fetchPosts(),
  fetchComments(),
]);
```

#### `async-defer-await`: Move await into branches

Only await where the value is actually needed.

```tsx
// ❌ Blocks entire function
async function getData() {
  const data = await fetchData();
  if (condition) {
    return data.processed;
  }
  return null; // Awaited even when not needed
}

// ✅ Deferred await
async function getData() {
  const dataPromise = fetchData();
  if (condition) {
    const data = await dataPromise;
    return data.processed;
  }
  return null; // No await at all
}
```

#### `async-suspense-boundaries`: Use Suspense for streaming

```tsx
// ✅ Stream content progressively
export default function Page() {
  return (
    <Suspense fallback={<HeaderSkeleton />}>
      <Header />
    </Suspense>
    <Suspense fallback={<ContentSkeleton />}>
      <Content />
    </Suspense>
  );
}
```

---

### Category 2: Bundle Size (CRITICAL)

#### `bundle-barrel-imports`: Avoid Barrel File Imports

Import directly from source files to avoid loading thousands of unused modules.

```tsx
// ❌ Imports entire library (1,583 modules, ~2.8s extra)
import { Check, X, Menu } from "lucide-react";

// ✅ Direct imports (3 modules, ~2KB vs ~1MB)
import Check from "lucide-react/dist/esm/icons/check";
import X from "lucide-react/dist/esm/icons/x";
import Menu from "lucide-react/dist/esm/icons/menu";

// ✅ Alternative: Next.js 13.5+
// next.config.js
module.exports = {
  experimental: {
    optimizePackageImports: ["lucide-react", "@mui/material"],
  },
};
```

**Impact**: 15-70% faster dev boot, 28% faster builds, 40% faster cold starts.

#### `bundle-dynamic-imports`: Use next/dynamic for heavy components

```tsx
import dynamic from "next/dynamic";

// ✅ Load Chart only when needed
const Chart = dynamic(() => import("@/components/Chart"), {
  loading: () => <ChartSkeleton />,
  ssr: false,
});
```

#### `bundle-defer-third-party`: Load analytics after hydration

```tsx
useEffect(() => {
  // Load analytics after page is interactive
  import("analytics").then((analytics) => analytics.init());
}, []);
```

---

### Category 3: Server-Side Performance (HIGH)

#### `server-cache-react`: Per-Request Deduplication

```tsx
import { cache } from "react";

// ✅ Deduplicated within single request
export const getCurrentUser = cache(async () => {
  const session = await auth();
  if (!session?.user?.id) return null;
  return await db.user.findUnique({
    where: { id: session.user.id },
  });
});
```

**Note**: Use primitive args for cache hits (objects create new references).

#### `server-cache-lru`: Cross-Request Caching

```tsx
import { LRUCache } from "lru-cache";

const cache = new LRUCache<string, any>({
  max: 100,
  ttl: 1000 * 60 * 5, // 5 minutes
});

export async function getCachedData(key: string) {
  if (cache.has(key)) return cache.get(key);
  const data = await fetchData(key);
  cache.set(key, data);
  return data;
}
```

#### `server-parallel-fetching`: Restructure for parallel fetches

```tsx
// ❌ Waterfall in nested components
async function Dashboard() {
  const user = await getUser(); // 200ms
  return <Profile userId={user.id} />; // triggers another fetch
}

// ✅ Parallel fetches at route level
async function Dashboard() {
  const [user, profile] = await Promise.all([getUser(), getProfile()]);
  return <DashboardView user={user} profile={profile} />;
}
```

---

### Category 4: Re-render Optimization (MEDIUM)

#### `rerender-memo`: Extract to Memoized Components

```tsx
// ❌ Computes avatar even when loading
function Profile({ user, loading }: Props) {
  const avatar = useMemo(() => computeAvatarId(user), [user]);
  if (loading) return <Skeleton />;
  return <Avatar id={avatar} />;
}

// ✅ Skips computation when loading
const UserAvatar = memo(({ user }: { user: User }) => {
  const id = useMemo(() => computeAvatarId(user), [user]);
  return <Avatar id={id} />;
});

function Profile({ user, loading }: Props) {
  if (loading) return <Skeleton />;
  return <UserAvatar user={user} />;
}
```

#### `rerender-derived-state`: Subscribe to derived booleans

```tsx
// ❌ Re-renders on every count change
const [count, setCount] = useState(0);
const hasItems = count > 0;

// ✅ Component only re-renders when hasItems changes
const hasItems = useSyncExternalStore(
  subscribe,
  () => store.getState().items.length > 0,
);
```

#### `rerender-functional-setstate`: Use functional updates

```tsx
// ❌ Creates new callback reference each render
<Button onClick={() => setCount(count + 1)} />;

// ✅ Stable callback reference
const increment = useCallback(() => setCount((c) => c + 1), []);
<Button onClick={increment} />;
```

---

### Category 5: JavaScript Performance (MEDIUM)

#### `js-batch-dom-css`: Group CSS changes

```tsx
// ❌ Forces 3 reflows
element.style.width = "100px";
element.style.height = "100px";
element.style.margin = "10px";

// ✅ Single reflow
element.classList.add("sized-box");
// OR
element.style.cssText = "width:100px;height:100px;margin:10px";
```

#### `js-set-map-lookups`: Use Set/Map for O(1) lookups

```tsx
// ❌ O(n) on every check
const ids = [1, 2, 3, 4, 5];
if (ids.includes(targetId)) {
}

// ✅ O(1) lookup
const idSet = new Set([1, 2, 3, 4, 5]);
if (idSet.has(targetId)) {
}
```

---

### Category 6: Rendering Performance (MEDIUM)

#### `rendering-content-visibility`: Use for long lists

```css
.off-screen-section {
  content-visibility: auto;
  contain-intrinsic-size: 0 500px;
}
```

#### `rendering-conditional-render`: Use ternary, not &&

```tsx
// ❌ Can render "0" or "false" as text
{
  count && <Badge count={count} />;
}

// ✅ Always works correctly
{
  count > 0 ? <Badge count={count} /> : null;
}
```

---

### Quick Reference Summary

| Priority | Category       | Impact   | Key Rules                                    |
| -------- | -------------- | -------- | -------------------------------------------- |
| 1        | Async Patterns | CRITICAL | Promise.all, defer-await, Suspense           |
| 2        | Bundle Size    | CRITICAL | Direct imports, dynamic(), defer third-party |
| 3        | Server-Side    | HIGH     | React.cache, LRU cache, parallel fetches     |
| 4        | Re-render      | MEDIUM   | memo, derived state, functional setState     |
| 5        | JavaScript     | MEDIUM   | Batch DOM, Set/Map lookups                   |
| 6        | Rendering      | MEDIUM   | content-visibility, ternary conditionals     |

---

## Composition Patterns (10 Rules)

> **Source**: Vercel Composition Patterns
> **Purpose**: Avoid boolean prop proliferation

### Architecture Patterns

#### `architecture-avoid-boolean-props`: Use composition over booleans

```tsx
// ❌ Boolean prop proliferation
<Modal isLarge isFullscreen hasCloseButton hasOverlay />

// ✅ Composition pattern
<Modal size="fullscreen">
  <Modal.Overlay />
  <Modal.Content>
    <Modal.CloseButton />
    {children}
  </Modal.Content>
</Modal>
```

#### `architecture-compound-components`: Shared context pattern

```tsx
const TabsContext = createContext<TabsContextType | null>(null);

function Tabs({ children, defaultTab }: Props) {
  const [activeTab, setActiveTab] = useState(defaultTab);
  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      {children}
    </TabsContext.Provider>
  );
}

Tabs.Tab = function Tab({ id, children }: TabProps) {
  const { activeTab, setActiveTab } = useContext(TabsContext)!;
  return (
    <button onClick={() => setActiveTab(id)} data-active={activeTab === id}>
      {children}
    </button>
  );
};
```

### State Management Patterns

#### `state-lift-state`: Move state into provider

```tsx
// Provider is the only place that knows how state is managed
function CartProvider({ children }: Props) {
  const [items, setItems] = useState<CartItem[]>([]);
  const addItem = useCallback((item: CartItem) => {
    setItems((prev) => [...prev, item]);
  }, []);

  return (
    <CartContext.Provider value={{ items, addItem }}>
      {children}
    </CartContext.Provider>
  );
}
```

#### `state-context-interface`: Generic interface for DI

```tsx
interface ContextValue<T> {
  state: T;
  actions: {
    update: (value: Partial<T>) => void;
    reset: () => void;
  };
  meta: {
    loading: boolean;
    error: Error | null;
  };
}
```

### React 19 APIs

#### `react19-no-forwardref`: Use ref directly (React 19+)

```tsx
// ❌ React 18 pattern
const Input = forwardRef<HTMLInputElement, Props>((props, ref) => {
  return <input ref={ref} {...props} />;
});

// ✅ React 19 pattern - ref is just a prop
function Input({ ref, ...props }: Props & { ref?: Ref<HTMLInputElement> }) {
  return <input ref={ref} {...props} />;
}
```

---
