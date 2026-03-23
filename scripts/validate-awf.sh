#!/usr/bin/env bash
# =============================================================================
# validate-awf.sh — DOMYH AWF Consistency Validator
# =============================================================================
# Checks:
#   1. INDEX.yaml ↔ SKILL.md on-disk consistency (no orphans)
#   2. Workflows: success_criteria present in frontmatter
#   3. Workflows: skills field present in frontmatter
#   4. Core workflows: RULES section present
#   5. REFLECTION CHECKPOINT in save.md + think.md
# =============================================================================

set +e

AWF_ROOT="${1:-.}"
SKILLS_DIR="$AWF_ROOT/.agent/skills"
WORKFLOWS_DIR="$AWF_ROOT/.agent/workflows"
INDEX_FILE="$SKILLS_DIR/INDEX.yaml"
ERRORS=0
WARNINGS=0

# Colors
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}═══════════════════════════════════════════════${NC}"
echo -e "${CYAN} DOMYH AWF Consistency Validator${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════${NC}"
echo ""

# ─────────────────────────────────────────────
# Check 1: INDEX.yaml ↔ SKILL.md consistency
# ─────────────────────────────────────────────
echo -e "${CYAN}[1/5] INDEX.yaml ↔ SKILL.md consistency${NC}"

SKILL_COUNT_DISK=$(find "$SKILLS_DIR" -name "SKILL.md" -type f | wc -l | tr -d ' ')
SKILL_COUNT_INDEX=$(grep -c "path:" "$INDEX_FILE" 2>/dev/null || echo "0")

if [ "$SKILL_COUNT_DISK" -eq "$SKILL_COUNT_INDEX" ]; then
    echo -e "  ${GREEN}✅ Match: $SKILL_COUNT_DISK skills on disk = $SKILL_COUNT_INDEX in INDEX.yaml${NC}"
else
    echo -e "  ${RED}❌ MISMATCH: $SKILL_COUNT_DISK on disk vs $SKILL_COUNT_INDEX in INDEX.yaml${NC}"
    ((ERRORS++))

    # Find orphans (on disk but not in INDEX)
    while IFS= read -r skill_path; do
        skill_name=$(echo "$skill_path" | sed "s|$SKILLS_DIR/||" | sed 's|/SKILL.md||')
        if ! grep -q "path: \"$skill_name\"" "$INDEX_FILE" 2>/dev/null; then
            echo -e "    ${RED}→ Orphan: $skill_name (on disk, not in INDEX)${NC}"
        fi
    done < <(find "$SKILLS_DIR" -name "SKILL.md" -type f)

    # Find ghosts (in INDEX but not on disk)
    while IFS= read -r indexed_path; do
        if [ ! -f "$SKILLS_DIR/$indexed_path/SKILL.md" ]; then
            echo -e "    ${RED}→ Ghost: $indexed_path (in INDEX, not on disk)${NC}"
        fi
    done < <(grep 'path:' "$INDEX_FILE" | sed 's/.*path: "//;s/".*//')
fi

echo ""

# ─────────────────────────────────────────────
# Check 2: success_criteria in workflow frontmatters
# ─────────────────────────────────────────────
echo -e "${CYAN}[2/5] Workflow success_criteria coverage${NC}"

TOTAL_WF=0
MISSING_SC=0
for wf in "$WORKFLOWS_DIR"/*.md; do
    ((TOTAL_WF++))
    wf_name=$(basename "$wf")
    if ! grep -q "success_criteria" "$wf" 2>/dev/null; then
        echo -e "  ${YELLOW}⚠️ Missing success_criteria: $wf_name${NC}"
        ((MISSING_SC++))
        ((WARNINGS++))
    fi
done

if [ "$MISSING_SC" -eq 0 ]; then
    echo -e "  ${GREEN}✅ All $TOTAL_WF workflows have success_criteria${NC}"
else
    echo -e "  ${YELLOW}⚠️ $MISSING_SC/$TOTAL_WF workflows missing success_criteria${NC}"
fi

echo ""

# ─────────────────────────────────────────────
# Check 3: skills field in workflow frontmatters
# ─────────────────────────────────────────────
echo -e "${CYAN}[3/5] Workflow skills field coverage${NC}"

MISSING_SKILLS=0
for wf in "$WORKFLOWS_DIR"/*.md; do
    wf_name=$(basename "$wf")
    if ! grep -q "^skills:" "$wf" 2>/dev/null; then
        echo -e "  ${YELLOW}⚠️ Missing skills field: $wf_name${NC}"
        ((MISSING_SKILLS++))
        ((WARNINGS++))
    fi
done

if [ "$MISSING_SKILLS" -eq 0 ]; then
    echo -e "  ${GREEN}✅ All $TOTAL_WF workflows have skills field${NC}"
else
    echo -e "  ${YELLOW}⚠️ $MISSING_SKILLS/$TOTAL_WF workflows missing skills field${NC}"
fi

echo ""

# ─────────────────────────────────────────────
# Check 4: RULES section in core workflows
# ─────────────────────────────────────────────
echo -e "${CYAN}[4/5] RULES sections in core workflows${NC}"

CORE_WORKFLOWS=("code.md" "modify.md" "debug.md" "fix.md" "review.md")
MISSING_RULES=0
for wf_name in "${CORE_WORKFLOWS[@]}"; do
    wf="$WORKFLOWS_DIR/$wf_name"
    if [ -f "$wf" ]; then
        if ! grep -q "RULES (Always Apply)" "$wf" 2>/dev/null; then
            echo -e "  ${RED}❌ Missing RULES section: $wf_name${NC}"
            ((MISSING_RULES++))
            ((ERRORS++))
        fi
    else
        echo -e "  ${RED}❌ File not found: $wf_name${NC}"
        ((ERRORS++))
    fi
done

if [ "$MISSING_RULES" -eq 0 ]; then
    echo -e "  ${GREEN}✅ All ${#CORE_WORKFLOWS[@]} core workflows have RULES sections${NC}"
fi

echo ""

# ─────────────────────────────────────────────
# Check 5: REFLECTION CHECKPOINT in key workflows
# ─────────────────────────────────────────────
echo -e "${CYAN}[5/5] REFLECTION CHECKPOINT in key workflows${NC}"

REFLECTION_WORKFLOWS=("code.md" "modify.md" "debug.md" "review.md" "save.md" "think.md")
MISSING_REFLECT=0
for wf_name in "${REFLECTION_WORKFLOWS[@]}"; do
    wf="$WORKFLOWS_DIR/$wf_name"
    if [ -f "$wf" ]; then
        if ! grep -qi "REFLECTION" "$wf" 2>/dev/null; then
            echo -e "  ${YELLOW}⚠️ Missing REFLECTION: $wf_name${NC}"
            ((MISSING_REFLECT++))
            ((WARNINGS++))
        fi
    fi
done

if [ "$MISSING_REFLECT" -eq 0 ]; then
    echo -e "  ${GREEN}✅ All ${#REFLECTION_WORKFLOWS[@]} key workflows have REFLECTION section${NC}"
fi

echo ""

# ─────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────
echo -e "${CYAN}═══════════════════════════════════════════════${NC}"
if [ "$ERRORS" -eq 0 ] && [ "$WARNINGS" -eq 0 ]; then
    echo -e "${GREEN}✅ ALL CHECKS PASSED — $TOTAL_WF workflows, $SKILL_COUNT_DISK skills${NC}"
    exit 0
elif [ "$ERRORS" -eq 0 ]; then
    echo -e "${YELLOW}⚠️ $WARNINGS warning(s), 0 errors — $TOTAL_WF workflows, $SKILL_COUNT_DISK skills${NC}"
    exit 0
else
    echo -e "${RED}❌ $ERRORS error(s), $WARNINGS warning(s) — FIX REQUIRED${NC}"
    exit 1
fi
