import { writeFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';

const ROOT_DIR = process.cwd();
const CONFIGS_DIR = join(ROOT_DIR, 'configs');

const LEAN_TEMPLATE = `# DOMYH Awesome Code — NockDev

> {{LANGUAGE_INSTRUCTION}}

## ⚡ Core Principles & Execution Speed
1. **Think Before Coding**: Surface assumptions, search before creating, no speculative features.
2. **Parallel Tool Batching (Anti-Fragmentation)**: MANDATORY: Always execute independent file reads (\`view_file\`), symbol searches (\`hsa_search\`), and flow traces (\`hsa_trace_flow\`) in PARALLEL in a SINGLE turn. Never split independent lookups into sequential 1-tool turns.
3. **Cohesive Action Blocks**: Complete full logical units in 1-2 turns (e.g. [Read Target + Trace Callers in Turn 1] ➔ [Edit File + Verify Syntax in Turn 2]).
4. **Surgical Changes**: Touch only what is requested, match existing style EXACTLY.
5. **Verify Before Done**: Show test evidence, not assertions.
6. **Subagent Delegation**: For large repos (≥20 files) or complex audits, dispatch specialized subagents to keep context clean.

## 🚀 MCP Bootstrap & Tooling (when domyh-hsa available)
1. \`hsa_get_agent_config("bootstrap")\` — load config + skills + memory in 1 call.
2. \`hsa_session(action="intent", focus, mode)\` — declare intent at start.
3. \`hsa_search(query, action="skills")\` — find patterns before coding.
4. \`hsa_search(query)\` — search codebase (never grep when MCP available).
5. \`hsa_trace_flow(entry, direction:"both")\` — before modifying functions.
6. \`hsa_session(action="persist", task_summary, auto_notify:true)\` — persist state at end.

## 🛡️ Pre-Read, Trace Flow & Read-Back Mandate
- **Before MODIFYING**: Read target file (\`view_file\`) + trace callers (\`hsa_trace_flow\`) in 1 parallel turn ➔ edit ➔ read back file to verify diff.
- **Before CREATING**: Search similar (\`hsa_search\`) ➔ check utils/lib ➔ create.
- **Comment Policy**: Default NO comments. Add only when WHY is non-obvious.
- **Terminal Safety (Windows)**: No pipes (|), no interactive without \`-y\`, no infinite commands.

_DOMYH Awesome Code · NockDev_
`;

const TARGET_FILES = [
  join(CONFIGS_DIR, 'aider', 'root.CONVENTIONS.md'),
  join(CONFIGS_DIR, 'amazonq', 'root.amazonq.md'),
  join(CONFIGS_DIR, 'amp', 'root.AGENTS.md'),
  join(CONFIGS_DIR, 'antigravity', 'root.GEMINI.md'),
  join(CONFIGS_DIR, 'augment', 'root.guidelines.md'),
  join(CONFIGS_DIR, 'claude', 'root.CLAUDE.md'),
  join(CONFIGS_DIR, 'cline', 'root.clinerules.md'),
  join(CONFIGS_DIR, 'codex', 'root.AGENTS.md'),
  join(CONFIGS_DIR, 'continue', 'root.continue.md'),
  join(CONFIGS_DIR, 'cursor', 'root.cursorrules'),
  join(CONFIGS_DIR, 'gemini', 'root.GEMINI.md'),
  join(CONFIGS_DIR, 'jetbrains', 'root.guidelines.md'),
  join(CONFIGS_DIR, 'kiro', 'root.kiro.md'),
  join(CONFIGS_DIR, 'roo', 'root.roorules.md'),
  join(CONFIGS_DIR, 'tabnine', 'root.guidelines.md'),
  join(CONFIGS_DIR, 'trae', 'root.trae.md'),
  join(CONFIGS_DIR, 'vscode', 'root.copilot-instructions.md'),
  join(CONFIGS_DIR, 'windsurf', 'root.windsurfrules'),
];

for (const target of TARGET_FILES) {
  writeFileSync(target, LEAN_TEMPLATE, 'utf-8');
  console.log(`✅ Updated: ${target}`);
}

// Project root AGENTS.md and GEMINI.md
const ROOT_VN_INSTRUCTION = 'Tiếng Việt — PHẢI trả lời TOÀN BỘ bằng tiếng Việt. Chỉ giữ tiếng Anh cho code, technical terms, commands. KHÔNG tự chuyển ngôn ngữ.';
const ROOT_PROJECT_DIR = join(ROOT_DIR, '..');
const rootAgentsMd = join(ROOT_PROJECT_DIR, 'AGENTS.md');
const rootGeminiMd = join(ROOT_PROJECT_DIR, 'GEMINI.md');

if (existsSync(rootAgentsMd)) {
  writeFileSync(rootAgentsMd, LEAN_TEMPLATE.replace('{{LANGUAGE_INSTRUCTION}}', ROOT_VN_INSTRUCTION), 'utf-8');
  console.log(`✅ Updated: ${rootAgentsMd}`);
}
if (existsSync(rootGeminiMd)) {
  writeFileSync(rootGeminiMd, LEAN_TEMPLATE.replace('{{LANGUAGE_INSTRUCTION}}', ROOT_VN_INSTRUCTION), 'utf-8');
  console.log(`✅ Updated: ${rootGeminiMd}`);
}

console.log('🎉 All 20 root templates updated to Lean Root Architecture!');
