# Nexus CLI and Cleanup - Plan

**Last Updated**: 2026-01-07

---

## Context

**Load Before Reading**:
- `01-planning/01-overview.md` - Purpose and success criteria
- `01-planning/02-discovery.md` - Dependencies discovered

**Background**:
This project completes remaining work from Project 29 (Context Loading Optimization) which achieved 60.9% token reduction. Several items were deferred during implementation:
- CLI discovery hint exists but isn't executable
- Performance not measured
- Documentation not updated
- Project 29 not formally archived

---

## Approach

**Strategy**: Incremental completion with immediate testing

1. **CLI First** - Implement the --discover flag since it's a concrete deliverable that unblocks skill discovery
2. **Measure** - Profile hook performance before any optimization (baseline)
3. **Document** - Update docs to reflect current state
4. **Close** - Archive completed projects properly

**Principle**: Ship working code, not perfect code. Each phase delivers testable value.

---

## Key Decisions

| Decision | Choice | Why |
|----------|--------|-----|
| CLI command style | `--discover CATEGORY` flag | Consistent with existing nexus-loader.py patterns |
| Update XML hints | Yes, change to actual command | Prevents confusion when Claude sees non-executable hints |
| Performance target | <200ms | Original Project 29 requirement |
| Project 29 status | Archive after summary | Formal closure for project tracking |

---

## Dependencies & Links

**Files Impacted**:
- `00-system/core/nexus-loader.py` - Add --discover argument
- `00-system/core/nexus/loaders.py` - discover_skills_in_category() already implemented
- `00-system/core/orchestrator.md` - Add skill discovery docs
- `00-system/system-map.md` - Update architecture docs
- `.claude/hooks/session_start.py` - Add timing if not present

**External Systems**:
- None (all local Python)

**Related Projects**:
- **Project 29**: 02-projects/29-nexus-context-loading-optimization-and-xml-restructure/
- **Project 30**: 02-projects/30-improve-plan-project-skill/

---

## Technical Architecture

**CLI Discovery Flow**:
```
User/Claude runs: python nexus-loader.py --discover langfuse
                         │
                         ▼
              Parse --discover argument
                         │
                         ▼
         Call discover_skills_in_category("langfuse")
                         │
                         ▼
        Scan 03-skills/langfuse/**SKILL.md
                         │
                         ▼
        Extract YAML frontmatter (name, description)
                         │
                         ▼
        Format and print to stdout
```

**Performance Measurement**:
```python
# In session_start.py
import time
start = time.perf_counter()
# ... hook execution ...
duration_ms = (time.perf_counter() - start) * 1000
logging.info(f"Hook execution: {duration_ms:.1f}ms")
```

---

## Implementation Strategy

**Phase 1: CLI Discovery (Day 1)**
- Add --discover flag to nexus-loader.py
- Test with `--discover langfuse`
- Update XML hints in build_skills_xml_compact()

**Phase 2: Performance (Day 1)**
- Add timing to session_start.py
- Run 5-10 startup cycles
- Document results

**Phase 3: Documentation (Day 1-2)**
- Update system-map.md with new architecture
- Review and fix startup templates

**Phase 4: Cleanup (Day 2)**
- Write Project 29 summary
- Archive Project 29
- Review Project 30 status

**Testing Approach**:
- CLI: `python nexus-loader.py --discover langfuse` returns 71 skills
- Performance: Average <200ms across 10 runs
- Docs: Manual review for accuracy

---

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| Hook performance >200ms | Medium | Profile and optimize hot paths |
| Breaking existing functionality | High | Test after each change |
| Documentation drift | Low | Update docs in same PR as code |

---

## Open Questions

- [x] Should we keep `load-skill` syntax or switch to `--discover`? → **Use --discover (consistent with CLI)**
- [ ] Should we add `--list-categories` flag too?
- [ ] How to handle category not found errors?

---

## Success Metrics

1. **CLI Works**: `python nexus-loader.py --discover langfuse` outputs skill list
2. **Performance**: Hook execution <200ms (measured)
3. **Documentation**: system-map.md accurately reflects current architecture
4. **Closure**: Project 29 archived with summary

---

*Next: Execute phases in 04-steps.md*
