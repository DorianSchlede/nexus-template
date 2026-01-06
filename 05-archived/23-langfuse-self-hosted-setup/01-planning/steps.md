# Langfuse Self-Hosted Setup - Execution Steps

**Last Updated**: 2026-01-03

**IMPORTANT**: This file tracks project progress. Mark tasks complete with [x] as you finish them.

---

## Phase 1: Prerequisites

- [x] Verify Docker Desktop is installed and running
- [x] Verify Node.js and npm are installed (`node --version`, `npm --version`)
- [x] Verify Git is installed (`git --version`)
- [x] Check available disk space (need 10GB+)
- [x] Check available RAM (need 8GB+, 16GB recommended)

---

## Phase 2: Deploy Langfuse via Docker Compose

### 2.1 Clone Repository
```bash
git clone https://github.com/langfuse/langfuse.git
cd langfuse
```
- [x] Clone Langfuse repository to `04-workspace/langfuse/`
- [x] Navigate to langfuse directory

### 2.2 Configure Secrets
- [x] Create `.env` file with secure random values:
  - [x] `NEXTAUTH_SECRET` (32+ char random string)
  - [x] `SALT` (32+ char random string)
  - [x] `ENCRYPTION_KEY` (32+ char random string for AES-256)
  - [x] `POSTGRES_PASSWORD`
  - [x] `CLICKHOUSE_PASSWORD`
  - [x] `MINIO_ROOT_PASSWORD`
- [x] Updated port to 3002 (3000/3001 were in use)

### 2.3 Start Containers
```bash
docker compose up -d
```
- [x] Run docker compose up
- [x] Wait for containers to start (2-3 minutes)
- [x] Verify langfuse-web shows "Ready" in logs
- [x] Access http://localhost:3002 in browser

### 2.4 Initial Setup
- [x] Create admin account at http://localhost:3002
- [x] Create new project (e.g., "Claude Code")
- [x] Generate API keys (Project Settings -> API Keys)
- [x] Copy Public Key (`pk-lf-...`) and Secret Key (`sk-lf-...`)

---

## Phase 3: Install claude-langfuse-monitor

### 3.1 Install Package
```bash
npm install -g claude-langfuse-monitor
```
- [x] Install claude-langfuse-monitor globally

### 3.2 Configure
```bash
npx claude-langfuse-monitor config \
  --host http://localhost:3002 \
  --public-key pk-lf-YOUR_PUBLIC_KEY \
  --secret-key sk-lf-YOUR_SECRET_KEY
```
- [x] Run config command with your API keys
- [x] Verify config saved to ~/.claude-langfuse/config.json

### 3.3 Verify Setup
```bash
npx claude-langfuse-monitor status
```
- [x] Run status check
- [x] Confirm connection to Langfuse is working

---

## Phase 4: Start Monitoring

### 4.1 Test Run (Foreground)
```bash
npx claude-langfuse-monitor start --history 1
```
- [x] Start monitor in foreground
- [x] Open Claude Code and have a conversation
- [x] Check Langfuse UI for new traces
- [x] Verify session grouping and metadata

### 4.2 Background Daemon
```bash
npx claude-langfuse-monitor start --history 1 &
```
- [x] Start monitor as background daemon
- [x] Verify it's running

### 4.3 Verify Traces
- [x] Open Langfuse UI (http://localhost:3002)
- [x] Navigate to Traces
- [x] Confirm Claude Code conversations appear (2800+ traces synced)
- [x] Check tool invocations are captured
- [x] Verify session grouping by project

---

## Phase 5: Production Hardening (Optional)

### 5.1 Persistence
- [x] Verify Docker volumes are configured for data persistence
- [x] Test restart: `docker compose down && docker compose up -d`
- [x] Confirm data survives restart (2795 → 2797 traces after restart)

### 5.2 Auto-Start
- [x] Docker Desktop: Settings → General → "Start Docker Desktop when you sign in"
- [x] Created `start-monitor.bat` in `04-workspace/langfuse/`
- [x] Added `ensure_langfuse_running()` to SessionStart hook
- [x] Langfuse containers auto-start on every Claude Code session

### 5.3 Backup Strategy
- [x] Document backup procedure for PostgreSQL
- [x] Document backup procedure for ClickHouse
- [x] Created `BACKUP.md` in `04-workspace/langfuse/`

---

## Quick Reference Commands

```bash
# Langfuse Docker
docker compose up -d              # Start
docker compose down               # Stop
docker compose logs -f            # View logs
docker compose up --pull always   # Upgrade

# claude-langfuse-monitor
claude-langfuse config            # Configure
claude-langfuse status            # Check status
claude-langfuse start             # Start (foreground)
claude-langfuse start --daemon    # Start (background)
claude-langfuse start --history 48 # Process last 48 hours
```

---

## Troubleshooting

**Langfuse not starting:**
- Check Docker Desktop is running
- Check port 3000 is not in use
- View logs: `docker compose logs langfuse-web`

**Monitor not connecting:**
- Verify API keys are correct
- Check Langfuse is accessible at configured host
- Run `claude-langfuse status` for diagnostics

**Traces not appearing:**
- Ensure Claude Code has project folders in ~/.claude/projects/
- Check monitor is running: `claude-langfuse status`
- Have a conversation and wait 30 seconds for sync

---

## Sources

- [Docker Compose Deployment](https://langfuse.com/self-hosting/deployment/docker-compose)
- [Self-Host Langfuse](https://langfuse.com/self-hosting)
- [claude-langfuse-monitor](https://github.com/michaeloboyle/claude-langfuse-monitor)
- [Claude Code Integration Discussion](https://github.com/orgs/langfuse/discussions/9088)

---

*Project Status: COMPLETE*
