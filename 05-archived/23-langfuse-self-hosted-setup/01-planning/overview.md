---
id: 23-langfuse-self-hosted-setup
name: Langfuse Self-Hosted Setup
status: COMPLETE
description: "Load when user mentions 'setup langfuse', 'self-host langfuse', 'langfuse docker', 'claude code tracing', 'trace claude code'"
created: 2026-01-03
---

# Langfuse Self-Hosted Setup

## Purpose

Deploy a self-hosted Langfuse instance and integrate it with Claude Code for complete LLM observability. This provides:

1. **Full data ownership** - All traces stored on your infrastructure
2. **Claude Code tracing** - Capture all conversations, tool calls, and responses
3. **Cost tracking** - Monitor token usage and costs across all LLM calls
4. **No rate limits** - Self-hosted has no API rate limits

---

## Success Criteria

**Must achieve**:
- [ ] Langfuse running locally via Docker Compose
- [ ] Accessible at http://localhost:3000
- [ ] Claude Code conversations traced to Langfuse
- [ ] Sessions grouped by project/conversation
- [ ] Tool invocations captured (Bash, Read, Write, etc.)

**Nice to have**:
- [ ] Persistent storage configured
- [ ] Backup strategy documented
- [ ] Custom domain with HTTPS
- [ ] Integration with existing Beam Langfuse (https://tracing.beamstudio.ai)

---

## Context

**Background**:
- Currently using Beam's self-hosted Langfuse at https://tracing.beamstudio.ai
- Want local instance for Claude Code tracing specifically
- Claude Code emits OpenTelemetry logs (not traces) - requires special handling

**Stakeholders**:
- Developer using Claude Code daily
- Need visibility into AI assistant usage patterns

**Constraints**:
- Windows environment (Docker Desktop)
- Must work alongside existing Beam Langfuse instance
- Claude Code OTEL format requires transformation

---

## Architecture

```
┌─────────────────┐     ┌──────────────────────┐     ┌─────────────────┐
│   Claude Code   │────▶│ claude-langfuse-     │────▶│    Langfuse     │
│                 │     │ monitor (npm)        │     │  (Docker)       │
│  Conversations  │     │                      │     │                 │
│  Tool Calls     │     │ Watches ~/.claude/   │     │ localhost:3000  │
│  Responses      │     │ Converts to traces   │     │                 │
└─────────────────┘     └──────────────────────┘     └─────────────────┘
```

**Components**:
1. **Langfuse (Docker Compose)** - Self-hosted observability platform
   - Web UI + API (port 3000)
   - PostgreSQL (transactional data)
   - ClickHouse (trace/observation data)
   - Redis (caching)
   - MinIO (blob storage)

2. **claude-langfuse-monitor (npm)** - Bridge for Claude Code
   - Watches Claude Code project folders
   - Converts conversations to Langfuse traces
   - Runs as daemon or LaunchAgent

---

## Timeline

**Target**: Single session to deploy and configure

**Milestones**:
- Phase 1: Docker Compose deployment
- Phase 2: claude-langfuse-monitor setup
- Phase 3: Verify tracing works
- Phase 4: Configure persistence

---

*Next: Complete plan.md to define approach*
