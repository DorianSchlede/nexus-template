# Session Size & Complexity Analysis

**Phase**: 3 (Size & Complexity Analysis)
**Date**: 2026-01-05

---

## Summary

**Key Finding**: Most sessions fit within 100k context windows. Large sessions (100+ traces) may exceed 50k but still fit in 100k. Chunking is rarely needed.

---

## Session Size Measurements

### Sample Sessions (Without Full Observations)

| Session | Traces | File Size | Est Tokens | 50k Fit | 100k Fit | 200k Fit |
|---------|--------|-----------|------------|---------|----------|----------|
| Small (1c96db43...) | 8 | 93 KB | ~23k | Yes (47%) | Yes (23%) | Yes (12%) |
| Medium (8172830f...) | 14 | 132 KB | ~33k | Yes (66%) | Yes (33%) | Yes (16%) |
| Large (5ff25b22...) | 100 | 288 KB | ~72k | **No** (144%) | Yes (72%) | Yes (36%) |

**Note**: These measurements are from `get-session` which returns traces WITHOUT observations.

### With Full Observations

When fetching individual traces with `get-trace` (includes observations):

| Component | Size | Est Tokens |
|-----------|------|------------|
| Single trace + observation | ~28 KB | ~7k |
| Single observation | ~3 KB | ~700 |

**Extrapolation for full session with observations**:
- Small (8 traces): ~23k + (8 x 3k) = ~47k tokens
- Medium (14 traces): ~33k + (14 x 3k) = ~75k tokens
- Large (100 traces): ~72k + (100 x 3k) = ~372k tokens (EXCEEDS 200k!)

---

## Input Size Distribution

Individual trace inputs vary significantly:

| Session | Min Input | Max Input | Avg Input |
|---------|-----------|-----------|-----------|
| Small | 4 chars | 30 KB | ~10 KB |
| Medium | 26 chars | 47 KB | ~7 KB |
| Large | 0 chars | 41 KB | ~2 KB |

**Observation**: Larger sessions have smaller average inputs (more short tool confirmations).

---

## Context Window Recommendations

### For Scoring Sessions

| Context Size | What Can Fit |
|--------------|--------------|
| 50k tokens | Small sessions (< 15 traces) without observations |
| 100k tokens | Medium sessions (< 50 traces) without observations |
| 200k tokens | Large sessions (< 100 traces) without observations |
| **Cannot fit** | Large sessions WITH full observations |

### Recommended Approach

1. **Default**: Fetch session traces without observations (~30-70k tokens)
2. **Deep dive**: Fetch individual traces with observations only when needed
3. **Large sessions**: Chunk by trace batches (e.g., 20 traces at a time)

---

## Chunking Strategy

For sessions exceeding context:

### Option A: Time-Based Chunking
```
Session with 100 traces →
  Chunk 1: Traces 1-20 (first 20% of session)
  Chunk 2: Traces 21-40
  Chunk 3: Traces 41-60
  Chunk 4: Traces 61-80
  Chunk 5: Traces 81-100 (last 20% of session)
```

**Pros**: Preserves temporal context within each chunk
**Cons**: May split related interactions

### Option B: Summary + Sample
```
Session with 100 traces →
  Summary: Session metadata + trace list (no inputs)
  Sample: First 5, last 5, and 5 random traces with full content
```

**Pros**: Fits in small context, sees beginning/middle/end
**Cons**: May miss important middle context

### Option C: Hierarchical Scoring
```
Level 1: Score each trace individually (7k tokens each)
Level 2: Aggregate trace scores into session score
```

**Pros**: Can handle any session size
**Cons**: Loses cross-trace context

### Recommended: Option A with Smart Boundaries

Split at natural boundaries:
- After skill completion markers
- After user confirms completion
- After close-session patterns

---

## Implications for Scoring Architecture

1. **Trace-level scoring is feasible**
   - Each trace fits easily (< 30k tokens)
   - Include 1-2 context traces for continuity

2. **Session-level scoring needs strategy**
   - Small/medium: Score whole session
   - Large: Use chunking or hierarchical approach

3. **Observation-level scoring is cheap**
   - Only ~700 tokens per observation
   - Can score all observations without context pressure

4. **Input tokens not tracked**
   - Current tracing only captures output tokens
   - May need to estimate input costs from content size

---

## Data Points for Planning

| Metric | Value |
|--------|-------|
| Sessions in sample | 43 |
| Avg traces per session | ~15-20 (median) |
| Large session threshold | > 50 traces |
| Very large session threshold | > 100 traces |
| Max observed session | 100 traces |

---

## Open Questions

- [ ] What % of sessions are "large" (> 50 traces)?
- [ ] Do very long sessions (1000+ traces) exist?
- [ ] Can we get trace counts without fetching all data?

---

*Next: Phase 4 - Langfuse API Validation*
