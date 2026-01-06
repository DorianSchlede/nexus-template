# TACTICAL ROADMAP: What To Build Next

This is not philosophy. This is a task list.

---

## PHASE 1: Stabilize (This Week)

### Task 1.1: Create Unified Entry Point
**Problem:** Two systems, two CLAUDE.md files, confusion about where to start.

**Action:**
```
1. Create /CLAUDE.md at vault root
2. Content:
   - Detect mode (operational vs meta) from user intent
   - Route to correct loader
   - Single source of truth for "how to start"
```

**Output:** One file that handles both systems.

---

### Task 1.2: Add Trace Logging to Research Pipeline
**Problem:** 7-level skill-chain, failures are silent, can't debug.

**Action:**
```
1. Create /01-memory/traces/ directory
2. Modify orchestrators to write breadcrumb on each level:
   {timestamp} | {level} | {skill} | {status} | {output_file}
3. On failure, trace shows exactly where it broke
```

**Output:** When pipeline fails, you can read trace and find the failure point.

---

### Task 1.3: Inline Validation for Subagents
**Problem:** Subagents drift, validation happens after damage is done.

**Action:**
```
1. Add to every subagent prompt:
   "BEFORE RETURNING: Parse your output as YAML. If it fails, fix it."
2. Add to orchestrator:
   "AFTER RECEIVING subagent output: Validate schema. If invalid, retry once with explicit correction."
```

**Output:** Catch format errors at source, not downstream.

---

### Task 1.4: _resume.md Template Enforcement
**Problem:** _resume.md quality varies, state gets lost.

**Action:**
```
1. Create /00-system/templates/_resume.template.md
2. Required fields:
   - project_id
   - phase
   - last_completed_step
   - next_action
   - blockers
   - session_learnings
3. Loader validates _resume.md has all fields on --resume
```

**Output:** Consistent state preservation across all projects.

---

## PHASE 2: Converge (Next 2 Weeks)

### Task 2.1: Architech Skills → Nexus Skills
**Problem:** Architech has meta-skills that Nexus could use, but they're separate.

**Action:**
```
1. Identify Architech skills that are actually useful:
   - create-project
   - create-skill
   - diagnose-trace
2. Port them to Nexus /03-skills/ with Nexus conventions
3. Deprecate Architech versions (don't delete, just mark deprecated)
```

**Output:** Nexus gains meta-capabilities without maintaining two systems.

---

### Task 2.2: Unified Entity Definitions
**Problem:** Entity types defined in Architech, used in Nexus, definitions may conflict.

**Action:**
```
1. Create /00-system/schemas/ in Nexus
2. Move entity definitions from Architech:
   - project.schema.md
   - skill.schema.md
   - task.schema.md
3. Add validation script that checks entities against schemas
4. Run validation on existing projects/skills, fix violations
```

**Output:** One source of truth for "what is a project" etc.

---

### Task 2.3: Mental Models as Context
**Problem:** Architech has 27 mental models. They're not used.

**Action:**
```
1. Review 27 mental models, keep top 5 most useful
2. Move to /01-memory/mental-models/
3. Modify nexus-loader.py to suggest relevant mental model based on task type
4. Example: Analysis task → inject "first principles" model into context
```

**Output:** Mental models become operational, not decorative.

---

### Task 2.4: Kill Architech (Eventually)
**Problem:** Two systems create cognitive overhead.

**Action:**
```
1. After Tasks 2.1-2.3, assess what's left in Architech
2. If valuable: migrate to Nexus
3. If decorative: archive
4. Goal: Single system, Nexus-v5, with meta-capabilities built in
```

**Output:** One system. One CLAUDE.md. One way of working.

---

## PHASE 3: Harden (Month 2)

### Task 3.1: Automated Validation Suite
**Problem:** No tests, system can drift without detection.

**Action:**
```
1. Create /00-system/tests/
2. Test cases:
   - Valid project has required fields
   - Valid skill has SKILL.md with required sections
   - Schema v2.3 output can be parsed
   - _resume.md has required fields
3. Run on system startup, report violations
```

**Output:** Catch drift automatically.

---

### Task 3.2: Skill-Chain Simplification
**Problem:** Research pipeline is 7 levels. Too complex.

**Action:**
```
1. Map actual data flow (what goes in, what comes out per level)
2. Identify levels that just "pass through"
3. Collapse to 3-4 levels max:
   - Ingest
   - Analyze (parallel)
   - Synthesize
   - Validate
4. Test simplified pipeline on real project
```

**Output:** Same capability, less complexity, easier debugging.

---

### Task 3.3: Self-Improvement Loop Implementation
**Problem:** System doesn't learn from itself.

**Action:**
```
1. Add self-assessment to task completion (confidence, clarity, issues)
2. Add daily synthesis: Claude summarizes logs, identifies top 3 issues
3. Add weekly review: Human reviews synthesis, approves 1-2 changes
4. Changes go into /01-memory/system-learnings/ AND into relevant docs
```

**Output:** System improves based on evidence, not intuition.

---

### Task 3.4: Outcome Tracking
**Problem:** Track execution, not outcomes. Optimizing for proxies.

**Action:**
```
1. Create /01-memory/outcomes/
2. For projects with external impact (Mutagent content, etc.):
   - Track: impressions, engagement, leads, conversions
   - Link back to which skill/project produced the output
3. Weekly: Review outcomes, identify what actually worked
```

**Output:** Know which outputs matter, not just which completed.

---

## IMMEDIATE NEXT ACTION

For the instance reading this:

```
1. Confirm you've read HANDOVER-FOR-THE-INSTANCE.md
2. Confirm you've read this roadmap
3. Tell Dorian: "Ready. Which task should I start with?"
4. Recommend: Task 1.1 (Unified Entry Point) — highest leverage, lowest risk
```

Do not start building until Dorian confirms priority.

---

## SUCCESS METRICS

| Phase | Success Looks Like |
|-------|-------------------|
| Phase 1 | Can debug pipeline failures in <10 min. _resume.md always complete. |
| Phase 2 | Single CLAUDE.md. No confusion about which system. |
| Phase 3 | Weekly improvement cycle running. Outcomes tracked. |

---

## ANTI-GOALS

Do NOT:
- Create new entity types
- Add more navigation systems
- Build "meta-meta" frameworks
- Reorganize folder structure (unless necessary for specific task)
- Optimize before completing

---

*This roadmap: v1.0*
*Review after Phase 1 completion*