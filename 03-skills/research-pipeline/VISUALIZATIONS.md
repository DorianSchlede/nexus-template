# Research Pipeline Visualizations

**Last Updated**: 2026-01-02
**Status**: Active Development

---

## Overview

This directory contains multiple iterations of the research pipeline visualization, evolving from programmatic extraction to manually-crafted human-readable content.

---

## Current Recommended Version

**[research-pipeline.html](research-pipeline.html)** - **RECOMMENDED**
- **Type**: Manually written HTML
- **Content**: Handcrafted descriptions for all 29 steps across 3 phases
- **Approach**: Read actual SKILL.md files and wrote clear, human-readable explanations
- **Features**:
  - Phase 1: Planning & Acquisition (14 steps)
  - Phase 2: Analysis (5 steps)
  - Phase 3: Synthesis with 7-level architecture (10 steps)
  - Each step includes: What, Why, Creates, Solves, Badges
  - Dark theme, clean progressive disclosure UX

---

## Programmatic Generators (v6-v12)

All versions below use Python to extract content from SKILL.md files programmatically.

### Version 12 - Human-Readable Content Focus
**File**: [visualize_pipeline_v12.py](visualize_pipeline_v12.py)
**Output**: [research_pipeline_v12_human.html](research_pipeline_v12_human.html)
**Approach**: Most sophisticated programmatic extraction with better text cleaning
- Extracts: what, why, when, how, creates, uses, checks, scripts, solves
- Advanced regex patterns for description extraction
- Criticality badges (MUST-PASS / IMPORTANT / STANDARD)

### Version 11 - Content-Rich Extraction
**File**: [visualize_pipeline_v11.py](visualize_pipeline_v11.py)
**Output**: [research_pipeline_v11_content_rich.html](research_pipeline_v11_content_rich.html)
**Approach**: Richer programmatic extraction (purpose, context, details)
- Attempted to extract more semantic content automatically

### Version 10 - Premium Design
**File**: [visualize_pipeline_v10.py](visualize_pipeline_v10.py)
**Output**: [research_pipeline_v10_ultra.html](research_pipeline_v10_ultra.html)
**Approach**: Visual polish focus
- Premium gradient design
- User rejected: wanted content improvement, not visual enhancement

### Version 9 - Simple Flow (FIXED)
**File**: [visualize_pipeline_v9.py](visualize_pipeline_v9.py)
**Output**: [research_pipeline_v9_simple.html](research_pipeline_v9_simple.html)
**Status**: Fixed description extraction issue
- **Problem**: Was extracting formatting markers (`**MANDATORY:**`), commands, gap references
- **Solution**: Updated `parse_simple_step()` to skip noise and find actual explanatory text
- Clean flow visualization with basic step info

### Version 6-8 - Early Iterations
**Files**:
- [visualize_pipeline_v6.py](visualize_pipeline_v6.py) → [research_pipeline_v6.html](research_pipeline_v6.html)
- [visualize_pipeline_v7.py](visualize_pipeline_v7.py) → [research_pipeline_v7.html](research_pipeline_v7.html)
- [visualize_pipeline_v8.py](visualize_pipeline_v8.py) → [research_pipeline_v8.html](research_pipeline_v8.html)
- [visualize_pipeline.py](visualize_pipeline.py) (original)

**Status**: Early exploration of programmatic extraction approaches

---

## Additional Visualizations

### Flow Diagram
**File**: [research_pipeline_flow.html](research_pipeline_flow.html)
**Type**: Unknown (needs review)

### Version 5
**File**: [visualize_pipeline_v5.py](visualize_pipeline_v5.py)
**Output**: Unknown

---

## Development Evolution

The visualization development followed this progression:

1. **v6-v8**: Initial programmatic extraction attempts
2. **v9**: Fixed description extraction (skipping formatting noise)
3. **v10**: Attempted visual polish (user rejected - wanted content, not visuals)
4. **v11**: Attempted richer programmatic extraction
5. **v12**: Most sophisticated programmatic extraction with text cleaning
6. **Final (research-pipeline.html)**: **Manual content creation** - the correct approach
   - User feedback: "do text manually you fuck"
   - Abandoned regex extraction entirely
   - Read actual SKILL.md files and wrote human-understandable descriptions

---

## Key Learnings

1. **Programmatic extraction has limits**: Regex patterns can't understand semantic meaning
2. **Content > Visuals**: User prioritized information quality over design polish
3. **Manual curation wins**: Handcrafted content based on actual understanding beats automation
4. **Progressive disclosure**: Flow-first design with details on demand works best

---

## Files to Use

**For understanding the pipeline**:
- Use: [research-pipeline.html](research-pipeline.html)
- Read in browser: `file:///C:/Users/dsber/infinite/auto-company/strategy-nexus/03-skills/research-pipeline/research-pipeline.html`

**For reference**:
- System docs: [../../00-system/documentation/research-algorithm-en.md](../../00-system/documentation/research-algorithm-en.md)
- Architecture: [_index.md](_index.md)

**For development**:
- v12 generator: Most advanced programmatic approach (if needed)
- Source files: `orchestrators/*/SKILL.md` for actual step descriptions

---

## Next Steps

- [ ] Consider adding interactive filtering (by phase, orchestrator, gap)
- [ ] Add search functionality for finding specific steps
- [ ] Export to PDF for offline reference
- [ ] Consider adding timeline/sequence view

---

*Documentation for research pipeline visualization files*
