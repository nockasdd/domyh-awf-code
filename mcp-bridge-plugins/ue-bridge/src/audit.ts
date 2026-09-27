import * as crypto from "crypto";
import * as fs from "fs";
import * as os from "os";
import * as path from "path";

/**
 * Audit trail for code that reaches an editor.
 *
 * The token proves a caller is this bridge; it does not record what the bridge
 * was asked to run. Nothing else in the stack wrote one down either, so a
 * surprise change in a project had no way to be traced back to a call.
 *
 * The code itself is not stored — a hash answers "is this the same snippet I
 * ran before?" without keeping a copy of every script a session has executed
 * on disk. The first line of output is kept because it is usually the useful
 * part and is where an exfiltration would be visible.
 */

const MAX_STDOUT_HEAD = 400;

function stamp(): string {
  return new Date().toISOString();
}

function digest(code: string): string {
  return crypto.createHash("sha256").update(code, "utf8").digest("hex");
}

function head(text: unknown): string {
  if (typeof text !== "string" || text.length === 0) return "";
  const firstLine = text.split("\n", 1)[0];
  return firstLine.length > MAX_STDOUT_HEAD
    ? firstLine.slice(0, MAX_STDOUT_HEAD) + "…"
    : firstLine;
}

export function auditPath(): string {
  const override = process.env.HSA_UE_AUDIT_LOG;
  if (override) return override;
  return path.join(os.homedir(), ".domyh", "audit", "ue-exec.jsonl");
}

/**
 * Writes one JSON line. Never throws: an audit that can fail the exec it is
 * describing is worse than a missing line, because it makes the bridge look
 * unreliable during exactly the incident the log exists for.
 */
export function appendAudit(entry: Record<string, unknown>): void {
  try {
    const file = auditPath();
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.appendFileSync(file, JSON.stringify(entry) + "\n", "utf-8");
  } catch {
    /* see docstring */
  }
}

export function logAttempt(code: string, outcome: "ok" | "err" | "refused", error?: unknown): void {
  appendAudit({
    ts: stamp(),
    code_len: code.length,
    sha256: digest(code),
    outcome,
    error: typeof error === "string" ? head(error) : undefined,
  });
}

export function logResult(
  code: string,
  result: { ok?: boolean; output?: string; error?: string } | null,
): void {
  appendAudit({
    ts: stamp(),
    code_len: code.length,
    sha256: digest(code),
    outcome: result?.ok ? "ok" : "err",
    stdout_head: head(result?.output),
    error_head: head(result?.error),
  });
}
