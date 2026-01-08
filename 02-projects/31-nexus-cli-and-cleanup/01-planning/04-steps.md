# Nexus CLI and Cleanup - Execution Steps

**Last Updated**: 2026-01-08

---

## Context Requirements

**Project Location**: `02-projects/31-nexus-cli-and-cleanup/`

**Files to Load**:
- `01-planning/01-overview.md` - Purpose, success criteria
- `01-planning/02-discovery.md` - **DEEP DISCOVERY with line numbers**
- `01-planning/03-plan.md` - Approach, technical implementation
- `01-planning/04-steps.md` - This file

**Key Discovery Reference**:
- nexus-loader.py: L101-121 (args), L128-152 (dispatch)
- loaders.py: L1375-1478 (discover), L1480-1518 (list categories)
- session_start.py: L36, L858-862 (timing already exists)
- orchestrator.md: L244-254 (CLI hints)
- system-map.md: L82-95 (CLI section)

---

## Phase 1: CLI Implementation

### 1.1 Add --discover and --list-categories flags

- [ ] Add arguments to nexus-loader.py (after L120):
  ```python
  parser.add_argument('--discover', help='Discover skills in category (e.g., langfuse)')
  parser.add_argument('--list-categories', action='store_true', help='List all integration categories')
  ```

- [ ] Add dispatch logic (after L147):
  ```python
  elif args.discover:
      from nexus.loaders import discover_skills_in_category
      result = discover_skills_in_category(args.discover, args.base_path)
  elif args.list_categories:
      from nexus.loaders import list_integration_categories
      result = {"categories": list_integration_categories(args.base_path)}
  ```

### 1.2 Test CLI

- [ ] Test: `python 00-system/core/nexus-loader.py --discover langfuse`
  - Expected: JSON with 71 skills
- [ ] Test: `python 00-system/core/nexus-loader.py --list-categories`
  - Expected: JSON list of integration categories
- [ ] Test: `python 00-system/core/nexus-loader.py --discover nonexistent`
  - Expected: Helpful error message

---

## Phase 2: Documentation Updates

### 2.1 Update orchestrator.md (L244-254)

- [ ] Change CLI discovery section from `load-skill` to actual command:
  ```bash
  # List all integration categories
  python 00-system/core/nexus-loader.py --list-categories

  # Discover skills in a category
  python 00-system/core/nexus-loader.py --discover langfuse

  # Load specific skill
  python 00-system/core/nexus-loader.py --skill langfuse-get-trace
  ```

### 2.2 Update system-map.md (L92-94)

- [ ] Change CLI section from `load-skill {category} --help` to:
  ```bash
  # Discover skills in category
  python 00-system/core/nexus-loader.py --discover {category}

  # List all categories
  python 00-system/core/nexus-loader.py --list-categories
  ```

---

## Phase 3: Performance Verification

### 3.1 Read existing performance logs

- [ ] Check `00-system/.cache/session_start_output.log` for timing
- [ ] Verify average <200ms
- [ ] Document findings:
  ```
  Performance Results:
  - Average: ___ ms
  - Target: <200ms
  - Status: PASS/FAIL
  ```

*(No new instrumentation needed - session_start.py L858-862 already logs timing)*

---

## Phase 4: Project 29 Closure

### 4.1 Create Project 29 summary

- [ ] Write `02-projects/29-.../04-outputs/SUMMARY.md`:
  - Token reduction achieved (60.9%)
  - Key changes implemented
  - Lessons learned
  - Deferred items (moved to Project 31)

### 4.2 Update Project 29 status

- [ ] Change status in 01-overview.md: PLANNING → COMPLETE
- [ ] Update 04-steps.md to mark deferred items as "Moved to Project 31"

### 4.3 Archive Project 29

- [ ] Run archive-project skill or move to 05-archived/

---

## Phase 5: Project 30 Review

- [ ] Check `02-projects/30-improve-plan-project-skill/` status
- [ ] If complete: Update status and archive
- [ ] If incomplete: Document remaining work

---

## Phase 6: Cleanup & Completion

### 6.1 Cleanup

- [ ] Delete any *.backup files
- [ ] Remove deprecated TRASH folders if present
- [ ] Verify no orphaned files

### 6.2 Project 31 completion

- [ ] Update this project status: PLANNING → COMPLETE
- [ ] Update resume-context.md with final state
- [ ] Commit all changes

---

## Success Criteria

| Criteria | Test | Status |
|----------|------|--------|
| `--discover` works | `nexus-loader.py --discover langfuse` returns 71 skills | [ ] |
| `--list-categories` works | Returns list of integration categories | [ ] |
| Performance <200ms | Check cache logs | [ ] |
| orchestrator.md updated | L244-254 shows executable commands | [ ] |
| system-map.md updated | L92-94 shows executable commands | [ ] |
| Project 29 archived | Moved to 05-archived/ with summary | [ ] |

---

## Notes

**Blockers**: None

**Dependencies**:
- loaders.py functions already implemented (L1375-1518)
- session_start.py timing already exists (L858-862)

**Estimated Duration**: 1-2 hours (mostly wiring and docs)

---

*Mark tasks complete with [x] as you finish them*
