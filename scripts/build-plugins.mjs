/**
 * DOMYH Multi-Target Plugin Builder
 * Compiles the Single Source of Truth (SSoT) from domyh-awf & domyh-hsa-mcp into:
 *   1. Claude Code Plugin (.claude-plugin/plugin.json + agents/ + commands/ + skills/ + .mcp.json)
 *   2. Claude Code Marketplace (.claude-plugin/marketplace.json)
 *   3. Google Antigravity Plugin (plugin.json + mcp_config.json + rules/ + skills/)
 *   4. OpenAI Codex Plugin (AGENTS.md + rules/ + skills/ + .codex/)
 *   5. Cursor & VS Code MCP Bundles (.cursor/rules/ + mcp.json)
 */

import { existsSync, mkdirSync, writeFileSync, readFileSync, rmSync, readdirSync } from 'node:fs';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const ROOT_DIR = resolve(__dirname, '..');
const AGENT_DIR = join(ROOT_DIR, '.agent');
const CONFIGS_DIR = join(ROOT_DIR, 'configs');
const DIST_PLUGINS_DIR = join(ROOT_DIR, 'dist-plugins');

const VERSION = '7.2.3';
const HSA_VERSION = '2.0.8';
const AUTHOR = 'NockDev (DOMYH Awesome Code)';

console.log('🚀 Starting DOMYH Multi-Target Plugin Builder v' + VERSION + '...');

// ─── 0. CLEAN OUTPUT DIRECTORY ─────────────────────────────────────────────
if (existsSync(DIST_PLUGINS_DIR)) {
  rmSync(DIST_PLUGINS_DIR, { recursive: true, force: true });
}
mkdirSync(DIST_PLUGINS_DIR, { recursive: true });

// ─── HELPER: Copy directory safely ────────────────────────────────────────
function copyDir(src, dest, filterFn) {
  if (!existsSync(src)) return 0;
  mkdirSync(dest, { recursive: true });
  let count = 0;

  const entries = readdirSync(src, { withFileTypes: true });
  for (const entry of entries) {
    const srcPath = join(src, entry.name);
    const destPath = join(dest, entry.name);

    if (filterFn && !filterFn(srcPath, entry)) continue;

    if (entry.isDirectory()) {
      count += copyDir(srcPath, destPath, filterFn);
    } else if (entry.isFile()) {
      writeFileSync(destPath, readFileSync(srcPath));
      count++;
    }
  }
  return count;
}

// ─── 1. TARGET 1: CLAUDE CODE PLUGIN & MARKETPLACE ─────────────────────────
console.log('\n📦 [1/4] Building Claude Code Plugin & Marketplace...');
const claudePluginDir = join(DIST_PLUGINS_DIR, 'claude-plugin', 'domyh-awesome-code');
const claudeMarketplaceDir = join(DIST_PLUGINS_DIR, 'claude-marketplace');
mkdirSync(claudePluginDir, { recursive: true });
mkdirSync(claudeMarketplaceDir, { recursive: true });

// 1.1 Plugin Manifest (.claude-plugin/plugin.json)
const claudePluginMetaDir = join(claudePluginDir, '.claude-plugin');
mkdirSync(claudePluginMetaDir, { recursive: true });

const claudePluginManifest = {
  name: 'domyh-awesome-code',
  version: VERSION,
  description: 'Senior Software Engineer Rigor for Claude Code: Subagent-Driven Development (SDD), 2-Tier Review Gate, and High-Speed Code Intelligence via HSA MCP.',
  author: {
    name: 'NockDev',
    url: 'https://github.com/NockDev',
  },
  homepage: 'https://github.com/NockDev/domyh-awesome-code-agent',
  repository: 'https://github.com/NockDev/domyh-awesome-code-agent',
  license: 'MIT',
  keywords: ['skills', 'subagents', 'sdd', 'mcp', 'code-intelligence', 'tdd', 'architecture'],
};
writeFileSync(join(claudePluginMetaDir, 'plugin.json'), JSON.stringify(claudePluginManifest, null, 2), 'utf-8');

// 1.2 MCP Server Config (.mcp.json)
const claudeMcpConfig = {
  mcpServers: {
    'domyh-hsa': {
      command: 'npx',
      args: ['-y', `@nockdev/hsa@^${HSA_VERSION}`],
      env: {
        HSA_MCP_EXTENDED_RESPONSE: '0',
      },
    },
  },
};
writeFileSync(join(claudePluginDir, '.mcp.json'), JSON.stringify(claudeMcpConfig, null, 2), 'utf-8');

// 1.3 Custom Agents (agents/*.md)
const claudeAgentsDir = join(claudePluginDir, 'agents');
mkdirSync(claudeAgentsDir, { recursive: true });

const personasDir = join(AGENT_DIR, 'personas');
if (existsSync(personasDir)) {
  const personas = readdirSync(personasDir).filter(f => f.endsWith('.md'));
  for (const personaFile of personas) {
    const content = readFileSync(join(personasDir, personaFile), 'utf-8');
    writeFileSync(join(claudeAgentsDir, personaFile), content, 'utf-8');
  }
}

// 1.4 Slash Commands (commands/*.md)
const claudeCommandsDir = join(claudePluginDir, 'commands');
mkdirSync(claudeCommandsDir, { recursive: true });

const workflowsDir = join(AGENT_DIR, 'workflows');
if (existsSync(workflowsDir)) {
  const workflows = readdirSync(workflowsDir).filter(f => f.endsWith('.md'));
  for (const wfFile of workflows) {
    const content = readFileSync(join(workflowsDir, wfFile), 'utf-8');
    writeFileSync(join(claudeCommandsDir, wfFile), content, 'utf-8');
  }
}

// 1.5 Skills (skills/**/SKILL.md)
const claudeSkillsDir = join(claudePluginDir, 'skills');
const copiedSkills = copyDir(join(AGENT_DIR, 'skills'), claudeSkillsDir, (path, entry) => {
  return !path.includes('node_modules') && !path.includes('.git');
});

// 1.6 Hooks (hooks/hooks.json)
const claudeHooksDir = join(claudePluginDir, 'hooks');
mkdirSync(claudeHooksDir, { recursive: true });
const claudeHooksConfig = {
  hooks: {
    preToolExecution: [
      {
        matcher: '.*',
        description: 'Verify surgical scope and adherence to Task Contract',
      },
    ],
    postToolExecution: [
      {
        matcher: 'Edit|Write|Replace',
        description: 'Trigger 2-tier review gate and change verification',
      },
    ],
  },
};
writeFileSync(join(claudeHooksDir, 'hooks.json'), JSON.stringify(claudeHooksConfig, null, 2), 'utf-8');

// 1.7 Claude Marketplace Manifest (.claude-plugin/marketplace.json)
const claudeMarketplaceMetaDir = join(claudeMarketplaceDir, '.claude-plugin');
mkdirSync(claudeMarketplaceMetaDir, { recursive: true });

const claudeMarketplaceManifest = {
  name: 'nockdev-marketplace',
  owner: {
    name: 'NockDev',
    url: 'https://github.com/NockDev',
  },
  description: 'Official Marketplace for DOMYH Awesome Code Plugins and Agentic Extensions.',
  plugins: [
    {
      name: 'domyh-awesome-code',
      source: './plugins/domyh-awesome-code',
      description: 'Subagent-Driven Development (SDD), 2-Tier Quality Review Gates, and Fast Code Intelligence for Claude Code.',
      version: VERSION,
    },
  ],
};
writeFileSync(join(claudeMarketplaceMetaDir, 'marketplace.json'), JSON.stringify(claudeMarketplaceManifest, null, 2), 'utf-8');

// Copy plugin into marketplace catalog
const mktPluginDest = join(claudeMarketplaceDir, 'plugins', 'domyh-awesome-code');
copyDir(claudePluginDir, mktPluginDest);

console.log(`   ✅ Claude Code Plugin built (${copiedSkills} skill files, custom agents, slash commands)`);
console.log(`   ✅ Claude Marketplace manifest created (.claude-plugin/marketplace.json)`);

// ─── 2. TARGET 2: GOOGLE ANTIGRAVITY PLUGIN ────────────────────────────────
console.log('\n📦 [2/4] Building Google Antigravity Plugin...');
const agyPluginDir = join(DIST_PLUGINS_DIR, 'antigravity-plugin', 'domyh-awesome-code');
mkdirSync(agyPluginDir, { recursive: true });

// 2.1 Manifest (plugin.json)
const agyManifest = {
  name: 'domyh-awesome-code',
  version: VERSION,
  description: 'DOMYH Awesome Code Customization Bundle for Google Antigravity. Features SDD Subagents, 2-Tier Review Gate, and HSA Code Intelligence.',
  author: AUTHOR,
};
writeFileSync(join(agyPluginDir, 'plugin.json'), JSON.stringify(agyManifest, null, 2), 'utf-8');

// 2.2 MCP Server Config (mcp_config.json)
const agyMcpConfig = {
  mcpServers: {
    'domyh-hsa': {
      command: 'npx',
      args: ['-y', `@nockdev/hsa@^${HSA_VERSION}`],
      env: {
        HSA_MCP_EXTENDED_RESPONSE: '0',
      },
    },
  },
};
writeFileSync(join(agyPluginDir, 'mcp_config.json'), JSON.stringify(agyMcpConfig, null, 2), 'utf-8');

// 2.3 Rules (rules/)
const agyRulesDir = join(agyPluginDir, 'rules');
copyDir(join(AGENT_DIR, 'rules'), agyRulesDir);

// 2.4 Skills (skills/)
const agySkillsDir = join(agyPluginDir, 'skills');
copyDir(join(AGENT_DIR, 'skills'), agySkillsDir);

// 2.5 Hooks (hooks.json)
const agyHooks = {
  hooks: {
    beforeAction: {
      action: 'hsa_search',
      description: 'Search skills and patterns before action',
    },
    afterEdit: {
      action: 'hsa_check_changes',
      description: 'Update Merkle index after code edits',
    },
  },
};
writeFileSync(join(agyPluginDir, 'hooks.json'), JSON.stringify(agyHooks, null, 2), 'utf-8');

console.log('   ✅ Antigravity Plugin built (plugin.json, mcp_config.json, rules/, skills/, hooks.json)');

// ─── 3. TARGET 3: OPENAI CODEX PLUGIN & SCOPED PACKAGE ─────────────────────
console.log('\n📦 [3/4] Building OpenAI Codex Plugin & AGENTS.md Hierarchy...');
const codexPluginDir = join(DIST_PLUGINS_DIR, 'codex-plugin');
mkdirSync(codexPluginDir, { recursive: true });

// 3.1 AGENTS.md
const codexAgentsMd = join(CONFIGS_DIR, 'codex', 'root.AGENTS.md');
if (existsSync(codexAgentsMd)) {
  writeFileSync(join(codexPluginDir, 'AGENTS.md'), readFileSync(codexAgentsMd));
}

// 3.2 Rules and Skills
copyDir(join(AGENT_DIR, 'rules'), join(codexPluginDir, 'rules'));
copyDir(join(AGENT_DIR, 'skills'), join(codexPluginDir, 'skills'));

// 3.3 Codex Manifest
const codexManifest = {
  name: 'domyh-codex',
  version: VERSION,
  description: 'DOMYH Awesome Code for OpenAI Codex CLI / App.',
  mcp: {
    server: '@nockdev/hsa',
  },
};
writeFileSync(join(codexPluginDir, 'codex.json'), JSON.stringify(codexManifest, null, 2), 'utf-8');

console.log('   ✅ OpenAI Codex Plugin built (AGENTS.md, rules/, skills/, codex.json)');

// ─── 4. TARGET 4: CURSOR & VS CODE MCP / RULES BUNDLES ──────────────────────
console.log('\n📦 [4/4] Building Cursor & VS Code Bundles...');
const cursorBundleDir = join(DIST_PLUGINS_DIR, 'cursor-bundle');
const vscodeBundleDir = join(DIST_PLUGINS_DIR, 'vscode-bundle');
mkdirSync(cursorBundleDir, { recursive: true });
mkdirSync(vscodeBundleDir, { recursive: true });

// 4.1 Cursor rules & MCP
const cursorRulesFile = join(CONFIGS_DIR, 'cursor', 'root.cursorrules');
if (existsSync(cursorRulesFile)) {
  writeFileSync(join(cursorBundleDir, '.cursorrules'), readFileSync(cursorRulesFile));
}
copyDir(join(AGENT_DIR, 'rules'), join(cursorBundleDir, '.cursor', 'rules'));
const cursorMcp = {
  mcpServers: {
    'domyh-hsa': {
      command: 'npx',
      args: ['-y', `@nockdev/hsa@^${HSA_VERSION}`],
    },
  },
};
writeFileSync(join(cursorBundleDir, 'mcp.json'), JSON.stringify(cursorMcp, null, 2), 'utf-8');

// 4.2 VS Code Copilot & MCP
const vscodeInstructions = join(CONFIGS_DIR, 'vscode', 'root.copilot-instructions.md');
const vscodeMetaDir = join(vscodeBundleDir, '.github');
mkdirSync(vscodeMetaDir, { recursive: true });
if (existsSync(vscodeInstructions)) {
  writeFileSync(join(vscodeMetaDir, 'copilot-instructions.md'), readFileSync(vscodeInstructions));
}
writeFileSync(join(vscodeBundleDir, 'mcp.json'), JSON.stringify(cursorMcp, null, 2), 'utf-8');

console.log('   ✅ Cursor & VS Code Bundles built (.cursorrules, copilot-instructions.md, mcp.json)');

// ─── 5. GENERATE DISTRIBUTION SUMMARY & MANIFEST ───────────────────────────
const distSummary = {
  builder: 'DOMYH Multi-Target Plugin Builder',
  version: VERSION,
  builtAt: new Date().toISOString(),
  targets: {
    claude_code: {
      plugin_path: 'dist-plugins/claude-plugin/domyh-awesome-code',
      marketplace_path: 'dist-plugins/claude-marketplace',
      install_command: '/plugin install domyh@nockdev-marketplace',
    },
    antigravity: {
      plugin_path: 'dist-plugins/antigravity-plugin/domyh-awesome-code',
      install_path: '~/.gemini/antigravity/plugins/domyh-awesome-code',
    },
    codex: {
      plugin_path: 'dist-plugins/codex-plugin',
      config_file: 'AGENTS.md',
    },
    cursor: {
      bundle_path: 'dist-plugins/cursor-bundle',
    },
    vscode: {
      bundle_path: 'dist-plugins/vscode-bundle',
    },
  },
};
writeFileSync(join(DIST_PLUGINS_DIR, 'manifest.json'), JSON.stringify(distSummary, null, 2), 'utf-8');

console.log('\n🎉 ALL TARGETS BUILT SUCCESSFULLY! Output available at: ' + DIST_PLUGINS_DIR);
