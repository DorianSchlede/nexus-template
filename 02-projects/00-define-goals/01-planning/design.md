# Design Document: Project 00 - Define Goals

**Project ID**: 00-define-goals
**Last Updated**: 2025-11-04
**Status**: Production Ready

---

## Executive Summary

Project 00 is designed to deliver immediate value through goal capture while establishing the foundation for persistent memory. The design implements **concrete-before-abstract learning principles** to minimize cognitive load and maximize engagement.

**Key Metrics**:
- Time: 8-10 minutes
- Vocabulary: 4 terms only
- Tasks: 16 total
- Structure: Experience → Action → Explanation

---

## Design Philosophy

### Core Principle: Concrete Before Abstract

**The Flow**:
```
Section 0: Welcome + Language (minimal)
Section 1: Your Goals (concrete - 5 min value delivery)
Section 2: Optional Context (FYI only - no stopping)
Section 3: Create Memory (action - see it work)
Section 4: Understanding Memory (explanation - now grounded)
Section 5: Close-Session Habit (practice)
Section 6: What's Next (preview)
```

**Pattern**: Concrete → Action → Explanation
**Benefit**: Users experience value BEFORE learning architecture
**Result**: High engagement and retention

---

## Pedagogical Foundation

### Learning Science Applied

#### 1. Bloom's Taxonomy (Progressive Complexity)
Start at "Knowledge" level (your goals, your work) before moving to higher-order thinking.

#### 2. Constructivist Learning
Experience before explanation creates grounded learning with better retention.

#### 3. Problem-Based Learning
User's needs (goals) drive solution discovery, not the other way around.

#### 4. Cognitive Load Theory (Miller's Law)
4 terms total respects the 4-chunk working memory limit.

#### 5. Ebbinghaus Forgetting Curve
Experience + immediate practice = 80% retention (vs 10% for explanation alone).

#### 6. Peak-End Rule (Kahneman)
Peak = "Your goals captured in 5 min", Strong end = close-session works perfectly.

---

## Section-by-Section Design

### Section 0: Welcome + Language (30 seconds)

**Design Goals**:
- Minimal cognitive load
- Language selection immediate (respect user)
- NO system complexity before context

**Structure**:
- Simple welcome
- Language selection
- NO system state, NO project lists

**Why It Works**: User makes ONE simple choice, everything else is delayed until context exists.

---

### Section 1: Your Goals (5 minutes) - CONCRETE FIRST

**Design Goals**:
- Deliver immediate value (goals captured)
- Ground all future learning in user's actual work
- AI suggestions show collaborative intelligence
- Personal, concrete, directly useful

**Structure**:
1. What do you do? (role + work pattern)
2. 3-month goal + AI suggests metrics
3. 6-12 month vision + AI suggests milestones
4. Confirm understanding

**AI Suggestion Pattern**:
```
1. User provides context
2. AI synthesizes and suggests 2-3 options
3. Ask: "What resonates with you?"
4. User refines
5. Capture refined version
```

**Why It Works**:
- Concrete: Real goals, real work, real value
- Collaborative: AI helps without prescribing
- Time to value: 5 minutes
- Engagement: High (talking about themselves)

**Psychological Anchors**:
- Self-relevance bias: People engage more with personal content
- Goal-gradient effect: Seeing progress toward goal increases motivation
- Identity activation: Discussing role activates professional identity

---

### Section 2: Optional Context (15 seconds) - FYI ONLY

**Design Goals**:
- Awareness without pressure
- NO stopping, NO checking, NO momentum break
- Plant seed for future use

**Structure**:
- ONE sentence: "If you want to share documents, use 00-input/ folder"
- ONE clarification: "We don't need that now—let's continue!"

**Why It Works**:
- Maintains momentum
- Reduces decision fatigue
- Still provides awareness

---

### Section 3: Create Your Workspace (2 minutes) - ACTION

**Design Goals**:
- Show the system working
- Create tangible output
- Maintain transparency
- Set up "aha moment" for Section 4

**Structure**:
1. Announce (5 sec) - "Let me create your workspace..."
2. Execute init-memory.py (10 sec)
3. Show file tree (30 sec) - Visual confirmation
4. Brief explanations (45 sec) - What each file does

**Transparency Design**:
```
✅ Done! Here's what I created for you:

01-memory/
  ├── goals.md          ← Your goals and work context
  ├── roadmap.md        ← Your milestones and next steps
  ├── user-config.yaml  ← Your language and preferences
  ├── core-learnings.md ← For capturing insights
  └── session-reports/  ← Session summaries

02-projects/
  └── project-map.md    ← Tracks your projects
```

**Why It Works**:
- Visual: File tree is scannable
- Concrete: Real files created
- Personal: Contains THEIR content
- Sets up: Next section's explanation has context

**Psychological Principle**: Endowment effect - seeing "your files" increases perceived value

---

### Section 4: Understanding Memory (2 minutes) - EXPLANATION

**Design Goals**:
- Explain AFTER experience (grounded learning)
- Connect to what just happened
- Show future value (tomorrow's experience)
- Introduce minimal vocabulary

**Structure**:
1. Explain what just happened (30 sec)
   - "What I just created is YOUR MEMORY"
   - Contrast: Normal AI (stateless) vs Nexus (persistent)

2. Show the value (30 sec)
   - "Tomorrow, I'll load these files"
   - "I'll remember you're a [ROLE]"
   - "I'll remember your goal: [GOAL]"

3. Connect to their goal (30 sec)
   - "This memory is the foundation"
   - "Everything serves YOUR goal: [GOAL]"

4. Introduce vocabulary (30 sec)
   - Memory, Goals, Sessions, close-session
   - ONLY 4 terms introduced

**Why It Works**:
- Grounded: User saw files created, now learning WHY
- Relevant: Explained in context of THEIR goals
- Minimal: Only 4 new terms
- Future-focused: "Tomorrow" scenario is concrete

**Cognitive Principle**: Explanation after experience = 4x better retention

---

### Section 5: Close-Session Habit (2 minutes) - CRITICAL

**Design Goals**:
- Build the most important Nexus habit
- Make it memorable (practice immediately)
- Show it working (transparency)
- Create positive ending (Peak-End Rule)

**Structure**:
1. Introduce (20 sec) - "Most important habit"
2. Explain (40 sec) - What close-session does
3. Practice (30 sec) - "Say 'done' when ready"
4. Execute (30 sec) - Show it working

**Habit Formation Principles**:
- **Cue**: End of session
- **Routine**: Say "done"
- **Reward**: Progress saved, summary created
- **Practice**: Immediate (not delayed)

**Why It Works**:
- Immediate practice: Research shows immediate practice = 3x better habit formation
- Visible reward: User sees progress saved
- Simple trigger: "done" is natural
- Positive ending: Peak-End Rule satisfied

---

### Section 6: What's Next (1 minute)

**Design Goals**:
- Set expectations for journey
- Confirm progress made
- Leave on high note
- Clear next step

**Structure**:
1. Preview journey (40 sec)
   - 3 more sessions (35-40 min)
   - Brief description of each

2. Final message (20 sec)
   - What you accomplished today
   - "See you next time!"

**Why It Works**:
- Closure: Clear endpoint
- Progress: Visible accomplishment
- Expectations: No surprises
- Motivation: Clear path forward

---

## Vocabulary Management

### The 4-Term Limit

**Only 4 terms in Project 00**:
1. **Memory**: Files that persist across sessions
2. **Goals**: What you want to accomplish
3. **Sessions**: Each time we work together
4. **close-session**: How we end sessions properly

**Delayed to Later Projects**:
- Projects (Project 01)
- Skills (Project 01, experienced in Project 00 but not named)
- Workflows, Triggers (Project 02)
- YAML, Metadata (Project 03)
- MCP, Integration Hub (Project 03 or later)

**Why It Works**: Cognitive load research shows 3-5 new concepts per session is optimal.

---

## AI Suggestions Framework

### Design Pattern

```
Step 1: User provides context
   "What kind of work do you do?"
   → User: "I'm a freelance consultant"

Step 2: AI synthesizes and suggests 2-3 options
   "Based on [ROLE], I imagine your work involves:"
   - Client relationship management
   - Proposal and contract creation
   - Knowledge documentation and reuse

Step 3: Ask for resonance (not prescription)
   "Does that sound right, or is your situation different?"

Step 4: User refines
   User adds nuance, corrections, specifics

Step 5: Capture refined version
   Store USER's version, not AI's suggestion
```

### Key Principles

1. **Suggest, Don't Prescribe**
   - "Might involve" not "should do"
   - Invitation, not instruction

2. **Always Allow Refinement**
   - "Does this fit, or do you have something else in mind?"
   - "What resonates with you?"

3. **Base on Context**
   - Use ROLE to inform suggestions
   - Use WORK_PATTERN to refine

4. **2-3 Options Maximum**
   - Not overwhelming
   - Provides choice
   - Easy to scan

**Why It Works**:
- Collaborative intelligence (not prescriptive AI)
- User feels heard and understood
- Suggestions demonstrate system's capabilities

---

## Time Budget Breakdown

| Section | Time | Purpose |
|---------|------|---------|
| 0. Welcome + Language | 30 sec | Minimal intro, select language |
| 1. Your Goals | 5 min | **VALUE DELIVERY** - capture goals |
| 2. Optional Context | 15 sec | FYI only, no stopping |
| 3. Create Workspace | 2 min | **ACTION** - see it work |
| 4. Understanding Memory | 2 min | **EXPLANATION** - now grounded |
| 5. Close-Session Habit | 2 min | Practice critical habit |
| 6. What's Next | 1 min | Preview journey |
| **TOTAL** | **8-10 min** | |

**Benefits**:
- 5 minutes to first value (goals captured)
- NO abstract teaching before experience
- Expected <15% drop-off

---

## Psychological Design Elements

### 1. Self-Relevance Bias
**Application**: Section 1 focuses entirely on user's goals
**Effect**: Increases engagement and attention

### 2. Goal-Gradient Effect
**Application**: Show progress throughout ("Section 1 of 6")
**Effect**: Motivation increases as goal approaches

### 3. Endowment Effect
**Application**: "YOUR memory", "YOUR goals", "YOUR files"
**Effect**: Increases perceived value

### 4. Peak-End Rule (Kahneman)
**Application**:
- Peak: Goals captured in 5 minutes (early value)
- End: close-session works perfectly (positive ending)
**Effect**: Overall experience judged by peak + end

### 5. Cognitive Fluency
**Application**: Simple language, 4 terms only, clear structure
**Effect**: Easier processing = more positive evaluation

### 6. Identity Activation
**Application**: Asking about role activates professional identity
**Effect**: Primes user for work-focused thinking

### 7. Reciprocity Principle
**Application**: AI suggests helpful options → user wants to engage
**Effect**: Cooperative interaction pattern established

---

## Implementation Notes for AI

### Critical Rules

1. **NO system state complexity in first 30 seconds**
   - Don't show project lists
   - Don't show skill counts
   - Just welcome + language

2. **Goals BEFORE features**
   - Section 1 is goals
   - Features explained AFTER (Section 4)
   - Don't jump ahead

3. **Input folder is FYI ONLY**
   - One sentence
   - NO checking
   - NO permissions
   - NO stopping

4. **Only 4 terms this session**
   - Memory
   - Goals
   - Sessions
   - close-session
   - Nothing else!

5. **AI suggestions are invitations**
   - "Might" not "should"
   - "Could" not "must"
   - Always allow refinement

6. **Explanations AFTER experience**
   - Section 3: Create files (experience)
   - Section 4: Explain Memory (explanation)
   - Not the other way around

### Execution Checklist

Before starting Project 00, AI should verify:
- [ ] No Memory files exist yet (first-time user)
- [ ] User selected language in Section 0
- [ ] All subsequent messages in USER_LANGUAGE
- [ ] Goals captured with AI suggestions (Section 1)
- [ ] Input folder mentioned FYI only (Section 2)
- [ ] init-memory.py executed (Section 3)
- [ ] Files shown BEFORE explaining (Section 3 → 4)
- [ ] Only 4 terms introduced (Section 4)
- [ ] User practiced close-session (Section 5)
- [ ] User understands next steps (Section 6)

---

## Success Metrics

### Quantitative Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| Completion rate | >85% | % who finish Project 00 |
| Session 2 return rate | >75% | % who start Project 01 |
| Time to first value | 5 min | When goals captured |
| Vocabulary retention | >60% | Quiz after 24 hours |
| Drop-off in first 5 min | <15% | Analytics tracking |

### Qualitative Indicators

**Positive Signals**:
- User engages with goal questions (not one-word answers)
- User refines AI suggestions (collaborative)
- User says "done" without prompting (habit forming)
- User returns for Project 01 (value recognized)

**Negative Signals**:
- Vague or rushed goal responses (still confused)
- Passive acceptance of suggestions (not engaged)
- Forgets to practice close-session (didn't internalize)
- Doesn't return (no perceived value)

---

## Conclusion

Project 00 implements a **value-first** onboarding design that:
- Delivers value in 5 minutes
- Reduces cognitive load through minimal vocabulary
- Grounds learning in user's actual goals
- Maintains all core strengths (personalization, AI suggestions, language-first)

The result: An onboarding that respects user time, builds on psychological principles, and sets up success for the remaining 3 projects.

---

**Status**: Production Ready
**Last Updated**: 2025-11-04
