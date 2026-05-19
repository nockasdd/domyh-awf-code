---
library: angular
version: 20.x
latest: true
category: frontend
official_docs: https://angular.dev
last_updated: 2026-03-21
source: auto-fetched from github-dir
source_url: https://api.github.com/repos/angular/angular/contents/adev/src/content/guide
---

# Drag and drop


### CDK Installation

The [Component Dev Kit (CDK)](https://material.angular.dev/cdk/categories) is a set of behavior primitives for building components. To use the drag and drop directives, first install `@angular/cdk` from npm. You can do this from your terminal using Angular CLI:

```shell
ng add @angular/cdk
```


### Direct use of the DOM APIs and explicit sanitization calls

Unless you enforce Trusted Types, the built-in browser DOM APIs don't automatically protect you from security vulnerabilities.
For example, `document`, the node available through `ElementRef`, and many third-party APIs contain unsafe methods.
Likewise, if you interact with other libraries that manipulate the DOM, you likely won't have the same automatic sanitization as with Angular interpolations.
Avoid directly interacting with the DOM and instead use Angular templates where possible.

For cases where this is unavoidable, use the built-in Angular sanitization functions.
Sanitize untrusted values with the [DomSanitizer.sanitize](api/platform-browser/DomSanitizer#sanitize) method and the appropriate `SecurityContext`.
That function also accepts values that were marked as trusted using the `bypassSecurityTrust` functions, and does not sanitize them, as [described below](#trusting-safe-values).


### Configure custom cookie/header names

If your backend service uses different names for the XSRF token cookie or header, use `withXsrfConfiguration` to override the defaults.

Add it to the `provideHttpClient` call as follows:

```ts
export const appConfig: ApplicationConfig = {
  providers: [
    provideHttpClient(
      withXsrfConfiguration({
        cookieName: 'CUSTOM_XSRF_TOKEN',
        headerName: 'X-Custom-Xsrf-Header',
      }),
    ),
  ],
};
```


### Configuring allowed hosts

To allow specific hostnames, you need to add them to the allowlist. This is critical for ensuring your application works correctly and securely when deployed. The patterns support wildcards for flexible hostname matching.

You can configure the `allowedHosts` option in your `angular.json`:

```json {hideCopy}
{
  // ...
  "projects": {
    "your-project-name": {
      // ...
      "architect": {
        "build": {
          "builder": "@angular/build:application",
          "options": {
            "security": {
              "allowedHosts": [
                "example.com",
                "*.example.com" // allows all subdomains of example.com
              ]
            }
            // ... other options
          }
        }
      }
    }
  }
}
```

You can also configure `allowedHosts` when initializing the application engine:

```typescript
const appEngine = new AngularAppEngine({
  allowedHosts: ['example.com', '*.trusted-example.com'],
});

const nodeAppEngine = new AngularNodeAppEngine({
  allowedHosts: ['example.com', '*.trusted-example.com'],
});
```

For the Node.js variant `AngularNodeAppEngine`, you can also provide `NG_ALLOWED_HOSTS` (comma-separated list) environment variable for authorizing hosts.

```bash {hideDollar}
export NG_ALLOWED_HOSTS="example.com,*.trusted-example.com"
```


# Getting started with NgOptimizedImage

The `NgOptimizedImage` directive makes it easy to adopt performance best practices for loading images.

The directive ensures that the loading of the [Largest Contentful Paint (LCP)](http://web.dev/lcp) image is prioritized by:

- Automatically setting the `fetchpriority` attribute on the `<img>` tag
- Lazy loading other images by default
- Automatically generating a preconnect link tag in the document head
- Automatically generating a `srcset` attribute
- Generating a [preload hint](https://developer.mozilla.org/docs/Web/HTML/Link_types/preload) if app is using SSR

In addition to optimizing the loading of the LCP image, `NgOptimizedImage` enforces a number of image best practices, such as:

- Using [image CDN URLs to apply image optimizations](https://web.dev/image-cdns/#how-image-cdns-use-urls-to-indicate-optimization-options)
- Preventing layout shift by requiring `width` and `height`
- Warning if `width` or `height` have been set incorrectly
- Warning if the image will be visually distorted when rendered

If you're using a background image in CSS, [start here](#how-to-migrate-your-background-image).

**NOTE: Although the `NgOptimizedImage` directive was made a stable feature in Angular version 15, it has been backported and is available as a stable feature in versions 13.4.0 and 14.3.0 as well.**


## Getting Started

<docs-workflow>
<docs-step title="Import `NgOptimizedImage` directive">
Import `NgOptimizedImage` directive from `@angular/common`:

```ts
import {NgOptimizedImage} from '@angular/common';
```

and include it into the `imports` array of a standalone component or an NgModule:

```ts
imports: [
  NgOptimizedImage,
  // ...
],
```

</docs-step>
<docs-step title="(Optional) Set up a Loader">
An image loader is not **required** in order to use NgOptimizedImage, but using one with an image CDN enables powerful performance features, including automatic `srcset`s for your images.

A brief guide for setting up a loader can be found in the [Configuring an Image Loader](#configuring-an-image-loader-for-ngoptimizedimage) section at the end of this page.
</docs-step>
<docs-step title="Enable the directive">
To activate the `NgOptimizedImage` directive, replace your image's `src` attribute with `ngSrc`.

```html
<img ngSrc="cat.jpg" />
```

If you're using a [built-in third-party loader](#built-in-loaders), make sure to omit the base URL path from `src`, as that will be prepended automatically by the loader.
</docs-step>
<docs-step title="Mark images as `priority`">
Always mark the [LCP image](https://web.dev/lcp/#what-elements-are-considered) on your page as `priority` to prioritize its loading.

```html
<img ngSrc="cat.jpg" width="400" height="200" priority />
```

Marking an image as `priority` applies the following optimizations:

- Sets `fetchpriority=high` (read more about priority hints [here](https://web.dev/priority-hints))
- Sets `loading=eager` (read more about native lazy loading [here](https://web.dev/browser-level-image-lazy-loading))
- Automatically generates a [preload link element](https://developer.mozilla.org/docs/Web/HTML/Link_types/preload) if [rendering on the server](guide/ssr).

Angular displays a warning during development if the LCP element is an image that does not have the `priority` attribute. A page’s LCP element can vary based on a number of factors - such as the dimensions of a user's screen, so a page may have multiple images that should be marked `priority`. See [CSS for Web Vitals](https://web.dev/css-web-vitals/#images-and-largest-contentful-paint-lcp) for more details.
</docs-step>
<docs-step title="Include Width and Height">
In order to prevent [image-related layout shifts](https://web.dev/css-web-vitals/#images-and-layout-shifts), NgOptimizedImage requires that you specify a height and width for your image, as follows:

```html
<img ngSrc="cat.jpg" width="400" height="200" />
```

For **responsive images** (images which you've styled to grow and shrink relative to the viewport), the `width` and `height` attributes should be the intrinsic size of the image file. For responsive images it's also important to [set a value for `sizes`.](#responsive-images)

For **fixed size images**, the `width` and `height` attributes should reflect the desired rendered size of the image. The aspect ratio of these attributes should always match the intrinsic aspect ratio of the image.

NOTE: If you don't know the size of your images, consider using "fill mode" to inherit the size of the parent container, as described below.
</docs-step>
</docs-workflow>


## How to migrate your background image

Here's a simple step-by-step process for migrating from `background-image` to `NgOptimizedImage`. For these steps, we'll refer to the element that has an image background as the "containing element":

1. Remove the `background-image` style from the containing element.
2. Ensure that the containing element has `position: "relative"`, `position: "fixed"`, or `position: "absolute"`.
3. Create a new image element as a child of the containing element, using `ngSrc` to enable the `NgOptimizedImage` directive.
4. Give that element the `fill` attribute. Do not include a `height` and `width`.
5. If you believe this image might be your [LCP element](https://web.dev/lcp/), add the `priority` attribute to the image element.

You can adjust how the background image fills the container as described in the [Using fill mode](#using-fill-mode) section.


## Configuring an image loader for `NgOptimizedImage`

A "loader" is a function that generates an [image transformation URL](https://web.dev/image-cdns/#how-image-cdns-use-urls-to-indicate-optimization-options) for a given image file. When appropriate, `NgOptimizedImage` sets the size, format, and image quality transformations for an image.

`NgOptimizedImage` provides both a generic loader that applies no transformations, as well as loaders for various third-party image services. It also supports writing your own custom loader.

| Loader type                            | Behavior                                                                                                                                                                                                                       |
| :------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Generic loader                         | The URL returned by the generic loader will always match the value of `src`. In other words, this loader applies no transformations. Sites that use Angular to serve images are the primary intended use case for this loader. |
| Loaders for third-party image services | The URL returned by the loaders for third-party image services will follow API conventions used by that particular image service.                                                                                              |
| Custom loaders                         | A custom loader's behavior is defined by its developer. You should use a custom loader if your image service isn't supported by the loaders that come preconfigured with `NgOptimizedImage`.                                   |

Based on the image services commonly used with Angular applications, `NgOptimizedImage` provides loaders preconfigured to work with the following image services:

| Image Service             | Angular API               | Documentation                                                               |
| :------------------------ | :------------------------ | :-------------------------------------------------------------------------- |
| Cloudflare Image Resizing | `provideCloudflareLoader` | [Documentation](https://developers.cloudflare.com/images/image-resizing/)   |
| Cloudinary                | `provideCloudinaryLoader` | [Documentation](https://cloudinary.com/documentation/resizing_and_cropping) |
| ImageKit                  | `provideImageKitLoader`   | [Documentation](https://docs.imagekit.io/)                                  |
| Imgix                     | `provideImgixLoader`      | [Documentation](https://docs.imgix.com/)                                    |
| Netlify                   | `provideNetlifyLoader`    | [Documentation](https://docs.netlify.com/image-cdn/overview/)               |

To use the **generic loader** no additional code changes are necessary. This is the default behavior.


### Configuring server routes

You can create a server route config by declaring an array of [`ServerRoute`](api/ssr/ServerRoute 'API reference') objects. This configuration typically lives in a file named `app.routes.server.ts`.

```typescript
// app.routes.server.ts
import {RenderMode, ServerRoute} from '@angular/ssr';

export const serverRoutes: ServerRoute[] = [
  {
    path: '', // This renders the "/" route on the client (CSR)
    renderMode: RenderMode.Client,
  },
  {
    path: 'about', // This page is static, so we prerender it (SSG)
    renderMode: RenderMode.Prerender,
  },
  {
    path: 'profile', // This page requires user-specific data, so we use SSR
    renderMode: RenderMode.Server,
  },
  {
    path: '**', // All other routes will be rendered on the server (SSR)
    renderMode: RenderMode.Server,
  },
];
```

You can add this config to your application with [`provideServerRendering`](api/ssr/provideServerRendering 'API reference') using the [`withRoutes`](api/ssr/withRoutes 'API reference') function:

```typescript
import {provideServerRendering, withRoutes} from '@angular/ssr';
import {serverRoutes} from './app.routes.server';

// app.config.server.ts
const serverConfig: ApplicationConfig = {
  providers: [
    provideServerRendering(withRoutes(serverRoutes)),
    // ... other providers ...
  ],
};
```

When using the [App shell pattern](ecosystem/service-workers/app-shell), you must specify the component to be used as the app shell for client-side rendered routes. To do this, use the [`withAppShell`](api/ssr/withAppShell 'API reference') feature:

```typescript
import {provideServerRendering, withRoutes, withAppShell} from '@angular/ssr';
import {AppShell} from './app-shell';

const serverConfig: ApplicationConfig = {
  providers: [
    provideServerRendering(withRoutes(serverRoutes), withAppShell(AppShell)),
    // ... other providers ...
  ],
};
```


### Configuring the caching options

You can customize how Angular caches HTTP responses during server‑side rendering (SSR) and reuses them during hydration by configuring `HttpTransferCacheOptions`.  
This configuration is provided globally using `withHttpTransferCacheOptions` inside `provideClientHydration()`.

By default, `HttpClient` caches all `HEAD` and `GET` requests which don't contain `Authorization` or `Proxy-Authorization` headers. You can override those settings by using `withHttpTransferCacheOptions` to the hydration configuration.

```ts
import {bootstrapApplication} from '@angular/platform-browser';
import {provideClientHydration, withHttpTransferCacheOptions} from '@angular/platform-browser';

bootstrapApplication(App, {
  providers: [
    provideClientHydration(
      withHttpTransferCacheOptions({
        includeHeaders: ['ETag', 'Cache-Control'],
        filter: (req) => !req.url.includes('/api/profile'),
        includePostRequests: true,
        includeRequestsWithAuthHeaders: false,
      }),
    ),
  ],
});
```

---


## Configuring a server


### Manual setup

If you have a custom setup and didn't use Angular CLI to enable SSR, you can enable hydration manually by visiting your main application component or module and importing `provideClientHydration` from `@angular/platform-browser`. You'll then add that provider to your app's bootstrapping providers list.

```typescript
import {
  bootstrapApplication,
  provideClientHydration,
} from '@angular/platform-browser';
...

bootstrapApplication(App, {
  providers: [provideClientHydration()]
});
```

Alternatively if you are using NgModules, you would add `provideClientHydration` to your root app module's provider list.

```typescript
import {provideClientHydration} from '@angular/platform-browser';
import {NgModule} from '@angular/core';

@NgModule({
  declarations: [App],
  exports: [App],
  bootstrap: [App],
  providers: [provideClientHydration()],
})
export class AppModule {}
```

IMPORTANT: Make sure that the `provideClientHydration()` call is also included into a set of providers that is used to bootstrap an application on the **server**. In applications with the default project structure (generated by the `ng new` command), adding a call to the root `AppModule` should be sufficient, since this module is imported by the server module. If you use a custom setup, add the `provideClientHydration()` call to the providers list in the server bootstrap configuration.


### Preserve Whitespaces Configuration

When using the hydration feature, we recommend using the default setting of `false` for `preserveWhitespaces`. If this setting is not in your tsconfig, the value will be `false` and no changes are required. If you choose to enable preserving whitespaces by adding `preserveWhitespaces: true` to your tsconfig, it is possible you may encounter issues with hydration. This is not yet a fully supported configuration.

HELPFUL: Make sure that this setting is set **consistently** in `tsconfig.server.json` for your server and `tsconfig.app.json` for your browser builds. A mismatched value will cause hydration to break.

If you choose to set this setting in your tsconfig, we recommend to set it only in `tsconfig.app.json` which by default the `tsconfig.server.json` will inherit it from.


## How to skip hydration for particular components

Some components may not work properly with hydration enabled due to some of the aforementioned issues, like [Direct DOM Manipulation](#direct-dom-manipulation). As a workaround, you can add the `ngSkipHydration` attribute to a component's tag in order to skip hydrating the entire component.

```angular-html
<app-example ngSkipHydration />
```

Alternatively you can set `ngSkipHydration` as a host binding.

```typescript
@Component({
  ...
  host: {ngSkipHydration: 'true'},
})
class ExampleComponent {}
```

The `ngSkipHydration` attribute will force Angular to skip hydrating the entire component and its children. Using this attribute means that the component will behave as if hydration is not enabled, meaning it will destroy and re-render itself.

HELPFUL: This will fix rendering issues, but it means that for this component (and its children), you don't get the benefits of hydration. You will need to adjust your component's implementation to avoid hydration-breaking patterns (i.e. Direct DOM Manipulation) to be able to remove the skip hydration annotation.

The `ngSkipHydration` attribute can only be used on component host nodes. Angular throws an error if this attribute is added to other nodes.

Keep in mind that adding the `ngSkipHydration` attribute to your root application component would effectively disable hydration for your entire application. Be careful and thoughtful about using this attribute. It is intended as a last resort workaround. Components that break hydration should be considered bugs that need to be fixed.


## Automated Setup with `ng add`

Angular CLI provides a streamlined way to integrate Tailwind CSS into your project using the `ng add` command. This command automatically installs the necessary packages, configures Tailwind CSS, and updates your project's build settings.

First, navigate to your Angular project's root directory in a terminal and run the following command:

```shell
ng add tailwindcss
```

This command performs the following actions:

- Installs `tailwindcss` and its peer dependencies.
- Configures the project to use Tailwind CSS.
- Adds the Tailwind CSS `@import` statement to your styles.

After running `ng add tailwindcss`, you can immediately start using Tailwind's utility classes in your component templates.


## Manual Setup (Alternative Method)

If you prefer to set up Tailwind CSS manually, follow these steps:


### 2. Install Tailwind CSS

Next, open a terminal in your Angular project's root directory and run the following command to install Tailwind CSS and its peer dependencies:

<docs-code-multifile>
  <docs-code header="npm" language="shell">
    npm install tailwindcss @tailwindcss/postcss postcss
  </docs-code>
  <docs-code header="yarn" language="shell">
    yarn add tailwindcss @tailwindcss/postcss postcss
  </docs-code>
  <docs-code header="pnpm" language="shell">
    pnpm add tailwindcss @tailwindcss/postcss postcss
  </docs-code>
  <docs-code header="bun" language="shell">
    bun add tailwindcss @tailwindcss/postcss postcss
  </docs-code>
</docs-code-multifile>


### 3. Configure PostCSS Plugins

Next, add a `.postcssrc.json` file in the file root of the project.
Add the `@tailwindcss/postcss` plugin into your PostCSS configuration.

```json {header: '.postcssrc.json'}
{
  "plugins": {
    "@tailwindcss/postcss": {}
  }
}
```
