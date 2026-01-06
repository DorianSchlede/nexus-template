# Nexus Workflow Studio Integration - Execution Steps

**Last Updated**: 2026-01-01

**IMPORTANT**: This file tracks project progress. Mark tasks complete with [x] as you finish them.

---

## Phase 0: Setup & Planning

- [x] Clone cc-wf-studio repository
- [x] ULTRARESEARCH architecture analysis
- [x] Complete overview.md
- [x] Complete plan.md
- [x] Complete steps.md
- [x] ULTRATHINK mental models analysis
- [ ] Review with stakeholder

---

## Phase 0.5: MCP Validation (2-4 hours) ⭐ CRITICAL GATE

> **MENTAL MODEL INSIGHT**: First Principles + Pre-Mortem revealed that an MCP server
> might deliver 80% of value with 20% of effort. Test this BEFORE forking.

### 0.5.1 Build Minimal MCP Server
- [ ] Create `nexus-skills-mcp/` in 03-skills/ or separate repo
- [ ] Implement `list_skills` tool - returns all SKILL.md files
- [ ] Implement `get_skill` tool - returns skill metadata + content
- [ ] Implement `get_skill_hierarchy` tool - returns parent/child structure
- [ ] Test MCP server standalone with `mcp dev`

### 0.5.2 Test with cc-wf-studio
- [ ] Configure cc-wf-studio to use nexus-skills-mcp server
- [ ] Add MCP node pointing to nexus-skills server
- [ ] Can we visualize research-pipeline skill-chain?
- [ ] Document what works and what doesn't

### 0.5.3 GO/NO-GO Decision
- [ ] **If MCP sufficient**: Stop here, project complete with minimal effort
- [ ] **If MCP insufficient**: Document gaps, proceed to Phase 1
- [ ] Update plan.md with decision and rationale

---

## Phase 1: Foundation (Days 1-2)

> **Only proceed if Phase 0.5 shows MCP is insufficient**

### 1.1 Type System Setup
- [ ] Add NodeType enum values to workflow-definition.ts
  - [ ] `NexusOrchestrator = 'nexusOrchestrator'`
  - [ ] `NexusPhase = 'nexusPhase'`
  - [ ] `NexusSubSkill = 'nexusSubSkill'`
  - [ ] `NexusProject = 'nexusProject'`
- [ ] Define OrchestratorNodeData interface
  - [ ] `orchestratorId: string`
  - [ ] `orchestratorPath: string`
  - [ ] `description: string`
  - [ ] `childSkills: string[]`
  - [ ] `validationStatus: 'valid' | 'missing' | 'invalid'`
- [ ] Define PhaseNodeData interface
  - [ ] `phaseType: 'planning' | 'execution' | 'review' | 'custom'`
  - [ ] `phaseLabel: string`
  - [ ] `projectId?: string`
- [ ] Define NexusSubSkillNodeData interface
  - [ ] `skillId: string`
  - [ ] `skillPath: string`
  - [ ] `scope: 'personal' | 'project' | 'nexus'`
  - [ ] `nexusMetadata?: { category, version }`
- [ ] Define ProjectNodeData interface
  - [ ] `projectId: string`
  - [ ] `projectName: string`
  - [ ] `projectStatus: string`
  - [ ] `projectProgress: number`
- [ ] Add type union to WorkflowNode type
- [ ] Run TypeScript compile check

### 1.2 Extension Services
- [ ] Create `src/extension/services/nexus-skill-discovery.ts`
  - [ ] `findNexusRoot()` - Find parent with CLAUDE.md
  - [ ] `isNexusProject()` - Check for nexus markers
  - [ ] `scanNexusSkills()` - Glob 03-skills/**/SKILL.md
  - [ ] `parseNexusFrontmatter()` - Extract name, description, type
  - [ ] `getSkillHierarchy()` - Build parent/child tree
- [ ] Create `src/extension/services/nexus-project-loader.ts`
  - [ ] `loadNexusMetadata()` - Read context_startup.json
  - [ ] `getActiveProjects()` - Filter by status
  - [ ] `getProjectById()` - Single project lookup
- [ ] Add message types to messages.ts
  - [ ] `NEXUS_LOAD_SKILLS`
  - [ ] `NEXUS_SKILLS_LOADED`
  - [ ] `NEXUS_LOAD_PROJECTS`
  - [ ] `NEXUS_PROJECTS_LOADED`
  - [ ] `NEXUS_LOAD_ORCHESTRATORS`
  - [ ] `NEXUS_ORCHESTRATORS_LOADED`
- [ ] Verify extension compiles

---

## Phase 2: UI Components (Days 3-6)

### 2.1 Node Components
- [ ] Create `src/webview/src/components/nodes/OrchestratorNode.tsx`
  - [ ] Visual: Purple background, hub icon
  - [ ] Display: orchestratorId, child count
  - [ ] Handles: 1 input, 1 output
- [ ] Create `src/webview/src/components/nodes/PhaseNode.tsx`
  - [ ] Visual: Gradient based on phaseType
  - [ ] Display: phaseLabel, phase icon
  - [ ] Handles: 1 input, N outputs (per phase connections)
- [ ] Create `src/webview/src/components/nodes/NexusSubSkillNode.tsx`
  - [ ] Visual: Green background, skill icon
  - [ ] Display: skillId, scope badge
  - [ ] Handles: 1 input, 1 output
- [ ] Create `src/webview/src/components/nodes/ProjectNode.tsx`
  - [ ] Visual: Blue background, project icon
  - [ ] Display: projectName, progress bar
  - [ ] Handles: 1 input, 1 output
- [ ] Register all nodes in React Flow nodeTypes

### 2.2 Property Panels
- [ ] Create `src/webview/src/components/property-panels/OrchestratorPropertyPanel.tsx`
  - [ ] Dropdown: Select orchestrator from discovered list
  - [ ] Display: Child skills (read-only)
  - [ ] Button: "Open SKILL.md"
- [ ] Create `src/webview/src/components/property-panels/PhasePropertyPanel.tsx`
  - [ ] Select: Phase type (planning/execution/review/custom)
  - [ ] Input: Phase label
  - [ ] Optional: Link to project
- [ ] Create `src/webview/src/components/property-panels/NexusSubSkillPropertyPanel.tsx`
  - [ ] Browser: Skill selector with search
  - [ ] Display: Skill description
  - [ ] Badge: Scope (personal/project/nexus)
- [ ] Create `src/webview/src/components/property-panels/ProjectPropertyPanel.tsx`
  - [ ] Dropdown: Select from active projects
  - [ ] Display: Status, progress
  - [ ] Button: "Open project folder"
- [ ] Add cases to PropertyOverlay.tsx

### 2.3 Node Palette
- [ ] Add "Nexus" section to NodePalette.tsx
  - [ ] Conditional: Only show if isNexusProject()
  - [ ] Handlers: handleAddOrchestratorNode, etc.
  - [ ] Icons: Distinct from existing nodes
- [ ] Add position calculation for new nodes
- [ ] Test drag-and-drop for all 4 types

---

## Phase 3: Integration (Days 7-10)

### 3.1 SKILL.md Import
- [ ] Create `src/extension/commands/import-nexus-skill.ts`
  - [ ] File picker with SKILL.md filter
  - [ ] Parse frontmatter + content
  - [ ] Create workflow with single NexusSubSkill node
  - [ ] If skill-chain: Create multiple nodes with connections
- [ ] Add command: `nexus-workflow-studio.importSkillMd`
- [ ] Register in extension.ts
- [ ] Add keyboard shortcut

### 3.2 SKILL.md Export
- [ ] Add `generateNexusSkillMd()` to export-service.ts
  - [ ] Extract NexusSubSkill nodes
  - [ ] Generate YAML frontmatter
  - [ ] Generate routing table from connections
  - [ ] Generate workflow markdown
- [ ] Add command: `nexus-workflow-studio.exportAsSkillMd`
- [ ] Add to export dialog as option
- [ ] Handle skill-chain structure

### 3.3 Skill Discovery Integration
- [ ] Wire nexus-skill-discovery to vscode-bridge
  - [ ] `loadNexusSkills()` function
  - [ ] `loadNexusProjects()` function
  - [ ] `loadNexusOrchestrators()` function
- [ ] Update SkillBrowserDialog.tsx
  - [ ] Add "Nexus Skills" tab
  - [ ] Category filtering
  - [ ] Project filtering
- [ ] Cache skill list for performance
- [ ] Add refresh button

### 3.4 Message Bridge
- [ ] Add handlers in extension.ts for Nexus messages
- [ ] Add vscode-bridge functions for Nexus operations
- [ ] Test roundtrip: request → response

---

## Phase 4: Testing & Documentation (Days 11-13)

### 4.1 Unit Tests
- [ ] Test workflow-definition types
  - [ ] Valid Nexus node creation
  - [ ] Invalid node detection
- [ ] Test export-service.ts
  - [ ] Nexus node export format
  - [ ] SKILL.md generation
- [ ] Test nexus-skill-discovery.ts
  - [ ] Skill scanning
  - [ ] Hierarchy building

### 4.2 Integration Tests
- [ ] E2E: Add all 4 Nexus node types to workflow
- [ ] E2E: Configure each node via property panel
- [ ] E2E: Save and load workflow with Nexus nodes
- [ ] E2E: Export workflow as SKILL.md

### 4.3 Import/Export Roundtrip
- [ ] Import: 03-skills/research-pipeline/SKILL.md
- [ ] Verify: All orchestrators appear as nodes
- [ ] Modify: Add new connection
- [ ] Export: Save as SKILL.md
- [ ] Validate: Exported file is valid Nexus format

### 4.4 Documentation
- [ ] Update CLAUDE.md with Nexus development guide
- [ ] Document Nexus node types
- [ ] Document import/export workflow
- [ ] Add inline comments to new files

### 4.5 Build & Release
- [ ] Run `npm run build`
- [ ] Build VSIX package
- [ ] Test installation in fresh VSCode
- [ ] Verify all features work
- [ ] Tag release version

---

## Phase 5: Advanced Features (Future)

### 5.1 Skill-Chain Visualization
- [ ] Parse nested skill structure
- [ ] Generate SubAgentFlow for each level
- [ ] Auto-layout with dagre

### 5.2 Project Integration
- [ ] Read project steps.md
- [ ] Generate phase nodes from steps
- [ ] Two-way sync with project

### 5.3 Live Metadata
- [ ] Run nexus-loader.py for metadata
- [ ] WebSocket for live updates
- [ ] Status indicators on nodes

---

## Validation Checkpoints

| Checkpoint | Criteria | Status |
|------------|----------|--------|
| Types compile | `npm run typecheck` passes | [ ] |
| Extension loads | No errors in VSCode | [ ] |
| Nodes render | All 4 types visible | [ ] |
| Panels work | Can edit all properties | [ ] |
| Import works | SKILL.md → workflow | [ ] |
| Export works | workflow → SKILL.md | [ ] |
| Roundtrip valid | Import → edit → export → valid | [ ] |
| Tests pass | All unit + E2E tests | [ ] |
| VSIX installs | Clean install works | [ ] |

---

## Notes

**Current blockers**: None

**Dependencies**:
- cc-wf-studio source code (cloned to 04-workspace/)
- Nexus SKILL.md format documentation (analyzed)

---

*Mark tasks complete with [x] as you finish them*
