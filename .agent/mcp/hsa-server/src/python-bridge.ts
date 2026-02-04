/**
 * Python Bridge for HSA (Unified Module)
 * Executes Python scripts and returns results
 */

import { spawn } from "child_process";
import type { HSAConfig } from "./config.js";

export async function callPython(
  script: string,
  config: HSAConfig
): Promise<string> {
  return new Promise((resolve, reject) => {
    const python = spawn(config.pythonPath, ["-c", script], {
      cwd: config.projectPath,
      env: {
        ...process.env,
        PYTHONIOENCODING: "utf-8",
      },
    });

    let stdout = "";
    let stderr = "";

    python.stdout.on("data", (data) => {
      stdout += data.toString();
    });

    python.stderr.on("data", (data) => {
      stderr += data.toString();
    });

    python.on("close", (code) => {
      if (code === 0) {
        resolve(stdout.trim());
      } else {
        reject(new Error(`Python error (code ${code}): ${stderr || stdout}`));
      }
    });

    python.on("error", (error) => {
      reject(new Error(`Failed to spawn Python: ${error.message}`));
    });

    // Timeout after 30 seconds
    setTimeout(() => {
      python.kill();
      reject(new Error("Python script timeout (30s)"));
    }, 30000);
  });
}

/**
 * Check if HSA Python modules are available
 */
export async function checkHSAAvailable(config: HSAConfig): Promise<boolean> {
  const script = `
import sys
sys.path.insert(0, '${config.scriptsPath}')
try:
    from hsa import HSAEngine
    print('OK')
except ImportError as e:
    print(f'MISSING: {e}')
`;

  try {
    const result = await callPython(script, config);
    return result === "OK";
  } catch {
    return false;
  }
}

/**
 * Get HSA version
 */
export async function getHSAVersion(config: HSAConfig): Promise<string> {
  const script = `
import sys
sys.path.insert(0, '${config.scriptsPath}')
from hsa import __version__
print(__version__)
`;

  try {
    return await callPython(script, config);
  } catch {
    return "unknown";
  }
}
