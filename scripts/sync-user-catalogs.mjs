#!/usr/bin/env node
/**
 * scripts/sync-user-catalogs.mjs
 * SSoT synchronization to both ~/.agent and ~/.agents user home catalogs.
 * Solves ecosystem fragmentation (Codex/Amp using ~/.agents, Cursor/Gemini using ~/.agent).
 */

import fs from 'node:fs';
import path from 'node:path';
import { homedir } from 'node:os';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT_DIR = path.resolve(__dirname, '..');

const SOURCE_SKILLS = path.join(ROOT_DIR, '.agent', 'skills');
const SOURCE_RULES = path.join(ROOT_DIR, '.agent', 'rules');

const HOME = homedir();
const TARGETS = [
  { name: '~/.agent', base: path.join(HOME, '.agent') },
  { name: '~/.agents', base: path.join(HOME, '.agents') },
];

function syncDirectory(src, dest) {
  if (!fs.existsSync(src)) return 0;
  fs.mkdirSync(dest, { recursive: true });
  let count = 0;

  const entries = fs.readdirSync(src, { withFileTypes: true });
  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);

    if (entry.isDirectory()) {
      count += syncDirectory(srcPath, destPath);
    } else {
      let shouldCopy = false;
      if (!fs.existsSync(destPath)) {
        shouldCopy = true;
      } else {
        const srcStat = fs.statSync(srcPath);
        const destStat = fs.statSync(destPath);
        if (srcStat.size !== destStat.size || srcStat.mtimeMs > destStat.mtimeMs) {
          shouldCopy = true;
        }
      }

      if (shouldCopy) {
        fs.copyFileSync(srcPath, destPath);
        count++;
      }
    }
  }
  return count;
}

export function syncUserCatalogs() {
  console.log('🔄 Syncing user home agent catalogs (~/.agent and ~/.agents)...');

  for (const target of TARGETS) {
    const destSkills = path.join(target.base, 'skills');
    const destRules = path.join(target.base, 'rules');

    const sCount = syncDirectory(SOURCE_SKILLS, destSkills);
    const rCount = syncDirectory(SOURCE_RULES, destRules);

    console.log(`   ✅ ${target.name}: ${sCount} skill files, ${rCount} rule files updated.`);
  }

  console.log('🎉 Dual catalog sync complete!');
}

if (process.argv[1] && path.resolve(process.argv[1]) === path.resolve(__filename)) {
  syncUserCatalogs();
}

