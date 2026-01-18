---
name: setup-memory
description: "Configure Nexus memory with your role, goals, and context. Keywords: setup memory, personalize, configure, my goals, my role, about me, context upload. 10 min."
onboarding: true
priority: critical
---

## 🎯 AI Proactive Triggering (ONBOARDING SKILL - CRITICAL PRIORITY)

**This is the FIRST onboarding skill with CRITICAL priority. Suggest early and often.**

### When to Proactively Suggest (AI MUST check user-config.yaml)

Check `learning_tracker.completed.setup_memory` AND `goals.md` for `smart_default: true`. If not personalized:

**PROACTIVELY SUGGEST when user:**
1. **FIRST SESSION**: Always suggest during first interaction if goals not set
2. Asks for help with work that would benefit from context
3. Uses Nexus for meaningful work but hasn't personalized yet
4. Mentions their role, job, or what they do
5. Expresses frustration that AI doesn't understand their context
6. At menu display when `goals_personalized: false` - PROMINENTLY highlight

**Suggestion Pattern (first session):**
```
💡 Welcome to Nexus! To help you most effectively, I'd love to learn:
- Your context (documents, projects, background)
- Your role and situation
- Your goals (short-term and long-term)

This takes about 10 minutes and dramatically improves our collaboration.
Say 'setup memory' to personalize, or continue with defaults.
```

**Menu Integration:**
When displaying menu with `goals_personalized: false`:
```
🧠 MEMORY
   ⚠️ Not personalized ▸ 'setup memory' (10 min, highly recommended)
```

**DO NOT suggest if:**
- `learning_tracker.completed.setup_memory: true`
- `goals.md` no longer has `smart_default: true`
- User explicitly declined personalization multiple times

---

# Setup Memory

Guide user through context upload, goal definition, and system personalization.

## Purpose

Transform smart defaults into meaningful, personalized context. Captures uploaded context, user's role, goals, and work focus. **Uses SubAgents to analyze uploaded context** to prevent main context overflow.

**Time Estimate**: 10-12 minutes

---

## Workflow

### CRITICAL: Initialize Todo List

**FIRST ACTION when skill loads** - Create todo list to track progress:

```
TodoWrite:
1. [ ] Set language
2. [ ] Welcome & explain setup
3. [ ] Guide context upload
4. [ ] Discover role
5. [ ] Capture long-term vision
6. [ ] Define short-term goal
7. [ ] Identify work focus
8. [ ] Finalize and save to memory
```

This ensures:
- User sees progress through the setup
- No steps get skipped
- Clear visual feedback

---

### Step 1: Language (FIRST!)

**Display**:
```
    ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗
    ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝
    ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗
    ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║
    ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║
    ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝

         Welcome to Nexus!
```

**Ask immediately**: "What language should I use? / Welche Sprache? / Quelle langue?"

**Action**: Store in user-config.yaml, switch ALL following communication to that language.

---

### Step 2: Welcome (in user's language)

**Say** (in user's chosen language):
```
Hi! I'm Nexus - together we'll build YOUR productivity system.

You're not just using an AI. You're building a system that:
• Remembers who you are (no re-explaining)
• Organizes your files
• Grows with you over time

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 SETUP (2 short sessions):

1. NOW (10 min) → Your Memory
   I learn about you: context, role, goals

2. NEXT SESSION (5 min) → Your Workspace
   We organize your folders

After that, you're ready to build.

Let's start!
```

---

### Step 3: Context Upload (CRITICAL - USE SUBAGENTS)

**FIRST: Create the context folder** (if doesn't exist):
```bash
mkdir -p 04-workspace/context/
```

**Then show the user WHERE to put files:**
```
Hast du Dokumente, die ich kennen sollte?

Beispiele:
• **Über dich**: CV, LinkedIn-Export, Portfolio, Bio
• **Über deine Arbeit**: Projekt-Docs, Research, Notizen, Anforderungen

📁 SO GEHT'S:

   ┌─────────────────────────────────────┐
   │  📂 SIDEBAR (links)                 │
   │  ├── 00-system/                     │
   │  ├── 01-memory/                     │
   │  ├── ...                            │
   │  └── 04-workspace/                  │
   │      └── 📁 context/  ◀── HIER!    │
   └─────────────────────────────────────┘

1. Öffne 04-workspace/context/ in der Seitenleiste
2. Ziehe deine Dateien direkt in den Ordner
3. Sag mir Bescheid wenn fertig

⚠️ WICHTIG: Nicht in den Chat ziehen! Sonst lese ich alles
sofort und mein Kontext läuft voll.

Sag 'fertig' wenn die Dateien drin sind, oder 'skip' zum Überspringen.
```

**Wait for user confirmation ("fertig" or similar)**

**If user confirms files are ready:**

1. **CRITICAL: Spawn SubAgent(s) to analyze** - DO NOT read files yourself!

   **SubAgent Strategy:**
   | Files | Action |
   |-------|--------|
   | 1-3 files | 1 SubAgent |
   | 4-8 files | 2 SubAgents (parallel) |
   | 9+ files | 3+ SubAgents (chunked) |

4. **Use SubAgent Template below**

5. **Wait for SubAgent summary, then continue**

**If user skips**: Continue to Step 4.

---

#### SubAgent Template: Context Analysis

```markdown
## Task: Analyze Onboarding Context

**Files to analyze**: [LIST FILES IN 04-workspace/context/]

**Your job**: Read and analyze these files, then return a structured summary.

**Return format** (EXACTLY this structure):

### Person Summary
[2-3 sentences about who this person is, if determinable]

### Professional Context
- Role/Position: [extracted or "not specified"]
- Domain/Industry: [extracted or "not specified"]
- Skills/Expertise: [list if found]

### Work Context
- Current projects/focus: [extracted or "not specified"]
- Goals mentioned: [any goals found in docs]
- Key topics/themes: [recurring themes]

### Relevant Terms
[Domain-specific jargon, tools, technologies mentioned]

### Suggested Goals
Based on the context, this person might want to:
1. [suggestion]
2. [suggestion]
3. [suggestion]

**IMPORTANT**:
- Keep summary under 300 words total
- Only extract what's explicitly in the documents
- Mark uncertain information as "possibly" or "unclear"
```

---

### Step 4: Role Discovery

**Ask**: "What do you do? Tell me about your current role or situation."

**If context was uploaded**:
- Reference SubAgent findings: "Based on your documents, it looks like you're [X]. Is that right?"
- Let user confirm or correct

**AI Suggestion Pattern**: Listen, then offer 2-3 refined versions. Let user pick or refine.

**Store**: Update `## Current Role` in goals.md

---

### Step 5: Long-Term Vision (FIRST)

**Ask**: "Where do you want to be in 1-3 years? What's your big picture?"

**If context was uploaded**:
- Use SubAgent's "Suggested Goals" as conversation starters
- "Based on your documents, it seems like [X] might be important to you. Where does that fit in your vision?"

**Store**: Update `## Long-Term Vision (1-3 years)` in goals.md

---

### Step 6: Short-Term Goal (DERIVED)

**Ask**: "Given your vision of [their vision], what's the ONE thing you want to achieve in the next 3 months?"

**AI suggests based on**:
- Long-term vision (work backwards)
- Uploaded context (if available)
- SubAgent's suggested goals

**Help make it specific**. Capture:
- The goal itself
- Why it matters (connection to vision)
- 2-3 success metrics

**Store**: Update `## Short-Term Goal (3 months)` in goals.md

---

### Step 7: Work Focus

**Ask**: "What types of work will you use Nexus for? (writing, coding, research, planning, creative work...)"

**Store**: Update `## Work Focus` in goals.md

---

### Step 8: Finalize

**Actions** (MUST complete all):

1. **Remove `smart_default: true`** from goals.md YAML frontmatter (if present)

2. **Update `Last Updated`** timestamp in goals.md

3. **Mark skill complete** in user-config.yaml:
   ```yaml
   learning_tracker:
     completed:
       setup_memory: true
   ```

4. **Update language** in user-config.yaml (if user specified):
   ```yaml
   user_preferences:
     language: "{user's language}"
   ```

5. **Note context location** in user-config.yaml (if files uploaded):
   ```yaml
   context:
     path: "04-workspace/context/"
     files_uploaded: true
   ```

6. **Display completion**:
   ```
   ✅ Setup Memory Complete!

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   CAPTURED:
   • Your role: [role]
   • Long-term vision: [vision summary]
   • Short-term goal: [goal summary]
   • Work focus: [focus areas]
   • Context files: [if uploaded, else "none yet"]

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   📁 WHERE YOUR DATA LIVES:

   ┌─────────────────────────────────────┐
   │  📂 01-memory/                      │
   │  ├── goals.md      ◀── Your goals  │
   │  ├── user-config.yaml  ◀── Settings│
   │  └── memory-map.md                  │
   └─────────────────────────────────────┘

   You can edit goals.md anytime to update your goals.
   Open it in the sidebar to see exactly what I saved.

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   🧠 WHY THIS MATTERS:

   Every new chat session, Nexus automatically loads 01-memory/.

   That means:
   → I already know who you are
   → I already know your goals
   → No need to re-explain yourself

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   🚀 WHAT'S NEXT:

   1. Close this chat (type 'done' or just close)
   2. Open a NEW chat
   3. Say 'hi' - I'll greet you with your context loaded
   4. Say 'create folders' to organize your workspace

   The next session takes ~5 min and sets up your folder structure.

   See you in the next chat!
   ```

---

## Success Criteria

- [ ] Language preference captured
- [ ] Context uploaded and analyzed by SubAgent (if provided)
- [ ] Role clearly defined in goals.md
- [ ] Long-term vision captured
- [ ] Short-term goal specific and measurable with metrics
- [ ] Work focus defined
- [ ] `smart_default: true` removed from goals.md
- [ ] `learning_tracker.completed.setup_memory: true` in user-config.yaml

---

## Technical Notes

### Why SubAgents for Context?

The main Claude context has limited space. If user uploads 5 PDFs, reading them all would:
- Fill up context quickly
- Leave no room for the actual setup conversation
- Cause degraded performance

SubAgents:
- Run in isolated context
- Read and analyze files
- Return only the summary (300 words max)
- Main context stays clean

### SubAgent Invocation Example

```
Task tool with subagent_type="general-purpose":

"Analyze the files in 04-workspace/context/.
Read each file and return a structured summary following
the Context Analysis template. Keep total output under 300 words."
```
