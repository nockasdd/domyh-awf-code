# React — Advanced Patterns

# DOMYH Agent v4.2 — Tier 3 Reference

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

_DOMYH Agent v4.2 — Tier 3 Reference_
