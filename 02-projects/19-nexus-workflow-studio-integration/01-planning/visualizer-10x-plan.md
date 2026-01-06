# Research Pipeline Visualizer - 10x Plan

**Goal**: Transform the basic step list into a comprehensive workflow visualization that shows the complete research pipeline with all three orchestrators, their relationships, data flows, and operational details.

---

## Current State (v2)

- Single SKILL.md parsing
- Linear step list with phase colors
- Basic detail panel (inputs/outputs/scripts/gates)
- Static layout, no interaction beyond click

**Problems**:
- Doesn't show the 3-skill chain relationship
- Missing hierarchical depth (phases → steps → sub-steps → contracts)
- No file dependency graph
- No subagent spawn visualization
- No token budgets or concurrency info
- Ugly/basic styling

---

## Target State (v3 - 10x)

### Feature 1: Multi-Orchestrator Pipeline View

```
┌─────────────────────────────────────────────────────────────────────┐
│                    RESEARCH PIPELINE OVERVIEW                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────────┐     ┌──────────────────┐     ┌──────────────┐ │
│  │ create-research  │────▶│ analyze-research │────▶│ synthesize-  │ │
│  │    -project      │     │    -project      │     │   research   │ │
│  │                  │     │                  │     │   -project   │ │
│  │  14 steps        │     │  5 steps         │     │  10 steps    │ │
│  │  4 phases        │     │  3 phases        │     │  7 levels    │ │
│  │  3 gates         │     │  1 gate          │     │  1 gate      │ │
│  └──────────────────┘     └──────────────────┘     └──────────────┘ │
│         │                         │                       │         │
│         ▼                         ▼                       ▼         │
│  📄 _briefing.md           📄 index.md (per paper)  📄 _synthesis_  │
│  📄 _analysis_kit.md       📄 _analysis_log.md         report.md    │
│  📄 chunks ready           📄 validation_report                     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Implementation**:
- Parse all 3 SKILL.md files in orchestrators/
- Show pipeline overview at top
- Click to drill into any orchestrator
- Handoff arrows show data dependencies

### Feature 2: Hierarchical Drill-Down

```
PHASE A: VALIDATION
├─ Step 1: Validate Readiness
│   ├─ 1.1: Check _briefing.md exists
│   ├─ 1.2: Check _analysis_kit.md exists
│   ├─ 1.3: Check chunks ready
│   └─ 1.4: Display status
│
├─ Step 1.5: Read Pre-Calculated Allocation
│   └─ Contract:
│       ├─ INPUT: 01-planning/plan.md
│       └─ OUTPUT: parsed allocation table
```

**Implementation**:
- Parse `### N.M` patterns for sub-steps
- Extract contracts from code blocks
- Expandable/collapsible tree structure
- Show depth indicators

### Feature 3: Data Flow Graph

```
                    ┌─────────────────┐
                    │  _briefing.md   │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
┌────────────────┐  ┌────────────────┐  ┌────────────────┐
│ _analysis_kit  │  │ _extraction_   │  │ plan.md        │
│     .md        │  │    guide.md    │  │ (orchestrator) │
└────────┬───────┘  └────────┬───────┘  └────────┬───────┘
         │                   │                   │
         └───────────────────┼───────────────────┘
                             ▼
                    ┌─────────────────┐
                    │  SUBAGENTS      │
                    │  (parallel)     │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
┌────────────────┐  ┌────────────────┐  ┌────────────────┐
│   index.md     │  │ _analysis_log  │  │ _validation_   │
│  (per paper)   │  │    .md         │  │    report.md   │
└────────────────┘  └────────────────┘  └────────────────┘
```

**Implementation**:
- Extract all INPUT/OUTPUT patterns
- Build directed graph
- Use D3.js force layout or dagre
- Color by file type (config vs generated vs output)

### Feature 4: Subagent Architecture View

```
STEP 2: Analyze Papers
┌─────────────────────────────────────────────────────────────┐
│  SUBAGENT SPAWN                                             │
│  ─────────────────                                          │
│  Type: general-purpose                                      │
│  Concurrency: max 15 parallel                               │
│  Timeout: 5 min per paper                                   │
│  Retry: 1 attempt                                           │
│                                                             │
│  ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ... (15 slots)        │
│  │ ▶ │ │ ▶ │ │ ▶ │ │ ▶ │ │ ▶ │ │ ▶ │                        │
│  └───┘ └───┘ └───┘ └───┘ └───┘ └───┘                        │
│                                                             │
│  INPUT CONTRACT:                                            │
│  ├─ 03-skills/research-pipeline/shared/paper-analyze-core   │
│  ├─ {project_path}/02-resources/_briefing.md                │
│  ├─ {project_path}/02-resources/_analysis_kit.md            │
│  └─ {paper_path}/*.md chunks                                │
│                                                             │
│  OUTPUT:                                                    │
│  ├─ {paper_path}/index.md                                   │
│  └─ {paper_path}/_analysis_log.md                           │
└─────────────────────────────────────────────────────────────┘
```

**Implementation**:
- Parse `Task(...)` patterns
- Extract concurrency from comments
- Parse INPUT CONTRACT sections
- Show parallel execution slots

### Feature 5: Token Budget Visualization (Synthesis)

```
LEVEL 7: FINAL REPORT
┌─────────────────────────────────────────────────────────────┐
│  TOKEN BUDGET                                               │
│  ─────────────                                              │
│  ████████████████████░░░░░░░░░░  75,000 / 100,000           │
│                                                             │
│  Components:                                                │
│  ├─ Methodology:     3,000  ███                             │
│  ├─ Briefing:        2,050  ██                              │
│  ├─ Synthesis files: 45,000 █████████████████████████       │
│  ├─ Output reserve:  20,000 ██████████                      │
│  └─ Usable:          29,950 ██████████████                  │
│                                                             │
│  Status: ✓ No split required                                │
└─────────────────────────────────────────────────────────────┘
```

**Implementation**:
- Parse token budget tables from markdown
- Create progress bar visualization
- Show split strategy if needed

### Feature 6: Gates and User Decisions

```
┌─────────────────────────────────────────────────────────────┐
│  🚪 USER GATE: Selection Gate                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────┐     ┌─────────────────────┐        │
│  │  [Y] Approve        │────▶│  → acquisition      │        │
│  │  Continue to next   │     │  Phase B starts     │        │
│  └─────────────────────┘     └─────────────────────┘        │
│                                                             │
│  ┌─────────────────────┐     ┌─────────────────────┐        │
│  │  [N] Reject         │────▶│  → back to search   │        │
│  │  Refine selection   │     │  Step 3 repeats     │        │
│  └─────────────────────┘     └─────────────────────┘        │
│                                                             │
│  ┌─────────────────────┐     ┌─────────────────────┐        │
│  │  [S] Skip           │────▶│  → end session      │        │
│  │  Save progress      │     │  Resume later       │        │
│  └─────────────────────┘     └─────────────────────┘        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Implementation**:
- Parse [Y]/[N]/[S] options
- Show decision tree branching
- Indicate handoff targets

### Feature 7: Script vs Subagent Indicator

```
┌──────────────────────────────────────────────────────────────────┐
│ LEVEL 1: ROUTING           ⚙️ SCRIPT (deterministic)             │
├──────────────────────────────────────────────────────────────────┤
│ python build_synthesis_routing.py                                 │
│ Algorithm: Boolean lookup from chunk_index.fields_found           │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│ LEVEL 4: EXTRACTION        🤖 SUBAGENT (LLM)                     │
├──────────────────────────────────────────────────────────────────┤
│ Spawn: max 15 parallel Task(subagent_type="general-purpose")     │
│ Output: 03-working/_batch_{field}_{N}.yaml                       │
└──────────────────────────────────────────────────────────────────┘
```

**Implementation**:
- Detect script blocks vs Task spawns
- Color code: orange=script, purple=subagent
- Show which levels are deterministic

---

## UI/UX Improvements

### Better Layout
- Full viewport canvas with zoom/pan
- Minimap for navigation
- Sticky header with breadcrumb

### Better Styling
- Modern GitHub-like dark theme (already have)
- Smooth animations on expand/collapse
- Tooltips for truncated content
- Keyboard navigation (j/k for steps, Enter to expand)

### Better Information Density
- Card-based nodes with preview info
- Hover to see full content
- Search/filter by step name or content
- Status indicators (ready, in-progress, blocked)

---

## Technical Architecture

```python
# visualizer_v3.py

@dataclass
class Orchestrator:
    name: str
    path: Path
    phases: List[Phase]
    handoff_from: Optional[str]
    handoff_to: Optional[str]

@dataclass
class Phase:
    letter: str
    name: str
    steps: List[Step]

@dataclass
class Step:
    id: str
    number: str
    name: str
    description: str
    sub_steps: List[SubStep]
    inputs: List[FileRef]
    outputs: List[FileRef]
    scripts: List[str]
    subagent_spawn: Optional[SubagentConfig]
    user_gate: Optional[Gate]
    handoff_to: Optional[str]

@dataclass
class SubagentConfig:
    type: str
    concurrency: int
    timeout: str
    input_contract: List[str]
    output_contract: List[str]

@dataclass
class Gate:
    options: List[GateOption]

@dataclass
class GateOption:
    key: str  # Y, N, S
    label: str
    target: str

@dataclass
class FileRef:
    path: str
    type: str  # input, output, config
    format: str  # md, yaml, json

# New: Build file dependency graph
def build_dependency_graph(orchestrators: List[Orchestrator]) -> Dict:
    nodes = set()  # files
    edges = []  # step -> file or file -> step

    for orch in orchestrators:
        for phase in orch.phases:
            for step in phase.steps:
                for inp in step.inputs:
                    edges.append((inp.path, step.id, "input"))
                for out in step.outputs:
                    edges.append((step.id, out.path, "output"))

    return {"nodes": list(nodes), "edges": edges}
```

---

## Implementation Steps

1. **Parse all 3 orchestrators** (~30 min)
   - Update parser to handle multi-skill
   - Extract handoff relationships

2. **Build dependency graph** (~30 min)
   - Collect all file references
   - Build edges

3. **Create React-like component structure in HTML** (~1 hr)
   - Pipeline overview component
   - Orchestrator detail component
   - Step detail component
   - File graph component

4. **Add interactivity** (~1 hr)
   - Expand/collapse
   - Search/filter
   - Keyboard nav

5. **Polish styling** (~30 min)
   - Animations
   - Token budget bars
   - Subagent slot visualization

---

## Files to Create

| File | Purpose |
|------|---------|
| `visualize_pipeline.py` | Main script - parses all 3 orchestrators |
| `research_pipeline_flow.html` | Single HTML output for entire pipeline |

---

## Success Criteria

- [ ] Shows all 3 orchestrators with handoff arrows
- [ ] Drill into phases → steps → sub-steps
- [ ] See all inputs/outputs per step
- [ ] See subagent spawn details (concurrency, timeout, contract)
- [ ] See user gates with decision branches
- [ ] See token budgets (synthesis)
- [ ] File dependency graph view
- [ ] Search and filter
- [ ] Actually looks good (modern, dark, professional)

---

*Created: 2026-01-01*
