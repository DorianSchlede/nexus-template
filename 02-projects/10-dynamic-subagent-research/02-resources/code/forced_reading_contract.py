#!/usr/bin/env python3
"""Forced Reading Contract Generator.

Generates prompts that FORCE subagents to prove they read EVERYTHING.
Uses multiple verification mechanisms to prevent skimming.

KEY INSIGHT: LLMs tend to skim unless you:
1. Require proof of reading (3-point evidence)
2. Ask questions that require FULL content
3. Validate outputs against source
4. Make partial reading detectable

HIGH QUALITY DATA TRANSFER = FORCED COMPLETE READING
"""

import hashlib
import random
from pathlib import Path
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
import yaml
import re


# =============================================================================
# FORCED READING MECHANISMS
# =============================================================================

@dataclass
class ReadingProof:
    """Proof that a chunk was fully read."""
    chunk_id: str
    start_text: str      # First 100 chars after header
    mid_text: str        # 100 chars from 50% position
    end_text: str        # Last 100 chars
    content_hash: str    # SHA256 of full content
    line_count: int      # Total lines
    word_count: int      # Total words

    # Verification questions (must answer correctly)
    verification_questions: List[Dict[str, str]]


def generate_verification_questions(content: str, chunk_id: str) -> List[Dict[str, str]]:
    """Generate questions that REQUIRE reading the full chunk.

    Strategy: Ask about specific details from different parts of the chunk.
    Wrong answers = didn't read properly.
    """
    lines = content.split('\n')
    questions = []

    # Question from first third
    if len(lines) > 10:
        line_num = len(lines) // 5
        line_content = lines[line_num].strip()
        if len(line_content) > 20:
            questions.append({
                "location": "early",
                "line": line_num + 1,
                "question": f"What is on line {line_num + 1} of {chunk_id}?",
                "answer_contains": line_content[:50] if len(line_content) > 50 else line_content
            })

    # Question from middle
    if len(lines) > 20:
        line_num = len(lines) // 2
        line_content = lines[line_num].strip()
        if len(line_content) > 20:
            questions.append({
                "location": "middle",
                "line": line_num + 1,
                "question": f"What is on line {line_num + 1} of {chunk_id}?",
                "answer_contains": line_content[:50] if len(line_content) > 50 else line_content
            })

    # Question from last third
    if len(lines) > 30:
        line_num = len(lines) * 4 // 5
        line_content = lines[line_num].strip()
        if len(line_content) > 20:
            questions.append({
                "location": "late",
                "line": line_num + 1,
                "question": f"What is on line {line_num + 1} of {chunk_id}?",
                "answer_contains": line_content[:50] if len(line_content) > 50 else line_content
            })

    return questions


def extract_reading_proof(file_path: Path) -> ReadingProof:
    """Extract proof data from a file that subagent must reproduce."""
    content = file_path.read_text(encoding='utf-8')

    # Skip YAML frontmatter and header line
    if content.startswith('---'):
        end = content.find('---', 3)
        if end > 0:
            content = content[end + 3:].strip()

    # Skip first header line
    if content.startswith('#'):
        first_newline = content.find('\n')
        if first_newline > 0:
            content = content[first_newline + 1:].strip()

    lines = content.split('\n')
    words = content.split()

    # 3-point evidence
    start_text = content[:100].strip() if len(content) > 100 else content.strip()

    mid_pos = len(content) // 2
    mid_text = content[mid_pos:mid_pos + 100].strip() if len(content) > mid_pos + 100 else ""

    end_text = content[-100:].strip() if len(content) > 100 else content.strip()

    # Hash
    content_hash = hashlib.sha256(content.encode()).hexdigest()

    # Verification questions
    chunk_id = file_path.stem
    questions = generate_verification_questions(content, chunk_id)

    return ReadingProof(
        chunk_id=chunk_id,
        start_text=start_text,
        mid_text=mid_text,
        end_text=end_text,
        content_hash=content_hash,
        line_count=len(lines),
        word_count=len(words),
        verification_questions=questions
    )


# =============================================================================
# FORCED READING CONTRACT
# =============================================================================

def generate_forced_reading_contract(
    chunks: List[Path],
    task_type: str
) -> str:
    """Generate contract that FORCES complete reading.

    Mechanisms used:
    1. 3-point evidence requirement (start/mid/end)
    2. Hash verification
    3. Line-specific questions
    4. Word/line count verification
    5. Random spot checks
    """

    lines = [
        "## FORCED READING CONTRACT",
        "",
        "**Du MUSST beweisen, dass du JEDEN Chunk VOLLSTÄNDIG gelesen hast.**",
        "",
        "### Warum?",
        "- Oberflächliches Lesen führt zu falschen Extraktionen",
        "- Verpasste Details = verpasste Erkenntnisse",
        "- Dein Output wird VERIFIZIERT gegen die Quelldateien",
        "- Unvollständiges Lesen = ABLEHNUNG des Outputs",
        "",
        "### Proof-of-Reading Requirements",
        "",
        "Für JEDEN Chunk musst du in `_analysis_log.md` dokumentieren:",
        "",
        "```yaml",
        "chunk_evidence:",
        "  {chunk_id}:",
        "    # REQUIRED: 3-Point Evidence",
        "    start: \"{first 100 chars AFTER header}\"",
        "    mid: \"{100 chars from 50% position}\"",
        "    end: \"{last 100 chars}\"",
        "    ",
        "    # REQUIRED: Content Verification",
        "    hash: \"{SHA256 of full chunk content}\"",
        "    line_count: {N}",
        "    word_count: {N}",
        "    ",
        "    # REQUIRED: Spot Check Answers",
        "    spot_checks:",
        "      - line: {N}",
        "        content: \"{exact text on that line}\"",
        "```",
        "",
        "### Spot Check Questions",
        "",
        "Du MUSST diese Fragen korrekt beantworten (falsche Antwort = Ablehnung):",
        ""
    ]

    # Add chunk-specific requirements
    for chunk_path in chunks:
        if chunk_path.exists():
            proof = extract_reading_proof(chunk_path)

            lines.append(f"#### {proof.chunk_id}")
            lines.append("")
            lines.append(f"- **Erwartete Zeilenzahl**: {proof.line_count}")
            lines.append(f"- **Erwartete Wortzahl**: ~{proof.word_count}")
            lines.append(f"- **Hash-Prefix**: `{proof.content_hash[:16]}...`")
            lines.append("")

            if proof.verification_questions:
                lines.append("**Spot Check Fragen:**")
                for q in proof.verification_questions:
                    lines.append(f"- Zeile {q['line']}: Was steht dort?")
                lines.append("")

    lines.extend([
        "### Konsequenzen bei Nicht-Erfüllung",
        "",
        "| Verstoß | Konsequenz |",
        "|---------|------------|",
        "| 3-Point Evidence fehlt | Output ABGELEHNT |",
        "| Hash stimmt nicht | Output ABGELEHNT |",
        "| Spot Check falsch | Output ABGELEHNT |",
        "| Zeilenzahl falsch (>10% Abweichung) | Output MARKIERT |",
        "",
        "**KEINE AUSNAHMEN. KEIN ÜBERFLIEGEN. ALLES LESEN.**"
    ])

    return "\n".join(lines)


# =============================================================================
# ANTI-SKIMMING PROMPT SECTIONS
# =============================================================================

def generate_anti_skimming_prompt() -> str:
    """Generate prompt section that prevents skimming behavior."""

    return """## ANTI-SKIMMING PROTOKOLL

### Das Problem
LLMs neigen dazu zu überfliegen statt gründlich zu lesen. Das führt zu:
- Verpassten wichtigen Details
- Falschen oder unvollständigen Extraktionen
- Halluzinierten Informationen

### Die Lösung: Erzwungenes gründliches Lesen

**BEFORE reading each chunk:**
1. Note the total line count
2. Plan to process in sections (lines 1-100, 101-200, etc.)

**WHILE reading each chunk:**
1. Process sequentially - DO NOT skip ahead
2. For EVERY section, note at least one specific detail
3. If you find yourself skimming - STOP and re-read

**AFTER reading each chunk:**
1. Record 3-point evidence (start/mid/end)
2. Compute hash
3. Answer spot check questions

### Reading Strategy by Chunk Size

| Chunk Size | Strategy |
|------------|----------|
| < 200 lines | Read completely in one pass |
| 200-500 lines | Break into 3 sections, process each |
| > 500 lines | Break into 5 sections, summarize each before extraction |

### Self-Check Questions

After reading, ask yourself:
- "Can I describe the ENDING of this chunk?"
- "What was discussed in the MIDDLE?"
- "Were there any unexpected details?"

If you can't answer → you skimmed → RE-READ.

### Extraction After Full Reading

**CRITICAL**: Do NOT extract while reading.
1. FIRST: Read entire chunk
2. SECOND: Record proof-of-reading
3. THIRD: Go back and extract with specific line references

This prevents the "extract and forget the rest" pattern.
"""


def generate_chunk_processing_instructions(chunk_count: int) -> str:
    """Generate specific instructions for processing chunks."""

    return f"""## CHUNK PROCESSING INSTRUCTIONS

You will process {chunk_count} chunks. Here is your EXACT workflow:

### Phase 1: Initial Survey (5% of time)
- List all {chunk_count} chunks by filename
- Note estimated size of each
- Identify any particularly large chunks

### Phase 2: Sequential Deep Reading (80% of time)

For EACH chunk, follow this EXACT sequence:

```
1. OPEN chunk file
   ↓
2. SCROLL to end - note total lines
   ↓
3. RETURN to start
   ↓
4. READ lines 1-100 carefully
   - Note: What topic/concept is introduced?
   ↓
5. READ lines 101-200 carefully
   - Note: How does it develop?
   ↓
6. CONTINUE in 100-line sections
   ↓
7. RECORD 3-point evidence:
   - start: copy first 100 chars
   - mid: go to 50%, copy 100 chars
   - end: copy last 100 chars
   ↓
8. COMPUTE hash (SHA256 of full content)
   ↓
9. ANSWER spot check questions
   ↓
10. MARK chunk as FULLY READ in log
```

### Phase 3: Extraction (15% of time)

ONLY after ALL chunks are fully read:
- Go back to each chunk
- Extract items with EXACT line references
- Cross-reference between chunks

### FORBIDDEN Actions

- ❌ Extracting while reading (extract AFTER full read)
- ❌ Skipping sections that "look similar"
- ❌ Using chunk summaries instead of full content
- ❌ Guessing line numbers
- ❌ Approximating quotes
"""


# =============================================================================
# INTEGRATION WITH FACTORY
# =============================================================================

def enhance_prompt_with_forced_reading(
    base_prompt: str,
    chunk_paths: List[Path]
) -> str:
    """Add forced reading contract to any base prompt."""

    sections = [
        base_prompt,
        "",
        "---",
        "",
        generate_anti_skimming_prompt(),
        "",
        generate_chunk_processing_instructions(len(chunk_paths)),
        "",
        generate_forced_reading_contract(chunk_paths, "paper_analysis")
    ]

    return "\n".join(sections)


def generate_reading_verification_checklist(chunks: List[Path]) -> str:
    """Generate a checklist the subagent must complete."""

    lines = [
        "## READING VERIFICATION CHECKLIST",
        "",
        "Complete this checklist IN ORDER. Do not proceed until each item is checked.",
        "",
        "```markdown",
        "# Reading Progress"
    ]

    for chunk_path in chunks:
        chunk_id = chunk_path.stem
        lines.append(f"")
        lines.append(f"## {chunk_id}")
        lines.append(f"- [ ] Opened file and noted total lines: ___")
        lines.append(f"- [ ] Read lines 1-100")
        lines.append(f"- [ ] Read lines 101-200")
        lines.append(f"- [ ] Read remaining lines")
        lines.append(f"- [ ] Recorded start evidence (100 chars): ___")
        lines.append(f"- [ ] Recorded mid evidence (100 chars): ___")
        lines.append(f"- [ ] Recorded end evidence (100 chars): ___")
        lines.append(f"- [ ] Computed hash: ___")
        lines.append(f"- [ ] Answered spot checks: ___")

    lines.extend([
        "```",
        "",
        "**Transfer this checklist to your `_analysis_log.md` file with all values filled.**"
    ])

    return "\n".join(lines)


# =============================================================================
# VALIDATION SCRIPT
# =============================================================================

def validate_reading_proof(
    analysis_log: Dict,
    chunk_paths: List[Path]
) -> Tuple[bool, List[str]]:
    """Validate that subagent actually read everything.

    Returns (passed, errors).
    """
    errors = []

    chunk_evidence = analysis_log.get('chunk_evidence', {})

    for chunk_path in chunk_paths:
        chunk_id = chunk_path.stem

        if chunk_id not in chunk_evidence:
            errors.append(f"Missing evidence for {chunk_id}")
            continue

        evidence = chunk_evidence[chunk_id]
        actual_proof = extract_reading_proof(chunk_path)

        # Check start text
        if evidence.get('start', '')[:50] != actual_proof.start_text[:50]:
            errors.append(f"{chunk_id}: Start evidence mismatch")

        # Check end text
        if evidence.get('end', '')[-50:] != actual_proof.end_text[-50:]:
            errors.append(f"{chunk_id}: End evidence mismatch")

        # Check hash
        if evidence.get('hash', '')[:16] != actual_proof.content_hash[:16]:
            errors.append(f"{chunk_id}: Hash mismatch - possible incomplete reading")

        # Check line count (allow 10% tolerance for header variations)
        reported_lines = evidence.get('line_count', 0)
        if abs(reported_lines - actual_proof.line_count) > actual_proof.line_count * 0.1:
            errors.append(f"{chunk_id}: Line count mismatch ({reported_lines} vs {actual_proof.line_count})")

        # Check spot checks
        for q in actual_proof.verification_questions:
            spot_checks = evidence.get('spot_checks', [])
            found = False
            for sc in spot_checks:
                if sc.get('line') == q['line']:
                    if q['answer_contains'] in sc.get('content', ''):
                        found = True
                    else:
                        errors.append(f"{chunk_id}: Spot check line {q['line']} incorrect")
            if not found and spot_checks:
                errors.append(f"{chunk_id}: Missing spot check for line {q['line']}")

    return len(errors) == 0, errors


# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python forced_reading_contract.py <chunk_dir>")
        print("  Generates forced reading contract for chunks in directory")
        sys.exit(1)

    chunk_dir = Path(sys.argv[1])
    chunk_paths = sorted(chunk_dir.glob("*_*.md"))

    if not chunk_paths:
        print(f"No chunk files found in {chunk_dir}")
        sys.exit(1)

    print(f"Found {len(chunk_paths)} chunks")
    print()
    print(generate_forced_reading_contract(chunk_paths, "paper_analysis"))
