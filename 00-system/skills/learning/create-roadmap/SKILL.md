---
name: create-roadmap
description: "Create a prioritized roadmap of what to build next. Dynamic items based on your goals."
priority: high
duration: "3-5 min"
standalone: true
---

# Create Roadmap

Plan what to build next. AI suggests items based on your goals and context, you refine and prioritize.

---

## Purpose

- Transform vague goals into concrete BUILD items
- Prioritize by impact and dependencies
- Create a living document that guides your Nexus work

**Output**: `01-memory/roadmap.yaml`

---

## Pre-Execution

**Load context for personalization**:

```python
from pathlib import Path

# Check for existing context
goals_path = Path("01-memory/goals.md")
context_path = Path("01-memory/input/_analysis/analysis-summary.md")

has_goals = goals_path.exists()
has_context = context_path.exists()

if has_goals:
    goals_content = goals_path.read_text()

if has_context:
    context_content = context_path.read_text()
```

---

## Workflow

### Step 1: Understand Current State

**Display**:
```
CREATE ROADMAP
----------------------------------------------------

Let's plan what you'll build.

I'll suggest items based on:
  [[OK]] Your goals (01-memory/goals.md)
  [[OK]/[FAIL]] Context analysis (if uploaded)
  [[OK]/[FAIL]] Existing builds

You decide:
  - What to include
  - Priority order
  - How many items
```

---

### Step 2: Gather Preferences

**Use AskUserQuestion**:

```
Question 1: "How far ahead do you want to plan?"
Options:
- "Just the next step" - 1-2 items, immediate focus
- "This week/sprint" - 3-5 items, short-term
- "This month" - 5-8 items, medium-term
- "Full vision" - 8+ items, comprehensive

Question 2: "What matters most right now?" (multiSelect: true)
Options (DYNAMIC based on goals):
- "{Pain point 1 from goals}"
- "{Pain point 2 from goals}"
- "Quick wins - build momentum"
- "Foundation - set up properly first"
- "Revenue/results - prioritize impact"
```

---

### Step 3: Generate Suggestions

**AI generates roadmap items based on**:
- User's goal from goals.md
- Context insights (if available)
- User's planning horizon preference
- User's priority preference

**Item types**:
| Type | Description |
|------|-------------|
| BUILD | Finite work with deliverables |
| SKILL | Repeatable workflow to create |
| INTEGRATION | External tool to connect |

**Generate format**:
```python
suggestions = []

# Based on goals + context + preferences
# AI generates relevant items

# Example generation logic:
if "content" in goal_domain:
    suggestions.append({
        "name": "Content Calendar",
        "type": "BUILD",
        "rationale": "Addresses inconsistent posting",
        "priority": "high",
        "dependencies": []
    })

if has_context and "slack" in context_content.lower():
    suggestions.append({
        "name": "Slack Integration",
        "type": "INTEGRATION",
        "rationale": "Found in your files - automate notifications",
        "priority": "medium",
        "dependencies": []
    })
```

---

### Step 4: Present Suggestions

**Display**:
```
Based on your goals and context, here's what I suggest:

SUGGESTED ROADMAP
----------------------------------------------------

1. {Item Name} (BUILD)
   → {Rationale - why this matters for your goal}

2. {Item Name} (SKILL)
   → {Rationale}
   Depends on: #1

3. {Item Name} (INTEGRATION)
   → {Rationale}

4. {Item Name} (BUILD)
   → {Rationale}

----------------------------------------------------
```

**Use AskUserQuestion**:
```
Question: "What would you like to do?"
Options:
- "Looks good - save it"
- "Add an item"
- "Remove an item"
- "Change priority order"
- "Explain an item more"
```

---

### Step 5: Iterate Until Satisfied

**If "Add an item"**:
```
What would you like to add?

Type it out, or pick from these ideas:
  - {additional suggestion 1}
  - {additional suggestion 2}
  - {additional suggestion 3}
```

**If "Remove an item"**:
```
Which item should I remove?
  1. {item 1}
  2. {item 2}
  ...
```

**If "Change priority"**:
```
Current order:
  1. {item 1}
  2. {item 2}
  ...

What should be first?
```

**If "Explain an item"**:
```
Which item would you like me to explain?
```
Then provide detailed explanation with:
- What it would create
- How it addresses the goal
- Time estimate
- What "done" looks like

**Loop until user selects "Looks good - save it"**

---

### Step 6: Save Roadmap

**Create `01-memory/roadmap.yaml`** (YAML format for reliable parsing):

```yaml
# =============================================================================
# Your Roadmap - What you're building with this Nexus
# Created: {today}
# =============================================================================
#
# STATUS DERIVATION (automatic - never edit these fields manually):
# - build_id: Auto-set when you say "build {name}"
# - completed_at: Auto-set when build completes
# - Status is derived: completed_at set → done, build_id set → in progress
#
# TO START BUILDING: Say "build {item name}"
# TO UPDATE: Say "update roadmap"
# =============================================================================

items:
  - name: "{Item Name}"
    type: feature       # feature | integration | research | strategy | fix | improvement
    priority: high      # critical | high | medium | low
    rationale: "{Why this matters - connected to your goals}"
    done_when: "{Clear success criteria - what 'done' looks like}"
    build_id: null      # AUTO-SET when build created
    completed_at: null  # AUTO-SET when build completes
    depends_on: []

  - name: "{Item 2 Name}"
    type: feature
    priority: medium
    rationale: "{Rationale}"
    done_when: "{Criteria}"
    build_id: null
    completed_at: null
    depends_on:
      - "{Item Name}"   # If depends on item 1

  # {repeat for all items}
```

**CRITICAL - Format Rules**:
- **type** MUST be one of: `feature`, `integration`, `research`, `strategy`, `fix`, `improvement`
- **priority** MUST be one of: `critical`, `high`, `medium`, `low`
- **build_id** and **completed_at**: Always set to `null` initially (system manages these)
- **depends_on**: List of item names this depends on (empty list if none)

---

### Step 7: Confirm & Guide Next Step

**Display**:
```
Roadmap saved!
----------------------------------------------------

Created: 01-memory/roadmap.yaml

{count} items planned:
  1. {item 1} ({type}, {priority})
  2. {item 2} ({type}, {priority})
  ...

To start building:
→ "build {first item name}"

To update later:
→ "update roadmap"

Your roadmap syncs automatically - when you create builds, they link to roadmap items.
When builds complete, the roadmap updates.
```

---

## Integration Points

**With goals.md**:
- Reads goals to generate relevant suggestions
- Roadmap items should address stated friction/success criteria

**With context analysis**:
- If `01-memory/input/_analysis/analysis-summary.md` exists:
  - Use BUILD ideas from analysis
  - Reference tools for INTEGRATION suggestions
  - Incorporate patterns discovered

**With builds (BIDIRECTIONAL SYNC)**:
- **Forwards**: When you say "build {name}", plan-build matches against roadmap items by slug comparison and sets `build_id`
- **Backwards**: On session start, system auto-links unlinked items to existing builds by name match
- **Completion**: When build moves to complete/, system sets `completed_at` automatically
- Status is DERIVED (never stored): `completed_at` set → done; `build_id` in active → in_progress; no `build_id` → not started

---

## Standalone Usage

Can be called anytime:
```
"create roadmap"
"plan my roadmap"
"what should I build next"
```

To update existing roadmap:
```
"update roadmap"
"add to roadmap"
```

---

## Dynamic Item Count

**No fixed limit**. Item count depends on:
- User's planning horizon preference
- Complexity of goals
- Available context

Typical ranges:
- "Just next step": 1-2 items
- "This week": 3-5 items
- "This month": 5-8 items
- "Full vision": 8-15 items

---

## Error Handling

| Issue | Solution |
|-------|----------|
| No goals.md | Ask user to describe goals inline |
| User can't decide | Suggest starting with 3 items |
| Too many items | Recommend prioritizing top 5 |

---

*Standalone skill - can be used during onboarding or anytime later*
