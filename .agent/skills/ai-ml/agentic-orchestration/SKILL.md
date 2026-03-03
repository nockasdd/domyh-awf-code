---
name: agentic-orchestration
description: Multi-agent task delegation and orchestration patterns for AI coding assistants
---

# Agentic Orchestration Patterns

## When to Delegate (Sub-Agent)

Use sub-agents when:
- Task requires **>3 independent research paths**
- Context window approaching **>70% capacity**
- Task needs **specialist knowledge** (security audit, visual design, performance profiling)
- Multiple files need **parallel analysis**
- Current context would be **polluted** by sub-task details

## Anthropic's 5 Agentic Patterns

### 1. Prompt Chaining (Sequential)
```
Step1 → validate → Step2 → validate → Step3
```
Use for: Workflows with clear dependencies. Each step builds on previous output.

### 2. Routing (Classification)
```
Input → Classify → Route to specialist handler
```
Use for: Different input types need different processing. Map user intent → persona.

### 3. Parallelization (Fan-Out/Fan-In)
```
Task → [SubtaskA, SubtaskB, SubtaskC] → Merge results
```
Use for: Independent subtasks. Research multiple topics simultaneously.

### 4. Orchestrator-Worker (Delegation)
```
Orchestrator: Plan → Assign workers → Monitor → Synthesize
Workers: Execute specialized subtask → Report back
```
Use for: Complex tasks requiring dynamic decomposition by LLM.

### 5. Evaluator-Optimizer (Feedback Loop)
```
Generate → Evaluate quality → Refine → Re-evaluate → Accept
```
Use for: Quality-critical output. Code review, test coverage, documentation.

## HSA Tools for Orchestration

| Tool | Purpose | When |
|------|---------|------|
| `hsa_session` | Set orchestration goal | Session start |
| `hsa_delegate` | Create context packet for sub-agent | Before delegation |
| `hsa_delegate` | Select tools for sub-agent type | With handoff |
| `hsa_session` | Track trajectory → tactic → action | Throughout |
| `hsa_session` | Detect scope drift | Before unplanned work |
| `hsa_session` | Persist key facts | After discoveries |
| `hsa_feedback` | Rate result quality | After sub-agent returns |

## Delegation Flow

```
1. Declare intent (mode: plan_driven)
2. Break task into subtasks
3. For each subtask:
   a. Prepare handoff (task_type: code|test|review|debug|browser|research)
   b. Filter tools for sub-agent
   c. Sub-agent executes with isolated context
   d. Collect result, provide feedback
4. Synthesize all results
5. Verify complete solution
```

## Context Isolation Rules

- Sub-agents get **minimal context** — only what they need
- Sub-agents should NOT receive full conversation history
- Results from sub-agents should be **summarized** before merging
- Use `context: fork` (Claude Code) or subagent tools (VS Code) for isolation
