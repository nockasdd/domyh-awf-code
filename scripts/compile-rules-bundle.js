#!/usr/bin/env node
// scripts/compile-rules-bundle.js
// Compile rule files into pre-built bundles for minimal/standard/full profiles.
// Output: domyh-awf/.agent/rules/dist/{minimal,standard,full}.md
//
// Usage: node scripts/compile-rules-bundle.js [--check]
//   --check : Verify bundles up-to-date vs sources, exit 1 if drift detected.
//
// Why: minimal profile previously installed empty modules folder (whitelist
// referenced non-existent files). Compiled bundles guarantee minimal users
// receive condensed rules in a single ~50-line file.

import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(__dirname, "..");
const rulesDir = path.join(repoRoot, ".agent", "rules");
const distDir = path.join(rulesDir, "dist");

const args = process.argv.slice(2);
const checkOnly = args.includes("--check");

// Profile definitions — must match install.ts PROFILES
const PROFILES = {
  minimal: {
    description: "Minimal bundle — Tier 0 + 3 essential modules (~2K tokens)",
    sources: [
      "AGENT_RULES.md",
      "modules/behavioral-patterns.yaml",
      "modules/terminal-safety.yaml",
      "modules/progressive-escalation.yaml",
    ],
    truncate: 8000, // chars per source max
  },
  standard: {
    description: "Standard bundle — Tier 0-2 + all 5 modules (~5K tokens)",
    sources: [
      "AGENT_RULES.md",
      "prompt-injection-guard.md",
      "validation-framework.md",
      "modules/behavioral-patterns.yaml",
      "modules/complexity-scoring.yaml",
      "modules/progressive-escalation.yaml",
      "modules/terminal-safety.yaml",
      "modules/git-workflow.yaml",
    ],
    truncate: 12000,
  },
  full: {
    description: "Full bundle — everything including domain rules (~10K tokens)",
    sources: [
      "AGENT_RULES.md",
      "prompt-injection-guard.md",
      "validation-framework.md",
      "modules/behavioral-patterns.yaml",
      "modules/complexity-scoring.yaml",
      "modules/progressive-escalation.yaml",
      "modules/terminal-safety.yaml",
      "modules/git-workflow.yaml",
      "domain/orchestration-comm.yaml",
      "domain/orchestration-deleg.yaml",
    ],
    truncate: 20000,
  },
};

function readSource(rel) {
  const abs = path.join(rulesDir, rel);
  if (!fs.existsSync(abs)) {
    console.error(`  Missing source: ${rel}`);
    return null;
  }
  return fs.readFileSync(abs, "utf-8");
}

function compileBundle(name, profile) {
  const parts = [];
  parts.push(`# DOMYH Rules Bundle — ${name}`);
  parts.push(`> ${profile.description}`);
  parts.push(`> Generated: ${new Date().toISOString()} — DO NOT EDIT (regenerate via compile-rules-bundle.js)`);
  parts.push("");

  const missingSources = [];
  for (const src of profile.sources) {
    const content = readSource(src);
    if (content === null) {
      missingSources.push(src);
      continue;
    }
    const truncated = content.length > profile.truncate
      ? content.slice(0, profile.truncate) + `\n\n[... truncated at ${profile.truncate} chars ...]`
      : content;
    parts.push(`---`);
    parts.push(`## SOURCE: ${src}`);
    parts.push("");
    parts.push(truncated);
    parts.push("");
  }

  if (missingSources.length > 0) {
    console.error(`  ${name}: ${missingSources.length} missing source(s) — bundle incomplete`);
    return { content: null, missingSources };
  }

  return { content: parts.join("\n"), missingSources: [] };
}

function sha256(content) {
  return crypto.createHash("sha256").update(content, "utf-8").digest("hex").slice(0, 16);
}

let driftDetected = false;
let buildFailed = false;

if (!fs.existsSync(distDir) && !checkOnly) {
  fs.mkdirSync(distDir, { recursive: true });
}

const manifest = {
  generated: new Date().toISOString(),
  bundles: {},
};

for (const [name, profile] of Object.entries(PROFILES)) {
  const result = compileBundle(name, profile);
  if (result.content === null) {
    buildFailed = true;
    continue;
  }

  const bundlePath = path.join(distDir, `${name}.md`);
  const newHash = sha256(result.content);
  manifest.bundles[name] = {
    path: `dist/${name}.md`,
    sha256: newHash,
    size: result.content.length,
    sources: profile.sources.length,
  };

  if (checkOnly) {
    if (!fs.existsSync(bundlePath)) {
      console.error(`  ${name}: bundle missing at ${bundlePath}`);
      driftDetected = true;
      continue;
    }
    const existing = fs.readFileSync(bundlePath, "utf-8");
    const existingHash = sha256(existing.replace(/^> Generated: .*\n/m, "")); // ignore timestamp line
    const newHashNoTime = sha256(result.content.replace(/^> Generated: .*\n/m, ""));
    if (existingHash !== newHashNoTime) {
      console.error(`  ${name}: DRIFT detected (hash mismatch)`);
      driftDetected = true;
    } else {
      console.log(`  ${name}: up-to-date (${result.content.length} chars)`);
    }
  } else {
    fs.writeFileSync(bundlePath, result.content);
    console.log(`  ${name}: written (${result.content.length} chars, sha256: ${newHash})`);
  }
}

if (!checkOnly && !buildFailed) {
  fs.writeFileSync(path.join(distDir, "manifest.json"), JSON.stringify(manifest, null, 2));
  console.log(`  manifest.json written`);
}

if (driftDetected) {
  console.error("\nDrift detected. Run: node scripts/compile-rules-bundle.js");
  process.exit(1);
}
if (buildFailed) {
  console.error("\nBuild failed: missing sources.");
  process.exit(1);
}

console.log(`\n${checkOnly ? "Check" : "Compile"} complete.`);
