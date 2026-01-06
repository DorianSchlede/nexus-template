# Implementation Steps

## Phase 1: Measurement Baseline (FIRST PRIORITY)
- [ ] Create benchmark script to measure current startup time
- [ ] Measure cache file size breakdown (what contributes most to 84KB?)
- [ ] Profile cold vs warm startup time
- [ ] Count tokens per section (metadata, memory_content, instructions)
- [ ] Document current baseline metrics

## Phase 2: Token Reduction - Skills Metadata
- [ ] Reduce skill metadata to essentials: name, description (truncated to 100 chars), file_path
- [ ] Remove duplicate skill entries (core vs learning vs regular)
- [ ] Consider skill "categories" summary instead of full list
- [ ] Lazy-load skill descriptions only when skill is invoked
- [ ] Measure: Target 15KB -> 5KB for skills section

## Phase 3: Token Reduction - Project Metadata
- [ ] Remove `_file_path` from minimal project output (derivable from ID)
- [ ] Truncate description to 80 chars in metadata
- [ ] Remove `tasks_total` and `tasks_completed` (derivable from progress)
- [ ] Only include `current_task` for IN_PROGRESS projects
- [ ] Measure: Target 10KB -> 3KB for projects section

## Phase 4: Token Reduction - Memory Content
- [ ] Don't embed full `orchestrator.md` (6KB) - provide key rules summary
- [ ] Don't embed full `system-map.md` (4KB) - AI can read if needed
- [ ] Keep `goals.md` embedded (user-specific, small)
- [ ] Keep `user-config.yaml` embedded (small, critical for personalization)
- [ ] Remove `memory-map.md` from auto-embed (rarely referenced)
- [ ] Measure: Target 20KB -> 8KB for memory_content

## Phase 5: Attention Sandwich Optimization
- [ ] Reduce duplication - keep full instructions at END only
- [ ] At START: minimal "action" + "project_id" for resume mode
- [ ] Measure instruction overhead: currently ~2KB duplicated

## Phase 6: Caching Improvements
- [ ] Add cache version check (invalidate if nexus package version changes)
- [ ] Add modification timestamp caching for skills/projects
- [ ] Implement incremental metadata updates (only re-scan changed files)
- [ ] Add gzip compression option for cache files

## Phase 7: Code Cleanup
- [ ] Consolidate datetime imports across modules
- [ ] Extract YAML parsing to shared utility
- [ ] Remove backward-compat shims from nexus-loader.py
- [ ] Add type hints where missing

## Phase 8: Performance Testing
- [ ] Re-run benchmark script with optimizations
- [ ] Compare before/after cache sizes
- [ ] Compare before/after startup times
- [ ] Verify no functionality regression

---

## Token Budget Analysis (Current)

```
Section              | Estimated Size | Tokens (~4 chars/token)
---------------------|----------------|------------------------
Instructions (START) | 2,000 chars    | 500 tokens
memory_content       | 35,000 chars   | 8,750 tokens
  - orchestrator.md  | 12,000 chars   | 3,000 tokens
  - system-map.md    | 8,000 chars    | 2,000 tokens
  - memory-map.md    | 5,000 chars    | 1,250 tokens
  - goals.md         | 6,000 chars    | 1,500 tokens
  - user-config.yaml | 4,000 chars    | 1,000 tokens
metadata.projects    | 12,000 chars   | 3,000 tokens
metadata.skills      | 30,000 chars   | 7,500 tokens
stats                | 2,000 chars    | 500 tokens
Instructions (END)   | 2,000 chars    | 500 tokens
JSON overhead        | 3,000 chars    | 750 tokens
---------------------|----------------|------------------------
TOTAL                | 84,000 chars   | 21,000 tokens
```

## Token Budget (Target)

```
Section              | Target Size    | Tokens
---------------------|----------------|--------
Instructions (START) | 500 chars      | 125
memory_content       | 12,000 chars   | 3,000
  - orchestrator (summary) | 2,000    | 500
  - goals.md         | 6,000          | 1,500
  - user-config.yaml | 4,000          | 1,000
metadata.projects    | 4,000 chars    | 1,000
metadata.skills      | 8,000 chars    | 2,000
stats                | 1,500 chars    | 375
Instructions (END)   | 2,000 chars    | 500
JSON overhead        | 2,000 chars    | 500
---------------------|----------------|--------
TOTAL                | 30,000 chars   | 7,500 tokens (64% reduction)
```

---

## Quick Wins (Do First)

1. **Remove memory-map.md from auto-embed** - 5KB savings, zero impact
2. **Truncate skill descriptions to 100 chars** - 10KB savings
3. **Remove `_file_path` from minimal outputs** - 5KB savings
4. **Summarize orchestrator.md instead of embedding** - 10KB savings

Total quick wins: ~30KB = 35% reduction with minimal code changes
