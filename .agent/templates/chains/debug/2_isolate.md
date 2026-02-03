# Debug Chain — Step 2: Isolate

> Prompt chaining step for debugging process

---

## Context

Based on reproduction data, isolate the problem area.

## Input

```yaml
{ { reproduction } }
```

## Task

### 1. Narrow Down Location

Use binary search approach:

- Start broad, narrow systematically
- Eliminate working areas
- Focus on suspicious areas

### 2. Identify Scope

- Single function or multiple?
- Single file or cross-cutting?
- Data issue or logic issue?

### 3. Find Minimal Case

- What's the smallest input that fails?
- Can you simplify the scenario?
- What's the difference between working and failing?

## Output Format

```yaml
isolation:
  scope:
    primary_file: "file:line_range"
    related_files:
      - "file1:relevance"
      - "file2:relevance"

  narrowed_location:
    function: "[function name]"
    file: "[file path]"
    line_range: "start-end"

  issue_type: "[logic|data|state|timing|external]"

  minimal_case:
    input: "[Minimal input that fails]"
    steps: "[Minimal steps to reproduce]"

  difference_analysis:
    working: "[What works]"
    failing: "[What fails]"
    difference: "[Key difference]"

  suspected_causes:
    - "[Possible cause 1]"
    - "[Possible cause 2]"
    - "[Possible cause 3]"
```

---

_Chain Step 2 of 5 • Input: reproduction • Output: isolation_
