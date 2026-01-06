---
name: langfuse-get-project
description: "Get Langfuse project info. Load when user says 'get project', 'current project', 'project info', 'langfuse project'."
---

# Get Project

Get the project associated with the current API key.

## Usage

### CLI
```bash
python scripts/get_project.py
```

### Python
```python
from get_project import get_project

project = get_project()
```

## API Reference

```
GET /api/public/projects
```

See: `langfuse-master/references/api-reference.md`
