---
name: pdf-preprocess
description: Convert PDFs to clean markdown for LLM consumption. Load when user says "preprocess pdf", "convert pdf to markdown", "chunk pdf", or wants to prepare academic papers for analysis. Preserves headings and tables, auto-chunks to max 1000 lines.
---

# PDF Preprocess

Convert PDF documents to structured markdown optimized for LLM consumption.

## Quick Start

```bash
# Single PDF
python 03-skills/research-pipeline/skills/pdf-preprocess/scripts/pdf_to_markdown.py "paper.pdf"

# All PDFs in folder
python 03-skills/research-pipeline/skills/pdf-preprocess/scripts/pdf_to_markdown.py "./papers/" --batch

# Recursive (subfolders)
python 03-skills/research-pipeline/skills/pdf-preprocess/scripts/pdf_to_markdown.py "./papers/" --batch --recursive

# Custom chunk size and overlap
python 03-skills/research-pipeline/skills/pdf-preprocess/scripts/pdf_to_markdown.py "paper.pdf" --max-lines 500 --overlap 50
```

## What It Does

1. Creates a folder per PDF (named after the PDF)
2. Moves the PDF into its folder
3. Extracts markdown with preserved headings and tables
4. Chunks into max 1000 lines per file with 100 line overlap (splits at paragraph boundaries)
5. Saves as `{name}_1.md`, `{name}_2.md`, etc.
6. Generates `_metadata.json` with chunk info

## Defaults

- `--max-lines` / `-m`: 1000 lines per chunk
- `--overlap` / `-o`: 100 lines overlap between chunks

## Output Structure

```
papers/
└── TA_LLM/
    └── Braun_Clarke_2006/           # Folder per PDF
        ├── Braun_Clarke_2006.pdf    # Original (moved here)
        ├── Braun_Clarke_2006_1.md   # Chunk 1
        ├── Braun_Clarke_2006_2.md   # Chunk 2
        └── _metadata.json           # Index
```

## Requirements

```bash
pip install pymupdf4llm
```

## Notes

- Uses `pymupdf4llm` for fast, high-quality extraction
- Tables convert to GitHub-flavored markdown
- Headings detected by font size hierarchy
- Chunks split at paragraph boundaries when possible
- Batch mode creates `_batch_summary.json` in folder
