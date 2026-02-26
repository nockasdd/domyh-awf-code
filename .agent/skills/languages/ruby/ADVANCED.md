# Ruby Advanced Patterns — DOMYH Awesome Code

> Deep dive into Ruby 3.3/3.4 advanced patterns

---

## 🔧 Metaprogramming Patterns

### Dynamic Method Definition

```ruby
class ApiClient
  ENDPOINTS = %w[users posts comments].freeze

  ENDPOINTS.each do |endpoint|
    define_method("fetch_#{endpoint}") do |id = nil|
      path = id ? "/#{endpoint}/#{id}" : "/#{endpoint}"
      get(path)
    end

    define_method("create_#{endpoint.chomp('s')}") do |params|
      post("/#{endpoint}", params)
    end
  end
end

client = ApiClient.new
client.fetch_users       # GET /users
client.fetch_users(1)    # GET /users/1
client.create_user(name: "John")  # POST /users
```

### Method Missing with Respond To

```ruby
class FlexibleHash
  def initialize(hash = {})
    @data = hash
  end

  def method_missing(name, *args, &block)
    key = name.to_s
    if key.end_with?("=")
      @data[key.chomp("=").to_sym] = args.first
    elsif @data.key?(name)
      @data[name]
    else
      super
    end
  end

  def respond_to_missing?(name, include_private = false)
    @data.key?(name) || name.to_s.end_with?("=") || super
  end
end
```

---

## 🔗 Concurrent Ruby Patterns

### Async/Await with Fibers

```ruby
require 'async'
require 'async/http/internet'

class AsyncHttpClient
  def fetch_all(urls)
    Async do
      internet = Async::HTTP::Internet.new

      tasks = urls.map do |url|
        Async do
          response = internet.get(url)
          { url: url, body: response.read, status: response.status }
        ensure
          response&.close
        end
      end

      tasks.map(&:wait)
    ensure
      internet&.close
    end
  end
end
```

### Thread Pool with Connection Pool

```ruby
require 'connection_pool'

class DatabasePool
  def initialize(size: 5)
    @pool = ConnectionPool.new(size: size, timeout: 5) do
      PG.connect(host: 'localhost', dbname: 'app')
    end
  end

  def query(sql, *params)
    @pool.with do |conn|
      conn.exec_params(sql, params)
    end
  end
end
```

---

## 🏗️ Domain-Driven Design

### Value Objects

```ruby
class Money
  include Comparable

  attr_reader :amount, :currency

  def initialize(amount, currency = "USD")
    @amount = BigDecimal(amount.to_s)
    @currency = currency.to_s.upcase
    freeze
  end

  def +(other)
    ensure_same_currency!(other)
    Money.new(amount + other.amount, currency)
  end

  def *(multiplier)
    Money.new(amount * multiplier, currency)
  end

  def <=>(other)
    ensure_same_currency!(other)
    amount <=> other.amount
  end

  def to_s
    "#{currency} #{amount.round(2)}"
  end

  private

  def ensure_same_currency!(other)
    raise ArgumentError, "Currency mismatch" unless currency == other.currency
  end
end
```

### Aggregate Root

```ruby
class Order
  include ActiveModel::Model

  attr_accessor :id, :customer_id, :status
  attr_reader :line_items, :events

  def initialize(attributes = {})
    super
    @line_items = []
    @events = []
    @status ||= :draft
  end

  def add_item(product_id:, quantity:, price:)
    raise InvalidStateError unless status == :draft

    item = LineItem.new(product_id: product_id, quantity: quantity, price: price)
    @line_items << item
    record_event(ItemAdded.new(order_id: id, item: item))
    item
  end

  def submit
    raise InvalidStateError unless status == :draft
    raise EmptyOrderError if line_items.empty?

    @status = :submitted
    record_event(OrderSubmitted.new(order_id: id, total: total))
  end

  def total
    line_items.sum(&:subtotal)
  end

  private

  def record_event(event)
    @events << event
  end
end
```

---

## 🔄 Railway-Oriented Programming

```ruby
module Result
  class Success
    attr_reader :value

    def initialize(value)
      @value = value
    end

    def success? = true
    def failure? = false

    def map
      Success.new(yield(value))
    rescue => e
      Failure.new(e.message)
    end

    def flat_map
      yield(value)
    rescue => e
      Failure.new(e.message)
    end

    def or_else(_) = self
  end

  class Failure
    attr_reader :error

    def initialize(error)
      @error = error
    end

    def success? = false
    def failure? = true

    def map = self
    def flat_map = self
    def or_else = yield(error)
  end
end

# Usage
def validate_user(params)
  return Result::Failure.new("Email required") if params[:email].blank?
  return Result::Failure.new("Name required") if params[:name].blank?
  Result::Success.new(params)
end

def create_user(params)
  user = User.create!(params)
  Result::Success.new(user)
rescue ActiveRecord::RecordInvalid => e
  Result::Failure.new(e.message)
end

def send_welcome_email(user)
  UserMailer.welcome(user).deliver_later
  Result::Success.new(user)
end

# Pipeline
result = validate_user(params)
  .flat_map { |p| create_user(p) }
  .flat_map { |u| send_welcome_email(u) }

case result
when Result::Success
  render json: result.value
when Result::Failure
  render json: { error: result.error }, status: :unprocessable_entity
end
```

---

## 🔒 Advanced Sorbet Types

```ruby
# typed: strict
require 'sorbet-runtime'

module Types
  Email = T.type_alias { String }
  UserId = T.type_alias { Integer }

  class UserParams < T::Struct
    const :name, String
    const :email, Email
    const :role, T.nilable(String), default: nil
  end
end

class UserRepository
  extend T::Sig
  extend T::Generic

  Entity = type_member { { fixed: User } }

  sig { params(id: Types::UserId).returns(T.nilable(User)) }
  def find(id)
    User.find_by(id: id)
  end

  sig { params(params: Types::UserParams).returns(User) }
  def create!(params)
    User.create!(params.serialize)
  end

  sig { params(scope: T.proc.params(q: User::ActiveRecord_Relation).returns(User::ActiveRecord_Relation)).returns(T::Array[User]) }
  def where(&scope)
    scope.call(User.all).to_a
  end
end
```

---

## ⚡ Performance Optimization

### Batch Processing

```ruby
class BatchProcessor
  BATCH_SIZE = 1000

  def process_users
    User.find_in_batches(batch_size: BATCH_SIZE) do |batch|
      batch.each { |user| process_user(user) }
    end
  end

  # Even better with pluck for read-only
  def export_emails
    User.active.pluck(:id, :email).each do |id, email|
      yield(id, email)
    end
  end

  # Bulk insert
  def import_users(data)
    records = data.map { |d| { name: d[:name], email: d[:email], created_at: Time.current } }
    User.insert_all(records)
  end

  # Bulk update
  def deactivate_old_users
    User.where("last_login_at < ?", 1.year.ago).update_all(active: false)
  end
end
```

### Memoization Patterns

```ruby
class ExpensiveCalculation
  def result
    @result ||= compute_expensive_value
  end

  # With arguments
  def calculate(n)
    @cache ||= {}
    @cache[n] ||= expensive_computation(n)
  end

  # Thread-safe memoization
  def thread_safe_result
    return @result if defined?(@result)
    @mutex ||= Mutex.new
    @mutex.synchronize { @result ||= compute_expensive_value }
  end
end
```

---
