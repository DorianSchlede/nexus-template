# Discovery: Project Skill Handover

## Files to Modify

| File | Purpose | Change |
|------|---------|--------|
| `00-system/skills/projects/plan-project/SKILL.md` | Plan project workflow | Replace Step 10-11 (close session) with handover prompt |
| `00-system/skills/projects/execute-project/SKILL.md` | Execute project workflow | No changes needed - already handles fresh starts |

---

## Current Handover Flow (Problem)

```
PLAN-PROJECT SESSION
├─ Steps 1-9: Planning workflow
├─ Step 10: "Execute in SEPARATE SESSION" message
└─ Step 11: Trigger close-session
                    ↓
        [SESSION BOUNDARY - User must restart]
                    ↓
EXECUTE-PROJECT SESSION
├─ User says "work on {project}"
└─ Starts execution fresh
```

**Problems:**
1. Friction: User must close, restart, re-navigate
2. Context loss: Planning insights not carried over
3. Momentum loss: User is ready NOW but forced to wait

---

## Proposed Handover Flow (Solution)

```
PLAN-PROJECT SESSION (CONTINUED)
├─ Steps 1-9: Planning workflow
├─ Step 10 (NEW): Ask "Ready to start executing?"
│   ├─ YES → Load execute-project, continue in same session
│   └─ NO → Trigger close-session (preserve current behavior)
└─ Seamless transition to execution
```

---

## Patterns to Reuse

1. **execute-project SKILL.md** already has all execution logic
2. **resume-context.md** already tracks state (no changes needed)
3. **nexus-loader.py --project ID** can load project context mid-session

---

## Risks

| Risk | Mitigation |
|------|------------|
| Context window overflow | User has option to defer; most projects are <30% of context |
| Breaking existing behavior | Defer option preserves backward compatibility |

---

*Discovery complete. Ready for planning.*
