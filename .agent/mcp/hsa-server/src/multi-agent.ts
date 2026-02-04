/**
 * HSA v5.0 — Multi-Agent Coordination
 * Agent squad support for collaborative workflows
 * Follows 2026 MCP multi-agent patterns
 */

import { logger, generateTraceContext } from "./observability.js";
import type { HSAConfig } from "./config.js";

// ============================================================
// TYPES
// ============================================================

export interface Agent {
  id: string;
  name: string;
  type: "primary" | "specialist" | "reviewer" | "coordinator";
  capabilities: string[];
  status: "idle" | "working" | "waiting" | "completed";
  currentTask?: string;
}

export interface Task {
  id: string;
  description: string;
  type: "analysis" | "coding" | "testing" | "review" | "research";
  status: "pending" | "assigned" | "in-progress" | "completed" | "failed";
  assignedTo?: string;
  result?: unknown;
  dependencies?: string[];
  createdAt: Date;
  completedAt?: Date;
}

export interface Squad {
  id: string;
  name: string;
  agents: Agent[];
  tasks: Task[];
  coordinator: string;
  status: "forming" | "active" | "completing" | "disbanded";
  createdAt: Date;
}

export interface Delegation {
  taskId: string;
  fromAgent: string;
  toAgent: string;
  reason: string;
  timestamp: Date;
}

// ============================================================
// SQUAD MANAGEMENT
// ============================================================

const log = logger.child({ component: "multi-agent" });
const activeSquads = new Map<string, Squad>();
const delegationHistory: Delegation[] = [];

export function createSquad(name: string, coordinator: Agent): Squad {
  const squadId = `squad_${Date.now().toString(36)}`;
  
  const squad: Squad = {
    id: squadId,
    name,
    agents: [coordinator],
    tasks: [],
    coordinator: coordinator.id,
    status: "forming",
    createdAt: new Date(),
  };
  
  activeSquads.set(squadId, squad);
  log.info({ squadId, name }, "Squad created");
  
  return squad;
}

export function addAgentToSquad(squadId: string, agent: Agent): boolean {
  const squad = activeSquads.get(squadId);
  if (!squad) return false;
  
  squad.agents.push(agent);
  log.info({ squadId, agentId: agent.id }, "Agent joined squad");
  
  return true;
}

export function removeAgentFromSquad(squadId: string, agentId: string): boolean {
  const squad = activeSquads.get(squadId);
  if (!squad) return false;
  
  squad.agents = squad.agents.filter((a) => a.id !== agentId);
  log.info({ squadId, agentId }, "Agent left squad");
  
  return true;
}

export function disbandSquad(squadId: string): void {
  const squad = activeSquads.get(squadId);
  if (squad) {
    squad.status = "disbanded";
    activeSquads.delete(squadId);
    log.info({ squadId }, "Squad disbanded");
  }
}

// ============================================================
// TASK MANAGEMENT
// ============================================================

export function createTask(
  squadId: string,
  description: string,
  type: Task["type"],
  dependencies?: string[]
): Task | null {
  const squad = activeSquads.get(squadId);
  if (!squad) return null;
  
  const task: Task = {
    id: `task_${Date.now().toString(36)}`,
    description,
    type,
    status: "pending",
    dependencies,
    createdAt: new Date(),
  };
  
  squad.tasks.push(task);
  log.info({ squadId, taskId: task.id, type }, "Task created");
  
  return task;
}

export function assignTask(squadId: string, taskId: string, agentId: string): boolean {
  const squad = activeSquads.get(squadId);
  if (!squad) return false;
  
  const task = squad.tasks.find((t) => t.id === taskId);
  const agent = squad.agents.find((a) => a.id === agentId);
  
  if (!task || !agent) return false;
  
  // Check dependencies
  if (task.dependencies) {
    const allDepsComplete = task.dependencies.every((depId) => {
      const dep = squad.tasks.find((t) => t.id === depId);
      return dep?.status === "completed";
    });
    
    if (!allDepsComplete) {
      log.warn({ taskId, agentId }, "Cannot assign - dependencies not complete");
      return false;
    }
  }
  
  task.status = "assigned";
  task.assignedTo = agentId;
  agent.status = "working";
  agent.currentTask = taskId;
  
  log.info({ squadId, taskId, agentId }, "Task assigned");
  return true;
}

export function completeTask(squadId: string, taskId: string, result: unknown): boolean {
  const squad = activeSquads.get(squadId);
  if (!squad) return false;
  
  const task = squad.tasks.find((t) => t.id === taskId);
  if (!task) return false;
  
  task.status = "completed";
  task.result = result;
  task.completedAt = new Date();
  
  // Update agent status
  const agent = squad.agents.find((a) => a.id === task.assignedTo);
  if (agent) {
    agent.status = "idle";
    agent.currentTask = undefined;
  }
  
  log.info({ squadId, taskId }, "Task completed");
  return true;
}

// ============================================================
// TASK DELEGATION
// ============================================================

export function delegateTask(
  squadId: string,
  taskId: string,
  fromAgentId: string,
  toAgentId: string,
  reason: string
): boolean {
  const squad = activeSquads.get(squadId);
  if (!squad) return false;
  
  const task = squad.tasks.find((t) => t.id === taskId);
  const fromAgent = squad.agents.find((a) => a.id === fromAgentId);
  const toAgent = squad.agents.find((a) => a.id === toAgentId);
  
  if (!task || !fromAgent || !toAgent) return false;
  
  // Record delegation
  delegationHistory.push({
    taskId,
    fromAgent: fromAgentId,
    toAgent: toAgentId,
    reason,
    timestamp: new Date(),
  });
  
  // Update assignment
  task.assignedTo = toAgentId;
  fromAgent.status = "idle";
  fromAgent.currentTask = undefined;
  toAgent.status = "working";
  toAgent.currentTask = taskId;
  
  log.info({ taskId, fromAgentId, toAgentId, reason }, "Task delegated");
  return true;
}

// ============================================================
// COORDINATION HELPERS
// ============================================================

export function findAvailableAgent(
  squadId: string,
  requiredCapability?: string
): Agent | null {
  const squad = activeSquads.get(squadId);
  if (!squad) return null;
  
  return squad.agents.find((agent) => {
    if (agent.status !== "idle") return false;
    if (requiredCapability && !agent.capabilities.includes(requiredCapability)) {
      return false;
    }
    return true;
  }) || null;
}

export function getSquadStatus(squadId: string): object | null {
  const squad = activeSquads.get(squadId);
  if (!squad) return null;
  
  return {
    id: squad.id,
    name: squad.name,
    status: squad.status,
    agents: squad.agents.map((a) => ({
      id: a.id,
      name: a.name,
      status: a.status,
      currentTask: a.currentTask,
    })),
    tasks: {
      total: squad.tasks.length,
      pending: squad.tasks.filter((t) => t.status === "pending").length,
      inProgress: squad.tasks.filter((t) => t.status === "in-progress").length,
      completed: squad.tasks.filter((t) => t.status === "completed").length,
    },
  };
}

export function listActiveSquads(): Squad[] {
  return Array.from(activeSquads.values());
}

// ============================================================
// MCP TOOL INTEGRATION
// ============================================================

export async function handleMultiAgentRequest(
  action: string,
  args: Record<string, unknown>,
  config: HSAConfig
): Promise<unknown> {
  switch (action) {
    case "create_squad":
      return createSquad(
        args.name as string,
        args.coordinator as Agent
      );
      
    case "add_agent":
      return addAgentToSquad(
        args.squadId as string,
        args.agent as Agent
      );
      
    case "create_task":
      return createTask(
        args.squadId as string,
        args.description as string,
        args.type as Task["type"],
        args.dependencies as string[] | undefined
      );
      
    case "assign_task":
      return assignTask(
        args.squadId as string,
        args.taskId as string,
        args.agentId as string
      );
      
    case "complete_task":
      return completeTask(
        args.squadId as string,
        args.taskId as string,
        args.result
      );
      
    case "squad_status":
      return getSquadStatus(args.squadId as string);
      
    case "list_squads":
      return listActiveSquads();
      
    default:
      throw new Error(`Unknown multi-agent action: ${action}`);
  }
}
