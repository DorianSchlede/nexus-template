# Teaching Scripts: Define Goals (Project 00)

**Purpose**: Reusable teaching content templates with variable injection points for personalized examples.

**Usage**: AI generates examples by injecting user's actual context into these templates.

---

## Script 1: Projects Examples Generator

### Context Variables Required:
- `{USER_GOAL}`: User's stated short-term goal
- `{USER_DOMAIN}`: Inferred domain (consulting, research, product, startup, content, etc.)

### Template:

```
Projects are temporal work with beginning, middle, and end.

Let me show you using YOUR goal:

**Project Examples (from YOUR context)**:
1. {USER_GOAL} ← Your actual goal!
2. {RELATED_PROJECT_2}
3. {RELATED_PROJECT_3}

See the pattern? Each has a clear ENDPOINT. When finished, you mark COMPLETE.

**Counter-Example** (what it's NOT):
- "Weekly status reports" → This repeats every week with no endpoint = Skill, not Project!
```

### Example Generation Logic:

**If USER_DOMAIN == "consulting"**:
- RELATED_PROJECT_2: "Design your service offering packages"
- RELATED_PROJECT_3: "Create client onboarding system"

**If USER_DOMAIN == "research"**:
- RELATED_PROJECT_2: "Design and run experiment A"
- RELATED_PROJECT_3: "Write literature review chapter"

**If USER_DOMAIN == "product"**:
- RELATED_PROJECT_2: "Conduct user research for features"
- RELATED_PROJECT_3: "Design and implement authentication system"

**If USER_DOMAIN == "startup"**:
- RELATED_PROJECT_2: "Build MVP for customer validation"
- RELATED_PROJECT_3: "Run pilot program with first 10 users"

**If USER_DOMAIN == "content"**:
- RELATED_PROJECT_2: "Create launch content series (10 episodes)"
- RELATED_PROJECT_3: "Design and build content distribution system"

---

## Script 2: Skills Examples Generator

### Context Variables Required:
- `{USER_ROLE}`: User's stated role
- `{USER_PATTERN}`: User's work pattern
- `{USER_DOMAIN}`: Inferred domain

### Template:

```
Skills are reusable workflows you run repeatedly.

Based on your {USER_ROLE} work:

**Skill Examples (from YOUR context)**:
1. {SKILL_EXAMPLE_1}
2. {SKILL_EXAMPLE_2}
3. {SKILL_EXAMPLE_3}

These repeat—you create once, use many times.

**Counter-Example** (what it's NOT):
- "{USER_GOAL}" → This is one-time work = Project, not Skill!
```

### Example Generation Logic:

**If "client" in USER_PATTERN.lower()**:
- SKILL_EXAMPLE_1: "Client proposal generator"
- SKILL_EXAMPLE_2: "Weekly client status report"
- SKILL_EXAMPLE_3: "Monthly invoice generation"

**If "research" in USER_ROLE.lower() OR USER_DOMAIN == "research"**:
- SKILL_EXAMPLE_1: "Paper annotation workflow"
- SKILL_EXAMPLE_2: "Data analysis template"
- SKILL_EXAMPLE_3: "Literature review process"

**If "product" in USER_ROLE.lower() OR "feature" in USER_PATTERN.lower()**:
- SKILL_EXAMPLE_1: "Feature specification template"
- SKILL_EXAMPLE_2: "Weekly sprint planning"
- SKILL_EXAMPLE_3: "Stakeholder update generator"

**If "startup" in USER_DOMAIN OR "entrepreneur" in USER_ROLE.lower()**:
- SKILL_EXAMPLE_1: "Weekly experiment review"
- SKILL_EXAMPLE_2: "Investor update generator"
- SKILL_EXAMPLE_3: "User interview synthesis"

**If "content" in USER_ROLE.lower() OR USER_DOMAIN == "content"**:
- SKILL_EXAMPLE_1: "Video editing workflow"
- SKILL_EXAMPLE_2: "Content calendar planning"
- SKILL_EXAMPLE_3: "Thumbnail creation template"

---

## Script 3: Memory Examples Generator

### Context Variables Required:
- `{SHORT_TERM_GOAL}`: User's 3-month goal
- `{USER_PATTERN}`: User's work pattern
- `{USER_CHALLENGE}`: User's stated challenge

### Template:

```
Memory means I'll remember YOUR specific context:

**Your Context (persists across sessions)**:
- Your goal: {SHORT_TERM_GOAL}
- Your work pattern: {USER_PATTERN}
- Your challenge: {USER_CHALLENGE}

Tomorrow I remember THIS—not a generic template!

Next session, I'll say:
"Welcome back! Let's continue working on {SHORT_TERM_GOAL}"

That's the power of persistent memory.
```

---

## Script 4: Session Flow Visual

### Context Variables Required:
- None (generic script)

### Content:

```
Every Nexus session follows this pattern:

**Load → Work → Close**

Here's what that looks like:

┌────────────────────────────────────────┐
│ Session 1:                             │
│   Load: Empty (first time)             │
│   Work: Define goals, create memory    │
│   Close: 'done' → Saves goals.md       │
└────────────────────────────────────────┘
              ↓
┌────────────────────────────────────────┐
│ Session 2:                             │
│   Load: goals.md ← YOU defined this!   │
│   Work: Create workspace, first project│
│   Close: 'done' → Saves project updates│
└────────────────────────────────────────┘
              ↓
┌────────────────────────────────────────┐
│ Session 3:                             │
│   Load: goals, roadmap, projects       │
│   Work: Continue project work          │
│   Close: 'done' → Session report created│
└────────────────────────────────────────┘

The CLOSE step is CRITICAL!
```

---

## Script 5: Close-Session Practice Setup

### Context Variables Required:
- `{SHORT_TERM_GOAL}`: User's goal (for confirmation message)

### Template:

```
Now for the MOST IMPORTANT part: practicing close-session.

When you're done working, you need to tell me so I can:
✅ Save your progress
✅ Update project status
✅ Create session report
✅ Prepare memory for next time

**How?**
Just say: "done" or "that's all for today" or "let's end here"

**What happens if you forget?**
❌ System thinks session is still active
❌ Next session gets confused
❌ Progress tracking breaks

This is THE critical habit!

**Let's practice RIGHT NOW.**

When you're ready to end this session, just say "done" or "that's it for now"

[WAIT FOR USER TO SAY "done"]
```

---

## Script 6: Close-Session Confirmation

### Context Variables Required:
- `{SHORT_TERM_GOAL}`: User's goal (to show in confirmation)

### Template:

```
✅ Perfect! Watch what happened...

[close-session skill executed]

**What just happened:**
✅ close-session skill executed
✅ Updated project-map.md: Marked Project 00 as COMPLETE
✅ Created session report in session-reports/
✅ Recorded: "Initialized Nexus with goals: {SHORT_TERM_GOAL}"
✅ Set next onboarding project: 01-first-project

Every session ends this way. You just built the critical habit! 🎉

**Next session:**
We'll load your goals and create your workspace + first real project (Project 01)

See you next time! 👋
```

---

## Script 7: Domain Classifier

### Purpose:
Infer USER_DOMAIN from USER_ROLE and SHORT_TERM_GOAL for example generation.

### Classification Logic:

```python
def classify_domain(user_role, short_term_goal):
    """
    Infer domain from role and goal keywords
    Returns: consulting | research | product | startup | content | general
    """
    combined = (user_role + " " + short_term_goal).lower()

    # Consulting domain
    if any(word in combined for word in ["consult", "client", "agency", "service"]):
        return "consulting"

    # Research domain
    if any(word in combined for word in ["research", "phd", "dissertation", "study", "academic", "paper"]):
        return "research"

    # Product domain
    if any(word in combined for word in ["product", "feature", "sprint", "user research", "ship"]):
        return "product"

    # Startup domain
    if any(word in combined for word in ["startup", "launch", "mvp", "validate", "entrepreneur"]):
        return "startup"

    # Content domain
    if any(word in combined for word in ["content", "youtube", "video", "blog", "podcast", "creator"]):
        return "content"

    # Finance domain
    if any(word in combined for word in ["finance", "accounting", "budget", "financial"]):
        return "finance"

    # Marketing domain
    if any(word in combined for word in ["marketing", "campaign", "brand", "growth"]):
        return "marketing"

    # Default
    return "general"
```

---

## Script 8: Welcome Message

### Context Variables Required:
- None (generic)

### Content:

```
Welcome to Nexus! 🚀

I'm excited to help you get started.

This is your first onboarding session. By the end (about 12-15 minutes), you'll:
✅ Understand how Nexus works
✅ Have your goals defined
✅ Have your memory system initialized
✅ Know the most critical Nexus habit (close-session)

Let me start by explaining what Nexus actually is...
```

---

## Script 9: What is Nexus?

### Context Variables Required:
- None (generic)

### Content:

```
Nexus is a work organization system that runs through AI conversation.

The KEY difference from normal AI chat: **Nexus remembers everything across sessions.**

Here's what that looks like:

**Normal AI:**
- Session 1: "I'm a consultant launching a business..."
- Session 2: "I'm a consultant launching a business..." ← Repeat!
- Session 3: "I'm a consultant launching a business..." ← Exhausting!

**Nexus:**
- Session 1: "I'm a consultant launching a business..."
- Session 2: "Welcome back! Let's continue your consulting business launch"
- Session 3: "Ready to work on client-proposal-system?" ← Remembers!

That's the difference—true memory persistence.

Make sense so far?
```

---

## Script 10: Discovery Questions (Conversational Flow)

### Context Variables Required:
- None (collect as you go)

### Conversational Template:

```
Great! Now let's talk about YOUR work.

[Q1] What's your primary role or focus area right now?
→ [Listen for: consultant, researcher, product manager, student, entrepreneur, etc.]
→ [Extract: USER_ROLE]

[Acknowledge response]

[Q2] How do you currently organize your work?
→ [Listen for: Tools, pain points, current system]
→ [Note any interesting patterns]

[Acknowledge response]

[Q3] What's your typical workload like?
→ [Listen for: "5-7 clients", "3 projects", "full-time + side project"]
→ [Extract: USER_PATTERN]

[Acknowledge response]

[Q4] What's the biggest challenge you're facing with work organization?
→ [Listen for: tracking, context switching, overwhelming complexity]
→ [Extract: USER_CHALLENGE]

[Acknowledge response]

[Synthesize]
"Perfect. So let me make sure I understand:
- You're a {USER_ROLE}
- Managing {USER_PATTERN}
- Main challenge is {USER_CHALLENGE}

This context helps me personalize Nexus for YOUR specific needs.

Does that sound right?"

[Confirm understanding]
```

---

## Notes for AI

**Personalization Rules**:
1. ALWAYS inject user's actual context into templates
2. NEVER use placeholder text in final output
3. Generate 3+ examples per concept
4. Use contrasting examples (what it IS and what it's NOT)
5. Reference user's stated goal by name at least once per teaching moment

**Domain-Specific Examples**:
- Consulting: Clients, proposals, service offerings, invoices
- Research: Papers, experiments, datasets, literature reviews
- Product: Features, sprints, user research, stakeholder updates
- Startup: MVPs, experiments, validation, pivots
- Content: Videos, scripts, assets, publishing

**Variable Injection Pattern**:
1. Capture context (Section 4-5)
2. Classify domain (Script 7)
3. Generate examples (Scripts 1-2)
4. Inject into teaching moments (Section 6)
5. Use in file creation (Section 7)

---

**Teaching Scripts Version**: 1.0
**Last Updated**: 2025-11-03
**Status**: Ready for Use
