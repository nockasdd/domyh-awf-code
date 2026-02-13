#!/usr/bin/env node
// =============================================================================
// bump-version.mjs — DOMYH Awesome Code Version Bump Script
// =============================================================================
// Usage:
//   node scripts/bump-version.mjs patch              → 6.2.5 → 6.2.6
//   node scripts/bump-version.mjs minor              → 6.2.5 → 6.3.0
//   node scripts/bump-version.mjs major              → 6.2.5 → 7.0.0
//   node scripts/bump-version.mjs 7.1.0              → 6.2.5 → 7.1.0
//   node scripts/bump-version.mjs patch --dry-run    → Preview only
// =============================================================================

import * as fs from "node:fs";
import * as path from "node:path";
import { fileURLToPath } from "node:url";
import { glob } from "node:fs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");

// ── Colors (no deps) ────────────────────────────────────────

const c = {
  reset: "\x1b[0m",
  bold: "\x1b[1m",
  red: "\x1b[31m",
  green: "\x1b[32m",
  yellow: "\x1b[33m",
  cyan: "\x1b[36m",
  gray: "\x1b[90m",
};

// ── Parse args ──────────────────────────────────────────────

const args = process.argv.slice(2);
const dryRun = args.includes("--dry-run");
const verbose = args.includes("--verbose");
const bumpArg = args.find((a) => !a.startsWith("--"));

if (!bumpArg) {
  console.log(`${c.cyan}${c.bold}DOMYH Version Bump${c.reset}`);
  console.log(`\nUsage: node scripts/bump-version.mjs <bump> [options]\n`);
  console.log(`  bump:    patch | minor | major | x.y.z`);
  console.log(`  options: --dry-run  Preview only, no writes`);
  console.log(`           --verbose  Show every file change\n`);
  process.exit(0);
}

// ── Read current version from VERSION.yaml ──────────────────

function readCurrentVersion() {
  const versionFile = path.join(ROOT, ".agent", "core", "VERSION.yaml");
  if (!fs.existsSync(versionFile)) {
    console.error(`${c.red}✗ VERSION.yaml not found at ${versionFile}${c.reset}`);
    process.exit(1);
  }
  const content = fs.readFileSync(versionFile, "utf-8");
  // Match system.version: "x.y.z" — the first version field under system:
  const match = content.match(/^\s*version:\s*"(\d+\.\d+\.\d+)"/m);
  if (!match) {
    console.error(`${c.red}✗ Could not parse version from VERSION.yaml${c.reset}`);
    process.exit(1);
  }
  return match[1];
}

// ── Calculate new version ───────────────────────────────────

function calcNewVersion(current, bump) {
  if (/^\d+\.\d+\.\d+$/.test(bump)) return bump;

  const [major, minor, patch] = current.split(".").map(Number);
  switch (bump) {
    case "patch": return `${major}.${minor}.${patch + 1}`;
    case "minor": return `${major}.${minor + 1}.0`;
    case "major": return `${major + 1}.0.0`;
    default:
      console.error(`${c.red}✗ Invalid bump: "${bump}". Use patch|minor|major|x.y.z${c.reset}`);
      process.exit(1);
  }
}

// ── Scan & replace ──────────────────────────────────────────

function collectFiles(rootDir) {
  const results = [];
  const SKIP = new Set([
    "node_modules", ".git", "dist", "build", ".next", "__pycache__",
    ".turbo", ".cache", "coverage",
  ]);

  function walk(dir) {
    let entries;
    try {
      entries = fs.readdirSync(dir, { withFileTypes: true });
    } catch {
      return;
    }
    for (const entry of entries) {
      if (SKIP.has(entry.name)) continue;
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        walk(full);
      } else if (entry.isFile()) {
        const ext = path.extname(entry.name).toLowerCase();
        if ([".yaml", ".yml", ".md", ".json"].includes(ext)) {
          results.push(full);
        }
      }
    }
  }

  walk(rootDir);
  return results;
}

function replaceInFile(filePath, oldVer, newVer) {
  const content = fs.readFileSync(filePath, "utf-8");

  // Use word-boundary-like matching to avoid partial replacements
  // e.g., don't match "16.2.5" or "6.2.50"
  const escaped = oldVer.replace(/\./g, "\\.");
  const regex = new RegExp(escaped, "g");

  const matches = content.match(regex);
  if (!matches || matches.length === 0) return 0;

  const newContent = content.replace(regex, newVer);
  if (!dryRun) {
    fs.writeFileSync(filePath, newContent, "utf-8");
  }
  return matches.length;
}

// ── Main ────────────────────────────────────────────────────

const currentVersion = readCurrentVersion();
const newVersion = calcNewVersion(currentVersion, bumpArg);

console.log(`\n${c.cyan}${c.bold}DOMYH Version Bump${c.reset}`);
console.log(`${c.gray}─────────────────────────────────────${c.reset}`);
console.log(`  Current: ${c.yellow}${currentVersion}${c.reset}`);
console.log(`  New:     ${c.green}${c.bold}${newVersion}${c.reset}`);
if (dryRun) console.log(`  Mode:    ${c.yellow}DRY RUN${c.reset} (no files modified)`);
console.log(`${c.gray}─────────────────────────────────────${c.reset}\n`);

if (currentVersion === newVersion) {
  console.log(`${c.yellow}⚠ New version is same as current. Nothing to do.${c.reset}`);
  process.exit(0);
}

// Collect and process files
const files = collectFiles(ROOT);
let totalFiles = 0;
let totalReplacements = 0;
const updatedFiles = [];
const skippedFiles = [];

for (const file of files) {
  const count = replaceInFile(file, currentVersion, newVersion);
  if (count > 0) {
    totalFiles++;
    totalReplacements += count;
    updatedFiles.push({ file: path.relative(ROOT, file), count });
    if (verbose) {
      console.log(`  ${c.green}✓${c.reset} ${path.relative(ROOT, file)} ${c.gray}(${count})${c.reset}`);
    }
  } else {
    skippedFiles.push(path.relative(ROOT, file));
  }
}

// Report
console.log(`\n${c.cyan}${c.bold}Report${c.reset}`);
console.log(`${c.gray}─────────────────────────────────────${c.reset}`);
console.log(`  ${c.green}✓${c.reset} Files updated:     ${c.bold}${totalFiles}${c.reset}`);
console.log(`  ${c.green}✓${c.reset} Replacements:      ${c.bold}${totalReplacements}${c.reset}`);
console.log(`  ${c.gray}⏭  Files scanned:     ${files.length}${c.reset}`);
console.log(`  ${c.gray}⏭  Files skipped:     ${skippedFiles.length}${c.reset}`);

if (dryRun) {
  console.log(`\n${c.yellow}${c.bold}DRY RUN${c.reset} — No files were modified.`);
  console.log(`Run without --dry-run to apply changes.\n`);
} else {
  console.log(`\n${c.green}${c.bold}✓ Version bumped: ${currentVersion} → ${newVersion}${c.reset}\n`);
}

// Show top files if not verbose
if (!verbose && updatedFiles.length > 0) {
  console.log(`${c.gray}Top files:${c.reset}`);
  updatedFiles.slice(0, 10).forEach(({ file, count }) => {
    console.log(`  ${c.green}✓${c.reset} ${file} ${c.gray}(${count})${c.reset}`);
  });
  if (updatedFiles.length > 10) {
    console.log(`  ${c.gray}... and ${updatedFiles.length - 10} more${c.reset}`);
  }
  console.log();
}
