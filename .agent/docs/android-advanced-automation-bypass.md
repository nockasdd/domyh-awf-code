---
library: android-advanced-automation-bypass
version: 1
latest: true
category: other
official_docs: https://frida.re
last_updated: 2026-03-26
---

# android-advanced-automation-bypass v1

> Research-focused overview of root hiding (Zygisk, Shamiko, KernelSU), Frida dynamic instrumentation (Java and native hooks), SSL pinning bypass, memory reading (`/proc/pid/mem`), and ART hooking frameworks (SandHook, LSPlant, Dobby). For Security Research and QA Robustness testing only.

## Scope, Legal & Ethics Disclaimer

```text
⚠️ IMPORTANT: ETHICAL USE ONLY

The techniques documented here are intended EXCLUSIVELY for:
  1. Security Research — vulnerability assessment, pen-testing lab environments
  2. QA Robustness — testing root/tamper detection strength of your own apps
  3. Forensics — analyzing malware behavior in sandboxed environments
  4. Education — understanding Android security architecture

This documentation does NOT endorse or support:
  ✗ Bypassing protections on apps you do not own or have authorization to test
  ✗ Game cheating or Terms of Service violations
  ✗ Distribution of cracked/modified applications
  ✗ Any activity that violates applicable laws or regulations

All examples use controlled test environments and target apps built for testing.
```

## Version Comparison
<!-- MANDATORY — helps agent disambiguate versions instantly -->
| Feature            | v1                            | v{latest} |
|:-------------------|:------------------------------|:----------|
| Zygisk overview    | Zygote injection model        | —         |
| Shamiko model      | Root hiding strategy          | —         |
| KernelSU           | Kernel-level su daemon         | —         |
| Frida patterns     | Java & native hooks           | —         |
| ART hook frameworks| SandHook, LSPlant, Dobby      | —         |
| Memory reading     | `/proc/pid/mem`               | —         |

## Installation
<!-- MANDATORY — exact install commands with version pinning -->
```bash
# Frida tools (host)
pip install frida-tools==12.*

# Verify connection to device
frida-ps -U              # list processes via USB
frida-ps -H 192.168.1.5  # list processes via TCP

# Frida server (device) — must match frida-tools version
# Download from: https://github.com/frida/frida/releases
adb push frida-server-16.x.x-android-arm64 /data/local/tmp/frida-server
adb shell "chmod 755 /data/local/tmp/frida-server"
adb shell "/data/local/tmp/frida-server -D &"

# Objection (Frida-based exploration toolkit)
pip install objection
objection -g com.example.app explore
```

## Configuration
<!-- MANDATORY — complete config example, annotated -->

### Frida Client Setup (Python)
```python
import frida

# Connect to USB device
device = frida.get_usb_device(timeout=10)

# Attach to running process
session = device.attach("com.example.app")

# Or spawn new process (inject at startup)
pid = device.spawn(["com.example.app"])
session = device.attach(pid)

# Load JavaScript hook script
with open("hook_script.js", "r") as f:
    script_source = f.read()
script = session.create_script(script_source)
script.on("message", lambda msg, data: print(f"[Frida] {msg}"))
script.load()

# Resume if spawned
device.resume(pid)

# Keep script alive
import sys
sys.stdin.read()
```

### Magisk/Zygisk Configuration
```text
Magisk Manager → Settings:
  ✅ Zygisk: Enabled
  ✅ DenyList: Configured for target apps (banking, game checker apps)

Module installation:
  Magisk → Modules → Install from ZIP
    → Shamiko-vX.Y.Z.zip (closed-source root hider)
    → OR ZygiskAssistant-vX.Y.Z.zip (open-source alternative)

Reboot required after module installation.
```

## Core API
<!-- MANDATORY — most-used APIs with params, types, return values -->

### Zygisk Architecture (Zygote Injection)

```text
Android Boot Sequence (relevant part):

init → zygote64 (com.android.internal.os.ZygoteInit)
  ↓
Zygote process starts, loads system libraries
  ↓
Magisk's Zygisk hooks ZygoteInit.forkAndSpecialize()
  ↓
When app requests launch: Zygote forks a child process
  ↓
Zygisk injects native library into the forked child
  ↓
The child app process now runs with injected module loaded
  ↓
Module can hook any Java/native method in the app's address space

Key files on device (Magisk systemless):
  /data/adb/magisk/                  — Magisk binaries
  /data/adb/modules/<module_name>/   — Zygisk modules
  /data/adb/magisk.db                — Policy database
```

### Shamiko / ZygiskAssistant Root Hiding

```text
Root Detection APIs that Shamiko intercepts:

1. File existence checks:
   /system/app/Superuser.apk
   /system/xbin/su
   /sbin/su
   /data/local/xbin/su
   → Shamiko hooks open()/access()/stat() to return ENOENT

2. System properties:
   ro.secure=1         (should be 1 on production)
   ro.debuggable=0     (should be 0 on production)
   ro.build.tags       (should NOT contain "test-keys")
   → Shamiko hooks __system_property_get() to return safe values

3. SELinux status:
   getenforce → returns "Enforcing" (even if actually Permissive)

4. Package manager:
   pm list packages → filters out com.topjohnwu.magisk

5. Process list:
   /proc/self/maps → removes entries containing magisk/frida/xposed
   /proc/<pid>/status → hides TracerPid if Frida is attached

6. SafetyNet / Play Integrity:
   Magisk's DenyList + Shamiko prevents detection of modified boot images
```

### Frida Java Hooks

```javascript
// Hook Java method: bypass root detection
Java.perform(function() {
    // Target: com.example.app.security.RootChecker.isDeviceRooted()
    var RootChecker = Java.use("com.example.app.security.RootChecker");

    RootChecker.isDeviceRooted.implementation = function() {
        console.log("[*] RootChecker.isDeviceRooted() intercepted → false");
        return false;
    };

    // Hook overloaded method (specify signature)
    RootChecker.checkRoot.overload("java.lang.String").implementation = function(path) {
        console.log("[*] checkRoot called with path: " + path);
        return false;
    };
});
```

```javascript
// Hook Java method: SSL pinning bypass (OkHttp3)
Java.perform(function() {
    var CertificatePinner = Java.use("okhttp3.CertificatePinner");
    CertificatePinner.check.overload(
        "java.lang.String", "java.util.List"
    ).implementation = function(hostname, peerCertificates) {
        console.log("[*] SSL pin check bypassed for: " + hostname);
        return; // no-op, skip certificate validation
    };

    // Also bypass X509TrustManager for custom implementations
    var X509TrustManager = Java.use("javax.net.ssl.X509TrustManager");
    var TrustAllCerts = Java.registerClass({
        name: "com.frida.TrustAllCerts",
        implements: [X509TrustManager],
        methods: {
            checkClientTrusted: function() {},
            checkServerTrusted: function() {},
            getAcceptedIssuers: function() { return []; }
        }
    });
});
```

```javascript
// Hook Java method: intercept and modify network responses
Java.perform(function() {
    var JSONObject = Java.use("org.json.JSONObject");
    var String = Java.use("java.lang.String");

    // Intercept all JSONObject.getString() calls to find interesting data
    JSONObject.getString.implementation = function(key) {
        var value = this.getString(key);
        console.log("[*] JSONObject.getString('" + key + "') = " + value);
        return value;
    };
});
```

### Frida Native Hooks (C/C++ layer)

```javascript
// Hook native function: intercept dlopen to detect library loading
Interceptor.attach(Module.findExportByName(null, "dlopen"), {
    onEnter: function(args) {
        var path = Memory.readUtf8String(args[0]);
        if (path && path.indexOf("libnative") !== -1) {
            console.log("[*] dlopen: " + path);
        }
    },
    onLeave: function(retval) {
        // retval is the loaded library handle
    }
});

// Hook specific function in a loaded native library by offset
var libBase = Module.findBaseAddress("libnative-lib.so");
if (libBase !== null) {
    // Hook function at offset 0x1A2B4 (found via Ghidra/IDA analysis)
    Interceptor.attach(libBase.add(0x1A2B4), {
        onEnter: function(args) {
            console.log("[*] native_check() called");
            console.log("    arg0 = " + args[0].toInt32());
            console.log("    arg1 = " + Memory.readUtf8String(args[1]));
        },
        onLeave: function(retval) {
            console.log("[*] native_check() returning: " + retval.toInt32());
            retval.replace(ptr(0x1)); // force return 1 (true)
        }
    });
}
```

```javascript
// Hook native function: intercept file access for rootkit analysis
Interceptor.attach(Module.findExportByName("libc.so", "open"), {
    onEnter: function(args) {
        var path = Memory.readUtf8String(args[0]);
        if (path !== null) {
            var suspicious = [
                "/system/xbin/su", "/sbin/su", "/data/local/tmp/frida",
                "/proc/self/maps", "/proc/self/status"
            ];
            for (var i = 0; i < suspicious.length; i++) {
                if (path.indexOf(suspicious[i]) !== -1) {
                    console.log("[!] Suspicious open(): " + path);
                    // Optionally redirect: Memory.writeUtf8String(args[0], "/dev/null");
                }
            }
        }
    }
});
```

### ART Hooking Frameworks (Architecture Overview)

```text
Framework Comparison:

| Framework  | Layer      | Android Support | Mechanism                        |
|:-----------|:-----------|:----------------|:---------------------------------|
| LSPlant    | ART/Java   | 5.0 – 15+      | Direct ART method entry replace  |
| SandHook   | ART+Native | 4.4 – 11        | Inline hook + trampoline         |
| Dobby      | Native     | All (ARM/ARM64) | Inline hook at instruction level |
| Pine       | ART/Java   | 5.0 – 14        | ART method entry manipulation    |
| LSPosed    | Framework  | 8.1 – 14        | Xposed API via LSPlant backend   |

LSPlant (used by LSPosed):
  - Replaces ART method entry point
  - Handles JIT/AOT compiled methods
  - Deoptimizes methods before hooking
  - Most reliable for modern Android

SandHook:
  - Hybrid Java + Native hooking
  - Disables VM inlining before hook
  - Good for Android 4.4-11

Dobby:
  - Pure native inline hook
  - Works at instruction level (ARM/ARM64/x86)
  - Similar to Substrate/Cydia but cross-platform
  - Best for hooking .so library functions
```

```java
// SandHook example: Java method hook setup
import de.robv.android.xposed.XC_MethodHook;

public class ExampleHook {
    public static void initHooks() {
        // Disable ART inline compiler optimizations
        SandHookConfig.delayHook = false;
        SandHook.disableVMInline();
        SandHook.disableDex2oatInline();

        // Register hook class
        SandHook.addHookClass(TargetMethodHooks.class);
    }
}
```

### Linux Memory Reading (`/proc/`)

```bash
# Find target process PID
adb shell pidof com.example.app
# Output: 12345

# View memory mappings
adb shell cat /proc/12345/maps
# Output:
# 00400000-00402000 r-xp 00000000 fe:00 1234 /system/lib64/libart.so
# 7a3b4c5000-7a3b4d0000 rw-p 00000000 00:00 0  [anon:libc_malloc]
```

```c
// C: read process memory via /proc/pid/mem (requires root)
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdint.h>

int read_process_memory(pid_t pid, uintptr_t address, void* buffer, size_t size) {
    char mem_path[64];
    snprintf(mem_path, sizeof(mem_path), "/proc/%d/mem", pid);

    int fd = open(mem_path, O_RDONLY);
    if (fd < 0) return -1;

    if (lseek(fd, (off_t)address, SEEK_SET) == (off_t)-1) {
        close(fd);
        return -1;
    }

    ssize_t bytes_read = read(fd, buffer, size);
    close(fd);
    return (int)bytes_read;
}

// Usage: read 4 bytes (int32) at known offset
int32_t player_hp;
read_process_memory(12345, 0x7a3b4c5100, &player_hp, sizeof(player_hp));
printf("Player HP: %d\n", player_hp);
```

```python
# Python: memory reader via ADB shell
import subprocess

def read_process_maps(serial: str, pid: int) -> str:
    """Read /proc/<pid>/maps to find memory regions."""
    cmd = ["adb", "-s", serial, "shell", f"cat /proc/{pid}/maps"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout

def find_base_address(maps: str, library: str) -> int:
    """Find base address of a loaded library from maps output."""
    for line in maps.strip().split("\n"):
        if library in line and "r-xp" in line:
            addr_range = line.split()[0]
            base = addr_range.split("-")[0]
            return int(base, 16)
    return 0
```

## Common Patterns
<!-- RECOMMENDED — real-world usage examples -->

```javascript
// Frida: comprehensive root/emulator detection bypass
Java.perform(function() {
    // 1. RootBeer library bypass
    var RootBeer = Java.use("com.scottyab.rootbeer.RootBeer");
    RootBeer.isRooted.implementation = function() { return false; };
    RootBeer.isRootedWithoutBusyBoxCheck.implementation = function() { return false; };

    // 2. SafetyNet bypass (basic)
    var SafetyNet = Java.use("com.google.android.gms.safetynet.SafetyNetApi");
    // Note: full SafetyNet bypass requires hardware attestation spoofing

    // 3. Emulator detection bypass
    var Build = Java.use("android.os.Build");
    Build.PRODUCT.value = "walleye";
    Build.MODEL.value = "Pixel 2";
    Build.MANUFACTURER.value = "Google";
    Build.BRAND.value = "google";
    Build.HARDWARE.value = "walleye";
    Build.FINGERPRINT.value = "google/walleye/walleye:11/RP1A.200720.009/6720564:user/release-keys";
});
```

```javascript
// Frida: enumerate loaded classes and methods (recon)
Java.perform(function() {
    Java.enumerateLoadedClasses({
        onMatch: function(className) {
            if (className.indexOf("security") !== -1 ||
                className.indexOf("root") !== -1 ||
                className.indexOf("detect") !== -1) {
                console.log("[CLASS] " + className);
            }
        },
        onComplete: function() {
            console.log("[*] Enumeration complete");
        }
    });
});
```

## Gotchas & Breaking Changes
<!-- CRITICAL — things that trip up agents and humans -->

- ⚠️ **Ethics**: All techniques here are for **authorized security research and QA only**. Unauthorized bypassing of app protections violates laws (CFAA, DMCA, GDPR) and terms of service.
- ⚠️ **Frida version matching**: `frida-server` version on device MUST exactly match `frida-tools` version on host. Mismatch causes `ProtocolError`.
- ⚠️ **Frida detection**: Many apps (banking, games) actively detect Frida via `/proc/self/maps` scanning, port scanning (27042), and library name checks. Shamiko + Frida can be detected by sophisticated anti-tamper SDKs.
- ⚠️ **Zygisk + Shamiko updates**: Both are actively developed. APIs and module formats change frequently. Pin versions in test environments.
- ⚠️ **SELinux**: Some operations require SELinux to be permissive (`setenforce 0`). Production devices should NOT have permissive SELinux.
- ⚠️ **Memory offsets**: ART internal offsets change per Android version, OEM ROM, and even security patch level. Never hardcode — use symbol resolution (Frida `Module.findExportByName()`).

## Migration
<!-- MANDATORY if not latest — checklist to upgrade to next version -->

- [ ] Add prominent ethics disclaimer at the top of file (✅ done).
- [ ] Keep Frida script examples generic — use `com.example.app` package names.
- [ ] Update Frida API calls when new major version ships (check frida.re/docs).
- [ ] Track Zygisk module format changes when Magisk updates.
- [ ] Document KernelSU as the emerging alternative to Magisk for kernel-level root.

<!--
BM25 DESIGN RULES:
- H1 = library name (root search anchor)
- H2 = feature category
- Code:prose ratio >= 70:30
- Keep 5-30KB per file
-->
