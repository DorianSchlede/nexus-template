---
name: skip-onboarding
description: Load when user says "skip onboarding", "exit onboarding", "I already know Nexus", or "mark onboarding complete". Validates minimum requirements and allows early exit from onboarding flow.
---

# Skip Onboarding Skill

**Purpose:** Allow users who already know Nexus to exit onboarding early with proper validation.

---

## Trigger Keywords

- "skip onboarding"
- "exit onboarding"
- "I already know Nexus"
- "mark onboarding complete"
- "finish onboarding early"

---

## Workflow

### Step 1: Validate Minimum Requirements

Run validation checks:

```python
# Check Requirement A: Memory Initialized
memory_files = [
    '01-memory/goals.md',
    '01-memory/roadmap.md',
    '01-memory/user-config.yaml'
]
memory_initialized = all(file_exists(f) for f in memory_files)

# Check Requirement B: Workspace Created
workspace_initialized = (
    file_exists('04-workspace/workspace-map.md') and
    has_folders_in('04-workspace/')
)
```

**Requirements Mapping:**
- **Requirement A (Memory)**: Completed in Project 00 (Define Goals)
- **Requirement B (Workspace)**: Completed in Project 01 (First Project)

---

### Step 2: Handle Based on Validation Status

#### **Case 1: BOTH Requirements Met** ✅✅

```
Display:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ ONBOARDING REQUIREMENTS MET
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Memory initialized (goals.md, roadmap.md, user-config.yaml)
✅ Workspace created (workspace-map.md + folders)

You've completed the essential setup!

Would you like me to mark all onboarding projects as complete?
This will:
- Mark Projects 00, 01, 02, 03 as COMPLETE
- Remove onboarding suggestions from menu
- Show regular work suggestions instead

Say "yes" to complete onboarding, or "no" to continue learning.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**If user says "yes":**
1. Run: `python 00-system/core/bulk-complete-onboarding.py`
2. Display completion message
3. Show next steps

**If user says "no":**
1. Acknowledge: "No problem! Continue onboarding at your own pace."
2. Return to menu

---

#### **Case 2: Only Memory Initialized** ✅❌

```
Display:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  PARTIAL SETUP COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Memory initialized
❌ Workspace not created yet

To skip onboarding, you need workspace structure set up.

Options:

1️⃣  Complete Project 01 (First Project) - 15 minutes
   → Sets up workspace structure properly
   → Teaches workspace organization
   → Then you can skip remaining projects

2️⃣  Create workspace manually:
   → Create 04-workspace/workspace-map.md
   → Add at least one folder in 04-workspace/
   → Then say "skip onboarding" again

Which would you prefer?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Actions:**
- If user chooses Option 1: Load Project 01
- If user chooses Option 2: Provide guidance, wait for completion
- If user creates workspace manually: Re-run validation

---

#### **Case 3: Nothing Initialized** ❌❌

```
Display:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  ESSENTIAL SETUP REQUIRED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ Memory not initialized
❌ Workspace not created

To use Nexus effectively, you need at least:
- Memory initialized (your goals, role, preferences)
- Workspace structure (organized file system)

This takes 20-25 minutes total across 2 projects.

Let's start with Project 00 (Define Goals) - 9-11 minutes.
This creates your persistent memory so I can remember you.

Ready to begin?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Actions:**
- If user says "yes": Load Project 00
- If user says "no": Acknowledge and return to menu

---

### Step 3: Post-Skip Actions (After Bulk Completion)

```
Display:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎉 ONBOARDING COMPLETE!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ All onboarding projects marked complete
✅ Memory system initialized
✅ Workspace structure created
✅ You're ready to work!

Next steps:
• Create your first real project: "create project for [goal]"
• Create a reusable skill: "create skill for [workflow]"
• Learn advanced features: "explain Nexus"

Or just tell me naturally what you want to work on.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Edge Cases

### User Says "Tasks Already Complete"

If user mentions tasks are already done but not marked:

```
"Got it! Let me mark them complete.

Running bulk-complete-tasks for current project..."

[Run: python 00-system/skills/bulk-complete/scripts/bulk-complete.py --project <project-id> --all --no-confirm]

✅ All tasks marked complete

Want to continue onboarding or skip remaining projects?
```

---

## Notes

- This skill validates before allowing skip
- Ensures minimum viable setup exists
- Provides clear options at each stage
- Gracefully handles partial completion
- Works with bulk-complete-onboarding.py script
