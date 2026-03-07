# Step 1: Discovery

> Detect project type, stack, and auto-activate experts.

## Prompt

1. Call `hsa_detect(stack)` — identify languages, frameworks, **project type**
2. Call `hsa_explore(snapshot)` — count files, understand structure
3. Determine project type:
   - electron/tauri deps → Desktop App
   - commander/yargs/clap → CLI Tool
   - publishConfig/exports → Library/SDK
   - react-native/flutter → Mobile App
   - @modelcontextprotocol → MCP Plugin
   - default → Web Application
4. Auto-activate conditional experts based on detection:
   - UI files (.vue/.tsx/.jsx) → UX expert
   - Database config → Data expert
   - k8s/terraform/docker → Cloud expert
   - AI/ML deps → AI-Safety expert
5. Check for recent changes: `git diff --name-only HEAD~5..HEAD`
6. List active experts + supplementary checklists detected

## Output
```
Active experts: [list]
Supplementary: [if any]
Project type: [type]
Weight profile: [profile]
Files scanned: [count]
Recent commits: [count]
```
