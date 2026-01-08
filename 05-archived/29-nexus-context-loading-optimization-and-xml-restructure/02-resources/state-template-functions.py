# State Template Functions for Dynamic Instructions
# Location: 00-system/core/nexus/loaders.py
# Purpose: MECE-compliant state-aware instruction generation

from typing import Dict, Any, List


def build_next_action_instruction(context: Dict[str, Any]) -> str:
    """
    Generate state-specific instruction using priority-based selection.

    Uses MECE principle: Mutually Exclusive, Collectively Exhaustive.
    First match wins - no overlapping states.

    Args:
        context: Full startup context with stats, projects, onboarding

    Returns:
        Markdown string with clear next-action directive
    """
    # Priority 1: Onboarding incomplete
    if len(context.get("pending_onboarding", [])) > 0:
        return _template_onboarding_incomplete(context)

    # Priority 2: Active work exists
    if len(context.get("active_projects", [])) > 0:
        return _template_active_projects(context)

    # Priority 3: Workspace needs sync
    if context.get("workspace_needs_validation", False):
        return _template_workspace_modified(context)

    # Priority 4: Fresh start (configured, no projects)
    if context.get("total_projects", 0) == 0 and context.get("goals_personalized", False):
        return _template_fresh_workspace(context)

    # Priority 5: System ready (fallback)
    return _template_system_ready(context)


# ============================================================================
# EDITABLE TEMPLATE FUNCTIONS - Customize state behaviors here
# ============================================================================

def _template_onboarding_incomplete(context: Dict[str, Any]) -> str:
    """
    STATE 1: Onboarding incomplete

    WHEN: User hasn't completed setup-memory or setup-workspace
    ACTION: Gently suggest completing onboarding
    """
    pending = context["pending_onboarding"]
    pending_list = "\n".join(f"- {skill}" for skill in pending[:3])

    return f"""CRITICAL: User onboarding incomplete

Pending setup:
{pending_list}

Display menu, then suggest completing onboarding:
"Before we start, would you like to configure your goals?
Say 'setup memory' for a 5-min setup."

If user declines, proceed with their request.
Wait for user input."""


def _template_active_projects(context: Dict[str, Any]) -> str:
    """
    STATE 2: Active projects exist

    WHEN: User has IN_PROGRESS or PLANNING projects
    ACTION: Highlight project continuations
    """
    projects = context["active_projects"][:2]  # Max 2
    project_list = "\n".join(
        f"- Project {p['id']}: {p['name']} ({p['status']}, {p.get('progress', 0)}%)"
        for p in projects
    )

    return f"""ACTIVE PROJECTS DETECTED

Current work:
{project_list}

Display menu with project continuations highlighted in suggestions.

When user says:
- "continue [project name/ID]" → Load execute-project immediately
- New request → Check if it relates to existing project first
- Unclear → Ask: "Continue existing project or start something new?"

Wait for user input."""


def _template_workspace_modified(context: Dict[str, Any]) -> str:
    """
    STATE 3: Workspace changes detected

    WHEN: Files added/modified in 04-workspace/ since last validation
    ACTION: Suggest running update-workspace-map
    """
    return """WORKSPACE CHANGES DETECTED

Files modified in 04-workspace/ since last session.

Display menu with "validate workspace" in suggestions.

When user asks about workspace:
1. Offer to run update-workspace-map skill
2. Show what changed
3. Update map automatically or guide manual update

Wait for user input."""


def _template_fresh_workspace(context: Dict[str, Any]) -> str:
    """
    STATE 4: Fresh workspace (configured but no projects)

    WHEN: Goals configured, no active projects
    ACTION: Emphasize starting first project
    """
    return """READY TO START

User has configured goals but no active projects yet.

Display menu, emphasize "Start your first project" in suggestions.

When user describes work:
1. Assess if it's finite deliverable (project) vs repeatable pattern (skill)
2. Suggest plan-project for finite work
3. Suggest relevant skill for utilities

Be proactive in offering structure.
Wait for user input."""


def _template_system_ready(context: Dict[str, Any]) -> str:
    """
    STATE 5: System ready (fallback for all other cases)

    WHEN: Onboarding complete, no active projects, workspace current
    ACTION: Open-ended, ready for anything
    """
    return """SYSTEM READY

Onboarding complete. No active projects. Workspace validated.

Display menu with "What would you like to build?" emphasis.

Be ready for:
- New project request → plan-project
- Skill execution → Match and load
- Exploration → Explain capabilities

Wait for user input."""


# ============================================================================
# SUGGESTED NEXT STEPS - Complementary to instructions
# ============================================================================

def build_suggested_next_steps(context: Dict[str, Any]) -> List[str]:
    """
    Build prioritized list of suggested actions based on state.

    Returns ordered list of suggestions (max 5).
    """
    suggestions = []

    # Priority 1: Critical onboarding
    if not context.get("goals_personalized"):
        suggestions.append("'setup memory' - configure your goals and role (5 min)")

    if not context.get("workspace_configured"):
        suggestions.append("'setup workspace' - organize your folder structure (10 min)")

    # Priority 2: Active work
    active_projects = [p for p in context.get("projects", [])
                      if p.get("status") in ("IN_PROGRESS", "PLANNING")]

    for proj in active_projects[:2]:  # Max 2 project suggestions
        name = proj["name"]
        progress = proj.get("progress", 0)
        suggestions.append(f"'continue {name}' - resume at {progress}%")

    # Priority 3: Workspace maintenance
    if context.get("workspace_needs_validation"):
        suggestions.append("'validate workspace' - sync workspace-map.md")

    # Priority 4: End of session
    suggestions.append("'close session' - save progress and learnings")

    # Priority 5: Exploration (if room)
    if len(suggestions) < 5:
        if context.get("total_projects") == 0:
            suggestions.append("'create project' - start your first project")
        else:
            suggestions.append("'explain nexus' - learn system capabilities")

    # Return top 5
    return suggestions[:5]


# ============================================================================
# TESTING UTILITIES
# ============================================================================

def test_state_selection():
    """Test that states are MECE and select correctly."""

    # Test 1: Onboarding incomplete (Priority 1)
    ctx1 = {"pending_onboarding": ["setup-memory", "setup-workspace"]}
    assert "CRITICAL" in build_next_action_instruction(ctx1)

    # Test 2: Active projects (Priority 2)
    ctx2 = {"pending_onboarding": [], "active_projects": [{"id": 29, "name": "Test", "status": "IN_PROGRESS", "progress": 50}]}
    assert "ACTIVE PROJECTS" in build_next_action_instruction(ctx2)

    # Test 3: Workspace modified (Priority 3)
    ctx3 = {"pending_onboarding": [], "active_projects": [], "workspace_needs_validation": True}
    assert "WORKSPACE CHANGES" in build_next_action_instruction(ctx3)

    # Test 4: Fresh workspace (Priority 4)
    ctx4 = {"pending_onboarding": [], "active_projects": [], "workspace_needs_validation": False, "total_projects": 0, "goals_personalized": True}
    assert "READY TO START" in build_next_action_instruction(ctx4)

    # Test 5: System ready (Priority 5 - fallback)
    ctx5 = {"pending_onboarding": [], "active_projects": [], "workspace_needs_validation": False, "total_projects": 5, "goals_personalized": True}
    assert "SYSTEM READY" in build_next_action_instruction(ctx5)

    print("All state selection tests passed!")


if __name__ == "__main__":
    test_state_selection()
