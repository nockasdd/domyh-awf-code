---
library: mcp
version: latest
latest: true
category: ai-sdk
official_docs: https://modelcontextprotocol.io
last_updated: 2026-03-21
source: auto-fetched from llms-full
source_url: https://modelcontextprotocol.io/llms-full.txt
---

# Example Clients
Source: https://modelcontextprotocol.io/clients

A list of applications that support MCP integrations

This page showcases applications that support the Model Context Protocol (MCP). Each client may support different MCP features:

| Feature          | Description                                                                                                  |
| ---------------- | ------------------------------------------------------------------------------------------------------------ |
| <FeatureBadge /> | Server-exposed data and content                                                                              |
| <FeatureBadge /> | Pre-defined templates for LLM interactions                                                                   |
| <FeatureBadge /> | Executable functions that LLMs can invoke                                                                    |
| <FeatureBadge /> | Support for tools/prompts/resources changed notifications                                                    |
| <FeatureBadge /> | Server-provided guidance for LLMs                                                                            |
| <FeatureBadge /> | Server-initiated LLM completions                                                                             |
| <FeatureBadge /> | Filesystem boundary definitions                                                                              |
| <FeatureBadge /> | User information requests                                                                                    |
| <FeatureBadge /> | [Client ID Metadata Document](specification/latest/basic/authorization#client-id-metadata-documents) support |
| <FeatureBadge /> | [Dynamic Client Registration](specification/latest/basic/authorization#dynamic-client-registration) support  |
| <FeatureBadge /> | Long-running operation tracking                                                                              |
| <FeatureBadge /> | Interactive HTML interfaces                                                                                  |

<Note>
  This list is maintained by the community. If you notice any inaccuracies or would like to add or update information about MCP support in your application, please [submit a pull request](https://github.com/modelcontextprotocol/modelcontextprotocol/pulls).
</Note>


## Prerequisites

Before starting this tutorial, ensure you have the following installed on your system:


## Installing the Filesystem Server

The process involves configuring Claude Desktop to automatically start the Filesystem Server whenever you launch the application. This configuration is done through a JSON file that tells Claude Desktop which servers to run and how to connect to them.

<Steps>
  <Step title="Open Claude Desktop Settings">
    Start by accessing the Claude Desktop settings. Click on the Claude menu in your system's menu bar (not the settings within the Claude window itself) and select "Settings..."

    On macOS, this appears in the top menu bar:

    <Frame>
      <img alt="Claude Desktop menu showing Settings option" />
    </Frame>

    This opens the Claude Desktop configuration window, which is separate from your Claude account settings.
  </Step>

  <Step title="Access Developer Settings">
    In the Settings window, navigate to the "Developer" tab in the left sidebar. This section contains options for configuring MCP servers and other developer features.

    Click the "Edit Config" button to open the configuration file:

    <Frame>
      <img alt="Developer settings showing Edit Config button" />
    </Frame>

    This action creates a new configuration file if one doesn't exist, or opens your existing configuration. The file is located at:

    * **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
    * **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
  </Step>

  <Step title="Configure the Filesystem Server">
    Replace the contents of the configuration file with the following JSON structure. This configuration tells Claude Desktop to start the Filesystem Server with access to specific directories:

    <CodeGroup>
      ```json macOS theme={null}
      {
        "mcpServers": {
          "filesystem": {
            "command": "npx",
            "args": [
              "-y",
              "@modelcontextprotocol/server-filesystem",
              "/Users/username/Desktop",
              "/Users/username/Downloads"
            ]
          }
        }
      }
      ```

      ```json Windows theme={null}
      {
        "mcpServers": {
          "filesystem": {
            "command": "npx",
            "args": [
              "-y",
              "@modelcontextprotocol/server-filesystem",
              "C:\\Users\\username\\Desktop",
              "C:\\Users\\username\\Downloads"
            ]
          }
        }
      }
      ```
    </CodeGroup>

    Replace `username` with your actual computer username. The paths listed in the `args` array specify which directories the Filesystem Server can access. You can modify these paths or add additional directories as needed.

    <Tip>
      **Understanding the Configuration**

      * `"filesystem"`: A friendly name for the server that appears in Claude Desktop
      * `"command": "npx"`: Uses Node.js's npx tool to run the server
      * `"-y"`: Automatically confirms the installation of the server package
      * `"@modelcontextprotocol/server-filesystem"`: The package name of the Filesystem Server
      * The remaining arguments: Directories the server is allowed to access
    </Tip>

    <Warning>
      **Security Consideration**

      Only grant access to directories you're comfortable with Claude reading and modifying. The server runs with your user account permissions, so it can perform any file operations you can perform manually.
    </Warning>
  </Step>

  <Step title="Restart Claude Desktop">
    After saving the configuration file, completely quit Claude Desktop and restart it. The application needs to restart to load the new configuration and start the MCP server.

    Upon successful restart, you'll see an MCP server indicator <img /> in the bottom-right corner of the conversation input box:

    <Frame>
      <img alt="Claude Desktop interface showing MCP server indicator" />
    </Frame>

    Click on this indicator to view the available tools provided by the Filesystem Server:

    <Frame>
      <img alt="Available filesystem tools in Claude Desktop" />
    </Frame>

    If the server indicator doesn't appear, refer to the [Troubleshooting](#troubleshooting) section for debugging steps.
  </Step>
</Steps>


## Getting Started

Each SDK provides the same functionality but follows the idioms and best practices of its language. All SDKs support:

* Creating MCP servers that expose tools, resources, and prompts
* Building MCP clients that can connect to any MCP server
* Local and remote transport protocols
* Protocol compliance with type safety

Visit the SDK page for your chosen language to find installation instructions, documentation, and examples.


## Getting started


### Installation and basic usage

The Inspector runs directly through `npx` without requiring installation:

```bash theme={null}
npx @modelcontextprotocol/inspector <command>
```

```bash theme={null}
npx @modelcontextprotocol/inspector <command> <arg1> <arg2>
```


### Keycloak Setup

From your terminal application, run the following command to start the Keycloak container:

```bash theme={null}
docker run -p 127.0.0.1:8080:8080 -e KC_BOOTSTRAP_ADMIN_USERNAME=admin -e KC_BOOTSTRAP_ADMIN_PASSWORD=admin quay.io/keycloak/keycloak start-dev
```

This command will pull the Keycloak container image locally and bootstrap the basic configuration. It will run on port `8080` and have an `admin` user with `admin` password.

<Warning>
  **Not for Production**

  The configuration above may be suitable for testing and experimentation; however, you should never use it in production. Refer to the [Configuring Keycloak for production](https://www.keycloak.org/server/configuration-production) guide for additional details on how to deploy the authorization server for scenarios that require reliability, security, and high availability.
</Warning>

You will be able to access the Keycloak authorization server from your browser at `http://localhost:8080`.

<Frame>
  <img alt="Keycloak admin dashboard authentication dialog." />
</Frame>

When running with the default configuration, Keycloak will already support many of the capabilities that we need for MCP servers, including Dynamic Client Registration. You can check this by looking at the OIDC configuration, available at:

```http theme={null}
http://localhost:8080/realms/master/.well-known/openid-configuration
```

We will also need to set up Keycloak to support our scopes and allow our host (local machine) to dynamically register clients, as the default policies restrict anonymous dynamic client registration.

Go to **Client scopes** in the Keycloak dashboard and create a new `mcp:tools` scope. We will use this to access all of the tools on our MCP server.

<Frame>
  <img alt="Configuring Keycloak scopes." />
</Frame>

After creating the scope, make sure that you assign its type to **Default** and have flipped the **Include in token scope** switch, as this will be needed for token validation.

Let's now also set up an **audience** for our Keycloak-issued tokens. An audience is important to configure because it embeds the intended destination directly into the issued access token. This helps your MCP server to verify that the token it got was actually meant for it rather than some other API. This is key to help avoid token passthrough scenarios.

To do this, open your `mcp:tools` client scope and click on **Mappers**, followed by **Configure a new mapper**. Select **Audience**.

<Frame>
  <img alt="Configuring an audience for a token in Keycloak." />
</Frame>

For **Name**, use `audience-config`. Add a value for **Included Custom Audience**, set to `http://localhost:3000`. This will be the URI of our test server.

<Warning>
  **Not for Production**

  The audience configuration above is meant for testing. For production scenarios, additional set-up and configuration will be required to ensure that audiences are properly constrained for issued tokens. Specifically, the audience needs to be based on the resource parameter passed from the client, not a fixed value.
</Warning>

Now, navigate to **Clients**, then **Client registration**, and then **Trusted Hosts**. Disable the **Client URIs Must Match** setting and add the hosts from which you're testing. You can get your current host IP by running the `ifconfig` command on Linux or macOS, or `ipconfig` on Windows. You can see the IP address you need to add by looking at the keycloak logs for a line that looks like `Failed to verify remote host : 192.168.215.1`. Check that the IP address is associated with your host. This may be for a bridge network depending on your docker setup.

<Frame>
  <img alt="Setting up client registration details in Keycloak." />
</Frame>

<Warning>
  **Getting the Host**

  If you are running Keycloak from a container, you will also be able to see the host IP from the Terminal in the container logs.
</Warning>

Lastly, we need to register a new client that we can use with the **MCP server itself** to talk to Keycloak for things like [token introspection](https://oauth.net/2/token-introspection/). To do that:

1. Go to **Clients**.
2. Click **Create client**.
3. Give your client a unique **Client ID** and click **Next**.
4. Enable **Client authentication** and click **Next**.
5. Click **Save**.

Worth noting that token introspection is just *one of* the available approaches to validate tokens. This can also be done with the help of standalone libraries, specific to each language and platform.

When you open the client details, go to **Credentials** and take note of the **Client Secret**.

<Frame>
  <img alt="Creating a new client in Keycloak." />
</Frame>

<Warning>
  **Handling Secrets**

  Never embed client credentials directly in your code. We recommend using environment variables or specialized solutions for secret storage.
</Warning>

With Keycloak configured, every time the authorization flow is triggered, your MCP server will receive a token like this:

```text theme={null}
eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI1TjcxMGw1WW5MWk13WGZ1VlJKWGtCS3ZZMzZzb3JnRG5scmlyZ2tlTHlzIn0.eyJleHAiOjE3NTU1NDA4MTcsImlhdCI6MTc1NTU0MDc1NywiYXV0aF90aW1lIjoxNzU1NTM4ODg4LCJqdGkiOiJvbnJ0YWM6YjM0MDgwZmYtODQwNC02ODY3LTgxYmUtMTIzMWI1MDU5M2E4IiwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdDo4MDgwL3JlYWxtcy9tYXN0ZXIiLCJhdWQiOiJodHRwOi8vbG9jYWxob3N0OjMwMDAiLCJzdWIiOiIzM2VkNmM2Yi1jNmUwLTQ5MjgtYTE2MS1mMmY2OWM3YTAzYjkiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiI3OTc1YTViNi04YjU5LTRhODUtOWNiYS04ZmFlYmRhYjg5NzQiLCJzaWQiOiI4ZjdlYzI3Ni0zNThmLTRjY2MtYjMxMy1kYjA4MjkwZjM3NmYiLCJzY29wZSI6Im1jcDp0b29scyJ9.P5xCRtXORly0R0EXjyqRCUx-z3J4uAOWNAvYtLPXroykZuVCCJ-K1haiQSwbURqfsVOMbL7jiV-sD6miuPzI1tmKOkN_Yct0Vp-azvj7U5rEj7U6tvPfMkg2Uj_jrIX0KOskyU2pVvGZ-5BgqaSvwTEdsGu_V3_E0xDuSBq2uj_wmhqiyTFm5lJ1WkM3Hnxxx1_AAnTj7iOKMFZ4VCwMmk8hhSC7clnDauORc0sutxiJuYUZzxNiNPkmNeQtMCGqWdP1igcbWbrfnNXhJ6NswBOuRbh97_QraET3hl-CNmyS6C72Xc0aOwR_uJ7xVSBTD02OaQ1JA6kjCATz30kGYg
```

Decoded, it will look like this:

```json theme={null}
{
  "alg": "RS256",
  "typ": "JWT",
  "kid": "5N710l5YnLZMwXfuVRJXkBKvY36sorgDnlrirgkeLys"
}.{
  "exp": 1755540817,
  "iat": 1755540757,
  "auth_time": 1755538888,
  "jti": "onrtac:b34080ff-8404-6867-81be-1231b50593a8",
  "iss": "http://localhost:8080/realms/master",
  "aud": "http://localhost:3000",
  "sub": "33ed6c6b-c6e0-4928-a161-f2f69c7a03b9",
  "typ": "Bearer",
  "azp": "7975a5b6-8b59-4a85-9cba-8faebdab8974",
  "sid": "8f7ec276-358f-4ccc-b313-db08290f376f",
  "scope": "mcp:tools"
}.[Signature]
```

<Warning>
  **Embedded Audience**

  Notice the `aud` claim embedded in the token - it's currently set to be the URI of the test MCP server and it's inferred from the scope that we've previously configured. This will be important in our implementation to validate.
</Warning>


## Getting started


## Prerequisites

You'll need [Node.js](https://nodejs.org/en/download) 18 or higher. Familiarity
with [MCP tools](/specification/latest/server/tools) and
[resources](/specification/latest/server/resources) is recommended since MCP
Apps combine both primitives. Experience with the
[MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
will help you better understand the server-side patterns.


## Getting started

The fastest way to create an MCP App is using an AI coding agent with the MCP
Apps skill. If you prefer to set up a project manually, skip to
[Manual setup](#manual-setup).


### Manual setup

If you're not using an AI coding agent, or prefer to understand the setup
process, follow these steps.

<Steps>
  <Step title="Create the project structure">
    A typical MCP App project separates the server code from the UI code:

    <Tree>
      <Tree.Folder name="my-mcp-app">
        <Tree.File name="package.json" />

        <Tree.File name="tsconfig.json" />

        <Tree.File name="vite.config.ts" />

        <Tree.File name="server.ts" />

        <Tree.File name="mcp-app.html" />

        <Tree.Folder name="src">
          <Tree.File name="mcp-app.ts" />
        </Tree.Folder>
      </Tree.Folder>
    </Tree>

    The server registers the tool and serves the UI resource. The UI resource will eventually be rendered in a secure iframe with deny-by-default CSP configuration. If your app has CSS and JS assets, you will need to [configure CSP](https://apps.extensions.modelcontextprotocol.io/api/documents/Patterns.html#configuring-csp-and-cors), or you can bundle your assets into the HTML with a tool like `vite-plugin-singlefile`, which is what we will do in this tutorial.
  </Step>

  <Step title="Install dependencies">
    ```bash theme={null}
    npm install @modelcontextprotocol/ext-apps @modelcontextprotocol/sdk
    npm install -D typescript vite vite-plugin-singlefile express cors @types/express @types/cors tsx
    ```

    The `ext-apps` package provides helpers for both the server side (registering tools and resources) and the client side (the `App` class for UI-to-host communication). Vite with the `vite-plugin-singlefile` plugin is used here to bundle your UI and assets into a single HTML file for convenience, but this is optional — you can use any bundler or serve unbundled files if you [configure CSP](https://apps.extensions.modelcontextprotocol.io/api/documents/Patterns.html#configuring-csp-and-cors).
  </Step>

  <Step title="Configure the project">
    <Tabs>
      <Tab title="package.json">
        The `"type": "module"` setting enables ES module syntax. The `build` script uses the `INPUT` environment variable to tell Vite which HTML file to bundle. The `serve` script runs your server using `tsx` for TypeScript execution.

        ```json theme={null}
        {
          "type": "module",
          "scripts": {
            "build": "INPUT=mcp-app.html vite build",
            "serve": "npx tsx server.ts"
          }
        }
        ```
      </Tab>

      <Tab title="tsconfig.json">
        The TypeScript configuration targets modern JavaScript (`ES2022`) and uses ESNext modules with bundler resolution, which works well with Vite. The `include` array covers both the server code in the root and UI code in `src/`.

        ```json theme={null}
        {
          "compilerOptions": {
            "target": "ES2022",
            "module": "ESNext",
            "moduleResolution": "bundler",
            "strict": true,
            "esModuleInterop": true,
            "skipLibCheck": true,
            "outDir": "dist"
          },
          "include": ["*.ts", "src/**/*.ts"]
        }
        ```
      </Tab>

      <Tab title="vite.config.ts">
        ```typescript theme={null}
        import { defineConfig } from "vite";
        import { viteSingleFile } from "vite-plugin-singlefile";

        export default defineConfig({
          plugins: [viteSingleFile()],
          build: {
            outDir: "dist",
            rollupOptions: {
              input: process.env.INPUT,
            },
          },
        });
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step title="Build the project">
    With the project structure and configuration in place, continue to [Building an MCP App](#building-an-mcp-app) below to implement the server and UI.
  </Step>
</Steps>


## Implementation guide


## Implementation guide


## Definitions

Tasks represent parties as either "requestors" or "receivers," defined as follows:

* **Requestor:** The sender of a task-augmented request. This can be the client or the server — either can create tasks.
* **Receiver:** The receiver of a task-augmented request, and the entity executing the task. This can be the client or the server — either can receive and execute tasks.


## Cross-API Compatibility

The sampling specification is designed to work across multiple LLM provider APIs (Claude, OpenAI, Gemini, etc.). Key design decisions for compatibility:


### Prerequisites

Before contributing, ensure you have the following installed and ready:

* **[Git](https://git-scm.com/downloads)** - For cloning repositories and submitting changes
* **[Node.js 24+](https://nodejs.org/)** - Required for building and testing our projects
* **npm** - Comes with Node.js, used for dependency management
* **[GitHub account](https://github.com/signup)** - For submitting pull requests and issues
* **Language-specific tooling** - If contributing to an SDK, you'll need the appropriate
  development environment for that language (e.g., Python, Rust, Go)

Verify your setup:

```bash theme={null}
node --version  # Should be 24.x or higher
npm --version   # Should be 11.x or higher
git --version   # Any recent version
```

<Note>
  These commands work the same on macOS, Linux, and Windows, so you're good to
  go on any platform.
</Note>


# Install dependencies
npm install


### Current Approach (Inline Definition):

The RPC method definition contains the full structure of its parameters and results.

```ts theme={null}
export interface CallToolRequest extends Request {
  method: "tools/call";
  params: {
    name: string;
    arguments?: { [key: string]: unknown };
  };
}
```


### Tier Definitions
