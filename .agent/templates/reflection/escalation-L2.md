# 🪞 LEVEL 2: REFLECT — Analyze WHY current approach failed

1. **LIST** all attempts tried:

| # | Approach | File:Line | Result | Why it failed |
|---|----------|-----------|--------|---------------|

2. **FIND PATTERNS** in failures:
   - All fail at same spot? → Bug is upstream
   - Different failure each time? → Multiple bugs / race condition
   - Fixing 1 bug creates another? → Tight coupling issue

3. **CHECK COGNITIVE BIASES**:
   - □ Confirmation: "Am I only seeking evidence supporting my hypothesis?" → List 3 COUNTER-evidence pieces
   - □ Anchoring: "Is my first hypothesis still dominant?" → Generate 2 NEW hypotheses, rank by evidence
   - □ Tunnel Vision: "Have I checked beyond the code?" → code ✓ config ✓ env ✓ deps ✓ data ✓ logs ✓

4. **SAVE** episodic memory entry
