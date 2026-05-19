---
library: clerk
version: latest
latest: true
category: backend
official_docs: https://clerk.com/docs
last_updated: 2026-03-21
source: auto-fetched from llms-full
source_url: https://clerk.com/docs/llms-full.txt
---

## Installation

<Tabs items={["JS Backend SDK", "With other SDKs"]}>
  <Tab>
    If you are using the JS Backend SDK on its own, you can install it using the following command:

    ```npm {{ filename: 'terminal' }}
    npm install @clerk/backend
    ```
  </Tab>

  <Tab>
    Clerk SDKs expose an instance of the JS Backend SDK for use in server environments, so there is no need to install it separately.
  </Tab>
</Tabs>


## Installation

1. To get started, install the `@clerk/ui` package.

   ```npm
   npm install @clerk/ui
   ```
2. To use a theme, import it from `@clerk/ui` and apply it using the <SDKLink href="/docs/:sdk:/guides/customizing-clerk/appearance-prop/overview" sdks={["astro","chrome-extension","expo","nextjs","nuxt","react","react-router","remix","tanstack-react-start","vue","js-frontend","fastify","expressjs","js-backend","go","ruby"]} code={true}>appearance prop</SDKLink>.


## Installation

1. To get started, install the `@clerk/ui` package.

   ```npm
   npm install @clerk/ui
   ```
2. To use a theme, import it from `@clerk/ui` and apply it using the <SDKLink href="/docs/:sdk:/guides/customizing-clerk/appearance-prop/overview" sdks={["astro","chrome-extension","expo","nextjs","nuxt","react","react-router","remix","tanstack-react-start","vue","js-frontend","fastify","expressjs","js-backend","go","ruby"]} code={true}>appearance prop</SDKLink>.


## Installation

1. To get started, install the `@clerk/ui` package.

   ```npm
   npm install @clerk/ui
   ```
2. To use a theme, import it from `@clerk/ui` and apply it using the <SDKLink href="/docs/:sdk:/guides/customizing-clerk/appearance-prop/overview" sdks={["astro","chrome-extension","expo","nextjs","nuxt","react","react-router","remix","tanstack-react-start","vue","js-frontend","fastify","expressjs","js-backend","go","ruby"]} code={true}>appearance prop</SDKLink>.


## Methods


### `<TaskSetupMFA />`

* <SDKLink href="/docs/:sdk:/reference/components/authentication/task-setup-mfa#mount-task-setup-mfa" sdks={["js-frontend","nextjs","react","react-router","tanstack-react-start"]} code={true}>mountTaskSetupMFA()</SDKLink>
* <SDKLink href="/docs/:sdk:/reference/components/authentication/task-setup-mfa#unmount-task-setup-mfa" sdks={["js-frontend","nextjs","react","react-router","tanstack-react-start"]} code={true}>unmountTaskSetupMFA()</SDKLink>

[client-ref]: /docs/reference/objects/client

[session-ref]: /docs/reference/objects/session

[user-ref]: /docs/reference/objects/user

[organization-ref]: /docs/reference/objects/organization

[api-ref]: /docs/reference/objects/api-keys

[billing-ref]: /docs/reference/objects/billing

[components-ref]: /docs/reference/components/overview

[ap-ref]: /docs/guides/account-portal/overview

---
title: "`SignInFuture` object"
description: The SignInFuture object holds the state of the current sign-in and
  provides helper methods to navigate and complete the sign-in process.
sdk: js-frontend, astro, chrome-extension, expo, nextjs, react, react-router,
  tanstack-react-start, nuxt, vue
sdkScoped: "true"
canonical: /docs/:sdk:/reference/objects/sign-in-future
lastUpdated: 2026-03-19T19:28:59.000Z
availableSdks: js-frontend,astro,chrome-extension,expo,nextjs,react,react-router,tanstack-react-start,nuxt,vue
notAvailableSdks: android,ios,expressjs,fastify,remix,go,ruby,js-backend
activeSdk: vue
sourceFile: /docs/reference/objects/sign-in-future.mdx
---

> \[!IMPORTANT]
> The APIs described here are stable, and will become the default in the next major version of `clerk-js`.

The `SignInFuture` object holds the state of the current sign-in and provides helper methods to navigate and complete the sign-in process. It is used to manage the sign-in lifecycle, including the first and second factor verification, and the creation of a new session.


### `initializePaymentMethod()`

Initializes a payment method for the Organization.

```ts
function initializePaymentMethod(params): Promise<BillingInitializedPaymentMethod>
```


### `initializePaymentMethod()`

Initializes a payment method for the user.

```ts
function initializePaymentMethod(params): Promise<BillingInitializedPaymentMethod>
```


## Installation

1. To get started, install the `@clerk/ui` package.

   ```npm
   npm install @clerk/ui
   ```
2. To use a theme, import it from `@clerk/ui` and apply it using the <SDKLink href="/docs/:sdk:/guides/customizing-clerk/appearance-prop/overview" sdks={["astro","chrome-extension","expo","nextjs","nuxt","react","react-router","remix","tanstack-react-start","vue","js-frontend","fastify","expressjs","js-backend","go","ruby"]} code={true}>appearance prop</SDKLink>.


### `initializePaymentMethod()`

Initializes a payment method for the Organization.

```ts
function initializePaymentMethod(params): Promise<BillingInitializedPaymentMethod>
```


### `<TaskSetupMFA />`

* <SDKLink href="/docs/:sdk:/reference/components/authentication/task-setup-mfa#mount-task-setup-mfa" sdks={["js-frontend","nextjs","react","react-router","tanstack-react-start"]} code={true}>mountTaskSetupMFA()</SDKLink>
* <SDKLink href="/docs/:sdk:/reference/components/authentication/task-setup-mfa#unmount-task-setup-mfa" sdks={["js-frontend","nextjs","react","react-router","tanstack-react-start"]} code={true}>unmountTaskSetupMFA()</SDKLink>

[client-ref]: /docs/reference/objects/client

[session-ref]: /docs/reference/objects/session

[user-ref]: /docs/reference/objects/user

[organization-ref]: /docs/reference/objects/organization

[api-ref]: /docs/reference/objects/api-keys

[billing-ref]: /docs/reference/objects/billing

[components-ref]: /docs/reference/components/overview

[ap-ref]: /docs/guides/account-portal/overview

---
title: "`Session` object"
description: The Session object is an abstraction over an HTTP session. It
  models the period of information exchange between a user and the server.
search:
  rank: 1
  keywords:
    - getToken()
sdk: js-frontend, astro, chrome-extension, expo, nextjs, react, react-router,
  tanstack-react-start, nuxt, vue
sdkScoped: "true"
canonical: /docs/:sdk:/reference/objects/session
lastUpdated: 2026-03-19T19:28:59.000Z
availableSdks: js-frontend,astro,chrome-extension,expo,nextjs,react,react-router,tanstack-react-start,nuxt,vue
notAvailableSdks: android,ios,expressjs,fastify,remix,go,ruby,js-backend
activeSdk: nuxt
sourceFile: /docs/reference/objects/session.mdx
---

The `Session` object is an abstraction over an HTTP session. It models the period of information exchange between a user and the server.

The `Session` object includes methods for recording session activity and ending the session client-side. For security reasons, sessions can also expire server-side.

As soon as a <SDKLink href="/docs/:sdk:/reference/objects/user" sdks={["js-frontend","astro","chrome-extension","expo","nextjs","react","react-router","tanstack-react-start","nuxt","vue"]} code={true}>User</SDKLink> signs in, Clerk creates a `Session` for the current <SDKLink href="/docs/:sdk:/reference/objects/client" sdks={["js-frontend","astro","chrome-extension","expo","nextjs","react","react-router","tanstack-react-start","nuxt","vue"]} code={true}>Client</SDKLink>. Clients can have more than one sessions at any point in time, but only one of those sessions will be **active**.

In certain scenarios, a session might be replaced by another one. This is often the case with [multi-session applications](/docs/guides/secure/session-options#multi-session-applications).

All sessions that are **expired**, **removed**, **replaced**, **ended** or **abandoned** are not considered valid.

> \[!NOTE]
> For more information regarding the different session states, see the [guide on session management](/docs/guides/secure/session-options).


### `initializePaymentMethod()`

Initializes a payment method for the user.

```ts
function initializePaymentMethod(params): Promise<BillingInitializedPaymentMethod>
```


## Installation

1. To get started, install the `@clerk/ui` package.

   ```npm
   npm install @clerk/ui
   ```
2. To use a theme, import it from `@clerk/ui` and apply it using the <SDKLink href="/docs/:sdk:/guides/customizing-clerk/appearance-prop/overview" sdks={["astro","chrome-extension","expo","nextjs","nuxt","react","react-router","remix","tanstack-react-start","vue","js-frontend","fastify","expressjs","js-backend","go","ruby"]} code={true}>appearance prop</SDKLink>.


### `<TaskSetupMFA />`

* <SDKLink href="/docs/:sdk:/reference/components/authentication/task-setup-mfa#mount-task-setup-mfa" sdks={["js-frontend","nextjs","react","react-router","tanstack-react-start"]} code={true}>mountTaskSetupMFA()</SDKLink>
* <SDKLink href="/docs/:sdk:/reference/components/authentication/task-setup-mfa#unmount-task-setup-mfa" sdks={["js-frontend","nextjs","react","react-router","tanstack-react-start"]} code={true}>unmountTaskSetupMFA()</SDKLink>

[client-ref]: /docs/reference/objects/client

[session-ref]: /docs/reference/objects/session

[user-ref]: /docs/reference/objects/user

[organization-ref]: /docs/reference/objects/organization

[api-ref]: /docs/reference/objects/api-keys

[billing-ref]: /docs/reference/objects/billing

[components-ref]: /docs/reference/components/overview

[ap-ref]: /docs/guides/account-portal/overview

---
title: "`Organization` object"
description: The Organization object holds information about an Organization, as
  well as methods for managing it.
sdk: js-frontend, astro, chrome-extension, expo, nextjs, react, react-router,
  tanstack-react-start, nuxt, vue
sdkScoped: "true"
canonical: /docs/:sdk:/reference/objects/organization
lastUpdated: 2026-03-19T19:28:59.000Z
availableSdks: js-frontend,astro,chrome-extension,expo,nextjs,react,react-router,tanstack-react-start,nuxt,vue
notAvailableSdks: android,ios,expressjs,fastify,remix,go,ruby,js-backend
activeSdk: astro
sourceFile: /docs/reference/objects/organization.mdx
---

The `Organization` object holds information about an Organization, as well as methods for managing it.

To use these methods, you must have the **Organizations** feature [enabled in your app's settings in the Clerk Dashboard](/docs/guides/organizations/configure#enable-organizations).


### `initializePaymentMethod()`

Initializes a payment method for the Organization.

```ts
function initializePaymentMethod(params): Promise<BillingInitializedPaymentMethod>
```


### `initializePaymentMethod()`

Initializes a payment method for the user.

```ts
function initializePaymentMethod(params): Promise<BillingInitializedPaymentMethod>
```


## Installation

If you're using Go Modules and have a `go.mod` file in your project's root, you can import `clerk-sdk-go` directly in your `.go` files:

```go
import (
  "github.com/clerk/clerk-sdk-go/v2"
)
```

Alternatively, you can `go get` the package explicitly and it will add the necessary dependencies to your `go.mod` file:

```sh {{ filename: 'terminal' }}
go get -u github.com/clerk/clerk-sdk-go/v2
```


## Installation

1. To get started, install the `@clerk/ui` package.

   ```npm
   npm install @clerk/ui
   ```
2. To use a theme, import it from `@clerk/ui` and apply it using the <SDKLink href="/docs/:sdk:/guides/customizing-clerk/appearance-prop/overview" sdks={["astro","chrome-extension","expo","nextjs","nuxt","react","react-router","remix","tanstack-react-start","vue","js-frontend","fastify","expressjs","js-backend","go","ruby"]} code={true}>appearance prop</SDKLink>.


## Installation

1. To get started, install the `@clerk/ui` package.

   ```npm
   npm install @clerk/ui
   ```
2. To use a theme, import it from `@clerk/ui` and apply it using the <SDKLink href="/docs/:sdk:/guides/customizing-clerk/appearance-prop/overview" sdks={["astro","chrome-extension","expo","nextjs","nuxt","react","react-router","remix","tanstack-react-start","vue","js-frontend","fastify","expressjs","js-backend","go","ruby"]} code={true}>appearance prop</SDKLink>.


## When to use `<TaskSetupMFA />`

Clerk's sign-in flows, such as the [Sign-in Account Portal page](/docs/guides/account-portal/overview#sign-in), <SDKLink href="/docs/:sdk:/reference/components/unstyled/sign-in-button" sdks={["astro","chrome-extension","expo","nextjs","nuxt","react","react-router","remix","tanstack-react-start","vue"]} code={true}>\<SignInButton /></SDKLink>, and <SDKLink href="/docs/:sdk:/reference/components/authentication/sign-in" sdks={["astro","chrome-extension","expo","nextjs","nuxt","react","react-router","remix","tanstack-react-start","vue","js-frontend"]} code={true}>\<SignIn /></SDKLink> component, automatically handle the `setup-mfa` session task flow for you, including rendering the `<TaskSetupMFA />` component when needed.

If you want to customize the route where the `<TaskSetupMFA />` component is rendered or customize its appearance, you can host it yourself within your application.

<If notSdk="js-frontend">
  ## Example

  The following example demonstrates how to host the `<TaskSetupMFA />` component on a custom page. You first need to [set the `taskUrls` option on your Clerk integration](/docs/guides/configure/session-tasks#using-the-task-urls-option) so that users are redirected to the page where you host the `<TaskSetupMFA />` component when they have a pending `setup-mfa` session task.

  <If sdk="tanstack-react-start">
    > \[!NOTE]
    > To see the full `__root.tsx` setup you need for Clerk with TanStack React Start, see the <SDKLink href="/docs/tanstack-react-start/getting-started/quickstart" sdks={["tanstack-react-start"]}>TanStack React Start quickstart</SDKLink>.

    ```tsx {{ filename: 'src/routes/__root.tsx', mark: [12] }}
    import * as React from 'react'
    import { HeadContent, Scripts } from '@tanstack/react-router'
    import { ClerkProvider } from '@clerk/tanstack-react-start'

    function RootDocument({ children }: { children: React.ReactNode }) {
      return (
        <html>
          <head>
            <HeadContent />
          </head>
          <body>
            <ClerkProvider taskUrls={{ 'setup-mfa': '/session-tasks/setup-mfa' }}>
              {children}
            </ClerkProvider>
            <Scripts />
          </body>
        </html>
      )
    }
    ```

    ```tsx {{ filename: 'src/routes/session-tasks/setup-mfa.tsx' }}
    import { TaskSetupMFA } from '@clerk/tanstack-react-start'
    import { createFileRoute } from '@tanstack/react-router'

    export const Route = createFileRoute('/session-tasks/setup-mfa')({
      component: SetupMfaPage,
    })

    function SetupMfaPage() {
      return <TaskSetupMFA redirectUrlComplete="/dashboard" />
    }
    ```
  </If>
</If>


### Infinite pagination

The following example demonstrates how to use the `infinite` property to fetch and append new data to the existing list. The `memberships` attribute will be populated with the first page of the Organization's memberships. When the "Load more" button is clicked, the `fetchNext` helper function will be called to append the next page of memberships to the list.

<If sdk="tanstack-react-start">
  ```tsx {{ filename: 'app/routes/members.tsx' }}
  import { useOrganization } from '@clerk/tanstack-react-start'
  import { createFileRoute } from '@tanstack/react-router'

  export const Route = createFileRoute('/members')({
    component: MemberListPage,
  })

  export default function MemberListPage() {
    const { memberships } = useOrganization({
      memberships: {
        infinite: true, // Append new data to the existing list
        keepPreviousData: true, // Persist the cached data until the new data has been fetched
      },
    })

    // Handle loading state
    if (!memberships) return <div>Loading...</div>

    return (
      <div>
        <h2>Organization members</h2>
        <ul>
          {memberships.data?.map((membership) => (
            <li key={membership.id}>
              {membership.publicUserData?.firstName} {membership.publicUserData?.lastName} &lt;
              {membership.publicUserData?.identifier}&gt; :: {membership.role}
            </li>
          ))}
        </ul>

        <button
          disabled={!memberships.hasNextPage} // Disable the button if there are no more available pages to be fetched
          onClick={memberships.fetchNext}
        >
          Load more
        </button>
      </div>
    )
  }
  ```
</If>


### Infinite pagination

The following example demonstrates how to use the `infinite` property to fetch and append new data to the existing list. The `userMemberships` attribute will be populated with the first page of the user's Organization memberships. When the "Load more" button is clicked, the `fetchNext` helper function will be called to append the next page of memberships to the list.

<If sdk="tanstack-react-start">
  ```tsx {{ filename: 'components/JoinedOrganizations.tsx' }}
  import { useOrganizationList } from '@clerk/tanstack-react-start'

  export function JoinedOrganizations() {
    const { isLoaded, setActive, userMemberships } = useOrganizationList({
      userMemberships: {
        infinite: true,
      },
    })

    // Handle loading state
    if (!isLoaded) return <div>Loading...</div>

    return (
      <>
        <ul>
          {userMemberships.data?.map((mem) => (
            <li key={mem.id}>
              <span>{mem.organization.name}</span>
              <button onClick={() => setActive({ organization: mem.organization.id })}>Select</button>
            </li>
          ))}
        </ul>

        <button disabled={!userMemberships.hasNextPage} onClick={() => userMemberships.fetchNext()}>
          Load more
        </button>
      </>
    )
  }
  ```
</If>


### `<TaskSetupMFA />`

* <SDKLink href="/docs/:sdk:/reference/components/authentication/task-setup-mfa#mount-task-setup-mfa" sdks={["js-frontend","nextjs","react","react-router","tanstack-react-start"]} code={true}>mountTaskSetupMFA()</SDKLink>
* <SDKLink href="/docs/:sdk:/reference/components/authentication/task-setup-mfa#unmount-task-setup-mfa" sdks={["js-frontend","nextjs","react","react-router","tanstack-react-start"]} code={true}>unmountTaskSetupMFA()</SDKLink>

[client-ref]: /docs/reference/objects/client

[session-ref]: /docs/reference/objects/session

[user-ref]: /docs/reference/objects/user

[organization-ref]: /docs/reference/objects/organization

[api-ref]: /docs/reference/objects/api-keys

[billing-ref]: /docs/reference/objects/billing

[components-ref]: /docs/reference/components/overview

[ap-ref]: /docs/guides/account-portal/overview

---
title: "`Billing` object"
description: The Billing object provides methods for managing billing for a user
  or organization.
sdk: js-frontend, astro, chrome-extension, expo, nextjs, react, react-router,
  tanstack-react-start, nuxt, vue
sdkScoped: "true"
canonical: /docs/:sdk:/reference/objects/billing
lastUpdated: 2026-03-19T19:28:59.000Z
availableSdks: js-frontend,astro,chrome-extension,expo,nextjs,react,react-router,tanstack-react-start,nuxt,vue
notAvailableSdks: android,ios,expressjs,fastify,remix,go,ruby,js-backend
activeSdk: tanstack-react-start
sourceFile: /docs/reference/objects/billing.mdx
---

> \[!WARNING]
>
> Billing is currently in Beta and its APIs are experimental and may undergo breaking changes. To mitigate potential disruptions, we recommend [pinning](/docs/pinning) your SDK and `clerk-js` package versions.

The `Billing` object provides methods for managing billing for a user or organization.

> \[!NOTE]
> If an `orgId` parameter is not provided, the methods will automatically use the current user's ID.


### `initializePaymentMethod()`

Initializes a payment method for the Organization.

```ts
function initializePaymentMethod(params): Promise<BillingInitializedPaymentMethod>
```


### `initializePaymentMethod()`

Initializes a payment method for the user.

```ts
function initializePaymentMethod(params): Promise<BillingInitializedPaymentMethod>
```


## Installation

1. To get started, install the `@clerk/ui` package.

   ```npm
   npm install @clerk/ui
   ```
2. To use a theme, import it from `@clerk/ui` and apply it using the <SDKLink href="/docs/:sdk:/guides/customizing-clerk/appearance-prop/overview" sdks={["astro","chrome-extension","expo","nextjs","nuxt","react","react-router","remix","tanstack-react-start","vue","js-frontend","fastify","expressjs","js-backend","go","ruby"]} code={true}>appearance prop</SDKLink>.


# Reverification preset is set to `LAX`
use Clerk::Rack::Reverification,
  preset: Clerk::StepUp::Preset::LAX,
  routes: ["/*"]

run App.new
```


## Getting started


### Installation

```shell
