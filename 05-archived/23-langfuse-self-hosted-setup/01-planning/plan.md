# Langfuse Self-Hosted Setup - Plan

**Last Updated**: 2026-01-03

---

## Approach

Two-phase deployment:

1. **Deploy Langfuse via Docker Compose**
   - Clone official repository
   - Update secrets in docker-compose.yml
   - Start containers
   - Create project and get API keys

2. **Install claude-langfuse-monitor**
   - Install npm package globally
   - Configure with Langfuse API keys
   - Run as background daemon
   - Verify traces appear

---

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **Deployment method** | Docker Compose | Simplest for local dev, official support |
| **Claude Code bridge** | claude-langfuse-monitor | Only working solution (native OTEL doesn't work) |
| **Port** | 3000 (default) | Avoid conflict with other services |
| **Storage** | Docker volumes | Persistence without external DB setup |

---

## Resources Needed

**Tools/Access**:
- Docker Desktop (Windows)
- Node.js / npm
- Git

**System Requirements**:
- 4+ CPU cores
- 8GB+ RAM (16GB recommended)
- 10GB+ disk space

**Information**:
- Langfuse repo: https://github.com/langfuse/langfuse
- claude-langfuse-monitor: https://github.com/michaeloboyle/claude-langfuse-monitor

---

## Dependencies & Links

**External Systems**:
- Docker Hub: Langfuse container images
- npm: claude-langfuse-monitor package
- Claude Code: ~/.claude/ project folders

**Related Projects**:
- Project 08: Langfuse Integration (COMPLETE) - API skills for Beam instance
- Project 22: Langfuse Integration Expansion - Additional API endpoints

**Files Created**:
- Docker Compose config (cloned from repo)
- ~/.claude-langfuse/config.json (monitor config)

---

## Technical Details

### Docker Compose Components

| Container | Purpose | Port |
|-----------|---------|------|
| langfuse-web | Main app + API | 3000 |
| langfuse-worker | Async processing | - |
| postgres | Transactional DB | 5432 |
| clickhouse | Analytics DB | 8123/9000 |
| redis | Cache | 6379 |
| minio | Blob storage | 9000/9090 |

### claude-langfuse-monitor

**What it captures**:
- User messages
- Assistant responses
- Tool invocations (Bash, Read, Write, etc.)
- Session grouping by project
- Git branch metadata
- Timing information

**How it works**:
- Watches `~/.claude/projects/` for changes
- Reads conversation transcripts
- Converts to Langfuse trace format
- Sends via Langfuse Python SDK

---

## Open Questions

- [x] How does Claude Code tracing work? → claude-langfuse-monitor watches project folders
- [x] Does native OTEL work? → No, CC emits logs not traces, needs transformation
- [ ] Can we run alongside Beam Langfuse? → Yes, different ports/instances
- [ ] Windows compatibility for monitor? → Need to test (macOS-focused)

---

## Alternative Approaches Considered

1. **Native OTEL Integration**
   - Status: Doesn't work
   - Reason: Claude Code emits OTEL logs, Langfuse expects traces

2. **Custom Stop Hook (like LangSmith)**
   - Status: Possible but complex
   - Reason: claude-langfuse-monitor already solves this

3. **LiteLLM Proxy**
   - Status: Works but heavyweight
   - Reason: Adds complexity for simple use case

---

*Next: Complete steps.md to break down execution*
