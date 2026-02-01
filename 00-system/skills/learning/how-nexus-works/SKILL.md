---
name: how-nexus-works
description: "Learn how Nexus works - the system tour. ~7 min."
onboarding: true
priority: critical
duration: "7 min"
---

# How Nexus Works

A guided tour of your AI operating system.

---

## Workflow

When this skill loads, guide the user through 5 parts in sequence. Keep the tone conversational and educational - not condescending. Each part should feel natural, not like reading a manual.

---

## Part 1: Two Work Modes

**Display**:
```
PART 1/5: Two Work Modes

Nexus has TWO modes of operation:

**BUILD Mode** 🔨
- Create something NEW
- Has a clear END (when it's done, it's done)
- Example: Build a sales playbook, create a proposal generator
- You PLAN it, then you BUILD it

**WORK Mode** 💼
- USE what you've built
- REPEATABLE (use it again and again)
- Example: "proposal [client]" → generates proposal using your playbook

The distinction:
- If it ENDS → BUILD
- If it REPEATS → WORK (via skills)
```

**Wait for acknowledgment**, then continue.

---

## Part 2: The Four Pillars

**Display**:
```
PART 2/5: The Four Pillars

Your Nexus system has 4 core components:

📁 **01-memory/** - Your system's brain
   - goals.md: What you want to achieve
   - Loaded EVERY session (AI never forgets you)

📁 **02-builds/** - Your workshop
   - Projects with clear beginning and end
   - Each build: 4 documents (overview, discovery, plan, steps)

📁 **03-skills/** - Your AI workforce
   - Reusable automations
   - Trigger: "follow-up [client]" → skill runs

📁 **04-workspace/** - Your files
   - Organized by YOUR structure
   - AI navigates via workspace-map.md
```

**Wait for acknowledgment**, then continue.

---

## Part 3: The Core Innovation

**Display**:
```
PART 3/5: The Core Innovation

Three things make Nexus different:

1. **Collaborative Planning**
   AI doesn't just execute vague ideas
   It interviews YOU to extract what you REALLY need

2. **AI Navigates YOUR Structure**
   You design the folders
   AI learns the map, operates within YOUR system

3. **Cross-Session Continuity**
   While building, AI NEVER forgets
   Pick up EXACTLY where you left off
```

**Wait for acknowledgment**, then continue.

---

## Part 4: Session Boundaries

**Display**:
```
PART 4/5: Session Boundaries

IMPORTANT: Clean session boundaries matter.

Good practice:
- 1 session = 1 topic
- Planning session → close → New session → Execution
- Each session has clear focus

Why?
- Better AI performance (focused context)
- Cleaner summaries
- Easier to resume later

How:
- When you finish a topic, open a NEW chat/session
- Don't mix multiple topics in one session
```

**Wait for acknowledgment**, then continue.

---

## Part 5: The Build Workflow

**Display**:
```
PART 5/5: The Build Workflow

When you want to BUILD something:

Session 1 (PLANNING):
- Say "build [X]" or "create [Y]"
- AI loads plan-build skill
- You fill 4 documents TOGETHER
- Mental models applied (why this matters)
- End session (planning complete)

Session 2 (EXECUTION):
- Say "continue [build name]"
- AI loads execute-build skill
- AI executes the plan YOU approved
- You review outputs
- End session (build complete)

Why separate sessions?
- Planning = thinking (needs focus)
- Execution = doing (different mindset)
- Clean context = better results
```

---

## End of Skill

After Part 5, display:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SESSION COMPLETE ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

You now understand how Nexus works!

Your progress saves automatically.

IMPORTANT: Clean session boundaries matter in Nexus.
Each session = one focus.

This session: System learning (DONE)
Next session: Set up your goals and build your first system

→ Open a NEW chat/session when ready to continue
```

**State Updates**:
```yaml
onboarding:
  status: "tour_complete"
  in_progress_skill: null

learning_tracker:
  completed:
    how_nexus_works: true
```

---

## Notes

- Keep each part to ~1-2 minutes of reading
- Wait for user acknowledgment between parts
- Don't rush - let concepts sink in
- Tone: Educational but not condescending
- End with clear session boundary teaching
