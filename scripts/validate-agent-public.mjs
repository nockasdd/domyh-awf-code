#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const AGENT_DIR = path.join(ROOT, ".agent");

const errors = [];
const warnings = [];

function toPosix(filePath) {
  return filePath.replace(/\\/g, "/");
}

function relativeToAgent(filePath) {
  return toPosix(path.relative(AGENT_DIR, filePath));
}

function addError(message) {
  errors.push(message);
}

function addWarning(message) {
  warnings.push(message);
}

function fileExists(relativePath, baseDir = AGENT_DIR) {
  return fs.existsSync(path.join(baseDir, relativePath));
}

function readText(filePath) {
  return fs.readFileSync(filePath, "utf-8");
}

function walkFiles(dir, collector = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      walkFiles(fullPath, collector);
    } else if (entry.isFile()) {
      collector.push(fullPath);
    }
  }
  return collector;
}

function isIgnoredPublicFile(relativePath) {
  return relativePath.startsWith("private/")
    || relativePath.startsWith("memory/")
    || relativePath.startsWith("hsa/")
    || relativePath === "core/session_cache.json";
}

function parseYamlBlockList(content, key) {
  const lines = content.split(/\r?\n/);
  const items = [];
  let collecting = false;
  let baseIndent = 0;

  for (const line of lines) {
    const indent = line.match(/^\s*/)?.[0].length ?? 0;

    if (!collecting) {
      const match = line.match(new RegExp(`^(\\s*)${key}:\\s*$`));
      if (!match) continue;
      collecting = true;
      baseIndent = match[1].length;
      continue;
    }

    if (!line.trim()) continue;
    if (indent <= baseIndent) break;

    const itemMatch = line.match(/^\s*-\s+(.+?)\s*$/);
    if (!itemMatch) continue;
    const item = itemMatch[1].split("#")[0].trim().replace(/^["']|["']$/g, "");
    if (item.length > 0) items.push(item);
  }

  return items;
}

function parseYamlScalar(content, key) {
  const match = content.match(new RegExp(`^\\s*${key}:\\s*["']?([^"'#\\n]+)["']?`, "m"));
  return match?.[1]?.trim();
}

function collectManifestPaths(content) {
  const results = [];
  const lines = content.split(/\r?\n/);
  const pathKeys = new Set(["rules_dir", "rules_index", "context_snapshot", "memory_paths", "reference_dir", "file"]);

  for (const line of lines) {
    const match = line.match(/^\s*([a-zA-Z_]+):\s*(.+?)\s*$/);
    if (!match) continue;
    const [, key, rawValue] = match;
    if (!pathKeys.has(key)) continue;

    const value = rawValue.split("#")[0].trim().replace(/^["']|["']$/g, "");
    if (value.length === 0 || value.includes("file:line")) continue;
    results.push(value);
  }

  return results;
}

function validateJsonFiles() {
  const jsonFiles = walkFiles(AGENT_DIR).filter((filePath) => {
    if (!filePath.endsWith(".json")) return false;
    return !isIgnoredPublicFile(relativeToAgent(filePath));
  });

  for (const jsonFile of jsonFiles) {
    try {
      const parsed = JSON.parse(readText(jsonFile));
      const relativePath = relativeToAgent(jsonFile);
      if (relativePath.startsWith("ide/")) {
        const configFiles = parsed.configFiles ?? parsed.config_files;
        if (!parsed.name || (!configFiles && !parsed.mcp_servers)) {
          addError(`${relativePath}: missing required IDE template fields`);
        }
      }
    } catch (error) {
      addError(`${relativeToAgent(jsonFile)}: invalid JSON (${error.message})`);
    }
  }
}

function validateManifestReferences() {
  const manifestPath = path.join(AGENT_DIR, "manifest.yaml");
  const manifestContent = readText(manifestPath);
  const referencedPaths = collectManifestPaths(manifestContent);
  const workflowFiles = new Set(
    fs.readdirSync(path.join(AGENT_DIR, "workflows"))
      .filter((name) => name.endsWith(".md"))
      .map((name) => `workflows/${name}`),
  );
  const referencedWorkflowFiles = new Set();

  for (const referencedPath of referencedPaths) {
    if (!fileExists(referencedPath)) {
      addError(`manifest.yaml references missing path: ${referencedPath}`);
      continue;
    }
    if (referencedPath.startsWith("workflows/")) {
      referencedWorkflowFiles.add(referencedPath);
    }
  }

  for (const workflowFile of workflowFiles) {
    if (!referencedWorkflowFiles.has(workflowFile)) {
      addWarning(`workflow not referenced from manifest.yaml: ${workflowFile}`);
    }
  }
}

function validateSkillDirectories() {
  const skillsRoot = path.join(AGENT_DIR, "skills");
  const categoryDirs = fs.readdirSync(skillsRoot, { withFileTypes: true }).filter((entry) => entry.isDirectory());

  for (const categoryDir of categoryDirs) {
    const categoryPath = path.join(skillsRoot, categoryDir.name);
    const skillDirs = fs.readdirSync(categoryPath, { withFileTypes: true }).filter((entry) => entry.isDirectory());

    for (const skillDir of skillDirs) {
      const skillPath = path.join(categoryPath, skillDir.name);
      const metaPath = path.join(skillPath, "META.yaml");
      const skillDocPath = path.join(skillPath, "SKILL.md");
      const relativeSkillPath = relativeToAgent(skillPath);

      if (!fs.existsSync(metaPath)) {
        addError(`${relativeSkillPath}: missing META.yaml`);
        continue;
      }
      if (!fs.existsSync(skillDocPath)) {
        addError(`${relativeSkillPath}: missing SKILL.md`);
      }

      const metaContent = readText(metaPath);
      const metaName = parseYamlScalar(metaContent, "name");
      const metaCategory = parseYamlScalar(metaContent, "category");
      if (!metaName) addError(`${relativeToAgent(metaPath)}: missing skill name`);
      if (!metaCategory) addError(`${relativeToAgent(metaPath)}: missing category`);

      const dataFiles = parseYamlBlockList(metaContent, "data_files");
      for (const dataFile of dataFiles) {
        const candidatePath = dataFile.includes("/") ? dataFile : `data/${dataFile}`;
        if (!fileExists(candidatePath, skillPath)) {
          addError(`${relativeToAgent(metaPath)}: missing data file ${dataFile}`);
        }
      }
    }
  }
}

function validateCriticalPaths() {
  const versionPath = path.join(AGENT_DIR, "core", "VERSION.yaml");
  const versionContent = readText(versionPath);
  const version = versionContent.match(/^\s*version:\s*"(\d+\.\d+\.\d+)"/m)?.[1];
  if (!version) {
    addError("core/VERSION.yaml: could not extract system version");
  }

  const memoryPathsContent = readText(path.join(AGENT_DIR, "core", "MEMORY_PATHS.yaml"));
  const criticalPaths = [
    parseYamlScalar(memoryPathsContent, "session_cache"),
    parseYamlScalar(memoryPathsContent, "notes"),
    parseYamlScalar(memoryPathsContent, "context_snapshot"),
    parseYamlScalar(memoryPathsContent, "project_state"),
    parseYamlScalar(memoryPathsContent, "audit_summary"),
  ].filter(Boolean);

  for (const criticalPath of criticalPaths) {
    if (!fileExists(criticalPath)) {
      addError(`core/MEMORY_PATHS.yaml references missing path: ${criticalPath}`);
    }
  }

  if (version) {
    const ideCompatibility = readText(path.join(ROOT, "IDE_COMPATIBILITY.md"));
    if (!ideCompatibility.includes(version)) {
      addError(`IDE_COMPATIBILITY.md does not contain SSoT version ${version}`);
    }
  }
}

function validatePersonas() {
  const personasDir = path.join(AGENT_DIR, "personas");
  const schemaPath = path.join(personasDir, "persona.schema.yaml");
  if (!fs.existsSync(schemaPath)) {
    addError("personas/persona.schema.yaml is missing");
  }

  const personaFiles = fs.readdirSync(personasDir)
    .filter((name) => name.endsWith(".md") && name !== "README.md");

  if (personaFiles.length === 0) {
    addError("personas/: no persona markdown files found");
  }
}

function main() {
  if (!fs.existsSync(AGENT_DIR)) {
    console.error("❌ .agent/ not found");
    process.exit(1);
  }

  validateJsonFiles();
  validateManifestReferences();
  validateSkillDirectories();
  validateCriticalPaths();
  validatePersonas();

  if (warnings.length > 0) {
    console.log("⚠️ Warnings:");
    for (const warning of warnings) {
      console.log(`  - ${warning}`);
    }
  }

  if (errors.length > 0) {
    console.error("❌ Public agent validation failed:");
    for (const error of errors) {
      console.error(`  - ${error}`);
    }
    process.exit(1);
  }

  console.log("✅ Public agent content validated successfully");
}

main();
