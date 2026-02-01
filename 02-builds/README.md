# Builds

Builds are finite projects with a clear beginning, middle, and end. Use builds for features, research, designs, or any work that has completion criteria.

## Structure

```
02-builds/
├── active/          # Work in progress
│   └── {ID}-{name}/
│       ├── 01-planning/     # Purpose, plan, steps
│       ├── 02-resources/    # Reference materials
│       ├── 03-working/      # Work in progress
│       └── 04-outputs/      # Final deliverables
└── complete/        # Archived builds
```

## Commands

- **Start new**: `plan build [name]` or `build [name]`
- **Continue**: `continue build [ID]` or just the build number
- **Archive**: `archive build [name]`

## Planning Folder

Each build's `01-planning/` contains:
- `01-overview.md` - YAML metadata + purpose
- `02-discovery.md` - Research, questions
- `03-plan.md` - Approach, decisions
- `04-steps.md` - Execution checklist
- `resume-context.md` - Cross-session continuity

## Workflow

1. **Plan** - Define scope, research, create steps
2. **Execute** - Work through steps, track progress
3. **Deliver** - Move outputs to workspace
4. **Archive** - Move to complete/ when done
