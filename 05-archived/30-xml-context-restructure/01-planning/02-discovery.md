# XML Context Restructure - Discovery

**Time-box**: 15 min | **Last Updated**: 2026-01-05

---

## Dependencies

### Files to Modify

| File | Purpose | Risk |
|------|---------|------|
| `.claude/hooks/session_start.py` | Main hook that builds context | HIGH - core functionality |
| `00-system/core/nexus/loaders.py` | Loads skills, projects, orchestrator | MEDIUM - data source |
| `00-system/core/nexus/state.py` | State detection functions | LOW - helper functions |

### Files to Read (Context)

| File | Purpose |
|------|---------|
| `00-system/core/orchestrator.md` | Full orchestrator content for startup |
| `00-system/system-map.md` | System structure reference |
| `04-workspace/workspace-map.md` | Workspace structure reference |
| `01-memory/goals.md` | User goals content |
| `02-projects/*/01-planning/resume-context.md` | Project resume state |
| `02-projects/*/01-planning/04-steps.md` | Phase detection |

### External Dependencies

- Claude Code hook system (additionalContext field)
- Transcript files at `~/.claude/projects/*/*.jsonl`

---

## Existing Patterns to Reuse

### Current Functions (session_start.py)

| Function | Keep/Modify | Notes |
|----------|-------------|-------|
| `find_active_project_from_cache()` | KEEP | Works well for project detection |
| `detect_project_phase()` | KEEP | Phase 1 completion detection |
| `load_resume_context()` | KEEP | Parses resume-context.md |
| `auto_load_project_files()` | MODIFY | Change output from markdown to XML |
| `build_resume_header()` | REPLACE | New XML builder |
| `build_startup_context()` | REPLACE | New XML builder |

### Current Functions (loaders.py)

| Function | Keep/Modify | Notes |
|----------|-------------|-------|
| `scan_projects()` | KEEP | Returns project metadata |
| `scan_skills_tiered()` | MODIFY | Need to add trigger patterns |
| `extract_essential_orchestrator()` | REPLACE | Full XML structure |
| `load_full_startup_context()` | REPLACE | New XML builder |

### Transcript Parsing (NEW)

Need to create: `check_transcript_for_project_work(transcript_path)`
- Read last N entries from JSONL transcript
- Look for project-related patterns:
  - "plan-project" or "execute-project" skill mentions
  - Project file paths (01-planning/, 02-resources/)
  - Project ID references

---

## Risks & Unknowns

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Break existing sessions | HIGH | HIGH | Thorough testing before deploy |
| XML parsing issues | LOW | MEDIUM | Use simple XML structure |
| Performance regression | MEDIUM | LOW | Profile hook execution time |
| Transcript parsing slow | MEDIUM | LOW | Only read last 50 entries |
| Missing edge cases | HIGH | MEDIUM | Document all scenarios |

---

## Edge Cases Identified

### Session Sources

| Source | Has Project? | Was Working? | Mode |
|--------|--------------|--------------|------|
| new | - | - | STARTUP |
| compact | Yes | Yes (plan/exec) | COMPACT |
| compact | Yes | No (skill/chat) | STARTUP |
| compact | No | - | STARTUP |
| resume | Yes | Yes | COMPACT |
| resume | Yes | No | STARTUP |
| resume | No | - | STARTUP |

### Project States

| State | Detection | Action |
|-------|-----------|--------|
| No projects exist | `02-projects/` empty | STARTUP, suggest plan-project |
| No resume-context.md | Files missing | STARTUP |
| Multiple resume-context.md | Multiple projects | Pick most recent by timestamp |
| Malformed resume-context.md | Parse error | STARTUP, log warning |
| 04-steps.md missing | File not found | Default to plan-project |
| Phase 1 incomplete | Checkboxes unchecked | plan-project |
| Phase 1 complete | All [x] | execute-project |

### Transcript Analysis

| Pattern | Indicates |
|---------|-----------|
| "plan-project" in messages | Was planning |
| "execute-project" in messages | Was executing |
| Project file paths | Was working on project |
| Skill file paths | Was running skill |
| No patterns | General chat |

---

## Key Insights

1. **COMPACT vs RESUME distinction**:
   - COMPACT = auto-summary triggered (check transcript for project work)
   - RESUME = user explicitly resumed (assume project work)

2. **Mode determination flow**:
   ```
   source == "new" → STARTUP
   source == "compact" → check_transcript() → project work? → COMPACT : STARTUP
   source == "resume" → has active project? → COMPACT : STARTUP
   ```

3. **Skill auto-loading**:
   - When AI suggests "plan-project" → also load plan-project/SKILL.md
   - When AI suggests "execute-project" → also load execute-project/SKILL.md
   - This requires embedding skill content in the suggestion

4. **Dynamic skill construction**:
   - Scan `00-system/skills/` for system skills
   - Scan `03-skills/` for user skills
   - Extract name + description from YAML frontmatter
   - Group by category (from folder structure)

---

*Discovery complete. See 03-plan.md for full XML specification.*
