# XML Context Restructure - Plan

**Last Updated**: 2026-01-05

---

## Approach

Replace all JSON/markdown context injection with semantic XML. Two distinct modes:

1. **STARTUP** - Fresh session OR non-project continuation
2. **COMPACT** - Project continuation after auto-summary

Key principle: **Project-first workflow** - AI should always suggest planning a project before doing work.

---

## Key Decisions

| Decision | Choice | Why |
|----------|--------|-----|
| Format | XML with semantic tags | Better structure than JSON, no escaping issues |
| Mode detection | Parse transcript for compact | Accurate detection of project work |
| Skill loading | Dynamic from filesystem | Always up-to-date |
| Orchestrator | Full file content in startup | Needed for menu display |
| Routing priority | Learning → Skill → Project → Plan → Integration | Project-first workflow |
| Skill auto-load | Embed SKILL.md when suggesting | AI has full instructions |

---

## Dependencies & Links

**Files Impacted**:
- `.claude/hooks/session_start.py` - Main context builder
- `00-system/core/nexus/loaders.py` - Data loading functions
- `00-system/core/nexus/state.py` - State detection

**External Systems**:
- Claude Code hook system (additionalContext field)
- Transcript files (`~/.claude/projects/*/*.jsonl`)

**Related Projects**:
- Project 28: Context Deduplication (completed - foundation work)

---

## XML Specification

### STARTUP MODE

```xml
<nexus-context version="v4" mode="startup">
<!--
================================================================================
NEXUS OPERATING SYSTEM - PRIMARY CONTEXT INJECTION
================================================================================
This is the HYPER IMPORTANT primary working mode of Claude Code operating
inside the NEXUS system. All routing decisions, skill loading, and project
management flows through this context.

MODE: startup (fresh session or non-project continuation)
================================================================================
-->

  <session id="{uuid}" source="{new|compact|resume}" timestamp="{iso}"/>

  <orchestrator-file path="00-system/core/orchestrator.md">
    <!-- Full orchestrator.md content for menu display and behavior rules -->
    {orchestrator_content}
  </orchestrator-file>

  <core-routing importance="CRITICAL">
    <!--
    PRIMARY DECISION RULES - Read these first!
    These 3 skills handle 90% of user work.
    -->
    <primary-skills>
      <skill name="plan-project" priority="HIGH">
        <trigger>User wants to START something NEW with a deliverable</trigger>
        <trigger>User describes a task/goal without referencing existing project</trigger>
        <trigger>User says: "I want to...", "Help me...", "Can you...", "Let's..."</trigger>
        <trigger>User asks AI to do substantial work (not just questions)</trigger>
        <action>ALWAYS suggest creating a project first, then load plan-project/SKILL.md</action>
      </skill>
      <skill name="execute-project" priority="HIGH">
        <trigger>User references EXISTING project by name, ID, or number</trigger>
        <trigger>User says: "continue", "resume", "work on [project]"</trigger>
        <action>Load project context and execute-project/SKILL.md</action>
      </skill>
      <skill name="create-skill" priority="MEDIUM">
        <trigger>User wants to AUTOMATE repeating work</trigger>
        <trigger>User describes doing something "every time", "always", "repeatedly"</trigger>
        <action>Load create-skill/SKILL.md</action>
      </skill>
      <skill name="mental-models" priority="MEDIUM">
        <trigger>User needs to make a decision or analyze options</trigger>
        <trigger>User is stuck, uncertain, or weighing tradeoffs</trigger>
        <trigger>User says: "help me think", "what should I consider", "pros and cons"</trigger>
        <trigger>Planning phase of any project (proactively suggest)</trigger>
        <action>Load mental-models/SKILL.md, suggest 2-3 relevant frameworks</action>
        <proactive-suggest>
          <when>During plan-project Phase 6 (03-plan.md)</when>
          <when>User presents multiple options without clear winner</when>
          <when>High-stakes decision detected</when>
        </proactive-suggest>
      </skill>
    </primary-skills>

    <routing-priority>
      <rule priority="1">If onboarding incomplete → suggest learning skill (with action)</rule>
      <rule priority="2">Skill trigger keyword → load matched skill SKILL.md</rule>
      <rule priority="3">Project reference (name/ID/number) → execute-project</rule>
      <rule priority="4">New task without project → SUGGEST plan-project (load SKILL.md)</rule>
      <rule priority="5">Decision/analysis needed → SUGGEST mental-models (proactively during planning)</rule>
      <rule priority="6">Integration keyword → load {name}-connect skill</rule>
      <rule priority="7">No match → respond naturally, consider if this should be a project</rule>
    </routing-priority>

    <never-do importance="CRITICAL">
      <rule>Never create PROJECTS without loading plan-project/SKILL.md first</rule>
      <rule>Never create SKILLS without loading create-skill/SKILL.md first</rule>
      <rule>Never create folders directly → always use skills</rule>
      <rule>Never auto-load learning skills → suggest with action, let user decide</rule>
      <rule>Never read project files directly → use execute-project skill</rule>
      <rule>Never start substantial work without a project → suggest plan-project</rule>
    </never-do>

    <always-do importance="CRITICAL">
      <rule>ALWAYS work inside projects for substantial work</rule>
      <rule>ALWAYS suggest plan-project before starting new work</rule>
      <rule>ALWAYS load skill SKILL.md before executing skill workflows</rule>
      <rule>ALWAYS check 04-steps.md for current progress when resuming</rule>
    </always-do>

    <mode-rules>
      <rule mode="planning">Project status=PLANNING: Discuss approach, fill templates</rule>
      <rule mode="execution">Project status=IN_PROGRESS: Follow steps.md checkboxes</rule>
    </mode-rules>
  </core-routing>

  <user-goals>
    <!-- Full content of 01-memory/goals.md -->
    {goals_content}
  </user-goals>

  <active-projects>
    <!-- ALL projects with status IN_PROGRESS or PLANNING -->
    <!-- DYNAMICALLY CONSTRUCTED from scan_projects() -->
    <project id="{id}" status="{status}" progress="{percent}">
      <name>{name}</name>
      <current-task>{task}</current-task>
    </project>
    <!-- ... more projects ... -->
  </active-projects>

  <system-skills location="00-system/skills/">
    <!-- DYNAMICALLY CONSTRUCTED from filesystem scan -->
    <category name="projects">
      <skill name="plan-project" action="read 00-system/skills/projects/plan-project/SKILL.md">
        {description}
      </skill>
      <skill name="execute-project" action="read 00-system/skills/projects/execute-project/SKILL.md">
        {description}
      </skill>
      <!-- ... more skills ... -->
    </category>
    <category name="learning">
      <skill name="learn-nexus" action="read 00-system/skills/learning/learn-nexus/SKILL.md">
        {description}
      </skill>
      <!-- ... more skills ... -->
    </category>
    <category name="system">
      <!-- ... -->
    </category>
    <category name="tools">
      <!-- ... -->
    </category>
    <category name="skill-dev">
      <!-- ... -->
    </category>
  </system-skills>

  <integration-skills location="03-skills/*-connect/">
    <!-- DYNAMICALLY CONSTRUCTED from filesystem scan -->
    <skill name="airtable-connect" action="read 03-skills/airtable/airtable-connect/SKILL.md">
      {description}
    </skill>
    <!-- ... more integrations ... -->
  </integration-skills>

  <user-skills location="03-skills/">
    <!-- DYNAMICALLY CONSTRUCTED from filesystem scan (non-connect skills) -->
    <skill name="paper-search" action="read 03-skills/research-pipeline/paper-search/SKILL.md">
      {description}
    </skill>
    <!-- ... more user skills ... -->
  </user-skills>

  <state>
    <goals-personalized>{true|false}</goals-personalized>
    <workspace-configured>{true|false}</workspace-configured>
    <onboarding-complete>{true|false}</onboarding-complete>
    <pending-onboarding>
      <!-- Only if onboarding incomplete -->
      <item action="read 00-system/skills/learning/learn-projects/SKILL.md">learn-projects (8-10 min)</item>
      <item action="read 00-system/skills/learning/learn-skills/SKILL.md">learn-skills (10-12 min)</item>
      <item action="read 00-system/skills/learning/learn-integrations/SKILL.md">learn-integrations (10-12 min)</item>
      <item action="read 00-system/skills/learning/learn-nexus/SKILL.md">learn-nexus (15-18 min)</item>
    </pending-onboarding>
  </state>

  <stats projects="{total}" active="{active}" skills="{count}"/>

  <action>display_menu</action>

  <suggested-next-actions>
    <!-- Dynamic based on state -->
    <action priority="1" condition="has_active_projects">Continue active project: "work on {project-name}"</action>
    <action priority="2" condition="always">Start new work: "plan a project to [goal]"</action>
    <action priority="3" condition="onboarding_incomplete">Complete onboarding: "{pending_skill}" ({time})</action>
    <action priority="4" condition="always">Check status: "show my projects"</action>
  </suggested-next-actions>

  <instruction importance="MANDATORY">
    ================================================================================
    MANDATORY: STARTUP SEQUENCE
    ================================================================================

    STEP 1 - MANDATORY: Display Nexus menu
    - Show ASCII banner
    - Show active projects with progress
    - Show suggested next actions

    STEP 2 - MANDATORY: Adjust suggestions based on state
    - If onboarding_incomplete → Prioritize: "Complete {pending_skill} to unlock full potential"
    - If has_active_projects → Prioritize: "Continue {project_name} at {progress}%"
    - If no_projects → Prioritize: "Start your first project: 'plan a project to [goal]'"

    STEP 3 - MANDATORY: Route user input correctly
    - New work request → ALWAYS suggest plan-project first, then load skill
    - Project reference → Load execute-project skill
    - Skill trigger → Load matched skill

    ================================================================================
    Wait for user input after displaying menu.
    ================================================================================
  </instruction>

</nexus-context>
```

### STARTUP MODE - Continue Working (Cases 4-6)

When `compact` session but user was NOT working on a project (skill work or chat):

```xml
<instruction importance="MANDATORY">
  ================================================================================
  MANDATORY: CONTINUE SESSION (NO PROJECT CONTEXT)
  ================================================================================

  Previous session was compacted. User was NOT working on a project.

  DO NOT display menu.
  DO NOT ask "how can I help?"

  Continue naturally from where conversation left off.
  If user starts new work → suggest plan-project skill.

  ================================================================================
</instruction>
```

### COMPACT MODE (Project Continuation)

```xml
<nexus-context version="v4" mode="compact">
<!--
================================================================================
NEXUS OPERATING SYSTEM - PROJECT CONTINUATION CONTEXT
================================================================================
This is the HYPER IMPORTANT project continuation mode of Claude Code operating
inside the NEXUS system. User was actively working on a project in the previous
session - load full context and continue.

MODE: compact (continuing project work after auto-summary)
PROJECT: {project_id}
PHASE: {planning|execution}
SKILL: {plan-project|execute-project}
================================================================================
-->

  <session id="{uuid}" source="compact" timestamp="{iso}"/>

  <resume-project id="{project_id}" phase="{planning|execution}">
    <skill>{plan-project|execute-project}</skill>
    <current-task>{first unchecked task from 04-steps.md}</current-task>
    <progress>{completed}/{total} tasks</progress>
  </resume-project>

  <system-files>
    <file path="00-system/core/orchestrator.md">
      {orchestrator_content}
    </file>
    <file path="00-system/system-map.md">
      {system_map_content}
    </file>
    <file path="04-workspace/workspace-map.md">
      {workspace_map_content}
    </file>
  </system-files>

  <project-files project-id="{project_id}">
    <!-- DYNAMIC: Load from resume-context.md files_to_load -->
    <!-- Planning phase: ALL files (overview, discovery, plan, steps) -->
    <!-- Execution phase: overview + steps only -->
    <file path="{path_from_files_to_load}">
      {content}
    </file>
    <!-- ... more files based on phase ... -->
  </project-files>

  <skill-file path="00-system/skills/projects/{skill}/SKILL.md">
    <!-- plan-project/SKILL.md for planning phase -->
    <!-- execute-project/SKILL.md for execution phase -->
    {skill_content}
  </skill-file>

  <action>continue_working</action>

  <instruction importance="MANDATORY">
    ================================================================================
    MANDATORY INITIALIZATION SEQUENCE
    ================================================================================

    You are resuming project: {project_id}
    Phase: {planning|execution}

    STEP 1 - MANDATORY: Create TodoWrite immediately
    - Parse 04-steps.md for current phase tasks
    - Add all unchecked [ ] items to todo list
    - Mark current task as in_progress

    STEP 2 - MANDATORY: Follow skill instructions
    - Planning phase → Follow plan-project/SKILL.md workflow
    - Execution phase → Follow execute-project/SKILL.md workflow

    STEP 3 - MANDATORY: Continue from current task
    - First unchecked task: {current_task}
    - DO NOT skip tasks, DO NOT re-read files already loaded above

    ================================================================================
    DO NOT display menu. DO NOT ask what to do. START WORKING IMMEDIATELY.
    ================================================================================
  </instruction>

</nexus-context>
```

### COMPACT MODE - Planning Phase Instruction

```xml
<instruction importance="MANDATORY">
  ================================================================================
  MANDATORY: PROJECT PLANNING CONTINUATION
  ================================================================================

  Project: {project_id}
  Phase: PLANNING (Phase 1 incomplete)

  STEP 1 - MANDATORY: Initialize TodoWrite
  - Read 04-steps.md Phase 1 tasks
  - Create todo list with all unchecked planning tasks
  - Mark first unchecked task as in_progress

  STEP 2 - MANDATORY: Follow plan-project skill
  - Complete planning documents: overview → discovery → plan → steps
  - Use mental models for key decisions (suggest if appropriate)
  - Pause for user confirmation at each document

  STEP 3 - MANDATORY: Update progress
  - Mark tasks [x] as completed in 04-steps.md
  - Update resume-context.md with current state

  ================================================================================
  DO NOT start implementation until ALL Phase 1 tasks are [x] complete.
  DO NOT display menu. START on current planning task immediately.
  ================================================================================
</instruction>
```

### COMPACT MODE - Execution Phase Instruction

```xml
<instruction importance="MANDATORY">
  ================================================================================
  MANDATORY: PROJECT EXECUTION CONTINUATION
  ================================================================================

  Project: {project_id}
  Phase: EXECUTION (Phase 1 complete, implementing)

  STEP 1 - MANDATORY: Initialize TodoWrite
  - Read 04-steps.md for current execution phase
  - Find first unchecked [ ] task
  - Create todo list with remaining tasks
  - Mark current task as in_progress

  STEP 2 - MANDATORY: Follow execute-project skill
  - Work on ONE task at a time
  - Mark [x] complete immediately when done
  - Move to next unchecked task

  STEP 3 - MANDATORY: Track progress
  - Update 04-steps.md checkboxes as you complete
  - Update resume-context.md with significant progress

  ================================================================================
  Current task: {first_unchecked_task}
  DO NOT display menu. START on this task immediately.
  ================================================================================
</instruction>
```

---

## Implementation Strategy

### Phase 1: Mode Detection Logic

```python
def determine_context_mode(source: str, transcript_path: str, active_project_id: str) -> str:
    """
    Determine which context mode to use.

    Returns: "startup" | "compact"
    """
    # Fresh session - always startup
    if source == "new":
        return "startup"

    # Compact - check if was working on project
    if source == "compact":
        if not active_project_id:
            return "startup"

        was_working_on_project = check_transcript_for_project_work(transcript_path, active_project_id)
        return "compact" if was_working_on_project else "startup"

    # Resume - user explicitly resumed, assume project work
    if source == "resume":
        return "compact" if active_project_id else "startup"

    return "startup"


def check_transcript_for_project_work(transcript_path: str, project_id: str) -> bool:
    """
    Analyze transcript to determine if user was planning/executing a project.

    Reads last 50 entries, looks for:
    - "plan-project" or "execute-project" mentions
    - Project file paths (01-planning/, 02-resources/)
    - Project ID references
    """
    import json
    from pathlib import Path

    transcript = Path(transcript_path)
    if not transcript.exists():
        return False

    try:
        lines = transcript.read_text().strip().split('\n')
        last_entries = lines[-50:] if len(lines) > 50 else lines

        project_patterns = [
            "plan-project",
            "execute-project",
            f"{project_id}",
            "01-planning/",
            "02-resources/",
            "03-working/",
            "04-outputs/",
        ]

        for line in last_entries:
            try:
                entry = json.loads(line)
                content = str(entry)
                if any(pattern in content for pattern in project_patterns):
                    return True
            except:
                continue

        return False
    except:
        return False
```

### Phase 2: XML Builder Functions

```python
def build_startup_xml(project_dir: str) -> str:
    """Build complete STARTUP mode XML context."""
    # ... implementation
    pass

def build_compact_xml(project_dir: str, project_id: str, phase: str) -> str:
    """Build complete COMPACT mode XML context."""
    # ... implementation
    pass

def build_skills_xml(project_dir: str) -> str:
    """Dynamically construct skills XML from filesystem."""
    # ... implementation
    pass
```

### Phase 3: Integration

- Replace JSON output in session_start.py main()
- Update loaders.py to return XML-compatible structures
- Test all edge cases

---

## Mode Detection Cases

### Variables
- **Session source**: `new` | `compact` | `resume`
- **Last loaded project**: project_id from transcript | none
- **Previous activity**: project planning | project execution | skill work | chat
- **Project phase**: planning (Phase 1 incomplete) | execution (Phase 1 complete)

### All Cases

| # | Source | Last Project | Activity | Phase | Mode | Skill | Action |
|---|--------|--------------|----------|-------|------|-------|--------|
| 1 | `new` | - | - | - | STARTUP | none | Display menu (suggestions based on onboarding state) |
| 2 | `compact` | Project X | project planning | planning | COMPACT | plan-project | Continue planning, load files_to_load |
| 3 | `compact` | Project X | project execution | execution | COMPACT | execute-project | Continue execution, load 01-overview + 04-steps |
| 4 | `compact` | Project X | skill work after | - | STARTUP | none | Continue working (no menu) |
| 5 | `compact` | none | skill work | - | STARTUP | none | Continue working (no menu) |
| 6 | `compact` | none | chat | - | STARTUP | none | Continue working (no menu) |
| 7 | `compact` | Project X | chat about project | planning | COMPACT | plan-project | Continue planning |
| 8 | `resume` | Project X | any | planning | COMPACT | plan-project | Continue planning |
| 9 | `resume` | Project X | any | execution | COMPACT | execute-project | Continue execution |
| 10 | `resume` | none | any | - | STARTUP | none | Display menu |

### Key Distinctions

**Case 4 vs Case 7**:
- Case 4: User loaded project, then switched to `paper-search` skill → STARTUP (moved on)
- Case 7: User loaded project, was chatting about it (no skill switch) → COMPACT (still in context)

**Cases 4-6**: `compact` without project work → STARTUP but with `continue_working` action (no menu display)

### File Loading by Phase

**Planning phase**: Load ALL files from `resume-context.md files_to_load`
- 01-overview.md, 02-discovery.md, 03-plan.md, 04-steps.md

**Execution phase**: Load minimal files
- 01-overview.md (reference)
- 04-steps.md (current progress - CRITICAL)

### Detection Logic

```python
def determine_context_mode(source: str, transcript_path: str) -> dict:
    """
    Returns: {
        "mode": "startup" | "compact",
        "project_id": str | None,
        "phase": "planning" | "execution" | None,
        "skill": "plan-project" | "execute-project" | None,
        "action": "display_menu" | "continue_working"
    }
    """
    # Rule 1: New session = STARTUP with menu
    if source == "new":
        return {"mode": "startup", "project_id": None, "phase": None,
                "skill": None, "action": "display_menu"}

    # Rule 2: Get last loaded project from transcript
    last_project = get_last_loaded_project_from_transcript(transcript_path)

    # Rule 3: Check if switched to skill AFTER project
    switched_to_skill = check_if_switched_to_skill_after_project(transcript_path, last_project)

    # Rule 4: Compact without project OR switched away = STARTUP + continue
    if source == "compact" and (not last_project or switched_to_skill):
        return {"mode": "startup", "project_id": None, "phase": None,
                "skill": None, "action": "continue_working"}

    # Rule 5: Resume without project = STARTUP with menu
    if source == "resume" and not last_project:
        return {"mode": "startup", "project_id": None, "phase": None,
                "skill": None, "action": "display_menu"}

    # Rule 6: Project work detected - determine phase
    phase = detect_project_phase(last_project)  # Check 04-steps.md Phase 1
    skill = "plan-project" if phase == "planning" else "execute-project"

    return {
        "mode": "compact",
        "project_id": last_project,
        "phase": phase,
        "skill": skill,
        "action": "continue_working"
    }
```

---

## Open Questions

- [x] Transcript parsing: YES, parse for project detection
- [x] Continue mode: NO, same as STARTUP with different instruction
- [x] Orchestrator: Full content in startup
- [x] Skills listing: All skills with action paths

---

## Mental Model Analysis Findings

Applied: Devil's Advocate, Assumption Testing, Pre-Mortem, Second-Order Thinking

### Critical Assumptions to Validate

| Assumption | Risk | Validation |
|------------|------|------------|
| XML improves Claude routing behavior | HIGH | Test routing accuracy after deployment |
| Transcript parsing reliably detects project work | HIGH | Test with 20 real transcripts |
| `importance="CRITICAL"` attributes affect AI behavior | MEDIUM | Observe behavior with/without |
| 200ms performance target achievable | MEDIUM | Profile during implementation |

### Pre-Mortem: Top Failure Modes

| Failure Mode | Prevention |
|--------------|------------|
| XML escaping breaks orchestrator content | Add `escape_xml_content()` with markdown code block tests |
| Wrong mode detected constantly | Add debug logging for detection decisions |
| Token explosion in STARTUP | Enforce 20K token limit, truncate if needed |
| Phase detection wrong | Trust 04-steps.md checkboxes over status field |

### Second-Order Effects to Monitor

1. AI may start expecting XML format elsewhere (learned behavior)
2. Debugging requires understanding XML structure
3. Future changes must maintain XML schema compatibility
4. Schema lock-in risk - document and version the format

### Decisions Made

- **No fallback**: Commit fully to XML, no JSON fallback mode
- **Keep transcript parsing**: Resume-context.md timestamp approach rejected (stale data issue)
- **Token limit**: 20K for STARTUP, 10K for COMPACT
- **Mental models in routing**: Add as core skill with proactive suggestions

---

*Next: Break down execution in 04-steps.md*
