# Nexus Loader Optimization Plan

> **STATUS: PARTIALLY IMPLEMENTED** - MVC pattern already added to loaders.py!

---

## ALREADY IMPLEMENTED: MVC Pattern in loaders.py

**Discovery**: Lines 668-923 in `loaders.py` already contain slim generators!

| Function | Purpose | Token Target |
|----------|---------|--------------|
| `extract_essential_orchestrator()` | Strip ASCII banner, keep rules | ~3.5K |
| `generate_project_index_slim()` | id, name, status, progress% only | ~40/project |
| `generate_skill_categories()` | Categories instead of 100 skills | ~500 |
| `generate_slim_startup()` | Full slim startup bundle | ~6K total |
| `generate_slim_resume()` | Even slimmer for resume | ~2K total |

**Current vs Implemented**:
| Metric | Current Cache | MVC Startup | MVC Resume |
|--------|---------------|-------------|------------|
| Target | 82KB / 20K tokens | ~6K tokens | ~2K tokens |
| Reduction | - | 70% | 90% |

### What's Actually Happening

**TWO PARALLEL IMPLEMENTATIONS EXIST:**

| Location | Functions | Status |
|----------|-----------|--------|
| `loaders.py` | `generate_slim_startup()` / `generate_slim_resume()` | **NOT USED** |
| `session_start.py` | `build_startup_context()` / `build_resume_context()` | **ACTUALLY USED** |

**session_start.py (MVC v3.2)** has its own inline implementation:
- Zero dependencies on loaders.py
- Much smaller context (~1K tokens)
- Has **25K test padding hardcoded** at line 193!

**loaders.py** functions are orphaned - implemented but never called.

### Decisions Needed

- [ ] Remove duplicate `loaders.py` slim functions? (orphaned code)
- [ ] Or wire `loaders.py` functions into `session_start.py`?
- [ ] Remove the 25K test padding from production hook?
- [ ] Which implementation is better for routing accuracy?

---

## PROPOSAL: Cache Size Reduction (Original Analysis)

### Measured Baseline (2025-12-31)

```
Total cache: 82,111 chars (20,527 tokens)
```

### Cache Breakdown by Section

| Section | Chars | Tokens | % | Priority |
|---------|-------|--------|---|----------|
| metadata_skills | 40,599 | 10,149 | 49.4% | **P0** |
| memory_total | 25,301 | 6,325 | 30.8% | **P1** |
| ├─ orchestrator.md | 12,023 | 3,005 | 14.6% | P1 |
| ├─ system-map.md | 3,714 | 928 | 4.5% | P2 |
| ├─ memory-map.md | 2,168 | 542 | 2.6% | P2 |
| ├─ user-config.yaml | 1,560 | 390 | 1.9% | Keep |
| └─ goals.md | 1,087 | 271 | 1.3% | Keep |
| metadata_projects | 10,331 | 2,582 | 12.6% | **P1** |
| stats | 1,489 | 372 | 1.8% | Keep |
| instructions (x2) | 956 | 238 | 1.2% | P3 |

### Counts
- Projects: 17
- Skills: 100

### Proposed Changes

| Change | Savings | Risk |
|--------|---------|------|
| P0: Truncate skill descriptions to 50 chars | 30KB | Medium - routing may degrade |
| P1a: Replace orchestrator.md with summary | 11KB | High - AI behavior may change |
| P1b: Slim project metadata | 6KB | Low |
| P2: Remove system-map.md, memory-map.md | 6KB | Medium |
| P3: Slim attention sandwich | 0.5KB | Low |
| **TOTAL** | **53KB (65%)** | - |

### Expected Results

| Metric | Before | After | Reduction |
|--------|--------|-------|-----------|
| Cache size | 82KB | ~29KB | 65% |
| Tokens | 20,527 | ~7,250 | 65% |
| % of context window | 10.3% | 3.6% | - |

---

## CROSS-INVESTIGATION REQUIRED

Before implementing, review these related projects for conflicts/synergies:

### Project 14: Advanced Hook System

**Relevance**: SessionStart hook outputs context to Claude. Changes here affect hook output.

**Files to Review**:
- [ ] `.claude/hooks/session_start.py` - Current SLIM POINTER pattern
- [ ] `02-projects/14-advanced-hook-system/01-planning/steps.md` - Hook research notes
- [ ] `02-projects/14-advanced-hook-system/_resume.md` - Current status

**Questions**:
1. Does SessionStart hook depend on specific metadata fields we're removing?
2. Will the SLIM POINTER pattern still work with reduced cache?
3. Should hook output format change to match new cache structure?

### Project 17: Hook Pattern Research

**Relevance**: Researching patterns across 9 repos. May find context-loading patterns.

**Files to Review**:
- [ ] `02-projects/17-hook-pattern-research/01-planning/plan.md` - Research plan
- [ ] `02-projects/17-hook-pattern-research/02-resources/_briefing.md` - Extraction schema
- [ ] Pattern files when extracted (Wave 1 outputs)

**Questions**:
1. What context-loading patterns exist in other repos?
2. How do other systems handle large context injection?
3. Are there lazy-loading patterns we should adopt?

### Hook Repos to Examine

Based on Project 17's corpus, examine these for context optimization patterns:

| Repo | Path | What to Look For |
|------|------|------------------|
| hooks-mastery | `04-workspace/00-ai-native-org/hook-repos/claude-code-hooks-mastery/` | SessionStart patterns |
| safety-net | `04-workspace/00-ai-native-org/hook-repos/claude-code-safety-net/` | Context size patterns |
| cc-tools | `04-workspace/00-ai-native-org/hook-repos/claude-code-tools/` | Context injection |

---

## PLAN: Investigation Steps

### Phase 1: Cross-Project Review

- [ ] Read Project 14 session_start.py hook implementation
- [ ] Read Project 14 steps.md for hook output research
- [ ] Read Project 17 _briefing.md extraction schema
- [ ] Search hook-repos for "context" or "startup" patterns
- [ ] Document findings in `02-resources/cross-investigation.md`

### Phase 2: Pattern Research

- [ ] Grep hook-repos for SessionStart implementations
- [ ] Identify how other projects handle large context
- [ ] Document best practices from community
- [ ] Update proposal based on findings

### Phase 3: Prototype

- [ ] Create branch for optimization changes
- [ ] Implement P0 (skills truncation) only
- [ ] Measure new cache size
- [ ] Test SessionStart hook still works
- [ ] Document results

### Phase 4: Full Implementation (if prototype succeeds)

- [ ] Implement remaining changes (P1a, P1b, P2, P3)
- [ ] Update Project 14 hooks if needed
- [ ] Full regression testing
- [ ] Update ARCHITECTURE.md

---

## DETAILED PROPOSALS

### P0: Skills Metadata (49% of cache) → Target 75% reduction

**Problem**: 100 skills × ~400 chars each = 40KB

**Current structure**:
```json
{
  "name": "airtable-master",
  "description": "Shared resource library for Airtable integration skills. DO NOT load directly - provides common references (setup, API docs, error handling, field types) and scripts used by airtable-connect, airtable-query, and airtable-sync.",
  "_file_path": "C:\\Users\\dsber\\...\\SKILL.md"
}
```

**Proposed structure**:
```json
{
  "name": "airtable-master",
  "desc": "Airtable shared resources"
}
```

**Changes**:
1. Truncate `description` to 50 chars max → rename to `desc`
2. Remove `_file_path` (derivable from name)
3. Consider grouping by category (airtable/*, notion/*, etc.)

**Savings**: 40KB → 10KB = **30KB saved**

**File**: `loaders.py` → `scan_skills()`

**Risk Assessment**:
- Skill routing uses description for keyword matching
- Need to verify 50 chars is sufficient for trigger words
- May need to add `triggers` field instead of relying on description

---

### P1a: Don't Embed orchestrator.md (14.6%)

**Problem**: 12KB embedded on every startup, rarely read in full

**Proposed solution**: Replace with 500-char summary of key rules

**Summary to embed instead**:
```
## Nexus Rules (Summary)
- Display menu on startup (header + goals + projects + actions)
- Route to skills based on triggers in metadata
- Use TodoWrite for multi-step tasks
- Update _resume.md before context compaction
- Load project/skill via nexus-loader.py before working
- Read full orchestrator.md: 00-system/core/orchestrator.md
```

**Savings**: 12KB → 0.5KB = **11.5KB saved**

**File**: `config.py` → `MANDATORY_MAPS` or `service.py` → `startup()`

**Risk Assessment**:
- **HIGH RISK**: AI behavior rules live in orchestrator.md
- Need to ensure summary captures critical routing logic
- May need AI to always Read() orchestrator.md on startup

---

### P1b: Projects Metadata (12.6%) → Target 60% reduction

**Problem**: 17 projects × ~600 chars each = 10KB

**Current structure**:
```json
{
  "id": "14-advanced-hook-system",
  "name": "Advanced Hook System",
  "description": "Comprehensive Claude Code hooks for context injection, safety, and session management",
  "status": "IN_PROGRESS",
  "onboarding": false,
  "created": "2025-12-30",
  "updated": null,
  "progress": 0.538,
  "tasks_total": 13,
  "tasks_completed": 7,
  "current_task": "Test fresh session and resume scenarios",
  "_file_path": "C:\\Users\\dsber\\...\\overview.md"
}
```

**Proposed structure**:
```json
{
  "id": "14-advanced-hook-system",
  "name": "Advanced Hook System",
  "status": "IN_PROGRESS",
  "progress": 0.54,
  "current_task": "Test fresh session and resume scenarios"
}
```

**Changes**:
1. Remove `description` (read from overview.md if needed)
2. Remove `_file_path` (derivable from id)
3. Remove `onboarding`, `created`, `updated` (rarely used)
4. Remove `tasks_total`, `tasks_completed` (derivable from progress)
5. Only include `current_task` for IN_PROGRESS projects
6. Round `progress` to 2 decimal places

**Savings**: 10KB → 4KB = **6KB saved**

**File**: `loaders.py` → `scan_projects()`

---

### P2: Don't Embed system-map.md & memory-map.md (7.1%)

**Problem**: 6KB embedded, AI can read on demand

**Proposed solution**: Remove from `MANDATORY_MAPS`, provide path in instructions

**Savings**: 6KB → 0KB = **6KB saved**

**File**: `config.py` → `MANDATORY_MAPS`

---

### P3: Attention Sandwich Optimization (1.2%)

**Problem**: Instructions duplicated at START and END (956 chars total)

**Proposed solution**:
- Keep full instructions at END only (recency effect is stronger)
- At START: just `{"action": "...", "project_id": "..."}`

**Savings**: 0.5KB (minor)

**File**: `service.py` → `startup()`

---

## Implementation Order (After Investigation)

```mermaid
flowchart LR
    INV[Investigation] --> P0[P0: Skills 30KB]
    P0 --> TEST[Test Hooks]
    TEST --> P1a[P1a: Orchestrator 11KB]
    P1a --> P1b[P1b: Projects 6KB]
    P1b --> P2[P2: Maps 6KB]
    P2 --> P3[P3: Instructions 0.5KB]
```

---

## Files to Modify (Pending Investigation)

| File | Proposed Changes |
|------|------------------|
| `loaders.py` | Truncate skill desc, slim project metadata |
| `config.py` | Remove system-map.md, memory-map.md from MANDATORY_MAPS |
| `service.py` | Orchestrator summary, slim attention sandwich |
| `.claude/hooks/session_start.py` | May need updates for new cache format |

---

## Risks

1. **Breaking changes**: Skills/projects code might depend on removed fields
   - Mitigation: Grep for `_file_path`, `description` usage before removing

2. **AI behavior**: Less context might confuse routing
   - Mitigation: Ensure skill names + truncated desc are sufficient for matching

3. **Orchestrator summary**: AI might miss important rules
   - Mitigation: Include "Read full file at X" instruction prominently

4. **Hook compatibility**: SessionStart hook may depend on cache structure
   - Mitigation: Review Project 14 hooks before changing

---

## Validation Plan

After each change:
1. Run `python nexus-loader.py --startup`
2. Measure cache size
3. Test skill loading: `python nexus-loader.py --skill execute-project`
4. Test project loading: `python nexus-loader.py --project 14`
5. Start fresh Claude session and verify context injection works
6. Verify no errors in SessionStart hook

---

## Open Questions

- [ ] What patterns do hook-repos use for context loading?
- [ ] Does Project 14 hook depend on specific cache fields?
- [ ] Should we add a `triggers` field to skills instead of relying on description?
- [ ] Is 50 chars enough for skill descriptions to enable routing?
- [ ] Should orchestrator.md always be Read() on startup instead of embedded?
