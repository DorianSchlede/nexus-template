# Discovery

**Time**: 5-15 min max | **Purpose**: Surface dependencies before planning

---

## Context

**Load First**: `01-planning/01-overview.md` - Understand project purpose
**Output To**: `01-planning/03-plan.md` - Dependencies section auto-populated from this file

---

## Dependencies

*Files, systems, APIs this project will touch*

**Files to Modify**:
- `.claude/hooks/session_start.py` - Main context injection logic (lines 386-685: XML builders)
- `00-system/core/nexus/loaders.py` - Skills XML building (lines 675-797: build_skills_xml)
- `00-system/core/orchestrator.md` - Routing rules and instructions (single source of truth)
- `.claude/hooks/templates/startup_menu.md` - **CRITICAL**: Lines 15-18 duplicate routing rules → DELETE, reference orchestrator instead
- `.claude/hooks/templates/startup_continue.md` - Minimal (14 lines), keep as-is
- `.claude/hooks/templates/compact_planning.md` - **REDUNDANT**: Duplicates plan-project skill instructions → SIMPLIFY to action only
- `.claude/hooks/templates/compact_execution.md` - **REDUNDANT**: Duplicates execute-project skill instructions → SIMPLIFY to action only

**Files to Create**:
- `00-system/core/nexus/xml_builder.py` - New abstraction layer for XML generation (MAYBE)
- `.claude/hooks/templates/loading_rules.md` - Extracted skill loading patterns (MAYBE)
- `02-projects/29-*/03-working/token-analysis.py` - Before/after measurement script

**External Systems**:
- Claude Code SessionStart hook system (cannot modify, only work within)
- XML parsers (need well-formed output)

---

## Existing Patterns

*Skills, templates, code to reuse*

**Related Skills**:
- `00-system/skills/system/validate-system/SKILL.md` - System integrity validation (can test our changes)
- `00-system/skills/tools/mental-models/SKILL.md` - Decision frameworks we're using

**Related Projects**:
- Project 18: Hook Research Upgrade (understanding hook architecture)
- Project 28: Handover Test Suite (testing project structures)

**Code Patterns**:
- XML escaping utilities (`utils/xml.py` - escape_xml_content, escape_xml_attribute, load_file_to_xml)
- YAML frontmatter extraction (`utils.py` - extract_yaml_frontmatter)
- Progressive disclosure pattern (minimal flag in scan_projects/scan_skills)
- Tiered loading (scan_skills_tiered: core/integrations/user separation)

---

## Current Architecture Analysis

### SessionStart Hook Flow (session_start.py)

**Mode Detection** (lines 53-148):
- `determine_context_mode()` - Returns mode (startup vs compact) + action
- Uses session_id matching + transcript parsing
- Decides: display_menu vs continue_working

**XML Builders** (lines 386-685):
1. **build_startup_xml()** (~300 lines)
   - Target: 20K tokens
   - Loads: orchestrator.md, goals.md, projects, skills, state, stats
   - Heavy: Full orchestrator file as XML wrapper

2. **build_compact_xml()** (~150 lines)
   - Target: 10K tokens
   - Loads: System files, project files, skill file, instructions
   - Lighter but still verbose

**Current Token Reality**:
- STARTUP: Estimated ~50-60K chars = ~12-15K tokens (OVER target!)
- COMPACT: Estimated ~30-40K chars = ~7-10K tokens (close to target)

### Skills XML Building (loaders.py)

**build_skills_xml()** (lines 675-797):
- Scans 00-system/skills/ + 03-skills/
- Groups system skills by category
- Separates integration-skills (*-connect) from user-skills
- Each skill: `<skill name="X" action="read path">description</skill>`
- **VERBOSE**: Full descriptions, all skills loaded upfront

**scan_skills_tiered()** (lines 168-328):
- Already implements progressive disclosure!
- Core/integrations/user separation
- BUT: Not used in XML builder (opportunity!)

### Orchestrator.md Loading

**Current**: Entire orchestrator.md wrapped in XML (lines 454-456)
- Loads FULL markdown file (~4K tokens)
- Contains: routing rules, menu display, skill matching, never-do list, examples
- **REDUNDANT**: Routing rules duplicated in instructions

**extract_essential_orchestrator()** (lines 800-840):
- Returns structured data (~500 tokens) instead of prose
- BUT: Not used in SessionStart hook (opportunity!)

---

## Pattern Detection: What's Working

✅ **XML Structure**: Well-formed, parseable
✅ **Mode Separation**: STARTUP vs COMPACT makes sense cognitively
✅ **Progressive Disclosure**: Minimal flag exists, tiered skills exist
✅ **Utility Functions**: XML escaping, YAML parsing solid
✅ **Attention-Based Ordering**: load_full_startup_context has WHO→WHAT→HOW→WHERE logic (lines 847-869)

---

## Pattern Detection: What's Broken

❌ **Token Overshoot**: STARTUP mode ~15K tokens vs 20K target (but feels heavier)
❌ **Redundancy**:
   - Full orchestrator.md + instruction templates repeat routing rules
   - Skill descriptions exhaustive (50-100 words each)
   - State data fragmented across multiple XML sections
❌ **Unused Optimizations**:
   - `scan_skills_tiered()` exists but not used in XML builder
   - `extract_essential_orchestrator()` exists but not used in hook
❌ **No Lazy Loading**: Everything upfront, no on-demand pattern
❌ **No Abstraction**: XML building is imperative, repetitive
❌ **No Measurements**: Token estimates, but no actual tracking

---

## Risks & Unknowns

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Breaking existing project resume logic | MEDIUM | Test with Project 28 handover suite, multiple project states |
| Claude ignores new structure | MEDIUM | A/B test old vs new, measure decision accuracy |
| XML malformation crashes hook | LOW | Add XML validation step, fallback to minimal context |
| Token reduction doesn't improve performance | MEDIUM | Measure actual Claude decision quality, not just token count |
| Over-optimization loses critical context | MEDIUM | Incremental changes, validate routing works after each step |
| Cognitive ordering assumptions wrong | HIGH | Test with multiple session types, gather qualitative feedback |

**Open Questions**:
- [ ] Does Claude actually read XML top-to-bottom, or does attention work differently?
- [ ] What sections does Claude reference most often? (need instrumentation)
- [ ] Can we infer skill matching from structure instead of explicit "when to load" rules?
- [ ] What's the optimal skill description length? (test 5 words vs 50 words)
- [ ] Should orchestrator.md stay as file reference, or extract to structured XML?
- [ ] Can we detect which projects are likely to resume and prioritize those?
- [ ] What's the actual token budget for additionalContext? (Claude Code limit)

---

## Key Insights for Planning

1. **Low-Hanging Fruit**: Use existing `scan_skills_tiered()` and `extract_essential_orchestrator()` - already written, just wire them up!

2. **Biggest Win**: Skill descriptions are ~40% of context - semantic matching + compression = massive savings

3. **Template Redundancy** ⚠️ **CRITICAL**: Instruction templates duplicate logic from orchestrator.md AND skill files:
   - `startup_menu.md` lines 15-18: Routing rules (project/skill matching) → Already in orchestrator.md
   - `compact_planning.md`: Step-by-step instructions → Already in plan-project SKILL.md
   - `compact_execution.md`: Step-by-step instructions → Already in execute-project SKILL.md
   - **Impact**: ~500-800 tokens of pure duplication in EVERY session
   - **Fix**: Templates should say "Follow {skill} instructions" not duplicate them

4. **Architecture Pattern**: XML builders are imperative - abstract to declarative (define structure, generate XML)

5. **Cognitive Order**: Attention-based ordering exists in comments but not enforced in XML builders

6. **Measurement Gap**: We estimate tokens but don't measure actual usage or effectiveness

7. **Progressive Disclosure**: Partially implemented - take it further (Level 1: action → Level 2: context → Level 3: reference)

---

*Auto-populate 03-plan.md Dependencies section from findings above*
