#!/usr/bin/env python3
"""
PDF to Markdown Converter for LLM Consumption

Converts PDFs to clean markdown with:
- Preserved headings and table structure
- Auto-chunking to max N lines per file
- One folder per source PDF with all chunks inside

Uses pymupdf4llm for best speed/quality balance.

Usage:
    python pdf_to_markdown.py input.pdf
    python pdf_to_markdown.py ./papers/ --batch
    python pdf_to_markdown.py input.pdf --max-lines 500
    python pdf_to_markdown.py input.pdf --overlap 100
"""

import argparse
import json
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

try:
    import pymupdf4llm
except ImportError:
    print("ERROR: pymupdf4llm not installed. Run: pip install pymupdf4llm")
    sys.exit(1)


DEFAULT_MAX_LINES = 1000
DEFAULT_OVERLAP_LINES = 100


def sanitize_filename(name: str) -> str:
    """Create safe filename from PDF name."""
    # Remove extension
    name = Path(name).stem
    # Replace problematic chars
    name = re.sub(r'[<>:"/\\|?*]', '_', name)
    # Collapse multiple underscores/spaces
    name = re.sub(r'[\s_]+', '_', name)
    # Trim length
    return name[:100].strip('_')


def extract_markdown(pdf_path: Path) -> str:
    """Extract markdown from PDF using pymupdf4llm."""
    md_text = pymupdf4llm.to_markdown(str(pdf_path))
    return md_text


def chunk_by_lines(text: str, max_lines: int, overlap_lines: int = 0) -> list[str]:
    """
    Split text into chunks of max_lines each with overlap.
    Splits at paragraph boundaries (double newlines) when possible.
    Overlap repeats the last N lines from previous chunk at start of next.
    """
    lines = text.split('\n')

    if len(lines) <= max_lines:
        return [text]

    chunks = []
    current_start = 0
    prev_end = 0

    while current_start < len(lines):
        # Determine end of this chunk
        current_end = min(current_start + max_lines, len(lines))

        # Try to find a good break point (empty line = paragraph boundary)
        # Look backwards within last 20% of chunk
        if current_end < len(lines):
            lookback_start = current_start + int(max_lines * 0.8)
            break_point = None

            for i in range(current_end - 1, lookback_start, -1):
                if lines[i].strip() == '':
                    break_point = i + 1  # Include the empty line
                    break

            if break_point:
                current_end = break_point

        # Extract chunk
        chunk_lines = lines[current_start:current_end]
        chunk_text = '\n'.join(chunk_lines)
        chunks.append(chunk_text)

        # Store where this chunk ended
        prev_end = current_end

        # Move start for next chunk
        # Effective content moves forward by (chunk_size - overlap)
        next_start = current_end - overlap_lines

        # Ensure we always make forward progress
        if next_start <= current_start:
            next_start = current_end

        # If we've covered everything, break
        if current_end >= len(lines):
            break

        current_start = next_start

    return chunks


def process_pdf(pdf_path: Path, max_lines: int = DEFAULT_MAX_LINES, overlap_lines: int = DEFAULT_OVERLAP_LINES) -> dict:
    """
    Process a single PDF:
    1. Create folder with PDF name (if not already in one)
    2. Move PDF into folder
    3. Extract markdown and chunk with overlap
    4. Save chunks as {name}_1.md, {name}_2.md, etc.
    5. Create _metadata.json

    Returns metadata dict.
    """
    safe_name = sanitize_filename(pdf_path.name)
    parent_dir = pdf_path.parent

    # Check if PDF is already in its own folder
    if parent_dir.name == safe_name:
        # Already in correct folder, use it
        pdf_folder = parent_dir
        new_pdf_path = pdf_path
    else:
        # Create folder for this PDF
        pdf_folder = parent_dir / safe_name
        pdf_folder.mkdir(exist_ok=True)

        # Move PDF into folder
        new_pdf_path = pdf_folder / pdf_path.name
        if not new_pdf_path.exists():
            shutil.move(str(pdf_path), str(new_pdf_path))

    # Extract markdown
    print(f"  Extracting markdown...")
    md_text = extract_markdown(new_pdf_path)

    # Chunk the markdown with overlap
    chunks = chunk_by_lines(md_text, max_lines, overlap_lines)
    print(f"  Created {len(chunks)} chunk(s) (overlap: {overlap_lines} lines)")

    # Save chunks
    chunk_files = []
    for i, chunk in enumerate(chunks, 1):
        chunk_filename = f"{safe_name}_{i}.md"
        chunk_path = pdf_folder / chunk_filename

        # Add header to chunk
        header = f"<!-- Source: {pdf_path.name} | Chunk {i}/{len(chunks)} -->\n\n"

        with open(chunk_path, 'w', encoding='utf-8') as f:
            f.write(header + chunk)

        chunk_files.append({
            "filename": chunk_filename,
            "chunk_number": i,
            "line_count": len(chunk.split('\n')),
            "char_count": len(chunk)
        })

    # Create metadata
    metadata = {
        "source_pdf": pdf_path.name,
        "processed_at": datetime.now().isoformat(),
        "max_lines_per_chunk": max_lines,
        "overlap_lines": overlap_lines,
        "total_chunks": len(chunks),
        "total_lines": sum(c["line_count"] for c in chunk_files),
        "total_chars": sum(c["char_count"] for c in chunk_files),
        "chunks": chunk_files
    }

    # Save metadata
    metadata_path = pdf_folder / "_metadata.json"
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    return metadata


def process_folder(folder_path: Path, max_lines: int = DEFAULT_MAX_LINES, overlap_lines: int = DEFAULT_OVERLAP_LINES, recursive: bool = False) -> list[dict]:
    """Process all PDFs in a folder."""
    pattern = "**/*.pdf" if recursive else "*.pdf"
    pdf_files = list(folder_path.glob(pattern))

    # Filter out PDFs that are already inside their own folder
    pdf_files = [p for p in pdf_files if p.parent.name != sanitize_filename(p.name)]

    if not pdf_files:
        print(f"No PDFs found in {folder_path}")
        return []

    print(f"Found {len(pdf_files)} PDF(s) to process")

    results = []
    for i, pdf_path in enumerate(pdf_files, 1):
        print(f"\n[{i}/{len(pdf_files)}] Processing: {pdf_path.name}")
        try:
            metadata = process_pdf(pdf_path, max_lines, overlap_lines)
            results.append(metadata)
            print(f"  Done: {metadata['total_chunks']} chunks, {metadata['total_chars']:,} chars")
        except Exception as e:
            print(f"  ERROR: {e}")
            results.append({"source_pdf": pdf_path.name, "error": str(e)})

    # Save batch summary
    summary_path = folder_path / "_batch_summary.json"
    summary = {
        "processed_at": datetime.now().isoformat(),
        "total_pdfs": len(pdf_files),
        "successful": len([r for r in results if "error" not in r]),
        "failed": len([r for r in results if "error" in r]),
        "max_lines_per_chunk": max_lines,
        "overlap_lines": overlap_lines,
        "results": results
    }
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(f"\nBatch summary saved to: {summary_path}")
    return results


def main():
    parser = argparse.ArgumentParser(
        description="Convert PDFs to markdown chunks for LLM consumption"
    )
    parser.add_argument(
        "input",
        help="PDF file or folder path"
    )
    parser.add_argument(
        "--batch", "-b",
        action="store_true",
        help="Process all PDFs in folder"
    )
    parser.add_argument(
        "--recursive", "-r",
        action="store_true",
        help="Process subfolders recursively (with --batch)"
    )
    parser.add_argument(
        "--max-lines", "-m",
        type=int,
        default=DEFAULT_MAX_LINES,
        help=f"Maximum lines per chunk (default: {DEFAULT_MAX_LINES})"
    )
    parser.add_argument(
        "--overlap", "-o",
        type=int,
        default=DEFAULT_OVERLAP_LINES,
        help=f"Overlap lines between chunks (default: {DEFAULT_OVERLAP_LINES})"
    )

    args = parser.parse_args()
    input_path = Path(args.input).resolve()

    if not input_path.exists():
        print(f"ERROR: Path not found: {input_path}")
        sys.exit(1)

    print(f"PDF to Markdown Converter")
    print(f"Max lines per chunk: {args.max_lines} | Overlap: {args.overlap} lines")
    print("=" * 50)

    if args.batch or input_path.is_dir():
        if not input_path.is_dir():
            print(f"ERROR: --batch requires a folder path")
            sys.exit(1)
        results = process_folder(input_path, args.max_lines, args.overlap, args.recursive)
        print(f"\nProcessed {len(results)} PDF(s)")
    else:
        if not input_path.suffix.lower() == '.pdf':
            print(f"ERROR: Not a PDF file: {input_path}")
            sys.exit(1)
        metadata = process_pdf(input_path, args.max_lines, args.overlap)
        print(f"\nDone: {metadata['total_chunks']} chunks saved to {input_path.parent / sanitize_filename(input_path.name)}")


if __name__ == "__main__":
    main()
