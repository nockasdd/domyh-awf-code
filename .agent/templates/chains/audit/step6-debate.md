# Step 6: Debate Round

> Expert panel discusses systemic findings. Only triggered if Systemic-Critical found.

## Trigger Condition

IF holistic synthesis found any `Systemic-Critical` finding → run debate.
IF only Systemic-Warning or Observation → skip to step 7.

## Debate Protocol

For EACH systemic finding:

1. **Moderator** (agent) presents the finding
2. **Each relevant expert responds**:
   - **FOR**: "This is a real problem because..."
   - **AGAINST**: "This is acceptable because..."
   - **CONDITION**: "This is fine IF [condition], dangerous IF [condition]"
3. **Moderator synthesizes**:
   - **CONFIRMED**: Multiple experts agree → keep severity
   - **DOWNGRADED**: Strong counter-arguments → lower severity
   - **CONDITIONAL**: Depends on context → specify conditions

## Example

```
Finding: "No rate limiting on any API endpoint"
Security:     FOR — critical, allows DoS
Architecture: CONDITION — fine for internal microservice, critical for public API
Performance:  FOR — will cause cascading failures under load
DevOps:       AGAINST — reverse proxy handles rate limiting externally
Verdict:      CONDITIONAL — verify reverse proxy config exists
              → if yes: P2, if no: P0
```
