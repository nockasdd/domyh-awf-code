# 🔍 LEVEL 4: WIDEN — Expand scope BEYOND current area

## UPSTREAM/DOWNSTREAM
- Trace ALL callers: is the data passed in correct?
- Trace ALL callees: are return values handled?
- Do middleware/interceptors/hooks affect the flow?

## DIFF FORENSICS
- `git log --oneline -20 -- [affected_files]`
- `git diff HEAD~5 -- [affected_files]`
- When did it last work? Which commit changed it?

## ENVIRONMENTAL AUDIT
- Runtime version, ENV vars, port conflicts
- Dependencies compatible? Lock file stale?
- Config conflict? Feature flags? API keys?
- External services available? Response format changed?

## CONTRACT VERIFICATION
- Function input types match caller output?
- API request format match spec?
- DB model match actual table schema?
- Event payload match subscriber expectation?
