#!/usr/bin/env python3
"""
Generate Structure Script
Creates a complete philosophy document structure from research notes.
"""

import json
import sys
from typing import Dict, List, Any
from datetime import date


STANDARD_SECTIONS = [
    {
        "id": "executive-summary",
        "title": "Executive Summary",
        "description": "Core philosophy in 3-5 sentences, the problem, the solution, and proof of effectiveness"
    },
    {
        "id": "foundational-principles",
        "title": "Foundational Principles",
        "description": "5-8 key principles with definition, rationale (why it works), and application guidance"
    },
    {
        "id": "framework",
        "title": "Framework & Methodology",
        "description": "Step-by-step application process, decision trees, and workflow patterns"
    },
    {
        "id": "anti-patterns",
        "title": "Anti-Patterns Dictionary",
        "description": "Common mistakes with symptoms, why they fail, fixes, and impact metrics"
    },
    {
        "id": "checklists",
        "title": "Design Checklists",
        "description": "Pre-design, mid-design, post-design, and execution checklists"
    },
    {
        "id": "case-studies",
        "title": "Case Studies",
        "description": "Real-world examples with before/after comparisons and results"
    },
    {
        "id": "measurement",
        "title": "Measurement Framework",
        "description": "Success metrics, KPIs, red flags, and measurement methods"
    },
    {
        "id": "references",
        "title": "Research References",
        "description": "Academic sources, industry research, and authoritative documentation"
    }
]


def generate_document_structure(domain: str, research_notes: Dict[str, Any] = None) -> str:
    """
    Generate a complete philosophy document structure.

    Args:
        domain: The domain (e.g., "Landing Page Design")
        research_notes: Optional research findings to incorporate

    Returns:
        Markdown document structure with placeholders
    """

    doc = f"""# {domain} Philosophy: Design Standards & Best Practices

**Document Type**: Design Standards & Philosophy
**Scope**: {domain}
**Status**: Living Document
**Version**: 1.0
**Last Updated**: {date.today().strftime("%Y-%m-%d")}

---

## Table of Contents

"""

    # Generate table of contents
    for i, section in enumerate(STANDARD_SECTIONS, 1):
        doc += f"{i}. [{section['title']}](#{section['id']})\n"

    doc += "\n---\n\n"

    # Generate sections
    for section in STANDARD_SECTIONS:
        doc += f"## {section['title']}\n\n"
        doc += f"> **Purpose**: {section['description']}\n\n"

        if section['id'] == 'executive-summary':
            doc += """**Core Philosophy**: [STATE CORE PHILOSOPHY IN 1 SENTENCE]

**The Problem**: [DESCRIBE THE PROBLEM THIS PHILOSOPHY SOLVES]

**The Solution**: [DESCRIBE THE APPROACH/METHODOLOGY]

**Proof**: [CITE RESEARCH OR EVIDENCE OF EFFECTIVENESS]

---

"""

        elif section['id'] == 'foundational-principles':
            doc += """### Principle 1: [PRINCIPLE NAME]

**Definition**: [Clear definition of the principle]

**Why This Works**: [Research-backed rationale]

**Application**:
- [X] WRONG: [Example of incorrect application]
- [OK] RIGHT: [Example of correct application]

**Test**: [How to verify if principle is being followed]

---

[REPEAT FOR 5-8 PRINCIPLES]

"""

        elif section['id'] == 'framework':
            doc += """### [FRAMEWORK NAME]

```
[VISUAL FRAMEWORK DIAGRAM OR FLOWCHART]
```

#### Phase 1: [PHASE NAME]

**Purpose**: [What this phase accomplishes]

**Key Activities**:
- [Activity 1]
- [Activity 2]
- [Activity 3]

**Quality Checklist**:
- [ ] [Quality criterion 1]
- [ ] [Quality criterion 2]
- [ ] [Quality criterion 3]

**Time Budget**: [X%] of total process

---

[REPEAT FOR EACH PHASE]

"""

        elif section['id'] == 'anti-patterns':
            doc += """### Anti-Pattern 1: "[PATTERN NAME]"

**Symptom**: [How to recognize this mistake]

**Example**:
```
[X] WRONG:
[Concrete example of the anti-pattern]
```

**Why It Fails**: [Explanation with research/metrics]

**Fix**: [How to avoid or correct]

**Metrics**: [Impact data if available]

---

[REPEAT FOR 5-10 ANTI-PATTERNS]

"""

        elif section['id'] == 'checklists':
            doc += """### Pre-Design Checklist

**Define Success Criteria**:
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

**Audience Analysis**:
- [ ] [Analysis point 1]
- [ ] [Analysis point 2]

---

### Mid-Design Checklist

**[Category 1]**:
- [ ] [Check 1]
- [ ] [Check 2]

**[Category 2]**:
- [ ] [Check 1]
- [ ] [Check 2]

---

### Post-Design Checklist

**Quality Assurance**:
- [ ] [QA check 1]
- [ ] [QA check 2]

**Validation**:
- [ ] [Validation check 1]
- [ ] [Validation check 2]

---

"""

        elif section['id'] == 'case-studies':
            doc += """### Case Study: [BUILD/EXAMPLE NAME]

**Context**: [Background and situation]

**Challenge**: [What problem needed solving]

**Approach**: [How principles were applied]

**Before**:
- [Metric 1]: [Before value]
- [Metric 2]: [Before value]
- [Metric 3]: [Before value]

**After**:
- [Metric 1]: [After value] ([X%] improvement)
- [Metric 2]: [After value] ([X%] improvement)
- [Metric 3]: [After value] ([X%] improvement)

**Key Insights**:
- [Insight 1]
- [Insight 2]
- [Insight 3]

---

[REPEAT FOR 2-3 CASE STUDIES]

"""

        elif section['id'] == 'measurement':
            doc += """### Success Metrics Hierarchy

```
+--------------------------------------------------------+
| TIER 1: CRITICAL METRICS (Make or Break)              |
+--------------------------------------------------------+
| * [Metric 1]: [Description]                           |
|   Target: [X%] | Baseline: [Y%]                       |
|                                                        |
| * [Metric 2]: [Description]                           |
|   Target: [X%] | Baseline: [Y%]                       |
+--------------------------------------------------------+

[REPEAT FOR TIER 2, 3, 4]
```

### Red Flags

```
[!!] CRITICAL RED FLAGS:

1. [Metric] < [Threshold]
   -> [What this indicates] - [Required action]

2. [Metric] < [Threshold]
   -> [What this indicates] - [Required action]

[!]  WARNING SIGNS:

3. [Metric] [Condition]
   -> [What this indicates] - [Suggested action]
```

---

"""

        elif section['id'] == 'references':
            doc += """### Academic Sources

1. **[Topic Area]**:
   - Author, A. (Year). "Title of paper/book"
   - Author, B. (Year). "Another reference"

2. **[Another Topic]**:
   - Author, C. (Year). "Reference"

### Industry Research

1. **[Source Name]**: [Key findings or reports]
2. **[Source Name]**: [Key findings or reports]

### Best Practice Documentation

1. **[Resource Name]**: [Description and URL if applicable]
2. **[Resource Name]**: [Description and URL if applicable]

---

"""

        doc += "\n"

    doc += f"""## Conclusion

**Document Status**: Living Document - Update as research evolves

**Last Major Update**: {date.today().strftime("%Y-%m-%d")}

**Next Review**: [Specify timeline]

**Maintained By**: [Team/Role]

---

*"[INSPIRATIONAL CLOSING QUOTE RELATED TO THE DOMAIN]"*
"""

    return doc


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_structure.py <domain>")
        sys.exit(1)

    domain = sys.argv[1]
    structure = generate_document_structure(domain)
    print(structure)


if __name__ == "__main__":
    main()
