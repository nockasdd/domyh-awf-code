# Vue.js — Advanced Patterns

# DOMYH Awesome Code — Tier 3 Reference

## Table of Contents

- [Composition API](#composition-api)
- [Reactivity System](#reactivity-system)
- [Performance](#performance)
- [Testing](#testing)

---

## Composition API

### Composables

```ts
// useAsync.ts
export function useAsync<T>(fn: () => Promise<T>) {
  const data = ref<T | null>(null);
  const error = ref<Error | null>(null);
  const loading = ref(false);

  const execute = async () => {
    loading.value = true;
    error.value = null;
    try {
      data.value = await fn();
    } catch (e) {
      error.value = e as Error;
    } finally {
      loading.value = false;
    }
  };

  return { data, error, loading, execute };
}

// useFetch.ts
export function useFetch<T>(url: MaybeRef<string>) {
  const urlRef = toRef(url);
  const { data, error, loading, execute } = useAsync(() =>
    fetch(urlRef.value).then((r) => r.json()),
  );

  watch(urlRef, execute, { immediate: true });

  return { data, error, loading, refresh: execute };
}
```

### Provide/Inject with TypeScript

```ts
// Typed injection key
const UserKey: InjectionKey<Ref<User>> = Symbol("user");

// Provider
const user = ref<User>({ id: "1", name: "Admin" });
provide(UserKey, user);

// Consumer
const user = inject(UserKey);
if (!user) throw new Error("User not provided");

// With default
const user = inject(UserKey, ref({ id: "", name: "Guest" }));
```

---

## Reactivity System

### Deep vs Shallow

```ts
// Shallow reactive - only root level reactive
const state = shallowReactive({
  nested: { count: 0 },
});
state.nested = { count: 1 }; // Triggers update
state.nested.count = 2; // Does NOT trigger

// ShallowRef for large objects
const largeData = shallowRef<BigObject>(null);
largeData.value = newData; // Triggers update
largeData.value.field = "x"; // Does NOT trigger

// TriggerRef for manual updates
triggerRef(largeData); // Force trigger
```

### Custom Ref

```ts
function useDebouncedRef<T>(value: T, delay = 200) {
  let timeout: ReturnType<typeof setTimeout>;
  return customRef((track, trigger) => ({
    get() {
      track();
      return value;
    },
    set(newValue) {
      clearTimeout(timeout);
      timeout = setTimeout(() => {
        value = newValue;
        trigger();
      }, delay);
    },
  }));
}

// Usage
const searchQuery = useDebouncedRef("", 300);
```

---

## Performance

### Virtual List

```ts
// useVirtualList.ts
export function useVirtualList<T>(
  items: Ref<T[]>,
  options: { itemHeight: number; containerHeight: number },
) {
  const scrollTop = ref(0);

  const visibleItems = computed(() => {
    const start = Math.floor(scrollTop.value / options.itemHeight);
    const visible = Math.ceil(options.containerHeight / options.itemHeight);
    return {
      start,
      end: Math.min(start + visible + 1, items.value.length),
      items: items.value.slice(start, start + visible + 1),
    };
  });

  const totalHeight = computed(() => items.value.length * options.itemHeight);

  const offsetY = computed(() => visibleItems.value.start * options.itemHeight);

  const onScroll = (e: Event) => {
    scrollTop.value = (e.target as HTMLElement).scrollTop;
  };

  return { visibleItems, totalHeight, offsetY, onScroll };
}
```

### Component Caching

```vue
<template>
  <KeepAlive :max="5">
    <component :is="currentView" :key="route.path" />
  </KeepAlive>
</template>

<script setup>
// Control caching behavior
onActivated(() => {
  // Called when component is restored from cache
  fetchLatestData();
});

onDeactivated(() => {
  // Called when component is cached
  cleanupSubscriptions();
});
</script>
```

---

## Testing

### Component Testing

```ts
import { mount } from "@vue/test-utils";
import { createTestingPinia } from "@pinia/testing";

describe("UserList", () => {
  it("renders users from store", async () => {
    const wrapper = mount(UserList, {
      global: {
        plugins: [
          createTestingPinia({
            initialState: {
              users: { list: [{ id: "1", name: "Test" }] },
            },
          }),
        ],
      },
    });

    expect(wrapper.text()).toContain("Test");
  });

  it("emits select on click", async () => {
    const wrapper = mount(UserList);
    await wrapper.find(".user-item").trigger("click");
    expect(wrapper.emitted("select")).toBeTruthy();
  });
});
```

---

_DOMYH Awesome Code — Tier 3 Reference_
