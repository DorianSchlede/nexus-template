# Output Locations Reference

Where slack-power saves extracted content to workspace.

## Default Paths

| Workflow | Output Path | Filename Pattern |
|----------|-------------|------------------|
| get-thread | `04-workspace/07-insights/slack-extracts/` | `{date}-{target}-thread.md` |
| extract-schemas | `04-workspace/07-insights/technical/` | `{date}-{source}-schemas.md` |
| extract-actions | `04-workspace/07-insights/slack-extracts/` | `{date}-actions.md` |
| meeting-prep | `04-workspace/07-insights/meeting-prep/` | `{date}-{person}.md` |

## Path Variables

| Variable | Format | Example |
|----------|--------|---------|
| `{date}` | YYYY-MM-DD | 2025-12-31 |
| `{target}` | username or channel | burak, engineering |
| `{source}` | username, channel, or search term | burak, MetaTuner |
| `{person}` | username | burak |

## Folder Structure

```
04-workspace/
└── 07-insights/
    ├── patterns/           # Cross-interview patterns (existing)
    ├── decisions/          # Key decisions (existing)
    ├── technical/          # Schemas, code snippets, interfaces
    ├── meeting-prep/       # Context documents before meetings
    └── slack-extracts/     # General extractions, threads, actions
```

## Configuration

In `01-memory/user-config.yaml`:

```yaml
slack_power:
  auto_save: "ask"  # Options: "ask", "always", "never"
```

- **ask**: Prompt before saving (default)
- **always**: Auto-save without prompt, show path
- **never**: Display only, don't save
