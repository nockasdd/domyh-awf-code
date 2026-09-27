# Agent Communication Protocol v7.1.0
# Protocol for agent-to-agent communication during orchestration
# Source: A2A JSON-RPC, AutoGen messaging, OpenAI Swarm handoffs
---
name: agent-communication
rule_id: "MOD-COM-001"

description: |
  Defines how agents communicate during orchestration.
  Three channels: shared state, handoff packets, event log.

category: "workflow"

context:
  always_apply: false
  personas: ["orchestrator"]
  trigger: "When orchestration is active"

# ═══ COMMUNICATION CHANNELS ═══

channels:
  # Channel 1: Shared State (primary)
  shared_state:
    description: "All agents read/write orchestration-state.yaml"
    location: "memory/orchestration/orch-{id}.yaml"
    operations:
      read: "Any specialist can read shared_context at any time"
      write_decisions: "Specialist appends to shared_context.decisions[]"
      write_output: "Specialist writes to own task.output"
      write_blockers: "Specialist adds to shared_context.blockers[]"

  # Channel 2: Handoff Packet (one-time injection)
  handoff:
    description: "Orchestrator → Specialist via hsa_delegate"
    when: "Task assignment in EXECUTE step"
    includes:
      - "Project snapshot (stack, structure)"
      - "Relevant files for this specific task"
      - "Constraints and conventions"
      - "Prior task outputs (if task has dependencies)"
      - "Tool allow/deny list"
    max_tokens: 1500

  # Channel 3: Event Log (append-only audit trail)
  event_log:
    description: "All state changes recorded for observability"
    location: "memory/orchestration/orch-{id}.yaml → event_log[]"
    events:
      - "started: Task execution began"
      - "completed: Task finished successfully"
      - "failed: Task encountered error"
      - "retried: Task retry attempt"
      - "checkpoint: State snapshot saved"
      - "decision: Agent made architectural/technical decision"
      - "blocker: Agent cannot proceed, needs input"

  # Channel 4: Native subagent dispatch
  native_dispatch:
    description: "Hand a prepared contract to the platform's own subagent tool"
    when: "A subtask is independent enough to run without the main context"
    task_types: [code, test, review, debug, browser, research]
    lifecycle:
      1: "hsa_delegate({action:'prepare', task_type:'[type]', focus_files:[...]})"
      2: "Dispatch through the platform's native subagent tool (Agent, invoke_subagent, background agent)"
      3: "Collect the result when it returns"
      4: "hsa_delegate({action:'verify', focus_files:[...], modified_files:[...]})"
    # MANDATORY: evaluate delegation before the EXECUTE step
    mandatory_evaluation:
      trigger: "Before EXECUTE step in any workflow"
      check: "Does the platform expose a subagent tool?"
      scoring: "See delegation-intelligence skill 1% Trigger Gate"
      auto_delegate: "Complexity ≥ 8 (>200 LOC, multi-file, complex algorithm)"
      suggest_delegate: "Complexity 5-7 (>100 LOC, moderate changes)"
      skip: "Complexity < 5 or no subagent tool available"

# ═══ COMMUNICATION FLOW ═══

flow:
  steps:
    1: "Orchestrator creates state → writes dag.tasks[]"
    2: "For each task assignment:"
    3: "  a. Orchestrator prepares handoff packet (hsa_delegate)"
    4: "  b. Orchestrator updates task.status = 'running'"
    5: "  c. Specialist reads: handoff packet + shared_context"
    6: "  d. Specialist executes task using assigned workflow"
    7: "  e. Specialist writes: task.output + shared_context.decisions[]"
    8: "  f. Orchestrator reads output → decides next task"
    9: "After all tasks: Orchestrator synthesizes results"

# ═══ MESSAGE FORMAT ═══

message_format:
  from: "{persona_name}"
  to: "orchestrator | shared_context"
  type: "decision | blocker | output | request"
  content: "{structured data}"
  timestamp: "{ISO}"

# ═══ STATE PERMISSIONS ═══

permissions:
  orchestrator:
    read: ["*"]
    write: ["dag", "event_log", "budget", "shared_context", "status"]
  specialist:
    read: ["shared_context", "own_task", "dependency_task.output"]
    write: ["own_task.output", "shared_context.decisions", "shared_context.blockers"]

integration:
  tier: 2
  related_modules: ["agent-delegation", "complexity-scoring", "stop-conditions"]
