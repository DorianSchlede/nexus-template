---
id: 03-memory-loader-script
name: Memory Loader Script
description: Load when user mentions "memory loader", "consolidated memory", "single memory load", "optimize memory loading". Creates a script that loads all memory MD files in a single call instead of multiple parallel Read operations.
status: COMPLETE
onboarding: false
created: 2025-12-11
updated: 2025-12-11
completed: 2025-12-11
tags: [optimization, memory, loader, script]
---

# Memory Loader Script

## Problem Statement

Currently, the Nexus startup sequence requires the AI to:
1. Run `nexus-loader.py --startup`
2. Receive a `files_to_load` array with 4+ file paths
3. Make multiple parallel Read tool calls to load each file

This creates overhead - multiple tool invocations when a single script could return all content.

## Solution

Create `memory-loader.py` that:
- Reads all memory files (system-map.md, memory-map.md, goals.md, user-config.yaml)
- Concatenates them with clear delimiters
- Returns combined content in a single JSON output
- Optionally integrated into `nexus-loader.py` or as standalone

## Success Criteria

- [ ] Single script call returns all memory content
- [ ] Clear file delimiters for AI parsing
- [ ] Token-efficient output format
- [ ] Backward compatible with existing workflow
