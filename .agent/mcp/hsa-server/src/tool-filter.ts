/**
 * HSA v6.0 — Tool Filtering
 * Intelligent tool selection to prevent context bloat
 * Reduces token usage by 30-50%
 */

import { Tool } from "@modelcontextprotocol/sdk/types.js";
import { tools as allTools } from "./tools.js";
import { logger, metrics } from "./observability.js";

// ============================================================
// TYPES
// ============================================================

export interface ToolSelector {
  keywords: string[];
  patterns: RegExp[];
  tools: string[];
}

export interface FilterResult {
  tools: Tool[];
  filtered: number;
  reason: string;
}

// ============================================================
// TOOL CATEGORIES
// ============================================================

const log = logger.child({ component: "tool-filter" });

/**
 * Tool selection based on context keywords
 */
const TOOL_SELECTORS: ToolSelector[] = [
  {
    keywords: ["context", "file", "code", "read", "view"],
    patterns: [/get.*context/i, /file.*content/i],
    tools: ["hsa_get_context", "hsa_prefetch", "hsa_status"],
  },
  {
    keywords: ["stack", "detect", "project", "framework", "language"],
    patterns: [/tech.*stack/i, /detect.*project/i],
    tools: ["hsa_detect_stack", "hsa_status"],
  },
  {
    keywords: ["change", "diff", "modified", "update", "watch"],
    patterns: [/file.*change/i, /what.*changed/i],
    tools: ["hsa_check_changes", "hsa_status"],
  },
  {
    keywords: ["health", "status", "monitor", "check"],
    patterns: [/server.*status/i, /health.*check/i],
    tools: ["hsa_health", "hsa_status"],
  },
  {
    keywords: ["agent", "squad", "task", "delegate", "multi"],
    patterns: [/multi.*agent/i, /task.*assign/i],
    tools: ["hsa_multi_agent", "hsa_status"],
  },
  {
    keywords: ["stream", "real-time", "live", "subscribe"],
    patterns: [/stream.*data/i, /real.*time/i],
    tools: ["hsa_streaming", "hsa_status"],
  },
];

/**
 * Core tools always included
 */
const CORE_TOOLS = ["hsa_status"];

/**
 * Max tools to return to prevent bloat
 */
const MAX_TOOLS = 5;

// ============================================================
// FILTERING LOGIC
// ============================================================

/**
 * Extract keywords from context
 */
function extractKeywords(context: string): string[] {
  const words = context.toLowerCase()
    .replace(/[^a-z0-9\s]/g, " ")
    .split(/\s+/)
    .filter((w) => w.length > 2);
  
  return [...new Set(words)];
}

/**
 * Score a selector based on context match
 */
function scoreSelector(selector: ToolSelector, keywords: string[], context: string): number {
  let score = 0;
  
  // Keyword matching
  for (const kw of selector.keywords) {
    if (keywords.includes(kw.toLowerCase())) {
      score += 2;
    }
  }
  
  // Pattern matching
  for (const pattern of selector.patterns) {
    if (pattern.test(context)) {
      score += 5;
    }
  }
  
  return score;
}

/**
 * Get relevant tools for context
 */
export function getRelevantTools(context: string): FilterResult {
  const keywords = extractKeywords(context);
  const toolScores = new Map<string, number>();
  
  // Score each selector
  for (const selector of TOOL_SELECTORS) {
    const score = scoreSelector(selector, keywords, context);
    
    if (score > 0) {
      for (const tool of selector.tools) {
        const current = toolScores.get(tool) || 0;
        toolScores.set(tool, current + score);
      }
    }
  }
  
  // Add core tools
  for (const core of CORE_TOOLS) {
    const current = toolScores.get(core) || 0;
    toolScores.set(core, current + 1);
  }
  
  // If no matches, return core tools only
  if (toolScores.size === 0) {
    const coreTools = allTools.filter((t) => CORE_TOOLS.includes(t.name));
    return {
      tools: coreTools,
      filtered: allTools.length - coreTools.length,
      reason: "No context match, using core tools only",
    };
  }
  
  // Sort by score and take top N
  const sorted = [...toolScores.entries()]
    .sort((a, b) => b[1] - a[1])
    .slice(0, MAX_TOOLS)
    .map(([name]) => name);
  
  const filteredTools = allTools.filter((t) => sorted.includes(t.name));
  const filtered = allTools.length - filteredTools.length;
  
  log.debug({ 
    keywords: keywords.slice(0, 10),
    selected: sorted,
    filtered,
  }, "Tool filtering applied");
  
  metrics.toolsFiltered.inc({ count: filtered.toString() });
  
  return {
    tools: filteredTools,
    filtered,
    reason: `Selected ${filteredTools.length} tools based on context`,
  };
}

/**
 * Get all tools (no filtering)
 */
export function getAllTools(): Tool[] {
  return allTools;
}

/**
 * Get tool by name
 */
export function getToolByName(name: string): Tool | undefined {
  return allTools.find((t) => t.name === name);
}

/**
 * Token estimation for tool definitions
 */
export function estimateToolTokens(tools: Tool[]): number {
  // Rough estimate: ~50 tokens per tool definition
  return tools.reduce((sum, tool) => {
    const descLen = (tool.description?.length || 0) / 4;
    const schemaLen = JSON.stringify(tool.inputSchema).length / 4;
    return sum + 20 + descLen + schemaLen;
  }, 0);
}

/**
 * Get filter stats
 */
export function getFilterStats(): object {
  return {
    totalTools: allTools.length,
    maxReturned: MAX_TOOLS,
    categories: TOOL_SELECTORS.length,
    coreTools: CORE_TOOLS,
  };
}
