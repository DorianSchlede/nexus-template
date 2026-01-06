# Nexus Workflow Studio Integration - Plan

**Last Updated**: 2026-01-01

---

## Approach

Fork cc-wf-studio and extend it with Nexus-specific capabilities:

1. **Phase 1 - Foundation**: Type system + extension services
2. **Phase 2 - UI**: Node components + property panels
3. **Phase 3 - Integration**: Import/export + skill discovery
4. **Phase 4 - Testing**: E2E validation + documentation

Key principle: Follow existing cc-wf-studio patterns exactly - every new feature mirrors an existing one.

---

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **Fork vs Extend** | Fork | Need significant customization, avoid upstream conflicts |
| **Custom nodes vs Skill wrapper** | Custom nodes (4 types) | Clear semantics, native UI, proper validation |
| **Metadata storage** | In workflow JSON | Consistent with existing patterns (MCP, Skill nodes) |
| **Export format** | Dual: .claude + SKILL.md | Support both ecosystems |
| **Bidirectional sync** | Yes, with warnings | Users expect visual edits to persist |

---

## Resources Needed

**Tools/Access**:
- Node.js 18+ (already have)
- VSCode Extension development environment
- TypeScript 5.3+
- React 19 (webview)

**Codebase Knowledge**:
- cc-wf-studio architecture (ULTRARESEARCH complete)
- Nexus SKILL.md format (analyzed)
- nexus-loader.py metadata schema

**Reference Files**:
- `04-workspace/cc-wf-studio/` - Source repository (cloned)
- `03-skills/research-pipeline/` - Example skill-chain to visualize
- `00-system/.cache/context_startup.json` - Nexus metadata format

---

## Dependencies & Links

**Files in cc-wf-studio to Modify**:

| File | Change |
|------|--------|
| `src/shared/types/workflow-definition.ts` | Add NodeType enums + interfaces |
| `src/shared/types/messages.ts` | Add Nexus message types |
| `src/extension/services/export-service.ts` | Add Nexus export handlers |
| `src/extension/utils/validate-workflow.ts` | Add Nexus validation |
| `src/webview/src/components/NodePalette.tsx` | Add Nexus node buttons |
| `src/webview/src/components/PropertyOverlay.tsx` | Route to Nexus panels |
| `resources/workflow-schema.json` | Add Nexus node schemas |

**New Files to Create**:

| File | Purpose |
|------|---------|
| `src/extension/services/nexus-skill-discovery.ts` | Scan 03-skills/ |
| `src/extension/services/nexus-project-loader.ts` | Load project metadata |
| `src/extension/commands/nexus-integration.ts` | Handle Nexus messages |
| `src/webview/src/components/nodes/OrchestratorNode.tsx` | Render Orchestrator |
| `src/webview/src/components/nodes/PhaseNode.tsx` | Render Phase |
| `src/webview/src/components/nodes/NexusSubSkillNode.tsx` | Render SubSkill |
| `src/webview/src/components/nodes/ProjectNode.tsx` | Render Project |
| `src/webview/src/components/property-panels/` (4 files) | Node property editors |

**External Dependencies**:
- cc-wf-studio upstream: https://github.com/breaking-brake/cc-wf-studio
- Nexus skill format: `03-skills/**/SKILL.md`
- Nexus metadata: `00-system/.cache/context_startup.json`

---

## Technical Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                    Nexus Workflow Studio                     │
├─────────────────────────────────────────────────────────────┤
│  Extension Host                                              │
│  ├─ nexus-skill-discovery.ts  → Scan 03-skills/             │
│  ├─ nexus-project-loader.ts   → Read project metadata       │
│  ├─ nexus-integration.ts      → Handle Nexus messages       │
│  └─ export-service.ts         → Export to SKILL.md          │
├─────────────────────────────────────────────────────────────┤
│  Webview (React)                                             │
│  ├─ Nexus Node Components     → 4 visual node types         │
│  ├─ Nexus Property Panels     → 4 configuration UIs         │
│  ├─ Nexus Section in Palette  → Drag-and-drop source        │
│  └─ vscode-bridge extensions  → Nexus API calls             │
├─────────────────────────────────────────────────────────────┤
│  Shared Types                                                │
│  ├─ workflow-definition.ts    → Nexus node interfaces       │
│  └─ messages.ts               → Nexus message types         │
└─────────────────────────────────────────────────────────────┘
            │                           │
            ▼                           ▼
    ┌───────────────┐           ┌───────────────┐
    │ 03-skills/    │           │ 02-projects/  │
    │ SKILL.md files│           │ Project data  │
    └───────────────┘           └───────────────┘
```

### Data Flow

```
IMPORT: SKILL.md → Parse frontmatter → Create Skill node → Add to workflow
EXPORT: Workflow → Serialize nodes → Generate SKILL.md → Write to 03-skills/
```

### Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Extension | TypeScript | 5.3 |
| Webview | React + Zustand | 19 + 5.0 |
| Canvas | React Flow | 11.10 |
| Build | Vite | 7.3 |
| Lint | Biome | 2.3 |

---

## Implementation Strategy

### Phase 1: Foundation (Days 1-2)

**Goal**: Type system complete, extension services scaffolded

Tasks:
1. Add NodeType enum values (4 types)
2. Define interfaces for each Nexus node
3. Create nexus-skill-discovery.ts (scan 03-skills/)
4. Create nexus-project-loader.ts (read metadata)
5. Add Nexus message types to messages.ts

**Validation**: TypeScript compiles, no runtime errors

### Phase 2: UI Components (Days 3-6)

**Goal**: All 4 node types visible and configurable

Tasks:
1. Create 4 node components (follow existing patterns)
2. Create 4 property panel components
3. Add Nexus section to NodePalette
4. Wire PropertyOverlay to new panels
5. Add handlers for node add/delete/update

**Validation**: Can add all 4 node types, configure properties

### Phase 3: Integration (Days 7-10)

**Goal**: Full import/export working

Tasks:
1. Implement SKILL.md import parser
2. Implement SKILL.md export generator
3. Wire nexus-skill-discovery to SkillBrowserDialog
4. Add "Import Nexus Skill" command
5. Add "Export as SKILL.md" command

**Validation**: Can import research-pipeline/SKILL.md and export back

### Phase 4: Testing & Docs (Days 11-13)

**Goal**: Production-ready extension

Tasks:
1. Unit tests for type validation
2. Unit tests for export logic
3. E2E: Create workflow with Nexus nodes
4. E2E: Import/export roundtrip
5. Update CLAUDE.md with development guide
6. Build and test VSIX package

**Validation**: All tests pass, VSIX installs cleanly

---

## Mental Models Applied (ULTRATHINK Session)

### First Principles Analysis

**Core question**: What's the absolute core problem we're solving?

**Assumptions challenged**:
| Assumption | Challenge | Fundamental Truth |
|------------|-----------|-------------------|
| Need to fork | Could we use MCP to extend? | **Fork is optional** - MCP server could expose Nexus data to existing editor |
| 4 node types | What's the minimum? | **1 node type** (NexusSkill) could represent all - orchestrator/skill is metadata |
| Bidirectional | What do users actually need? | **Import is primary** - users want to SEE existing skills, export is secondary |
| Visual editing | Why visual? | **Understanding complex flows** - the real value is comprehension, not creation |

**INSIGHT**: The fundamental need is **understanding skill-chain structure**, not necessarily editing. A read-only visualizer might deliver 80% of the value with 20% of the effort.

**Alternative approaches discovered**:
- **Option A (Original)**: Full fork + 4 custom nodes + bidirectional (~13 days)
- **Option B (Minimal)**: MCP server exposes Nexus skills → existing cc-wf-studio visualizes (~4 hours)
- **Option C (Middle)**: Import-only + 1 generic NexusSkill node type (~3 days)

### Inversion: What Would Guarantee Failure?

**Failure recipes identified**:
1. Overengineer from day 1 - Build all 4 node types before testing if 1 works
2. Ignore upstream changes - Fork and never sync, get left behind
3. Perfect bidirectional sync - Spend weeks on edge cases nobody uses
4. Skip the MCP option - Build custom when existing infrastructure works
5. No user testing - Build what we think users want, not what they need

**Anti-patterns to AVOID**:
- ❌ Building before validating the use case
- ❌ Custom solution when existing tools suffice
- ❌ Full feature set before MVP
- ❌ Ignoring the MCP server approach

### Second-Order Thinking: Consequences of Consequences

**Fork decision chain**:
- **1st order**: Visual workflow editing works
- **2nd order**: Must maintain fork (ongoing cost), upstream updates require merge
- **3rd order**: Fork diverges → harder to merge, "visual" becomes expected interface
- **4th order**: System complexity increases, visual editor becomes a dependency

**MCP decision chain**:
- **1st order**: Nexus exposes skills via MCP
- **2nd order**: Any MCP-compatible editor can visualize (not just cc-wf-studio)
- **3rd order**: Zero maintenance - cc-wf-studio updates just work
- **4th order**: Other tools can consume the same MCP interface

**INSIGHT**: Forking creates **maintenance burden that compounds**. MCP approach has better long-term economics.

### Pre-Mortem: 6 Months Later This Failed

**Failure mode 1: Overbuilt**
- Built all 4 node types, property panels, export/import
- Took 3 weeks instead of 3 days
- By completion, priorities changed → never used
- **Prevention**: Build ONE thing, test if valuable, then expand

**Failure mode 2: MCP would have worked**
- Discovered after building that MCP server + existing cc-wf-studio = same result
- Wasted weeks on custom code
- **Prevention**: Prototype MCP approach in 2 hours first

**Failure mode 3: Wrong abstraction**
- Built around "visual editing" but users just wanted "understanding"
- Read-only visualizer would have been enough
- **Prevention**: Validate use case with users first

**HIGHEST RISK**: Building the wrong thing (visual editor) when users just need visualization.

---

## Revised Approach (Post-Mental-Models)

### NEW Phase 0: MCP Validation (2-4 hours) ⭐ CRITICAL
- [ ] Build minimal `nexus-skills` MCP server
- [ ] Expose: skill list, skill metadata, skill hierarchy
- [ ] Test: Does cc-wf-studio show Nexus skills as Skill nodes?
- [ ] **GO/NO-GO**: If MCP works → skip fork entirely

### Phase 1: Minimal Viable Visualizer (1-2 days)
- [ ] IF MCP insufficient: Add ONE node type (NexusSkill)
- [ ] Import only (no export)
- [ ] Test with research-pipeline skill-chain
- [ ] **VALIDATE**: Is this useful? Continue or stop?

### Phase 2: Enhanced Nodes (3-4 days)
- [ ] Only if Phase 1 validated by user
- [ ] Add Orchestrator and Phase distinction
- [ ] Add property panels

### Phase 3: Bidirectional (5+ days)
- [ ] Only if users explicitly request
- [ ] Export to SKILL.md
- [ ] Full sync

---

## Pre-Mortem Risk Inventory

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Overbuilding before validation | HIGH | HIGH | Phase 0 MCP test first |
| Fork maintenance burden | MEDIUM | HIGH | Minimize changes, use extension points |
| Upstream breaking changes | MEDIUM | MEDIUM | Pin version, document delta |
| Wrong feature (edit vs view) | HIGH | HIGH | User interview before Phase 2 |
| SKILL.md parser complexity | MEDIUM | LOW | Start with happy path only |

---

## Open Questions

- [x] Should we try MCP first before forking? → **YES, mandatory Phase 0**
- [ ] Is visualization enough or is editing required?
- [ ] Should we support nested skill-chains in the visual editor?
- [ ] How to handle skill dependencies (e.g., paper-analyze-core is "DO NOT LOAD DIRECTLY")?

---

*Next: Complete steps.md to break down execution*
