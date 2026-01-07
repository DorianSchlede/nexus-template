# Spawned Project: Weekly Quality Monitoring

**Parent Research**: Project 27 - Langfuse Annotation and Scoring Integration
**Estimated Effort**: Medium (3-4 sessions)
**Priority**: Medium (after scorer is working)
**Updated**: 2026-01-05 (Post-Validation Revision)

---

## Purpose

Create an automated weekly workflow that scores sessions, synthesizes patterns, and produces a monitoring report. This provides **visibility into session quality** for human review and decision-making.

**Important Distinction**: This is a **monitoring dashboard**, not a closed self-improvement loop. The system:
- Collects and scores session data
- Identifies patterns and outliers
- Generates suggestions for human review
- Does NOT automatically apply changes

Human review is required to close the loop by deciding which suggestions to implement.

---

## Scope

### Must Do
1. Build session fetcher that gets unscored sessions from past 7 days
2. Batch scoring with SessionScorer (from Project 29)
3. Pattern synthesizer to aggregate scores and identify trends
4. Suggestion generator to produce human-reviewable recommendations
5. Weekly report generator with actionable insights
6. Scheduled skill for Sunday 2am execution

### Out of Scope
- SessionScorer implementation (Project 29)
- Human calibration (Project 31)
- **Automatic application of suggestions** (by design - requires human review)
- Feedback loop closure (human responsibility)

---

## Dependencies

**Requires**:
- Score configs in Langfuse (Project 28)
- SessionScorer working (Project 29)
- Langfuse API access

**Enables**:
- Quality visibility and trend tracking
- Evidence-based decision making (human)
- Systematic identification of improvement opportunities

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              WEEKLY QUALITY MONITORING PIPELINE              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Schedule: Sunday 2:00 AM                                   │
│                                                              │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐ │
│  │  FETCH  │───►│  SCORE  │───►│SYNTHESIZE│───►│ SUGGEST │ │
│  │Sessions │    │Sessions │    │ Patterns │    │For Human│ │
│  │(7 days) │    │(batch)  │    │          │    │ Review  │ │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘ │
│       │              │              │              │        │
│       ▼              ▼              ▼              ▼        │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐ │
│  │Filter:  │    │Langfuse │    │Dimension │    │Pending  │ │
│  │min 3    │    │Scores   │    │Stats     │    │Review   │ │
│  │traces   │    │Storage  │    │Outliers  │    │Section  │ │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘ │
│                                                              │
│                         ┌─────────┐                         │
│                         │ REPORT  │                         │
│                         │ Weekly  │◄────── Human reviews    │
│                         │Dashboard│       and decides       │
│                         └─────────┘                         │
│                              │                               │
│                              ▼                               │
│                    01-memory/session-reports/               │
│                                                              │
│  ════════════════════════════════════════════════════════   │
│  HUMAN REVIEW REQUIRED: Suggestions in "Pending Review"     │
│  section require manual decision before implementation.     │
│  ════════════════════════════════════════════════════════   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Implementation Steps

### Phase 1: Session Fetcher

```python
def fetch_sessions_for_scoring(
    days_back: int = 7,
    min_traces: int = 3,
    exclude_scored: bool = True
) -> List[SessionInfo]:
    """Fetch sessions eligible for scoring."""

    # 1. Get sessions from date range
    from_date = datetime.now() - timedelta(days=days_back)
    sessions = langfuse.list_sessions(from_timestamp=from_date)

    # 2. Filter by trace count
    eligible = []
    for session in sessions:
        traces = langfuse.list_traces(session_id=session.id)
        if len(traces) >= min_traces:
            eligible.append(SessionInfo(
                id=session.id,
                trace_count=len(traces),
                created_at=session.createdAt
            ))

    # 3. Exclude already scored (check for overall_quality score)
    if exclude_scored:
        eligible = [s for s in eligible if not has_overall_quality_score(s.id)]

    return eligible
```

### Phase 2: Batch Scorer

```python
def score_sessions_batch(session_ids: List[str]) -> BatchResult:
    """Score multiple sessions with progress tracking."""

    scorer = SessionScorer()
    results = []

    for i, session_id in enumerate(session_ids):
        print(f"Scoring {i+1}/{len(session_ids)}: {session_id[:8]}...")

        try:
            scores = scorer.score_session(session_id)
            results.append(ScoringResult(
                session_id=session_id,
                scores=scores,
                success=True
            ))
        except Exception as e:
            results.append(ScoringResult(
                session_id=session_id,
                error=str(e),
                success=False
            ))

    return BatchResult(
        total=len(session_ids),
        success=len([r for r in results if r.success]),
        failed=len([r for r in results if not r.success]),
        results=results
    )
```

### Phase 3: Pattern Synthesizer

```python
def synthesize_patterns(scores: List[SessionScores]) -> SynthesisReport:
    """Analyze scores to identify patterns and trends."""

    # 1. Calculate dimension statistics
    dimension_stats = {}
    for dim in DIMENSIONS:
        values = [normalize_score(s[dim]) for s in scores]
        dimension_stats[dim] = {
            "mean": statistics.mean(values),
            "stdev": statistics.stdev(values) if len(values) > 1 else 0,
            "min": min(values),
            "max": max(values),
            "below_threshold": len([v for v in values if v < 0.7])
        }

    # 2. Identify outliers
    overall_scores = [s["overall_quality"]["score"] for s in scores]
    outliers = {
        "excellent": [s for s, o in zip(scores, overall_scores) if o > 0.85],
        "poor": [s for s, o in zip(scores, overall_scores) if o < 0.5]
    }

    # 3. Extract common issues from low-scoring sessions
    issues = extract_common_issues([s for s in scores if s["overall_quality"]["score"] < 0.7])

    return SynthesisReport(
        sessions_analyzed=len(scores),
        dimension_stats=dimension_stats,
        outliers=outliers,
        common_issues=issues
    )
```

### Phase 4: Suggestion Generator (For Human Review)

```python
def generate_suggestions(synthesis: SynthesisReport) -> List[Suggestion]:
    """Generate suggestions for HUMAN review - NOT auto-applied."""

    suggestions = []

    # Check each dimension
    for dim, stats in synthesis.dimension_stats.items():
        if stats["mean"] < 0.7:
            suggestion = generate_dimension_suggestion(dim, stats)
            suggestions.append(suggestion)

    # Add issue-based suggestions
    for issue in synthesis.common_issues[:3]:
        suggestion = generate_issue_suggestion(issue)
        suggestions.append(suggestion)

    return suggestions

def generate_dimension_suggestion(dim: str, stats: dict) -> Suggestion:
    """Use Claude subagent to generate specific improvement suggestion."""

    # This runs via Task tool with subagent
    prompt = f"""
    The dimension "{dim}" is underperforming:
    - Mean score: {stats['mean']:.2f}
    - Sessions below 0.7: {stats['below_threshold']}

    Suggest 1-2 specific changes that could improve this dimension.
    Focus on changes to:
    1. CLAUDE.md instructions
    2. Skill workflows
    3. System prompts

    Be specific and actionable. These will be reviewed by a human
    before any implementation.
    """

    # Execute via Task tool subagent
    result = execute_subagent(prompt)

    return Suggestion(
        dimension=dim,
        severity="high" if stats["mean"] < 0.5 else "medium",
        suggestion=result,
        evidence=stats,
        status="pending_review"  # ALWAYS starts as pending
    )
```

### Phase 5: Report Generator

```python
def generate_weekly_report(
    synthesis: SynthesisReport,
    suggestions: List[Suggestion]
) -> str:
    """Generate markdown report for session-reports/."""

    report = f"""# Weekly Session Analysis Report

**Period**: {synthesis.date_range[0]} to {synthesis.date_range[1]}
**Sessions Analyzed**: {synthesis.sessions_analyzed}

---

## Dimension Performance

| Dimension | Mean | Min | Max | Below 0.7 |
|-----------|------|-----|-----|-----------|
"""

    for dim, stats in synthesis.dimension_stats.items():
        report += f"| {dim} | {stats['mean']:.2f} | {stats['min']:.2f} | {stats['max']:.2f} | {stats['below_threshold']} |\n"

    report += f"""

---

## Outliers

**Excellent Sessions** ({len(synthesis.outliers['excellent'])}):
{format_outlier_list(synthesis.outliers['excellent'])}

**Poor Sessions** ({len(synthesis.outliers['poor'])}):
{format_outlier_list(synthesis.outliers['poor'])}

---

## Suggestions for Review

**Status**: Pending Human Review

"""

    for i, suggestion in enumerate(suggestions, 1):
        report += f"""### {i}. {suggestion.dimension} ({suggestion.severity})

**Status**: {suggestion.status}

{suggestion.suggestion}

**To implement**: Review suggestion, then manually apply if approved.

"""

    report += """
---

## Human Actions Required

1. Review each suggestion above
2. Decide: Approve / Reject / Modify
3. If approved, manually implement changes
4. Mark as "implemented" in next week's report

**Note**: This system provides visibility, not automation.
The improvement loop closes when YOU take action.
"""

    return report
```

### Phase 6: Scheduled Skill

Create `03-skills/langfuse/langfuse-weekly-analysis/SKILL.md`:

```yaml
---
name: langfuse-weekly-analysis
description: "Run weekly analysis of Claude Code sessions. Scores unscored sessions, synthesizes patterns, generates improvement suggestions."
schedule: "0 2 * * 0"  # Sunday 2am
---
```

---

## Success Criteria

- [ ] Fetches unscored sessions from past 7 days
- [ ] Batch scores 20+ sessions without failure
- [ ] Produces dimension statistics and outlier analysis
- [ ] Generates 2+ suggestions for human review
- [ ] Creates weekly monitoring report in `01-memory/session-reports/`
- [ ] Report clearly separates data from suggestions
- [ ] Suggestions marked as "pending_review" by default
- [ ] Skill can be run manually or scheduled

---

## Risks

| Risk | Mitigation |
|------|------------|
| API rate limits | Add delays between scoring calls |
| Scorer failures | Retry logic, skip failed sessions |
| No sessions to score | Graceful exit, note in report |
| Suggestion quality | Human review before applying |

---

## Outputs

- `03-skills/langfuse/langfuse-weekly-monitoring/` skill
- Weekly reports in `01-memory/session-reports/weekly-YYYY-MM-DD.md`
- Suggestions in report's "Pending Review" section (NOT auto-applied)

---

## Important: What This Is NOT

This is **NOT** a self-improving system. It is a **monitoring dashboard** that:

1. **Collects data**: Scores sessions automatically
2. **Identifies patterns**: Surfaces trends and outliers
3. **Generates suggestions**: Proposes potential improvements
4. **Requires human action**: YOU must decide what to implement

The feedback loop is only closed when a human:
- Reviews the weekly report
- Decides which suggestions to implement
- Manually makes changes to system files
- Tracks what was implemented vs rejected

Without human action, this is just a dashboard showing metrics.

---

*Ready to execute as Project 30*
