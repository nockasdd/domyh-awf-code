---
library: android-emulator-internals
version: 1
latest: true
category: infra
official_docs: https://android.googlesource.com/platform/external/qemu/+/emu-master-dev/android/docs/GPU-EMULATION.TXT
last_updated: 2026-03-26
---

# android-emulator-internals v1

> QEMU/AVD architecture, Goldfish vs Ranchu boards, GPU emulation modes (host, angle, swiftshader), ADB bridge, headless CI setup, and impact on capture pipelines.

## Version Comparison
<!-- MANDATORY — helps agent disambiguate versions instantly -->
| Feature          | v1                          | v{latest} |
|:-----------------|:----------------------------|:----------|
| Board            | Goldfish / Ranchu           | —         |
| GPU emulation    | host, swiftshader, angle    | —         |
| Headless CI      | CLI-only, no window         | —         |
| 3rd-party emus   | BlueStacks, LDPlayer, Nox  | —         |
| Cloud emulators  | Cuttlefish (crosvm)         | —         |

## Installation
<!-- MANDATORY — exact install commands with version pinning -->
```bash
# Install emulator and system image via sdkmanager
sdkmanager "platform-tools" "emulator" \
  "system-images;android-34;google_apis;x86_64"

# Create AVD
avdmanager create avd -n hsa-ci-avd \
  -k "system-images;android-34;google_apis;x86_64" \
  --device "pixel_5"

# Verify
emulator -list-avds
```

## Configuration
<!-- MANDATORY — complete config example, annotated -->
```bash
# Start emulator headless (no window, no audio, no boot animation)
emulator -avd hsa-ci-avd -no-window -no-audio -no-boot-anim -accel on

# Start with specific GPU mode
emulator -avd hsa-ci-avd -gpu host        # Host GPU (fastest, may crash)
emulator -avd hsa-ci-avd -gpu angle       # ANGLE/DirectX backend (Windows)
emulator -avd hsa-ci-avd -gpu swiftshader_indirect  # Software (headless/CI)

# Start with custom port (avoid conflicts with multiple instances)
emulator -avd hsa-ci-avd -port 5556

# Wait for device boot (CI script pattern)
adb wait-for-device
adb shell 'while [ -z "$(getprop sys.boot_completed)" ]; do sleep 1; done'
adb shell input keyevent 82  # unlock screen
```

### AVD config.ini GPU Settings
```ini
# Located at: ~/.android/avd/<name>.avd/config.ini
hw.gpu.enabled=yes
hw.gpu.mode=host
# Alternatives: angle, swiftshader_indirect, mesa, auto, guest
```

## Core API
<!-- MANDATORY — most-used APIs with params, types, return values -->

### Goldfish vs Ranchu Architecture

```text
Goldfish (qemu1 — legacy):
  Board: goldfish
  Storage: goldfish NAND virtual device
  I/O: goldfish_pipe (custom IPC to host)
  GPU: goldfish_fb (framebuffer)
  Status: deprecated, used in pre-API 25

Ranchu (qemu2 — modern):
  Board: ranchu (QEMU 2.x+ based)
  Storage: virtio-blk (faster I/O)
  I/O: virtio-console + goldfish_pipe (hybrid)
  GPU: virtio-gpu or host opengl passthrough
  Status: current default for Android Studio emulator
```

### Hardware Acceleration Backends

| Host OS   | Backend  | Mechanism                        | Performance |
|:----------|:---------|:---------------------------------|:------------|
| Linux     | KVM      | Kernel-based Virtual Machine     | ★★★★★       |
| Windows   | WHPX     | Windows Hypervisor Platform      | ★★★★        |
| Windows   | HAXM     | Intel HAXM (deprecated)          | ★★★         |
| macOS     | HVF      | Hypervisor.framework             | ★★★★★       |

### GPU Emulation Modes & ANGLE

```text
Mode: host
  Backend: Host GPU via OpenGL/Vulkan passthrough
  Performance: Fastest rendering, full GPU accel
  Risk: Driver compatibility issues (crashes on some GPU/driver combos)
  Capture: DXGI/host-side capture works well

Mode: angle (Windows only)
  Backend: ANGLE translates GLES → DirectX 11
  Performance: Near-host speed, more stable than raw OpenGL on Windows
  Capture: DXGI capture works (DirectX surface)

Mode: swiftshader_indirect
  Backend: CPU-based software rendering (Google SwiftShader)
  Performance: Slow (~10-30% of GPU speed)
  Capture: No GPU surface → DXGI capture does NOT work
  Use case: Headless CI, cloud instances without GPU

Mode: mesa
  Backend: Mesa3D LLVMpipe software rendering
  Performance: Similar to swiftshader
  Use case: Fallback for obscure GPU drivers

Mode: auto (default)
  Behavior: Tries host → angle → swiftshader in order
```

| GPU Mode     | FPS (typical) | DXGI Capture | Headless CI | Stability |
|:-------------|:--------------|:-------------|:------------|:----------|
| host         | 30-60         | ✅           | ❌ (needs display) | ⚠️ Driver dependent |
| angle        | 25-50         | ✅           | ❌           | ✅ Stable on Windows |
| swiftshader  | 5-15          | ❌           | ✅           | ✅ Very stable |
| mesa         | 5-15          | ❌           | ✅           | ✅ Stable |

### Impact on Capture Pipelines

```text
Pipeline Selection by GPU Mode:

GPU=host/angle (with display):
  → Host-side capture (DXGI/PrintWindow) is BEST: ultra-low latency, 60fps
  → scrcpy also works but adds extra overhead
  → Recommended for local automation workstations

GPU=swiftshader/mesa (headless/CI):
  → DXGI capture NOT available (no GPU surface to capture)
  → Must use device-side capture: scrcpy, minicap, or screenrecord
  → screencap loop (pseudo-stream) is simplest fallback
  → Recommended for CI/CD test clusters

Multi-instance (many emulators):
  → Each instance needs unique -port value
  → ADB auto-discovers on ports 5555-5585 (odd ports)
  → Agent must maintain port registry to avoid collision
```

### Emulator Console (Telnet)

```bash
# Connect to emulator console (port = emulator port - 1, e.g., 5554)
telnet localhost 5554

# Authenticate (required on newer emulator versions)
auth <token_from_~/.emulator_console_auth_token>

# Useful console commands
avd name                    # Get AVD name
avd snapshot save clean     # Save snapshot for fast boot
avd snapshot load clean     # Restore snapshot (~3s boot)
geo fix -122.08 37.42       # Set GPS location
sms send 12345 "Test SMS"   # Inject SMS
network delay gprs          # Simulate slow network
power status full           # Set battery to full
kill                        # Shutdown emulator
```

### 3rd-Party Emulators (BlueStacks/LDPlayer/Nox)

```text
LDPlayer ADB Port Convention:
  Instance 0: TCP 5555
  Instance 1: TCP 5557
  Instance 2: TCP 5559
  Pattern: 5555 + (instance_index * 2)

BlueStacks ADB Port:
  Varies by version; check BlueStacks settings or adb devices
  Typically: TCP 5555 or 5575

Agent strategy:
  1. Scan ports 5555-5585 with adb connect 127.0.0.1:<port>
  2. Filter by adb devices -l (check model name)
  3. Treat discovered emulators same as physical devices for ADB commands
  4. For host-side capture: identify window handle via FindWindow/EnumWindows
```

### Cuttlefish (Cloud Emulator)

```bash
# Cuttlefish is Google's cloud-native Android emulator
# Uses crosvm (Chrome OS VM monitor) instead of QEMU
# Device name: vsoc_x86_64 / cuttlefish

# Typical CI deployment:
launch_cvd --gpu_mode=drm_virgl --start_webrtc=true --num_instances=4

# Connect via ADB (cuttlefish binds on predictable ports)
adb connect localhost:6520
```

## Common Patterns
<!-- RECOMMENDED — real-world usage examples -->

```bash
# CI Pattern: headless emulator with snapshot for fast clean-state boot
emulator -avd hsa-ci-avd -no-window -gpu swiftshader_indirect \
  -no-audio -no-boot-anim -snapshot clean-state &
adb wait-for-device
adb shell 'while [ -z "$(getprop sys.boot_completed)" ]; do sleep 1; done'

# Run test suite
./gradlew connectedAndroidTest

# Cleanup
adb emu kill
```

```python
# Multi-emulator orchestration pattern
import subprocess

def start_emulator(avd_name: str, port: int, gpu: str = "swiftshader_indirect"):
    cmd = [
        "emulator", "-avd", avd_name, "-port", str(port),
        "-no-window", "-no-audio", "-no-boot-anim",
        "-gpu", gpu
    ]
    return subprocess.Popen(cmd)

# Start 3 emulators on different ports
procs = [
    start_emulator("hsa-ci-avd", 5556, "swiftshader_indirect"),
    start_emulator("hsa-ci-avd", 5558, "swiftshader_indirect"),
    start_emulator("hsa-ci-avd", 5560, "swiftshader_indirect"),
]

# Wait for all to boot, then run parallel tests...
```

## Gotchas & Breaking Changes
<!-- CRITICAL — things that trip up agents and humans -->

- ⚠️ **GPU mode `host` crashes**: On some Nvidia/AMD driver combos, `host` GPU triggers segfaults in OpenGL. Fallback to `angle` (Windows) or `swiftshader_indirect` (Linux CI).
- ⚠️ **Multiple instances port conflict**: Without explicit `-port`, emulators fight over 5554/5555. Always assign unique ports.
- ⚠️ **Snapshot compatibility**: AVD snapshots are tied to the exact emulator version. After Android SDK update, delete old snapshots to avoid boot loops.
- ⚠️ **HAXM deprecated**: Intel HAXM is deprecated in favor of WHPX (Windows) and HVF (macOS). Remove HAXM if using newer emulator versions.
- ⚠️ **Cuttlefish vs QEMU**: Cuttlefish does NOT use QEMU console commands. Use `adb` and WebRTC interface instead.

## Migration
<!-- MANDATORY if not latest — checklist to upgrade to next version -->

- [ ] Standardize AVD config for all CI runners (Linux: KVM + swiftshader, Windows: WHPX + angle).
- [ ] Add GPU health check: render a small OpenGL test, fallback to swiftshader on failure.
- [ ] Migrate from HAXM to WHPX on Windows build machines.
- [ ] Document port allocation strategy for multi-emulator test clusters.

<!--
BM25 DESIGN RULES:
- H1 = library name (root search anchor)
- H2 = feature category
- Code:prose ratio >= 70:30
- Keep 5-30KB per file
-->
