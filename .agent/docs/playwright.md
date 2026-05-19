---
library: playwright
version: latest
latest: true
category: testing
official_docs: https://playwright.dev
last_updated: 2026-03-21
source: auto-fetched from github-dir
source_url: https://api.github.com/repos/microsoft/playwright/contents/docs/src
---

### New APIs

- New property [`property: TestConfig.tag`] adds a tag to all tests in this run. This is useful when using [merge-reports](./test-sharding.md#merging-reports-from-multiple-shards).
- [`event: Worker.console`] event is emitted when JavaScript within the worker calls one of console API methods, e.g. console.log or console.dir. [`method: Worker.waitForEvent`] can be used to wait for it.
- [`method: Locator.description`] returns locator description previously set with [`method: Locator.describe`], and [`method: Locator.toString`] now uses the description when available.
- New option [`option: Locator.click.steps`] in [`method: Locator.click`] and [`method: Locator.dragTo`] that configures the number of `mousemove` events emitted while moving the mouse pointer to the target element.
- Network requests issued by [Service Workers](./service-workers.md#network-events-and-routing) are now reported and can be routed through the [BrowserContext](./api/class-browsercontext.md), only in Chromium. You can opt out using the `PLAYWRIGHT_DISABLE_SERVICE_WORKER_NETWORK` environment variable.
- Console messages from Service Workers are dispatched through [`event: Worker.console`]. You can opt out of this using the `PLAYWRIGHT_DISABLE_SERVICE_WORKER_CONSOLE` environment variable.


# Generate agent files for each agentic loop

### New APIs

- New methods [`method: Page.consoleMessages`] and [`method: Page.pageErrors`] for retrieving the most recent console messages from the page
- New method [`method: Page.requests`] for retrieving the most recent network requests from the page
- Added [`--test-list` and `--test-list-invert`](./test-cli.md#test-list) to allow manual specification of specific tests from a file


### New APIs

- New Property [`property: TestStepInfo.titlePath`] Returns the full title path starting from the test file, including test and step titles.


### New APIs

- [`method: LocatorAssertions.toHaveAttribute#2`]


### Potentially breaking change in Playwright Test Global Setup

It is unlikely that this change will affect you, no action is required if your tests keep running as they did.

We've noticed that in rare cases, the set of tests to be executed was configured in the global setup by means of the environment variables. We also noticed some applications that were post processing the reporters' output in the global teardown. If you are doing one of the two, [learn more](https://github.com/microsoft/playwright/issues/12018)


#### New APIs

- [`method: BrowserType.launch`] now accepts the new `'channel'` option. Read more in [our documentation](./browsers).



# Initialize clock with some time before the test time and let the page load

# Setup the handler.
page.add_locator_handler(
    page.get_by_role("heading", name="Hej! You are in control of your cookies."),
    lambda: page.get_by_role("button", name="Accept all").click(),
)

## Install browsers

Playwright can install supported browsers. Running the command without arguments will install the default browsers.

```bash js
npx playwright install
```

```bash java
mvn exec:java -e -D exec.mainClass=com.microsoft.playwright.CLI -D exec.args="install"
```

```bash python
playwright install
```

```bash csharp
pwsh bin/Debug/netX/playwright.ps1 install
```

You can also install specific browsers by providing an argument:

```bash js
npx playwright install webkit
```

```bash java
mvn exec:java -e -D exec.mainClass=com.microsoft.playwright.CLI -D exec.args="install webkit"
```

```bash python
playwright install webkit
```

```bash csharp
pwsh bin/Debug/netX/playwright.ps1 install webkit
```

See all supported browsers:

```bash js
npx playwright install --help
```

```bash java
mvn exec:java -e -D exec.mainClass=com.microsoft.playwright.CLI -D exec.args="install --help"
```

```bash python
playwright install --help
```

```bash csharp
pwsh bin/Debug/netX/playwright.ps1 install --help
```


### Install browsers via API
* langs: csharp

It's possible to run Command line tools commands via the .NET API:

```csharp
var exitCode = Microsoft.Playwright.Program.Main(new[] {"install"});
if (exitCode != 0)
{
    throw new Exception($"Playwright exited with code {exitCode}");
}
```


## Install system dependencies

System dependencies can get installed automatically. This is useful for CI environments.

```bash js
npx playwright install-deps
```

```bash java
mvn exec:java -e -D exec.mainClass=com.microsoft.playwright.CLI -D exec.args="install-deps"
```

```bash python
playwright install-deps
```

```bash csharp
pwsh bin/Debug/netX/playwright.ps1 install-deps
```

You can also install the dependencies for a single browser by passing it as an argument:

```bash js
npx playwright install-deps chromium
```

```bash java
mvn exec:java -e -D exec.mainClass=com.microsoft.playwright.CLI -D exec.args="install-deps chromium"
```

```bash python
playwright install-deps chromium
```

```bash csharp
pwsh bin/Debug/netX/playwright.ps1 install-deps chromium
```

It's also possible to combine `install-deps` with `install` so that the browsers and OS dependencies are installed with a single command.

```bash js
npx playwright install --with-deps chromium
```

```bash java
mvn exec:java -e -D exec.mainClass=com.microsoft.playwright.CLI -D exec.args="install --with-deps chromium"
```

```bash python
playwright install --with-deps chromium
```

```bash csharp
pwsh bin/Debug/netX/playwright.ps1 install --with-deps chromium
```

See [system requirements](./intro.md#system-requirements) for officially supported operating systems.


# Install new browsers
npx playwright install
```
Check the [release notes](./release-notes.md) to see what the latest version is and what changes have been released.

```bash

#### Installing Google Chrome & Microsoft Edge

If Google Chrome or Microsoft Edge is not available on your machine, you can install
them using the Playwright command line tool:

```bash lang=js
npx playwright install msedge
```

```bash lang=python
playwright install msedge
```

```bash lang=csharp
pwsh bin/Debug/netX/playwright.ps1 install msedge
```

```batch lang=java
mvn exec:java -e -D exec.mainClass=com.microsoft.playwright.CLI -D exec.args="install msedge"
```

:::warning
Google Chrome or Microsoft Edge installations will be installed at the
default global location of your operating system overriding your current browser installation.
:::

Run with the `--help` option to see a full a list of browsers that can be installed.


## Install behind a firewall or a proxy

By default, Playwright downloads browsers from Microsoft's CDN.

Sometimes companies maintain an internal proxy that blocks direct access to the public
resources. In this case, Playwright can be configured to download browsers via a proxy server.

```bash tab=bash-bash lang=js
HTTPS_PROXY=https://192.0.2.1 npx playwright install
```

```batch tab=bash-batch lang=js
set HTTPS_PROXY=https://192.0.2.1
npx playwright install
```

```powershell tab=bash-powershell lang=js
$Env:HTTPS_PROXY="https://192.0.2.1"
npx playwright install
```

```bash tab=bash-bash lang=python
pip install playwright
HTTPS_PROXY=https://192.0.2.1 playwright install
```

```batch tab=bash-batch lang=python
set HTTPS_PROXY=https://192.0.2.1
pip install playwright
playwright install
```

```powershell tab=bash-powershell lang=python
$Env:HTTPS_PROXY="https://192.0.2.1"
pip install playwright
playwright install
```

```bash tab=bash-bash lang=java
HTTPS_PROXY=https://192.0.2.1 mvn exec:java -e -D exec.mainClass=com.microsoft.playwright.CLI -D exec.args="install"
```

```batch tab=bash-batch lang=java
set HTTPS_PROXY=https://192.0.2.1
mvn exec:java -e -D exec.mainClass=com.microsoft.playwright.CLI -D exec.args="install"
```

```powershell tab=bash-powershell lang=java
$Env:HTTPS_PROXY="https://192.0.2.1"
mvn exec:java -e -D exec.mainClass=com.microsoft.playwright.CLI -D exec.args="install"
```

```bash tab=bash-bash lang=csharp
HTTPS_PROXY=https://192.0.2.1 pwsh bin/Debug/netX/playwright.ps1 install
```

```batch tab=bash-batch lang=csharp
set HTTPS_PROXY=https://192.0.2.1
pwsh bin/Debug/netX/playwright.ps1 install
```

```powershell tab=bash-powershell lang=csharp
$Env:HTTPS_PROXY="https://192.0.2.1"
pwsh bin/Debug/netX/playwright.ps1 install
```

If the requests of the proxy get intercepted with a custom untrusted certificate authority (CA) and it yields to `Error: self signed certificate in certificate chain` while downloading the browsers, you must set your custom root certificates via the [`NODE_EXTRA_CA_CERTS`](https://nodejs.org/api/cli.html#node_extra_ca_certsfile) environment variable before installing the browsers:

```bash tab=bash-bash
export NODE_EXTRA_CA_CERTS="/path/to/cert.pem"
```

```batch tab=bash-batch
set NODE_EXTRA_CA_CERTS="C:\certs\root.crt"
```

```powershell tab=bash-powershell
$Env:NODE_EXTRA_CA_CERTS="C:\certs\root.crt"
```

If your network is slow to connect to Playwright browser archive, you can increase the connection timeout in milliseconds with `PLAYWRIGHT_DOWNLOAD_CONNECTION_TIMEOUT` environment variable:

```bash tab=bash-bash lang=js
PLAYWRIGHT_DOWNLOAD_CONNECTION_TIMEOUT=120000 npx playwright install
```

```batch tab=bash-batch lang=js
set PLAYWRIGHT_DOWNLOAD_CONNECTION_TIMEOUT=120000
npx playwright install
```

```powershell tab=bash-powershell lang=js
$Env:PLAYWRIGHT_DOWNLOAD_CONNECTION_TIMEOUT="120000"
npx playwright install
```

```bash tab=bash-bash lang=python
pip install playwright
PLAYWRIGHT_DOWNLOAD_CONNECTION_TIMEOUT=120000 playwright install
```

```batch tab=bash-batch lang=python
set PLAYWRIGHT_DOWNLOAD_CONNECTION_TIMEOUT=120000
pip install playwright
playwright install
```

```powershell tab=bash-powershell lang=python
$Env:PLAYWRIGHT_DOWNLOAD_CONNECTION_TIMEOUT="120000"
pip install playwright
playwright install
```

```bash tab=bash-bash lang=java
PLAYWRIGHT_DOWNLOAD_CONNECTION_TIMEOUT=120000 mvn exec:java -e -D exec.mainClass=com.microsoft.playwright.CLI -D exec.args="install"
```

```batch tab=bash-batch lang=java
set PLAYWRIGHT_DOWNLOAD_CONNECTION_TIMEOUT=120000
mvn exec:java -e -D exec.mainClass=com.microsoft.playwright.CLI -D exec.args="install"
```

```powershell tab=bash-powershell lang=java
$Env:PLAYWRIGHT_DOWNLOAD_CONNECTION_TIMEOUT="120000"
mvn exec:java -e -D exec.mainClass=com.microsoft.playwright.CLI -D exec.args="install"
```

```bash tab=bash-bash lang=csharp
PLAYWRIGHT_DOWNLOAD_CONNECTION_TIMEOUT=120000 pwsh bin/Debug/netX/playwright.ps1 install
```

```batch tab=bash-batch lang=csharp
set PLAYWRIGHT_DOWNLOAD_CONNECTION_TIMEOUT=120000
pwsh bin/Debug/netX/playwright.ps1 install
```

```powershell tab=bash-powershell lang=csharp
$Env:PLAYWRIGHT_DOWNLOAD_CONNECTION_TIMEOUT="120000"
pwsh bin/Debug/netX/playwright.ps1 install
```

If you are [installing dependencies](#install-system-dependencies) and need to use a proxy on Linux, make sure to run the command as a root user. Otherwise, Playwright will attempt to become a root and will not pass environment variables like `HTTPS_PROXY` to the linux package manager.

```bash js
sudo HTTPS_PROXY=https://192.0.2.1 npx playwright install-deps
```

```bash java
sudo HTTPS_PROXY=https://192.0.2.1 mvn exec:java -e -D exec.mainClass=com.microsoft.playwright.CLI -D exec.args="install-deps"
```

```bash python
sudo HTTPS_PROXY=https://192.0.2.1 playwright install-deps
```

```bash csharp
sudo HTTPS_PROXY=https://192.0.2.1 pwsh bin/Debug/netX/playwright.ps1 install-deps
```


## Using a pre-installed Node.js
* langs: python, java, dotnet
By default, Playwright uses its bundled Node.js runtime for operations such as browser installation and script execution. If you want Playwright to use a pre-installed Node.js binary instead of the bundled runtime, you can specify it using the `PLAYWRIGHT_NODEJS_PATH` environment variable. This can be useful in environments where you need to use a specific version of Node.js or where the bundled runtime is not compatible.

```bash tab=bash-bash lang=js
PLAYWRIGHT_NODEJS_PATH="/usr/local/bin/node" npx playwright install
```

```batch tab=bash-batch lang=js
set PLAYWRIGHT_NODEJS_PATH=C:\Program Files\nodejs\node.exe
npx playwright install
```

```powershell tab=bash-powershell lang=js
$Env:PLAYWRIGHT_NODEJS_PATH="C:\Program Files\nodejs\node.exe"
npx playwright install
```

```bash tab=bash-bash lang=python
pip install playwright
PLAYWRIGHT_NODEJS_PATH="/usr/local/bin/node" playwright install
```

```batch tab=bash-batch lang=python
set PLAYWRIGHT_NODEJS_PATH=C:\Program Files\nodejs\node.exe
pip install playwright
playwright install
```

```powershell tab=bash-powershell lang=python
$Env:PLAYWRIGHT_NODEJS_PATH="C:\Program Files\nodejs\node.exe"
pip install playwright
playwright install
```

```bash tab=bash-bash lang=java
PLAYWRIGHT_NODEJS_PATH="/usr/local/bin/node" mvn exec:java -e -D exec.mainClass=com.microsoft.playwright.CLI -D exec.args="install"
```

```batch tab=bash-batch lang=java
set PLAYWRIGHT_NODEJS_PATH=C:\Program Files\nodejs\node.exe
mvn exec:java -e -D exec.mainClass=com.microsoft.playwright.CLI -D exec.args="install"
```

```powershell tab=bash-powershell lang=java
$Env:PLAYWRIGHT_NODEJS_PATH="C:\Program Files\nodejs\node.exe"
mvn exec:java -e -D exec.mainClass=com.microsoft.playwright.CLI -D exec.args="install"
```

```bash tab=bash-bash lang=csharp
PLAYWRIGHT_NODEJS_PATH="/usr/local/bin/node" pwsh bin/Debug/netX/playwright.ps1 install
```

```batch tab=bash-batch lang=csharp
set PLAYWRIGHT_NODEJS_PATH=C:\Program Files\nodejs\node.exe
pwsh bin/Debug/netX/playwright.ps1 install
```

```powershell tab=bash-powershell lang=csharp
$Env:PLAYWRIGHT_NODEJS_PATH="C:\Program Files\nodejs\node.exe"
pwsh bin/Debug/netX/playwright.ps1 install
```


### Hermetic install
* langs: js

You can opt into the hermetic install and place binaries in the local folder:


```bash tab=bash-bash

### List all installed browsers:

Prints list of browsers from all playwright installations on the machine.

```bash js
npx playwright install --list
```

```bash java
mvn exec:java -e -D exec.mainClass=com.microsoft.playwright.CLI -D exec.args="install --list"
```

```bash python
playwright install --list
```

```bash csharp
pwsh bin/Debug/netX/playwright.ps1 install --list
```


### Uninstall browsers

This will remove the browsers (chromium, firefox, webkit) of the current Playwright installation:

```bash js
npx playwright uninstall
```

```bash java
mvn exec:java -e -D exec.mainClass=com.microsoft.playwright.CLI -D exec.args="uninstall"
```

```bash python
playwright uninstall
```

```bash csharp
pwsh bin/Debug/netX/playwright.ps1 uninstall
```

To remove browsers of other Playwright installations as well, pass `--all` flag:

```bash js
npx playwright uninstall --all
```

```bash java
mvn exec:java -e -D exec.mainClass=com.microsoft.playwright.CLI -D exec.args="uninstall --all"
```

```bash python
playwright uninstall --all
```

```bash csharp
pwsh bin/Debug/netX/playwright.ps1 uninstall --all
```


---


# Scroll the footer into view, forcing an "infinite list" to load more content
await page.get_by_text("Footer text").scroll_into_view_if_needed()
```

```python sync

# Scroll the footer into view, forcing an "infinite list" to load more content
page.get_by_text("Footer text").scroll_into_view_if_needed()
```

```csharp
// Scroll the footer into view, forcing an "infinite list" to load more content
await page.GetByText("Footer text").ScrollIntoViewIfNeededAsync();
```

If you would like to control the scrolling more precisely, use [`method: Mouse.wheel`] or [`method: Locator.evaluate`]:

```js
// Position the mouse and scroll with the mouse wheel
await page.getByTestId('scrolling-container').hover();
await page.mouse.wheel(0, 10);

// Alternatively, programmatically scroll a specific element
await page.getByTestId('scrolling-container').evaluate(e => e.scrollTop += 100);
```

```java
// Position the mouse and scroll with the mouse wheel
page.getByTestId("scrolling-container").hover();
page.mouse.wheel(0, 10);

// Alternatively, programmatically scroll a specific element
page.getByTestId("scrolling-container").evaluate("e => e.scrollTop += 100");
```

```python async

## Record using custom setup

If you would like to use codegen in some non-standard setup (for example, use [`method: BrowserContext.route`]), it is possible to call [`method: Page.pause`] that will open a separate window with codegen controls.

```js
const { chromium } = require('@playwright/test');

(async () => {
  // Make sure to run headed.
  const browser = await chromium.launch({ headless: false });

  // Setup context however you like.
  const context = await browser.newContext({ /* pass any options */ });
  await context.route('**/*', route => route.continue());

  // Pause the page, and start recording manually.
  const page = await context.newPage();
  await page.pause();
})();
```

```java
import com.microsoft.playwright.*;

public class Example {
  public static void main(String[] args) {
    try (Playwright playwright = Playwright.create()) {
      BrowserType chromium = playwright.chromium();
      // Make sure to run headed.
      Browser browser = chromium.launch(new BrowserType.LaunchOptions().setHeadless(false));
      // Setup context however you like.
      BrowserContext context = browser.newContext(/* pass any options */);
      context.route("**/*", route -> route.resume());
      // Pause the page, and start recording manually.
      Page page = context.newPage();
      page.pause();
    }
  }
}
```

```python async
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        # Make sure to run headed.
        browser = await p.chromium.launch(headless=False)

        # Setup context however you like.
        context = await browser.new_context() # Pass any options
        await context.route('**/*', lambda route: route.continue_())

        # Pause the page, and start recording manually.
        page = await context.new_page()
        await page.pause()

asyncio.run(main())
```

```python sync
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # Make sure to run headed.
    browser = p.chromium.launch(headless=False)

    # Setup context however you like.
    context = browser.new_context() # Pass any options
    context.route('**/*', lambda route: route.continue_())

    # Pause the page, and start recording manually.
    page = context.new_page()
    page.pause()
```

```csharp
using Microsoft.Playwright;

using var playwright = await Playwright.CreateAsync();
var chromium = playwright.Chromium;
// Make sure to run headed.
var browser = await chromium.LaunchAsync(new() { Headless = false });

// Setup context however you like.
var context = await browser.NewContextAsync(); // Pass any options
await context.RouteAsync("**/*", route => route.ContinueAsync());

// Pause the page, and start recording manually.
var page = await context.NewPageAsync();
await page.PauseAsync();
```


---


### Step 1: Install Playwright Test for components for your respective framework

<Tabs
  groupId="js-package-manager"
  defaultValue="npm"
  values={[
    {label: 'npm', value: 'npm'},
    {label: 'yarn', value: 'yarn'},
    {label: 'pnpm', value: 'pnpm'},
  ]
}>
<TabItem value="npm">

```bash
npm init playwright@latest -- --ct
```

</TabItem>

<TabItem value="yarn">

```bash
yarn create playwright --ct
```

</TabItem>

<TabItem value="pnpm">

```bash
pnpm create playwright --ct
```

 </TabItem>

</Tabs>

This step creates several files in your workspace:

```html title="playwright/index.html"
<html lang="en">
  <body>
    <div id="root"></div>
    <script type="module" src="./index.ts"></script>
  </body>
</html>
```

This file defines an html file that will be used to render components during testing.
It must contain element with `id="root"`, that's where components are mounted. It must
also link the script called `playwright/index.{js,ts,jsx,tsx}`.

You can include stylesheets, apply theme and inject code into the page where
component is mounted using this script. It can be either a `.js`, `.ts`, `.jsx` or `.tsx` file.

```js title="playwright/index.ts"
// Apply theme here, add anything your component needs at runtime here.
```


## API reference


# Instead of installing all browsers
npx playwright install --with-deps


# Install only Chromium
npx playwright install chromium --with-deps
```

This saves both download time and disk space on your CI machines.
