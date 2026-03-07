# Step 2: Scope Contract

> Display options, wait for user selection. ⛔ STOP.

## Display to User

```
🔬 Audit Pro — Scope Selection

Project: {name} ({type})
Active Experts: {list}
Weight Profile: {profile}

Select scope (1-10):
 1. full          — All experts, all checkpoints
 2. security      — Security expert only
 3. architecture  — Architecture expert only
 4. performance   — Performance expert only
 5. quality       — Quality expert only
 6. devops        — DevOps expert only
 7. quick         — Security + Architecture only
 8. desktop       — Core 5 + Desktop supplement
 9. cli           — Core 5 + CLI supplement
 10. diff         — Changed files only (last 5 commits)

Previous audit score: {score or "none"}
```

## Rules
- ⛔ STOP here and WAIT for user input
- Do NOT proceed without user selection
- After selection → load only relevant checklists (token optimization)
