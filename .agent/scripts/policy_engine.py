#!/usr/bin/env python3
"""
DOMYH Awesome Code — Policy Engine v2.0
Research-backed: OpenAI Instruction Hierarchy (2024), Claude Code Hooks (2025)

This engine provides deterministic enforcement of rules, independent of LLM behavior.
Can be integrated with Claude Code hooks, Cursor hooks, or run standalone.
"""

import json
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Optional


class Severity(Enum):
    """Rule severity levels"""
    BLOCK = "block"  # Response INVALID if violated
    WARN = "warn"    # Log warning, continue


@dataclass
class Requirement:
    """A single rule requirement"""
    id: str
    text: str
    severity: Severity
    tier: int = 0
    anchor: str = ""
    check_fn: Optional[Callable] = None
    
    def check(self, context: dict, response: str = "") -> bool:
        """Check if requirement is satisfied"""
        if self.check_fn:
            return self.check_fn(context, response)
        return True  # Default: pass if no check function


@dataclass
class Violation:
    """A rule violation"""
    requirement_id: str
    severity: Severity
    message: str
    timestamp: str
    context_snippet: str = ""


class PolicyEngine:
    """
    Deterministic policy enforcement engine.
    Loads rules from SACRED_RULES.xml and validates prompts/responses.
    """
    
    def __init__(self, rules_path: str = ".agent/rules/SACRED_RULES.xml"):
        self.rules_path = Path(rules_path)
        self.requirements: list[Requirement] = []
        self.violations: list[Violation] = []
        self.session_rules: dict = {}
        
        self._load_sacred_rules()
        self._load_session_rules()
        self._register_builtin_checks()
    
    def _load_sacred_rules(self) -> None:
        """Load rules from SACRED_RULES.xml"""
        if not self.rules_path.exists():
            print(f"Warning: Rules file not found: {self.rules_path}")
            return
        
        tree = ET.parse(self.rules_path)
        root = tree.getroot()
        
        for req in root.findall(".//requirement"):
            self.requirements.append(Requirement(
                id=req.get("id", "UNKNOWN"),
                text=req.findtext("text", ""),
                severity=Severity(req.get("severity", "warn")),
                tier=int(req.get("tier", 0)),
                anchor=req.findtext("anchor", "")
            ))
    
    def _load_session_rules(self) -> None:
        """Load user session rules"""
        session_path = Path(".agent/memory/session_rules.json")
        if session_path.exists():
            with open(session_path) as f:
                self.session_rules = json.load(f)
    
    def _register_builtin_checks(self) -> None:
        """Register built-in check functions for known rules"""
        checks = {
            "LANG_001": self._check_vietnamese,
            "MCP_001": self._check_mcp_tools,
            "EXEC_002": self._check_no_destructive,
        }
        
        for req in self.requirements:
            if req.id in checks:
                req.check_fn = checks[req.id]
    
    # ─────────────────────────────────────────────────────────────────────────
    # BUILT-IN CHECK FUNCTIONS
    # ─────────────────────────────────────────────────────────────────────────
    
    def _check_vietnamese(self, context: dict, response: str) -> bool:
        """Check if response contains Vietnamese characters"""
        vietnamese_pattern = r'[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]'
        return bool(re.search(vietnamese_pattern, response.lower()))
    
    def _check_mcp_tools(self, context: dict, response: str) -> bool:
        """Check that browser tool is NOT used"""
        browser_patterns = [
            r'\bbrowser_subagent\b',
            r'\bopen_browser\b',
            r'\bbrowser tool\b',
        ]
        for pattern in browser_patterns:
            if re.search(pattern, response, re.IGNORECASE):
                return False  # Violation: browser tool mentioned
        return True
    
    def _check_no_destructive(self, context: dict, response: str) -> bool:
        """Check for destructive actions without confirmation"""
        destructive_patterns = [
            r'\brm -rf\b',
            r'\bDELETE FROM\b',
            r'\bDROP TABLE\b',
            r'\bformat\s+[a-z]:\b',
        ]
        for pattern in destructive_patterns:
            if re.search(pattern, response, re.IGNORECASE):
                # Check if confirmation was requested
                if "confirm" not in response.lower():
                    return False
        return True
    
    # ─────────────────────────────────────────────────────────────────────────
    # PUBLIC API
    # ─────────────────────────────────────────────────────────────────────────
    
    def run_pre_check(self, context: dict) -> dict:
        """
        Run PRE-LLM validation.
        Called BEFORE sending prompt to model.
        
        Args:
            context: Current prompt context
            
        Returns:
            dict with 'blocking' and 'warnings' violations
        """
        blocking = []
        warnings = []
        
        for req in self.requirements:
            if not req.check(context, ""):
                violation = Violation(
                    requirement_id=req.id,
                    severity=req.severity,
                    message=req.text,
                    timestamp=datetime.now().isoformat()
                )
                
                if req.severity == Severity.BLOCK:
                    blocking.append(violation)
                else:
                    warnings.append(violation)
        
        return {"blocking": blocking, "warnings": warnings}
    
    def run_post_check(self, context: dict, response: str) -> list[Violation]:
        """
        Run POST-LLM validation.
        Called AFTER receiving response from model.
        
        Args:
            context: Current prompt context
            response: Model's response
            
        Returns:
            List of violations found
        """
        violations = []
        
        for req in self.requirements:
            if not req.check(context, response):
                violation = Violation(
                    requirement_id=req.id,
                    severity=req.severity,
                    message=f"Violated: {req.text}",
                    timestamp=datetime.now().isoformat(),
                    context_snippet=response[:200]
                )
                violations.append(violation)
                self.violations.append(violation)
        
        return violations
    
    def is_response_valid(self, context: dict, response: str) -> bool:
        """
        Quick check if response is valid (no blocking violations).
        
        Returns:
            True if response passes all block-severity rules
        """
        violations = self.run_post_check(context, response)
        blocking = [v for v in violations if v.severity == Severity.BLOCK]
        return len(blocking) == 0
    
    def get_active_rules_summary(self) -> str:
        """Get a summary of active rules for injection into context"""
        lines = ["=== ACTIVE RULES ==="]
        for req in self.requirements:
            if req.severity == Severity.BLOCK:
                lines.append(f"• {req.id}: {req.text[:50]}...")
        return "\n".join(lines)
    
    def save_violations_log(self, path: str = ".agent/memory/violations.json") -> None:
        """Save violations to log file"""
        log_path = Path(path)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            "last_updated": datetime.now().isoformat(),
            "total_violations": len(self.violations),
            "violations": [
                {
                    "id": v.requirement_id,
                    "severity": v.severity.value,
                    "message": v.message,
                    "timestamp": v.timestamp
                }
                for v in self.violations
            ]
        }
        
        with open(log_path, 'w') as f:
            json.dump(data, f, indent=2)


# ─────────────────────────────────────────────────────────────────────────────
# HOOK INTEGRATION HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def hook_before_prompt(prompt: str, context: dict) -> tuple[str, dict]:
    """
    Claude Code / Cursor pre-hook integration.
    Injects rules into prompt head and validates context.
    
    Usage in hooks config:
        beforeSubmitPrompt:
            command: python policy_engine.py hook_before "$PROMPT"
    """
    engine = PolicyEngine()
    
    # Check for blocking issues
    result = engine.run_pre_check(context)
    if result["blocking"]:
        raise ValueError(f"Blocked by policy: {result['blocking'][0].message}")
    
    # Inject rules summary at head
    rules_summary = engine.get_active_rules_summary()
    enhanced_prompt = f"{rules_summary}\n\n---\n\n{prompt}"
    
    return enhanced_prompt, context


def hook_after_response(response: str, context: dict) -> str:
    """
    Claude Code / Cursor post-hook integration.
    Validates response against rules.
    
    Usage in hooks config:
        afterResponse:
            command: python policy_engine.py hook_after "$RESPONSE"
    """
    engine = PolicyEngine()
    
    if not engine.is_response_valid(context, response):
        engine.save_violations_log()
        # Optionally flag response as invalid
        return f"⚠️ POLICY VIOLATION DETECTED\n\n{response}"
    
    return response


# ─────────────────────────────────────────────────────────────────────────────
# CLI INTERFACE
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: policy_engine.py [validate|summary|hook_before|hook_after]")
        sys.exit(1)
    
    command = sys.argv[1]
    engine = PolicyEngine()
    
    if command == "validate":
        # Validate a response from stdin
        response = sys.stdin.read()
        if engine.is_response_valid({}, response):
            print("✅ Response VALID")
            sys.exit(0)
        else:
            print("❌ Response INVALID - policy violations detected")
            sys.exit(1)
    
    elif command == "summary":
        # Print active rules summary
        print(engine.get_active_rules_summary())
    
    elif command == "hook_before":
        # Pre-hook: inject rules into prompt
        prompt = sys.argv[2] if len(sys.argv) > 2 else ""
        enhanced, _ = hook_before_prompt(prompt, {})
        print(enhanced)
    
    elif command == "hook_after":
        # Post-hook: validate response
        response = sys.argv[2] if len(sys.argv) > 2 else ""
        result = hook_after_response(response, {})
        print(result)
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
