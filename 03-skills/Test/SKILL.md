---
name: Test
description: [TODO: Complete and informative explanation of what the skill does and when to use it. Include WHEN to use this skill - specific scenarios, file types, or tasks that trigger it. Be specific and include key terms for discoverability.]
---

# Test

[TODO: One-line purpose statement - what this skill does in 1 sentence]

## Purpose

[TODO: 2-3 sentences explaining:
- What this skill does
- When to use it
- Why it's useful]

**Key Features** (optional):
- [TODO: Feature 1]
- [TODO: Feature 2]
- [TODO: Feature 3]

**Time Estimate** (optional): [TODO: X-Y minutes]

---

## Workflow

### Step 1: Initialize TodoList

Create TodoWrite with all workflow steps:
```
- [ ] [TODO: First step description]
- [ ] [TODO: Second step description]
- [ ] [TODO: Third step description]
- [ ] [TODO: Additional steps as needed]
- [ ] Close session to save progress
```

This creates transparency and allows progress tracking.

**Mark tasks complete as you finish each step.**

---

### Step 2: [TODO: First Work Step Name]

[TODO: Describe what happens in this step]

**Actions**:
1. [TODO: Action 1]
2. [TODO: Action 2]
3. [TODO: Action 3]

**If loading resources:**
- Load [references/file-name.md](references/file-name.md) for [purpose]
- Execute scripts/script-name.py for [task]

**Mark this todo complete before proceeding.**

---

### Step 3: [TODO: Second Work Step Name]

[TODO: Describe what happens in this step]

**Mark this todo complete before proceeding.**

---

### Step N: [TODO: Add More Steps as Needed]

[TODO: Add additional workflow steps here]

**Mark this todo complete before proceeding.**

---

### Step N-1: Share to Team (Optional but Recommended)

After your skill is ready, consider sharing it with the team via Notion:

**Benefits of sharing:**
- Team discovers and reuses your work
- Collaborative improvement (others can update)
- Centralized skill library for the company

**To share:**
Say "export this skill to Notion" or use the `export-skill-to-notion` skill.

**What happens:**
1. AI packages the skill (or uses existing .skill file)
2. AI infers Team (General/Solutions/Engineering/Sales)
3. You confirm metadata before pushing
4. Skill appears in "Beam Nexus Skills" database with full .skill file attached
5. Teammates can query and import with `query-notion-db` and `import-skill-to-nexus`

**Skip this if:**
- Skill is personal/experimental/not ready to share
- Contains sensitive or client-specific info

**Mark this todo complete after deciding (share or skip).**

---

### Final Step: Close Session

Once the workflow is complete, **automatically trigger the close-session skill**:

```
Auto-triggering close-session to save progress...
```

The close-session skill will:
- Update system memory
- Save context for next session
- Create session report
- Clean up temporary files

**This is the final mandatory step.** Do not skip - it ensures all progress is preserved.

---

## Resources

This skill includes example resource directories for bundled resources:

### scripts/
Executable code (Python/Bash/etc.) for deterministic operations.

**Example**: scripts/example.py - Placeholder script (customize or delete)

### references/
Documentation loaded into context as needed.

**Example**: references/api_reference.md - Placeholder docs (customize or delete)

### assets/
Files used in output, not loaded into context.

**Example**: assets/example_asset.txt - Placeholder asset (customize or delete)

**Delete any unneeded directories.** Not every skill requires all three types of resources.

---

## Notes

[TODO: Add any important notes, tips, warnings, or best practices]

**About [Topic]:**
- [TODO: Note 1]
- [TODO: Note 2]
