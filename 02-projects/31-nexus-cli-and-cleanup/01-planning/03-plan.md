# Nexus CLI and Cleanup - Plan

**Last Updated**: 2026-01-08

---

## Context

**Load Before Reading**:
- `01-planning/01-overview.md` - Purpose and success criteria
- `01-planning/02-discovery.md` - **DEEP DISCOVERY with exact line numbers**

**Background**:
This project completes remaining work from Project 29 (Context Loading Optimization) which achieved 60.9% token reduction. The deep discovery revealed:
- CLI discovery functions exist but aren't wired to CLI
- Performance instrumentation already exists (no new code needed)
- Documentation has non-executable CLI hints
- Project 29 ready for archival

---

## Deep Discovery Summary

### What's Already Implemented (No Work Needed)

| Component | Location | Status |
|-----------|----------|--------|
| `discover_skills_in_category()` | loaders.py L1375-1478 | ✅ Fully implemented |
| `list_integration_categories()` | loaders.py L1480-1518 | ✅ Fully implemented |
| Performance timing | session_start.py L36, L858-862 | ✅ Already instrumented |
| 6 MECE state templates | .claude/hooks/templates/ | ✅ All implemented |
| add-integration skill | 00-system/skills/system/add-integration/ | ✅ Full 622 lines |

### What Needs Implementation

| Component | Location | Change Required |
|-----------|----------|-----------------|
| `--discover` flag | nexus-loader.py L101-121, L128-152 | Add argument + dispatch |
| `--list-categories` flag | nexus-loader.py L101-121, L128-152 | Add argument + dispatch |
| CLI hint update | orchestrator.md L244-254 | Change to actual command |
| CLI hint update | system-map.md L82-95 | Change to actual command |

---

## Approach

**Strategy**: Minimal wiring with immediate testing

1. **CLI Wiring** - Add two flags that connect to existing functions
2. **Doc Updates** - Fix CLI hints to show executable commands
3. **Verify Performance** - Read existing logs (no new instrumentation)
4. **Close** - Archive completed projects

**Principle**: The heavy lifting is done. This is just wiring and documentation.

---

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| CLI command style | `--discover CATEGORY` | Consistent with nexus-loader.py patterns |
| Add list-categories | `--list-categories` | Function exists at L1480, useful for discovery |
| Skip timing code | Already exists | session_start.py L858-862 logs timing |
| Update XML hints | Yes | Prevents confusion with non-executable hints |
| JSON output | `json.dumps(result, indent=2)` | Follow existing pattern |

---

## Technical Implementation

### nexus-loader.py Changes

**Add arguments (after L120)**:
```python
parser.add_argument('--discover', help='Discover skills in category (e.g., langfuse)')
parser.add_argument('--list-categories', action='store_true', help='List all integration categories')
```

**Add dispatch (after L147)**:
```python
elif args.discover:
    from nexus.loaders import discover_skills_in_category
    result = discover_skills_in_category(args.discover, args.base_path)
elif args.list_categories:
    from nexus.loaders import list_integration_categories
    result = {"categories": list_integration_categories(args.base_path)}
```

### orchestrator.md Changes (L244-254)

**From**:
```bash
load-skill langfuse --help
```

**To**:
```bash
python 00-system/core/nexus-loader.py --discover langfuse
python 00-system/core/nexus-loader.py --list-categories
```

### system-map.md Changes (L92-94)

**From**:
```bash
load-skill {category} --help
```

**To**:
```bash
python 00-system/core/nexus-loader.py --discover {category}
```

---

## Inherited from Project 29

### Remaining Tasks (Moved Here)

From Project 29 Phase 7-8:
- [ ] Profile hook performance: <200ms average
- [ ] Update system-map.md with new architecture
- [ ] Document CLI usage in relevant skill files
- [ ] Update orchestrator.md inline comments
- [ ] Delete backup files (*.backup)
- [ ] Archive project resources to 04-outputs/
- [ ] Create final summary in 04-outputs/SUMMARY.md

### Completed in Project 29

- [x] Token reduction ≥30% → **ACHIEVED: 60.9% reduction**
- [x] Routing accuracy ≥95% → Skills routing verified
- [x] MECE state templates → 6 startup states implemented
- [x] CLI discovery pattern → Skills collapsed to categories
- [x] Merge feature branch to main

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Breaking existing args | LOW | High | Test all args after changes |
| Category not found | LOW | Low | Function returns helpful message |
| Import errors | LOW | Medium | Functions already exported |

---

## Open Questions (All Resolved)

- [x] Keep `load-skill` or `--discover`? → **Use --discover**
- [x] Add `--list-categories`? → **Yes, function exists**
- [x] Add timing instrumentation? → **No, already exists**
- [x] JSON or text output? → **JSON with indent=2**
- [x] Category not found handling? → **Function returns helpful message**

---

## Success Metrics

1. **CLI Works**: `python nexus-loader.py --discover langfuse` outputs 71 skills
2. **Categories Work**: `python nexus-loader.py --list-categories` lists integrations
3. **Performance**: Verify <200ms from existing logs
4. **Documentation**: orchestrator.md and system-map.md show executable commands
5. **Closure**: Project 29 archived with summary

---

*Next: Execute in 04-steps.md*
