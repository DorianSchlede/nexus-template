# Framework 3: User Mental Models v2

**Project**: 02-nexus-ui-wireframing
**Framework**: Cognitive Mapping
**Version**: 2.0 - Updated for Build vs Work model
**Status**: CONFIRMED

---

## Core Question

> How does the user THINK about the system?

---

## Mental Model Fundamentals

A Mental Model is the internal representation a user has of a system. Good UI design aligns with the user's mental model - or consciously shifts it.

```
User's Mental Model  <-->  System's Actual Model
         |                        |
    User's Actions    -->    System Response
         |                        |
   Model Reinforced  <--   Feedback Loop
```

---

## The Core Mental Model Shift (v2)

### From: "I use AI tools"
### To: "I build MY system"

| Old Model | New Model |
|-----------|-----------|
| AI helps with tasks | I BUILD systems that do tasks |
| Chat = work | Build = create / Work = use |
| Sessions are ephemeral | My system grows over time |
| AI is the tool | MY system is what I've built |

---

## Build vs Work: The Fundamental Distinction

**This is the CORE mental model users must internalize.**

| BUILD | WORK |
|-------|------|
| Create something **new** | **Use** what was built |
| **Finite** (has end) | **Ongoing** (repeatable) |
| Plan → Build → Done | Trigger → Execute → Result |
| Output: **Artifacts** | Output: **Outcomes** |
| Tab: 🔨 Build | Tab: 💼 Work |
| Hard (requires thinking) | Easy (system does it) |

**UI Reinforcement**:
- Different tab types
- Different colors (Build = blue/yellow, Work = green)
- Different language ("Build this" vs "Work on this")

---

## Competing Mental Models (v2)

### Tier 1: Vanilla AI (ChatGPT, Claude, Gemini)

```
+------------------------------------------------------------+
|              VANILLA AI MENTAL MODEL                        |
+------------------------------------------------------------+
|                                                             |
|  "I chat with an AI"        → Conversation, not system      |
|  "Each chat is a session"   → Ephemeral, starts from zero   |
|  "I ask, AI answers"        → Reactive, not proactive       |
|  "Chats are isolated"       → No context between chats      |
|                                                             |
+------------------------------------------------------------+
```

### Tier 2: Projects (GPT Projects, Claude Projects)

```
+------------------------------------------------------------+
|              PROJECTS MENTAL MODEL                          |
+------------------------------------------------------------+
|                                                             |
|  "I have persistent context"  → Better, but manual          |
|  "I upload files for context" → No structure                |
|  "Each project is separate"   → No cross-learning           |
|  "Output is still chat text"  → No structured deliverables  |
|                                                             |
+------------------------------------------------------------+
```

### Tier 3: Nexus Mental Model (Target)

```
+------------------------------------------------------------+
|                 NEXUS MENTAL MODEL                          |
+------------------------------------------------------------+
|                                                             |
|  "I'm building MY system"      → Ownership, not tool        |
|  "Build creates, Work uses"    → Clear distinction          |
|  "My system grows over time"   → Accumulation, progress     |
|  "I see my progress (X% built)"→ Visible growth             |
|  "Skills automate my patterns" → Reusable automation        |
|  "Tabs show my active work"    → Familiar browser model     |
|                                                             |
+------------------------------------------------------------+
```

---

## The Five Mental Model Shifts (v2)

### Shift 1: From "Chat" to "Build vs Work"

| Competitors | Nexus |
|-------------|-------|
| "New Chat" | "New Build" or "Open Work" |
| All chats the same | Build tabs vs Work tabs |
| Arbitrary content | Structured (4 docs) vs Quick (skills) |

**UI Reinforcement**:
```
NOT: [New Chat] [New Chat] [New Chat]
BUT: [🗺️ Roadmap] [📁 Workspace] │ [🔨 ICP Build] [💼 Work] [+]
     (fixed)                     │ (multiple, user-created)
```

---

### Shift 2: From "Ephemeral" to "Persistent + Growing"

| Competitors | Nexus |
|-------------|-------|
| "This session" | "My system" |
| No progress | "45% built" |
| Starts from zero | Continues where you left off |
| Nothing accumulates | Everything builds on previous |

**UI Reinforcement**:
```
ALWAYS VISIBLE:
+----------------------------------------------------+
|  YOUR SYSTEM IS 45% BUILT                          |
|  [===============              ]                   |
+----------------------------------------------------+
```

---

### Shift 3: From "Asking AI" to "Building with AI"

| Competitors | Nexus |
|-------------|-------|
| "Help me with X" | "Build X" |
| AI gives answer | AI + User build together |
| Output = Text | Output = 4 documents + deliverable |

**UI Reinforcement**:
- 4-document structure visible
- Progress through phases (PLANNING → BUILDING → DONE)
- Artifacts saved in Workspace

---

### Shift 4: From "AI helps" to "MY system works"

| Competitors | Nexus |
|-------------|-------|
| "ChatGPT" is the star | "YOUR System" is the star |
| "ChatGPT can..." | "You have built..." |
| Tool branding | Ownership language |

**Ownership Language**:
| Instead of | Say |
|------------|-----|
| "AI created" | "You built" |
| "Nexus says" | "Your system includes" |
| "New Chat" | "New Build" |
| "Powered by Nexus" | "Your 10x Operating System" |

---

### Shift 5: From "Prompts" to "Skills" (Work Mode)

| Competitors | Nexus |
|-------------|-------|
| Copy-paste prompts | Trigger natural language |
| Manual repetition | Automated skills |
| "Run this prompt again" | "Execute follow-up skill" |

**UI Reinforcement**:
```
💼 WORK TAB:
+--------------------------------------------+
|  QUICK SKILLS:                             |
|  [📧 Follow-up Email] [📝 Meeting Notes]  |
|                                            |
|  Or just tell me what you need...          |
+--------------------------------------------+
```

---

## Tab-Based Mental Model (v2 NEW)

Users think in terms of **browser tabs** - familiar from web browsing.

### Fixed Tabs = Navigation Anchors

```
[🗺️ Roadmap] [📁 Workspace] [📥 Inbox]
```

- Always there, can't close
- Overview of the system
- "Where do I go to see X?"

### Multiple Tabs = Active Work

```
[🔨 ICP Build ×] [💼 Work Session ×] [+]
```

- User opens and closes
- Focused work on one thing
- "What am I currently working on?"

**Why This Works**: Users already understand tabs from browsers. No new pattern to learn.

---

## Onboarding: Progressive Model Building

The 8-step onboarding deliberately introduces concepts in order:

| Step | Mental Model Introduced | Real UI Used |
|------|-------------------------|--------------|
| 1-3 | "System learns about me" | Onboarding chat |
| 4 | "I have organized files" | **Real Workspace tab** |
| 5 | "I plan what to build" | **Real Roadmap tab** |
| 6 | "Build has 4 documents" | **Real Build tab (Planning)** |
| 7 | "AI executes my plan" | **Real Build tab (Building)** |
| 8 | "I use what I built" | **Real Work tab** |

**Key Insight**: By using REAL UI during onboarding, users learn the product by using it.

---

## Mental Model Alignment Matrix (v2)

| Concept | User expects (ChatGPT) | Nexus delivers | UI Element for Shift |
|---------|------------------------|----------------|---------------------|
| Work mode | Chat | Build vs Work | Two tab types |
| Navigation | Chats | Tabs (fixed + multiple) | Tab bar |
| Session | Ephemeral | Persistent + Growing | Progress % |
| Output | Text | 4 documents + deliverable | Document tabs |
| Automation | Copy prompts | Skills in Work tab | Quick Actions |
| Ownership | "AI's answer" | "YOUR system" | Language everywhere |

---

## UI Elements That Reinforce the Model

### 1. System Status (Permanent Reminder)

```
+--------------------------------------------------------------+
|  [NEXUS]  YOUR SYSTEM IS 45% BUILT    [🎤] [🔍] [⚙️] [?]     |
+--------------------------------------------------------------+
```

**Function**: User ALWAYS sees they're building something.

---

### 2. Tab Bar with Fixed/Multiple Sections

```
+--------------------------------------------------------------+
|  [🗺️ Roadmap] [📁 Workspace] [📥 Inbox]  │  [🔨 ICP ×] [+]   |
|  ═══════════════════════════════════════  │                   |
|  FIXED (always there)                     │  MULTIPLE (yours) |
+--------------------------------------------------------------+
```

**Function**: Clear navigation with ownership of work tabs.

---

### 3. Build Phase Indicators

```
🔵 PLANNING: ICP Definition          [60%]
🟡 BUILDING: ICP Definition          [55%]
✅ DONE: ICP Definition
```

**Function**: User always knows Build state.

---

### 4. Work Tab Quick Actions

```
QUICK SKILLS:
[📧 Follow-up Email] [📝 Meeting Notes] [📊 Analysis]

Or just tell me what you need...
```

**Function**: Work = using what you've built (skills) or getting help.

---

## Cognitive Load Management

### Familiar First Principle

Use patterns users already know:

| Familiar (use) | New (introduce carefully) |
|----------------|---------------------------|
| Browser tabs | Fixed vs Multiple tabs |
| Google Drive | Workspace file browser |
| Kanban board | Roadmap |
| Chat | Build chat + Work copilot |

### Progressive Disclosure

1. **Onboarding**: Learn by using real UI
2. **First Build**: Full cycle with guidance
3. **Subsequent**: Use system independently

---

## Key Takeaways for UI Design (v2)

1. **Build vs Work is the core distinction** - reinforce everywhere
2. **Tabs are the navigation model** - fixed for overview, multiple for work
3. **Use "YOUR" language everywhere** - ownership > tool
4. **Show progress permanently** - X% built in header
5. **Onboarding uses real UI** - learn by doing
6. **Skills are in Work, not separate** - part of "using" not "building"

---

## Key Changes from v1

| Aspect | v1 | v2 |
|--------|----|----|
| Primary distinction | Planning vs Execution | **Build vs Work** |
| Navigation | Mode switching | **Tab-based (fixed + multiple)** |
| Skill mental model | Separate mode | **Part of Work tab** |
| Onboarding | Generic wizard | **8 steps with real UI** |
| Progress | % complete | **% built (ownership language)** |

---

*Mental Models Framework v2 - Updated 2026-01-13 for Build vs Work model*
