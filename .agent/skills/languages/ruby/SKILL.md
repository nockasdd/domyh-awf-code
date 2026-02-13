---
name: ruby
detect: ["Gemfile", "*.rb", "*.gemspec", "Rakefile", "config.ru"]
version: "6.2.5"
category: scripting
tier: 1
---

# Ruby Patterns — DOMYH Awesome Code

> **Version**: Ruby 3.3/3.4 (2025-2026)
> **Frameworks**: Rails 8, Hotwire, Hanami 2
> **Philosophy**: Convention over configuration, developer happiness

---

## 🎯 When to Use This Skill

Use for: Web apps, APIs, scripting, DevOps tools, prototyping.
**NOT for**: High-performance systems (→ rust), mobile apps (→ flutter).

---

## 📦 Recommended Stack (2025-2026)

### Web Frameworks

| Framework    | Use Case           | Install               |
| ------------ | ------------------ | --------------------- |
| **Rails 8**  | Full-stack web 🏆  | `gem install rails`   |
| **Hanami 2** | Clean architecture | `gem install hanami`  |
| **Sinatra**  | Microservices      | `gem install sinatra` |
| **Roda**     | Fast routing       | `gem install roda`    |

### Testing

| Library        | Use Case       | Install                   |
| -------------- | -------------- | ------------------------- |
| **RSpec**      | BDD testing 🏆 | `gem install rspec-rails` |
| **Minitest**   | Rails default  | Built-in                  |
| **Capybara**   | Integration    | `gem install capybara`    |
| **FactoryBot** | Test fixtures  | `gem install factory_bot` |

### Type Checking

| Tool       | Use Case         | Install              |
| ---------- | ---------------- | -------------------- |
| **Sorbet** | Static typing 🏆 | `gem install sorbet` |
| **RBS**    | Type signatures  | `gem install rbs`    |
| **Steep**  | Type checker     | `gem install steep`  |

---

## 🆕 Ruby 3.3/3.4 Features

### YJIT (Production Ready)

```ruby
# Enable YJIT for 15-25% performance boost
# In config/application.rb for Rails
RubyVM::YJIT.enable if defined?(RubyVM::YJIT)

# Or via environment
# RUBY_YJIT_ENABLE=1 rails server
```

### Pattern Matching (3.0+)

```ruby
# ✅ Hash pattern matching
case response
in { status: 200, body: }
  process_success(body)
in { status: 404 }
  handle_not_found
in { status: 500, error: message }
  log_error(message)
else
  handle_unknown
end

# ✅ Array pattern matching
case coordinates
in [x, y]
  Point2D.new(x, y)
in [x, y, z]
  Point3D.new(x, y, z)
end

# ✅ Guard clauses
case user
in { role: "admin" } if user.active?
  grant_admin_access
in { role: "user" }
  grant_user_access
end
```

### Data Class (3.2+)

```ruby
# ✅ Immutable value objects
User = Data.define(:id, :name, :email) do
  def display_name
    "#{name} <#{email}>"
  end
end

user = User.new(id: 1, name: "John", email: "john@example.com")
user.display_name  # => "John <john@example.com>"

# Immutable - raises FrozenError
user.name = "Jane"  # Error!
```

### Fiber Scheduler (Async I/O)

```ruby
require 'async'

Async do
  # Concurrent HTTP requests
  results = 3.times.map do |i|
    Async { fetch_data(i) }
  end.map(&:wait)
end
```

---

## 🚀 Rails 8 Best Practices

### Project Structure

```
app/
├── controllers/
│   └── api/
│       └── v1/
├── models/
│   └── concerns/
├── services/        # Business logic
├── queries/         # Complex queries
├── jobs/
├── mailers/
└── views/
    └── components/  # ViewComponent
config/
db/
├── migrate/
└── seeds/
spec/
├── models/
├── requests/
├── services/
└── factories/
```

### Service Object Pattern

```ruby
# app/services/users/create_service.rb
module Users
  class CreateService
    Result = Data.define(:success?, :user, :errors)

    def initialize(params:, current_user: nil)
      @params = params
      @current_user = current_user
    end

    def call
      user = User.new(user_params)

      if user.save
        notify_admin(user)
        Result.new(success?: true, user: user, errors: [])
      else
        Result.new(success?: false, user: nil, errors: user.errors.full_messages)
      end
    end

    private

    attr_reader :params, :current_user

    def user_params
      params.slice(:name, :email, :password)
    end

    def notify_admin(user)
      AdminMailer.new_user(user).deliver_later
    end
  end
end

# Controller usage
class UsersController < ApplicationController
  def create
    result = Users::CreateService.new(params: user_params).call

    if result.success?
      render json: result.user, status: :created
    else
      render json: { errors: result.errors }, status: :unprocessable_entity
    end
  end
end
```

### Query Object Pattern

```ruby
# app/queries/active_users_query.rb
class ActiveUsersQuery
  def initialize(relation = User.all)
    @relation = relation
  end

  def call(since: 30.days.ago, role: nil)
    scope = @relation
      .where("last_login_at > ?", since)
      .where.not(confirmed_at: nil)
      .order(last_login_at: :desc)

    scope = scope.where(role: role) if role
    scope
  end
end

# Usage
ActiveUsersQuery.new.call(since: 7.days.ago, role: "admin")
```

### Hotwire/Turbo Patterns

```ruby
# app/controllers/posts_controller.rb
class PostsController < ApplicationController
  def create
    @post = Post.new(post_params)

    respond_to do |format|
      if @post.save
        format.turbo_stream
        format.html { redirect_to @post }
      else
        format.turbo_stream { render turbo_stream: turbo_stream.replace("post_form", partial: "form") }
        format.html { render :new, status: :unprocessable_entity }
      end
    end
  end
end
```

```erb
<!-- app/views/posts/create.turbo_stream.erb -->
<%= turbo_stream.prepend "posts" do %>
  <%= render @post %>
<% end %>

<%= turbo_stream.update "post_form" do %>
  <%= render "form", post: Post.new %>
<% end %>
```

---

## 🔒 Sorbet Type Checking

```ruby
# typed: strict

class UserService
  extend T::Sig

  sig { params(id: Integer).returns(T.nilable(User)) }
  def find(id)
    User.find_by(id: id)
  end

  sig { params(params: T::Hash[Symbol, T.untyped]).returns(User) }
  def create!(params)
    User.create!(params)
  end

  sig { params(user: User, role: String).returns(T::Boolean) }
  def assign_role(user, role)
    user.update(role: role)
  end
end
```

---

## 🧪 RSpec Testing

```ruby
# spec/services/users/create_service_spec.rb
require 'rails_helper'

RSpec.describe Users::CreateService do
  describe '#call' do
    subject(:service) { described_class.new(params: params) }

    context 'with valid params' do
      let(:params) { attributes_for(:user) }

      it 'creates a user' do
        expect { service.call }.to change(User, :count).by(1)
      end

      it 'returns success result' do
        result = service.call
        expect(result).to be_success
        expect(result.user).to be_persisted
      end

      it 'sends admin notification' do
        expect { service.call }
          .to have_enqueued_mail(AdminMailer, :new_user)
      end
    end

    context 'with invalid params' do
      let(:params) { { email: 'invalid' } }

      it 'does not create a user' do
        expect { service.call }.not_to change(User, :count)
      end

      it 'returns failure result with errors' do
        result = service.call
        expect(result).not_to be_success
        expect(result.errors).to include(/Email/)
      end
    end
  end
end
```

---

## 📊 Performance Best Practices

### N+1 Query Prevention

```ruby
# ❌ Bad - N+1 queries
users = User.all
users.each { |u| puts u.posts.count }

# ✅ Good - Eager loading
users = User.includes(:posts).all
users.each { |u| puts u.posts.size }

# ✅ Good - Counter cache
class Post < ApplicationRecord
  belongs_to :user, counter_cache: true
end
# Add posts_count column to users table
```

### Caching

```ruby
# Fragment caching
<% cache @post do %>
  <%= render @post %>
<% end %>

# Low-level caching
Rails.cache.fetch("user_#{id}", expires_in: 1.hour) do
  User.find(id).to_json
end

# Russian doll caching
<% cache [@post, @post.comments.maximum(:updated_at)] do %>
  <%= render @post.comments %>
<% end %>
```

---

## ✅ Production Checklist

### Code Quality

- [ ] RuboCop linting passing
- [ ] Sorbet types (strict mode for critical paths)
- [ ] Brakeman security scan
- [ ] No N+1 queries (Bullet gem)

### Performance

- [ ] YJIT enabled
- [ ] Database indexes optimized
- [ ] Caching strategy implemented
- [ ] Background jobs for heavy tasks

### Testing

- [ ] RSpec coverage > 80%
- [ ] Request specs for all endpoints
- [ ] Factory Bot for test data
- [ ] CI/CD pipeline passing

### Security

- [ ] Strong parameters enforced
- [ ] CSRF protection enabled
- [ ] Secure headers configured
- [ ] Secrets in credentials

---

_DOMYH Awesome Code • Ruby 3.3/3.4 + Rails 8_
