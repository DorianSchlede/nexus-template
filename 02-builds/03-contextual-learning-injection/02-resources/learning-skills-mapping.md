# Learning Skills Mapping

Vollständige Übersicht aller Learning Skills mit ihren situativen Triggern.

---

## 1. Learn Builds

**Skill Path**: `00-system/skills/learning/learn-builds/SKILL.md`
**Duration**: 8-10 min
**Topics**: Builds vs Skills, Decision Framework, Build Structure, Lifecycle

**Trigger-Punkt**: User wird zu plan-build geroutet (erstes Mal)

**Trigger Code**:
```python
tool == 'Read' and 'plan-build/SKILL.md' in path
```

**Flag**: `first_encounters.learn_builds_offered`

**Prompt Template**:
```
🎯 FIRST TIME: BUILD PLANNING

This is your first time planning a build. Would you like me to:
1) Load the 8-10 min "Learn Builds" lesson now (covers: Builds vs Skills, Decision Framework, Build Structure)
2) Skip for now (I'll ask again next time)
3) Skip forever (don't ask again)

Choose 1, 2, or 3.
```

---

## 2. Learn Skills

**Skill Path**: `00-system/skills/learning/learn-skills/SKILL.md`
**Duration**: 10-12 min
**Topics**: Skill-Worthiness Framework, Skill Structure, Triggering

**Trigger-Punkt**: User wird zu create-skill geroutet (erstes Mal)

**Trigger Code**:
```python
tool == 'Read' and 'create-skill/SKILL.md' in path
```

**Flag**: `first_encounters.learn_skills_offered`

**Prompt Template**:
```
🎯 FIRST TIME: SKILL CREATION

This is your first time creating a skill. Would you like me to:
1) Load the 10-12 min "Learn Skills" lesson now (covers: Skill-Worthiness Framework, Structure, Triggering)
2) Skip for now (I'll ask again next time)
3) Skip forever (don't ask again)

Choose 1, 2, or 3.
```

---

## 3. Learn Integrations

**Skill Path**: `00-system/skills/learning/learn-integrations/SKILL.md`
**Duration**: 10-12 min
**Topics**: MCP Protocol, Available Integrations, When to Integrate

**Trigger-Punkt**: User wird zu add-integration oder connect-* geroutet (erstes Mal)

**Trigger Code**:
```python
tool == 'Read' and (
    'add-integration/SKILL.md' in path or
    'connect-notion/SKILL.md' in path or
    'connect-slack/SKILL.md' in path or
    'connect-airtable/SKILL.md' in path or
    'connect-google/SKILL.md' in path
)
```

**Flag**: `first_encounters.learn_integrations_offered`

**Prompt Template**:
```
🎯 FIRST TIME: INTEGRATION SETUP

This is your first time setting up an integration. Would you like me to:
1) Load the 10-12 min "Learn Integrations" lesson now (covers: MCP Protocol, Available Integrations, When to Integrate)
2) Skip for now (I'll ask again next time)
3) Skip forever (don't ask again)

Choose 1, 2, or 3.
```

---

## 4. Create Folders

**Skill Path**: `00-system/skills/learning/create-folders/SKILL.md`
**Duration**: 5 min
**Topics**: Workspace Structure Setup, Organization Patterns

**Trigger-Punkt**: User schreibt zum ersten Mal in 04-workspace/

**Trigger Code**:
```python
tool == 'Write' and '04-workspace/' in path
```

**Flag**: `first_encounters.create_folders_offered`

**Prompt Template**:
```
🎯 FIRST TIME: WORKSPACE USAGE

This is your first time using the workspace. Would you like me to:
1) Load the 5 min "Create Folders" lesson now (covers: Workspace Structure Setup, Organization Patterns)
2) Skip for now (I'll ask again next time)
3) Skip forever (don't ask again)

Choose 1, 2, or 3.
```

---

## 5. Learn Nexus

**Skill Path**: `00-system/skills/learning/learn-nexus/SKILL.md`
**Duration**: 15-18 min
**Topics**: Philosophy, 7 Problems, 7 Design Principles, Pitfalls, Expert Patterns

**Trigger-Punkt**: SCHWIERIG - Kein natürlicher Tool-Trigger

**Options**:
- A) SessionStart Hook nach 3+ Sessions?
- B) Manual trigger only ("learn nexus")
- C) Suggest after completing other learning skills?

**Flag**: `first_encounters.learn_nexus_offered`

**Prompt Template** (if triggered):
```
🎯 SYSTEM MASTERY AVAILABLE

You've been using Nexus for a while. Would you like me to:
1) Load the 15-18 min "Learn Nexus" lesson now (covers: Philosophy, Design Principles, Expert Patterns)
2) Skip for now (I'll ask again later)
3) Skip forever (don't ask again)

Choose 1, 2, or 3.
```

**Recommendation**: OUT OF SCOPE for PostToolUse Hook. Handle separately via SessionStart or manual trigger.

---

## 6. Setup Memory

**Skill Path**: `00-system/skills/learning/setup-memory/SKILL.md`
**Duration**: 5-7 min
**Topics**: Initial Onboarding, Goals, Preferences

**Trigger-Punkt**: Erste Session (SessionStart Hook)

**Flag**: `first_encounters.setup_memory_offered`

**Recommendation**: OUT OF SCOPE for PostToolUse Hook. This is first-session onboarding, handled by SessionStart Hook.

---

## Summary: PostToolUse Hook Scope

**IN SCOPE** (4 Learning Skills):
1. ✅ learn-builds (plan-build trigger)
2. ✅ learn-skills (create-skill trigger)
3. ✅ learn-integrations (add-integration/connect-* trigger)
4. ✅ create-folders (workspace write trigger)

**OUT OF SCOPE** (2 Learning Skills):
5. ❌ learn-nexus (no natural tool trigger - handle separately)
6. ❌ setup-memory (first session only - SessionStart Hook)

---

## Choice Handling Logic

**Choice 1 - Load onboarding:**
```
- Read: {skill_path}
- Execute full lesson content
- The lesson itself marks completion via user-config.yaml flag
- Continue with original workflow after lesson
```

**Choice 2 - Skip for now:**
```
- Do NOT modify any flags in user-config.yaml
- Flag remains false
- Continue with original workflow immediately
- Next trigger will ask again
```

**Choice 3 - Skip forever:**
```
- Edit 01-memory/user-config.yaml
- Set first_encounters.{skill_name}_offered: true
- Continue with original workflow immediately
- Never ask again
```

---

## Implementation Priority

**Phase 1** (High Value):
- learn-builds (most critical - foundational concept)
- learn-skills (second most critical)

**Phase 2** (Medium Value):
- learn-integrations (useful but not everyone needs)
- create-folders (nice to have)

**Phase 3** (Future):
- learn-nexus (advanced, handle separately)
- setup-memory (already handled via SessionStart)
