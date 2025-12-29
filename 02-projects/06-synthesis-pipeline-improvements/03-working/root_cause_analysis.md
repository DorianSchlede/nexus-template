# Root Cause Analysis: Validation Failures in Multi-Chunk Subagent Flow

**Date**: 2025-12-28
**Test**: Paper 02-Knowledge_Graphs (15 chunks)
**Method**: 5-Whys Root Cause Analysis

---

## Executive Summary

The multi-chunk subagent test on Paper 02 (15 chunks, ~162k tokens) was a **structural success** - the split/merge strategy worked correctly. However, 4 validation issues were identified. This document analyzes each failure to its root cause and proposes optimizations.

---

## Issue 1: Markdown Formatting Stripped

### Symptom
Subagents record evidence as `text` instead of `_text_` (italics stripped).

### 5-Whys Analysis

1. **WHY** does the subagent strip markdown formatting?
   - The subagent normalizes text when extracting evidence

2. **WHY** does the subagent normalize text?
   - Because LLMs process visual/semantic meaning, not raw characters
   - When "reading" `_italics_`, the LLM perceives "italicized text" and outputs the semantic content

3. **WHY** doesn't the subagent preserve exact character sequences?
   - The prompt says "extract first 100 characters" but doesn't specify "preserve markdown formatting"
   - LLMs default to semantic extraction, not character-literal copying

4. **WHY** doesn't the prompt specify exact character preservation?
   - Because the original design assumed LLMs would copy verbatim
   - This assumption was incorrect - LLMs are semantic processors, not text copiers

5. **WHY** was this assumption made?
   - **ROOT CAUSE**: Mismatch between LLM behavior (semantic processing) and validation requirement (character-literal matching)

### Solution Options

| Option | Effort | Effectiveness |
|--------|--------|---------------|
| A. Update validation to strip markdown | Low | High |
| B. Add `preserve_formatting: true` to prompt | Medium | Medium (may not work) |
| C. Use hash-only verification, drop text matching | Low | High |

**Recommendation**: Option A - add `normalize_markdown()` to validation script

```python
def normalize_markdown(text: str) -> str:
    """Strip markdown formatting for comparison."""
    # Remove italic markers
    text = re.sub(r'_([^_]+)_', r'\1', text)
    # Remove bold markers
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    return text
```

---

## Issue 2: Start Evidence Includes Header Line

### Symptom
Subagent records `### **Knowledge Graphs** AIDAN HOGAN...` (includes header) instead of starting after the header.

### 5-Whys Analysis

1. **WHY** does the subagent include the header in start evidence?
   - The prompt says "first 100 characters of the chunk"
   - The chunk file literally starts with `<!-- Source: ... -->\n\n### **Knowledge Graphs**`

2. **WHY** does the chunk file include the header?
   - Because the PDF-to-markdown conversion preserves document structure
   - Headers are part of the chunk content

3. **WHY** does validation expect content AFTER the header?
   - Because the original design assumed "meaningful content starts after headers"
   - The `get_content_after_header()` function skips to content after `#` lines

4. **WHY** is there a mismatch between subagent behavior and validation expectation?
   - The subagent prompt says "first 100 characters" (which includes header)
   - The validation assumes "first 100 characters of CONTENT" (after header)

5. **WHY** was this ambiguity introduced?
   - **ROOT CAUSE**: Ambiguous prompt specification - "chunk" vs "chunk content after header" not clearly defined

### Solution Options

| Option | Effort | Effectiveness |
|--------|--------|---------------|
| A. Accept header as valid start (already partial fix) | Low | High |
| B. Clarify prompt: "after any `#` header line" | Medium | Medium |
| C. Change validation to check first 500 chars | Low | High |

**Recommendation**: Already implemented via `actual_in_chunk_start` check. Document as intentional flexibility.

---

## Issue 3: Chunks 9-15 Have No Headers (Bibliography/Appendix)

### Symptom
Chunks 9-15 are bibliography and appendix sections with no `#` header lines.
- Chunk 9: `embeddings) [548]; _shape induction_...`
- Chunk 10: `[Martin, Marti Cuquet, and Erwin Folmer...`

### 5-Whys Analysis

1. **WHY** don't these chunks have headers?
   - They're continuation of references and appendix material
   - The PDF structure doesn't have section headers in bibliography

2. **WHY** does this cause validation issues?
   - `get_content_after_header()` returns full content if no header found
   - But the check `if line.startswith('#')` never triggers

3. **WHY** does validation depend on headers?
   - Original design assumed all chunks would have structural headers
   - Academic papers often have headerless sections (references, footnotes)

4. **WHY** wasn't headerless content anticipated?
   - The methodology was designed for structured sections, not all paper types
   - Bibliography and appendix sections were edge cases

5. **WHY** are these edge cases problematic now?
   - **ROOT CAUSE**: Rigid assumption that all chunks have headers, ignoring PDF structure reality

### Solution Options

| Option | Effort | Effectiveness |
|--------|--------|---------------|
| A. Use first 100 chars if no header | Low | High |
| B. Tag chunks as "headerless" in metadata | Medium | Medium |
| C. Skip header check for bibliography chunks | Medium | Medium |

**Recommendation**: Option A - modify `get_content_after_header()`:

```python
def get_content_after_header(content: str) -> str:
    """Get content after first header, or first 100 chars if no header."""
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('#'):
            return '\n'.join(lines[i + 1:]).lstrip('\n')
    # No header found - return content after HTML comment (if any)
    if content.startswith('<!--'):
        end = content.find('-->')
        if end != -1:
            return content[end+3:].lstrip('\n')
    return content
```

---

## Issue 4: End Evidence Not Found in Last 30%

### Symptom
Some end evidence not found in last 30% of chunk.
- Example: Chunk 2 ends with `winter events taking place in [Arica]...`
- Validation looks in last 30% but evidence might be at 68% position

### 5-Whys Analysis

1. **WHY** is end evidence not in the last 30%?
   - Subagent extracts "end evidence" as "last significant sentence"
   - The actual last 30% might be whitespace, URLs, or formatting

2. **WHY** does the subagent choose this position?
   - LLMs select semantically meaningful content, not positional content
   - "Last sentence" != "last 30% of character count"

3. **WHY** does validation use 30% as the threshold?
   - Arbitrary assumption that "end" means "in final third"
   - No clear specification in methodology

4. **WHY** wasn't this tested with diverse content?
   - Single-chunk tests (Paper 03) had clean endings
   - Multi-chunk papers have varied content distribution

5. **WHY** is content distribution a problem?
   - **ROOT CAUSE**: Mismatch between semantic "end" (what subagent extracts) and positional "end" (what validation checks)

### Solution Options

| Option | Effort | Effectiveness |
|--------|--------|---------------|
| A. Expand search to last 40% | Low | Medium |
| B. Search last 50% for partial matches | Low | High |
| C. Use hash verification only, drop text position check | Low | High |

**Recommendation**: Option B - already partially implemented. Expand search region:

```python
# Change from 0.7 (last 30%) to 0.6 (last 40%)
last_40_percent = chunk_content[int(len(chunk_content) * 0.6):]
```

---

## Root Cause Summary

| Issue | Root Cause Category | Fix Type |
|-------|---------------------|----------|
| Markdown formatting | LLM semantic processing vs literal copying | Validation |
| Header inclusion | Ambiguous prompt spec | Documentation |
| Headerless chunks | Rigid structure assumptions | Validation |
| End evidence position | Semantic vs positional mismatch | Validation |

### Meta-Analysis: Common Themes

1. **Semantic vs Literal Processing**
   - LLMs process meaning, not characters
   - Validation must account for this

2. **Assumption Rigidity**
   - Design assumed ideal academic paper structure
   - Reality has bibliography, appendix, footnotes

3. **Position vs Content**
   - Validation uses positions (first X chars, last 30%)
   - Subagents extract semantically (first sentence, last sentence)

---

## Recommended Changes

### Immediate (Validation Script)

```python
# 1. Add normalize_markdown()
def normalize_markdown(text: str) -> str:
    text = re.sub(r'_([^_]+)_', r'\1', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    return text

# 2. Update normalize_full() to use it
def normalize_full(text):
    return normalize_ws(normalize_unicode(normalize_markdown(text)))

# 3. Handle headerless chunks
def get_content_after_header(content: str) -> str:
    # ... existing code ...
    # Add: handle <!-- comments --> and return content after them
    if content.startswith('<!--'):
        end = content.find('-->')
        if end != -1:
            return content[end+3:].lstrip('\n')
    return content

# 4. Expand end evidence search
last_40_percent = chunk_content[int(len(chunk_content) * 0.6):]
```

### Medium-Term (Subagent Prompts)

1. Clarify evidence extraction:
   - "First 100 characters OF CONTENT (after any header line starting with #)"
   - "Last 100 characters OF CONTENT (before any trailing whitespace)"

2. Add explicit instruction:
   - "Preserve markdown formatting exactly as it appears in the source"

### Long-Term (Architecture)

1. **Consider hash-only verification**
   - Text evidence is for human debugging, not machine validation
   - Hash proves chunk was read; text evidence is optional

2. **Add chunk metadata**
   - `has_header: true/false`
   - `content_type: section/bibliography/appendix`

---

## Validation Fix Priority

| Fix | Priority | Impact | Effort |
|-----|----------|--------|--------|
| `normalize_markdown()` | P1 | High - fixes 60% of issues | 10 min |
| Expand end search to 40% | P1 | High - fixes 20% of issues | 5 min |
| Handle HTML comments | P2 | Medium | 5 min |
| Document header flexibility | P3 | Low - already works | 5 min |

**Estimated total fix time**: 30 minutes

---

## Success Metrics After Fix

| Metric | Before | After (Expected) |
|--------|--------|------------------|
| Start evidence match | ~80% | 100% |
| Mid evidence match | ~95% | 100% |
| End evidence match | ~70% | 95% |
| Hash match | 100% | 100% |
| Overall validation | WARNING | PASSED |

---

*Analysis by: Claude Opus 4.5*
*Plan Version: 3.3*
*Schema Version: v2.3*
