# Implementation Plan

## Approach: Extend nexus-loader.py with --load-memory Flag

Instead of a separate script, we add a `--load-memory` flag to `nexus-loader.py` that:
1. Loads all memory files from `files_to_load`
2. Returns their content directly in JSON output
3. AI reads content from script output instead of separate Read calls

## Output Format

```json
{
  "loaded_at": "2025-12-11T...",
  "bundle": "startup",
  "system_state": "...",
  "memory_content": {
    "system-map.md": "# Nexus-v3 System Map\n...",
    "memory-map.md": "# Memory Map\n...",
    "goals.md": "# Your Goals\n...",
    "user-config.yaml": "---\nuser_preferences:\n..."
  },
  "instructions": {...},
  "metadata": {...}
}
```

## Alternative: Embedded Content Mode

Add a simpler approach - the script already identifies files to load. Just add their content inline:

```python
if args.embed_content:
    for file_path in result['files_to_load']:
        with open(file_path, 'r') as f:
            result['memory_content'][Path(file_path).name] = f.read()
```

## Implementation Steps

1. Add `--embed-content` flag to nexus-loader.py
2. When flag is set, read all `files_to_load` and embed content
3. Return content in `memory_content` dictionary
4. Update orchestrator.md to use new pattern (optional)
5. Test with startup sequence

## Token Considerations

Current approach: ~500 tokens for file paths + AI makes Read calls
New approach: ~3000-4000 tokens for embedded content

Trade-off: Slightly higher token count but fewer tool invocations = faster startup.
