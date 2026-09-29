#!/usr/bin/env node
// scripts/generate-skills-index.mjs
// Regenerate .agent/skills/INDEX.yaml from the per-skill META.yaml files.
//
// Usage:
//   node scripts/generate-skills-index.mjs           # write INDEX.yaml
//   node scripts/generate-skills-index.mjs --check   # exit 1 if INDEX.yaml is stale
//
// Why: INDEX.yaml drifted from disk before. It claimed 106 in the header and 108
// in the footer, and core/graph-patterns + governance/context-compaction were
// missing entirely — a non-HSA agent reading the index could not route to them.
// META.yaml is the per-skill source of truth; the index is derived and must not
// be hand-edited.

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const skillsDir = path.resolve(__dirname, "..", ".agent", "skills");
const indexPath = path.join(skillsDir, "INDEX.yaml");

const checkOnly = process.argv.slice(2).includes("--check");

const CATEGORY_ORDER = [
  "core",
  "cross-cutting",
  "languages",
  "frameworks",
  "devops",
  "ai-ml",
  "governance",
  "tooling",
];

// detect: a glob is a *hint* for non-HSA agents, kept per category in the index.
// META.yaml carries triggers (keywords/intents) for HSA routing, not file globs,
// so globs stay hand-maintained here and are preserved across regeneration.
function collectSkills() {
  const byCategory = new Map();

  for (const category of CATEGORY_ORDER) {
    const categoryDir = path.join(skillsDir, category);
    if (!fs.existsSync(categoryDir)) continue;

    const entries = fs
      .readdirSync(categoryDir, { withFileTypes: true })
      .filter((e) => e.isDirectory())
      .map((e) => e.name)
      .sort();

    const skills = [];
    for (const name of entries) {
      const metaPath = path.join(categoryDir, name, "META.yaml");
      if (!fs.existsSync(metaPath)) continue;

      const meta = fs.readFileSync(metaPath, "utf-8");
      const declaredName = meta.match(/^name:\s*["']?([\w.-]+)["']?\s*$/m)?.[1];
      const declaredCategory = meta.match(/^category:\s*["']?([\w-]+)["']?\s*$/m)?.[1];

      if (declaredName && declaredName !== name) {
        console.error(`  ${name}: META.yaml name is "${declaredName}" — directory mismatch`);
        process.exit(1);
      }
      if (declaredCategory && declaredCategory !== category) {
        console.error(`  ${category}/${name}: META.yaml category is "${declaredCategory}" — directory mismatch`);
        process.exit(1);
      }

      skills.push({ name, detect: readDetect(meta) });
    }
    byCategory.set(category, skills);
  }

  return byCategory;
}

function readDetect(meta) {
  // META.yaml carries two different activation channels: `detect` is a file glob
  // for non-HSA agents, `triggers` holds the keywords and intents HSA routes on.
  // Reading only `detect` left every index entry empty, because the skills that
  // declare triggers are the ones with no `detect` block at all.
  const globs = matchYamlList(meta, "detect");
  const triggers = readTriggers(meta);
  return [...new Set([...globs, ...triggers])];
}

function matchYamlList(text, key) {
  const block = text.match(new RegExp(`^${key}:\\s*\\[([^\\]]*)\\]`, "m"));
  return block ? splitFlowList(block[1]) : [];
}

function splitFlowList(body) {
  return body
    .split(",")
    .map((s) => unquote(s))
    .filter(Boolean);
}

function unquote(value) {
  return value.trim().replace(/^["']|["']$/g, "").trim();
}

const TRIGGER_KEYS = "file_patterns|keywords|intents|triggers";

// Every META.yaml in the tree is scanned, not just the ones with a `triggers:`
// parent. Some skills nest the same three keys directly under another root, and
// 22 of them put `keywords` under a key the generator never looked at, so a
// parent-scoped scan silently returned nothing for the whole languages category.
function readTriggers(meta) {
  // META.yaml is checked out with CRLF on Windows, and an unstripped \r defeats
  // every $-anchored match below — which is how 21 skills kept reporting no
  // triggers at all despite declaring them.
  const lines = meta.split(/\r?\n/);
  const collected = [];
  let keyIndent = null;
  let flowDepth = 0;

  for (const line of lines) {
    if (/^\S/.test(line)) {
      // A top-level key closes whatever list was open, except the ones that
      // carry a multi-line flow list, whose closing bracket is also top-level.
      if (flowDepth === 0) keyIndent = null;
    }

    const key = line.match(new RegExp(`^(\\s*)(${TRIGGER_KEYS}):\\s*(.*)$`));
    if (key) {
      keyIndent = key[1].length;
      const inline = key[3].trim();
      if (inline.startsWith("[")) {
        const closing = inline.indexOf("]");
        if (closing !== -1) {
          collected.push(...splitFlowList(inline.slice(1, closing)));
          flowDepth = 0;
        } else {
          // Multi-line flow list: the items arrive on their own lines until the
          // lone "]" that closes them.
          flowDepth = 1;
        }
      } else {
        flowDepth = 0;
      }
      continue;
    }

    if (flowDepth > 0) {
      const closing = line.match(/^\s*\]\s*,?\s*$/);
      if (closing) {
        flowDepth = 0;
        keyIndent = null;
        continue;
      }
      const inlineItem = line.match(/^\s*([^-\s][^,]*?)\s*,?\s*$/);
      if (inlineItem) {
        const value = unquote(inlineItem[1]);
        if (value) collected.push(value);
      }
      continue;
    }

    // A key with nothing after its colon can still open a flow list on the next
    // line. One META.yaml writes the bracket on its own line; without this the
    // whole list was skipped and the skill indexed with zero triggers.
    if (keyIndent !== null) {
      const indent = line.length - line.trimStart().length;
      if (indent > keyIndent && line.trim() === "[") {
        flowDepth = 1;
        continue;
      }
    }

    const item = line.match(/^(\s*)-\s*(.*)$/);
    if (item && keyIndent !== null && item[1].length > keyIndent) {
      const value = unquote(item[2]);
      if (value) collected.push(value);
    }
  }

  return collected;
}

function preserveExistingDetect(byCategory) {
  if (!fs.existsSync(indexPath)) return;

  const existing = fs.readFileSync(indexPath, "utf-8");
  const order = new Map();

  for (const line of existing.split("\n")) {
    const match = line.match(/^\s*([\w-]+):\s*\{ path: "([^"]+)", detect: (\[[^\]]*\]) \}/);
    if (!match) continue;

    const [, key, skillPath, detectRaw] = match;
    const relPath = skillPath.replace(/^.*\//, "");
    const category = skillPath.split("/")[0];

    const skills = byCategory.get(category);
    if (!skills) continue;
    const found = skills.find((s) => s.name === key || s.name === relPath);
    if (!found) continue;

    if (found.detect.length === 0) {
      found.detect = detectRaw
        .replace(/^\[|\]$/g, "")
        .split(",")
        .map((s) => s.trim().replace(/^["']|["']$/g, ""))
        .filter(Boolean);
    }

    if (!order.has(category)) order.set(category, []);
    order.get(category).push(found.name);
  }

  // The index is hand-curated by insertion/priority, not alphabetical. Keep the
  // existing order so regeneration does not reshuffle the whole file; new skills
  // land at the end of their category, already sorted from collectSkills().
  for (const [category, skills] of byCategory) {
    const seq = order.get(category);
    if (!seq) continue;
    const rank = new Map(seq.map((name, i) => [name, i]));
    skills.sort((a, b) => (rank.get(a.name) ?? Infinity) - (rank.get(b.name) ?? Infinity));
  }
}

function render(byCategory) {
  const total = [...byCategory.values()].reduce((sum, s) => sum + s.length, 0);
  const lines = [
    "# Skills Routing Index — Universal Discovery",
    "# GENERATED by scripts/generate-skills-index.mjs — do not hand-edit",
    `# ${total} skills across ${byCategory.size} categories`,
    "#",
    "# Usage (non-HSA agents):",
    "#   1. Read this file → find skill by name → get path + detect patterns",
    "#   2. Read .agent/skills/{path}/SKILL.md",
    "#   Total: 2 tool calls",
    "",
    "routing:",
  ];

  for (const category of CATEGORY_ORDER) {
    const skills = byCategory.get(category);
    if (!skills || skills.length === 0) continue;

    const width = Math.max(...skills.map((s) => s.name.length));
    lines.push(`  # --- ${category} (${skills.length}) ---`);
    for (const skill of skills) {
      const key = skill.name.padEnd(width + 1);
      const detect = skill.detect.length > 0 ? `["${skill.detect.join('", "')}"]` : "[]";
      lines.push(`  ${key}: { path: "${category}/${skill.name}", detect: ${detect} }`);
    }
    lines.push("");
  }

  lines.push("# Category summary (for human reference only — agent uses routing above)");
  lines.push(
    `# ${[...byCategory.entries()].map(([c, s]) => `${c}: ${s.length}`).join(" | ")} | TOTAL: ${total}`,
  );
  lines.push("");

  return lines.join("\n");
}

const byCategory = collectSkills();
preserveExistingDetect(byCategory);
const generated = render(byCategory);

if (checkOnly) {
  const current = fs.existsSync(indexPath) ? fs.readFileSync(indexPath, "utf-8") : "";
  if (current !== generated) {
    console.error("Drift detected. Run: node scripts/generate-skills-index.mjs");
    process.exit(1);
  }
  console.log("INDEX.yaml up-to-date");
} else {
  fs.writeFileSync(indexPath, generated);
  const total = [...byCategory.values()].reduce((sum, s) => sum + s.length, 0);
  console.log(`INDEX.yaml written — ${total} skills across ${byCategory.size} categories`);
}
