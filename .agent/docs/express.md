---
library: express
version: 5.x
latest: true
category: backend
official_docs: https://expressjs.com
last_updated: 2026-03-21
source: auto-fetched from github-dir
source_url: https://api.github.com/repos/expressjs/expressjs.com/contents/en/guide
---

# Moving to Express 5

<h2 id="overview">Overview</h2>

Express 5 is not very different from Express 4; although it maintains the same basic API, there are still changes that break compatibility with the previous version. Therefore, an application built with Express 4 might not work if you update it to use Express 5.

To install this version, you need to have a Node.js version 18 or higher. Then, execute the following command in your application directory:

```sh
npm install "express@5"
```

You can then run your automated tests to see what fails, and fix problems according to the updates listed below. After addressing test failures, run your app to see what errors occur. You'll find out right away if the app uses any methods or properties that are not supported.


## Removed methods and properties

If you use any of these methods or properties in your app, it will crash. So, you'll need to change your app after you update to version 5.

<h3 id="app.del">app.del()</h3>

Express 5 no longer supports the `app.del()` function. If you use this function, an error is thrown. For registering HTTP DELETE routes, use the `app.delete()` function instead.

Initially, `del` was used instead of `delete`, because `delete` is a reserved keyword in JavaScript. However, as of ECMAScript 6, `delete` and other reserved keywords can legally be used as property names.

{% capture codemod-route-del-to-delete %}
You can replace the deprecated signatures with the following command:

```plain-text
npx codemod@latest @expressjs/route-del-to-delete
```
{% endcapture %}

{% include admonitions/note.html content=codemod-route-del-to-delete %}

```js
// v4
app.del('/user/:id', (req, res) => {
  res.send(`DELETE /user/${req.params.id}`)
})

// v5
app.delete('/user/:id', (req, res) => {
  res.send(`DELETE /user/${req.params.id}`)
})
```

<h3 id="app.param">app.param(fn)</h3>

The `app.param(fn)` signature was used for modifying the behavior of the `app.param(name, fn)` function. It has been deprecated since v4.11.0, and Express 5 no longer supports it at all.

<h3 id="plural">Pluralized method names</h3>

The following method names have been pluralized. In Express 4, using the old methods resulted in a deprecation warning. Express 5 no longer supports them at all:

`req.acceptsCharset()` is replaced by `req.acceptsCharsets()`.

`req.acceptsEncoding()` is replaced by `req.acceptsEncodings()`.

`req.acceptsLanguage()` is replaced by `req.acceptsLanguages()`.

{% capture codemod-pluralized-methods %}
You can replace the deprecated signatures with the following command:

```plain-text
npx codemod@latest @expressjs/pluralize-method-names
```
{% endcapture %}

{% include admonitions/note.html content=codemod-pluralized-methods %}

```js
// v4
app.all('/', (req, res) => {
  req.acceptsCharset('utf-8')
  req.acceptsEncoding('br')
  req.acceptsLanguage('en')

  // ...
})

// v5
app.all('/', (req, res) => {
  req.acceptsCharsets('utf-8')
  req.acceptsEncodings('br')
  req.acceptsLanguages('en')

  // ...
})
```

<h3 id="leading">Leading colon (:) in the name for app.param(name, fn)</h3>

A leading colon character (:) in the name for the `app.param(name, fn)` function is a remnant of Express 3, and for the sake of backwards compatibility, Express 4 supported it with a deprecation notice. Express 5 will silently ignore it and use the name parameter without prefixing it with a colon.

This should not affect your code if you follow the Express 4 documentation of [app.param](/{{ page.lang }}/4x/api.html#app.param), as it makes no mention of the leading colon.

<h3 id="req.param">req.param(name)</h3>

This potentially confusing and dangerous method of retrieving form data has been removed. You will now need to specifically look for the submitted parameter name in the `req.params`, `req.body`, or `req.query` object.

{% capture codemod-req-param %}
You can replace the deprecated signatures with the following command:

```plain-text
npx codemod@latest @expressjs/explicit-request-params
```
{% endcapture %}

{% include admonitions/note.html content=codemod-req-param %}

```js
// v4
app.post('/user', (req, res) => {
  const id = req.param('id')
  const body = req.param('body')
  const query = req.param('query')

  // ...
})

// v5
app.post('/user', (req, res) => {
  const id = req.params.id
  const body = req.body
  const query = req.query

  // ...
})
```

<h3 id="res.json">res.json(obj, status)</h3>

Express 5 no longer supports the signature `res.json(obj, status)`. Instead, set the status and then chain it to the `res.json()` method like this: `res.status(status).json(obj)`.

{% capture codemod-status-send-order %}
You can replace the deprecated signatures with the following command:

```plain-text
npx codemod@latest @expressjs/status-send-order
```
{% endcapture %}

{% include admonitions/note.html content=codemod-status-send-order %}

```js
// v4
app.post('/user', (req, res) => {
  res.json({ name: 'Ruben' }, 201)
})

// v5
app.post('/user', (req, res) => {
  res.status(201).json({ name: 'Ruben' })
})
```

<h3 id="res.jsonp">res.jsonp(obj, status)</h3>

Express 5 no longer supports the signature `res.jsonp(obj, status)`. Instead, set the status and then chain it to the `res.jsonp()` method like this: `res.status(status).jsonp(obj)`.

{% include admonitions/note.html content=codemod-status-send-order %}


```js
// v4
app.post('/user', (req, res) => {
  res.jsonp({ name: 'Ruben' }, 201)
})

// v5
app.post('/user', (req, res) => {
  res.status(201).jsonp({ name: 'Ruben' })
})
```

<h3 id="res.redirect">res.redirect(url, status)</h3>

Express 5 no longer supports the signature `res.redirect(url, status)`. Instead, use the following signature: `res.redirect(status, url)`.

{% capture codemod-redirect-arg-order %}
You can replace the deprecated signatures with the following command:

```plain-text
npx codemod@latest @expressjs/redirect-arg-order
```
{% endcapture %}

{% include admonitions/note.html content=codemod-redirect-arg-order %}

```js
// v4
app.get('/user', (req, res) => {
  res.redirect('/users', 301)
})

// v5
app.get('/user', (req, res) => {
  res.redirect(301, '/users')
})
```


<h3 id="magic-redirect">res.redirect('back') and res.location('back')</h3>

Express 5 no longer supports the magic string `back` in the `res.redirect()` and `res.location()` methods. Instead, use the `req.get('Referrer') || '/'` value to redirect back to the previous page. In Express 4, the `res.redirect('back')` and `res.location('back')` methods were deprecated.

{% capture codemod-back-redirect-deprecated %}
You can replace the deprecated signatures with the following command:

```plain-text
npx codemod@latest @expressjs/back-redirect-deprecated
```
{% endcapture %}

{% include admonitions/note.html content=codemod-back-redirect-deprecated %}

```js
// v4
app.get('/user', (req, res) => {
  res.redirect('back')
})

// v5
app.get('/user', (req, res) => {
  res.redirect(req.get('Referrer') || '/')
})
```

<h3 id="res.send.body">res.send(body, status)</h3>

Express 5 no longer supports the signature `res.send(obj, status)`. Instead, set the status and then chain it to the `res.send()` method like this: `res.status(status).send(obj)`.

{% include admonitions/note.html content=codemod-status-send-order %}


```js
// v4
app.get('/user', (req, res) => {
  res.send({ name: 'Ruben' }, 200)
})

// v5
app.get('/user', (req, res) => {
  res.status(200).send({ name: 'Ruben' })
})
```

<h3 id="res.send.status">res.send(status)</h3>

Express 5 no longer supports the signature `res.send(status)`, where `status` is a number. Instead, use the `res.sendStatus(statusCode)` function, which sets the HTTP response header status code and sends the text version of the code: "Not Found", "Internal Server Error", and so on.
If you need to send a number by using the `res.send()` function, quote the number to convert it to a string, so that Express does not interpret it as an attempt to use the unsupported old signature.

{% include admonitions/note.html content=codemod-status-send-order %}


```js
// v4
app.get('/user', (req, res) => {
  res.send(200)
})

// v5
app.get('/user', (req, res) => {
  res.sendStatus(200)
})
```

<h3 id="res.sendfile">res.sendfile()</h3>

The `res.sendfile()` function has been replaced by a camel-cased version `res.sendFile()` in Express 5.

**Note:** In Express 5, `res.sendFile()` uses the `mime-types` package for MIME type detection, which returns different Content-Type values than Express 4 for several common file types:

- JavaScript files (.js): now "text/javascript" instead of "application/javascript"
- JSON files (.json): now "application/json" instead of "text/json"
- CSS files (.css): now "text/css" instead of "text/plain"
- XML files (.xml): now "application/xml" instead of "text/xml"
- Font files (.woff): now "font/woff" instead of "application/font-woff"
- SVG files (.svg): now "image/svg+xml" instead of "application/svg+xml"

{% capture codemod-camelcase-sendfile %}
You can replace the deprecated signatures with the following command:

```plain-text
npx codemod@latest @expressjs/camelcase-sendfile
```
{% endcapture %}

{% include admonitions/note.html content=codemod-camelcase-sendfile %}

```js
// v4
app.get('/user', (req, res) => {
  res.sendfile('/path/to/file')
})

// v5
app.get('/user', (req, res) => {
  res.sendFile('/path/to/file')
})
```

<h3 id="router.param">router.param(fn)</h3>

The `router.param(fn)` signature was used for modifying the behavior of the `router.param(name, fn)` function. It has been deprecated since v4.11.0, and Express 5 no longer supports it at all.

<h3 id="express.static.mime">express.static.mime</h3>

In Express 5, `mime` is no longer an exported property of the `static` field.
Use the [`mime-types` package](https://github.com/jshttp/mime-types) to work with MIME type values.

**Important:** This change affects not only direct usage of `express.static.mime` but also other Express methods that rely on MIME type detection, such as `res.sendFile()`. The following MIME types have changed from Express 4:

- JavaScript files (.js): now served as "text/javascript" instead of "application/javascript"
- JSON files (.json): now served as "application/json" instead of "text/json"
- CSS files (.css): now served as "text/css" instead of "text/plain"
- HTML files (.html): now served as "text/html; charset=utf-8" instead of just "text/html"
- XML files (.xml): now served as "application/xml" instead of "text/xml"
- Font files (.woff): now served as "font/woff" instead of "application/font-woff"

```js
// v4
express.static.mime.lookup('json')

// v5
const mime = require('mime-types')
mime.lookup('json')
```

<h3 id="express:router-debug-logs">express:router debug logs</h3>

In Express 5, router handling logic is performed by a dependency. Therefore, the
debug logs for the router are no longer available under the `express:` namespace.
In v4, the logs were available under the namespaces `express:router`, `express:router:layer`,
and `express:router:route`. All of these were included under the namespace `express:*`.
In v5.1+, the logs are available under the namespaces `router`, `router:layer`, and `router:route`.
The logs from `router:layer` and `router:route` are included in the namespace `router:*`.
To achieve the same detail of debug logging when using `express:*` in v4, use a conjunction of
`express:*`, `router`, and `router:*`.

```sh

### Route paths based on string patterns

{% capture caution-string-patterns %} The string patterns in Express 5 no longer work. Please refer to the [migration guide](/{{ page.lang }}/guide/migrating-5.html#path-syntax) for more information.{% endcapture %}

{% include admonitions/caution.html content=caution-string-patterns %}

This route path will match `acd` and `abcd`.

```js
app.get('/ab?cd', (req, res) => {
  res.send('ab?cd')
})
```

This route path will match `abcd`, `abbcd`, `abbbcd`, and so on.

```js
app.get('/ab+cd', (req, res) => {
  res.send('ab+cd')
})
```

This route path will match `abcd`, `abxcd`, `abRANDOMcd`, `ab123cd`, and so on.

```js
app.get('/ab*cd', (req, res) => {
  res.send('ab*cd')
})
```

This route path will match `/abe` and `/abcde`.

```js
app.get('/ab(cd)?e', (req, res) => {
  res.send('ab(cd)?e')
})
```


### Installation

```bash
$ npm install cassandra-driver
```


### Installation

```bash
$ npm install couchbase
```


### Installation

```bash
$ npm install nano
```


### Installation

```bash
$ npm install level levelup leveldown
```


### Installation

```bash
$ npm install mysql
```


### Installation

```bash
$ npm install mongodb
```


### Installation

```bash
$ npm install neo4j-driver
```


### Installation

 NOTE: [See installation prerequisites](https://github.com/oracle/node-oracledb#-installation).

```bash
$ npm install oracledb
```


### Installation

```bash
$ npm install pg-promise
```


### Installation

```bash
$ npm install redis
```


### Installation

```bash
$ npm install tedious
```


### Installation

```bash
$ npm install sqlite3
```


### Installation

```bash
$ npm install elasticsearch
```


## Advanced options

When running through Node.js, you can set a few environment variables that will change the behavior of the debug logging:

| Name      | Purpose                                         |
|-----------|-------------------------------------------------|
| `DEBUG`   | Enables/disables specific debugging namespaces. |
| `DEBUG_COLORS`| Whether or not to use colors in the debug output. |
| `DEBUG_DEPTH` | Object inspection depth. |
| `DEBUG_FD`    | File descriptor to write debug output to. |
| `DEBUG_SHOW_HIDDEN` | Shows hidden properties on inspected objects. |

{% capture debug-text %}

The environment variables beginning with `DEBUG_` end up being
converted into an Options object that gets used with `%o`/`%O` formatters.
See the Node.js documentation for
[`util.inspect()`](https://nodejs.org/api/util.html#util_util_inspect_object_options)
for the complete list.

{% endcapture %}

{% include admonitions/note.html content=debug-text %}


---


## overriding express api

---
layout: page
title: Overriding the Express API
description: Discover how to customize and extend the Express.js API by overriding methods and properties on the request and response objects using prototypes.
menu: guide
order: 4
---


# Overriding the Express API

The Express API consists of various methods and properties on the request and response objects. These are inherited by prototype. There are two extension points for the Express API:

1. The global prototypes at `express.request` and `express.response`.
2. App-specific prototypes at `app.request` and `app.response`.

Altering the global prototypes will affect all loaded Express apps in the same process. If desired, alterations can be made app-specific by only altering the app-specific prototypes after creating a new app.


## Methods

You can override the signature and behavior of existing methods with your own, by assigning a custom function.

Following is an example of overriding the behavior of [res.sendStatus](/4x/api.html#res.sendStatus).

```js
app.response.sendStatus = function (statusCode, type, message) {
  // code is intentionally kept simple for demonstration purpose
  return this.contentType(type)
    .status(statusCode)
    .send(message)
}
```

The above implementation completely changes the original signature of `res.sendStatus`. It now accepts a status code, encoding type, and the message to be sent to the client.

The overridden method may now be used this way:

```js
res.sendStatus(404, 'application/json', '{"error":"resource not found"}')
```
