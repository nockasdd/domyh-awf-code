---
library: nodejs
version: 22.x
latest: true
category: runtime
official_docs: https://nodejs.org/docs
last_updated: 2026-03-21
source: auto-fetched from github-dir
source_url: https://api.github.com/repos/nodejs/node/contents/doc/api
---

# File system

<!--introduced_in=v0.10.0-->

> Stability: 2 - Stable

<!--name=fs-->

<!-- source_link=lib/fs.js -->

The `node:fs` module enables interacting with the file system in a
way modeled on standard POSIX functions.

To use the promise-based APIs:

```mjs
import * as fs from 'node:fs/promises';
```

```cjs
const fs = require('node:fs/promises');
```

To use the callback and sync APIs:

```mjs
import * as fs from 'node:fs';
```

```cjs
const fs = require('node:fs');
```

All file system operations have synchronous, callback, and promise-based
forms, and are accessible using both CommonJS syntax and ES6 Modules (ESM).


## Promises API

<!-- YAML
added: v10.0.0
changes:
  - version: v14.0.0
    pr-url: https://github.com/nodejs/node/pull/31553
    description: Exposed as `require('fs/promises')`.
  - version:
    - v11.14.0
    - v10.17.0
    pr-url: https://github.com/nodejs/node/pull/26581
    description: This API is no longer experimental.
  - version: v10.1.0
    pr-url: https://github.com/nodejs/node/pull/20504
    description: The API is accessible via `require('fs').promises` only.
-->

The `fs/promises` API provides asynchronous file system methods that return
promises.

The promise APIs use the underlying Node.js threadpool to perform file
system operations off the event loop thread. These operations are not
synchronized or threadsafe. Care must be taken when performing multiple
concurrent modifications on the same file or data corruption may occur.


## Callback API

The callback APIs perform all operations asynchronously, without blocking the
event loop, then invoke a callback function upon completion or error.

The callback APIs use the underlying Node.js threadpool to perform file
system operations off the event loop thread. These operations are not
synchronized or threadsafe. Care must be taken when performing multiple
concurrent modifications on the same file or data corruption may occur.


## Synchronous API

The synchronous APIs perform all operations synchronously, blocking the
event loop until the operation completes or fails.


## n api


# Node-API

<!--introduced_in=v8.0.0-->

<!-- type=misc -->

> Stability: 2 - Stable

Node-API (formerly N-API) is an API for building native Addons. It is
independent from the underlying JavaScript runtime (for example, V8) and is
maintained as part of Node.js itself. This API will be Application Binary
Interface (ABI) stable across versions of Node.js. It is intended to insulate
addons from changes in the underlying JavaScript engine and allow modules
compiled for one major version to run on later major versions of Node.js without
recompilation. The [ABI Stability][] guide provides a more in-depth explanation.

Addons are built/packaged with the same approach/tools outlined in the section
titled [C++ Addons][]. The only difference is the set of APIs that are used by
the native code. Instead of using the V8 or [Native Abstractions for Node.js][]
APIs, the functions available in Node-API are used.

APIs exposed by Node-API are generally used to create and manipulate
JavaScript values. Concepts and operations generally map to ideas specified
in the ECMA-262 Language Specification. The APIs have the following
properties:

* All Node-API calls return a status code of type `napi_status`. This
  status indicates whether the API call succeeded or failed.
* The API's return value is passed via an out parameter.
* All JavaScript values are abstracted behind an opaque type named
  `napi_value`.
* In case of an error status code, additional information can be obtained
  using `napi_get_last_error_info`. More information can be found in the error
  handling section [Error handling][].


## Environment life cycle APIs

[Section Agents][] of the [ECMAScript Language Specification][] defines the concept
of an "Agent" as a self-contained environment in which JavaScript code runs.
Multiple such Agents may be started and terminated either concurrently or in
sequence by the process.

A Node.js environment corresponds to an ECMAScript Agent. In the main process,
an environment is created at startup, and additional environments can be created
on separate threads to serve as [worker threads][]. When Node.js is embedded in
another application, the main thread of the application may also construct and
destroy a Node.js environment multiple times during the life cycle of the
application process such that each Node.js environment created by the
application may, in turn, during its life cycle create and destroy additional
environments as worker threads.

From the perspective of a native addon this means that the bindings it provides
may be called multiple times, from multiple contexts, and even concurrently from
multiple threads.

Native addons may need to allocate global state which they use during
their life cycle of an Node.js environment such that the state can be
unique to each instance of the addon.

To this end, Node-API provides a way to associate data such that its life cycle
is tied to the life cycle of a Node.js environment.


### `napi_set_instance_data`

<!-- YAML
added:
 - v12.8.0
 - v10.20.0
napiVersion: 6
-->

```c
napi_status napi_set_instance_data(node_api_basic_env env,
                                   void* data,
                                   napi_finalize finalize_cb,
                                   void* finalize_hint);
```

* `[in] env`: The environment that the Node-API call is invoked under.
* `[in] data`: The data item to make available to bindings of this instance.
* `[in] finalize_cb`: The function to call when the environment is being torn
  down. The function receives `data` so that it might free it.
  [`napi_finalize`][] provides more details.
* `[in] finalize_hint`: Optional hint to pass to the finalize callback during
  collection.

Returns `napi_ok` if the API succeeded.

This API associates `data` with the currently running Node.js environment. `data`
can later be retrieved using `napi_get_instance_data()`. Any existing data
associated with the currently running Node.js environment which was set by means
of a previous call to `napi_set_instance_data()` will be overwritten. If a
`finalize_cb` was provided by the previous call, it will not be called.


### `napi_get_instance_data`

<!-- YAML
added:
 - v12.8.0
 - v10.20.0
napiVersion: 6
-->

```c
napi_status napi_get_instance_data(node_api_basic_env env,
                                   void** data);
```

* `[in] env`: The environment that the Node-API call is invoked under.
* `[out] data`: The data item that was previously associated with the currently
  running Node.js environment by a call to `napi_set_instance_data()`.

Returns `napi_ok` if the API succeeded.

This API retrieves data that was previously associated with the currently
running Node.js environment via `napi_set_instance_data()`. If no data is set,
the call will succeed and `data` will be set to `NULL`.


## Basic Node-API data types

Node-API exposes the following fundamental data types as abstractions that are
consumed by the various APIs. These APIs should be treated as opaque,
introspectable only with other Node-API calls.


### `napi_status`

<!-- YAML
added: v8.0.0
napiVersion: 1
-->

Integral status code indicating the success or failure of a Node-API call.
Currently, the following status codes are supported.

```c
typedef enum {
  napi_ok,
  napi_invalid_arg,
  napi_object_expected,
  napi_string_expected,
  napi_name_expected,
  napi_function_expected,
  napi_number_expected,
  napi_boolean_expected,
  napi_array_expected,
  napi_generic_failure,
  napi_pending_exception,
  napi_cancelled,
  napi_escape_called_twice,
  napi_handle_scope_mismatch,
  napi_callback_scope_mismatch,
  napi_queue_full,
  napi_closing,
  napi_bigint_expected,
  napi_date_expected,
  napi_arraybuffer_expected,
  napi_detachable_arraybuffer_expected,
  napi_would_deadlock,  /* unused */
  napi_no_external_buffers_allowed,
  napi_cannot_run_js
} napi_status;
```

If additional information is required upon an API returning a failed status,
it can be obtained by calling `napi_get_last_error_info`.


### `napi_extended_error_info`

<!-- YAML
added: v8.0.0
napiVersion: 1
-->

```c
typedef struct {
  const char* error_message;
  void* engine_reserved;
  uint32_t engine_error_code;
  napi_status error_code;
} napi_extended_error_info;
```

* `error_message`: UTF8-encoded string containing a VM-neutral description of
  the error.
* `engine_reserved`: Reserved for VM-specific error details. This is currently
  not implemented for any VM.
* `engine_error_code`: VM-specific error code. This is currently
  not implemented for any VM.
* `error_code`: The Node-API status code that originated with the last error.

See the [Error handling][] section for additional information.


### `napi_env`

`napi_env` is used to represent a context that the underlying Node-API
implementation can use to persist VM-specific state. This structure is passed
to native functions when they're invoked, and it must be passed back when
making Node-API calls. Specifically, the same `napi_env` that was passed in when
the initial native function was called must be passed to any subsequent
nested Node-API calls. Caching the `napi_env` for the purpose of general reuse,
and passing the `napi_env` between instances of the same addon running on
different [`Worker`][] threads is not allowed. The `napi_env` becomes invalid
when an instance of a native addon is unloaded. Notification of this event is
delivered through the callbacks given to [`napi_add_env_cleanup_hook`][] and
[`napi_set_instance_data`][].


### `napi_value`

This is an opaque pointer that is used to represent a JavaScript value.


### `napi_threadsafe_function`

<!-- YAML
added: v10.6.0
napiVersion: 4
-->

This is an opaque pointer that represents a JavaScript function which can be
called asynchronously from multiple threads via
`napi_call_threadsafe_function()`.


### `napi_threadsafe_function_call_mode`

<!-- YAML
added: v10.6.0
napiVersion: 4
-->

A value to be given to `napi_call_threadsafe_function()` to indicate whether
the call should block whenever the queue associated with the thread-safe
function is full.

```c
typedef enum {
  napi_tsfn_nonblocking,
  napi_tsfn_blocking
} napi_threadsafe_function_call_mode;
```


### Node-API memory management types


### Node-API callback types


### Object creation functions


### Functions to get global instances


### `napi_async_init`

<!-- YAML
added: v8.6.0
napiVersion: 1
changes:
  - version: v25.0.0
    pr-url: https://github.com/nodejs/node/pull/59828
    description: The `async_resource` object will now be held as a strong reference.
-->

```c
napi_status napi_async_init(napi_env env,
                            napi_value async_resource,
                            napi_value async_resource_name,
                            napi_async_context* result)
```

* `[in] env`: The environment that the API is invoked under.
* `[in] async_resource`: Object associated with the async work
  that will be passed to possible `async_hooks` [`init` hooks][] and can be
  accessed by [`async_hooks.executionAsyncResource()`][].
* `[in] async_resource_name`: Identifier for the kind of resource that is being
  provided for diagnostic information exposed by the `async_hooks` API.
* `[out] result`: The initialized async context.

Returns `napi_ok` if the API succeeded.

In order to retain ABI compatibility with previous versions, passing `NULL`
for `async_resource` does not result in an error. However, this is not
recommended as this will result in undesirable behavior with  `async_hooks`
[`init` hooks][] and `async_hooks.executionAsyncResource()` as the resource is
now required by the underlying `async_hooks` implementation in order to provide
the linkage between async callbacks.

Previous versions of this API were not maintaining a strong reference to
`async_resource` while the `napi_async_context` object existed and instead
expected the caller to hold a strong reference. This has been changed, as a
corresponding call to [`napi_async_destroy`][] for every call to
`napi_async_init()` is a requirement in any case to avoid memory leaks.


## Global setup and teardown

<!-- YAML
added: v24.0.0
-->

> Stability: 1.0 - Early development

The test runner supports specifying a module that will be evaluated before all tests are executed and
can be used to setup global state or fixtures for tests. This is useful for preparing resources or setting up
shared state that is required by multiple tests.

This module can export any of the following:

* A `globalSetup` function which runs once before all tests start
* A `globalTeardown` function which runs once after all tests complete

The module is specified using the `--test-global-setup` flag when running tests from the command line.

```cjs
// setup-module.js
async function globalSetup() {
  // Setup shared resources, state, or environment
  console.log('Global setup executed');
  // Run servers, create files, prepare databases, etc.
}

async function globalTeardown() {
  // Clean up resources, state, or environment
  console.log('Global teardown executed');
  // Close servers, remove files, disconnect from databases, etc.
}

module.exports = { globalSetup, globalTeardown };
```

```mjs
// setup-module.mjs
export async function globalSetup() {
  // Setup shared resources, state, or environment
  console.log('Global setup executed');
  // Run servers, create files, prepare databases, etc.
}

export async function globalTeardown() {
  // Clean up resources, state, or environment
  console.log('Global teardown executed');
  // Close servers, remove files, disconnect from databases, etc.
}
```

If the global setup function throws an error, no tests will be run and the process will exit with a non-zero exit code.
The global teardown function will not be called in this case.


### `request.setSocketKeepAlive([enable][, initialDelay])`

<!-- YAML
added: v0.5.9
-->

* `enable` {boolean}
* `initialDelay` {number}

Once a socket is assigned to this request and is connected
[`socket.setKeepAlive()`][] will be called.


## `process.initgroups(user, extraGroup)`

<!-- YAML
added: v0.9.4
-->

* `user` {string|number} The user name or numeric identifier.
* `extraGroup` {string|number} A group name or numeric identifier.

The `process.initgroups()` method reads the `/etc/group` file and initializes
the group access list, using all groups of which the user is a member. This is
a privileged operation that requires that the Node.js process either have `root`
access or the `CAP_SETGID` capability.

Use care when dropping privileges:

```mjs
import { getgroups, initgroups, setgid } from 'node:process';

console.log(getgroups());         // [ 0 ]
initgroups('nodeuser', 1000);     // switch user
console.log(getgroups());         // [ 27, 30, 46, 1000, 0 ]
setgid(1000);                     // drop root gid
console.log(getgroups());         // [ 27, 30, 46, 1000 ]
```

```cjs
const { getgroups, initgroups, setgid } = require('node:process');

console.log(getgroups());         // [ 0 ]
initgroups('nodeuser', 1000);     // switch user
console.log(getgroups());         // [ 27, 30, 46, 1000, 0 ]
setgid(1000);                     // drop root gid
console.log(getgroups());         // [ 27, 30, 46, 1000 ]
```

This function is only available on POSIX platforms (i.e. not Windows or
Android).
This feature is not available in [`Worker`][] threads.


# Run snapshot.js to initialize the application and snapshot the

### `--test-global-setup=module`

<!-- YAML
added: v24.0.0
-->

> Stability: 1.0 - Early development

Specify a module that will be evaluated before all tests are executed and
can be used to setup global state or fixtures for tests.

See the documentation on [global setup and teardown][] for more details.


### `ERR_CONTEXT_NOT_INITIALIZED`

The vm context passed into the API is not yet initialized. This could happen
when an error occurs (and is caught) during the creation of the
context, for example, when the allocation fails or the maximum call stack
size is reached when the context is created.

<a id="ERR_CPU_PROFILE_ALREADY_STARTED"></a>


### `ERR_CRYPTO_INITIALIZATION_FAILED`

<!-- YAML
added: v15.0.0
-->

Initialization of the crypto subsystem failed.

<a id="ERR_CRYPTO_INVALID_AUTH_TAG"></a>


### `ERR_CRYPTO_JOB_INIT_FAILED`

<!-- YAML
added: v15.0.0
-->

Initialization of an asynchronous crypto operation failed.

<a id="ERR_CRYPTO_JWK_UNSUPPORTED_CURVE"></a>


### `ERR_TTY_INIT_FAILED`

The initialization of a TTY failed due to a system error.

<a id="ERR_UNAVAILABLE_DURING_EXIT"></a>


### `ERR_WORKER_INIT_FAILED`

The `Worker` initialization failed.

<a id="ERR_WORKER_INVALID_EXEC_ARGV"></a>


### `ERR_ZLIB_INITIALIZATION_FAILED`

Creation of a [`zlib`][] object failed due to incorrect configuration.

<a id="ERR_ZSTD_INVALID_PARAM"></a>


### Client-initiated renegotiation attack mitigation

<!-- type=misc -->

The TLS protocol allows clients to renegotiate certain aspects of the TLS
session. Unfortunately, session renegotiation requires a disproportionate amount
of server-side resources, making it a potential vector for denial-of-service
attacks.

To mitigate the risk, renegotiation is limited to three times every ten minutes.
An `'error'` event is emitted on the [`tls.TLSSocket`][] instance when this
threshold is exceeded. The limits are configurable:

* `tls.CLIENT_RENEG_LIMIT` {number} Specifies the number of renegotiation
  requests. **Default:** `3`.
* `tls.CLIENT_RENEG_WINDOW` {number} Specifies the time renegotiation window
  in seconds. **Default:** `600` (10 minutes).

The default renegotiation limits should not be modified without a full
understanding of the implications and risks.

TLSv1.3 does not support renegotiation.


#### `initialize()`

<!-- YAML
added:
  - v20.6.0
  - v18.19.0
-->

* `data` {any} The data from `register(loader, import.meta.url, { data })`.

The `initialize` hook is only accepted by [`register`][]. `registerHooks()` does
not support nor need it since initialization done for synchronous hooks can be run
directly before the call to `registerHooks()`.

The `initialize` hook provides a way to define a custom function that runs in
the hooks thread when the hooks module is initialized. Initialization happens
when the hooks module is registered via [`register`][].

This hook can receive data from a [`register`][] invocation, including
ports and other transferable objects. The return value of `initialize` can be a
{Promise}, in which case it will be awaited before the main application thread
execution resumes.

Module customization code:

```mjs
// path-to-my-hooks.js

export async function initialize({ number, port }) {
  port.postMessage(`increment: ${number + 1}`);
}
```

Caller code:

```mjs
import assert from 'node:assert';
import { register } from 'node:module';
import { MessageChannel } from 'node:worker_threads';

// This example showcases how a message channel can be used to communicate
// between the main (application) thread and the hooks running on the hooks
// thread, by sending `port2` to the `initialize` hook.
const { port1, port2 } = new MessageChannel();

port1.on('message', (msg) => {
  assert.strictEqual(msg, 'increment: 2');
});
port1.unref();

register('./path-to-my-hooks.js', {
  parentURL: import.meta.url,
  data: { number: 1, port: port2 },
  transferList: [port2],
});
```

```cjs
const assert = require('node:assert');
const { register } = require('node:module');
const { pathToFileURL } = require('node:url');
const { MessageChannel } = require('node:worker_threads');

// This example showcases how a message channel can be used to communicate
// between the main (application) thread and the hooks running on the hooks
// thread, by sending `port2` to the `initialize` hook.
const { port1, port2 } = new MessageChannel();

port1.on('message', (msg) => {
  assert.strictEqual(msg, 'increment: 2');
});
port1.unref();

register('./path-to-my-hooks.js', {
  parentURL: pathToFileURL(__filename),
  data: { number: 1, port: port2 },
  transferList: [port2],
});
```


#### `event.initEvent(type[, bubbles[, cancelable]])`

<!-- YAML
added: v19.5.0
-->

> Stability: 3 - Legacy: The WHATWG spec considers it deprecated and users
> shouldn't use it at all.

* `type` {string}
* `bubbles` {boolean}
* `cancelable` {boolean}

Redundant with event constructors and incapable of setting `composed`.
This is not used in Node.js and is provided purely for completeness.
