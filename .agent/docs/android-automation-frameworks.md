---
library: android-automation-frameworks
version: 1
latest: true
category: testing
official_docs: https://appium.io/docs/en/latest/
last_updated: 2026-03-26
---

# android-automation-frameworks v1

> High-level Android automation with Appium, UIAutomator2, Espresso, Maestro, Airtest, Poco, and pure-python-adb. Includes orchestration design patterns for agent-driven control.

## Version Comparison
<!-- MANDATORY — helps agent disambiguate versions instantly -->
| Feature                    | v1                          | v{latest} |
|:---------------------------|:----------------------------|:----------|
| Appium WebDriver mapping   | W3C spec                    | —         |
| UIAutomator2 JSON-RPC      | HTTP/JSONRPC patterns       | —         |
| Espresso idling resources  | sync + anti-flaky            | —         |
| Maestro declarative flows  | YAML → ADB/Appium mapping   | —         |
| Airtest/Poco               | image + hierarchy drivers   | —         |
| pure-python-adb            | async + multi-device usage  | —         |

## Installation
<!-- MANDATORY — exact install commands with version pinning -->
```bash
# Appium server (Node.js)
npm install -g appium@latest
appium driver install uiautomator2

# Python automation stacks
pip install pure-python-adb Appium-Python-Client airtest pocoui

# Maestro (macOS/Linux)
curl -Ls "https://get.maestro.mobile.dev" | bash
```

## Configuration
<!-- MANDATORY — complete config example, annotated -->

### Appium Desired Capabilities (W3C format)
```json
{
  "platformName": "Android",
  "appium:automationName": "UiAutomator2",
  "appium:appPackage": "com.example.app",
  "appium:appActivity": ".MainActivity",
  "appium:newCommandTimeout": 300,
  "appium:udid": "emulator-5554",
  "appium:noReset": true
}
```

### pure-python-adb Client Setup
```python
from ppadb.client import Client as AdbClient

# Connect to local ADB server (must be running)
client = AdbClient(host="127.0.0.1", port=5037)
devices = client.devices()
for d in devices:
    print(f"{d.serial} — {d.shell('getprop ro.product.model').strip()}")
```

### Maestro Flow File (YAML)
```yaml
# maestro/login-flow.yaml
appId: com.example.app
---
- launchApp
- tapOn: "Email"
- inputText: "test@example.com"
- tapOn: "Password"
- inputText: "secret123"
- tapOn: "Login"
- assertVisible: "Welcome"
```

## Core API
<!-- MANDATORY — most-used APIs with params, types, return values -->

### UIAutomator2 JSON-RPC Pattern

UIAutomator2 runs a server APK on-device, exposing an HTTP/JSONRPC endpoint (default port 9008).

```bash
# Forward port from device to host
adb forward tcp:9008 tcp:9008
```

```json
// POST http://127.0.0.1:9008/jsonrpc/0
// Click element by text
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "click",
  "params": [{"text": "Settings", "className": "android.widget.TextView"}]
}

// Scroll to element
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "scrollTo",
  "params": [{"text": "Advanced", "scrollable": true}]
}

// Dump UI hierarchy (XML)
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "dumpWindowHierarchy",
  "params": [false]
}
```

### Appium WebDriver Protocol Mapping
```python
from appium import webdriver
from appium.options.android import UiAutomator2Options

options = UiAutomator2Options()
options.platform_name = "Android"
options.udid = "emulator-5554"
options.app_package = "com.example.app"
options.app_activity = ".MainActivity"

driver = webdriver.Remote("http://localhost:4723", options=options)

# Find and click element
el = driver.find_element(by="xpath", value="//*[@text='OK']")
el.click()

# Swipe gesture
driver.swipe(start_x=500, start_y=1500, end_x=500, end_y=300, duration=300)

# Take screenshot into memory
png_bytes = driver.get_screenshot_as_png()

driver.quit()
```

| Appium WebDriver Command           | UIAutomator2 / ADB Protocol Mapping                     |
|:------------------------------------|:---------------------------------------------------------|
| `POST /session`                     | Install `appium-uiautomator2-server.apk`, start service |
| `POST /element/{id}/click`          | JSONRPC `click` with element ID                          |
| `POST /appium/device/install_app`   | `adb -s <serial> install <apk_path>`                     |
| `GET /source`                       | `dumpWindowHierarchy` → XML                              |
| `POST /actions` (W3C Actions)       | Translated to `injectInputEvent` via service             |

### Espresso Idling Resources (Anti-Flaky Pattern)

Espresso uses idling resources to synchronize test execution with app state. This is critical for avoiding flaky tests.

```java
// Register custom idling resource for network calls
IdlingRegistry.getInstance().register(new OkHttp3IdlingResource("OkHttp", okHttpClient));

// Espresso waits until all idling resources are idle before proceeding
onView(withText("Submit")).perform(click());
// ^ This call blocks until idling resources signal idle
onView(withText("Success")).check(matches(isDisplayed()));

// Unregister when done
IdlingRegistry.getInstance().unregister(resource);
```

## Common Patterns
<!-- RECOMMENDED — real-world usage examples -->

### Airtest (Image-Based) + Poco (Hierarchy-Based)
```python
from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

# Initialize device connection
init_device("Android", uuid="emulator-5554")

# Image-based: click by template matching (good for game UIs)
if exists(Template("ok_button.png", threshold=0.8)):
    touch(Template("ok_button.png"))

# Hierarchy-based: click by text (good for native Android UIs)
poco = AndroidUiautomationPoco(use_airtest_input=True)
poco(text="Play Now").click()
poco(name="com.example:id/score_label").wait_for_appearance(timeout=10)
score = poco(name="com.example:id/score_label").get_text()
```

### pure-python-adb Multi-Device Automation
```python
from ppadb.client import Client as AdbClient

client = AdbClient(host="127.0.0.1", port=5037)

def run_on_all_devices(shell_cmd: str) -> dict[str, str]:
    results = {}
    for device in client.devices():
        output = device.shell(shell_cmd)
        results[device.serial] = output.strip()
    return results

# Install APK on all connected devices
for device in client.devices():
    device.install("app-release.apk", reinstall=True)

# Capture screenshot from specific device
device = client.device("192.168.1.100:5555")
raw_png = device.screencap()
with open("screen.png", "wb") as f:
    f.write(raw_png)
```

### Orchestration Patterns: When to Choose What

| Scenario                       | Recommended Stack              | Rationale                                    |
|:-------------------------------|:-------------------------------|:---------------------------------------------|
| Native Android UI testing      | Appium + UIAutomator2          | W3C standard, rich element selectors         |
| Game automation (Unity/Cocos)  | Airtest (image-based)          | No accessibility tree in game renderers      |
| Game + native menu hybrid      | Airtest + Poco                 | Image for game, hierarchy for menus          |
| Declarative smoke tests        | Maestro                        | YAML flows, fast iteration, CI-friendly      |
| Custom ADB scripting           | pure-python-adb (ppadb)        | Lightweight, direct control, multi-device    |
| Anti-flaky integration tests   | Espresso (on-device)           | Idling resources prevent race conditions     |

### Agent Automation Design Patterns

```text
Pattern 1 — Vision-Driven Loop (Low-fps, 1–5 fps)
  screencap / exec-out gzip → downscale / ROI crop → OpenCV template match → decision tree → adb input tap
  Target: turn-based games, menu navigation, QA screenshot validation
  CPU: low | Latency: 200–500ms per cycle

Pattern 2 — Stream-Driven Loop (High-fps, 15–60 fps)
  scrcpy / minicap H.264/JPEG stream → decoder → ring buffer → inference engine → minitouch / scrcpy input
  Target: real-time action games, continuous monitoring
  CPU: high | Latency: 30–100ms per cycle
  Requires: skip-frame policy, backpressure management

Pattern 3 — Emulator Host-GPU Loop (Emulator only)
  Emulator GPU mode (host/angle) → DXGI / PrintWindow capture → EmguCV → adb / minitouch input
  Target: emulator-only blitz automation
  CPU: medium | Latency: 10–50ms per cycle
  Restriction: Windows host only, not applicable to physical devices
```

## Gotchas & Breaking Changes
<!-- CRITICAL — things that trip up agents and humans -->

- ⚠️ **Appium W3C vs JSONWire**: Newer Appium drivers (2.x+) only support W3C WebDriver protocol. Legacy `desiredCapabilities` format is rejected — use `appium:options` prefix.
- ⚠️ **Airtest DPI sensitivity**: Image templates are resolution-dependent. Always normalize display size (`adb shell wm size 1080x1920`) before capturing templates.
- ⚠️ **UIAutomator2 StaleObject**: Calling methods on elements after the UI has changed throws `UiObjectNotFoundException`. Re-find element before each interaction.
- ⚠️ **Port forwarding conflicts**: When automating >2 devices, register unique forward ports per device (e.g., `adb -s <serial> forward tcp:900N tcp:9008`) to prevent socket collision.
- ⚠️ **Maestro** currently only supports Android and iOS — no emulator-specific optimizations. Best used for smoke tests, not pixel-precise automation.

## Migration
<!-- MANDATORY if not latest — checklist to upgrade to next version -->

- [ ] Migrate all Appium tests from JSONWire to W3C capabilities format (`appium:` prefix).
- [ ] Standardize `init_device()` / `AndroidUiautomationPoco()` to support multi-device via shared config.
- [ ] Add `IFrameSource` abstraction to decouple capture backend (screencap vs scrcpy vs DXGI) from automation logic.
- [ ] Implement skip-frame / backpressure middleware for stream-driven loops.

<!--
BM25 DESIGN RULES:
- H1 = library name (root search anchor)
- H2 = feature category
- Code:prose ratio >= 70:30
- Keep 5-30KB per file
-->
