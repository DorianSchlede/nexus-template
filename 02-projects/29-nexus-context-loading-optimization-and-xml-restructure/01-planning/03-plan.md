# Nexus Context Loading Optimization and XML Restructure - Plan

**Last Updated**: 2026-01-06

---

## Context

**Load Before Reading**:
- `01-planning/01-overview.md` - Purpose and success criteria
- `01-planning/02-discovery.md` - Dependencies discovered

---

## Mental Models Applied

This plan uses FIVE mental models for comprehensive analysis:

1. **First Principles** - Strip assumptions, rebuild from fundamentals
2. **Pareto Analysis (80/20)** - Identify high-impact optimizations
3. **Systems Thinking** - Understand interdependencies and feedback loops
4. **Pre-Mortem Analysis** - Imagine failures before they happen
5. **A/B Testing Framework** - Measure before/after scientifically

---

## 1. FIRST PRINCIPLES: What Does Claude Actually Need?

### Fundamental Questions

**Q: Why do we inject context at all?**
A: Claude Code sessions are stateless. Each session needs: WHO (user identity/goals), WHAT (current work), HOW (behavior rules), WHERE (available tools/skills).

**Q: When does Claude need this information?**
A: **NOT all at once!** Different information needed at different decision points:
- **Startup**: WHO am I? WHAT should I do? → Goals + Menu
- **Routing**: WHERE should I go? → Skill triggers (semantic, not exhaustive)
- **Execution**: HOW do I do this? → Skill content (loaded on-demand)
- **Planning**: WHAT's the context? → Project files (loaded when needed)

**Q: What's the MINIMUM to make a decision?**
- Identity: User role/goals (100-200 tokens)
- Current state: Active projects (50-100 tokens)
- Action: What to do NOW (50 tokens)
- Routing hints: How to find skills (500-1000 tokens)

**Total minimum**: ~700-1350 tokens vs current 12-15K!

### Stripping Assumptions

**Assumption**: "Claude needs full orchestrator.md to understand routing"
**Reality**: Claude can infer from structure. If skills have `<category name="projects">`, Claude knows these are project-related.

**Assumption**: "Skill descriptions must be exhaustive to match user intent"
**Reality**: 1-2 trigger words + semantic matching works. "create project" vs "create proj

ect, new project, start project, plan project, begin project..."

**Assumption**: "All skills must be loaded upfront"
**Reality**: Progressive disclosure - load categories first, details on-demand.

**Assumption**: "XML must wrap full markdown content"
**Reality**: XML can be structured data that REFERENCES markdown files, not duplicate them.

---

## 2. PARETO ANALYSIS: The 20% That Drives 80% Impact

### Token Distribution Analysis (from discovery)

Current STARTUP context (~12-15K tokens):
- **Orchestrator.md**: ~4,000 tokens (27%)
- **Skill descriptions**: ~6,000 tokens (40%) ← **BIGGEST WIN**
- **Project metadata**: ~800 tokens (5%)
- **User goals**: ~400 tokens (3%)
- **State/stats**: ~200 tokens (1%)
- **Instructions**: ~1,500 tokens (10%)
- **XML structure**: ~2,100 tokens (14%)

### The Vital Few (20% of changes → 80% of gains)

**High-Impact Changes** (ranked by token savings × implementation ease):

1. **Compress Skill Descriptions** (40% of tokens)
   - Current: 50-100 words per skill
   - Target: 5-10 words + 1-2 trigger keywords
   - **Savings**: ~4,500 tokens (~30% total reduction)
   - **Ease**: EASY - just edit descriptions

2. **Reference Orchestrator, Don't Duplicate** (27% of tokens)
   - Current: Full orchestrator.md wrapped in XML
   - Target: Structured routing rules OR reference to file
   - **Savings**: ~3,500 tokens (~23% total reduction)
   - **Ease**: MEDIUM - use existing `extract_essential_orchestrator()`

3. **Consolidate Redundant Instructions** (10% of tokens)
   - Current: Routing rules in orchestrator + instructions + skill descriptions
   - Target: Single source of truth
   - **Savings**: ~1,000 tokens (~7% total reduction)
   - **Ease**: EASY - delete duplicates

**Combined Impact**: ~9,000 tokens saved (~60% reduction!) with EASY-MEDIUM effort.

### The Trivial Many (80% of changes → 20% of gains)

- XML attribute vs element optimization (~200 tokens, HARD to maintain)
- Project encoding compression (~300 tokens, breaks readability)
- Stats consolidation (~100 tokens, minimal impact)

**Skip these** - not worth complexity.

---

## 3. SYSTEMS THINKING: Interdependencies & Feedback Loops

### System Map

```
┌─────────────────────────────────────────────────────────────┐
│                     CLAUDE CODE                              │
│  (We cannot modify - black box with SessionStart hook API) │
└──────────────────┬──────────────────────────────────────────┘
                   │ SessionStart event
                   ▼
    ┌──────────────────────────────────────┐
    │    session_start.py (Hook)           │
    │  - determine_context_mode()          │
    │  - build_startup_xml() ◄─────┐      │
    │  - build_compact_xml()        │      │
    └───────┬──────────────────────┴──────┘
            │                       │
            │ calls                 │ calls
            ▼                       ▼
  ┌──────────────────┐    ┌────────────────────────┐
  │  nexus/loaders.py│    │  orchestrator.md       │
  │ - build_skills_  │    │  - Routing rules       │
  │   xml()          │    │  - Menu display        │
  │ - scan_skills_   │    │  - Skill matching      │
  │   tiered()       │    │  - Never-do list       │
  └──────────────────┘    └────────────────────────┘
            │
            │ generates
            ▼
  ┌────────────────────────────────────────┐
  │   additionalContext (XML string)       │
  │   Injected into Claude's context       │
  └───────────┬────────────────────────────┘
              │
              ▼
  ┌────────────────────────────────────────┐
  │         CLAUDE INSTANCE                │
  │  Reads context → Makes decisions       │
  │  - Display menu?                       │
  │  - Load skill?                         │
  │  - Resume project?                     │
  └───────────┬────────────────────────────┘
              │
              │ decision impacts
              ▼
  ┌────────────────────────────────────────┐
  │       USER EXPERIENCE                  │
  │  - Correct routing?                    │
  │  - Clear next actions?                 │
  │  - Fast startup?                       │
  └────────────────────────────────────────┘
```

### Feedback Loops

**Positive Loop** (virtuous cycle):
- Cleaner context → Faster Claude decisions → Better UX → More trust in system → More usage → More optimization opportunities

**Negative Loop** (vicious cycle):
- Too aggressive optimization → Missing context → Wrong routing → User confusion → Manual corrections → System distrust

**Balancing Loop** (stabilizing):
- Token reduction → Measure routing accuracy → If accuracy drops → Add context back → Find equilibrium

### Critical Dependencies

**Cascade Risk**: Changing skill descriptions affects:
1. Skill matching logic (semantic inference)
2. Menu display (user-facing text)
3. Onboarding suggestions (trigger keywords)
4. Integration detection (naming patterns)

**Tight Coupling**: orchestrator.md ↔ instruction templates ↔ skill descriptions
- Change one → Must validate all three

**Temporal Dependency**: SessionStart hook must complete <200ms
- Optimization that adds processing time defeats purpose

---

## 4. PRE-MORTEM ANALYSIS: How Could This Fail?

### Imagined Failure Scenarios (12 months from now)

**Scenario 1: "The Routing Apocalypse"**
- **Failure**: Claude can't match user requests to skills anymore
- **Root Cause**: Skill descriptions too compressed, lost semantic richness
- **Evidence**: Users typing "create project" → Claude responds "I don't know what you mean"
- **Prevention**:
  - Keep 1-2 full example phrases in each description
  - Test with 20+ varied user inputs per skill
  - A/B test current vs compressed descriptions

**Scenario 2: "The Menu Nightmare"**
- **Failure**: Startup menu is gibberish or missing critical sections
- **Root Cause**: Removed orchestrator.md, lost menu display instructions
- **Evidence**: Menu shows "undefined" or skips entire sections
- **Prevention**:
  - Keep menu template in instructions, not orchestrator
  - Test menu rendering in 5 different states (no projects, planning, execution, etc.)
  - Validate XML structure before output

**Scenario 3: "The Resume Black Hole"**
- **Failure**: Project resume completely broken, always goes to menu
- **Root Cause**: Changed mode detection logic, broke session_id matching
- **Evidence**: Users mid-project → Get startup menu instead of continuation
- **Prevention**:
  - DON'T touch `determine_context_mode()` logic
  - Test with Project 28 handover suite
  - Add logging to track mode decisions

**Scenario 4: "The Performance Paradox"**
- **Failure**: Hook takes 500ms, times out, falls back to minimal context
- **Root Cause**: Added XML validation + processing overhead
- **Evidence**: session_start_output.log shows >200ms execution time
- **Prevention**:
  - Profile every change with time.perf_counter()
  - Keep processing under 150ms (buffer for safety)
  - Lazy-load expensive operations (don't validate unless debug mode)

**Scenario 5: "The Cognitive Collapse"**
- **Failure**: Claude makes worse decisions despite fewer tokens
- **Root Cause**: Removed information Claude was silently using
- **Evidence**: Increased errors, wrong skill loading, confused responses
- **Prevention**:
  - Measure decision quality BEFORE optimizing
  - A/B test with real user interactions
  - Incremental rollout (10% of sessions → 50% → 100%)

**Scenario 6: "The Maintenance Maze"**
- **Failure**: Code becomes unmaintainable, future devs can't modify
- **Root Cause**: Over-abstraction, clever code that's hard to understand
- **Evidence**: Bug fixes take days, new skills can't be added
- **Prevention**:
  - Prefer explicit over clever
  - Document WHY decisions were made (this plan!)
  - Keep XML builders readable (no metaprogramming magic)

### Early Warning Signals

Monitor these metrics to catch failures early:
- **Routing accuracy**: % of user inputs matched to correct skill
- **Hook execution time**: Average ms (target <150ms)
- **Token count**: Startup vs Compact modes
- **Error rate**: Malformed XML, failed mode detection
- **User corrections**: How often users manually fix routing

---

## 5. A/B TESTING FRAMEWORK: Measuring Impact

### Hypothesis

**H1**: Reducing skill descriptions to 5-10 words will maintain routing accuracy while saving ~4,500 tokens.

**H2**: Referencing orchestrator.md instead of inlining will maintain behavior compliance while saving ~3,500 tokens.

**H3**: Cognitive ordering (action-first) will improve decision speed with no token change.

### Metrics to Track

**Primary Metrics** (success/failure):
- **Token Count**: Startup context size (chars → estimated tokens)
- **Routing Accuracy**: % of inputs correctly matched (manual validation)
- **Hook Performance**: Execution time in ms

**Secondary Metrics** (quality signals):
- **Decision Quality**: Claude's responses are appropriate for context
- **Error Rate**: XML malformation, missing sections
- **User Satisfaction**: Subjective feedback on experience

### Test Design

**Baseline Measurement** (Week 1):
1. Run 50 test sessions with current system
2. Record: tokens, execution time, routing decisions
3. Create "golden dataset" of expected behaviors

**A/B Split** (Week 2-3):
- **Group A** (Control): Current system
- **Group B** (Treatment): Optimized system
- Random 50/50 split per session
- Run 100 sessions each group

**Measurement Points**:
- Session startup (display_menu)
- Skill routing (user input → skill match)
- Project resume (compact mode)

**Success Criteria**:
- Token reduction ≥30% (Group B vs A)
- Routing accuracy ≥95% (same as Group A)
- Hook performance <200ms (same or better than A)
- Zero XML errors (strict requirement)

**Decision Rules**:
- If ALL criteria met → Roll out to 100%
- If 2/4 criteria met → Investigate, iterate
- If <2 criteria met → Rollback, rethink approach

---

## Approach: The 3-Wave Strategy

Based on mental models above, we'll optimize in THREE waves (Pareto-driven, risk-mitigated):

### Wave 1: Low-Hanging Fruit (Week 1) - 60% Token Reduction

**Changes**:
1. Compress skill descriptions (40% of tokens)
2. Use `extract_essential_orchestrator()` (27% of tokens)
3. Remove instruction template redundancy (10% of tokens)

**Implementation**:
- Edit skill YAML frontmatter descriptions
- Wire up existing `extract_essential_orchestrator()` in hook
- Consolidate routing rules to orchestrator only

**Risk**: LOW - Using existing patterns, minimal logic change
**Measurement**: Before/after token count, routing accuracy test

### Wave 2: Progressive Disclosure (Week 2) - Additional 15% Reduction

**Changes**:
1. Skill categories first, details on-demand
2. Lazy-load full orchestrator.md (reference in XML)
3. Consolidate state/stats into single section

**Implementation**:
- Modify `build_skills_xml()` to use tiered structure
- Add `<orchestrator-ref>` instead of full content
- Merge `<state>` and `<stats>` XML sections

**Risk**: MEDIUM - Changes XML structure, need validation
**Measurement**: Routing still works, menu renders correctly

### Wave 3: Cognitive Optimization (Week 3) - Performance Gain

**Changes**:
1. Enforce action-first ordering in XML
2. Add attention markers (CRITICAL, REFERENCE, etc.)
3. Test different cognitive flows

**Implementation**:
- Reorder XML sections in builders
- Add XML attributes for importance
- A/B test orderings

**Risk**: HIGH - Hypothesis-driven, may not work
**Measurement**: Decision speed, quality subjective tests

---

## Key Decisions

| Decision | Choice | Why |
|----------|--------|-----|
| **Wave Strategy** | 3 phases (fruit → disclosure → cognition) | Pareto: High-impact first, de-risk incrementally |
| **Skill Descriptions** | 5-10 words + 1-2 triggers | First principles: Minimum for semantic matching |
| **Orchestrator Loading** | Extract essential OR reference file | Systems thinking: Reduce duplication, single source of truth |
| **Testing Approach** | A/B with golden dataset | Pre-mortem: Catch failures early, measure scientifically |
| **XML Structure** | Keep current format, optimize content | Low risk: Don't break parsers or existing logic |
| **Mode Detection** | DON'T TOUCH | Pre-mortem: High coupling, high failure risk |
| **Performance Budget** | <150ms (buffer from 200ms target) | Systems thinking: Temporal constraint is hard limit |

---

## Dependencies & Links

*Auto-populated from 02-discovery.md*

**Files Impacted**:
- `.claude/hooks/session_start.py` - XML builders (lines 386-685)
- `00-system/core/nexus/loaders.py` - `build_skills_xml()` (lines 675-797)
- `00-system/core/orchestrator.md` - Routing rules consolidation
- `.claude/hooks/templates/*.md` - Remove redundant instructions
- `00-system/skills/**/SKILL.md` - Compress all skill descriptions

**External Systems**:
- Claude Code SessionStart hook API (read-only constraint)
- XML parsers (must maintain well-formed output)

**Related Projects**:
- Project 18: Hook Research Upgrade (context system understanding)
- Project 28: Handover Test Suite (testing infrastructure)

---

## Technical Architecture

**System Components**:
1. **Mode Detector** (`determine_context_mode`) - Unchanged, decides STARTUP vs COMPACT
2. **XML Builders** (`build_startup_xml`, `build_compact_xml`) - Refactored for efficiency
3. **Skill Scanner** (`build_skills_xml`) - Use tiered loading, compressed descriptions
4. **Orchestrator Extractor** (`extract_essential_orchestrator`) - Wire into hook (already exists!)
5. **Measurement Layer** - NEW - Token tracking, decision logging

**Data Flow**:
```
SessionStart event
  → determine_context_mode() [DON'T TOUCH]
  → IF startup:
      → build_startup_xml()
          → scan_skills_tiered() [REPLACE current build_skills_xml]
          → extract_essential_orchestrator() [REPLACE inline orchestrator.md]
          → load user goals
          → build state/stats (consolidated)
          → generate instructions (deduplicated)
      → Output: <nexus-context mode="startup"> ... </nexus-context>
  → IF compact:
      → build_compact_xml()
          → Load minimal project context
          → Reference skill file (not inline)
      → Output: <nexus-context mode="compact"> ... </nexus-context>
  → Log metrics (tokens, time, structure)
  → Return to Claude Code
```

**Technology Stack**:
- Python 3.11+ (existing)
- XML generation (xml.sax.saxutils.escape, existing utilities)
- YAML parsing (existing `extract_yaml_frontmatter`)
- Performance profiling (time.perf_counter, existing)

---

## Implementation Strategy

**Development Phases**:

### Phase 1: Measurement Baseline (Days 1-2)
1. Add token tracking to session_start.py
2. Run 50 test sessions, record metrics
3. Create golden dataset of routing behaviors
4. Document current performance

### Phase 2: Wave 1 - Quick Wins (Days 3-5)
1. Edit all skill descriptions (5-10 words each)
2. Wire `extract_essential_orchestrator()` into `build_startup_xml()`
3. Remove redundant routing rules from instruction templates
4. Test with golden dataset
5. Measure: token reduction, routing accuracy

### Phase 3: Wave 2 - Progressive Disclosure (Days 6-8)
1. Modify `build_skills_xml()` to use tiered structure
2. Replace inline orchestrator with reference or structured extract
3. Consolidate state/stats sections
4. Test menu rendering in 5 states
5. Measure: token reduction, XML validity

### Phase 4: Wave 3 - Cognitive Optimization (Days 9-10)
1. Reorder XML sections (action-first)
2. Add importance attributes
3. A/B test different orderings
4. Measure: decision quality (subjective)

### Phase 5: Validation & Rollout (Days 11-12)
1. Run Project 28 handover test suite
2. Test project resume in multiple states
3. Validate hook performance <150ms
4. Document changes
5. Deploy to production

**Testing Approach**:
- **Unit Tests**: XML well-formedness, token counting
- **Integration Tests**: Mode detection → XML generation → Claude routing
- **Regression Tests**: Golden dataset (50 sessions) must pass
- **Performance Tests**: Hook execution time profiling
- **Manual Tests**: Menu display, skill loading, project resume

**Deployment Plan**:
- **Staged Rollout**: 10% sessions → 50% → 100% (monitor metrics at each stage)
- **Rollback Plan**: Git branch per wave, easy revert
- **Monitoring**: Log all mode decisions, token counts, errors for 1 week post-deploy

---

## Open Questions

From discovery, prioritized by decision impact:

**HIGH PRIORITY** (answer in Phase 1):
- [ ] What's the actual token budget for additionalContext? (Test Claude Code limit)
- [ ] What's optimal skill description length? (Test 5 vs 10 vs 50 words with routing accuracy)

**MEDIUM PRIORITY** (answer in Phase 2):
- [ ] Does Claude read XML top-to-bottom or random access? (Test with ordering experiments)
- [ ] Can we detect which projects likely to resume? (Analyze session patterns)

**LOW PRIORITY** (answer in Phase 3, optional):
- [ ] What sections does Claude reference most? (Would need instrumentation Claude doesn't expose)
- [ ] Can we infer skill matching from structure alone? (Experimental, risky)

**DEFER** (interesting but not blocking):
- [ ] Should orchestrator.md be split into multiple files? (Scope creep, separate project)

---

## Risk Mitigation Summary

**From Pre-Mortem**:
1. Routing failures → Keep 1-2 example phrases, test extensively
2. Menu breaks → Separate template, validate in 5 states
3. Resume broken → DON'T touch mode detection, use handover suite
4. Performance regression → Profile every change, <150ms budget
5. Worse decisions → Baseline measurement, A/B testing, incremental rollout
6. Unmaintainable code → Document WHY, prefer explicit over clever

**Kill Switches**:
- Wave 1 fails → Rollback, re-evaluate approach
- Wave 2 fails → Keep Wave 1 wins, defer progressive disclosure
- Wave 3 fails → Keep Wave 1+2, cognitive optimization is optional

---

*Next: Break down execution in 04-steps.md*
