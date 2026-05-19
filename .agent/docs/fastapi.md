---
library: fastapi
version: latest
latest: true
category: backend
official_docs: https://fastapi.tiangolo.com
last_updated: 2026-03-21
source: auto-fetched from github-dir
source_url: https://api.github.com/repos/fastapi/fastapi/contents/docs/en/docs/tutorial
---

# Bigger Applications - Multiple Files { #bigger-applications-multiple-files }

If you are building an application or a web API, it's rarely the case that you can put everything in a single file.

**FastAPI** provides a convenience tool to structure your application while keeping all the flexibility.

/// info

If you come from Flask, this would be the equivalent of Flask's Blueprints.

///


## `APIRouter` { #apirouter }

Let's say the file dedicated to handling just users is the submodule at `/app/routers/users.py`.

You want to have the *path operations* related to your users separated from the rest of the code, to keep it organized.

But it's still part of the same **FastAPI** application/web API (it's part of the same "Python Package").

You can create the *path operations* for that module using `APIRouter`.


### Import `APIRouter` { #import-apirouter }

You import it and create an "instance" the same way you would with the class `FastAPI`:

{* ../../docs_src/bigger_applications/app_an_py310/routers/users.py hl[1,3] title["app/routers/users.py"] *}


### *Path operations* with `APIRouter` { #path-operations-with-apirouter }

And then you use it to declare your *path operations*.

Use it the same way you would use the `FastAPI` class:

{* ../../docs_src/bigger_applications/app_an_py310/routers/users.py hl[6,11,16] title["app/routers/users.py"] *}

You can think of `APIRouter` as a "mini `FastAPI`" class.

All the same options are supported.

All the same `parameters`, `responses`, `dependencies`, `tags`, etc.

/// tip

In this example, the variable is called `router`, but you can name it however you want.

///

We are going to include this `APIRouter` in the main `FastAPI` app, but first, let's check the dependencies and another `APIRouter`.


## Another module with `APIRouter` { #another-module-with-apirouter }

Let's say you also have the endpoints dedicated to handling "items" from your application in the module at `app/routers/items.py`.

You have *path operations* for:

* `/items/`
* `/items/{item_id}`

It's all the same structure as with `app/routers/users.py`.

But we want to be smarter and simplify the code a bit.

We know all the *path operations* in this module have the same:

* Path `prefix`: `/items`.
* `tags`: (just one tag: `items`).
* Extra `responses`.
* `dependencies`: they all need that `X-Token` dependency we created.

So, instead of adding all that to each *path operation*, we can add it to the `APIRouter`.

{* ../../docs_src/bigger_applications/app_an_py310/routers/items.py hl[5:10,16,21] title["app/routers/items.py"] *}

As the path of each *path operation* has to start with `/`, like in:

```Python hl_lines="1"
@router.get("/{item_id}")
async def read_item(item_id: str):
    ...
```

...the prefix must not include a final `/`.

So, the prefix in this case is `/items`.

We can also add a list of `tags` and extra `responses` that will be applied to all the *path operations* included in this router.

And we can add a list of `dependencies` that will be added to all the *path operations* in the router and will be executed/solved for each request made to them.

/// tip

Note that, much like [dependencies in *path operation decorators*](dependencies/dependencies-in-path-operation-decorators.md), no value will be passed to your *path operation function*.

///

The end result is that the item paths are now:

* `/items/`
* `/items/{item_id}`

...as we intended.

* They will be marked with a list of tags that contain a single string `"items"`.
    * These "tags" are especially useful for the automatic interactive documentation systems (using OpenAPI).
* All of them will include the predefined `responses`.
* All these *path operations* will have the list of `dependencies` evaluated/executed before them.
    * If you also declare dependencies in a specific *path operation*, **they will be executed too**.
    * The router dependencies are executed first, then the [`dependencies` in the decorator](dependencies/dependencies-in-path-operation-decorators.md), and then the normal parameter dependencies.
    * You can also add [`Security` dependencies with `scopes`](../advanced/security/oauth2-scopes.md).

/// tip

Having `dependencies` in the `APIRouter` can be used, for example, to require authentication for a whole group of *path operations*. Even if the dependencies are not added individually to each one of them.

///

/// check

The `prefix`, `tags`, `responses`, and `dependencies` parameters are (as in many other cases) just a feature from **FastAPI** to help you avoid code duplication.

///


## The main `FastAPI` { #the-main-fastapi }

Now, let's see the module at `app/main.py`.

Here's where you import and use the class `FastAPI`.

This will be the main file in your application that ties everything together.

And as most of your logic will now live in its own specific module, the main file will be quite simple.


### Import `FastAPI` { #import-fastapi }

You import and create a `FastAPI` class as normally.

And we can even declare [global dependencies](dependencies/global-dependencies.md) that will be combined with the dependencies for each `APIRouter`:

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[1,3,7] title["app/main.py"] *}


### Import the `APIRouter` { #import-the-apirouter }

Now we import the other submodules that have `APIRouter`s:

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[4:5] title["app/main.py"] *}

As the files `app/routers/users.py` and `app/routers/items.py` are submodules that are part of the same Python package `app`, we can use a single dot `.` to import them using "relative imports".


### Include the `APIRouter`s for `users` and `items` { #include-the-apirouters-for-users-and-items }

Now, let's include the `router`s from the submodules `users` and `items`:

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[10:11] title["app/main.py"] *}

/// info

`users.router` contains the `APIRouter` inside of the file `app/routers/users.py`.

And `items.router` contains the `APIRouter` inside of the file `app/routers/items.py`.

///

With `app.include_router()` we can add each `APIRouter` to the main `FastAPI` application.

It will include all the routes from that router as part of it.

/// note | Technical Details

It will actually internally create a *path operation* for each *path operation* that was declared in the `APIRouter`.

So, behind the scenes, it will actually work as if everything was the same single app.

///

/// check

You don't have to worry about performance when including routers.

This will take microseconds and will only happen at startup.

So it won't affect performance. ⚡

///


### Include an `APIRouter` with a custom `prefix`, `tags`, `responses`, and `dependencies` { #include-an-apirouter-with-a-custom-prefix-tags-responses-and-dependencies }

Now, let's imagine your organization gave you the `app/internal/admin.py` file.

It contains an `APIRouter` with some admin *path operations* that your organization shares between several projects.

For this example it will be super simple. But let's say that because it is shared with other projects in the organization, we cannot modify it and add a `prefix`, `dependencies`, `tags`, etc. directly to the `APIRouter`:

{* ../../docs_src/bigger_applications/app_an_py310/internal/admin.py hl[3] title["app/internal/admin.py"] *}

But we still want to set a custom `prefix` when including the `APIRouter` so that all its *path operations* start with `/admin`, we want to secure it with the `dependencies` we already have for this project, and we want to include `tags` and `responses`.

We can declare all that without having to modify the original `APIRouter` by passing those parameters to `app.include_router()`:

{* ../../docs_src/bigger_applications/app_an_py310/main.py hl[14:17] title["app/main.py"] *}

That way, the original `APIRouter` will stay unmodified, so we can still share that same `app/internal/admin.py` file with other projects in the organization.

The result is that in our app, each of the *path operations* from the `admin` module will have:

* The prefix `/admin`.
* The tag `admin`.
* The dependency `get_token_header`.
* The response `418`. 🍵

But that will only affect that `APIRouter` in our app, not in any other code that uses it.

So, for example, other projects could use the same `APIRouter` with a different authentication method.


## Check the automatic API docs { #check-the-automatic-api-docs }

Now, run your app:

<div class="termy">

```console
$ fastapi dev

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

And open the docs at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

You will see the automatic API docs, including the paths from all the submodules, using the correct paths (and prefixes) and the correct tags:

<img src="/img/tutorial/bigger-applications/image01.png">


## Include an `APIRouter` in another { #include-an-apirouter-in-another }

The same way you can include an `APIRouter` in a `FastAPI` application, you can include an `APIRouter` in another `APIRouter` using:

```Python
router.include_router(other_router)
```

Make sure you do it before including `router` in the `FastAPI` app, so that the *path operations* from `other_router` are also included.


---


## Exclude parameters from OpenAPI { #exclude-parameters-from-openapi }

To exclude a query parameter from the generated OpenAPI schema (and thus, from the automatic documentation systems), set the parameter `include_in_schema` of `Query` to `False`:

{* ../../docs_src/query_params_str_validations/tutorial014_an_py310.py hl[10] *}


### FastAPI Data Filtering { #fastapi-data-filtering }

Now, for FastAPI, it will see the return type and make sure that what you return includes **only** the fields that are declared in the type.

FastAPI does several things internally with Pydantic to make sure that those same rules of class inheritance are not used for the returned data filtering, otherwise you could end up returning much more data than what you expected.

This way, you can get the best of both worlds: type annotations with **tooling support** and **data filtering**.


## Install `SQLModel` { #install-sqlmodel }

First, make sure you create your [virtual environment](../virtual-environments.md), activate it, and then install `sqlmodel`:

<div class="termy">

```console
$ pip install sqlmodel
---> 100%
```

</div>


## first steps


### Interactive API docs { #interactive-api-docs }

Now go to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

You will see the automatic interactive API documentation (provided by [Swagger UI](https://github.com/swagger-api/swagger-ui)):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)


### Alternative API docs { #alternative-api-docs }

And now, go to [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc).

You will see the alternative automatic documentation (provided by [ReDoc](https://github.com/Rebilly/ReDoc)):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)


### OpenAPI { #openapi }

**FastAPI** generates a "schema" with all your API using the **OpenAPI** standard for defining APIs.


#### API "schema" { #api-schema }

In this case, [OpenAPI](https://github.com/OAI/OpenAPI-Specification) is a specification that dictates how to define a schema of your API.

This schema definition includes your API paths, the possible parameters they take, etc.


#### OpenAPI and JSON Schema { #openapi-and-json-schema }

OpenAPI defines an API schema for your API. And that schema includes definitions (or "schemas") of the data sent and received by your API using **JSON Schema**, the standard for JSON data schemas.


#### Check the `openapi.json` { #check-the-openapi-json }

If you are curious about how the raw OpenAPI schema looks like, FastAPI automatically generates a JSON (schema) with the descriptions of all your API.

You can see it directly at: [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json).

It will show a JSON starting with something like:

```JSON
{
    "openapi": "3.1.0",
    "info": {
        "title": "FastAPI",
        "version": "0.1.0"
    },
    "paths": {
        "/items/": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {



...
```


#### What is OpenAPI for { #what-is-openapi-for }

The OpenAPI schema is what powers the two interactive documentation systems included.

And there are dozens of alternatives, all based on OpenAPI. You could easily add any of those alternatives to your application built with **FastAPI**.

You could also use it to generate code automatically, for clients that communicate with your API. For example, frontend, mobile or IoT applications.


### `fastapi dev` with path { #fastapi-dev-with-path }

You can also pass the file path to the `fastapi dev` command, and it will guess the FastAPI app object to use:

```console
$ fastapi dev main.py
```

But you would have to remember to pass the correct path every time you call the `fastapi` command.

Additionally, other tools might not be able to find it, for example the [VS Code Extension](../editor-support.md) or [FastAPI Cloud](https://fastapicloud.com), so it is recommended to use the `entrypoint` in `pyproject.toml`.


### Step 1: import `FastAPI` { #step-1-import-fastapi }

{* ../../docs_src/first_steps/tutorial001_py310.py hl[1] *}

`FastAPI` is a Python class that provides all the functionality for your API.

/// note | Technical Details

`FastAPI` is a class that inherits directly from `Starlette`.

You can use all the [Starlette](https://www.starlette.dev/) functionality with `FastAPI` too.

///


### Step 2: create a `FastAPI` "instance" { #step-2-create-a-fastapi-instance }

{* ../../docs_src/first_steps/tutorial001_py310.py hl[3] *}

Here the `app` variable will be an "instance" of the class `FastAPI`.

This will be the main point of interaction to create all your API.


#### About FastAPI Cloud { #about-fastapi-cloud }

**[FastAPI Cloud](https://fastapicloud.com)** is built by the same author and team behind **FastAPI**.

It streamlines the process of **building**, **deploying**, and **accessing** an API with minimal effort.

It brings the same **developer experience** of building apps with FastAPI to **deploying** them to the cloud. 🎉

FastAPI Cloud is the primary sponsor and funding provider for the *FastAPI and friends* open source projects. ✨


## Install custom exception handlers { #install-custom-exception-handlers }

You can add custom exception handlers with [the same exception utilities from Starlette](https://www.starlette.dev/exceptions/).

Let's say you have a custom exception `UnicornException` that you (or a library you use) might `raise`.

And you want to handle this exception globally with FastAPI.

You could add a custom exception handler with `@app.exception_handler()`:

{* ../../docs_src/handling_errors/tutorial003_py310.py hl[5:7,13:18,24] *}

Here, if you request `/unicorns/yolo`, the *path operation* will `raise` a `UnicornException`.

But it will be handled by the `unicorn_exception_handler`.

So, you will receive a clean error, with an HTTP status code of `418` and a JSON content of:

```JSON
{"message": "Oops! yolo did something. There goes a rainbow..."}
```

/// note | Technical Details

You could also use `from starlette.requests import Request` and `from starlette.responses import JSONResponse`.

**FastAPI** provides the same `starlette.responses` as `fastapi.responses` just as a convenience for you, the developer. But most of the available responses come directly from Starlette. The same with `Request`.

///


#### FastAPI's `HTTPException` vs Starlette's `HTTPException` { #fastapis-httpexception-vs-starlettes-httpexception }

**FastAPI** has its own `HTTPException`.

And **FastAPI**'s `HTTPException` error class inherits from Starlette's `HTTPException` error class.

The only difference is that **FastAPI**'s `HTTPException` accepts any JSON-able data for the `detail` field, while Starlette's `HTTPException` only accepts strings for it.

So, you can keep raising **FastAPI**'s `HTTPException` as normally in your code.

But when you register an exception handler, you should register it for Starlette's `HTTPException`.

This way, if any part of Starlette's internal code, or a Starlette extension or plug-in, raises a Starlette `HTTPException`, your handler will be able to catch and handle it.

In this example, to be able to have both `HTTPException`s in the same code, Starlette's exceptions is renamed to `StarletteHTTPException`:

```Python
from starlette.exceptions import HTTPException as StarletteHTTPException
```


### Reuse **FastAPI**'s exception handlers { #reuse-fastapis-exception-handlers }

If you want to use the exception along with the same default exception handlers from  **FastAPI**, you can import and reuse the default exception handlers from `fastapi.exception_handlers`:

{* ../../docs_src/handling_errors/tutorial006_py310.py hl[2:5,15,21] *}

In this example you are just printing the error with a very expressive message, but you get the idea. You can use the exception and then just reuse the default exception handlers.


---


### OpenAPI support { #openapi-support }

OpenAPI doesn't support a way to declare a *path parameter* to contain a *path* inside, as that could lead to scenarios that are difficult to test and define.

Nevertheless, you can still do it in **FastAPI**, using one of the internal tools from Starlette.

And the docs would still work, although not adding any documentation telling that the parameter should contain a path.


## `examples` in JSON Schema - OpenAPI { #examples-in-json-schema-openapi }

When using any of:

* `Path()`
* `Query()`
* `Header()`
* `Cookie()`
* `Body()`
* `Form()`
* `File()`

you can also declare a group of `examples` with additional information that will be added to their **JSON Schemas** inside of **OpenAPI**.


### OpenAPI-specific `examples` { #openapi-specific-examples }

Since before **JSON Schema** supported `examples` OpenAPI had support for a different field also called `examples`.

This **OpenAPI-specific** `examples` goes in another section in the OpenAPI specification. It goes in the **details for each *path operation***, not inside each JSON Schema.

And Swagger UI has supported this particular `examples` field for a while. So, you can use it to **show** different **examples in the docs UI**.

The shape of this OpenAPI-specific field `examples` is a `dict` with **multiple examples** (instead of a `list`), each with extra information that will be added to **OpenAPI** too.

This doesn't go inside of each JSON Schema contained in OpenAPI, this goes outside, in the *path operation* directly.


### Using the `openapi_examples` Parameter { #using-the-openapi-examples-parameter }

You can declare the OpenAPI-specific `examples` in FastAPI with the parameter `openapi_examples` for:

* `Path()`
* `Query()`
* `Header()`
* `Cookie()`
* `Body()`
* `Form()`
* `File()`

The keys of the `dict` identify each example, and each value is another `dict`.

Each specific example `dict` in the `examples` can contain:

* `summary`: Short description for the example.
* `description`: A long description that can contain Markdown text.
* `value`: This is the actual example shown, e.g. a `dict`.
* `externalValue`: alternative to `value`, a URL pointing to the example. Although this might not be supported by as many tools as `value`.

You can use it like this:

{* ../../docs_src/schema_extra_example/tutorial005_an_py310.py hl[23:49] *}


### OpenAPI Examples in the Docs UI { #openapi-examples-in-the-docs-ui }

With `openapi_examples` added to `Body()` the `/docs` would look like:

<img src="/img/tutorial/body-fields/image02.png">


### Pydantic and FastAPI `examples` { #pydantic-and-fastapi-examples }

When you add `examples` inside a Pydantic model, using `schema_extra` or `Field(examples=["something"])` that example is added to the **JSON Schema** for that Pydantic model.

And that **JSON Schema** of the Pydantic model is included in the **OpenAPI** of your API, and then it's used in the docs UI.

In versions of FastAPI before 0.99.0 (0.99.0 and above use the newer OpenAPI 3.1.0) when you used `example` or `examples` with any of the other utilities (`Query()`, `Body()`, etc.) those examples were not added to the JSON Schema that describes that data (not even to OpenAPI's own version of JSON Schema), they were added directly to the *path operation* declaration in OpenAPI (outside the parts of OpenAPI that use JSON Schema).

But now that FastAPI 0.99.0 and above uses OpenAPI 3.1.0, that uses JSON Schema 2020-12, and Swagger UI 5.0.0 and above, everything is more consistent and the examples are included in JSON Schema.


### Swagger UI and OpenAPI-specific `examples` { #swagger-ui-and-openapi-specific-examples }

Now, as Swagger UI didn't support multiple JSON Schema examples (as of 2023-08-26), users didn't have a way to show multiple examples in the docs.

To solve that, FastAPI `0.103.0` **added support** for declaring the same old **OpenAPI-specific** `examples` field with the new parameter `openapi_examples`. 🤓


## Metadata for API { #metadata-for-api }

You can set the following fields that are used in the OpenAPI specification and the automatic API docs UIs:

| Parameter | Type | Description |
|------------|------|-------------|
| `title` | `str` | The title of the API. |
| `summary` | `str` | A short summary of the API. <small>Available since OpenAPI 3.1.0, FastAPI 0.99.0.</small> |
| `description` | `str` | A short description of the API. It can use Markdown. |
| `version` | `string` | The version of the API. This is the version of your own application, not of OpenAPI. For example `2.5.0`. |
| `terms_of_service` | `str` | A URL to the Terms of Service for the API. If provided, this has to be a URL. |
| `contact` | `dict` | The contact information for the exposed API. It can contain several fields. <details><summary><code>contact</code> fields</summary><table><thead><tr><th>Parameter</th><th>Type</th><th>Description</th></tr></thead><tbody><tr><td><code>name</code></td><td><code>str</code></td><td>The identifying name of the contact person/organization.</td></tr><tr><td><code>url</code></td><td><code>str</code></td><td>The URL pointing to the contact information. MUST be in the format of a URL.</td></tr><tr><td><code>email</code></td><td><code>str</code></td><td>The email address of the contact person/organization. MUST be in the format of an email address.</td></tr></tbody></table></details> |
| `license_info` | `dict` | The license information for the exposed API. It can contain several fields. <details><summary><code>license_info</code> fields</summary><table><thead><tr><th>Parameter</th><th>Type</th><th>Description</th></tr></thead><tbody><tr><td><code>name</code></td><td><code>str</code></td><td><strong>REQUIRED</strong> (if a <code>license_info</code> is set). The license name used for the API.</td></tr><tr><td><code>identifier</code></td><td><code>str</code></td><td>An [SPDX](https://spdx.org/licenses/) license expression for the API. The <code>identifier</code> field is mutually exclusive of the <code>url</code> field. <small>Available since OpenAPI 3.1.0, FastAPI 0.99.0.</small></td></tr><tr><td><code>url</code></td><td><code>str</code></td><td>A URL to the license used for the API. MUST be in the format of a URL.</td></tr></tbody></table></details> |

You can set them as follows:

{* ../../docs_src/metadata/tutorial001_py310.py hl[3:16, 19:32] *}

/// tip

You can write Markdown in the `description` field and it will be rendered in the output.

///

With this configuration, the automatic API docs would look like:

<img src="/img/tutorial/metadata/image01.png">


### **FastAPI** app file { #fastapi-app-file }

Let's say you have a file structure as described in [Bigger Applications](bigger-applications.md):

```
.
├── app
│   ├── __init__.py
│   └── main.py
```

In the file `main.py` you have your **FastAPI** app:


{* ../../docs_src/app_testing/app_a_py310/main.py *}


## Install FastAPI { #install-fastapi }

The first step is to install FastAPI.

Make sure you create a [virtual environment](../virtual-environments.md), activate it, and then **install FastAPI**:

<div class="termy">

```console
$ pip install "fastapi[standard]"

---> 100%
```

</div>

/// note

When you install with `pip install "fastapi[standard]"` it comes with some default optional standard dependencies, including `fastapi-cloud-cli`, which allows you to deploy to [FastAPI Cloud](https://fastapicloud.com).

If you don't want to have those optional dependencies, you can instead install `pip install fastapi`.

If you want to install the standard dependencies but without the `fastapi-cloud-cli`, you can install with `pip install "fastapi[standard-no-fastapi-cloud-cli]"`.

///

/// tip

FastAPI has an [official extension for VS Code](https://marketplace.visualstudio.com/items?itemName=FastAPILabs.fastapi-vscode) (and Cursor), which provides a lot of features, including a path operation explorer, path operation search, CodeLens navigation in tests (jump to definition from tests), and FastAPI Cloud deployment and logs, all from your editor.

///
