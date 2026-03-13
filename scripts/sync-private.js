#!/usr/bin/env node
// scripts/sync-private.js
// Sync private skills from domyh-awf/.agent/private → all IDE global directories
// Usage: node scripts/sync-private.js [--dry-run] [--verbose]

import fs from "node:fs";
import path from "node:path";
import { homedir } from "node:os";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const HOME = homedir();
const APPDATA = process.env.APPDATA || HOME;

// ═══════════════════════════════════════════════════════════════════════
// Source: domyh-awf/.agent/private/
// ═══════════════════════════════════════════════════════════════════════
const sourcePrivate = path.resolve(__dirname, "..", ".agent", "private");

// ═══════════════════════════════════════════════════════════════════════
// IDE Global Targets (mirrored from nock-cli IDE_REGISTRY)
// Only IDEs with globalPath + skills support
// ═══════════════════════════════════════════════════════════════════════
const IDE_TARGETS = [
  // Tier 0
  { name: "Codex CLI", globalBase: path.join(HOME, ".codex"), agentDir: ".agents" },

  // Tier 1
  { name: "Cursor", globalBase: path.join(HOME, ".cursor", "rules"), agentDir: ".agent" },
  { name: "Claude Code", globalBase: path.join(HOME, ".claude"), agentDir: ".agent" },
  { name: "Gemini CLI", globalBase: path.join(HOME, ".gemini"), agentDir: ".agent" },
  { name: "VS Code + Copilot", globalBase: path.join(APPDATA, "Code - Insiders", "User"), agentDir: ".agent" },
  { name: "Windsurf", globalBase: path.join(HOME, ".codeium", "windsurf", "memories"), agentDir: ".agent" },

  // Tier 2
  { name: "Cline", globalBase: path.join(HOME, "Documents", "Cline", "Rules"), agentDir: ".agent" },
  { name: "Continue.dev", globalBase: path.join(HOME, ".continue", "rules"), agentDir: ".agent" },
  { name: "Roo Code", globalBase: path.join(HOME, ".roo"), agentDir: ".agent" },
  { name: "JetBrains AI", globalBase: path.join(HOME, ".junie"), agentDir: ".agent" },
  { name: "Amazon Q", globalBase: path.join(HOME, ".aws", "amazonq"), agentDir: ".agent" },
  { name: "Kiro", globalBase: path.join(HOME, ".kiro"), agentDir: ".agent" },
  { name: "Tabnine", globalBase: path.join(HOME, ".tabnine"), agentDir: ".agent" },

  // Tier 3
  { name: "Antigravity", globalBase: path.join(HOME, ".gemini", "antigravity"), agentDir: ".agent" },
  { name: "OpenCode", globalBase: path.join(HOME, ".config", "opencode"), agentDir: ".agent" },
  { name: "Augment Code", globalBase: path.join(HOME, ".augment"), agentDir: ".agent" },
];

// ═══════════════════════════════════════════════════════════════════════
// Helpers
// ═══════════════════════════════════════════════════════════════════════
function countFiles(dir) {
  if (!fs.existsSync(dir)) return 0;
  let count = 0;
  for (const item of fs.readdirSync(dir)) {
    const full = path.join(dir, item);
    try {
      const stat = fs.lstatSync(full);
      count += stat.isDirectory() ? countFiles(full) : 1;
    } catch { /* skip */ }
  }
  return count;
}

function copyRecursive(src, dest) {
  fs.cpSync(src, dest, {
    recursive: true,
    force: true,
    filter: (source) => {
      const basename = path.basename(source);
      // Skip _template (not a real skill)
      if (basename === "_template") return false;
      // Skip .git
      if (basename === ".git") return false;
      return true;
    },
  });
}

// ═══════════════════════════════════════════════════════════════════════
// Main
// ═══════════════════════════════════════════════════════════════════════
const args = process.argv.slice(2);
const dryRun = args.includes("--dry-run");
const verbose = args.includes("--verbose") || args.includes("-v");

console.log("🔒 Syncing Private Skills to IDE Global Directories");
console.log(`   Source: ${sourcePrivate}`);
console.log();

// Validate source
if (!fs.existsSync(sourcePrivate)) {
  console.error(`❌ Source not found: ${sourcePrivate}`);
  process.exit(1);
}

// Read _index.yaml to show skill count
const indexPath = path.join(sourcePrivate, "_index.yaml");
let skillCount = 0;
if (fs.existsSync(indexPath)) {
  const content = fs.readFileSync(indexPath, "utf-8");
  const match = content.match(/count:\s*(\d+)/);
  skillCount = match ? parseInt(match[1], 10) : 0;
}

// List skills
const skills = fs.readdirSync(sourcePrivate)
  .filter(f => {
    if (f.startsWith("_") || f === "README.md") return false;
    const full = path.join(sourcePrivate, f);
    return fs.existsSync(full) && fs.lstatSync(full).isDirectory();
  });

console.log(`   Skills (${skills.length}): ${skills.join(", ")}`);
console.log(`   Priority: -1 (highest — overrides public skills)`);
if (dryRun) console.log("   🔍 DRY RUN — no files will be written");
console.log();

let synced = 0;
let skipped = 0;

for (const target of IDE_TARGETS) {
  const targetDir = path.join(target.globalBase, target.agentDir, "private");

  // Only sync if parent global dir exists (IDE is installed)
  if (!fs.existsSync(target.globalBase)) {
    if (verbose) {
      console.log(`   ⏭️  ${target.name.padEnd(20)} — not installed`);
    }
    skipped++;
    continue;
  }

  if (dryRun) {
    console.log(`   📋 ${target.name.padEnd(20)} → ${targetDir}`);
    synced++;
    continue;
  }

  try {
    // Ensure parent .agent dir exists
    const agentDir = path.join(target.globalBase, target.agentDir);
    fs.mkdirSync(agentDir, { recursive: true });

    // Copy private skills
    copyRecursive(sourcePrivate, targetDir);
    const fileCount = countFiles(targetDir);
    console.log(`   ✅ ${target.name.padEnd(20)} → ${fileCount} files`);
    synced++;
  } catch (err) {
    console.log(`   ❌ ${target.name.padEnd(20)} — ${err.message}`);
  }
}

console.log();
console.log(`✅ Synced: ${synced} IDE(s), Skipped: ${skipped} (not installed)`);
if (dryRun) console.log("   Run without --dry-run to apply changes.");
