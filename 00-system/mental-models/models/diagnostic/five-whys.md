---
name: Root Cause Analysis (5 Whys)
category: diagnostic
description: Drill to fundamental causes
when_to_use:
  - Problem-solving
  - Getting beyond symptoms
  - Incident analysis
  - Process improvement
best_for: Finding root causes, not just symptoms
---

# Root Cause Analysis (5 Whys)

**Purpose**: Drill down to fundamental causes

## Questions to Ask

- Why did this happen?
- Why did THAT happen? (for each answer)
- Have we reached a cause we can actually address?
- Are there multiple root causes?
- Which root cause has the biggest impact?

## Process

1. State the problem clearly
2. Ask "Why did this happen?"
3. Take the answer and ask "Why?" again
4. Repeat until you reach a root cause (typically 5 times)
5. Verify you've reached an actionable root cause

## Example

**Problem**: Website went down

1. Why? → Server crashed
2. Why? → Memory ran out
3. Why? → Memory leak in application
4. Why? → Connections weren't being closed properly
5. Why? → Developer didn't know the API requirement

**Root cause**: Training gap on API usage

## Tips

- Don't stop at symptoms
- Sometimes you need more or fewer than 5 whys
- Multiple branches may exist (multiple root causes)
- Verify root cause with data if possible

## Output

Root cause(s) that can be addressed
