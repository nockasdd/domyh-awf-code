/**
 * HSA MCP Server Configuration
 * Unified configuration for HSA module
 */

import { resolve, join } from "path";
import { existsSync } from "fs";

export interface HSAConfig {
  projectPath: string;
  scriptsPath: string;
  pythonPath: string;
  cacheDir: string;
}

/**
 * Get configuration from environment and defaults
 */
export function getConfig(): HSAConfig {
  // Project path from env or current directory
  const projectPath = process.env.HSA_PROJECT_PATH || process.cwd();
  
  // Scripts path - look for .agent/scripts/hsa (unified module)
  let scriptsPath = process.env.HSA_SCRIPTS_PATH || "";
  
  if (!scriptsPath) {
    // Try project-local first
    const localScripts = join(projectPath, ".agent", "scripts");
    if (existsSync(join(localScripts, "hsa"))) {
      scriptsPath = localScripts;
    } else {
      // Try global DOMYH installation
      const globalScripts = join(
        process.env.DOMYH_HOME || join(process.env.HOME || process.env.USERPROFILE || "", ".domyh"),
        ".agent",
        "scripts"
      );
      if (existsSync(join(globalScripts, "hsa"))) {
        scriptsPath = globalScripts;
      } else {
        // Fallback to project scripts (will error if not found)
        scriptsPath = join(projectPath, ".agent", "scripts");
      }
    }
  }
  
  // Python path from env or default
  const pythonPath = process.env.HSA_PYTHON_PATH || process.env.PYTHON_PATH || "python";
  
  // Cache directory
  const cacheDir = process.env.HSA_CACHE_DIR || join(projectPath, ".hsa_cache");

  return {
    projectPath: resolve(projectPath),
    scriptsPath: resolve(scriptsPath),
    pythonPath,
    cacheDir: resolve(cacheDir),
  };
}

/**
 * Validate configuration
 */
export function validateConfig(config: HSAConfig): { valid: boolean; errors: string[] } {
  const errors: string[] = [];
  
  if (!existsSync(config.projectPath)) {
    errors.push(`Project path not found: ${config.projectPath}`);
  }
  
  const hsaModulePath = join(config.scriptsPath, "hsa");
  if (!existsSync(hsaModulePath)) {
    errors.push(`HSA modules not found at: ${hsaModulePath}`);
  }
  
  return {
    valid: errors.length === 0,
    errors,
  };
}
