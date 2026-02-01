---
name: create-folders
description: "create folders, setup workspace, organize folders, where to put files."
onboarding: true
priority: high
---

## [TARGET] AI Proactive Triggering (ONBOARDING SKILL)

**This is an ONBOARDING skill with HIGH PRIORITY. Natural follow-up after setup-memory.**

### When to Proactively Suggest

Check `learning_tracker.completed.create_folders` in user-config.yaml. If `false`:

**PROACTIVELY SUGGEST when user:**
1. Just completed setup-memory (natural next step)
2. Asks where to save files or how to organize work
3. Creates files in wrong locations
4. Mentions file organization, folder structure, or workspace setup
5. At menu display when `workspace_configured: false`

**Menu Integration:**
```
[DIR] FOLDERS
   Not configured ▸ 'create folders' (5 min)
```

**DO NOT suggest if:**
- `learning_tracker.completed.create_folders: true`
- User has already organized 04-workspace/ manually

---

# Create Folders

Guide user through workspace folder design.

## Purpose

Create a practical folder structure in `04-workspace/` based on user's work patterns. These are **normal folders like on any computer** - the user can browse them in the sidebar, drag files in, rename them anytime.

**Time Estimate**: 5-8 minutes

---

## Workflow

### CRITICAL: Initialize Todo List

**FIRST ACTION when skill loads** - Create todo list to track progress:

```
TodoWrite:
1. [ ] Explain what workspace is
2. [ ] Understand user's work patterns
3. [ ] Design folder structure together
4. [ ] Create folders
5. [ ] Finalize and document
```

---

### Step 1: Welcome & Explain

**Display**:
```
[DIR] WORKSPACE SETUP

Let's organize your workspace - this is where YOUR files live.
```

**Explain clearly**:
```
Think of 04-workspace/ like a folder on your computer.

┌─────────────────────────────────────┐
│  📂 SIDEBAR (left)                  │
│  ├── 00-system/    ← Nexus brain    │
│  ├── 01-memory/    ← Your goals     │
│  ├── 02-builds/    ← Active work    │
│  ├── 03-skills/    ← Automations    │
│  └── 04-workspace/ ← YOUR FILES ◀── │
└─────────────────────────────────────┘

04-workspace/ is yours:
• Drag files directly into folders
• Create new folders anytime
• Organize however you want

We'll set up a starting structure now. You can always change it later.
```

---

### Step 2: Understand Work Patterns

**Read** goals.md for context about user's role and work focus.

**Ask**: "What kinds of files and content do you work with? For example: documents, research, client work, projects, notes..."

**Listen for patterns** - the AI needs to understand:
- What "things" does the user deal with? (clients, projects, topics, products...)
- What "phases" does work go through? (draft → review → done, inbox → processing → output...)

---

### Step 3: Design Structure (AI KNOWLEDGE - NOT SHOWN TO USER)

**AI uses these principles internally to guide the conversation:**

#### Two Fundamental Organization Principles:

**A) Process-based (by status/phase)**
```
├── inbox/          → What comes in
├── active/         → What you're working on
├── done/           → What's finished
└── archive/        → Old stuff
```
*Best for: Clear workflows, pipelines, status-driven work*

**B) Entity-based (by thing/object)**
```
├── clients/        → One folder per client
├── projects/       → One folder per project
├── topics/         → One folder per topic
└── templates/      → Reusable stuff
```
*Best for: Many similar things to track, relationship-driven work*

**C) Hybrid (both combined)**
```
├── clients/              → Entity
│   └── client-a/
│       ├── inbox/        → Process
│       ├── active/
│       └── done/
```

#### How AI applies this:

1. **Listen** to how user describes their work
2. **Identify** whether they think in "phases" or "things"
3. **Suggest** appropriate structure based on their patterns
4. **Don't lecture** about theory - just propose practical folders

**Example conversation:**
- User: "I work with different clients and each has ongoing projects"
- AI thinks: Entity-based (clients as primary), maybe hybrid with status
- AI suggests: `clients/`, `templates/`, `archive/` with subfolders per client

**Example conversation:**
- User: "I collect research, process it, then publish articles"
- AI thinks: Process-based (clear phases)
- AI suggests: `research/`, `drafts/`, `published/`, `archive/`

---

### Step 4: Propose & Iterate

**Propose 3-7 folders** based on user's work patterns.

**Show visually**:
```
Based on your work, here's a starting structure:

[DIR] 04-workspace/
├── [folder 1]/     ← [short description]
├── [folder 2]/     ← [short description]
├── [folder 3]/     ← [short description]
└── context/        ← Already exists (your uploaded docs)

Does this work? We can add, remove, or rename anything.
```

**Iterate** until user is happy. Keep it simple - 3-7 folders max to start.

**Remind**: "You can always add more folders later. Start simple."

---

### Step 5: Create Folders

**Create** agreed structure in 04-workspace/:

```bash
mkdir -p 04-workspace/[folder1]
mkdir -p 04-workspace/[folder2]
# etc.
```

**Note**: `04-workspace/context/` already exists from setup-memory (if they uploaded files).

---

### Step 6: Update Workspace Map

**Create/update** `04-workspace/workspace-map.md`:

```markdown
# Workspace Map

> Your file organization in 04-workspace/
> Last updated: [date]

## Folder Structure

[folder tree with descriptions]

## Organization Principle

[Brief note: process-based / entity-based / hybrid]

## Usage Notes

[Any user-specified notes]
```

---

### Step 7: Finalize

**Actions** (MUST complete all):

1. **Mark skill complete** in user-config.yaml:
   ```yaml
   learning_tracker:
     completed:
       create_folders: true
   ```

2. **Set workspace configured**:
   ```yaml
   workspace_configured: true
   ```

3. **Display completion**:
   ```
   [OK] Workspace Setup Complete!

   ---------------------------------------------------------

   CREATED:
   [DIR] 04-workspace/
   ├── [list created folders]
   └── workspace-map.md

   ---------------------------------------------------------

   [DIR] HOW TO USE:

   • Drag files directly into folders (in the sidebar)
   • Create new subfolders anytime you need them
   • Rename or reorganize whenever - it's your space

   ---------------------------------------------------------

   🎉 ONBOARDING COMPLETE!

   Your system foundation is ready:
   [OK] Memory configured (who you are, your goals)
   [OK] Workspace organized (where your files live)

   ---------------------------------------------------------

   🏗️ YOUR SYSTEM NOW:

   ┌─────────────────────────────────────────────────────┐
   │  🧠 MEMORY     [OK] Ready (01-memory/)                 │
   │                  Loaded automatically every session │
   │                                                     │
   │  [DIR] WORKSPACE  [OK] Ready (04-workspace/)              │
   │                  Your files, organized your way     │
   │                                                     │
   │  🏗️ BUILDS       Your tool to EXTEND the system     │
   │                  Build: software, integrations,     │
   │                  content, research, strategies,     │
   │                  processes - even new SKILLS        │
   │                                                     │
   │  [*] SKILLS       Repeatable workflows (created      │
   │                  through BUILDS, then reused)       │
   └─────────────────────────────────────────────────────┘

   The system grows with you:
   • BUILDS extend your system (8 types: software, integrations,
     research, strategy, content, process, skills, generic)
   • SKILLS are automated workflows you create through builds
   • Everything flows through your WORKSPACE

   ---------------------------------------------------------

   [GO] WHAT'S NEXT:

   Close this chat and open a NEW one.

   Why? Each chat = one focused task. Clean context = better results.

   In the next chat, just tell me what you want to work on:
   • "I want to build [something]" → We'll plan a BUILD
   • "Help me with [task]" → We'll get it done
   • "I do [X] every week" → We might create a SKILL

   ---------------------------------------------------------

   Optional deep-dives (anytime):
   • 'learn builds' - master project planning & execution
   • 'learn skills' - create your own automations

   See you in the next chat - time to build your system! [GO]
   ```

---

## Success Criteria

- [ ] User understands 04-workspace/ is their file space
- [ ] Work patterns understood (process vs entity based)
- [ ] 3-7 practical folders created
- [ ] workspace-map.md created with structure documentation
- [ ] `learning_tracker.completed.create_folders: true`
- [ ] `workspace_configured: true`
- [ ] User knows onboarding is complete
