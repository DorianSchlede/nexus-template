# Onboarding Core Insights

> **Source**: Sascha-Dorian conversation analysis (sascha-dorian.md)
> **Date**: 2026-01-23
> **Context**: Extracted insights about onboarding challenges and solutions from user testing session

---

## Executive Summary

The core onboarding challenge is **information overload** - introducing too many concepts simultaneously before users understand the fundamentals. The solution is **progressive disclosure**: introduce concepts step-by-step, explain "how it works" first, and force structured planning before execution.

---

## Critical Insights

### 1. Progressive Disclosure is Critical

**Problem Observed**:
> "Skills erklärt, aber du weißt noch gar nicht, was Skills sind... Der Nutzer sieht jetzt Konzepte, die er noch nicht kennt."

The system was introducing multiple concepts (Skills, Builds, Phases) simultaneously before users understood the basics.

**Solution**:
- Introduce concepts **one at a time**, not all at once
- Don't show all phases upfront - reveal them as the user progresses
- Force stepwise concept introduction in onboarding flow

**Implementation Note**:
> "Wir müssen forcieren, dass wir stückweise die Konzepte einführen und nicht alle Phasen auf einmal zeigen."

---

### 2. Explain "How It Works" First

**Problem Observed**:
> "Im Onboarding Prozess... der Nutzer hat irgendwelche Konzepte bekommen, die gar nicht richtig eingeleitet worden sind. Wir müssen irgendwie dieses 'How Nexus works' einführen."

Users were jumping into tasks without understanding the fundamental work modes and system structure.

**Solution - Teach These Concepts First**:

1. **Two Work Modes**: Build vs Execute
   - Build = work with a beginning, middle, and end
   - Execute = repeatable tasks via skills

2. **Core Folder Structure**:
   - `00-system/` = The engine (built by us)
   - `01-memory/` = Your goals and what AI learned
   - `02-builds/` = Build mode (structured planning)
   - `03-skills/` = Repeatable executables
   - `04-workspace/` = Your file organization

3. **Workspace Map Concept**:
   - A map that tells the AI what exists and where
   - Prevents the AI from shooting files in all directions
   - Must be created early and kept updated

---

### 3. People Jump to Execution Too Quickly

**Root Cause**:
> "Das Problem ist, dass die allermeisten Leute sofort in die Umsetzung gehen. Und deswegen kriegen sie keine gute Ergebnisse."

Both users AND the AI skip planning and jump straight to implementation, leading to:
- Poor quality results
- Disorganized work
- Files created but never reused

**Core Innovation**:
> "Die KI führt dich durch einen strukturierten Planungsprozess... Das ist die Kerninnovation."

The **planning process** is the key differentiator. Force users (and AI) to stay in planning mode before execution.

**Why It Matters**:
- Planning quality directly impacts execution success
- Collaborative planning creates ownership
- Clear plans prevent rework and wasted effort
- AI can do anything - the limitation is lack of precise planning

**Quote**:
> "Die einzige Limitation ist, dass du der KI nicht genau sagst, was du willst... Ich muss sie forcen in diesen Planungsprozess."

---

### 4. Context Organization Must Come Early

**Problem Observed**:
> "Der hat dann nämlich in alle Richtungen Files geschossen, wusste aber gar nicht, was er hat und dann hat er irgendwas gemacht, aber hat es nie wieder benutzt."

Without proper workspace structure early, the AI:
- Creates files everywhere
- Doesn't know what it has
- Never reuses created assets
- User loses track of everything

**Solution - Workspace Map**:
> "Nächsten Chat erstellt er mit dir ein Workspace und arbeitet es mit dir gemeinsam und erstellt dann eine Karte für die KI."

**What the Workspace Map Does**:
1. Explains to the AI what exists and where it is
2. Gets loaded every session (AI is "permanently aware")
3. AI automatically sorts new work into the right place
4. Auto-detects when map is outdated and prompts update

**Implementation Timing**:
Workspace setup should be one of the first onboarding steps, right after explaining how the system works.

---

### 5. Reduce Mental Model Complexity

**Design Goal**:
> "Meine Idee war halt die Komplexität, die mentalen Modelle, die man haben muss, um das System zu verstehen, halt deutlich zu reduzieren."

**Before**: Users needed to understand too many concepts upfront (Projects vs Skills vs Builds vs Integrations vs Research types, etc.)

**After**: Simplify to core concepts:
- Want to BUILD something? → Use builds
- Want to EXECUTE something? → Use skills
- Two modes, clear entry points, reduced cognitive load

**Outcome**:
> "Dadurch haben jetzt die Adoption Rate in der Firma... [increased]"

Simpler mental models = better adoption.

---

### 6. Language Preference Matters

**User Feedback**:
> "Ich finde schon geil, dass man am Anfang seine Sprache auswählt... Todo für AI Agents: die Sprache einbauen an den Anfang und forcieren, dass immer die Sprache des Nutzers gewählt wird."

**Implementation**:
- Ask language preference at the very start
- Store in user-config.yaml
- Force AI to consistently use that language
- Don't mix languages (was happening: English/German mixing)

---

### 7. Quality Over Speed in Onboarding

**Philosophy**:
> "Ich mache halt immer diese halbe Stunde Setup..."

Taking 30-60 minutes for proper setup leads to much better long-term results than rushing through in 5 minutes.

**Why Invest Time**:
- Proper setup prevents confusion later
- Structured onboarding creates good habits
- Users who understand the system use it effectively
- Rushed onboarding = poor adoption and abandonment

---

## Anti-Patterns Observed

### ❌ Concept Overload
Showing Skills, Builds, Projects, Workspace, Memory, Mental Models all at once in first screen.

### ❌ No "How It Works" Introduction
Jumping straight to "create your first build" without explaining the system.

### ❌ Skipping Workspace Setup
Letting users start working without organizing their file structure first.

### ❌ Execution Before Planning
Allowing AI to jump to implementation without thorough planning.

### ❌ Mixed Language
Not setting language preference and having inconsistent English/German mixing.

---

## Success Pattern: The Right Onboarding Flow

### Phase 1: System Understanding (5-8 min)
1. **Welcome** - What is Nexus?
2. **How It Works** - Two modes (Build vs Execute)
3. **Folder Structure** - Where things live
4. **Language Preference** - Set once, use everywhere

### Phase 2: Personal Context (8-10 min)
5. **Setup Memory** - Goals, role, preferences
6. **Create Workspace** - Organize file structure
7. **Build Workspace Map** - Teach AI where everything is

### Phase 3: First Action (Optional)
8. **Optional Learning Skills** - Deep dives into builds, skills, integrations
9. **First Build or Execute** - Start working with understanding

**Total Time**: 15-20 minutes for solid foundation

---

## Key Quotes

> "Die allermeisten Leute sofort in die Umsetzung gehen. Und deswegen kriegen sie keine gute Ergebnisse."

> "Wir müssen irgendwie dieses 'How Nexus works'... Da muss der Nutzer eingeführt werden."

> "Der Nutzer sieht jetzt Konzepte, die er noch nicht kennt. Wir müssen forcieren, dass wir stückweise die Konzepte einführen."

> "Die einzige Limitation ist meine Kreativität... Die einzige Limitation ist, dass du der KI nicht genau sagst, was du willst."

---

## Action Items for Improved Onboarding

1. ✅ Implement progressive concept disclosure
2. ✅ Add "How Nexus Works" as first onboarding step
3. ✅ Force workspace setup early in onboarding
4. ✅ Set language preference at start
5. ✅ Emphasize planning before execution
6. ✅ Reduce number of concepts presented initially
7. ✅ Create clear visual flow showing onboarding phases
8. ✅ Prevent phase/concept overload in initial screens

---

**Last Updated**: 2026-01-23
