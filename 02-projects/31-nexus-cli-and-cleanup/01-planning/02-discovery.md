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
- `00-system/core/nexus-loader.py` - Add --discover argument
- `00-system/core/nexus/loaders.py` - Update build_skills_xml_compact() CLI hints
- `00-system/core/orchestrator.md` - Add skill discovery documentation
- `00-system/system-map.md` - Update architecture documentation
- `.claude/hooks/session_start.py` - Add timing instrumentation

**Files to Create**:
- `02-projects/29-.../04-outputs/SUMMARY.md` - Project 29 final summary

**External Systems**:
- None (all local Python code)

---

## Existing Patterns

*Skills, templates, code to reuse*

**Related Skills**:
- `00-system/skills/system/list-skills/SKILL.md` - Similar pattern for listing
- `00-system/skills/projects/archive-project/SKILL.md` - For archiving Project 29

**Related Projects**:
- `02-projects/29-nexus-context-loading-optimization-and-xml-restructure/` - Parent project
- `02-projects/30-improve-plan-project-skill/` - Review status

**Code Patterns**:
- `discover_skills_in_category()` in loaders.py - Already implemented, needs CLI wiring
- `list_integration_categories()` in loaders.py - Could add `--list-categories` flag

**Key Implementation Already Done**:
```python
# In loaders.py - discover_skills_in_category() returns:
{
    "category": "langfuse",
    "skills": [...],  # List of skill metadata
    "count": 71,
    "formatted": "Langfuse Operations (71 skills):\n..."  # Ready to print
}
```

---

## Risks & Unknowns

*What could derail? What don't we know?*

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Hook performance >200ms | Low | Profile first, optimize if needed |
| Breaking existing functionality | Low | Test each change incrementally |
| nexus-loader.py arg conflicts | Low | Check existing args first |
| Category not found handling | Medium | Return helpful error message |

**Open Questions**:
- [x] Keep `load-skill` or use `--discover`? → Use `--discover` for consistency
- [ ] Add `--list-categories` flag for discovery?
- [ ] Should errors return JSON or text?

---

## Discovered Functions

**loaders.py already has**:
1. `discover_skills_in_category(category, base_path)` - Returns formatted skill list
2. `list_integration_categories(base_path)` - Returns list of category dicts
3. `build_skills_xml_compact(base_path)` - Uses `<cli>load-skill X --help</cli>` hints

**nexus-loader.py already has**:
- `--startup` - Build startup context
- `--resume` - Build resume context
- `--project ID` - Load project context
- `--skill NAME` - Load skill file
- `--list-projects` - List all projects
- `--list-skills` - List all skills

**Gap**: No `--discover CATEGORY` to call discover_skills_in_category()

---

*Auto-populate 03-plan.md Dependencies section from findings above*
