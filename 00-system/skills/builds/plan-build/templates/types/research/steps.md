# {{build_name}} - Execution Steps

**Build Type**: Research
**Status**: Planning

---

## Context Requirements

**Build Location**: `02-builds/{{build_id}}/`

**Files to Load for Execution**:
- `01-planning/02-discovery.md` - Research question and papers
- `02-resources/_briefing.md` - Extraction schema

**Output Location**: `04-outputs/`

---

## Phase 1: Planning & Acquisition (via create-research-build)

**Goal**: Define research and acquire papers
**Skill**: create-research-build

- [ ] Define research question
- [ ] Generate extraction schema
- [ ] Search academic APIs
- [ ] Review abstracts
- [ ] User approves paper selection
- [ ] Download papers
- [ ] Preprocess PDFs to markdown
- [ ] Generate analysis kit
- [ ] **CHECKPOINT**: Papers ready for analysis

---

## Phase 2: Analysis (via analyze-research-build)

**Goal**: Extract data from papers
**Skill**: analyze-research-build

- [ ] Validate readiness
- [ ] Spawn analysis subagents
- [ ] Analyze each paper
- [ ] Validate analysis logs
- [ ] **CHECKPOINT**: Analysis complete

---

## Phase 3: Synthesis (via synthesize-research-build)

**Goal**: Generate synthesis report
**Skill**: synthesize-research-build

- [ ] Build synthesis routing
- [ ] Calculate subagent allocation
- [ ] Generate prompts
- [ ] Run extraction subagents
- [ ] Verify output
- [ ] Aggregate patterns
- [ ] Generate synthesis report
- [ ] **CHECKPOINT**: Report ready

---

## Phase 4: Finalization

**Goal**: Complete build
**Context**: Synthesis complete

- [ ] Review synthesis report
- [ ] Update resume-context.md: current_phase: "complete"
- [ ] Update 01-overview.md success criteria checkboxes

---

## Summary

| Phase | Tasks | Checkpoints |
|-------|-------|-------------|
| Phase 1 | 9 | 1 |
| Phase 2 | 5 | 1 |
| Phase 3 | 8 | 1 |
| Phase 4 | 3 | 0 |
| **Total** | **25** | **3** |

---

*Mark tasks complete with [x] as you finish them*
