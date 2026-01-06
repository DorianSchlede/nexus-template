# Subagent Flow Optimization Report

**Project**: 06-synthesis-pipeline-improvements
**Date**: 2025-12-28
**Status**: Multi-Chunk Test Complete - Optimizations Identified

---

## 1. Test Summary

### Configuration
| Parameter | Value |
|-----------|-------|
| Test Paper | 02-Knowledge_Graphs |
| Total Chunks | 15 |
| Total Tokens | ~162,000 |
| Token Budget/Subagent | 70,000 |
| Subagents Used | 3 parallel + 1 merge |
| Chunk Allocation | 1-5, 6-10, 11-15 |

### Results
| Aspect | Status |
|--------|--------|
| Split Strategy | SUCCESS |
| Parallel Execution | SUCCESS |
| Merge Operation | SUCCESS |
| Schema v2.3 Compliance | SUCCESS |
| Hash Verification | SUCCESS (15/15) |
| Validation | PARTIAL (4 issues) |

---

## 2. Root Cause Analysis Summary

### Issue Matrix

| # | Issue | Root Cause | Category | Fix Location |
|---|-------|------------|----------|--------------|
| 1 | Markdown stripped | LLM semantic processing | Validation | `normalize_markdown()` |
| 2 | Header in start | Ambiguous prompt | Documentation | N/A (works) |
| 3 | Headerless chunks | Rigid assumptions | Validation | `get_content_after_header()` |
| 4 | End position | Semantic vs positional | Validation | Expand to 40% |

### Root Cause Categories

```
                    ┌─────────────────────────────────────┐
                    │         ROOT CAUSE TREE             │
                    └─────────────────────────────────────┘
                                    │
           ┌────────────────────────┼────────────────────────┐
           │                        │                        │
    ┌──────▼──────┐         ┌──────▼──────┐         ┌──────▼──────┐
    │   LLM       │         │  Design     │         │  Content    │
    │   Behavior  │         │  Assumptions│         │  Diversity  │
    └──────┬──────┘         └──────┬──────┘         └──────┬──────┘
           │                        │                        │
    - Semantic                - All chunks             - Bibliography
      processing               have headers            - Appendix
    - Normalization          - Position =             - Footnotes
                               meaning
```

---

## 3. Subagent Flow Optimizations

### 3.1 Current Flow (Pre-Optimization)

```
┌─────────────────────────────────────────────────────────────────┐
│                    CURRENT SUBAGENT FLOW                        │
└─────────────────────────────────────────────────────────────────┘

User Request
    │
    ▼
┌──────────────────────────────────────────────────────────────────┐
│ ORCHESTRATOR: analyze-research-project                           │
│ - Reads _briefing.md (fields, research_purpose)                  │
│ - Reads _analysis_kit.md (templates)                             │
│ - Calculates token budget                                        │
│ - Spawns subagents based on paper size                           │
└──────────────────────────────────────────────────────────────────┘
    │
    ▼ (spawn 3 parallel subagents for 15 chunks)
    │
    ├────────────────┬────────────────┤
    │                │                │
    ▼                ▼                ▼
┌────────────┐ ┌────────────┐ ┌────────────┐
│ Subagent 1 │ │ Subagent 2 │ │ Subagent 3 │
│ Chunks 1-5 │ │ Chunks 6-10│ │ Chunks 11-15│
│ ~50k tokens│ │ ~57k tokens│ │ ~55k tokens│
└────────────┘ └────────────┘ └────────────┘
    │                │                │
    ▼                ▼                ▼
index_part1.md  index_part2.md  index_part3.md
_log_part1.md   _log_part2.md   _log_part3.md
    │                │                │
    └────────────────┼────────────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │ MERGE SUBAGENT         │
        │ - Combines 3 parts     │
        │ - Dedupes extractions  │
        │ - Creates unified      │
        │   index.md & log       │
        └────────────────────────┘
                     │
                     ▼
              index.md (merged)
              _analysis_log.md (merged)
```

### 3.2 Identified Bottlenecks

| Bottleneck | Impact | Cause |
|------------|--------|-------|
| Evidence normalization | Validation fails | LLM semantic processing |
| Chunk boundary detection | Incorrect evidence | Headerless sections |
| Position-based checks | False negatives | Semantic extraction |
| Quote verification | False warnings | Paraphrase vs literal |

### 3.3 Optimized Flow (Post-Fix)

```
┌─────────────────────────────────────────────────────────────────┐
│                   OPTIMIZED SUBAGENT FLOW                       │
└─────────────────────────────────────────────────────────────────┘

User Request
    │
    ▼
┌──────────────────────────────────────────────────────────────────┐
│ ORCHESTRATOR: analyze-research-project                           │
│ + ENHANCED: Pre-scan chunk types (has_header, content_type)     │
│ + ENHANCED: Adjust evidence rules per content type              │
└──────────────────────────────────────────────────────────────────┘
    │
    ▼
┌──────────────────────────────────────────────────────────────────┐
│ CHUNK PRE-ANALYSIS (NEW)                                         │
│ - Identify headerless chunks                                     │
│ - Tag as: section | bibliography | appendix                      │
│ - Set evidence extraction rules per type                         │
└──────────────────────────────────────────────────────────────────┘
    │
    ▼ (spawn parallel subagents with enhanced prompts)
    │
    ├────────────────┬────────────────┤
    │                │                │
    ▼                ▼                ▼
┌────────────┐ ┌────────────┐ ┌────────────┐
│ Subagent 1 │ │ Subagent 2 │ │ Subagent 3 │
│ + Knows    │ │ + Knows    │ │ + Knows    │
│   content  │ │   content  │ │   content  │
│   types    │ │   types    │ │   types    │
└────────────┘ └────────────┘ └────────────┘
    │                │                │
    ▼                ▼                ▼
┌──────────────────────────────────────────────────────────────────┐
│ VALIDATION (ENHANCED)                                            │
│ + normalize_markdown() - strips _*, **, *                        │
│ + Headerless detection - uses first 100 chars if no #            │
│ + Expanded end search - 40% instead of 30%                       │
│ + Hash-primary verification (text is debugging aid only)         │
└──────────────────────────────────────────────────────────────────┘
```

---

## 4. Recommended Changes

### 4.1 Immediate (Validation Script)

**File**: `03-skills/research-pipeline/skills/paper-analyze/scripts/validate_analysis.py`

```python
# ADD: normalize_markdown() function
def normalize_markdown(text: str) -> str:
    """Strip markdown formatting for comparison."""
    if not text:
        return text
    # Remove italic markers
    text = re.sub(r'_([^_]+)_', r'\1', text)
    # Remove bold markers
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    return text

# UPDATE: normalize_full() to use normalize_markdown()
def normalize_full(text):
    return normalize_ws(normalize_unicode(normalize_markdown(text)))

# UPDATE: get_content_after_header() for HTML comments
def get_content_after_header(content: str) -> str:
    """Get content after header, or handle headerless chunks."""
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('#'):
            return '\n'.join(lines[i + 1:]).lstrip('\n')
    # Handle PDF source comments
    if content.startswith('<!--'):
        end = content.find('-->')
        if end != -1:
            return content[end+3:].lstrip('\n')
    return content

# UPDATE: Expand end search from 30% to 40%
last_40_percent = chunk_content[int(len(chunk_content) * 0.6):]
```

**Estimated Effort**: 30 minutes

### 4.2 Short-Term (Subagent Prompts)

**File**: `03-skills/research-pipeline/orchestrators/analyze-research-project/SKILL.md`

Add to prompt template:

```markdown
## Evidence Extraction Rules (IMPORTANT)

When recording chunk evidence:
1. **start**: First 100 characters AFTER any `#` header line
   - If no header, use first 100 characters after `<!-- -->` comment
2. **mid**: ~100 characters from the middle 60% of content
3. **end**: Last 100 characters BEFORE any trailing whitespace
4. **PRESERVE** markdown formatting exactly (`_italic_`, `**bold**`)
```

**Estimated Effort**: 15 minutes

### 4.3 Medium-Term (Chunk Pre-Analysis)

Add script: `pre_analyze_chunks.py`

```python
def analyze_chunk_structure(paper_path: Path) -> Dict:
    """Pre-analyze chunks to identify content types."""
    results = {}
    for chunk_file in sorted(paper_path.glob("*_[0-9]*.md")):
        chunk_num = int(re.search(r'_(\d+)\.md', chunk_file.name).group(1))
        content = chunk_file.read_text(encoding='utf-8')

        results[chunk_num] = {
            "has_header": any(line.startswith('#') for line in content.split('\n')),
            "content_type": classify_content(content),
            "token_count": len(content) // 4
        }
    return results

def classify_content(content: str) -> str:
    """Classify chunk content type."""
    lower = content.lower()
    if re.search(r'\[\d+\].*\d{4}', content):  # References pattern
        return "bibliography"
    if "definition " in lower or "theorem " in lower:
        return "appendix"
    if "acknowledgement" in lower or "funding" in lower:
        return "acknowledgements"
    return "section"
```

**Estimated Effort**: 1 hour

---

## 5. Token Budget Optimization

### Current Allocation

| Paper Size | Chunks | Tokens | Subagents | Overhead |
|------------|--------|--------|-----------|----------|
| Small | 1-3 | <35k | 1 | 0% |
| Medium | 4-6 | 35-70k | 1 | 0% |
| Large | 7-10 | 70-120k | 2 | 15% merge |
| Very Large | 11-15 | 120-180k | 3 | 20% merge |
| Huge | 16+ | 180k+ | 4+ | 25% merge |

### Optimization Opportunities

1. **Reduce merge overhead**
   - Current: Merge subagent re-reads all extractions
   - Optimized: Script-based merge (no LLM needed for combining)

2. **Dynamic chunk balancing**
   - Current: Equal chunk distribution
   - Optimized: Token-balanced distribution (chunk 9 has 12k, chunk 15 has 7k)

3. **Skip low-value chunks**
   - Current: Analyze all chunks equally
   - Optimized: Light-touch for bibliography (hash only, skip extraction)

---

## 6. Quality Metrics

### Before Optimization

| Metric | Value |
|--------|-------|
| Start evidence match rate | 80% |
| Mid evidence match rate | 95% |
| End evidence match rate | 70% |
| Hash verification rate | 100% |
| Quote verification rate | 85% |
| Overall validation pass | 0% (WARNING) |

### After Optimization (Expected)

| Metric | Value |
|--------|-------|
| Start evidence match rate | 100% |
| Mid evidence match rate | 100% |
| End evidence match rate | 95% |
| Hash verification rate | 100% |
| Quote verification rate | 95% |
| Overall validation pass | 100% (PASSED) |

---

## 7. Implementation Plan

### Phase 1: Validation Fixes (Today)
- [ ] Add `normalize_markdown()` to validate_analysis.py
- [ ] Update `normalize_full()` to use it
- [ ] Expand end search to 40%
- [ ] Handle HTML comments in headerless chunks
- [ ] Re-run validation on Paper 02

### Phase 2: Prompt Updates (Next Session)
- [ ] Update analyze-research-project SKILL.md
- [ ] Add evidence extraction rules
- [ ] Document header handling

### Phase 3: Architecture (Future)
- [ ] Create `pre_analyze_chunks.py`
- [ ] Implement script-based merge
- [ ] Add token-balanced chunk distribution

---

## 8. Lessons Learned

### Design Principles

1. **LLMs are semantic processors, not text copiers**
   - Validation must normalize for semantic equivalence
   - Exact string matching is too brittle

2. **Assume content diversity**
   - Not all chunks have headers
   - Bibliography, appendix, footnotes are common
   - Design for edge cases upfront

3. **Position != Meaning**
   - "End of chunk" is semantic, not positional
   - Use flexible search regions

4. **Hash is ground truth**
   - Text evidence is for debugging
   - Hash verification proves chunk was read
   - Consider hash-only validation for speed

### Anti-Patterns Identified

| Anti-Pattern | Impact | Fix |
|--------------|--------|-----|
| Exact string matching | False negatives | Normalized comparison |
| Rigid position checks | Edge case failures | Flexible regions |
| Assuming ideal structure | Bibliography failures | Content type detection |
| Over-specifying evidence | Validation complexity | Hash-primary |

---

## 9. Appendix: Validation Code Changes

### Full Diff (Recommended)

```diff
--- a/validate_analysis.py
+++ b/validate_analysis.py
@@ -83,6 +83,18 @@ def normalize_unicode(text: str) -> str:
     return text


+def normalize_markdown(text: str) -> str:
+    """Strip markdown formatting for comparison."""
+    if not text:
+        return text
+    # Remove italic markers
+    text = re.sub(r'_([^_]+)_', r'\1', text)
+    # Remove bold markers
+    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
+    text = re.sub(r'\*([^*]+)\*', r'\1', text)
+    return text
+
+
 def get_content_after_header(content: str) -> str:
     """Get content after the first header line (# ...)."""
     lines = content.split('\n')
@@ -90,7 +102,12 @@ def get_content_after_header(content: str) -> str:
         if line.startswith('#'):
             # Return everything after this line
             return '\n'.join(lines[i + 1:]).lstrip('\n')
-    # No header found, return original
+    # No header found, check for HTML comment
+    if content.startswith('<!--'):
+        end = content.find('-->')
+        if end != -1:
+            return content[end+3:].lstrip('\n')
+    # Return original if no structure found
     return content


@@ -369,7 +386,7 @@ def validate_paper(paper_path: Path, strict: bool = False, check_chunk_index: bo
         # Helper to fully normalize text (Unicode + whitespace)
         def normalize_full(text):
             """Normalize Unicode and whitespace for comparison."""
-            return normalize_ws(normalize_unicode(text))
+            return normalize_ws(normalize_unicode(normalize_markdown(text)))

         if expected_start != actual_start:
             # Allow flexibility for whitespace and Unicode normalization
@@ -420,7 +437,8 @@ def validate_paper(paper_path: Path, strict: bool = False, check_chunk_index: bo
         # Validate end (flexible: accept if ANY portion of cited text appears in last 30%)
         # Note: Subagents may extract/format evidence slightly differently
         actual_end = evidence.get("end", "").strip()
         if actual_end:
-            last_30_percent = chunk_content[int(len(chunk_content) * 0.7):]
+            # Expanded to 40% for better coverage
+            last_40_percent = chunk_content[int(len(chunk_content) * 0.6):]
```

---

*Report generated: 2025-12-28*
*Project: 06-synthesis-pipeline-improvements*
*Schema Version: v2.3*
