---
library: android-native-csharp-cpp
version: 1
latest: true
category: backend
official_docs: https://github.com/SharpAdb/AdvancedSharpAdbClient
last_updated: 2026-03-26
---

# android-native-csharp-cpp v1

> C# AdvancedSharpAdbClient integration, EmguCV vision pipelines, host-accelerated emulator capture (DXGI), performance queuing strategies, and C++ ADB protocol clients with native hook framework architecture (Dobby, SandHook, LSPlant).

## Version Comparison
<!-- MANDATORY — helps agent disambiguate versions instantly -->
| Feature                | v1                            | v{latest} |
|:-----------------------|:------------------------------|:----------|
| C# ADB client         | AdvancedSharpAdbClient 2.x    | —         |
| Screen pipeline        | ADB/scrcpy + EmguCV           | —         |
| Host capture           | DXGI + IFrameProvider         | —         |
| Performance strategies | Ring buffer, skip-frame, ROI  | —         |
| Native hooks (arch)    | SandHook/Dobby/LSPlant        | —         |

## Installation
<!-- MANDATORY — exact install commands with version pinning -->
```bash
# C# / .NET
dotnet add package AdvancedSharpAdbClient --version 2.*
dotnet add package Emgu.CV --version 4.*
dotnet add package Emgu.CV.runtime.windows --version 4.*

# For DXGI capture (SharpDX or Vortice)
dotnet add package Vortice.DXGI --version 3.*
dotnet add package Vortice.Direct3D11 --version 3.*
```

## Configuration
<!-- MANDATORY — complete config example, annotated -->

```csharp
using AdvancedSharpAdbClient;
using System.Net;

// 1. Start ADB server (points to platform-tools adb.exe)
AdbServer server = new AdbServer();
StartServerResult result = server.StartServer(
    @"C:\android-sdk\platform-tools\adb.exe",
    restartServerIfNewer: false
);
Console.WriteLine($"ADB server: {result}");

// 2. Create client connected to local ADB server
AdbClient client = new AdbClient(
    new IPEndPoint(IPAddress.Loopback, AdbClient.AdbServerPort) // 5037
);

// 3. Get device list
var devices = client.GetDevices();
foreach (var d in devices)
    Console.WriteLine($"{d.Serial} — {d.Model} — {d.State}");
```

## Core API
<!-- MANDATORY — most-used APIs with params, types, return values -->

### AdvancedSharpAdbClient Device Operations

```csharp
var device = client.GetDevices().First();

// Execute shell command and capture output
var receiver = new ConsoleOutputReceiver();
client.ExecuteRemoteCommand("getprop ro.build.version.release", device, receiver);
string androidVersion = receiver.ToString().Trim();

// Install APK
var pm = new PackageManager(client, device);
pm.InstallPackage(@"C:\apps\target.apk", reinstall: true);

// Send touch / input events
client.ExecuteRemoteCommand("input tap 500 700", device, receiver);
client.ExecuteRemoteCommand("input swipe 300 1000 300 300 200", device, receiver);
client.ExecuteRemoteCommand("input keyevent KEYCODE_HOME", device, receiver);
client.ExecuteRemoteCommand("input text 'Hello World'", device, receiver);
```

### AdvancedSharpAdbClient (High-Level Methods)

```csharp
// Click at coordinates
client.Click(device, new Cords(500, 700));

// Swipe gesture
client.Swipe(device, new Cords(500, 1000), new Cords(500, 300), speed: 500);

// Send key event
client.SendKeyEvent(device, "KEYCODE_BACK");

// Send text input
client.SendText(device, "automation_text");

// Get screenshot as Bitmap
System.Drawing.Image screenshot = client.GetFrameBuffer(device);
screenshot.Save("screen.png");
```

### EmguCV (OpenCV) Template Matching Pipeline

```csharp
using Emgu.CV;
using Emgu.CV.CvEnum;
using Emgu.CV.Structure;

/// <summary>
/// Find template image on screen and return center coordinates.
/// Returns null if confidence below threshold.
/// </summary>
public static (int x, int y)? FindTemplate(
    Mat screen, Mat template, double threshold = 0.85)
{
    using var result = new Mat();
    CvInvoke.MatchTemplate(screen, template, result, TemplateMatchingType.CcoeffNormed);

    double minVal = 0, maxVal = 0;
    System.Drawing.Point minLoc = default, maxLoc = default;
    CvInvoke.MinMaxLoc(result, ref minVal, ref maxVal, ref minLoc, ref maxLoc);

    if (maxVal < threshold) return null;

    int cx = maxLoc.X + template.Width / 2;
    int cy = maxLoc.Y + template.Height / 2;
    return (cx, cy);
}

// Usage in automation loop
var screen = CvInvoke.Imread("screen.png");
var template = CvInvoke.Imread("login_button.png");
var match = FindTemplate(screen, template);
if (match.HasValue)
    client.Click(device, new Cords(match.Value.x, match.Value.y));
```

### Host-Accelerated Emulator Capture (IFrameProvider)

Architecture for decoupling capture backend from automation logic:

```csharp
/// <summary>
/// Abstraction for frame capture from any source.
/// Implementations: DxgiProvider, MinicapProvider, ScrcpyProvider, ScreencapProvider
/// </summary>
public interface IFrameProvider : IDisposable
{
    /// <summary>Get latest frame. Returns false if no new frame available.</summary>
    bool TryGetFrame(out Mat frame);

    /// <summary>Actual display dimensions (for coordinate mapping).</summary>
    (int Width, int Height) DisplaySize { get; }

    /// <summary>Source identifier for logging.</summary>
    string SourceName { get; }
}

/// <summary>
/// Abstraction for sending input to device.
/// Implementations: AdbInputSink, MinitouchSink, ScrcpyControlSink
/// </summary>
public interface IInputSink : IDisposable
{
    void Tap(int x, int y);
    void Swipe(int x1, int y1, int x2, int y2, int durationMs);
    void KeyEvent(string keycode);
}
```

```csharp
// DXGI Desktop Duplication implementation (Windows 8+, DirectX 11)
// Requires: Vortice.DXGI, Vortice.Direct3D11
public class DxgiFrameProvider : IFrameProvider
{
    private readonly OutputDuplication _duplication;
    private readonly Texture2D _stagingTexture;

    public (int Width, int Height) DisplaySize { get; }
    public string SourceName => "DXGI";

    public DxgiFrameProvider(int outputIndex = 0)
    {
        // 1. Create D3D11 device
        // 2. Get DXGI output
        // 3. Create OutputDuplication
        // 4. Create staging texture for CPU readback
    }

    public bool TryGetFrame(out Mat frame)
    {
        // 1. AcquireNextFrame(timeout: 100ms)
        // 2. Map staging texture to CPU memory
        // 3. Copy BGRA pixels into Mat(height, width, DepthType.Cv8U, 4)
        // 4. ReleaseFrame()
        frame = new Mat(/* ... */);
        return true;
    }

    public void Dispose()
    {
        _duplication?.Dispose();
        _stagingTexture?.Dispose();
    }
}
```

```csharp
// Screencap-based provider (fallback, works everywhere)
public class ScreencapFrameProvider : IFrameProvider
{
    private readonly AdbClient _client;
    private readonly DeviceData _device;

    public (int Width, int Height) DisplaySize { get; }
    public string SourceName => "Screencap";

    public bool TryGetFrame(out Mat frame)
    {
        var image = _client.GetFrameBuffer(_device);
        using var ms = new MemoryStream();
        image.Save(ms, System.Drawing.Imaging.ImageFormat.Png);
        var bytes = ms.ToArray();
        frame = CvInvoke.Imdecode(bytes, ImreadModes.Color);
        return frame != null;
    }

    public void Dispose() { }
}
```

### Performance & Queuing Strategies

```csharp
// Double-buffer pattern: capture thread writes to one buffer,
// inference thread reads from the other, swap atomically.
public class DoubleBuffer<T> where T : class
{
    private T _front;  // read by consumer
    private T _back;   // written by producer
    private readonly object _lock = new();

    public void Write(T item)
    {
        lock (_lock) { _back = item; }
    }

    public T Read()
    {
        lock (_lock) { return _front; }
    }

    public void Swap()
    {
        lock (_lock) { (_front, _back) = (_back, _front); }
    }
}
```

```csharp
// Skip-frame policy: always process the latest frame, drop stale ones
public class LatestFrameQueue
{
    private Mat? _latest;
    private readonly object _lock = new();

    public void Enqueue(Mat frame)
    {
        lock (_lock)
        {
            _latest?.Dispose();  // release old frame
            _latest = frame;
        }
    }

    public Mat? Dequeue()
    {
        lock (_lock)
        {
            var frame = _latest;
            _latest = null;
            return frame;
        }
    }
}
```

```text
Performance Strategy Reference:

| Strategy       | Mechanism                              | When to Use                          |
|:---------------|:---------------------------------------|:-------------------------------------|
| Double-buffer  | Two buffers swapped atomically         | Capture + inference on separate threads |
| Skip-frame     | Keep only latest, dispose old frames   | Real-time where freshness > completeness |
| ROI cropping   | Crop region before template matching   | Reduce OpenCV processing time by 60-80% |
| --max-size     | Reduce scrcpy stream resolution at src | Lower network + decode overhead      |
| Ring buffer    | Fixed-size circular buffer (N frames)  | When analysis needs temporal context  |
```

```csharp
// ROI cropping: only process the region of interest
public static Mat CropROI(Mat fullFrame, System.Drawing.Rectangle roi)
{
    return new Mat(fullFrame, roi);
}

// Usage: crop health bar region before template matching
var roi = new System.Drawing.Rectangle(0, 0, 300, 50); // top-left area
var cropped = CropROI(screen, roi);
var match = FindTemplate(cropped, healthBarTemplate);
```

## Common Patterns
<!-- RECOMMENDED — real-world usage examples -->

```csharp
// Full automation loop: capture → match → act
public async Task AutomationLoop(IFrameProvider capture, IInputSink input)
{
    var template = CvInvoke.Imread("target.png");
    var frameQueue = new LatestFrameQueue();

    // Capture thread
    _ = Task.Run(() =>
    {
        while (true)
        {
            if (capture.TryGetFrame(out Mat frame))
                frameQueue.Enqueue(frame);
            Thread.Sleep(33); // ~30fps
        }
    });

    // Inference + action thread
    while (true)
    {
        var frame = frameQueue.Dequeue();
        if (frame == null) { await Task.Delay(10); continue; }

        var match = FindTemplate(frame, template);
        if (match.HasValue)
        {
            input.Tap(match.Value.x, match.Value.y);
            await Task.Delay(500); // cooldown
        }
        frame.Dispose();
    }
}
```

```text
Pipeline Architecture Selection:

Flow 1 (Device-side capture):
  ADB (scrcpy/minicap/screenrecord) → decode → EmguCV → ADB input
  → Works with physical devices and emulators
  → Latency: 30-500ms depending on method

Flow 2 (Host-side emulator capture):
  Emulator window (DXGI/PrintWindow) → DirectX → EmguCV → ADB/minitouch
  → Ultra-fast (~10-30ms), emulator only
  → Requires GPU mode: host or angle
```

## Gotchas & Breaking Changes
<!-- CRITICAL — things that trip up agents and humans -->

- ⚠️ **AdvancedSharpAdbClient version breaks**: API surface changes between major versions (exception types, method signatures). Always pin in `.csproj`.
- ⚠️ **EmguCV native DLLs**: Must install the correct runtime package (`Emgu.CV.runtime.windows` for Windows). Missing native DLLs cause `DllNotFoundException` at runtime.
- ⚠️ **DXGI requires admin rights** on some Windows configurations. `OutputDuplication` may fail with `DXGI_ERROR_ACCESS_DENIED` if UAC blocks it.
- ⚠️ **Mat disposal**: OpenCV `Mat` objects are unmanaged memory. Failure to `Dispose()` causes memory leaks — especially critical in tight loops.
- ⚠️ **Native hook frameworks** (SandHook/Dobby/LSPlant) are Android ART version-dependent. Never hardcode memory offsets — they change per Android version and OEM fork.

## Migration
<!-- MANDATORY if not latest — checklist to upgrade to next version -->

- [ ] Create `IAdbClient` abstraction (AdvancedSharpAdbClient vs AdbDotNet) for implementation swap.
- [ ] Implement `IFrameProvider` factory: auto-select DXGI (emulator) or Screencap (device) based on `adb devices -l` output.
- [ ] Add disposable frame pooling to reduce GC pressure on Mat objects.
- [ ] Move native hook content to architecture-only descriptions — no version-specific offsets.

<!--
BM25 DESIGN RULES:
- H1 = library name (root search anchor)
- H2 = feature category
- Code:prose ratio >= 70:30
- Keep 5-30KB per file
-->
