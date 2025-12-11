# Steps

## Phase 1: Implementation

- [x] Add `--embed-content` argument to nexus-loader.py argparse
- [x] Create `embed_file_contents()` function to read files
- [x] Integrate into `load_startup()` to populate `memory_content`
- [x] Return content keyed by filename in JSON output

## Phase 2: Testing

- [x] Test `--startup --embed-content` returns all memory files
- [x] Verify JSON output is valid and parseable
- [x] Confirm backward compatibility (without flag works as before)

## Phase 3: Documentation

- [x] Update orchestrator.md with new loading pattern
- [x] Update CLAUDE.md if startup sequence changes
- [x] Update system-map.md with new pattern
- [x] Make embedding default (remove --embed-content flag)
- [x] Remove all files_to_load references
