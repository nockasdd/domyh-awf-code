---
name: angular
detect: ["angular.json", "*.component.ts", "@angular/core"]
version: "4.3.0"
category: frontend
tier: 1
---

# Angular Patterns — DOMYH Agent v4.3

> **Version**: Angular 19/20 (2025-2026)
> **Philosophy**: Signals-first, standalone, zoneless-ready

---

## 🎯 When to Use This Skill

Use for: Enterprise web apps, type-safe SPA, complex forms.
**NOT for**: Simple sites (→ vue), mobile (→ react-native).

---

## 📦 Recommended Stack (2025-2026)

### Core

| Tool            | Use Case     |
| --------------- | ------------ |
| **Angular 19+** | Framework 🏆 |
| **Angular CLI** | Scaffolding  |
| **RxJS**        | Observables  |

### State

| Library              | Use Case              |
| -------------------- | --------------------- |
| **Signals**          | Angular reactivity 🏆 |
| **NgRx Signals**     | Complex state         |
| **Observable Store** | Simple state          |

### IDE Support

| IDE          | Features                 |
| ------------ | ------------------------ |
| **WebStorm** | Full Angular support 🏆  |
| **VS Code**  | Angular Language Service |

---

## 🆕 Angular 19/20 Features

### Signals (Stable)

```typescript
import { signal, computed, effect } from "@angular/core";

@Component({
  selector: "app-counter",
  standalone: true,
  template: `
    <button (click)="increment()">Count: {{ count() }}</button>
    <p>Double: {{ double() }}</p>
  `,
})
export class CounterComponent {
  // ✅ Signal for reactive state
  count = signal(0);

  // ✅ Computed for derived values
  double = computed(() => this.count() * 2);

  constructor() {
    // ✅ Effect for side effects
    effect(() => {
      console.log("Count changed:", this.count());
    });
  }

  increment() {
    // ✅ Update signal
    this.count.update((c) => c + 1);
    // Or: this.count.set(this.count() + 1);
  }
}
```

### Standalone Components (Default)

```typescript
// ✅ Angular 19: Standalone is default
@Component({
  selector: "app-user-card",
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <div class="card">
      <h2>{{ user().name }}</h2>
      <a [routerLink]="['/users', user().id]">View Profile</a>
    </div>
  `,
})
export class UserCardComponent {
  user = input.required<User>();
}
```

### Input/Output with Signals

```typescript
import { input, output, model } from "@angular/core";

@Component({
  selector: "app-form-field",
  standalone: true,
  template: ` <input [value]="value()" (input)="onInput($event)" /> `,
})
export class FormFieldComponent {
  // ✅ Signal-based inputs
  label = input<string>("");
  value = model<string>(""); // Two-way binding

  // ✅ Signal-based outputs
  valueChange = output<string>();

  onInput(event: Event) {
    const value = (event.target as HTMLInputElement).value;
    this.value.set(value);
    this.valueChange.emit(value);
  }
}
```

### Zoneless Change Detection

```typescript
// ✅ Angular 20: Zoneless stable
import { bootstrapApplication } from "@angular/platform-browser";
import { provideExperimentalZonelessChangeDetection } from "@angular/core";

bootstrapApplication(AppComponent, {
  providers: [provideExperimentalZonelessChangeDetection()],
});

// ✅ Component with signals works automatically
@Component({
  selector: "app-root",
  standalone: true,
  template: `<p>{{ message() }}</p>`,
})
export class AppComponent {
  message = signal("Hello");

  // No Zone.js needed - signals trigger change detection
}
```

---

## 🔧 Core Patterns

### Service with Signals

```typescript
@Injectable({ providedIn: "root" })
export class UserService {
  private users = signal<User[]>([]);
  private loading = signal(false);

  // Expose as readonly
  readonly users$ = this.users.asReadonly();
  readonly loading$ = this.loading.asReadonly();

  async loadUsers() {
    this.loading.set(true);
    try {
      const users = await this.http.get<User[]>("/api/users").toPromise();
      this.users.set(users);
    } finally {
      this.loading.set(false);
    }
  }
}
```

### HTTP with Signals

```typescript
@Component({
  selector: "app-users",
  standalone: true,
  imports: [CommonModule],
  template: `
    @if (loading()) {
      <p>Loading...</p>
    } @else {
      <ul>
        @for (user of users(); track user.id) {
          <li>{{ user.name }}</li>
        }
      </ul>
    }
  `,
})
export class UsersComponent {
  users = signal<User[]>([]);
  loading = signal(true);

  constructor(private http: HttpClient) {
    this.http.get<User[]>("/api/users").subscribe({
      next: (users) => this.users.set(users),
      complete: () => this.loading.set(false),
    });
  }
}
```

### New Control Flow

```html
<!-- ✅ Angular 17+: New control flow syntax -->
@if (user()) {
<h1>{{ user()!.name }}</h1>
} @else {
<p>No user</p>
} @for (item of items(); track item.id) {
<div>{{ item.name }}</div>
} @empty {
<p>No items</p>
} @switch (status()) { @case ('loading') { <spinner /> } @case ('error') {
<error-message /> } @default { <content /> } }

<!-- ✅ Deferred loading -->
@defer (on viewport) {
<heavy-component />
} @loading {
<p>Loading...</p>
} @placeholder {
<p>Placeholder</p>
}
```

---

## ✅ Best Practices Checklist

### Signals

- [ ] Use `signal()` for reactive state
- [ ] Use `computed()` for derived values
- [ ] Use `effect()` for side effects
- [ ] Prefer `input()` over `@Input()`

### Components

- [ ] Standalone components only
- [ ] Feature-based folder structure
- [ ] Small, focused components
- [ ] New control flow syntax

### Performance

- [ ] Enable zoneless mode
- [ ] Use `@defer` for lazy loading
- [ ] `track` in @for loops
- [ ] OnPush change detection

---

_DOMYH Agent v4.3 • Angular 19/20_
