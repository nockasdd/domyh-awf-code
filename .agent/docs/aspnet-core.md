---
library: aspnet-core
version: 9.x
latest: true
category: backend
official_docs: https://learn.microsoft.com/en-us/aspnet/core/
last_updated: 2026-03-21
source: auto-fetched from github-dir
source_url: https://api.github.com/repos/dotnet/AspNetCore.Docs/contents/aspnetcore/fundamentals
---

# Make HTTP requests using IHttpClientFactory in ASP.NET Core

[!INCLUDE[](~/includes/not-latest-version.md)]

:::moniker range=">= aspnetcore-6.0"

By [Kirk Larkin](https://github.com/serpent5), [Steve Gordon](https://github.com/stevejgordon), [Glenn Condron](https://github.com/glennc), and [Ryan Nowak](https://github.com/rynowak).

An <xref:System.Net.Http.IHttpClientFactory> can be registered and used to configure and create <xref:System.Net.Http.HttpClient> instances in an app. `IHttpClientFactory` offers the following benefits:

* Provides a central location for naming and configuring logical `HttpClient` instances. For example, a client named  *github* could be registered and configured to access [GitHub](https://github.com/). A default client can be registered for general access.
* Codifies the concept of outgoing middleware via delegating handlers in `HttpClient`. Provides extensions for Polly-based middleware to take advantage of delegating handlers in `HttpClient`.
* Manages the pooling and lifetime of underlying `HttpClientMessageHandler` instances. Automatic management avoids common DNS (Domain Name System) problems that occur when manually managing `HttpClient` lifetimes.
* Adds a configurable logging experience (via `ILogger`) for all requests sent through clients created by the factory.

The sample code in this topic version uses <xref:System.Text.Json> to deserialize JSON content returned in HTTP responses. For samples that use `Json.NET` and `ReadAsAsync<T>`, use the version selector to select a 2.x version of this topic.


## Prerequisites

Projects targeting .NET Framework require installation of the [Microsoft.Extensions.Http](https://www.nuget.org/packages/Microsoft.Extensions.Http/) NuGet package. Projects that target .NET Core and reference the [Microsoft.AspNetCore.App metapackage](xref:fundamentals/metapackage-app) already include the `Microsoft.Extensions.Http` package.


### ASP.NET Core endpoint definition

An ASP.NET Core endpoint is:

* Executable: Has a <xref:Microsoft.AspNetCore.Http.Endpoint.RequestDelegate>.
* Extensible: Has a [Metadata](xref:Microsoft.AspNetCore.Http.Endpoint.Metadata%2A) collection.
* Selectable: Optionally, has [routing information](xref:Microsoft.AspNetCore.Routing.RouteEndpoint.RoutePattern%2A).
* Enumerable: The collection of endpoints can be listed by retrieving the <xref:Microsoft.AspNetCore.Routing.EndpointDataSource> from [DI](xref:fundamentals/dependency-injection).

The following code shows how to retrieve and inspect the endpoint matching the current request:

:::code language="csharp" source="~/fundamentals/routing/samples/6.x/RoutingSample/Snippets/Program.cs" id="snippet_InspectEndpointMiddleware":::

The endpoint, if selected, can be retrieved from the `HttpContext`. Its properties can be inspected. Endpoint objects are immutable and cannot be modified after creation. The most common type of endpoint is a <xref:Microsoft.AspNetCore.Routing.RouteEndpoint>. `RouteEndpoint` includes information that allows it to be selected by the routing system.

In the preceding code, [app.Use](xref:Microsoft.AspNetCore.Builder.UseExtensions.Use%2A) configures an inline [middleware](xref:fundamentals/middleware/index).

<a name="mt"></a>

The following code shows that, depending on where `app.Use` is called in the pipeline, there may not be an endpoint:

:::code language="csharp" source="~/fundamentals/routing/samples/6.x/RoutingSample/Snippets/Program.cs" id="snippet_CurrentEndpointMiddlewareOrder":::

The preceding sample adds `Console.WriteLine` statements that display whether or not an endpoint has been selected. For clarity, the sample assigns a display name to the provided `/` endpoint.

The preceding sample also includes calls to `UseRouting` and `UseEndpoints` to control exactly when these middleware run within the pipeline.

Running this code with a URL of `/` displays:

```txt
1. Endpoint: (null)
2. Endpoint: Hello
3. Endpoint: Hello
```

Running this code with any other URL displays:

```txt
1. Endpoint: (null)
2. Endpoint: (null)
4. Endpoint: (null)
```

This output demonstrates that:

* The endpoint is always null before `UseRouting` is called.
* If a match is found, the endpoint is non-null between `UseRouting` and <xref:Microsoft.AspNetCore.Builder.EndpointRoutingApplicationBuilderExtensions.UseEndpoints%2A>.
* The `UseEndpoints` middleware is **terminal** when a match is found. [Terminal middleware](#tm) is defined later in this article.
* The middleware after `UseEndpoints` execute only when no match is found.

The `UseRouting` middleware uses the <xref:Microsoft.AspNetCore.Http.EndpointHttpContextExtensions.SetEndpoint%2A> method to attach the endpoint to the current context. It's possible to replace the `UseRouting` middleware with custom logic and still get the benefits of using endpoints. Endpoints are a low-level primitive like middleware, and aren't coupled to the routing implementation. Most apps don't need to replace `UseRouting` with custom logic.

The `UseEndpoints` middleware is designed to be used in tandem with the `UseRouting` middleware. The core logic to execute an endpoint isn't complicated. Use <xref:Microsoft.AspNetCore.Http.EndpointHttpContextExtensions.GetEndpoint%2A> to retrieve the endpoint, and then invoke its <xref:Microsoft.AspNetCore.Http.Endpoint.RequestDelegate> property.

The following code demonstrates how middleware can influence or react to routing:

:::code language="csharp" source="~/fundamentals/routing/samples/6.x/RoutingSample/Snippets/Program.cs" id="snippet_RequiresAudit":::
:::code language="csharp" source="~/fundamentals/routing/samples/6.x/RoutingSample/Snippets/RequiresAuditAttribute.cs" id="snippet_Class":::

The preceding example demonstrates two important concepts:

* Middleware can run before `UseRouting` to modify the data that routing operates upon.
  * Usually middleware that appears before routing modifies some property of the request, such as <xref:Microsoft.AspNetCore.Builder.RewriteBuilderExtensions.UseRewriter%2A>, <xref:Microsoft.AspNetCore.Builder.HttpMethodOverrideExtensions.UseHttpMethodOverride%2A>, or <xref:Microsoft.AspNetCore.Builder.UsePathBaseExtensions.UsePathBase%2A>.
* Middleware can run between `UseRouting` and <xref:Microsoft.AspNetCore.Builder.EndpointRoutingApplicationBuilderExtensions.UseEndpoints%2A> to process the results of routing before the endpoint is executed.
  * Middleware that runs between `UseRouting` and `UseEndpoints`:
    * Usually inspects metadata to understand the endpoints.
    * Often makes security decisions, as done by `UseAuthorization` and `UseCors`.
  * The combination of middleware and metadata allows configuring policies per-endpoint.

The preceding code shows an example of a custom middleware that supports per-endpoint policies. The middleware writes an *audit log* of access to sensitive data to the console. The middleware can be configured to *audit* an endpoint with the `RequiresAuditAttribute` metadata. This sample demonstrates an *opt-in* pattern where only endpoints that are marked as sensitive are audited. It's possible to define this logic in reverse, auditing everything that isn't marked as safe, for example. The endpoint metadata system is flexible. This logic could be designed in whatever way suits the use case.

The preceding sample code is intended to demonstrate the basic concepts of endpoints. **The sample is not intended for production use**. A more complete version of an *audit log* middleware would:

* Log to a file or database.
* Include details such as the user, IP address, name of the sensitive endpoint, and more.

The audit policy metadata `RequiresAuditAttribute` is defined as an `Attribute` for easier use with class-based frameworks such as controllers and SignalR. When using *route to code*:

* Metadata is attached with a builder API.
* Class-based frameworks include all attributes on the corresponding method and class when creating endpoints.

The best practices for metadata types are to define them either as interfaces or attributes. Interfaces and attributes allow code reuse. The metadata system is flexible and doesn't impose any limitations.

<a name="tm"></a>


## Service registration methods

For general guidance on service registrations, see [Service registration](/dotnet/core/extensions/dependency-injection/service-registration).

It's common to use multiple implementations when mocking types for testing. For more information, see <xref:test/integration-tests#inject-mock-services>.

Registering a service with only an implementation type is equivalent to registering the service with the same implementation and service type:

:::moniker range=">= aspnetcore-6.0"

```csharp
builder.Services.AddSingleton<MyDependency>();
```

:::moniker-end

:::moniker range="< aspnetcore-6.0"

```csharp
services.AddSingleton<MyDependency>();
```

:::moniker-end

Service registration methods can be used to register multiple service instances of the same service type. In the following example, <xref:Microsoft.Extensions.DependencyInjection.ServiceCollectionServiceExtensions.AddSingleton%2A> is called twice with `IMyDependency` as the service type. The second call to `AddSingleton` overrides the previous one when resolved as `IMyDependency` and adds to the previous one when multiple services are resolved via `IEnumerable<IMyDependency>`.

:::moniker range=">= aspnetcore-6.0"

```csharp
builder.Services.AddSingleton<IMyDependency, MyDependency>();
builder.Services.AddSingleton<IMyDependency, DifferentDependency>();

public class MyService
{
    public MyService(IMyDependency myDependency, 
       IEnumerable<IMyDependency> myDependencies)
    {
        Trace.Assert(myDependency is DifferentDependency);

        var dependencyArray = myDependencies.ToArray();
        Trace.Assert(dependencyArray[0] is MyDependency);
        Trace.Assert(dependencyArray[1] is DifferentDependency);
    }
}
```

:::moniker-end

:::moniker range="< aspnetcore-6.0"

```csharp
services.AddSingleton<IMyDependency, MyDependency>();
services.AddSingleton<IMyDependency, DifferentDependency>();

public class MyService
{
    public MyService(IMyDependency myDependency, 
       IEnumerable<IMyDependency> myDependencies)
    {
        Trace.Assert(myDependency is DifferentDependency);

        var dependencyArray = myDependencies.ToArray();
        Trace.Assert(dependencyArray[0] is MyDependency);
        Trace.Assert(dependencyArray[1] is DifferentDependency);
    }
}
```

:::moniker-end


## Register groups of services with extension methods

The ASP.NET Core framework convention for registering a group of related services is to use a single `Add{GROUP NAME}` extension method to register all of the services required by a framework feature, where the `{GROUP NAME}` placeholder is a descriptive group name. For example, the <xref:Microsoft.Extensions.DependencyInjection.RazorComponentsServiceCollectionExtensions.AddRazorComponents%2A> extension method registers services required for server-side rendering of Razor components.

Consider the following example that configures options and registers services:

:::moniker range=">= aspnetcore-6.0"

```csharp
builder.Services.Configure<PositionOptions>(
    builder.Configuration.GetSection(PositionOptions.Position));
builder.Services.Configure<ColorOptions>(
    builder.Configuration.GetSection(ColorOptions.Color));

builder.Services.AddScoped<IMyDependency, MyDependency>();
builder.Services.AddScoped<IMyDependency2, MyDependency2>();
```

:::moniker-end

:::moniker range="< aspnetcore-6.0"

```csharp
services.Configure<PositionOptions>(
    builder.Configuration.GetSection(PositionOptions.Position));
services.Configure<ColorOptions>(
    builder.Configuration.GetSection(ColorOptions.Color));

services.AddScoped<IMyDependency, MyDependency>();
services.AddScoped<IMyDependency2, MyDependency2>();
```

:::moniker-end

Related groups of registrations can be moved to an extension method to register services. In the following example:

* The `AddConfig` extension method binds configuration data to strongly-typed C# classes and registers the classes in the service container.
* The `AddDependencyGroup` extension method adds additional class (service) dependencies.

```csharp
namespace Microsoft.Extensions.DependencyInjection;

public static class ConfigServiceCollectionExtensions
{
    public static IServiceCollection AddConfig(
        this IServiceCollection services, IConfiguration config)
    {
        services.Configure<PositionOptions>(
            config.GetSection(PositionOptions.Position));
        services.Configure<ColorOptions>(
            config.GetSection(ColorOptions.Color));

        return services;
    }

    public static IServiceCollection AddDependencyGroup(
        this IServiceCollection services)
    {
        services.AddScoped<IMyDependency, MyDependency>();
        services.AddScoped<IMyDependency2, MyDependency2>();

        return services;
    }
}
```

The following code calls the preceding `AddConfig` and `AddDependencyGroup` extension methods to register the services:

:::moniker range=">= aspnetcore-6.0"

```csharp
builder.Services
    .AddConfig(builder.Configuration)
    .AddDependencyGroup();
```

:::moniker-end

:::moniker range="< aspnetcore-6.0"

```csharp
services
    .AddConfig(builder.Configuration)
    .AddDependencyGroup();
```

:::moniker-end

We recommend that apps follow the naming convention of creating extension methods in the <xref:Microsoft.Extensions.DependencyInjection?displayProperty=fullName> namespace, which:

* Encapsulates groups of service registrations.
* Provides convenient [IntelliSense](/visualstudio/ide/using-intellisense) access to the service.


## Working with a synchronous data processing API

When using a serializer/de-serializer that only supports synchronous reads and writes (for example, [Json.NET](https://www.newtonsoft.com/json/help/html/Introduction.htm)):

* Buffer the data into memory asynchronously before passing it into the serializer/de-serializer.

> [!WARNING]
> If the request is large, it could lead to an out of memory (OOM) condition. OOM can result in a Denial Of Service. For more information, see [Avoid reading large request bodies or response bodies into memory](#arlb) in this article.

ASP.NET Core 3.0 uses <xref:System.Text.Json> by default for JSON serialization. <xref:System.Text.Json>:

* Reads and writes JSON asynchronously.
* Is optimized for UTF-8 text.
* Typically is higher performance than `Newtonsoft.Json`.


## Environment-specific `Startup` class methods

The `Configure` and `ConfigureServices` methods support environment-specific versions of the form `Configure{ENVIRONMENT NAME}` and `Configure{ENVIRONMENT NAME}Services`, where the `{ENVIRONMENT NAME}` placeholder is the environment name. If a matching environment name isn't found for the named methods, the `ConfigureServices` or `Configure` method is used, respectively.

```csharp
public void ConfigureDevelopmentServices(IServiceCollection services)
{
    ...
}

public void ConfigureStagingServices(IServiceCollection services)
{
    ...
}

public void ConfigureProductionServices(IServiceCollection services)
{
    ...
}

public void ConfigureServices(IServiceCollection services)
{
    ...
}
```


## The Web API (Native AOT) template

The **ASP.NET Core Web API (Native AOT)** template (short name `webapiaot`) creates a project with AOT enabled. The template differs from the **Web API** project template in the following ways:

* Uses Minimal APIs only, as MVC isn't yet compatible with Native AOT.
* Uses the <xref:Microsoft.AspNetCore.Builder.WebApplication.CreateSlimBuilder> API to ensure only the essential features are enabled by default, minimizing the app's deployed size.
* Is configured to listen on HTTP only, as HTTPS traffic is commonly handled by an ingress service in cloud-native deployments.
* Doesn't include a launch profile for running under IIS or IIS Express.
* Creates an [`.http` file](xref:test/http-files) configured with sample HTTP requests that can be sent to the app's endpoints.
* Includes a sample `Todo` API instead of the weather forecast sample.
* Adds `PublishAot` to the project file, as shown [earlier in this article](#native-aot-publishing).
* Enables the [JSON serializer source generators](/dotnet/standard/serialization/system-text-json/source-generation). The source generator is used to generate serialization code at build time, which is required for Native AOT compilation.


## Minimal APIs and JSON payloads

The Minimal API framework is optimized for receiving and returning JSON payloads using <xref:System.Text.Json?displayProperty=fullName>. `System.Text.Json`:

* Imposes compatibility requirements for JSON and Native AOT.
* Requires the use of the [`System.Text.Json` source generator](/dotnet/standard/serialization/system-text-json/source-generation).

All types that are transmitted as part of the HTTP body or returned from request delegates in Minimal APIs apps must be configured on a <xref:System.Text.Json.Serialization.JsonSerializerContext> that is registered via ASP.NET Core’s dependency injection:

:::code language="csharp" source="~/fundamentals/aot/samples/Program.cs" highlight="7-10,25-99":::

In the preceding highlighted code:

* The JSON serializer context is registered with the [DI container](xref:fundamentals/dependency-injection). For more information, see:
  * [Combine source generators](/dotnet/standard/serialization/system-text-json/source-generation?pivots=dotnet-8-0#combine-source-generators)
  * <xref:System.Text.Json.JsonSerializerOptions.TypeInfoResolverChain>
* The custom `JsonSerializerContext` is annotated with the [`[JsonSerializable]`](/dotnet/api/system.text.json.serialization.jsonserializableattribute) attribute to enable source generated JSON serializer code for the `ToDo` type.

A parameter on the delegate that isn't bound to the body and does ***not*** need to be serializable. For example, a query string parameter that is a rich object type and implements `IParsable<T>`.

:::code language="csharp" source="~/fundamentals/aot/samples/Todo.cs" id="snippet_1":::


## minimal apis

---
title: Minimal APIs quick reference
author: wadepickett
description: Provides an overview of Minimal APIs in ASP.NET Core
ms.author: wpickett
content_well_notification: AI-contribution
monikerRange: '>= aspnetcore-6.0'
ms.date: 03/17/2026
uid: fundamentals/minimal-apis
ai-usage: ai-assisted
---

<!--
Editorial note: This file is a quick reference summary:
- When working on this file, open all the LATEST VERSION MD files in ~/fundamentals/minimal-apis/includes/ and search for the target text.
- Only include brief overviews, essential lists, and basic examples in this file.
- Do NOT add detailed explanations, advanced scenarios, or troubleshooting—move those to dedicated include files (for example: parameter-binding8-10.md) and link to them from here if needed.
- All in-depth content should be placed in the appropriate in-depth include file for maintainability and clarity.
- Use H3 (###) for section headings within this include.
-->


# Minimal APIs quick reference

[!INCLUDE[](~/includes/not-latest-version.md)]

:::moniker range=">= aspnetcore-10.0"

This document provides a quick reference for Minimal APIs. For a guided introduction, see <xref:tutorials/min-web-api>.

The Minimal APIs consist of:

* [`WebApplication` and `WebApplicationBuilder`](xref:fundamentals/minimal-apis/webapplication)
* [Route Handlers](xref:fundamentals/minimal-apis/route-handlers)

[!INCLUDE[](~/fundamentals/minimal-apis/includes/webapplication10.md)]


## Json+PipeReader deserialization in Minimal APIs

[!INCLUDE [](~/includes/net10pipereader.md)]


## Validation support in Minimal APIs

Enabling validation allows the ASP.NET Core runtime to perform validations defined on the:

* Query
* Header
* Request body

Validations are defined using attributes in the [`DataAnnotations`](xref:System.ComponentModel.DataAnnotations) namespace. 

When a parameter to a Minimal API endpoint is a class or record type, validation attributes are automatically applied. For example:

```csharp
public record Product(
    [Required] string Name,
    [Range(1, 1000)] int Quantity);
```
Developers customize the behavior of the validation system by:

* Creating custom [`[Validation]` attribute](xref:System.ComponentModel.DataAnnotations.ValidationAttribute) implementations.
* Implementing the [`IValidatableObject`](xref:System.ComponentModel.DataAnnotations.IValidatableObject) interface for complex validation logic.

If validation fails, the runtime returns a *400 - Bad Request* response with details of the validation errors.


### Enable built-in validation support for Minimal APIs

Enable the built-in validation support for Minimal APIs by calling the `AddValidation` extension method to register the required services in the service container for your application:

```csharp
builder.Services.AddValidation();
```

The implementation automatically discovers types that are defined in Minimal API handlers or as base types of types defined in Minimal API handlers. An endpoint filter performs validation on these types and is added for each endpoint.

Validation can be disabled for specific endpoints by using the `DisableValidation` extension method, as in the following example:

```csharp
app.MapPost("/products",
    ([EvenNumber(ErrorMessage = "Product ID must be even")] int productId, [Required] string name)
        => TypedResults.Ok(productId))
    .DisableValidation();
```

# Use ASP.NET Core APIs in a class library

By [Scott Addie](https://github.com/scottaddie)

This document provides guidance for using ASP.NET Core APIs in a class library. For all other library guidance, see [Open-source library guidance](/dotnet/standard/library-guidance/).


## Use an API that hasn't changed

Imagine a scenario in which you're upgrading a middleware library from .NET Core 2.2 to 3.1. The ASP.NET Core middleware APIs being used in the library haven't changed between ASP.NET Core 2.2 and 3.1. To continue supporting the middleware library in .NET Core 3.1, take the following steps:

* Follow the [standard library guidance](/dotnet/standard/library-guidance/).
* Add a package reference for each API's NuGet package if the corresponding assembly doesn't exist in the shared framework.


## Use an API that changed

Imagine a scenario in which you're upgrading a library from .NET Core 2.2 to .NET Core 3.1. An ASP.NET Core API being used in the library has a [breaking change](/dotnet/core/compatibility/breaking-changes) in ASP.NET Core 3.1. Consider whether the library can be rewritten to not use the broken API in all versions.

If you can rewrite the library, do so and continue to target an earlier target framework (for example, .NET Standard 2.0 or .NET Framework 4.6.1) with package references.

If you can't rewrite the library, take the following steps:

* Add a target for .NET Core 3.1.
* Add a `<FrameworkReference>` element for the shared framework.
* Use the [#if preprocessor directive](/dotnet/csharp/language-reference/preprocessor-directives/preprocessor-if) with the appropriate target framework symbol to conditionally compile code.

For example, synchronous reads and writes on HTTP request and response streams are disabled by default as of ASP.NET Core 3.1. ASP.NET Core 2.2 supports the synchronous behavior by default. Consider a middleware library in which synchronous reads and writes should be enabled where I/O is occurring. The library should enclose the code to enable synchronous features in the appropriate preprocessor directive. For example:

[!code-csharp[](target-aspnetcore/samples/middleware.cs?highlight=9-24)]


## Use an API removed from the shared framework

To use an ASP.NET Core assembly that was removed from the shared framework, add the appropriate package reference. For a list of packages removed from the shared framework in ASP.NET Core 3.1, see [Remove obsolete package references](xref:migration/22-to-30#remove-obsolete-package-references).

For example, to add the web API client:

```xml
<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <TargetFramework>net6.0</TargetFramework>
  </PropertyGroup>

  <ItemGroup>
    <FrameworkReference Include="Microsoft.AspNetCore.App" />
  </ItemGroup>

  <ItemGroup>
    <PackageReference Include="Microsoft.AspNet.WebApi.Client" Version="5.2.7" />
  </ItemGroup>

</Project>
```


## error handling api

---
title: Handle errors in ASP.NET Core APIs
author: brunolins16
description: Learn about error handling in ASP.NET Core APIs with Minimal APIs and controller-based approaches.
ai-usage: ai-assisted
ms.author: wpickett
monikerRange: '>= aspnetcore-7.0'
ms.date: 03/04/2026
uid: fundamentals/error-handling-api
---


# Handle errors in ASP.NET Core APIs

[!INCLUDE[](~/includes/not-latest-version.md)]


#### [Minimal APIs](#tab/minimal-apis)


## Prerequisites

* Any OS that supports ASP.NET Core:  
  * Windows 7 / Windows Server 2008 or later
  * Linux
  * macOS  
* If the app runs on Windows with IIS:
  * Windows 8 / Windows Server 2012 or later
  * IIS 8 / IIS 8 Express
  * WebSockets must be enabled. See the [IIS/IIS Express support](#iisiis-express-support) section.  
* If the app runs on [HTTP.sys](xref:fundamentals/servers/httpsys):
  * Windows 8 / Windows Server 2012 or later
* For supported browsers, see [Can I use](https://caniuse.com/?search=websockets).
