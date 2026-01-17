# plan-build Workflows

**Note**: The core router workflow is embedded in [SKILL.md](../SKILL.md). This file is supplementary reference only.

---

## Router Workflow Summary

```
1. TYPE DETECTION      → Semantic match from _type.yaml descriptions
2. BUILD SETUP       → Run init_build.py with detected type
3. DISCOVERY           → Skill-based OR inline (depends on type)
4. MENTAL MODELS       → Run AFTER discovery (informed questioning)
5. RE-DISCOVERY        → If gaps found (max 2 rounds)
6. FINALIZATION        → Merge into plan.md, generate steps.md
```

**Key Principle**: Discovery BEFORE Mental Models

---

## Type → Discovery Method

| Type | Discovery | Skill |
|------|-----------|-------|
| build | Inline | - |
| integration | Skill | add-integration |
| research | Skill | create-research-build |
| strategy | Inline | - |
| content | Inline | - |
| process | Inline | - |
| skill | Skill | create-skill |
| generic | Inline | - |

---

## See Also

- [SKILL.md](../SKILL.md) - **Primary source** for router workflow
- [routing-logic.md](routing-logic.md) - Decision tree details
- [build-types.md](build-types.md) - Type descriptions
- [ears-patterns.md](ears-patterns.md) - EARS requirement templates
