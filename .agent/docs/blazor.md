---
library: blazor
version: 9.x
latest: true
category: frontend
official_docs: https://learn.microsoft.com/en-us/aspnet/core/blazor/
last_updated: 2026-03-21
source: auto-fetched from github-dir
source_url: https://api.github.com/repos/dotnet/AspNetCore.Docs/contents/aspnetcore/blazor
---

## call web api

---
title: Call a web API from an ASP.NET Core Blazor app
author: guardrex
description: Learn how to call a web API from Blazor apps.
monikerRange: '>= aspnetcore-3.1'
ms.author: wpickett
ms.custom: mvc
ms.date: 12/18/2025
uid: blazor/call-web-api
---

# Call a web API from ASP.NET Core Blazor

[!INCLUDE[](~/includes/not-latest-version.md)]

This article describes how to call a web API from a Blazor app.


## Server-side scenarios for calling external web APIs

Server-based components call external web APIs using <xref:System.Net.Http.HttpClient> instances, typically created using <xref:System.Net.Http.IHttpClientFactory>. For guidance that applies to server-side apps, see <xref:fundamentals/http-requests>.

A server-side app doesn't include an <xref:System.Net.Http.HttpClient> service. Provide an <xref:System.Net.Http.HttpClient> to the app using the [`HttpClient` factory infrastructure](xref:fundamentals/http-requests).

In the `Program` file:

```csharp
builder.Services.AddHttpClient();
```

The following Razor component makes a request to a web API for GitHub branches similar to the *Basic Usage* example in the <xref:fundamentals/http-requests> article.

`CallWebAPI.razor`:

```razor
@page "/call-web-api"
@using System.Text.Json
@using System.Text.Json.Serialization
@inject IHttpClientFactory ClientFactory

<h1>Call web API from a server-side Razor component</h1>

@if (getBranchesError || branches is null)
{
    <p>Unable to get branches from GitHub. Please try again later.</p>
}
else
{
    <ul>
        @foreach (var branch in branches)
        {
            <li>@branch.Name</li>
        }
    </ul>
}

@code {
    private IEnumerable<GitHubBranch>? branches = [];
    private bool getBranchesError;
    private bool shouldRender;

    protected override bool ShouldRender() => shouldRender;

    protected override async Task OnInitializedAsync()
    {
        using var request = new HttpRequestMessage(HttpMethod.Get,
            "https://api.github.com/repos/dotnet/AspNetCore.Docs/branches");
        request.Headers.Add("Accept", "application/vnd.github.v3+json");
        request.Headers.Add("User-Agent", "HttpClientFactory-Sample");

        var client = ClientFactory.CreateClient();

        using var response = await client.SendAsync(request);

        if (response.IsSuccessStatusCode)
        {
            using var responseStream = await response.Content.ReadAsStreamAsync();
            branches = await JsonSerializer.DeserializeAsync
                <IEnumerable<GitHubBranch>>(responseStream);
        }
        else
        {
            getBranchesError = true;
        }

        shouldRender = true;
    }

    public class GitHubBranch
    {
        [JsonPropertyName("name")]
        public string? Name { get; set; }
    }
}
```

In the preceding example for C# 12 or later, an empty array (`[]`) is created for the `branches` variable. For earlier versions of C# compiled with an SDK earlier than .NET 8, create an empty array (`Array.Empty<GitHubBranch>()`).

For an additional working example, see the server-side file upload example that uploads files to a web API controller in the <xref:blazor/file-uploads#upload-files-to-a-server-with-server-side-rendering> article.

:::moniker range=">= aspnetcore-8.0"


## Service abstractions for web API calls

*This section applies to Blazor Web Apps that maintain a web API in the server project or transform web API calls to an external web API.*

When using the interactive WebAssembly and Auto render modes, components are prerendered by default. Auto components are also initially rendered interactively from the server before the Blazor bundle downloads to the client and the client-side runtime activates. This means that components using these render modes should be designed so that they run successfully from both the client and the server. If the component must call a server project-based API or transform a request to an external web API (one that's outside of the Blazor Web App) when running on the client, the recommended approach is to abstract that API call behind a service interface and implement client and server versions of the service:

* The client version calls the web API with a preconfigured <xref:System.Net.Http.HttpClient>.
* The server version can typically access the server-side resources directly. Injecting an <xref:System.Net.Http.HttpClient> on the server that makes calls back to the server isn't recommended, as the network request is typically unnecessary. Alternatively, the API might be external to the server project, but a service abstraction for the server is required to transform the request in some way, for example to add an access token to a proxied request.

When using the WebAssembly render mode, you also have the option of disabling prerendering, so the components only render from the client. For more information, see <xref:blazor/components/prerender#disable-prerendering>.

Examples ([sample apps](#sample-apps)):

* Movie list web API in the `BlazorWebAppCallWebApi` sample app.
* Streaming rendering weather data web API in the `BlazorWebAppCallWebApi_Weather` sample app.
* Weather data returned to the client in either the `BlazorWebAppOidc` (non-BFF pattern) or `BlazorWebAppOidcBff` (BFF pattern) sample apps. These apps demonstrate secure (web) API calls. For more information, see <xref:blazor/security/blazor-web-app-oidc>.


## Blazor Web App external web APIs

*This section applies to Blazor Web Apps that call a web API maintained by a separate (external) project, possibly hosted on a different server.*

Blazor Web Apps normally prerender client-side WebAssembly components, and Auto components render on the server during static or interactive server-side rendering (SSR). <xref:System.Net.Http.HttpClient> services aren't registered by default in a Blazor Web App's main project. If the app is run with only the <xref:System.Net.Http.HttpClient> services registered in the `.Client` project, as described in the [Add the `HttpClient` service](#add-the-httpclient-service) section, executing the app results in a runtime error:

> :::no-loc text="InvalidOperationException: Cannot provide a value for property 'Http' on type '...{COMPONENT}'. There is no registered service of type 'System.Net.Http.HttpClient'.":::

Use ***either*** of the following approaches:

* Add the <xref:System.Net.Http.HttpClient> services to the server project to make the <xref:System.Net.Http.HttpClient> available during SSR. Use the following service registration in the server project's `Program` file:

  ```csharp
  builder.Services.AddHttpClient();
  ```

  <xref:System.Net.Http.HttpClient> services are provided by the shared framework, so a package reference in the app's project file isn't required.

  Example: Todo list web API in the `BlazorWebAppCallWebApi` [sample app](#sample-apps)

* If prerendering isn't required for a WebAssembly component that calls the web API, disable prerendering by following the guidance in <xref:blazor/components/prerender#disable-prerendering>. If you adopt this approach, you don't need to add <xref:System.Net.Http.HttpClient> services to the main project of the Blazor Web App because the component isn't prerendered on the server.

For more information, see the [Client-side services fail to resolve during prerendering](xref:blazor/components/prerender#client-side-services-fail-to-resolve-during-prerendering) section of the *Prerendering* article.


## Client-side scenarios for calling external web APIs

Client-based components call external web APIs using <xref:System.Net.Http.HttpClient> instances, typically created with a preconfigured <xref:System.Net.Http.HttpClient> registered in the `Program` file:

```csharp
builder.Services.AddScoped(sp => 
    new HttpClient
    { 
        BaseAddress = new Uri(builder.HostEnvironment.BaseAddress) 
    });
```

The following Razor component makes a request to a web API for GitHub branches similar to the *Basic Usage* example in the <xref:fundamentals/http-requests> article.

`CallWebAPI.razor`:

```razor
@page "/call-web-api"
@using System.Text.Json
@using System.Text.Json.Serialization
@inject HttpClient Client

<h1>Call web API from a Blazor WebAssembly Razor component</h1>

@if (getBranchesError || branches is null)
{
    <p>Unable to get branches from GitHub. Please try again later.</p>
}
else
{
    <ul>
        @foreach (var branch in branches)
        {
            <li>@branch.Name</li>
        }
    </ul>
}

@code {
    private IEnumerable<GitHubBranch>? branches = [];
    private bool getBranchesError;
    private bool shouldRender;

    protected override bool ShouldRender() => shouldRender;

    protected override async Task OnInitializedAsync()
    {
        using var request = new HttpRequestMessage(HttpMethod.Get,
            "https://api.github.com/repos/dotnet/AspNetCore.Docs/branches");
        request.Headers.Add("Accept", "application/vnd.github.v3+json");
        request.Headers.Add("User-Agent", "HttpClientFactory-Sample");

        using var response = await Client.SendAsync(request);

        if (response.IsSuccessStatusCode)
        {
            using var responseStream = await response.Content.ReadAsStreamAsync();
            branches = await JsonSerializer.DeserializeAsync
                <IEnumerable<GitHubBranch>>(responseStream);
        }
        else
        {
            getBranchesError = true;
        }

        shouldRender = true;
    }

    public class GitHubBranch
    {
        [JsonPropertyName("name")]
        public string? Name { get; set; }
    }
}
```

In the preceding example for C# 12 or later, an empty array (`[]`) is created for the `branches` variable. For earlier versions of C# compiled with an SDK earlier than .NET 8, create an empty array (`Array.Empty<GitHubBranch>()`).

<!-- A version of the following content is also in the 
     Security > WebAssembly > Overview article under 
     the heading: "Web API requests" -->

To protect .NET/C# code and data, use [ASP.NET Core Data Protection](xref:security/data-protection/introduction) features with a server-side ASP.NET Core backend web API. The client-side Blazor WebAssembly app calls the server-side web API for secure app features and data processing.

Blazor WebAssembly apps are often prevented from making direct calls across origins to web APIs due to [Cross-Origin Request Sharing (CORS) security](#cross-origin-resource-sharing-cors). A typical exception looks like the following:

> :::no-loc text="Access to fetch at '{URL}' from origin 'https://localhost:{PORT}' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource. If an opaque response serves your needs, set the request's mode to 'no-cors' to fetch the resource with CORS disabled.":::

Even if you call <xref:Microsoft.AspNetCore.Components.WebAssembly.Http.WebAssemblyHttpRequestMessageExtensions.SetBrowserRequestMode%2A> with a <xref:Microsoft.AspNetCore.Components.WebAssembly.Http.BrowserRequestMode> field of `NoCors` (1) seeking to circumvent the preceding exception, the request often fails due to CORS restrictions on the web API's origin, such as a restriction that only allows calls from specific origins or a restriction that prevents JavaScript [`fetch`](https://developer.mozilla.org/docs/Web/API/Fetch_API/Using_Fetch) requests from a browser. The only way for such calls to succeed is for the web API that you're calling to allow your origin to call its origin with the correct CORS configuration. Most external web APIs don't allow you to configure their CORS policies. To deal with this restriction, adopt either of the following strategies:

* Maintain your own server-side ASP.NET Core backend web API. The client-side Blazor WebAssembly app calls your server-side web API, and your web API makes the request from its server-based C# code (not a browser) to the external web API with the correct CORS headers, returning the result to your client-side Blazor WebAssembly app.

* Use a proxy service to proxy the request from the client-side Blazor WebAssembly app to the external web API. The proxy service uses a server-side app to make the request on the client's behalf and returns the result after the call succeeds. In the following example based on [CloudFlare's CORS PROXY](https://corsproxy.io/), the `{REQUEST URI}` placeholder is the request URI:

  ```razor
  @using System.Net
  @inject IHttpClientFactory ClientFactory

  ...

  @code {
      public async Task CallApi()
      {
          var client = ClientFactory.CreateClient();

          var urlEncodedRequestUri = WebUtility.UrlEncode("{REQUEST URI}");

          using var request = new HttpRequestMessage(HttpMethod.Get, 
              $"https://corsproxy.io/?{urlEncodedRequestUri}");

          using var response = await client.SendAsync(request);

          ...
      }
  }
  ```


## DELETE (`DeleteAsync`) and additional extension methods

<xref:System.Net.Http> includes additional extension methods for sending HTTP requests and receiving HTTP responses. <xref:System.Net.Http.HttpClient.DeleteAsync%2A?displayProperty=nameWithType> is used to send an HTTP DELETE request to a web API.

In the following component code, the `<button>` element calls the `DeleteItem` method. The bound `<input>` element supplies the `id` of the item to delete.

```csharp
await Http.DeleteAsync($"todoitems/{id}");
```

:::moniker range=">= aspnetcore-9.0"


## Use a token handler for web API calls

Blazor Web Apps with OIDC authentication can use a token handler approach to make outgoing requests to secure external web API calls. This approach is used by the `BlazorWebAppOidc` and `BlazorWebAppOidcServer` sample apps described in the *Sample apps* section of this article.

For more information, see the following resources:

* <xref:blazor/security/additional-scenarios#use-a-token-handler-for-web-api-calls>
* *Secure an ASP.NET Core Blazor Web App with OpenID Connect (OIDC)*
  * [Without YARP and Aspire (Interactive Auto)](xref:blazor/security/blazor-web-app-oidc?pivots=without-yarp-and-aspire)
  * [Without YARP and Aspire (Interactive Server)](xref:blazor/security/blazor-web-app-oidc?pivots=without-yarp-and-aspire-server)


## Blazor framework component examples for testing web API access

Various network tools are publicly available for testing web API backend apps directly, such as [Firefox Browser Developer](https://www.mozilla.org/firefox/developer/). Blazor framework's reference source includes <xref:System.Net.Http.HttpClient> test assets that are useful for testing:

[`HttpClientTest` assets in the `dotnet/aspnetcore` GitHub repository](https://github.com/dotnet/aspnetcore/tree/main/src/Components/test/testassets/BasicTestApp/HttpClientTest)

[!INCLUDE[](~/includes/aspnetcore-repo-ref-source-links.md)]

:::moniker range=">= aspnetcore-8.0"


### `BlazorWebAppCallWebApi_Weather`

A weather data sample app that uses streaming rendering for weather data.


### `BlazorWebAssemblyCallWebApi`

Calls a todo list web API from a Blazor WebAssembly app:

* `Backend`: A web API app for maintaining a todo list, based on [Minimal APIs](xref:fundamentals/minimal-apis).
* `BlazorTodo`: A Blazor WebAssembly app that calls the web API with a preconfigured <xref:System.Net.Http.HttpClient> for todo list CRUD operations.


### Small payload size with fast initial load time

:::moniker range=">= aspnetcore-8.0"

Rendering components from the server reduces the app payload size and improves initial load times. When a fast initial load time is desired, use the Blazor Server hosting model or consider static server-side rendering.

:::moniker-end

:::moniker range="< aspnetcore-8.0"

Blazor Server apps have relatively small payload sizes with faster initial load times. When a fast initial load time is desired, adopt Blazor Server.

:::moniker-end


## Prerequisites

This section explains the prerequisites for debugging.


### Browser prerequisites

:::moniker range=">= aspnetcore-8.0"

The latest version of the following browsers:

* Google Chrome
* Microsoft Edge
* Firefox (browser developer tools only)

:::moniker-end

:::moniker range="< aspnetcore-8.0"

Debugging requires the latest version of the following browsers:

* Google Chrome (default)
* Microsoft Edge

:::moniker-end

Ensure that firewalls or proxies don't block communication with the debug proxy (`NodeJS` process). For more information, see the [Firewall configuration](#firewall-configuration) section.

> [!NOTE]
> Apple Safari on macOS isn't currently supported.


### IDE prerequisites

The latest version of Visual Studio or Visual Studio Code is required.


### Visual Studio Code prerequisites

Visual Studio Code requires the [C# Dev Kit for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-dotnettools.csdevkit) ([Getting Started with C# in VS Code](https://code.visualstudio.com/docs/csharp/get-started)). In the Visual Studio Code Extensions Marketplace, filter the extension list with "`c# dev kit`" to locate the extension:

![C# Dev Kit in the Visual Studio Code Extensions Marketplace](~/blazor/debug/_static/csharp-dev-kit.png)

Installing the C# Dev Kit automatically installs the following additional extensions:

* [.NET Install Tool](https://marketplace.visualstudio.com/items?itemName=ms-dotnettools.vscode-dotnet-runtime)
* [C#](https://marketplace.visualstudio.com/items?itemName=ms-dotnettools.csharp)
* [IntelliCode for C# Dev Kit](https://marketplace.visualstudio.com/items?itemName=ms-dotnettools.vscodeintellicode-csharp)

If you encounter warnings or errors, you can [open an issue (`microsoft/vscode-dotnettools` GitHub repository)](https://github.com/microsoft/vscode-dotnettools/issues) describing the problem.


### App configuration prerequisites

*The guidance in this subsection applies to client-side debugging.*
 
Open the `Properties/launchSettings.json` file of the startup project. Confirm the presence of the following `inspectUri` property in each launch profile of the file's `profiles` node. If the following property isn't present, add it to each profile:

```json
"inspectUri": "{wsProtocol}://{url.hostname}:{url.port}/_framework/debug/ws-proxy?browser={browserInspectUri}"
```

The `inspectUri` property:

* Enables the IDE to detect that the app is a Blazor app.
* Instructs the script debugging infrastructure to connect to the browser through Blazor's debugging proxy.

The placeholder values for the WebSocket protocol (`wsProtocol`), host (`url.hostname`), port (`url.port`), and inspector URI on the launched browser (`browserInspectUri`) are provided by the framework.


### Breakpoints in `OnInitialized{Async}` not hit

The Blazor framework's debugging proxy doesn't launch instantly on app startup, so breakpoints in the [`OnInitialized{Async}` lifecycle methods](xref:blazor/components/lifecycle#component-initialization-oninitializedasync) might not be hit. We recommend adding a delay at the start of the method body to give the debug proxy some time to launch before the breakpoint is hit. You can include the delay based on an [`if` compiler directive](/dotnet/csharp/language-reference/preprocessor-directives/preprocessor-if) to ensure that the delay isn't present for a release build of the app.

<xref:Microsoft.AspNetCore.Components.ComponentBase.OnInitialized%2A>:

```csharp
protected override void OnInitialized()
{
#if DEBUG
    Thread.Sleep(10000);
#endif

    ...
}
```

<xref:Microsoft.AspNetCore.Components.ComponentBase.OnInitializedAsync%2A>:

```csharp
protected override async Task OnInitializedAsync()
{
#if DEBUG
    await Task.Delay(10000);
#endif

    ...
}
```


## Prerequisites

Before diving into the implementation, ensure the necessary tools are installed. The [.NET SDK 8.0 or later](https://dotnet.microsoft.com/download) is required.


## Build a Blazor movie database app tutorial

For a tutorial experience building an app that uses EF Core for database operations, see <xref:blazor/tutorials/movie-database-app/index>. The tutorial shows you how to create a Blazor Web App that can display and manage movies in a movie database.

:::moniker-end
