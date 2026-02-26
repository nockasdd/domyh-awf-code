# 🧩 LEVEL 5: DECOMPOSE — Isolate through systematic elimination

## MINIMAL REPRODUCTION
1. Copy function → separate test file
2. Hardcode inputs → run → pass/fail?
   - PASS → bug is in CONTEXT not logic
   - FAIL → bug is IN the function
3. Add complexity incrementally: +DB → +middleware → +auth → which breaks it?
4. DoVer: hypothesis → minimal change → re-verify

## BINARY SEARCH
1. Identify full data path (input → output)
2. Add log/breakpoint at MIDPOINT
3. Data correct at mid? → bug in second half. Data wrong? → first half
4. Repeat until narrowed to ≤5 lines

## COMPONENT ISOLATION (parallel)

| Component Off | Result | Conclusion |
|---------------|--------|------------|
| Auth          |        |            |
| Cache         |        |            |
| Middleware    |        |            |
| External APIs |        |            |
| Database      |        |            |
