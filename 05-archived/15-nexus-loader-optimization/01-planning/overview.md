---
id: 15-nexus-loader-optimization
name: Nexus Loader Optimization
status: COMPLETE
description: Performance and token optimization for nexus-loader.py and the nexus package
created: 2025-12-31
completed: 2026-01-04
---

# Nexus Loader Optimization

## Goal

Optimize the nexus-loader system for:
1. **Faster startup** - Reduce cold start time
2. **Smaller token footprint** - Current 84KB (~21K tokens) is ~10% of context window
3. **Smarter caching** - Reduce redundant file reads
4. **Better progressive disclosure** - Load only what's needed

## Current State Analysis

### Package Structure (2,524 lines total)
| File | Lines | Purpose |
|------|-------|---------|
| loaders.py | 556 | Project/skill scanning, file loading |
| state.py | 504 | State detection, instruction building |
| sync.py | 344 | Upstream sync functionality |
| models.py | 321 | Data models and enums |
| utils.py | 285 | Utility functions |
| service.py | 270 | Main NexusService API |
| config.py | 171 | Configuration constants |
| __init__.py | 73 | Package exports |

### Current Output Size
- **Startup cache**: 84,139 bytes (~21,000 tokens)
- **Memory content**: 5 files embedded (orchestrator.md, system-map.md, memory-map.md, goals.md, user-config.yaml)
- **Metadata**: 14 projects + 100 skills fully serialized
- **Instructions**: Duplicated at START and END (Attention Sandwich)

## Optimization Opportunities

### 1. Token Reduction (HIGH IMPACT)

**Problem**: 84KB for startup is excessive. Much is redundant or unused.

**Solutions**:
- Compress skill metadata (100 skills with descriptions = ~15KB)
- Remove unused fields from project metadata
- Summarize instead of embedding full files
- Lazy-load references (don't embed all 5 memory files upfront)

**Target**: Reduce to 40KB (~10K tokens) = 50% reduction

### 2. Lazy Loading (MEDIUM IMPACT)

**Problem**: All skills and projects scanned on every startup.

**Solutions**:
- Cache skill/project metadata with file modification timestamps
- Only re-scan if files changed (stat check is cheap)
- Pre-compute metadata index on first run

**Target**: Sub-100ms startup for repeat sessions

### 3. Progressive Disclosure (MEDIUM IMPACT)

**Problem**: Full skill descriptions embedded even when not used.

**Solutions**:
- Startup: Only skill names and triggers
- On-demand: Load full SKILL.md when invoked
- Project metadata: Only ID, status, progress (not full description)

### 4. Caching Architecture (LOW IMPACT - ALREADY GOOD)

Current caching is solid:
- Session-specific cache files
- Stale cache cleanup
- Proper isolation

Minor improvements:
- Add cache versioning (invalidate on nexus package update)
- Compress cache files (gzip JSON)

### 5. Code Cleanup

**Redundancies identified**:
- `datetime` imported multiple times in different modules
- Duplicate YAML parsing logic in state.py and loaders.py
- Some backward-compat shims in nexus-loader.py can be removed

## Non-Goals

- Changing the API interface (backward compatible)
- Major architectural refactoring
- Adding new features (optimization only)

## Success Metrics

| Metric | Current | Target | Method |
|--------|---------|--------|--------|
| Startup cache size | 84KB | 40KB | Token analysis |
| Cold startup time | ~1.5s | <1s | Timing test |
| Warm startup time | ~0.5s | <0.2s | Timing test |
| Memory files loaded | 5 | 2-3 | Count |
| Skill metadata size | ~15KB | ~5KB | JSON size |

## Dependencies

- Project 14 (Advanced Hook System) - SessionStart hook integration
- No external dependencies

## References

- [00-system/core/nexus/](../../../00-system/core/nexus/) - Package source
- [00-system/core/nexus-loader.py](../../../00-system/core/nexus-loader.py) - CLI wrapper
