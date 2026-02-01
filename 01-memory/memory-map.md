<nexus-memory-map version="v4.0" updated="2026-01-07">
<!--
================================================================================
NEXUS MEMORY MAP - PERSISTENCE LAYER
================================================================================
Purpose: What memory files contain, their schemas, and how they evolve
For file locations: See system-map.md
For behavior rules: See orchestrator.md
================================================================================
-->

<section id="files">
## Memory Files

| File | Purpose | Updated By |
|------|---------|------------|
| goals.md | User identity + objectives | setup-memory |
| core-learnings.md | Accumulated insights | close-session |
| user-config.yaml | Preferences + tracking | setup-memory |
| integrations/*.yaml | Integration configs | *-connect skills |
| session-reports/*.md | Session history | close-session |
</section>

<section id="schemas">
## File Schemas

### goals.md
```
Current Role: [job title, context]
Short-Term Goal (3 months): [specific objective]
  - Success Metrics: [checkboxes]
Long-Term Vision (1-3 years): [direction]
Work Style: [focus areas, preferences]
```

### user-config.yaml
```yaml
user_preferences:
  language: "English"
  timezone: ""
  date_format: "YYYY-MM-DD"

learning_tracker:
  completed:
    setup_memory: true/false
    create_folders: true/false
    learn_integrations: true/false
    # ... more skills
```

### core-learnings.md
```
## What Works (Successes)
- Pattern that succeeded

## What to Avoid (Mistakes)
- Pattern that failed

## Best Practices
- Reusable pattern

## Insights
- Strategic realization
```

### integrations/*.yaml
```yaml
# e.g., langfuse.yaml, airtable-bases.yaml
api_key: [stored securely]
build_id: [connection info]
# Integration-specific config
```
</section>

<section id="evolution">
## How Memory Grows

```
Fresh Install → setup-memory → Working → close-session → Next Session
                    ↓              ↓           ↓
              goals.md set    work done    learnings captured
              user-config                  session-report created
```

### Update Triggers

| Event | Files Updated |
|-------|---------------|
| `setup-memory` skill | goals.md, user-config.yaml |
| `close-session` skill | core-learnings.md, session-reports/{date}.md |
| `*-connect` skills | integrations/{service}.yaml |
| Learning skill completed | user-config.yaml (learning_tracker) |
</section>

</nexus-memory-map>
