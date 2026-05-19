---
library: ruby-on-rails
version: 8.x
latest: true
category: backend
official_docs: https://guides.rubyonrails.org
last_updated: 2026-03-21
source: auto-fetched from github-dir
source_url: https://api.github.com/repos/rails/rails/contents/guides/source
---

#### `config.after_initialize`

Takes a block which will be run _after_ Rails has finished initializing the application. That includes the initialization of the framework itself, engines, and all the application's initializers in `config/initializers`. Note that this block _will_ be run for rake tasks. Useful for configuring values set up by other initializers:

```ruby
config.after_initialize do
  ActionView::Base.sanitized_allowed_tags.delete "div"
end
```


# use ActionDispatch::Session::MyCustomStore as the session store
config.session_store :my_custom_store
```

The default store is a cookie store with the application name as the session key.


# and follow the adapter's specific installation

### `Rails::Railtie#initializer`

Rails has several initializers that run on startup that are all defined by using the `initializer` method from `Rails::Railtie`. Here's an example of the `set_helpers_path` initializer from Action Controller:

```ruby
initializer "action_controller.set_helpers_path" do |app|
  ActionController::Helpers.helpers_path = app.helpers_paths
end
```

The `initializer` method takes three arguments with the first being the name for the initializer and the second being an options hash (not shown here) and the third being a block. The `:before` key in the options hash can be specified to specify which initializer this new initializer must run before, and the `:after` key will specify which initializer to run this initializer _after_.

Initializers defined using the `initializer` method will be run in the order they are defined in, with the exception of ones that use the `:before` or `:after` methods.

WARNING: You may put your initializer before or after any other initializer in the chain, as long as it is logical. Say you have 4 initializers called "one" through "four" (defined in that order) and you define "four" to go _before_ "two" but _after_ "three", that just isn't logical and Rails will not be able to determine your initializer order.

The block argument of the `initializer` method is the instance of the application itself, and so we can access the configuration on it by using the `config` method as done in the example.

Because `Rails::Application` inherits from `Rails::Railtie` (indirectly), you can use the `initializer` method in `config/application.rb` to define initializers for the application.


### Initializers

Below is a comprehensive list of all the initializers found in Rails in the order that they are defined (and therefore run in, unless otherwise stated).

* `load_environment_hook`: Serves as a placeholder so that `:load_environment_config` can be defined to run before it.

* `load_active_support`: Optionally requires `active_support/all` if `config.active_support.bare` is un-truthful, which is the default.

* `initialize_logger`: Initializes the logger (an `ActiveSupport::BroadcastLogger` object) for the application and makes it accessible at `Rails.logger`, provided that no initializer inserted before this point has defined `Rails.logger`.

* `initialize_cache`: If `Rails.cache` isn't set yet, initializes the cache by referencing the value in `config.cache_store` and stores the outcome as `Rails.cache`. If this object responds to the `middleware` method, its middleware is inserted before `Rack::Runtime` in the middleware stack.

* `set_clear_dependencies_hook`: This initializer - which runs only if `config.enable_reloading` is set to `true` - uses `ActionDispatch::Callbacks.after` to remove the constants which have been referenced during the request from the object space so that they will be reloaded during the following request.

* `bootstrap_hook`: Runs all configured `before_initialize` blocks.

* `i18n.callbacks`: In the development environment, sets up a `to_prepare` callback which will call `I18n.reload!` if any of the locales have changed since the last request. In production this callback will only run on the first request.

* `active_support.deprecation_behavior`: Sets up deprecation reporting behavior for [`Rails.application.deprecators`][] based on [`config.active_support.report_deprecations`](#config-active-support-report-deprecations), [`config.active_support.deprecation`](#config-active-support-deprecation), [`config.active_support.disallowed_deprecation`](#config-active-support-disallowed-deprecation), and [`config.active_support.disallowed_deprecation_warnings`](#config-active-support-disallowed-deprecation-warnings).

* `active_support.initialize_time_zone`: Sets the default time zone for the application based on the `config.time_zone` setting, which defaults to "UTC".

* `active_support.initialize_beginning_of_week`: Sets the default beginning of week for the application based on `config.beginning_of_week` setting, which defaults to `:monday`.

* `active_support.set_configs`: Sets up Active Support by using the settings in `config.active_support` by `send`'ing the method names as setters to `ActiveSupport` and passing the values through.

* `action_dispatch.configure`: Configures the `ActionDispatch::Http::URL.tld_length` to be set to the value of `config.action_dispatch.tld_length`.

* `action_view.set_configs`: Sets up Action View by using the settings in `config.action_view` by `send`'ing the method names as setters to `ActionView::Base` and passing the values through.

* `action_controller.assets_config`: Initializes the `config.action_controller.assets_dir` to the app's public directory if not explicitly configured.

* `action_controller.set_helpers_path`: Sets Action Controller's `helpers_path` to the application's `helpers_path`.

* `action_controller.parameters_config`: Configures strong parameters options for `ActionController::Parameters`.

* `action_controller.set_configs`: Sets up Action Controller by using the settings in `config.action_controller` by `send`'ing the method names as setters to `ActionController::Base` and passing the values through.

* `action_controller.compile_config_methods`: Initializes methods for the config settings specified so that they are quicker to access.

* `active_record.initialize_timezone`: Sets `ActiveRecord::Base.time_zone_aware_attributes` to `true`, as well as setting `ActiveRecord::Base.default_timezone` to UTC. When attributes are read from the database, they will be converted into the time zone specified by `Time.zone`.

* `active_record.logger`: Sets `ActiveRecord::Base.logger` - if it's not already set - to `Rails.logger`.

* `active_record.migration_error`: Configures middleware to check for pending migrations.

* `active_record.check_schema_cache_dump`: Loads the schema cache dump if configured and available.

* `active_record.set_configs`: Sets up Active Record by using the settings in `config.active_record` by `send`'ing the method names as setters to `ActiveRecord::Base` and passing the values through.

* `active_record.initialize_database`: Loads the database configuration (by default) from `config/database.yml` and establishes a connection for the current environment.

* `active_record.log_runtime`: Includes `ActiveRecord::Railties::ControllerRuntime` and `ActiveRecord::Railties::JobRuntime` which are responsible for reporting the time taken by Active Record calls for the request back to the logger.

* `active_record.set_reloader_hooks`: Resets all reloadable connections to the database if `config.enable_reloading` is set to `true`.

* `active_record.add_watchable_files`: Adds `schema.rb` and `structure.sql` files to watchable files.

* `active_job.logger`: Sets `ActiveJob::Base.logger` - if it's not already set -
  to `Rails.logger`.

* `active_job.set_configs`: Sets up Active Job by using the settings in `config.active_job` by `send`'ing the method names as setters to `ActiveJob::Base` and passing the values through.

* `action_mailer.logger`: Sets `ActionMailer::Base.logger` - if it's not already set - to `Rails.logger`.

* `action_mailer.set_configs`: Sets up Action Mailer by using the settings in `config.action_mailer` by `send`'ing the method names as setters to `ActionMailer::Base` and passing the values through.

* `action_mailer.compile_config_methods`: Initializes methods for the config settings specified so that they are quicker to access.

* `set_load_path`: This initializer runs before `bootstrap_hook`. Adds paths
  specified by `config.paths.load_paths` to `$LOAD_PATH`. And unless you set
  `config.add_autoload_paths_to_load_path` to `false`, it will also add all
  autoload paths specified by `config.autoload_paths`,
  `config.eager_load_paths`, `config.autoload_once_paths`.

* `set_autoload_paths`: This initializer runs before `bootstrap_hook`. Adds all sub-directories of `app` and paths specified by `config.autoload_paths`, `config.eager_load_paths` and `config.autoload_once_paths` to `ActiveSupport::Dependencies.autoload_paths`.

* `add_routing_paths`: Loads (by default) all `config/routes.rb` files (in the application and railties, including engines) and sets up the routes for the application.

* `add_locales`: Adds the files in `config/locales` (from the application, railties, and engines) to `I18n.load_path`, making available the translations in these files.

* `add_view_paths`: Adds the directory `app/views` from the application, railties, and engines to the lookup path for view files for the application.

* `add_mailer_preview_paths`: Adds the directory `test/mailers/previews` from the application, railties, and engines to the lookup path for mailer preview files for the application.

* `load_environment_config`: This initializer runs before `load_environment_hook`. Loads the `config/environments` file for the current environment.

* `prepend_helpers_path`: Adds the directory `app/helpers` from the application, railties, and engines to the lookup path for helpers for the application.

* `load_config_initializers`: Loads all Ruby files from `config/initializers` in the application, railties, and engines. The files in this directory can be used to hold configuration settings that should be made after all of the frameworks are loaded.

* `engines_blank_point`: Provides a point-in-initialization to hook into if you wish to do anything before engines are loaded. After this point, all railtie and engine initializers are run.

* `add_generator_templates`: Finds templates for generators at `lib/templates` for the application, railties, and engines, and adds these to the `config.generators.templates` setting, which will make the templates available for all generators to reference.

* `ensure_autoload_once_paths_as_subset`: Ensures that the `config.autoload_once_paths` only contains paths from `config.autoload_paths`. If it contains extra paths, then an exception will be raised.

* `add_to_prepare_blocks`: The block for every `config.to_prepare` call in the application, a railtie, or engine is added to the `to_prepare` callbacks for Action Dispatch which will be run per request in development, or before the first request in production.

* `add_builtin_route`: If the application is running under the development environment then this will append the route for `rails/info/properties` to the application routes. This route provides the detailed information such as Rails and Ruby version for `public/index.html` in a default Rails application.

* `build_middleware_stack`: Builds the middleware stack for the application, returning an object which has a `call` method which takes a Rack environment object for the request.

* `eager_load!`: If `config.eager_load` is `true`, runs the `config.before_eager_load` hooks and then calls `eager_load!` which will load all `config.eager_load_namespaces`.

* `finisher_hook`: Provides a hook for after the initialization of process of the application is complete, as well as running all the `config.after_initialize` blocks for the application, railties, and engines.

* `set_routes_reloader_hook`: Configures Action Dispatch to reload the routes file using `ActiveSupport::Callbacks.to_run`.

* `disable_dependency_loading`: Disables the automatic dependency loading if the `config.eager_load` is set to `true`.

[`Rails.application.deprecators`]: https://api.rubyonrails.org/classes/Rails/Application.html#method-i-deprecators

Database Pooling
----------------

Active Record database connections are managed by [`ActiveRecord::ConnectionAdapters::ConnectionPool`][] which ensures that a connection pool synchronizes the amount of thread access to a limited number of database connections. This limit defaults to 5 and can be configured in `database.yml`.

```yaml
development:
  adapter: sqlite3
  database: storage/development.sqlite3
  pool: 5
  timeout: 5000
```

Since the connection pooling is handled inside of Active Record by default, all application servers (Thin, Puma, Unicorn, etc.) should behave the same. The database connection pool is initially empty. As demand for connections increases it will create them until it reaches the connection pool limit.

Any one request will check out a connection the first time it requires access to the database. At the end of the request it will check the connection back in. This means that the additional connection slot will be available again for the next request in the queue.

If you try to use more connections than are available, Active Record will block
you and wait for a connection from the pool. If it cannot get a connection, a
timeout error similar to that given below will be thrown.

```
ActiveRecord::ConnectionTimeoutError - could not obtain a database connection within 5.000 seconds (waited 5.000 seconds)
```

If you get the above error, you might want to increase the size of the
connection pool by incrementing the `pool` option in `database.yml`

NOTE. If you are running in a multi-threaded environment, there could be a chance that several threads may be accessing multiple connections simultaneously. So depending on your current request load, you could very well have multiple threads contending for a limited number of connections.

[`ActiveRecord::ConnectionAdapters::ConnectionPool`]: https://api.rubyonrails.org/classes/ActiveRecord/ConnectionAdapters/ConnectionPool.html

Custom Configuration
--------------------

You can configure your own code through the Rails configuration object with
custom configuration under either the `config.x` namespace, or `config` directly.
The key difference between these two is that you should be using `config.x` if you
are defining _nested_ configuration (ex: `config.x.nested.hi`), and just
`config` for _single level_ configuration (ex: `config.hello`).

```ruby
config.x.payment_processing.schedule = :daily
config.x.payment_processing.retries  = 3
config.super_debugger = true
```

These configuration points are then available through the configuration object:

```ruby
Rails.configuration.x.payment_processing.schedule # => :daily
Rails.configuration.x.payment_processing.retries  # => 3
Rails.configuration.x.payment_processing.not_set  # => nil
Rails.configuration.super_debugger                # => true
```

You can also use `Rails::Application.config_for` to load whole configuration files:

```yaml

#### Cherry-picking a Definition

This example shows how to load [`Hash#with_indifferent_access`][Hash#with_indifferent_access].  This extension enables the conversion of a `Hash` into an [`ActiveSupport::HashWithIndifferentAccess`][ActiveSupport::HashWithIndifferentAccess] which permits access to the keys as either strings or symbols.

```ruby
{ a: 1 }.with_indifferent_access["a"] # => 1
```

For every single method defined as a core extension this guide has a note that says where such a method is defined. In the case of `with_indifferent_access` the note reads:

NOTE: Defined in `active_support/core_ext/hash/indifferent_access.rb`.

That means that you can require it like this:

```ruby
require "active_support"
require "active_support/core_ext/hash/indifferent_access"
```

Active Support has been carefully revised so that cherry-picking a file loads only strictly needed dependencies, if any.


### Autoloading during initialization

Applications that autoloaded reloadable constants during initialization outside of `to_prepare` blocks got those constants unloaded and had this warning issued since Rails 6.0:

```
DEPRECATION WARNING: Initialization autoloaded the constant ....

Being able to do this is deprecated. Autoloading during initialization is going
to be an error condition in future versions of Rails.

...
```

If you still get this warning in the logs, please check the section about autoloading when the application boots in the [autoloading guide](https://guides.rubyonrails.org/v7.0/autoloading_and_reloading_constants.html#autoloading-when-the-application-boots). You'd get a `NameError` in Rails 7 otherwise.

Constants managed by the `once` autoloader can be autoloaded during initialization, and they can be used normally, no need for a `to_prepare` block. However, the `once` autoloader is now set up earlier to support that. If the application has custom inflections, and the `once` autoloader should be aware of them, you need to move the code in `config/initializers/inflections.rb` to the body of the application class definition in `config/application.rb`:

```ruby
module MyApp
  class Application < Rails::Application
    # ...

    ActiveSupport::Inflector.inflections(:en) do |inflect|
      inflect.acronym "HTML"
    end
  end
end
```


# config/initializers/cookie_rotator.rb
Rails.application.config.after_initialize do
  Rails.application.config.action_dispatch.cookies_rotations.tap do |cookies|
    authenticated_encrypted_cookie_salt = Rails.application.config.action_dispatch.authenticated_encrypted_cookie_salt
    signed_cookie_salt = Rails.application.config.action_dispatch.signed_cookie_salt

    secret_key_base = Rails.application.secret_key_base

    key_generator = ActiveSupport::KeyGenerator.new(
      secret_key_base, iterations: 1000, hash_digest_class: OpenSSL::Digest::SHA1
    )
    key_len = ActiveSupport::MessageEncryptor.key_len

    old_encrypted_secret = key_generator.generate_key(authenticated_encrypted_cookie_salt, key_len)
    old_signed_secret = key_generator.generate_key(signed_cookie_salt)

    cookies.rotate :encrypted, old_encrypted_secret
    cookies.rotate :signed, old_signed_secret
  end
end
```


# incrementally modify your database, and then regenerate this schema definition.
#

#### Qualified names in class and module definitions

You can now robustly use constant paths in class and module definitions:

```ruby

# config/initializers/json_patch.rb
Mime::Type.register "application/json-patch+json", :json_patch
```

As JSON Patch was only recently made into an RFC, there aren't a lot of great
Ruby libraries yet. Aaron Patterson's
[hana](https://github.com/tenderlove/hana) is one such gem, but doesn't have
full support for the last few changes in the specification.


### config/initializers/wrap_parameters.rb

Add this file with the following contents, if you wish to wrap parameters into a nested hash. This is on by default in new applications.

```ruby

### config/initializers/session_store.rb

You need to change your session key to something new, or remove all sessions:

```ruby

# in config/initializers/session_store.rb
AppName::Application.config.session_store :cookie_store, key: "SOMETHINGNEW"
```

or

```bash
$ bin/rake db:sessions:clear
```


### Test Setup

Rails creates a `test` directory for you as soon as you create a Rails project
using `bin/rails new` _application_name_. If you list the contents of this directory
then you will see:

```bash
$ ls -F test
controllers/  fixtures/  helpers/  integration/  mailers/  models/  test_helper.rb
```


### Prerequisites

For this project, you will need:

* Ruby 3.3 or newer
* Rails 8.2.0 or newer
* A code editor

Follow the [Install Ruby on Rails Guide](install_ruby_on_rails.html) if you need
to install Ruby and/or Rails.

Let's verify the correct version of Rails is installed. To display the current
version, open a terminal and run the following. You should see a version number
printed out:

```bash
$ rails --version
Rails 8.2.0
```

The version shown should be Rails 8.2.0 or higher.


### Core Engine Setup


#### The Engine Class Definition: `lib/blorgh/engine.rb`

This file defines the engine class and tells Rails how to load and isolate it:

```ruby

# config/initializers/locale.rb


# Install the pg driver:

#   gem install pg

#   gem install pg -- --with-pg-config=/usr/local/bin/pg_config

#   gem install pg
