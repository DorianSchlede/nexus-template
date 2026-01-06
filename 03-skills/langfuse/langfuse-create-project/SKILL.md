---
name: langfuse-create-project
description: "Create a new project. Load when user says 'create langfuse project', 'new project'."
---

# Create Project

Create a new Langfuse project.

**Note**: This endpoint may be Cloud-only or require admin access.

## Usage

```bash
python scripts/create_project.py --name "My Project" --org "org-abc123"
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--name` | Yes | Project name |
| `--org` | Yes | Organization ID |

## API Reference

```
POST /api/public/v2/projects
```
