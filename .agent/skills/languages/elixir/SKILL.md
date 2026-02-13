---
name: elixir
detect: ["*.ex", "*.exs", "mix.exs", "mix.lock"]
version: "6.2.4"
category: functional
tier: 2
---

# Elixir Patterns — DOMYH Awesome Code

> **Version**: Elixir 1.16+ / OTP 26+
> **Framework**: Phoenix 1.7+, LiveView 0.20+
> **Philosophy**: Fault-tolerant, concurrent, functional

---

## 🎯 When to Use This Skill

Use for: Real-time apps, distributed systems, high concurrency.
**NOT for**: ML/AI (→ python), mobile (→ flutter).

---

## 📦 Why Elixir?

| Feature         | Elixir         | Go         | Node.js    |
| --------------- | -------------- | ---------- | ---------- |
| Concurrency     | Actors 🏆      | Goroutines | Event loop |
| Fault tolerance | Supervisors 🏆 | Manual     | Manual     |
| Hot code reload | Yes 🏆         | No         | No         |
| Real-time       | LiveView 🏆    | WebSocket  | Socket.io  |

---

## 🔧 Project Setup

```bash
# Create Phoenix project
mix phx.new myapp --live

# Create library
mix new mylib

# Run
cd myapp
mix deps.get
mix phx.server
```

### Project Structure

```
myapp/
├── lib/
│   ├── myapp/
│   │   ├── application.ex
│   │   ├── repo.ex
│   │   └── accounts/
│   │       ├── user.ex
│   │       └── accounts.ex
│   └── myapp_web/
│       ├── router.ex
│       ├── controllers/
│       ├── live/
│       └── components/
├── test/
├── priv/repo/migrations/
├── config/
└── mix.exs
```

---

## 🔄 Core Patterns

### Pattern Matching

```elixir
# ✅ Function clauses with pattern matching
defmodule Calculator do
  def calculate({:add, a, b}), do: a + b
  def calculate({:sub, a, b}), do: a - b
  def calculate({:mul, a, b}), do: a * b
  def calculate({:div, _, 0}), do: {:error, :division_by_zero}
  def calculate({:div, a, b}), do: a / b
end

# ✅ With guards
def process(value) when is_binary(value), do: String.upcase(value)
def process(value) when is_integer(value), do: value * 2
def process(_), do: {:error, :unsupported_type}

# ✅ Destructuring
def handle_response({:ok, %{body: body, status: 200}}), do: {:ok, body}
def handle_response({:ok, %{status: 404}}), do: {:error, :not_found}
def handle_response({:error, reason}), do: {:error, reason}
```

### Pipe Operator

```elixir
# ✅ Chain transformations
def process_user(params) do
  params
  |> validate_params()
  |> create_user()
  |> send_welcome_email()
  |> log_creation()
end

# ✅ With error handling
def process_order(params) do
  with {:ok, validated} <- validate_params(params),
       {:ok, order} <- create_order(validated),
       {:ok, _} <- charge_payment(order),
       {:ok, _} <- send_confirmation(order) do
    {:ok, order}
  else
    {:error, :invalid_params} -> {:error, "Invalid order params"}
    {:error, :payment_failed} -> {:error, "Payment failed"}
    error -> error
  end
end
```

---

## ⚡ OTP Patterns

### GenServer

```elixir
defmodule MyApp.Counter do
  use GenServer

  # Client API
  def start_link(initial_value) do
    GenServer.start_link(__MODULE__, initial_value, name: __MODULE__)
  end

  def increment, do: GenServer.call(__MODULE__, :increment)
  def decrement, do: GenServer.call(__MODULE__, :decrement)
  def get_value, do: GenServer.call(__MODULE__, :get)

  # Server Callbacks
  @impl true
  def init(initial_value) do
    {:ok, initial_value}
  end

  @impl true
  def handle_call(:increment, _from, state) do
    {:reply, state + 1, state + 1}
  end

  @impl true
  def handle_call(:decrement, _from, state) do
    {:reply, state - 1, state - 1}
  end

  @impl true
  def handle_call(:get, _from, state) do
    {:reply, state, state}
  end
end
```

### Supervisor

```elixir
defmodule MyApp.Application do
  use Application

  @impl true
  def start(_type, _args) do
    children = [
      MyApp.Repo,
      {Phoenix.PubSub, name: MyApp.PubSub},
      MyAppWeb.Endpoint,
      # Custom workers
      {MyApp.Counter, 0},
      {MyApp.Cache, []},
      # Dynamic supervisor
      {DynamicSupervisor, name: MyApp.TaskSupervisor, strategy: :one_for_one}
    ]

    opts = [strategy: :one_for_one, name: MyApp.Supervisor]
    Supervisor.start_link(children, opts)
  end
end
```

---

## 🌐 Phoenix LiveView

```elixir
# lib/myapp_web/live/counter_live.ex
defmodule MyAppWeb.CounterLive do
  use MyAppWeb, :live_view

  @impl true
  def mount(_params, _session, socket) do
    {:ok, assign(socket, count: 0)}
  end

  @impl true
  def handle_event("increment", _params, socket) do
    {:noreply, update(socket, :count, &(&1 + 1))}
  end

  @impl true
  def handle_event("decrement", _params, socket) do
    {:noreply, update(socket, :count, &(&1 - 1))}
  end

  @impl true
  def render(assigns) do
    ~H"""
    <div class="flex items-center gap-4">
      <button phx-click="decrement" class="btn">-</button>
      <span class="text-2xl"><%= @count %></span>
      <button phx-click="increment" class="btn">+</button>
    </div>
    """
  end
end
```

### Real-time with PubSub

```elixir
defmodule MyAppWeb.ChatLive do
  use MyAppWeb, :live_view

  @impl true
  def mount(_params, _session, socket) do
    if connected?(socket) do
      Phoenix.PubSub.subscribe(MyApp.PubSub, "chat:lobby")
    end
    {:ok, assign(socket, messages: [])}
  end

  @impl true
  def handle_event("send_message", %{"message" => message}, socket) do
    Phoenix.PubSub.broadcast(MyApp.PubSub, "chat:lobby", {:new_message, message})
    {:noreply, socket}
  end

  @impl true
  def handle_info({:new_message, message}, socket) do
    {:noreply, update(socket, :messages, fn msgs -> msgs ++ [message] end)}
  end
end
```

---

## 🗃️ Ecto Database

```elixir
# Schema
defmodule MyApp.Accounts.User do
  use Ecto.Schema
  import Ecto.Changeset

  schema "users" do
    field :name, :string
    field :email, :string
    field :password_hash, :string
    has_many :posts, MyApp.Blog.Post

    timestamps()
  end

  def changeset(user, attrs) do
    user
    |> cast(attrs, [:name, :email])
    |> validate_required([:name, :email])
    |> validate_format(:email, ~r/@/)
    |> unique_constraint(:email)
  end
end

# Context
defmodule MyApp.Accounts do
  alias MyApp.Repo
  alias MyApp.Accounts.User

  def list_users do
    Repo.all(User)
  end

  def get_user!(id), do: Repo.get!(User, id)

  def create_user(attrs) do
    %User{}
    |> User.changeset(attrs)
    |> Repo.insert()
  end

  def update_user(%User{} = user, attrs) do
    user
    |> User.changeset(attrs)
    |> Repo.update()
  end
end
```

---

## 🧪 Testing

```elixir
# test/myapp/accounts_test.exs
defmodule MyApp.AccountsTest do
  use MyApp.DataCase

  alias MyApp.Accounts

  describe "users" do
    @valid_attrs %{name: "John", email: "john@example.com"}
    @invalid_attrs %{name: nil, email: nil}

    test "list_users/0 returns all users" do
      {:ok, user} = Accounts.create_user(@valid_attrs)
      assert Accounts.list_users() == [user]
    end

    test "create_user/1 with valid data creates a user" do
      assert {:ok, %User{} = user} = Accounts.create_user(@valid_attrs)
      assert user.name == "John"
      assert user.email == "john@example.com"
    end

    test "create_user/1 with invalid data returns error changeset" do
      assert {:error, %Ecto.Changeset{}} = Accounts.create_user(@invalid_attrs)
    end
  end
end
```

---

## ✅ Production Checklist

### Code Quality

- [ ] Credo linting passing
- [ ] Dialyzer type checking
- [ ] mix format applied
- [ ] @doc on public functions

### OTP

- [ ] Supervision trees designed
- [ ] Restart strategies appropriate
- [ ] No crashes in hot paths

### Performance

- [ ] Database indexes optimized
- [ ] Ecto queries efficient
- [ ] PubSub for real-time

---

_DOMYH Awesome Code • Elixir 1.16+ Phoenix 1.7+_
