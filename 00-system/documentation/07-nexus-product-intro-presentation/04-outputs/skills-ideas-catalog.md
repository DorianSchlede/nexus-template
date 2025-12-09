# Skills Ideas Catalog - What You Can Build with Nexus

**Purpose**: Comprehensive catalog of Skills you can build to transform your Solutions Engineering workflow
**Audience**: Workshop participants looking for concrete ideas and implementation templates
**Based on**: Real pain points from Nov 2024 workshop + 7-phase client lifecycle JTBD research

---

## 🎯 How to Use This Catalog

**Pick Skills based on**:
1. **Your biggest pain point** (what takes the most time/causes most frustration)
2. **Highest ROI** (time savings estimates provided for each Skill)
3. **Team multiplier potential** (which Skills your team would reuse most)
4. **Phase coverage** (build Skills across all 7 phases for complete lifecycle automation)

**Implementation approach**:
- Week 2-3 of workshop: Build 2-3 Skills from "Quick Wins" section
- Month 2: Build 5-7 more Skills from your specific phase pain points
- Month 3+: Build advanced Skills and integrations

---

## ⚡ QUICK WINS - Start Here (Week 2-3)

These Skills have the highest ROI and easiest implementation. Build these first!

### 1. Weekly Client Update Automation ⭐ **HIGHEST ROI**

**Pain Point**: Manual status emails every Friday take 4 hours
**Time Savings**: 4 hours → 30 minutes (87.5% reduction)
**Phase**: All phases (Phase 2-7)

**What it does**:
- Auto-gathers project progress from Linear tasks
- Pulls latest test results from Airtable evaluations
- Generates formatted email with consistent structure
- Includes metrics, blockers, next steps

**Implementation**:
```markdown
SKILL: weekly-client-update

INPUTS:
- Linear board ID
- Airtable base ID (evaluations table)
- Client name
- Week ending date

PROCESS:
1. Fetch completed tasks from Linear (this week)
2. Fetch evaluation metrics from Airtable (latest run)
3. Generate email template with:
   - Summary: X tasks completed, Y in progress
   - Metrics: Accuracy X%, latency Y ms
   - Blockers: [extract from Linear blocked tasks]
   - Next week: [extract from Linear upcoming tasks]
4. Format as client-ready email

OUTPUTS:
- 04-outputs/weekly-update-[date].md
- Pre-filled email ready to send

MCP INTEGRATIONS:
- Linear: list_issues (filter: updated this week)
- Airtable: list_records (evals table, sort by date desc)
```

**Real example** (from workshop):
> "Every Friday I spend 4 hours manually compiling updates from Linear, Airtable, Slack threads, email chains... this would save me SO much time." - Workshop participant

---

### 2. Test Report Generation ⭐ **HIGH ROI**

**Pain Point**: Manual test report creation from Airtable eval data takes 3 hours
**Time Savings**: 3 hours → 20 minutes (89% reduction)
**Phase**: Phase 5 (Testing & Optimization)

**What it does**:
- Pulls evaluation data from Airtable
- Generates charts/visualizations (accuracy, latency, cost trends)
- Creates formatted report with executive summary
- Highlights regressions and improvements

**Implementation**:
```markdown
SKILL: test-report-generator

INPUTS:
- Airtable base ID (evaluations table)
- Test run date range
- Report template preference

PROCESS:
1. Fetch eval records from Airtable (date range)
2. Calculate metrics:
   - Accuracy: average, min, max, trend
   - Latency: p50, p95, p99
   - Cost: total, per-query average
   - Regressions: any metric worse than previous run
3. Generate visualizations (ASCII charts for markdown)
4. Write executive summary (1 paragraph)
5. Compile full report with test cases + results

OUTPUTS:
- 04-outputs/test-report-[date].md
- 04-outputs/test-metrics-[date].csv (raw data)

MCP INTEGRATIONS:
- Airtable: list_records (evals table)
- Airtable: search_records (for specific test cases)
```

**Real example** (from workshop):
> "I have 8 CSV files of test results that I manually compile into PowerPoint every sprint. This is mind-numbing work." - Workshop participant

---

### 3. Prompt Engineering Templates ⭐ **CONSISTENCY BOOST**

**Pain Point**: "Incorrect prompts → variable results" (Fahad's workshop quote)
**Time Savings**: Not about time - about **consistency and quality**
**Phase**: Phase 3 (Discovery), Phase 4 (Build)

**What it does**:
- Provides standardized prompt templates for common tasks
- Ensures consistent discovery questions
- Reduces prompt iteration cycles (get it right first time)
- Captures best-practice prompts from senior SEs

**Implementation**:
```markdown
SKILL: prompt-engineering-templates

TEMPLATES INCLUDED:
1. Discovery Deep Dive Prompts
   - Workflow extraction: "Walk me through a typical [X]..."
   - Edge case probing: "What happens when [exception]?"
   - Success criteria: "How would you measure success?"

2. Agent Scoping Prompts
   - Capability boundaries: "What should the agent NOT do?"
   - Data requirements: "What data sources are available?"
   - Integration points: "What systems does this connect to?"

3. Test Case Generation Prompts
   - Happy path: "Generate test cases for ideal scenario"
   - Edge cases: "Generate test cases for [exception type]"
   - Adversarial: "Generate test cases that would break this"

PROCESS:
1. User selects template category
2. User provides context (client name, workflow type)
3. Skill generates customized prompt with placeholders filled
4. User copies prompt and uses in discovery/build

OUTPUTS:
- 02-resources/prompts/discovery-prompts-[client].md
- 02-resources/prompts/build-prompts-[client].md
```

**Real example** (from workshop):
> "Consistency is more important than speed. Incorrect prompts lead to variable results, which causes rework." - Fahad (Workshop, Nov 2024)

---

## 📋 PHASE 1: Pre-Contract Assessment

### 4. Pre-Contract Assessment Checklist ⭐ **PREVENT DISASTERS**

**Pain Point**: "Kickoff Nov 1st, docs arrive Nov 20th → 20 days lost" - Hassan
**Time Savings**: 20+ days lost → 0 days lost
**Phase**: Phase 1 (Pre-Contract Assessment)

**What it does**:
- Flags missing requirements BEFORE kickoff date is set
- Validates all prerequisites are met
- Creates accountability checklist for Sales → SE handoff
- Prevents "surprise gaps" 3 weeks into project

**Implementation**:
```markdown
SKILL: pre-contract-assessment

CHECKLIST ITEMS:
□ Technical documentation received?
  - API specs
  - Data schemas
  - Integration requirements
  - Authentication flows

□ Access credentials provided?
  - Development environment
  - Staging environment
  - Data access (if needed for scoping)

□ Scope clarity achieved?
  - Success criteria defined
  - Edge cases discussed
  - Timeline realistic (SE sign-off)

□ Stakeholder availability confirmed?
  - Technical SME identified
  - Decision-maker accessible
  - Response time expectations set

GO/NO-GO DECISION:
If ANY item unchecked → Kickoff date NOT SET until resolved

PROCESS:
1. Load checklist template
2. Populate with client-specific items
3. Share with Sales team
4. Track completion status
5. Generate GO/NO-GO recommendation

OUTPUTS:
- 01-planning/pre-contract-assessment-[client].md
- 04-outputs/go-no-go-decision-[client].md

MCP INTEGRATIONS:
- Linear: create_issue (create blocking tasks for missing items)
- Gmail: Send checklist to Sales (template email)
```

**ROI Calculation**:
- Old way: 20 days lost waiting for docs (client frustration, delayed revenue)
- New way: 0 days lost (prerequisites validated before kickoff)
- **Impact**: Prevent $50K+ revenue delays per client

---

### 5. Lead Qualification Skill

**Pain Point**: Sales hands off leads that aren't technically feasible
**Time Savings**: 2-3 days of discovery → 2 hours of upfront validation
**Phase**: Phase 1 (Pre-Contract Assessment)

**What it does**:
- Validates technical feasibility before SE engagement
- Scores leads based on complexity, data availability, timeline
- Flags red flags early (unrealistic expectations, missing prerequisites)

**Implementation**:
```markdown
SKILL: lead-qualification

SCORING CRITERIA:
1. Technical Feasibility (0-10)
   - Are required integrations supported?
   - Is data structured/accessible?
   - Are success metrics measurable?

2. Complexity Assessment (0-10)
   - Number of integrations
   - Custom logic requirements
   - Edge case complexity

3. Timeline Realism (0-10)
   - Scope matches timeline?
   - Buffer for unknowns?
   - Client availability confirmed?

QUALIFICATION TIERS:
- 24-30: GREEN (ideal client, high success probability)
- 16-23: YELLOW (feasible, but needs clarification)
- 0-15: RED (high risk, recommend scope reduction or decline)

PROCESS:
1. Intake form (Sales completes during discovery call)
2. Auto-score based on criteria
3. Generate recommendation (GO/MODIFY/NO-GO)
4. If YELLOW/RED: List specific concerns to address

OUTPUTS:
- 01-planning/lead-qualification-[client].md
- 04-outputs/qualification-recommendation.md
```

---

## 🚀 PHASE 2: Project Setup

### 6. Kickoff Deck Generator

**Pain Point**: Manual kickoff deck creation takes 3-4 hours
**Time Savings**: 3-4 hours → 30 minutes
**Phase**: Phase 2 (Project Setup)

**What it does**:
- Auto-generates kickoff presentation from project plan
- Pulls goals, timeline, stakeholders from Linear/Notion
- Creates consistent slide structure

**Implementation**:
```markdown
SKILL: kickoff-deck-generator

SLIDE STRUCTURE:
1. Project Overview (auto-pulled from project plan)
2. Goals & Success Metrics (from discovery notes)
3. Timeline & Milestones (from roadmap.md)
4. Team & Roles (from Linear project members)
5. Communication Cadence (template + customizations)
6. Next Steps & Immediate Actions

PROCESS:
1. Read: 02-resources/discovery-notes.md
2. Read: 01-planning/roadmap.md
3. Fetch: Linear project members
4. Generate: Markdown slides with sections above
5. Output: Ready-to-present deck

OUTPUTS:
- 04-outputs/kickoff-deck-[client].md
- 04-outputs/kickoff-deck-[client].pdf (optional)

MCP INTEGRATIONS:
- Linear: get_project (fetch team members)
- Notion: Read discovery notes (if stored in Notion)
```

---

### 7. Linear Project Setup Automation

**Pain Point**: Manual Linear board setup takes 1-2 hours per client
**Time Savings**: 1-2 hours → 5 minutes
**Phase**: Phase 2 (Project Setup)

**What it does**:
- Creates Linear project with standard phases (Discovery → Build → Test → Launch)
- Generates template issues for each phase
- Sets up labels, milestones, automations

**Implementation**:
```markdown
SKILL: linear-project-setup

STANDARD PHASES (as Linear milestones):
1. Discovery & Scoping (2-3 weeks)
2. Build & Implement (4-8 weeks)
3. Testing & Optimization (2-3 weeks)
4. Go Live (1 week)
5. Maintenance (ongoing)

TEMPLATE ISSUES PER PHASE:
Phase 1 - Discovery:
- [ ] Deep dive discovery session
- [ ] Document current workflow
- [ ] Define success criteria
- [ ] Identify edge cases
- [ ] Create test case templates

Phase 2 - Build:
- [ ] Set up development environment
- [ ] Build core agent logic
- [ ] Implement integrations
- [ ] Add error handling
- [ ] Code review

...etc for all phases

PROCESS:
1. User provides: Client name, estimated timeline
2. Create Linear project
3. Create 5 milestones (phases)
4. Generate template issues for each phase
5. Set up labels (bug, feature, blocker, etc.)
6. Configure automations (auto-assign, status updates)

OUTPUTS:
- Linear project URL
- 04-outputs/linear-setup-summary.md

MCP INTEGRATIONS:
- Linear: create_project
- Linear: create_issue (bulk create template tasks)
- Linear: list_issue_statuses (use team's existing statuses)
```

---

## 🔍 PHASE 3: Discovery & Scoping

### 8. API Documentation Gatherer ⭐ **HIGH ROI**

**Pain Point**: "Integration takes time... 40% of discovery is integration R&D" - Jack
**Time Savings**: 40% of discovery phase → 10-15% of discovery
**Phase**: Phase 3 (Discovery & Scoping)

**What it does**:
- Auto-fetches API documentation from common sources
- Summarizes authentication methods, endpoints, rate limits
- Generates integration feasibility report
- Identifies common gotchas (based on past projects)

**Implementation**:
```markdown
SKILL: api-doc-gatherer

SUPPORTED SOURCES:
- Direct API spec URLs (OpenAPI/Swagger)
- Developer portal pages (parse with WebFetch)
- Context7 library documentation (via MCP)
- Internal knowledge base (past integration notes)

PROCESS:
1. User provides: API name or URL
2. Fetch documentation (WebFetch or Context7)
3. Extract key sections:
   - Authentication (API keys, OAuth, JWT?)
   - Base URL and versioning
   - Rate limits and quotas
   - Common endpoints (CRUD operations)
   - Webhooks/real-time capabilities
4. Check internal memory: Have we integrated this before?
5. Generate summary report

OUTPUTS:
- 02-resources/api-docs/[api-name]-summary.md
- 02-resources/api-docs/[api-name]-full-spec.json (if available)
- 03-working/integration-feasibility-[api-name].md

MCP INTEGRATIONS:
- WebFetch: Fetch developer portal pages
- Context7: get-library-docs (for common libraries)
- Obsidian: Search past project notes for integration patterns
```

**ROI Calculation**:
- Old way: 40% of 2-3 week discovery = 4-6 days spent on integration R&D
- New way: 10-15% of discovery = 1-2 days (with better quality)
- **Time saved**: 3-4 days per client

---

### 9. Discovery Deep Dive Session Guide

**Pain Point**: Inconsistent discovery sessions → missing edge cases
**Time Savings**: Not about time - about **capturing complete requirements first time**
**Phase**: Phase 3 (Discovery & Scoping)

**What it does**:
- Structured question framework for discovery calls
- Ensures all edge cases probed
- Captures tribal knowledge from senior SEs
- Generates actionable discovery notes

**Implementation**:
```markdown
SKILL: discovery-deep-dive-guide

QUESTION FRAMEWORK:
1. Current State Questions
   - Walk me through your current process for [X]
   - What tools do you use today?
   - Where do things typically break down?
   - What workarounds have you built?

2. Ideal State Questions
   - What would a perfect solution look like?
   - How would you measure success?
   - What would make this 10x better than today?

3. Edge Case Probing
   - What happens when [exception occurs]?
   - How do you handle [rare scenario]?
   - What's the worst case you've encountered?
   - What keeps you up at night about this workflow?

4. Data & Integration Questions
   - What data sources are involved?
   - What systems need to connect?
   - Who owns each data source?
   - What's the data freshness requirement?

5. Stakeholder & Process Questions
   - Who approves exceptions?
   - What compliance requirements exist?
   - Who are the power users?
   - What's the rollout plan?

PROCESS:
1. Load question framework
2. Conduct discovery session (use as checklist)
3. Take notes in structured format
4. AI summarizes into discovery report
5. Extract edge cases → test case templates

OUTPUTS:
- 02-resources/discovery-notes-[client].md (structured)
- 02-resources/edge-cases-[client].md (extracted)
- 03-working/test-case-templates-[client].md (generated)
```

---

### 10. Scope Document Generator

**Pain Point**: Manual scope docs take 2-3 hours, often miss details
**Time Savings**: 2-3 hours → 30 minutes
**Phase**: Phase 3 (Discovery & Scoping)

**What it does**:
- Auto-generates scope document from discovery notes
- Ensures all sections covered (in-scope, out-of-scope, assumptions)
- Creates client-ready deliverable

**Implementation**:
```markdown
SKILL: scope-doc-generator

DOCUMENT STRUCTURE:
1. Project Overview
   - Client name, workflow being automated
   - High-level goals

2. In-Scope
   - Features included
   - Integrations covered
   - Data sources accessed

3. Out-of-Scope (CRITICAL - prevents scope creep)
   - Features explicitly NOT included
   - Future phase considerations

4. Assumptions
   - Data availability
   - API access
   - Stakeholder availability
   - Timeline dependencies

5. Success Criteria
   - Measurable metrics
   - Acceptance criteria

6. Timeline & Milestones
   - Phase breakdown
   - Key deliverable dates

PROCESS:
1. Read: 02-resources/discovery-notes-[client].md
2. Extract: Goals, features, integrations
3. Generate: Scope document with all sections
4. Add: Out-of-scope section (from template + discovery)
5. Output: Client-ready scope doc

OUTPUTS:
- 04-outputs/scope-document-[client].md
- 04-outputs/scope-document-[client].pdf (optional)
```

---

## 🏗️ PHASE 4: Build & Implement

### 11. Code Review Checklist

**Pain Point**: Inconsistent code review standards
**Time Savings**: Not about time - about **code quality and preventing bugs**
**Phase**: Phase 4 (Build & Implement)

**What it does**:
- Standardized code review checklist
- Catches common mistakes (error handling, logging, testing)
- Ensures security best practices

**Implementation**:
```markdown
SKILL: code-review-checklist

CHECKLIST CATEGORIES:
1. Functionality
   □ Code does what it's supposed to do
   □ Edge cases handled
   □ Error messages are clear

2. Error Handling
   □ Try/catch blocks where needed
   □ Graceful degradation for API failures
   □ User-friendly error messages

3. Security
   □ No hardcoded credentials
   □ API keys in environment variables
   □ Input validation for user data
   □ SQL injection prevention (if applicable)

4. Testing
   □ Unit tests written
   □ Integration tests written
   □ Test coverage >80%

5. Documentation
   □ Function docstrings complete
   □ Complex logic commented
   □ README updated

6. Performance
   □ No N+1 queries
   □ Caching implemented where appropriate
   □ Rate limiting respected

PROCESS:
1. Load checklist template
2. Reviewer checks each item
3. Generate review summary (passed/failed items)
4. Create Linear issues for failed items

OUTPUTS:
- 03-working/code-review-[date].md
- Linear issues (for failed items)

MCP INTEGRATIONS:
- Linear: create_issue (for review findings)
```

---

### 12. Integration Testing Script Generator

**Pain Point**: Manual API testing is tedious and error-prone
**Time Savings**: 2-3 hours → 20 minutes per integration
**Phase**: Phase 4 (Build & Implement)

**What it does**:
- Auto-generates test scripts for API integrations
- Tests auth, common endpoints, error handling
- Validates integration before client demo

**Implementation**:
```markdown
SKILL: integration-test-generator

TEST CATEGORIES:
1. Authentication
   - Valid credentials → 200 OK
   - Invalid credentials → 401 Unauthorized
   - Expired token → 401 or 403

2. CRUD Operations
   - Create resource → 201 Created
   - Read resource → 200 OK
   - Update resource → 200 OK
   - Delete resource → 204 No Content

3. Error Handling
   - Malformed request → 400 Bad Request
   - Unauthorized access → 403 Forbidden
   - Resource not found → 404 Not Found
   - Rate limit exceeded → 429 Too Many Requests

4. Edge Cases
   - Large payload (1MB+)
   - Special characters in fields
   - Concurrent requests
   - Network timeout simulation

PROCESS:
1. User provides: API name, base URL, auth method
2. Load test template for auth type (API key, OAuth, etc.)
3. Generate test cases for endpoints
4. Output: Executable test script (Python or JS)
5. Run: Execute tests and generate report

OUTPUTS:
- 03-working/integration-tests-[api-name].py
- 04-outputs/integration-test-report-[api-name].md

MCP INTEGRATIONS:
- Context7: get-library-docs (for API client libraries)
```

---

## 🧪 PHASE 5: Testing & Optimization

### 13. Evaluation Framework Setup

**Pain Point**: Manual Airtable eval setup takes 2-3 hours
**Time Savings**: 2-3 hours → 15 minutes
**Phase**: Phase 5 (Testing & Optimization)

**What it does**:
- Auto-creates Airtable base for evaluations
- Sets up tables (Test Cases, Eval Runs, Results)
- Generates sample test cases from discovery notes

**Implementation**:
```markdown
SKILL: eval-framework-setup

AIRTABLE SCHEMA:
Table 1: Test Cases
- Test ID (auto-number)
- Test Name (text)
- Input (long text)
- Expected Output (long text)
- Category (single select: happy path, edge case, adversarial)
- Priority (single select: P0, P1, P2)

Table 2: Eval Runs
- Run ID (auto-number)
- Run Date (date)
- Model Version (text)
- Notes (long text)

Table 3: Results
- Result ID (auto-number)
- Test Case (link to Test Cases)
- Eval Run (link to Eval Runs)
- Actual Output (long text)
- Pass/Fail (checkbox)
- Accuracy Score (number, 0-100)
- Latency (ms) (number)
- Cost (number)
- Notes (long text)

PROCESS:
1. Create Airtable base (or use existing)
2. Create 3 tables with schema above
3. Import sample test cases (from discovery notes)
4. Set up views (by category, by priority, failed tests)
5. Generate test run template

OUTPUTS:
- Airtable base URL
- 04-outputs/airtable-setup-summary.md
- 03-working/sample-test-cases.csv (imported to Airtable)

MCP INTEGRATIONS:
- Airtable: create_table (for new bases)
- Airtable: create_field (for table schema)
- Airtable: create_record (bulk import test cases)
```

---

### 14. Regression Detection Skill

**Pain Point**: Manual regression testing misses subtle degradations
**Time Savings**: 1-2 hours → 10 minutes per test run
**Phase**: Phase 5 (Testing & Optimization)

**What it does**:
- Compares current eval run vs baseline
- Flags regressions (accuracy drop, latency increase, cost spike)
- Generates regression report with root cause hints

**Implementation**:
```markdown
SKILL: regression-detector

REGRESSION THRESHOLDS:
- Accuracy: >5% drop
- Latency: >20% increase
- Cost: >30% increase
- Failed test cases: Any previously passing test now fails

PROCESS:
1. Fetch: Latest eval run from Airtable
2. Fetch: Baseline eval run (or previous run)
3. Compare: Metrics for each test case
4. Identify: Regressions beyond thresholds
5. Generate: Regression report with affected tests

OUTPUTS:
- 04-outputs/regression-report-[date].md
- 04-outputs/regressions-to-investigate.csv

REPORT FORMAT:
## Regression Summary
- Total tests: X
- Regressions detected: Y
- P0 regressions: Z (CRITICAL)

## Regressions by Category
### Accuracy Regressions
- Test Case #42: 95% → 78% (-17%)
  - Root Cause Hint: Check prompt changes for [category]

### Latency Regressions
- Test Case #15: 200ms → 450ms (+125%)
  - Root Cause Hint: New API call added?

MCP INTEGRATIONS:
- Airtable: list_records (fetch eval runs)
- Linear: create_issue (create P0 tasks for critical regressions)
```

---

## 🚀 PHASE 6: Go Live

### 15. Go-Live Checklist

**Pain Point**: Forgetting critical go-live steps → production incidents
**Time Savings**: Not about time - about **preventing disasters**
**Phase**: Phase 6 (Go Live)

**What it does**:
- Comprehensive go-live checklist (security, monitoring, docs, training)
- Ensures nothing is forgotten
- Creates accountability before launch

**Implementation**:
```markdown
SKILL: go-live-checklist

CHECKLIST CATEGORIES:
1. Security
   □ Production API keys rotated (not dev keys!)
   □ Rate limiting configured
   □ Error messages don't leak sensitive data
   □ Access controls tested

2. Monitoring
   □ Logging enabled
   □ Alerting configured (errors, latency spikes)
   □ Dashboard set up for client visibility

3. Documentation
   □ User guide complete
   □ Admin guide complete
   □ Runbook for common issues
   □ Escalation path defined

4. Training
   □ End users trained
   □ Admins trained
   □ Support team briefed

5. Rollback Plan
   □ Rollback procedure documented
   □ Tested rollback in staging
   □ Rollback approval process clear

GO/NO-GO DECISION:
If ANY item unchecked → GO LIVE DELAYED

PROCESS:
1. Load checklist template
2. Review each item with team
3. Track completion status
4. Generate GO/NO-GO recommendation

OUTPUTS:
- 01-planning/go-live-checklist-[client].md
- 04-outputs/go-live-decision-[client].md

MCP INTEGRATIONS:
- Linear: create_issue (for incomplete checklist items)
- Gmail: Send go-live status to stakeholders
```

---

### 16. Production Migration Script

**Pain Point**: "Staging vs production - manually duplicate agent, change API keys, transfer all data" - Hassan
**Time Savings**: 4-6 hours → 15 minutes
**Phase**: Phase 6 (Go Live)

**What it does**:
- Automated staging → production migration
- Handles environment-specific config (API keys, URLs)
- Validates migration before cutover

**Implementation**:
```markdown
SKILL: version-rollout (production migration)

MIGRATION STEPS:
1. Pre-Migration Validation
   - Staging tests passing?
   - Production environment ready?
   - Rollback plan confirmed?

2. Configuration Migration
   - Copy agent config from staging
   - Replace environment-specific values:
     * API keys (staging → production)
     * Base URLs (staging → production)
     * Database connections
   - Validate config (no staging values left)

3. Data Migration (if needed)
   - Export necessary data from staging
   - Transform for production (e.g., remove test data)
   - Import to production

4. Post-Migration Validation
   - Run smoke tests in production
   - Verify integrations working
   - Check monitoring/alerting active

5. Cutover
   - Update DNS/routing (if applicable)
   - Notify stakeholders
   - Monitor for 1 hour post-launch

PROCESS:
1. User confirms: Staging validated, rollback ready
2. Execute migration script
3. Run validation checks
4. Generate migration report

OUTPUTS:
- 04-outputs/migration-report-[date].md
- 04-outputs/production-config.yaml (with prod values)

MCP INTEGRATIONS:
- Linear: create_issue (if migration validation fails)
- Gmail: Send migration status to stakeholders
```

**ROI Calculation** (Hassan's pain point):
- Old way: 4-6 hours manual migration, high error risk
- New way: 15 minutes automated migration, validated
- **Time saved**: 4-6 hours per client + prevented production incidents

---

## 🔧 PHASE 7: Maintenance

### 17. Incident Response Runbook Generator

**Pain Point**: No standardized runbook → chaotic incident response
**Time Savings**: Not about time - about **reducing MTTR (mean time to recovery)**
**Phase**: Phase 7 (Maintenance)

**What it does**:
- Auto-generates runbook for common incidents
- Step-by-step troubleshooting guides
- Escalation paths and contact info

**Implementation**:
```markdown
SKILL: incident-runbook-generator

RUNBOOK STRUCTURE:
1. Incident Detection
   - How to identify this incident (symptoms)
   - Monitoring alerts that fire

2. Immediate Actions (First 5 Minutes)
   - Stop the bleeding (disable feature, rollback, etc.)
   - Notify stakeholders (who and when)

3. Diagnosis Steps
   - Check logs for [error pattern]
   - Verify API health for [integration]
   - Test [specific scenario]

4. Resolution Steps
   - If [root cause A]: Do [fix A]
   - If [root cause B]: Do [fix B]
   - Validate fix with [test]

5. Post-Incident
   - Document root cause
   - Create Linear issue for permanent fix
   - Update runbook with learnings

COMMON INCIDENTS COVERED:
- API rate limit exceeded
- Authentication failures
- Data sync issues
- Performance degradation
- Integration outages

PROCESS:
1. User selects incident type (or describes symptoms)
2. Load relevant runbook template
3. Customize with client-specific details
4. Output: Ready-to-use runbook

OUTPUTS:
- 02-resources/runbooks/incident-[type]-[client].md
- 04-outputs/runbook-summary.md

MCP INTEGRATIONS:
- Linear: create_issue (for post-incident follow-ups)
- Obsidian: Search past incidents for patterns
```

---

### 18. Performance Monitoring Dashboard Setup

**Pain Point**: Manual performance tracking is inconsistent
**Time Savings**: 8+ hours/week → 30 minutes/week
**Phase**: Phase 7 (Maintenance)

**What it does**:
- Auto-generates performance dashboard template
- Tracks key metrics (latency, accuracy, cost, errors)
- Alerts on anomalies

**Implementation**:
```markdown
SKILL: monitoring-dashboard-setup

KEY METRICS:
1. Latency
   - p50, p95, p99
   - Trend over time (hourly, daily)

2. Accuracy
   - Overall accuracy (%)
   - By test case category
   - Regression alerts

3. Cost
   - Total cost (daily, weekly)
   - Cost per query
   - Cost trend (increasing?)

4. Error Rate
   - Total errors
   - Errors by type (API failures, timeouts, etc.)
   - Error trend

5. Usage
   - Queries per day
   - Active users
   - Peak usage times

PROCESS:
1. User provides: Airtable base ID (where eval data lives)
2. Create dashboard template (markdown or visualization)
3. Set up data refresh automation (daily)
4. Configure alerts (thresholds for anomalies)

OUTPUTS:
- 04-outputs/dashboard-[client].md (markdown with charts)
- 04-outputs/alerts-config.yaml (alert thresholds)

MCP INTEGRATIONS:
- Airtable: list_records (fetch latest eval data)
- Linear: create_issue (create tasks for anomalies)
```

---

## 🌐 ADVANCED SKILLS - Month 2+

### 19. Multi-Client Skills Aggregation

**Pain Point**: Learning from Client #1 doesn't transfer to Client #2
**Time Savings**: Client #2 is 50% faster than Client #1
**Phase**: All phases (cross-client learning)

**What it does**:
- Analyzes Skills used across multiple clients
- Identifies common patterns
- Suggests Skills to generalize for team library

**Implementation**:
```markdown
SKILL: skills-aggregation

ANALYSIS:
1. Scan all projects (02-projects/*)
2. Extract Skills used per project
3. Identify Skills used 3+ times (high reuse)
4. Calculate time savings per Skill
5. Rank Skills by ROI

OUTPUTS:
- 04-workspace/skills-analytics.md
  - Top 10 Skills by reuse count
  - Top 10 Skills by time savings
  - Skills to generalize (used in similar forms)
  - Skills gaps (phases with low Skill coverage)

RECOMMENDATIONS:
- "Weekly Client Update used on 8 clients → generalize for team"
- "API Doc Gatherer saved 4 days per client → share with team"
- "Phase 3 has only 2 Skills → opportunity for more automation"

MCP INTEGRATIONS:
- Obsidian: Search all project folders for Skill references
- Linear: Track time saved (from Skill metadata)
```

---

### 20. Continuous Skills Library Growth

**Pain Point**: Skills library stagnates after initial creation
**Time Savings**: Not about time - about **ongoing improvement culture**
**Phase**: All phases (continuous)

**What it does**:
- Weekly prompts to identify new Skill opportunities
- Tracks Skill usage and suggests improvements
- Facilitates team Skill sharing

**Implementation**:
```markdown
SKILL: continuous-improvement-prompt

WEEKLY PROMPTS:
1. Repetition Detection
   - "What task did you do 2+ times this week?"
   - "What manual process took >1 hour?"
   - "What would you want automated for next client?"

2. Skill Usage Analysis
   - "Which Skills did you use this week?"
   - "Which Skills saved you the most time?"
   - "Which Skills need improvements?"

3. Team Sharing Opportunities
   - "Which Skills would your team find useful?"
   - "Who on your team faces similar pain points?"
   - "What Skills have teammates built that you'd use?"

PROCESS:
1. Every Friday (or close-session trigger)
2. AI asks weekly prompts
3. User responds
4. AI identifies Skill opportunities
5. User decides: Build now, backlog, or skip

OUTPUTS:
- 01-memory/weekly-reflections/[date].md
- 03-skills/backlog.md (Skill ideas to build later)

MCP INTEGRATIONS:
- Obsidian: Append to weekly reflections
- Linear: Create backlog issues for Skill ideas
```

---

## 📊 ROI SUMMARY - Total Time Savings

**Quick Wins (Week 2-3)** - Build these 3 Skills first:
1. Weekly Client Update Automation: **4 hrs → 30 min** (87.5% reduction)
2. Test Report Generation: **3 hrs → 20 min** (89% reduction)
3. Prompt Engineering Templates: **Consistency boost** (reduce rework cycles)

**Total from Quick Wins**: ~6.5 hours/week saved + quality improvements

---

**Phase Coverage (Month 2)** - Build 5-7 more Skills:
4. Pre-Contract Assessment: **20+ days lost → 0 days lost** (prevent disasters)
5. API Doc Gatherer: **4-6 days → 1-2 days** (40% discovery → 10-15%)
6. Linear Project Setup: **1-2 hrs → 5 min**
7. Production Migration: **4-6 hrs → 15 min** (Hassan's pain point)
8. Incident Runbook: **MTTR reduction** (faster incident response)

**Total from Phase Coverage**: ~15-20 hours/week saved + disaster prevention

---

**Full Lifecycle Automation (Month 3)** - Complete Skills library:
- 20+ Skills covering all 7 phases
- Team library with 50+ Skills (aggregated across SEs)
- **Result**: Client #2 is 50% faster than Client #1

**Total Impact**:
- Individual SE: 3-4 clients/year → 6-8 clients/year (2x capacity)
- Team of 10 SEs: 30-40 clients/year → 60-80 clients/year
- **Revenue impact**: $700K → $1.4M (same team size)

---

## 🎯 NEXT STEPS - How to Get Started

### Week 2-3 (Workshop):
1. **Pick your biggest pain point** from Quick Wins section
2. **Build 2-3 Skills** (start with Weekly Update, Test Report, or Prompts)
3. **Test on current client** work
4. **Measure time savings** (before/after)

### Month 2:
1. **Build 5-7 more Skills** covering your specific phase pain points
2. **Share with 1-2 teammates** for feedback
3. **Iterate based on feedback**
4. **Track ROI** (time saved, quality improvements)

### Month 3+:
1. **Generalize Skills** for team library
2. **Start Client #2** using Skills from Client #1
3. **Measure 50% speedup** (compare timelines)
4. **Continuous aggregation** (add 1-2 Skills/week)

---

**Ready to build?** Start with the Quick Wins section and pick your most painful workflow to automate first!

**Questions?** Refer back to:
- [skills-library-catalog.md](skills-library-catalog.md) (JTBD research - complete phase breakdown)
- [workshop-context-system-overview.md](workshop-context-system-overview.md) (workshop onboarding flow)
- [final-presentation-solutions-version.md](final-presentation-solutions-version.md) (slides for motivation)

---

**Skills Ideas Catalog** - v1.0
**Created**: 2025-11-25
**Purpose**: Give workshop participants maximum concrete ideas for Skills to build
**Based on**: Real SE pain points (Nov 2024 workshop) + 7-phase JTBD research
