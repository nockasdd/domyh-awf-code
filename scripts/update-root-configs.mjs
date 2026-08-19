import fs from 'node:fs';
import path from 'node:path';

const targetFiles = [
  'domyh-awf/configs/antigravity/root.GEMINI.md',
  'domyh-awf/configs/claude/root.CLAUDE.md',
  'domyh-awf/configs/cursor/root.cursorrules',
  'domyh-awf/configs/codex/root.AGENTS.md',
  'domyh-awf/configs/gemini/root.GEMINI.md',
  'domyh-awf/configs/vscode/root.copilot-instructions.md',
  'domyh-awf/configs/windsurf/root.windsurfrules',
  'domyh-awf/configs/cline/root.clinerules.md',
  'domyh-awf/configs/roo/root.roorules.md',
  'domyh-awf/configs/amp/root.AGENTS.md',
  'domyh-awf/configs/continue/root.continue.md',
  'domyh-awf/configs/amazonq/root.amazonq.md',
  'domyh-awf/configs/augment/root.guidelines.md',
  'domyh-awf/configs/jetbrains/root.guidelines.md',
  'domyh-awf/configs/kiro/root.kiro.md',
  'domyh-awf/configs/tabnine/root.guidelines.md',
  'domyh-awf/configs/trae/root.trae.md',
  'domyh-awf/configs/aider/root.CONVENTIONS.md',
  'domyh-awf/AGENTS.md',
  'domyh-awf/GEMINI.md',
  'AGENTS.md',
  'GEMINI.md'
];

const oldTrace = `## Trace Flow (DRY enforcement)

Before MODIFYING: grep symbol → read callers → read tests → THEN edit.
Before CREATING: grep similar → check utils/lib → check exports → check archive → THEN create.
Before DEPENDENCY: search existing utils first.`;

const newTrace = `## Trace Flow (DRY enforcement)

Before MODIFYING: read target file (\`view_file\`) → trace callers (\`hsa_trace_flow\` or grep) → read tests → THEN edit → read back file to verify diff.
Before CREATING: search similar (\`hsa_search\`) → check utils/lib → check exports → check archive → THEN create.
Before DEPENDENCY: search existing utils first.`;

const oldCore = `## Core Rules

- Never generate harmful code
- Verify claims with file:line references
- Confirm before destructive actions (delete, drop, deploy)
- Use file outlines before full reads; parallel calls for independent ops
- Match existing style EXACTLY — no quote/whitespace/typehint changes unless asked
- Every changed line must trace directly to user's request`;

const newCore = `## Core Rules

- Never generate harmful code
- Pre-Read & Read-Back: Read file before editing; read back after editing to verify diff and syntax
- Verify claims with file:line references
- Confirm before destructive actions (delete, drop, deploy)
- Use file outlines before full reads; parallel calls for independent ops
- Match existing style EXACTLY — no quote/whitespace/typehint changes unless asked
- Every changed line must trace directly to user's request`;

let updatedCount = 0;
for (const relPath of targetFiles) {
  if (fs.existsSync(relPath)) {
    let content = fs.readFileSync(relPath, 'utf8');
    let changed = false;
    if (content.includes(oldTrace)) {
      content = content.replace(oldTrace, newTrace);
      changed = true;
    }
    if (content.includes(oldCore)) {
      content = content.replace(oldCore, newCore);
      changed = true;
    }
    if (changed) {
      fs.writeFileSync(relPath, content, 'utf8');
      updatedCount++;
      console.log('Updated:', relPath);
    }
  }
}
console.log('Total root templates updated:', updatedCount);
