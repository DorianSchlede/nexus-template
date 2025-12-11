---
name: setup-goals
description: "Personalize Nexus with your goals, role, and preferences. Load when user says 'setup goals', 'define goals', 'personalize nexus', 'set my goals', 'configure nexus', 'my goals', 'update goals', 'edit goals', 'change my goals', 'goals setup', 'personalize my goals', 'customize nexus', 'set up my profile', 'tell nexus about me', 'who am I', 'define my role', or asks about personalizing the system. Transforms smart default templates into personalized context. Takes 8-10 minutes. Optional but recommended for best experience."
---

# Setup Goals

Guide user through goal definition and system personalization.

## Purpose

Transform smart default templates into meaningful, personalized context that improves AI collaboration quality. Captures user's role, short-term goals (3 months), long-term vision (1-3 years), and work preferences.

**Time Estimate**: 8-10 minutes

---

## Workflow

### Step 1: Welcome & Language

**Display**:
```
━━━ SETUP GOALS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Let's personalize Nexus to understand your work context.
This takes about 8-10 minutes and improves AI collaboration.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Ask**: "What language would you like me to use? (English is default)"

**Action**: Store preference in user-config.yaml, switch all communication.

---

### Step 2: Role Discovery

**Ask**: "What do you do? Tell me about your current role or situation."

**AI Suggestion Pattern**: Listen, then offer 2-3 refined versions. Let user pick or refine.

**Store**: Update `## Current Role` in goals.md

---

### Step 3: Short-Term Goal

**Ask**: "What's the ONE thing you want to achieve in the next 3 months?"

**Help make it specific and measurable**. Capture:
- The goal itself
- Why it matters (motivation)
- 2-3 success metrics

**Store**: Update `## Short-Term Goal (3 months)` in goals.md

---

### Step 4: Long-Term Vision

**Ask**: "Where do you want to be in 1-3 years?"

Connect to short-term goal to show trajectory.

**Store**: Update `## Long-Term Vision (1-3 years)` in goals.md

---

### Step 5: Work Preferences

Quick questions:
1. "When do you do best work?" (morning/afternoon/evening)
2. "Typical session length?" (30min, 1hr, 2hrs+)
3. "What types of work?" (writing, coding, research, planning...)

**Store**: Update `## Work Style & Preferences` in goals.md

---

### Step 6: Finalize

**Actions** (MUST complete all):

1. **Remove `smart_default: true`** from goals.md YAML frontmatter (if present)

2. **Update `Last Updated`** timestamp in goals.md

3. **Mark skill complete** in user-config.yaml:
   ```yaml
   learning_tracker:
     completed:
       setup_goals: true  # ADD THIS LINE
   ```

4. **Update language** in user-config.yaml (if user specified):
   ```yaml
   user_preferences:
     language: "{user's language}"
   ```

---

### Step 7: Close-Session Practice

**Display**:
```
━━━ IMPORTANT HABIT ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
When done working, always say "done" or "close session".
This saves progress and helps me remember context.
Let's practice - say "done" now!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Wait for "done", then trigger close-session.

---

## Success Criteria

- [ ] Language preference captured in user-config.yaml
- [ ] Role clearly defined in goals.md
- [ ] Short-term goal specific and measurable
- [ ] Success metrics defined
- [ ] Long-term vision captured
- [ ] `smart_default: true` removed from goals.md
- [ ] `learning_tracker.completed.setup_goals: true` in user-config.yaml
- [ ] User practiced close-session
