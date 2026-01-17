---
name: Resource Dependency Mapping
slug: resource-dependency-mapping
category: time-resource
description: Identify critical resource constraints
when_to_use:
  - Build planning
  - Risk identification
  - Bottleneck prevention
  - Capacity planning
best_for: Understanding what resources you need and when
---

# Resource Dependency Mapping

**Purpose**: Identify critical resource constraints

## Questions to Ask

- What resources does this build require?
- Which resources are shared or constrained?
- What depends on what (dependency chain)?
- What's the critical path?
- What happens if a key resource is unavailable?
- Where do we need slack/buffer?

## Resource Categories

| Type | Examples |
|------|----------|
| **People** | Skills, availability, attention |
| **Money** | Budget, cash flow, funding |
| **Time** | Deadlines, schedules, availability |
| **Equipment** | Tools, systems, infrastructure |
| **Information** | Data, decisions, approvals |
| **External** | Vendors, partners, customers |

## Process

1. List all required resources
2. Identify constraints for each
3. Map dependencies (what needs what, when)
4. Find critical path (longest dependency chain)
5. Identify single points of failure
6. Build in slack/buffer for high-risk resources
7. Create contingency plans

## Dependency Types

- **Finish-to-Start**: B can't start until A finishes
- **Start-to-Start**: B can't start until A starts
- **Finish-to-Finish**: B can't finish until A finishes
- **Start-to-Finish**: B can't finish until A starts

## Critical Path

The longest chain of dependent activities. Delay here = build delay.

## Risk Indicators

- Single person with critical knowledge
- Shared resource across multiple builds
- External dependency with no control
- No buffer in schedule

## Output

Resource map with dependencies and critical path
