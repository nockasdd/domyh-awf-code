# 🎭 Personas System

> AI agent personas with identity, memory, and collaboration

---

## Overview

Personas define specialized agent roles with distinct:

- **Identity** — Role, goal, and backstory
- **Traits** — Behavioral characteristics
- **Memory** — Integration with memory system
- **Tools** — Permitted tool usage
- **Collaboration** — Multi-agent coordination

---

## Available Personas

| Persona          | Role                             | Triggers             | Version |
| ---------------- | -------------------------------- | -------------------- | ------- |
| **developer**    | Senior Code Craftsman            | `/code`, `/refactor` |         |
| **architect**    | Solution Architect               | `/plan`, `/design`   |         |
| **planner**      | Task Decomposition Specialist    | `/plan`, `/break`    |         |
| **researcher**   | Information Gathering Specialist | `/research`, `/find` |         |
| **orchestrator** | Multi-Agent Coordinator          | Auto-activated       |         |
| **security**     | Security Specialist              | `/security`, `/scan` |         |
| **auditor**      | 5-Expert Audit Panel             | `/ap`                |         |
| **debugger**     | Bug Hunter                       | `/debug`             |         |
| **tester**       | Quality Assurance                | `/test`              |         |
| **devops**       | Infrastructure Engineer          | `/deploy`            |         |
| **documenter**   | Technical Writer                 | `/doc`               |         |

---

## v6.4.10 Schema

All personas follow the enhanced schema:

```yaml
---
name: [persona_name]
persona_id: "[prefix]-001"

# Core Identity (CrewAI Pattern)
identity:
  role: "One-line role"
  goal: "Primary objective"
  backstory: |
    Multi-line background that shapes behavior...

# Behavioral Traits (Anthropic Pattern)
traits:
  communication_style: "direct but supportive"
  detail_level: "thorough with explanations"
  decision_making: "evidence-based"
  error_handling: "proactive"

# Cognitive Capabilities
capabilities:
  reasoning: true
  reflection: true
  planning: true
  multimodal: false

# Memory Integration (Letta Pattern)
memory:
  use_core_memory: true
  core_blocks: ["persona", "user", "project"]
  short_term: "conversation_history"
  long_term: "patterns/successes.json"

# Tool Permissions
tools:
  allowed: [list]
  restricted: [list]
  requires_approval: [list]

# Collaboration (LangGraph Pattern)
collaboration:
  can_delegate_to: [personas]
  reports_to: [personas]
  handoff_conditions:
    "condition": "target_persona"

# Triggers & Rules
triggers: ["/command1", "/command2"]
enforces: [rule1, rule2]

# Output Configuration
output:
  format: "structured_markdown"
  template: "path/to/template.md"
---
```

---

## Key Concepts

### Identity (CrewAI Pattern)

- **Role**: What the persona does
- **Goal**: What they're trying to achieve
- **Backstory**: Background that shapes behavior

### Memory Integration (Letta Pattern)

- Personas access core memory blocks
- Learn from successes and errors
- Build patterns over time

### Collaboration (LangGraph Pattern)

- Personas can delegate to others
- Handoff conditions trigger transitions
- Orchestrator coordinates complex tasks

---

## Directory Structure

```
.agent/personas/
├── README.md              # This file
├── persona.schema.yaml    # Schema definition
├── developer.md           # Enhanced
├── architect.md           # Enhanced
├── planner.md             # NEW
├── researcher.md          # NEW
├── orchestrator.md        # NEW
├── security.md            # NEW
├── auditor.md
├── debugger.md
├── tester.md
├── devops.md
└── documenter.md
```

---

## Usage

### Direct Trigger

```
/code implement user authentication
```

### Agent Auto-Selection

The router automatically selects the appropriate persona based on:

1. Command triggers
2. Intent classification
3. Task complexity

### Multi-Agent Flow

For complex tasks, the orchestrator coordinates:

```
User Request → Orchestrator → [Planner → Developer → Tester] → Result
```

---

## Best Practices

1. **Let personas use their strengths** — Don't ask developer for architecture decisions
2. **Trust the orchestrator** — For multi-domain tasks, let it coordinate
3. **Check persona memory** — Patterns in `patterns/` improve over time
4. **Customize traits** — Adjust communication style in `state.json`

---
