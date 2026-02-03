---
name: analyze-context
description: "Upload files for AI analysis. SubAgents extract insights and save structured documents."
priority: high
duration: "3-5 min"
standalone: true
---

# Analyze Context

Upload your existing files (docs, PDFs, code) and let SubAgents extract structured insights. Results are saved as clean documents - not dumped into chat context.

---

## Purpose

Help users upload context that informs:
- Goal refinement
- Workspace structure suggestions
- BUILD ideas
- Integration opportunities

**Key Principle**:
- `01-memory/input/` is TEMPORARY - holds uploads until organized
- SubAgents write to `01-memory/input/_analysis/` (also temporary)
- The "Organize Initial Context" BUILD distributes everything to `04-workspace/`
- After organization, `01-memory/input/` gets cleaned up

---

## Pre-Execution

**Create folders**:
```bash
mkdir -p 01-memory/input/           # Where user uploads files (temporary)
mkdir -p 01-memory/input/_analysis/ # Where analysis results go (temporary)
```

---

## Workflow

### Step 1: Explain & Invite Upload

**Display**:
```
CONTEXT UPLOAD
----------------------------------------------------

Have files that show what you work on?

I'll analyze them and extract:
  - What you do (role, domain)
  - Patterns in your work
  - Tools you use (integration opportunities)
  - Ideas for what to build

Upload to:
→ 01-memory/input/

Supported:
  - PDFs (text extraction automatic)
  - Word docs (.docx)
  - Text files (.txt, .md)
  - Images (.png, .jpg - for screenshots)
  - Code files

When done, type 'done'.
```

**Wait for user to upload and confirm "done"**

---

### Step 2: Scan & Validate Files

**Use Glob tool** to scan `01-memory/input/*`:

```python
from pathlib import Path

input_dir = Path("01-memory/input/")
uploaded_files = [f for f in input_dir.glob("*") if f.is_file()]

if not uploaded_files:
    print("No files found in 01-memory/input/")
    print("Please upload files and type 'done' when ready.")
    return

# Calculate total size
total_kb = sum(f.stat().st_size for f in uploaded_files) / 1024
file_count = len(uploaded_files)

print(f"Found {file_count} files ({total_kb:.1f} KB)")
```

---

### Step 3: Pre-Processing (Extract & Normalize)

**WHO does this?** The MAIN AI (you), BEFORE spawning SubAgents.

**WHY?** SubAgents can't read PDFs/DOCX reliably. We extract text first so they get clean .txt files.

**HOW it works:**

```
User uploads to 01-memory/input/:
  report.pdf (80 pages)
  notes.docx
  chat.json

Main AI pre-processes:
  1. Read report.pdf (Claude multimodal)
  2. Extract text → too large (150KB)
  3. Chunk into 3 parts → write to _analysis/extracted/
  4. Read notes.docx (via python-docx)
  5. Extract text → small enough
  6. Write to _analysis/extracted/notes.txt
  7. chat.json is already text → keep as-is

Result in _analysis/extracted/:
  report_chunk01.txt
  report_chunk02.txt
  report_chunk03.txt
  notes.txt

SubAgents receive paths to THESE files, not originals.
```

**CRITICAL: All files must be readable by SubAgents**

Before batching, convert all files to a format SubAgents can read:

| Original Format | Action | Result |
|----------------|--------|--------|
| `.txt`, `.md`, `.json` | Keep as-is | SubAgent reads directly |
| `.pdf` | Extract text | `_analysis/extracted/{name}.txt` |
| `.docx` | Extract text | `_analysis/extracted/{name}.txt` |
| `.png`, `.jpg` | Keep as-is | SubAgent uses Read tool (multimodal) |
| Large file (>50KB text) | Chunk | `_analysis/extracted/{name}_chunk{N}.txt` |

**Pre-Processing Script:**

```python
import os
from pathlib import Path

CHUNK_SIZE_KB = 50  # Split files larger than 50KB (~12,000 words)
EXTRACTED_DIR = Path("01-memory/input/_analysis/extracted")

def preprocess_files(uploaded_files):
    """
    Convert all files to SubAgent-readable format.
    Returns list of file paths for batching (may be more than input if chunked).
    """
    EXTRACTED_DIR.mkdir(parents=True, exist_ok=True)

    processable_files = []

    for file_path in uploaded_files:
        suffix = file_path.suffix.lower()

        if suffix == '.pdf':
            # Extract PDF to text
            extracted = extract_pdf_text(file_path)
            if extracted:
                processable_files.extend(extracted)  # May be multiple chunks

        elif suffix == '.docx':
            # Extract DOCX to text
            extracted = extract_docx_text(file_path)
            if extracted:
                processable_files.extend(extracted)

        elif suffix in ['.png', '.jpg', '.jpeg', '.gif', '.webp']:
            # Images: keep original, SubAgent uses multimodal Read
            processable_files.append(file_path)

        else:
            # Text-based files: check size, chunk if needed
            text_content = file_path.read_text(encoding='utf-8', errors='ignore')
            size_kb = len(text_content.encode('utf-8')) / 1024

            if size_kb > CHUNK_SIZE_KB:
                chunks = chunk_text(file_path.stem, text_content)
                processable_files.extend(chunks)
            else:
                processable_files.append(file_path)

    return processable_files


def extract_pdf_text(file_path):
    """Extract text from PDF, chunk if large"""
    try:
        import pdfplumber

        pdf = pdfplumber.open(file_path)
        full_text = ''

        for page in pdf.pages:
            page_text = page.extract_text() or ''
            full_text += page_text + '\n\n'

        pdf.close()

        # Check size and chunk if needed
        size_kb = len(full_text.encode('utf-8')) / 1024

        if size_kb > CHUNK_SIZE_KB:
            return chunk_text(file_path.stem, full_text)
        else:
            output_path = EXTRACTED_DIR / f"{file_path.stem}.txt"
            output_path.write_text(full_text)
            return [output_path]

    except Exception as e:
        print(f"PDF extraction failed for {file_path}: {e}")
        return []


def extract_docx_text(file_path):
    """Extract text from DOCX, chunk if large"""
    try:
        from docx import Document

        doc = Document(file_path)
        full_text = '\n'.join([p.text for p in doc.paragraphs])

        # Check size and chunk if needed
        size_kb = len(full_text.encode('utf-8')) / 1024

        if size_kb > CHUNK_SIZE_KB:
            return chunk_text(file_path.stem, full_text)
        else:
            output_path = EXTRACTED_DIR / f"{file_path.stem}.txt"
            output_path.write_text(full_text)
            return [output_path]

    except Exception as e:
        print(f"DOCX extraction failed for {file_path}: {e}")
        return []


def chunk_text(base_name, text, chunk_size_chars=50000):
    """
    Split large text into chunks.
    Returns list of chunk file paths.
    """
    chunks = []
    chunk_num = 1

    # Split by paragraphs to avoid cutting mid-sentence
    paragraphs = text.split('\n\n')
    current_chunk = ''

    for para in paragraphs:
        if len(current_chunk) + len(para) > chunk_size_chars:
            # Save current chunk
            chunk_path = EXTRACTED_DIR / f"{base_name}_chunk{chunk_num:02d}.txt"
            chunk_path.write_text(current_chunk)
            chunks.append(chunk_path)
            chunk_num += 1
            current_chunk = para
        else:
            current_chunk += '\n\n' + para if current_chunk else para

    # Save final chunk
    if current_chunk:
        chunk_path = EXTRACTED_DIR / f"{base_name}_chunk{chunk_num:02d}.txt"
        chunk_path.write_text(current_chunk)
        chunks.append(chunk_path)

    print(f"Split {base_name} into {len(chunks)} chunks")
    return chunks
```

**Display to user:**
```
Pre-processing {file_count} files...

  PDFs extracted: {pdf_count}
  DOCX extracted: {docx_count}
  Large files chunked: {chunked_count}

  Ready for analysis: {total_processable} items
```

**Error Recovery**:
- If pdfplumber not installed: `pip install pdfplumber`
- If python-docx not installed: `pip install python-docx`
- If extraction fails: Log error, skip file, continue with others
- If file unreadable: Mark as skipped, report to user

---

### Step 3b: AI Execution Guide (How YOU Do Pre-Processing)

**Option A: Use the pre-processing script (preferred)**

```bash
uv run 00-system/skills/learning/analyze-context/scripts/preprocess.py
```

The script automatically:
1. Scans `01-memory/input/` for uploaded files
2. Extracts text from PDFs (via pdfplumber)
3. Extracts text from DOCX (via python-docx)
4. Chunks large files (>50KB)
5. Outputs JSON list of processable file paths

**Output example:**
```
==================================================
PRE-PROCESSING COMPLETE
==================================================
Uploaded files:     20
PDFs extracted:     5
DOCX extracted:     3
Large files chunked:2
Skipped (errors):   0
Processable items:  24
==================================================

PROCESSABLE_FILES_JSON:
[
  "01-memory/input/_analysis/extracted/report_chunk01.txt",
  "01-memory/input/_analysis/extracted/report_chunk02.txt",
  ...
]
```

**Parse the JSON to get processable_files list for batching.**

**Option B: Manual with Claude's tools (fallback if script fails)**

For each file in `01-memory/input/`:

1. **PDF files:**
   ```
   - Use Read tool on the PDF (Claude reads PDFs natively)
   - If successful: extract text content
   - Check size: if > 50KB text, chunk it
   - Use Write tool to save to _analysis/extracted/{name}.txt or {name}_chunk{N}.txt
   ```

2. **DOCX files:**
   ```
   - Use Bash: python3 -c "from docx import Document; ..."
   - Or try Read tool (may work for simple DOCX)
   - Write extracted text to _analysis/extracted/{name}.txt
   ```

3. **Text files (.txt, .md, .json):**
   ```
   - Use Read tool to check size
   - If > 50KB: chunk and write to extracted/
   - If small: keep original path in processable list
   ```

4. **Images (.png, .jpg):**
   ```
   - Keep original path (SubAgent uses multimodal Read)
   ```

**Build the processable_files list:**

```python
processable_files = []

# For each uploaded file, add the appropriate path:
# - Original path for small text files and images
# - Extracted path for PDFs, DOCX
# - Multiple chunk paths for large files

# Example result:
processable_files = [
    Path("01-memory/input/_analysis/extracted/report_chunk01.txt"),
    Path("01-memory/input/_analysis/extracted/report_chunk02.txt"),
    Path("01-memory/input/_analysis/extracted/report_chunk03.txt"),
    Path("01-memory/input/_analysis/extracted/notes.txt"),
    Path("01-memory/input/chat.json"),  # small, kept as-is
    Path("01-memory/input/screenshot.png"),  # image, kept as-is
]
```

---

### Step 4: Calculate Agent Count & Create Batches

**CRITICAL: Batch the PRE-PROCESSED files, not originals**

```python
# Use pre-processed files from Step 3
processable_files = preprocess_files(uploaded_files)

print(f"Original uploads: {len(uploaded_files)}")
print(f"After pre-processing: {len(processable_files)} items")
# Note: count may be higher due to chunking large files
```

**Why pre-processed?**
- PDFs/DOCX → readable .txt files
- Large files → multiple chunks
- Images → kept as-is (multimodal)
- SubAgents can READ everything they're assigned

**Batch-based splitting (by count, not theme):**

```python
def calculate_batches(files, target_files_per_batch=5):
    """
    Split files into batches by count.
    Each SubAgent gets ~5 files to analyze thoroughly.

    Args:
        files: List of file paths
        target_files_per_batch: Aim for this many files per agent (default 5)

    Returns:
        List of batches, each batch is a list of files
    """
    file_count = len(files)

    # Calculate number of agents needed
    if file_count <= 5:
        agent_count = 1
    elif file_count <= 15:
        agent_count = 3
    elif file_count <= 30:
        agent_count = 5
    else:
        agent_count = min(10, (file_count + 4) // 5)  # Max 10 agents

    # Split files into batches
    batches = []
    batch_size = (file_count + agent_count - 1) // agent_count  # Ceiling division

    for i in range(0, file_count, batch_size):
        batch = files[i:i + batch_size]
        if batch:
            batches.append(batch)

    return batches

# Create batches from PRE-PROCESSED files
batches = calculate_batches(processable_files)
print(f"Created {len(batches)} batches for {len(processable_files)} items")
```

**Display to user**:
```
Splitting {file_count} files into {batch_count} batches for parallel analysis...

  Batch 1: {count} files
  Batch 2: {count} files
  ...
```

---

### Step 5: Spawn SubAgents in Parallel (Batch-Based)

**CRITICAL: SubAgents write DOCUMENTS, not dump into chat**

Each SubAgent:
1. Receives a numbered batch of files
2. Analyzes ALL files in its batch thoroughly
3. Writes to `01-memory/input/_analysis/batch-{N}-insights.md`
4. Returns only a brief summary (1-2 sentences)

**SubAgent Prompt Template**:

```markdown
# Context Analysis Agent - Batch {batch_number}

You are analyzing batch {batch_number} of {total_batches}.

## Your Task

1. Read ALL files in your batch
2. For EACH file, extract:
   - Main topic/purpose
   - Key information
   - Tools/services mentioned
   - Potential BUILD ideas
3. Write a STRUCTURED DOCUMENT to: 01-memory/input/_analysis/batch-{batch_number:02d}-insights.md
4. Return ONLY a 1-2 sentence summary to chat

## Files to Analyze

{file_list_with_paths}

## Document Structure

Write to `01-memory/input/_analysis/batch-{batch_number:02d}-insights.md`:

```markdown
# Batch {batch_number} Analysis

> Analyzed {file_count} files on {date}

## Files Analyzed

| File | Type | Main Topic |
|------|------|------------|
| {filename1} | {type} | {topic} |
| {filename2} | {type} | {topic} |

## Per-File Insights

### {filename1}

**Type**: {document type}
**Main Topic**: {what this file is about}
**Key Information**:
- {insight 1}
- {insight 2}

**Tools/Services Mentioned**: {list or "None"}
**Potential BUILD Ideas**: {ideas from this file}

---

### {filename2}

{repeat for each file}

---

## Batch Summary

**Common Themes**: {themes that appear across multiple files}
**Tools Mentioned**: {aggregated list}
**BUILD Ideas**: {aggregated list with source file}

---

*Auto-generated by analyze-context skill - Batch {batch_number}*
```

## IMPORTANT

- Analyze EACH file individually first
- Then synthesize common themes
- Write the FULL document to file
- Return ONLY a 1-2 sentence summary to chat
- Do NOT dump file contents into your response
```

**Spawn agents using Task tool** (parallel):
```python
# Use Task tool to spawn ALL agents in parallel
# Single message with multiple Task calls

for i, batch in enumerate(batches, start=1):
    file_list = "\n".join([f"- {f}" for f in batch])

    Task(
        subagent_type="general-purpose",
        prompt=agent_prompt.format(
            batch_number=i,
            total_batches=len(batches),
            file_list_with_paths=file_list,
            file_count=len(batch),
            date=today
        ),
        description=f"Analyzing batch {i}/{len(batches)} ({len(batch)} files)"
    )
```

---

### Step 6: Monitor & Display Progress

```
Analysis in progress...

  Batch 1: 5 files ████████░░ 80%
  Batch 2: 5 files ██████████ Done
  Batch 3: 5 files ██████░░░░ 60%
  Batch 4: 5 files ████░░░░░░ 40%
  Batch 5: 4 files ░░░░░░░░░░ Starting...

Waiting for all agents...
```

---

### Step 7: Aggregate All Batch Insights

After all SubAgents complete:

1. **Each agent wrote**: `01-memory/input/_analysis/batch-{N}-insights.md`
2. **Aggregation phase**: Read all batch files, synthesize into master summary

**CRITICAL: Validate completeness BEFORE aggregating**

**Aggregation Logic with Validation**:
```python
from pathlib import Path
from nexus.validation.validators import validate_aggregation_completeness

analysis_dir = Path("01-memory/input/_analysis/")
batch_files = sorted(analysis_dir.glob("batch-*-insights.md"))

# STEP 1: Validate all expected batches exist
expected_batch_count = len(batches)  # From Step 4
actual_batch_count = len(batch_files)

validate_aggregation_completeness(
    expected=expected_batch_count,
    actual=actual_batch_count,
    context="batch insights discovery"
)

# STEP 2: Read all batch insights
all_insights = []
for batch_file in batch_files:
    content = batch_file.read_text()
    all_insights.append({
        "file": batch_file.name,
        "content": content
    })

# STEP 3: Validate all batches were read
validate_aggregation_completeness(
    expected=expected_batch_count,
    actual=len(all_insights),
    context="batch insights reading"
)

# STEP 4: Now safe to create master summary
# All batches confirmed discovered and read
```

**If >3 batches: Use subagent for aggregation (recommended)**

```python
if expected_batch_count > 3:
    # Spawn aggregation subagent instead of doing it manually
    Task(
        subagent_type="general-purpose",
        prompt=f"""
        Aggregate all batch analysis files in 01-memory/input/_analysis/.

        CRITICAL REQUIREMENTS:
        1. List all batch-*-insights.md files (expect {expected_batch_count} files)
        2. Validate all {expected_batch_count} files exist before proceeding
        3. Read EVERY file completely (no skipping)
        4. Verify you read all {expected_batch_count} files
        5. ONLY THEN write aggregation summary

        Use nexus.validators.validate_aggregation_completeness() to validate:
        - After discovering files
        - After reading all files
        - Before writing summary

        Output: 01-memory/input/_analysis/analysis-summary.md
        """,
        description=f"Aggregating {expected_batch_count} batch insights"
    )
else:
    # Manual aggregation for ≤3 batches
    # ... use validation logic above
```

**Create master summary**: `01-memory/input/_analysis/analysis-summary.md`

```markdown
# Context Analysis Summary

> Analyzed {total_files} files in {batch_count} batches on {date}

## Overview

{2-3 sentence synthesis of what these files represent}

## Key Themes Discovered

Based on analysis across all files:

1. **{Theme 1}**: {description}
   - Found in: {list of relevant files}

2. **{Theme 2}**: {description}
   - Found in: {list of relevant files}

3. **{Theme 3}**: {description}
   - Found in: {list of relevant files}

## Tools & Services Mentioned

| Tool/Service | Frequency | Context |
|--------------|-----------|---------|
| {tool1} | {count} files | {how it's used} |
| {tool2} | {count} files | {how it's used} |

## BUILD Ideas (Prioritized)

1. **{BUILD idea}**
   - Rationale: {why}
   - Source: {which files suggested this}

2. **{BUILD idea}**
   - Rationale: {why}
   - Source: {which files suggested this}

3. **{BUILD idea}**
   - Rationale: {why}
   - Source: {which files suggested this}

## Workspace Structure Suggestion

Based on your files:
```
04-workspace/
├── {folder}/ - {why, based on file themes}
├── {folder}/ - {why}
└── {folder}/ - {why}
```

## Integration Opportunities

- **{tool}**: {how it could integrate with Nexus}

---

## Batch Reports

| Batch | Files | Report |
|-------|-------|--------|
| 1 | {count} | [batch-01-insights.md](batch-01-insights.md) |
| 2 | {count} | [batch-02-insights.md](batch-02-insights.md) |
| ... | ... | ... |

---

*Generated by analyze-context skill*
```

---

### Step 8: Display Results to User

```
Analysis complete!
----------------------------------------------------

Analyzed: {file_count} files in {batch_count} batches

Key themes discovered:
  - {theme 1}
  - {theme 2}
  - {theme 3}

BUILD ideas:
  - {idea 1}
  - {idea 2}

Tools found:
  - {tool 1}
  - {tool 2}

Saved to:
→ 01-memory/input/_analysis/analysis-summary.md (master)
→ 01-memory/input/_analysis/batch-{N}-insights.md (per batch)

These insights will inform your goals and workspace setup.
```

---

### Step 9: Add Roadmap Item for Context Processing

**AUTOMATIC**: When context is uploaded, add a roadmap item to process it properly.

**Check if roadmap.md exists**:
```python
from pathlib import Path

roadmap_path = Path("01-memory/roadmap.md")
```

**If roadmap exists, append item. If not, create with this item**:

```markdown
### Organize Initial Context

**Type**: Process
**Priority**: High
**Status**: Not Started
**Dependencies**: None

**Why This Matters**:
Your uploaded files ({file_count} files) are in a temporary holding area.
This build sorts them into your workspace where they become permanent,
organized context that informs all future work.

**What "Done" Looks Like**:
- Files moved from 01-memory/input/ to 04-workspace/{folders}/
- Key insights saved to 04-workspace/references/
- Workspace-map.md updated with new structure
- 01-memory/input/ cleared (ready for next upload)
```

**Display**:
```
Added to your roadmap:
→ "Organize Initial Context" (high priority)

Your uploaded files need to be sorted into your workspace.
This will be your first build - or you can do it after your current focus.
```

---

## Output Files (Temporary)

**All outputs are TEMPORARY until "Organize Initial Context" BUILD runs.**

```
01-memory/input/              # TEMPORARY - cleared after organization
├── {uploaded files}          # User's original files (any type/count)
└── _analysis/                # SubAgent outputs
    ├── analysis-summary.md   # Master summary (synthesized)
    ├── batch-01-insights.md  # Per-batch insights
    ├── batch-02-insights.md
    ├── batch-03-insights.md
    └── extracted/            # Raw text from PDFs/DOCX
        ├── document1.txt
        └── document2.txt
```

**Example with 20 files (mixed formats)**:
```
01-memory/input/
├── report.pdf              # 80 pages, large
├── notes.docx              # Word doc
├── chat-export-1.json      # ChatGPT export
├── chat-export-2.json
├── ... (20 files total)
└── _analysis/
    ├── extracted/                    # Pre-processed files
    │   ├── report_chunk01.txt        # Large PDF → 3 chunks
    │   ├── report_chunk02.txt
    │   ├── report_chunk03.txt
    │   └── notes.txt                 # DOCX → text
    ├── analysis-summary.md           # Synthesized from all batches
    ├── batch-01-insights.md          # Items 1-5
    ├── batch-02-insights.md          # Items 6-10
    ├── batch-03-insights.md          # Items 11-15
    ├── batch-04-insights.md          # Items 16-20
    └── batch-05-insights.md          # Items 21-22 (chunks count as items)
```

**Pre-processing expansion:**
- 20 uploaded files
- 1 large PDF → 3 chunks
- 1 DOCX → 1 txt
- = 22 processable items
- = 5 batches (4-5 items each)

**After "Organize Initial Context" BUILD**:
```
04-workspace/                 # PERMANENT - organized files
├── {folders by theme}/       # Files sorted based on content analysis
└── references/               # Key insights kept

01-memory/input/              # CLEARED
└── (empty, ready for next upload)
```

---

## Integration with Quick-Start

When called from quick-start Step 1:
- Insights inform Step 2 (goals)
- Workspace suggestions inform Step 3
- BUILD ideas inform Step 4

The AI should reference `01-memory/input/_analysis/analysis-summary.md` in subsequent steps.

---

## Standalone Usage

Can be called anytime:
```
"analyze context"
"upload files for analysis"
```

Will add new insights to existing context folder.

---

## Scaling Properties

**This architecture scales for any file count:**

| Uploaded | After Pre-Processing | Batches | Parallelism |
|----------|---------------------|---------|-------------|
| 1-5 | ~same | 1 | Single agent |
| 6-15 | may expand | 3 | 3 parallel agents |
| 16-30 | may expand | 5 | 5 parallel agents |
| 31-50 | may expand | 10 | 10 parallel agents (max) |
| 50+ | may expand | 10 | 10 agents, larger batches |

**Pre-processing can EXPAND file count:**
- 1 large PDF (100 pages) → 3-5 chunks
- 20 files uploaded → could become 30+ processable items
- This ensures NOTHING is too large for context

**Why batch-based > theme-based:**
- Theme detection from filename is unreliable
- A single file can contain multiple themes
- ChatGPT exports, meeting notes, etc. don't fit neat categories
- Batch-based ensures EVERY file gets analyzed
- Per-file insights in batch reports capture unique information

**Example scenarios:**

| Scenario | Pre-Processing | Batching |
|----------|----------------|----------|
| 30 ChatGPT chats (.json) | 30 items (no change) | 6 batches × 5 |
| 20 mixed PDFs | 25 items (some chunked) | 5 batches × 5 |
| 5 large reports + 10 notes | 15 items (reports chunked) | 3 batches × 5 |
| 1 massive PDF (200 pages) | 8 chunks | 2 batches × 4 |

---

## Error Handling

| Issue | Solution |
|-------|----------|
| No files uploaded | Prompt user to upload |
| pdfplumber not installed | `pip install pdfplumber` |
| python-docx not installed | `pip install python-docx` |
| PDF extraction fails | Log error, skip file, continue |
| DOCX extraction fails | Log error, skip file, continue |
| Password-protected PDF | Skip with warning |
| Scanned PDF (no text) | Skip with warning (OCR not supported) |
| SubAgent timeout | Retry that specific batch |
| File too large (>200 pages) | Chunked automatically (no limit) |
| Too many files (100+) | Warn user, still process in 10 batches |
| Batch agent fails | Other batches still complete, report partial results |
| Encoding error | Use `errors='ignore'`, log warning |

---

*Standalone skill - can be used during onboarding or anytime later*
