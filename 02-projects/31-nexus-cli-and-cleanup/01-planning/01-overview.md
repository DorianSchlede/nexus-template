---
id: 31-nexus-cli-and-cleanup
name: Nexus CLI and Cleanup
status: PLANNING
description: "Complete remaining Nexus optimization tasks: CLI discovery, performance profiling, documentation updates, and cleanup."
created: 2026-01-07
project_path: 02-projects/31-nexus-cli-and-cleanup/
---

# Nexus CLI and Cleanup

## Project Files

| File | Purpose |
|------|---------|
| 01-overview.md | This file - purpose, success criteria |
| 02-discovery.md | Dependencies, patterns, risks |
| 03-plan.md | Approach, decisions |
| 04-steps.md | Execution tasks |
| 02-resources/ | Reference materials |
| 03-working/ | Work in progress |
| 04-outputs/ | Final deliverables |

---

## Purpose

Complete the remaining work from Project 29 (Context Loading Optimization) and address open items discovered during implementation:

1. **CLI Discovery Implementation** - Make `load-skill {category} --help` actually executable
2. **Performance Profiling** - Verify hook execution <200ms
3. **Documentation Updates** - Update system-map.md, orchestrator.md
4. **Project 29 Cleanup** - Archive resources, update status to COMPLETE

---

## Success Criteria

**Must achieve**:
- [x] `load-skill langfuse --help` returns formatted skill list (CLI works)
- [ ] Hook execution time measured and documented (<200ms target)
- [ ] system-map.md updated with new architecture
- [ ] Project 29 archived with final summary

**Nice to have**:
- [ ] Add `--discover` flag to nexus-loader.py
- [ ] Performance optimization if hook >200ms
- [ ] 10 full session cycle tests

---

## Context

**Background**:
Project 29 achieved 60.9% token reduction (from ~13.5K to ~5.3K tokens) through:
- CLI discovery pattern for skills (87% reduction in skills XML)
- 6 MECE startup state templates
- XML format for orchestrator, system-map, memory-map

However, several items were deferred:
- The `<cli>load-skill langfuse --help</cli>` hint exists but Claude can't execute it
- Hook performance not measured
- Documentation not updated
- Project 29 not formally closed

**Stakeholders**:
- Daniel (user) - needs working CLI discovery
- Future Claude sessions - need accurate documentation

**Constraints**:
- Must maintain backward compatibility
- Hook must remain <200ms

---

## Related

- **Project 29**: 02-projects/29-nexus-context-loading-optimization-and-xml-restructure/
- **CLI Spec**: 02-projects/29-.../02-resources/TRASH/load-skill-cli-spec.md
- **Functions**: 00-system/core/nexus/loaders.py (discover_skills_in_category)

---

*Next: Fill in 04-steps.md with concrete tasks*
