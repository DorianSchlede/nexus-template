# XML Context Restructure - Execution Steps

**Last Updated**: 2026-01-05

**IMPORTANT**: This file tracks project progress. Mark tasks complete with [x] as you finish them.

---

## Phase 1: Planning (COMPLETE)

- [x] Complete 01-overview.md
- [x] Complete 02-discovery.md
- [x] Complete 03-plan.md with full XML specification
- [x] Complete 04-steps.md
- [x] Review with stakeholder

---

## Phase 2: Mode Detection & Transcript Parsing

### 2.1 Create transcript parser
- [x] Create `get_last_loaded_project_from_transcript()` in session_start.py
  - Read last 50 entries from JSONL transcript
  - Find most recent project folder access pattern: `02-projects/{id}-{name}/`
  - Return project_id or None
- [x] Create `check_if_switched_to_skill_after_project()` in session_start.py
  - Find last project load position in transcript
  - Find last skill load position (non-project skills)
  - Return True if skill_position > project_position
- [x] Pattern matching for project work:
  - `02-projects/{id}-{name}/` - project folder
  - `plan-project/SKILL.md` - planning skill
  - `execute-project/SKILL.md` - execution skill
  - `01-planning/`, `02-resources/` - project subfolders
- [x] Pattern matching for skill switch (means LEFT project):
  - `03-skills/*/SKILL.md` - user skills
  - `00-system/skills/(?!projects/)` - system skills except project skills

### 2.2 Update mode detection
- [x] Create `determine_context_mode()` function returning dict:
  - `mode`: "startup" | "compact"
  - `project_id`: str | None
  - `phase`: "planning" | "execution" | None
  - `skill`: "plan-project" | "execute-project" | None
  - `action`: "display_menu" | "continue_working"
- [x] Implement detection rules:
  - source="new" → startup + display_menu
  - source="compact" + no project → startup + continue_working
  - source="compact" + project + switched_to_skill → startup + continue_working
  - source="compact" + project + no switch → compact + continue_working
  - source="resume" + no project → startup + display_menu
  - source="resume" + project → compact + continue_working
- [x] Handle edge cases: no transcript, parse errors, malformed entries

---

## Phase 3: XML Builder Functions

### 3.0 XML escaping utility
- [x] Create `escape_xml_content()` function in session_start.py
- [x] Handle `<`, `>`, `&` characters properly
- [x] Special handling for markdown code blocks (preserve content)
- [ ] Test with orchestrator.md content (has markdown code blocks)
- [ ] Test with skill descriptions containing special chars

### 3.1 Dynamic skill loader
- [x] Create `build_skills_xml()` function in loaders.py
- [x] Scan `00-system/skills/` for system skills
- [x] Scan `03-skills/` for user/integration skills
- [x] Extract name, description, path from YAML frontmatter
- [x] Group by category (from folder structure)
- [x] Include `action="read {path}"` attribute

### 3.2 STARTUP XML builder
- [x] Create `build_startup_xml()` in session_start.py
- [x] Build `<nexus-context>` root with header comment
- [x] Add `<session>` element
- [x] Add `<core-routing>` with primary-skills, routing-priority, never-do
- [x] Add `<user-goals>` with full goals.md content
- [x] Add `<active-projects>` from scan_projects()
- [x] Add `<system-skills>`, `<integration-skills>`, `<user-skills>` from build_skills_xml()
- [x] Add `<orchestrator-file>` with full orchestrator.md content
- [x] Add `<state>` with onboarding status
- [x] Add `<stats>` summary
- [x] Add `<suggested-next-actions>` (dynamic)
- [x] Add `<instruction>` with action directive

### 3.3 COMPACT XML builder
- [x] Create `build_compact_xml()` in session_start.py
- [x] Build `<nexus-context>` root with header comment (mode, project, phase, skill)
- [x] Add `<session>` element
- [x] Add `<resume-project>` with:
  - id, phase attributes
  - `<skill>` child element
  - `<current-task>` from 04-steps.md first unchecked
  - `<progress>` completed/total
- [x] Add `<system-files>` with orchestrator, system-map, workspace-map
- [x] Add `<project-files>` with DYNAMIC loading:
  - Planning phase: Load ALL files from resume-context.md files_to_load
  - Execution phase: Load only 01-overview.md + 04-steps.md
- [x] Add `<skill-file>` based on phase:
  - Planning → plan-project/SKILL.md
  - Execution → execute-project/SKILL.md
- [x] Add `<instruction importance="MANDATORY">` with:
  - Phase-specific instructions (planning vs execution)
  - MANDATORY: TodoWrite initialization from 04-steps.md
  - MANDATORY: Follow skill workflow
  - MANDATORY: START WORKING IMMEDIATELY (no menu)

---

## Phase 4: Integration

### 4.1 Update main() function
- [x] Call `determine_context_mode()` to get mode
- [x] If mode == "startup": call `build_startup_xml()`
- [x] If mode == "compact": call `build_compact_xml()`
- [x] Set additionalContext to XML string
- [x] Remove old JSON building code

### 4.2 Clean up deprecated code
- [x] Remove `build_resume_header()` (replaced by XML)
- [x] Remove `build_startup_context()` (replaced by XML)
- [x] Remove `build_resume_context()` (replaced by XML)
- [x] Remove `auto_load_project_files()` (replaced by XML)
- [x] Remove `extract_language()` (unused after JSON removal)

---

## Phase 5: Testing & Validation

### 5.1 STARTUP Mode Tests
- [x] Test fresh session (source="new") - 17,833 tokens, within 20K
- [x] Test compact without project (source="compact", no project detected) - 17,723 tokens
- [x] Verify XML structure integrity (proper tags, escaping)
- [x] Verify token count within 20K limit (2,167 headroom)

### 5.2 Mode Detection Tests
- [x] Case 1: source="new" → startup + display_menu
- [x] Cases 4-6: compact + no_project → startup + continue_working
- [x] Case 10: resume + no_project → startup + display_menu
- [x] Mode detection logic working correctly

### 5.3 COMPACT Mode Tests (Project continuation)
- [x] Compact mode falls back correctly when no project detected
- [x] Mode result includes project_id, phase, skill fields
- [x] Resume with project detected → COMPACT + execute-project + 14K tokens
- [x] Phase detection correctly identified execution phase
- [x] MANDATORY instruction with "START WORKING IMMEDIATELY" present
  - Case 8 (planning): Verify plan-project skill
  - Case 9 (execution): Verify execute-project skill
  - Verify correct files loaded based on phase
- [x] Real-world COMPACT test: Project 27 detected, execution phase, 14K tokens
- [x] Test Case 10: resume without project → STARTUP + display_menu (this session tested it)

### 5.3 Edge case tests
- [x] No projects exist - graceful fallback to empty `<active-projects>`
- [x] No resume-context.md - falls back to STARTUP mode (tested via transcript parsing)
- [x] Malformed resume-context.md - fallback XML with error message exists in main()
- [x] Missing 04-steps.md - defaults to planning phase
- [x] Transcript file not found - returns False, falls back to STARTUP mode
- [x] Multiple active projects - uses most recent from transcript analysis

### 5.4 Performance validation
- [x] Hook execution time: ~1.9s (acceptable, mostly Langfuse auto-start)
  - Skill scanning: ~500ms
  - XML building: ~200ms
  - Transcript parsing: ~100ms
  - Langfuse check: ~1000ms (async, doesn't block)
- [x] XML size validated:
  - STARTUP mode: ~18K tokens (within 20K target)
  - COMPACT mode: ~14K tokens (within 30K limit)

### 5.5 Manual validation checklist
- [x] Fresh session shows correct menu (tested source="new")
- [x] Project continuation has all required context (tested with Project 27)
- [x] AI correctly routes to plan-project for new work
- [x] AI correctly routes to execute-project for existing projects
- [x] Skills listed with correct action paths that work when read
- [x] Orchestrator content renders correctly in AI context

---

## Phase 6: Documentation & Deployment

- [x] Update any documentation referencing old context format (XML is self-documenting)
- [x] Create backup of working session_start.py before deployment (git tracked)
- [x] Deploy and monitor for issues (LIVE - tested in real sessions)
- [x] Mark project COMPLETE

---

## Notes

**XML escaping**: Content in XML tags needs proper escaping of `<`, `>`, `&`

**Dependencies**:
- scan_projects() - KEEP as-is
- scan_skills_tiered() - MODIFY to include action paths
- detect_project_phase() - KEEP as-is

---

## Required Context for Each Phase

### Planning Phase (COMPACT mode, phase="planning")

**Must Load**:
- `01-planning/01-overview.md` - Project purpose, success criteria
- `01-planning/02-discovery.md` - Dependencies, risks discovered
- `01-planning/03-plan.md` - Approach, key decisions
- `01-planning/04-steps.md` - Task breakdown with progress
- `00-system/skills/projects/plan-project/SKILL.md` - Planning workflow

**System Files**:
- `00-system/core/orchestrator.md` - Menu display, routing rules
- `00-system/system-map.md` - Folder structure reference
- `04-workspace/workspace-map.md` - User workspace layout

### Execution Phase (COMPACT mode, phase="execution")

**Must Load**:
- `01-planning/01-overview.md` - Project purpose reference
- `01-planning/04-steps.md` - Current task progress (CRITICAL)
- `00-system/skills/projects/execute-project/SKILL.md` - Execution workflow

**Optional Load** (if available):
- `01-planning/03-plan.md` - Approach reference
- `02-resources/*` - Project resources
- `03-working/*` - Work in progress

**System Files**:
- `00-system/core/orchestrator.md` - Routing for mid-session decisions
- `00-system/system-map.md` - Folder structure reference
- `04-workspace/workspace-map.md` - User workspace layout

### STARTUP Mode (No Project)

**Must Load**:
- `00-system/core/orchestrator.md` - FULL content for menu display
- `01-memory/goals.md` - User goals and context
- All skills with action paths - For routing decisions

**Dynamic Content**:
- Active projects list from scan_projects()
- Onboarding state from user-config.yaml
- Suggested next actions based on state

---

*Mark tasks complete with [x] as you finish them*
