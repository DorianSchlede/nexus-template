# Writing Style Principles

Two complementary frameworks for clear, effective writing.

---

# Part 1: Classical Style (Pinker)

Focus: Clarity, precision, necessity.

---

## 1. Direct Language

Use active voice. Make the actor visible.

**Why**: Passive voice hides responsibility and adds words.

| Passive (Avoid) | Active (Use) |
|-----------------|--------------|
| The data was processed by the system | The system processed the data |
| Errors should be handled gracefully | Handle errors gracefully |
| The report will be generated | Generate the report |
| It was decided that... | We decided... / The team decided... |

**Nominalizations to avoid**: Convert abstract nouns back to verbs.

| Nominalization | Direct verb |
|----------------|-------------|
| Make a determination | Determine |
| Conduct an investigation | Investigate |
| Perform an analysis | Analyze |
| Give consideration to | Consider |

---

## 2. Necessary Content Only

Apply Occam's razor: if removing something doesn't reduce understanding, remove it.

**Filler phrases to delete**:
- "It is important to note that..."
- "As a matter of fact..."
- "In order to..." → "To..."
- "Due to the fact that..." → "Because..."
- "At this point in time..." → "Now..."
- "In the event that..." → "If..."

**Redundant modifiers**:
- "Completely eliminate" → "Eliminate"
- "Absolutely essential" → "Essential"
- "Final conclusion" → "Conclusion"
- "Future plans" → "Plans"
- "Past history" → "History"

**Test**: Read the sentence without the phrase. If meaning is preserved, delete it.

---

## 3. No Artificial Complexity

Structure should serve understanding, not demonstrate effort.

**Avoid**:
- Headers for single paragraphs
- Bullet lists with one item
- Tables with two rows
- Nested bullets beyond two levels
- Numbered lists when order doesn't matter

**Ask**: Does this structure help the reader scan and understand faster? If not, simplify.

❌ Over-structured:
```
## Introduction
### Overview
#### Purpose
This document explains X.
```

✅ Simple:
```
This document explains X.
```

---

## 4. Specific Over Abstract

Abstract language requires readers to guess your meaning. Specific language shows it.

| Abstract (Avoid) | Specific (Use) |
|------------------|----------------|
| Various factors | Cost, timeline, and team size |
| Certain aspects | The login flow and checkout process |
| Appropriate measures | Rate limiting and input validation |
| Relevant stakeholders | The product manager and tech lead |
| Significant improvements | 40% faster response time |

**When to use examples**: When a concept could be interpreted multiple ways.

**When NOT to use examples**: When the statement is already concrete.

---

## 5. Consistent Terminology

One concept = one name. Never vary terms for style.

**Problem**: Using "user", "customer", "client", and "account holder" interchangeably confuses readers.

**Solution**: Pick one term. Define it if needed. Use it everywhere.

**In code and prompts**:
- Variable names should match documentation
- Don't rename concepts between sections
- If you must introduce a synonym, explicitly state the equivalence

---

## 6. Clear Intent (For Prompts)

Every prompt should answer three questions:

**Goal**: What should be accomplished? One clear statement.
- ❌ "Help me with this text"
- ✅ "Summarize this text in 3 sentences"

**Constraints**: What boundaries apply?
```
- Do not add information not in the source
- Do not use bullet points
- Maximum 100 words
```

**Output Format**: What should the result look like?
```
Output Format: A single paragraph of plain text
```

---

## 7. Reader-First Order

Sequence information by how readers need it, not how you discovered it.

| Context | Order |
|---------|-------|
| Explaining a solution | Problem → Solution → Details |
| Teaching a concept | What → Why → How |
| Giving instructions | Goal → Steps → Edge cases |
| Reporting results | Summary → Evidence → Method |

**Anti-patterns**:
- Starting with caveats before the main point
- Explaining implementation before purpose
- Listing exceptions before the rule

**Test**: Can a reader stop at any point and still have understood something complete?

---

## 8. Verifiable Claims

Every statement should be based on fact, logic, or explicit definition—not impression.

**Avoid**:
- "It seems that..." (either it is or investigate further)
- "Generally speaking..." (specify when it applies)
- "Best practice is..." (cite source or explain why)
- "Obviously..." (if obvious, why state it?)

| Unverifiable | Verifiable |
|--------------|------------|
| The system is fast | Response time: 50ms p95 |
| Most users prefer X | 73% of surveyed users chose X |
| This approach is better | This approach reduces memory usage by 40% |

---

# Part 2: Smart Brevity (Axios)

Focus: Structure, scannability, impact.

Core philosophy: **"Brevity is confidence. Length is fear."**

---

## The 4 Components

### 1. Strong Headline

Grab attention in 6 words or fewer. Your audience decides in a split second whether to read.

**Rules**:
- Maximum 6 words
- Use strong, short words
- Put the news/action first
- Make it specific, not generic

| Weak | Strong |
|------|--------|
| "Update on the project status" | "Project ships Friday" |
| "Important information about changes" | "New policy starts Monday" |
| "Thoughts on the quarterly results" | "Revenue up 23% in Q3" |
| "A few things to consider" | "Three blockers need fixes" |

---

### 2. One Key Takeaway (The Lede)

First sentence = the ONE thing you want people to remember.

**Rules**:
- One sentence only
- Most important information
- Direct, short, sharp
- No warm-up, no context first

❌ Buried lede:
```
After several months of planning and coordination between
multiple teams, we're excited to share that the new
feature is ready.
```

✅ Direct lede:
```
The new feature launches tomorrow.
```

---

### 3. Why It Matters

Explain relevance to the reader. Use the exact phrase "Why it matters" or similar axiom.

**Purpose**: Connect information to reader's work/life.

**Format**:
```
**Why it matters**: [1-2 sentences on reader impact]
```

**Examples**:
- "Why it matters: This affects your Q4 planning timeline."
- "Why it matters: You'll need to update your workflow by Friday."
- "Why it matters: This reduces your review time by 50%."

---

### 4. Go Deeper (Optional Details)

Provide additional context for those who want it. Chunk into bullets.

**Axioms to use**:
- "Go deeper"
- "The details"
- "What's next"
- "What to watch"
- "The bottom line"

**Format**:
```
**Go deeper**:
• [Supporting point 1]
• [Supporting point 2]
• [Supporting point 3]
```

Keep bullets to 1-2 lines each. If longer, it's not scannable.

---

## Word-Level Rules

### Short Words Win

| Syllables | Strength |
|-----------|----------|
| 1 syllable | Strongest |
| 2 syllables | Medium |
| 3+ syllables | Weakest |

| Long (Avoid) | Short (Use) |
|--------------|-------------|
| Utilize | Use |
| Implement | Do, Build |
| Facilitate | Help |
| Demonstrate | Show |
| Approximately | About |
| Subsequently | Then |
| Regarding | About |
| Methodology | Method |

### Cut These Words

**Adverbs** (usually unnecessary):
- Very, really, extremely, highly
- Basically, essentially, fundamentally
- Actually, literally, definitely

**Hedge words** (commit or investigate):
- Seems, appears, might, could
- Somewhat, relatively, fairly
- Perhaps, possibly, potentially

**Filler phrases**:
- "As you know..."
- "I wanted to reach out..."
- "Just following up..."
- "Hope this finds you well..."

---

## Smart Brevity Format Template

```
**[6-word headline]**

[ONE sentence: the key takeaway.]

**Why it matters**: [1-2 sentences on reader relevance]

**The details**:
• [Bullet point 1]
• [Bullet point 2]
• [Bullet point 3]

**Bottom line**: [Optional final takeaway]
```

---

## Visual Formatting Rules

1. **Bold key terms** - Guide the scanner's eye
2. **Use bullets** - Not paragraphs for lists
3. **White space** - Break up dense text
4. **One idea per paragraph** - Max 3 sentences
5. **One message per slide/section** - Absorb in 3 seconds

---

## What to Avoid

The four ways to lose readers:
1. Too much text
2. Too much jargon
3. Too many choices
4. Buried point (lede not first)

Also avoid:
- Anecdotes (unless essential)
- Jokes (rarely land in text)
- Showing off knowledge
- Multiple asks in one message

---

# Part 3: Preserving Substance

The most important principle when editing existing content.

---

## The Core Rule

**Brevity ≠ Deletion. Simplify expression, preserve meaning.**

Shorter text that loses requirements is worse than longer text that contains them.

---

## The Substance Test

Before removing or condensing anything, ask:

1. **Is this a requirement?** → Keep it, make it explicit
2. **Is this a constraint?** → Keep it, make it specific
3. **Is this context that affects behavior?** → Condense, don't delete
4. **Is this truly redundant?** → Only delete if said elsewhere
5. **Is this an edge case?** → Keep, users need to know

---

## Editing Prompts: Common Mistakes

| Mistake | Why It's Wrong | Correct Approach |
|---------|----------------|------------------|
| Delete long paragraph | May contain buried requirements | Extract requirements as bullets |
| Remove "obvious" constraint | AI doesn't share your assumptions | Make implicit → explicit |
| Cut examples | Examples often define edge cases | Keep unless truly redundant |
| Simplify by omission | Loses information | Simplify by restructuring |

---

## Before vs After Examples

### Example 1: Buried Requirements

❌ **Wrong** (deleted substance):
```
Before: "When processing the data, make sure to handle
errors gracefully, log all failures, and never expose
raw error messages to users."

After: "Process the data carefully."
```

✅ **Right** (extracted and clarified):
```
Before: "When processing the data, make sure to handle
errors gracefully, log all failures, and never expose
raw error messages to users."

After: "Process the data with these rules:
- Handle errors gracefully
- Log all failures
- Never expose raw error messages to users"
```

### Example 2: Implicit Context

❌ **Wrong** (assumed it was obvious):
```
Before: "Generate a summary. Remember this is for
executives who only have 30 seconds."

After: "Generate a summary."
```

✅ **Right** (made explicit):
```
Before: "Generate a summary. Remember this is for
executives who only have 30 seconds."

After: "Generate an executive summary.
Constraint: Readable in 30 seconds (≤50 words)."
```

### Example 3: Edge Cases

❌ **Wrong** (removed "unnecessary" detail):
```
Before: "Extract the date. If no year is specified,
assume current year. If date is ambiguous (like 01/02),
use MM/DD format."

After: "Extract the date."
```

✅ **Right** (kept rules, restructured):
```
Before: "Extract the date. If no year is specified,
assume current year. If date is ambiguous (like 01/02),
use MM/DD format."

After: "Extract the date:
- Missing year → use current year
- Ambiguous format → interpret as MM/DD"
```

---

## Final Checklist

Before submitting any revision:

- [ ] Count requirements in original vs revision (should match or increase)
- [ ] All constraints still present?
- [ ] Edge cases preserved?
- [ ] Context that affects behavior kept?
- [ ] Result is shorter AND more explicit (not just shorter)?

**The goal**: Same information, clearer structure, fewer words.

---

# Summary

| Framework | Focus | Key Test |
|-----------|-------|----------|
| Classical Style | Clarity, precision | Can reader act without clarifying questions? |
| Smart Brevity | Structure, scannability | Can reader get the point in 10 seconds? |
| Preserve Substance | Meaning retention | Are all requirements still present? |

**Combined test**: Is every word necessary AND is the most important thing first AND is nothing lost?
