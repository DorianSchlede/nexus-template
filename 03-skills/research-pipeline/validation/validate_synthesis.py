#!/usr/bin/env python3
"""
Synthesis Validation Script

Validates that _synthesis.md:
1. Has required frontmatter fields
2. Lists papers that actually exist
3. Claims can be traced to source index.md files
4. Coverage metrics are accurate

Usage:
    python validate_synthesis.py <project_path> [--spot-check N]

Example:
    python validate_synthesis.py 02-projects/10-multi-agent-algorithms-research --spot-check 10
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
import yaml


@dataclass
class ValidationResult:
    """Results of synthesis validation"""
    passed: bool = True
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    stats: Dict = field(default_factory=dict)
    spot_checks: List[Dict] = field(default_factory=list)


def parse_yaml_frontmatter(content: str) -> Optional[Dict]:
    """Extract YAML frontmatter from markdown content"""
    if not content.startswith('---'):
        return None

    # Find the closing ---
    end_match = re.search(r'\n---\n', content[3:])
    if not end_match:
        return None

    yaml_content = content[3:end_match.start() + 3]
    try:
        return yaml.safe_load(yaml_content)
    except yaml.YAMLError:
        return None


def extract_paper_citations(content: str) -> List[str]:
    """Extract paper IDs mentioned in synthesis"""
    # Match patterns like "01-autogen", "42-maporl", "28-budget-control-multi-agent"
    # Must start with 2 digits, dash, then letters/numbers/dashes
    # Greedy match to capture full folder names
    pattern = r'\b(\d{2}-[a-z][a-z0-9]+(?:-[a-z][a-z0-9]+)*)\b'
    candidates = list(set(re.findall(pattern, content.lower())))

    # Filter out false positives (numeric ranges like "50-70", "91-92")
    valid_papers = []
    for c in candidates:
        # Check it's not just numbers after the dash
        after_dash = c.split('-', 1)[1] if '-' in c else ''
        if after_dash and not after_dash.replace('-', '').isdigit():
            valid_papers.append(c)

    return valid_papers


def extract_claims_with_sources(content: str) -> List[Dict]:
    """Extract claims that cite specific papers"""
    claims = []

    # Known paper name patterns to look for
    paper_names = [
        'AutoGen', 'MAPoRL', 'MedAide', 'PDL', 'LangGraph', 'CrewAI',
        'SwarmBench', 'IoA', 'SoNS', 'LLMCompiler', 'RECONCILE',
        'Graph of Thoughts', 'Budget Control', 'Principle Prompting',
        'A2A', 'MCP', 'Internet of Agents', 'Resilient P-t-E'
    ]

    lines = content.split('\n')

    for i, line in enumerate(lines):
        # Skip empty lines and headers
        if not line.strip() or line.startswith('#'):
            continue

        # Look for metrics with paper citations
        # Match: "X% ... (Paper)" or "(Paper): X%"
        for paper in paper_names:
            if paper.lower() in line.lower():
                # Find metrics in the same line
                metrics = re.findall(r'(\d+(?:\.\d+)?%|\d+(?:\.\d+)?x)', line)
                if metrics:
                    claims.append({
                        'line': i + 1,
                        'text': line.strip()[:100],
                        'claim': metrics[0],
                        'source': paper
                    })
                    break  # One claim per line

    return claims


def validate_frontmatter(frontmatter: Dict, validation: ValidationResult) -> None:
    """Validate synthesis frontmatter has required fields"""

    required_fields = [
        'synthesized_at',
        'papers_included',
        'research_question'
    ]

    recommended_fields = [
        'papers_excluded',
        'papers_read',
        'total_patterns_extracted',
        'coverage_percentage'
    ]

    for field in required_fields:
        if field not in frontmatter:
            validation.errors.append(f"Missing required frontmatter field: {field}")
            validation.passed = False

    for field in recommended_fields:
        if field not in frontmatter:
            validation.warnings.append(f"Missing recommended frontmatter field: {field}")


def validate_paper_references(
    synthesis_content: str,
    papers_dir: Path,
    validation: ValidationResult
) -> None:
    """Validate that cited papers exist and have index.md"""

    cited_papers = extract_paper_citations(synthesis_content)
    existing_papers = []
    missing_papers = []

    for paper_id in cited_papers:
        paper_path = papers_dir / paper_id / 'index.md'
        if paper_path.exists():
            existing_papers.append(paper_id)
        else:
            missing_papers.append(paper_id)

    validation.stats['cited_papers'] = len(cited_papers)
    validation.stats['existing_papers'] = len(existing_papers)
    validation.stats['missing_papers'] = missing_papers

    if missing_papers:
        validation.warnings.append(
            f"Synthesis cites {len(missing_papers)} papers not found in collection: {missing_papers[:5]}..."
        )


def spot_check_claims(
    synthesis_content: str,
    papers_dir: Path,
    num_checks: int,
    validation: ValidationResult
) -> None:
    """Spot-check random claims against source papers"""

    # Map paper names to paper IDs for lookup
    name_to_id = {
        'autogen': '01-autogen',
        'maporl': '42-maporl',
        'medaide': '30-medaide',
        'pdl': '22-pdl-prompting',
        'langgraph': '24-langgraph-translation',
        'swarmbench': '41-benchmarking-swarm-intelligence',
        'ioa': '40-internet-of-agents',
        'internet of agents': '40-internet-of-agents',
        'sons': '45-self-organizing-swarm',
        'graph of thoughts': '19-graph-of-thoughts',
        'budget control': '28-budget-control-multi-agent',
        'principle prompting': '21-principle-prompting',
        'resilient p-t-e': '31-resilient-llm-agents',
        'a2a': '39-agent-protocols-survey',
    }

    claims = extract_claims_with_sources(synthesis_content)

    if not claims:
        validation.warnings.append("No verifiable claims found in synthesis")
        return

    # Take first N claims (or all if fewer)
    claims_to_check = claims[:min(num_checks, len(claims))]

    verified = 0
    failed = 0

    for claim in claims_to_check:
        # Try to find source paper using name mapping
        source_lower = claim['source'].lower()
        paper_id = name_to_id.get(source_lower)

        check_result = {
            'claim': claim['claim'][:50],
            'source': claim['source'],
            'line': claim['line'],
            'verified': False,
            'reason': 'Source paper not found'
        }

        if paper_id:
            index_path = papers_dir / paper_id / 'index.md'
        else:
            # Try partial match on directory name
            matching = [d for d in papers_dir.iterdir()
                       if d.is_dir() and source_lower.replace(' ', '-') in d.name.lower()]
            index_path = matching[0] / 'index.md' if matching else None

        if index_path and index_path.exists():
            try:
                index_content = index_path.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                try:
                    index_content = index_path.read_text(encoding='cp1252')
                except Exception:
                    index_content = ''

            # Check if claim value appears in source
            claim_value = re.search(r'(\d+(?:\.\d+)?)', claim['claim'])
            if claim_value:
                if claim_value.group(1) in index_content:
                    check_result['verified'] = True
                    check_result['reason'] = 'Value found in source'
                    verified += 1
                else:
                    check_result['reason'] = 'Value not found in source index.md'
                    failed += 1
        else:
            failed += 1

        validation.spot_checks.append(check_result)

    validation.stats['spot_checks_total'] = len(claims_to_check)
    validation.stats['spot_checks_verified'] = verified
    validation.stats['spot_checks_failed'] = failed

    if len(claims_to_check) > 0 and failed > len(claims_to_check) * 0.3:  # >30% failure rate
        validation.errors.append(
            f"High spot-check failure rate: {failed}/{len(claims_to_check)} claims could not be verified"
        )
        validation.passed = False


def calculate_coverage(
    synthesis_content: str,
    papers_dir: Path,
    validation: ValidationResult
) -> None:
    """Calculate how many source patterns made it into synthesis"""

    total_patterns = 0
    papers_with_patterns = 0

    for paper_dir in papers_dir.iterdir():
        if not paper_dir.is_dir():
            continue

        index_path = paper_dir / 'index.md'
        if not index_path.exists():
            continue

        try:
            content = index_path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            # Try with Windows encoding
            try:
                content = index_path.read_text(encoding='cp1252')
            except Exception:
                continue
        frontmatter = parse_yaml_frontmatter(content)

        if frontmatter:
            high_priority = frontmatter.get('high_priority_fields_found', 0)
            if high_priority > 0:
                total_patterns += high_priority
                papers_with_patterns += 1

    # Count patterns in synthesis (rough estimate from section headers)
    synthesis_patterns = len(re.findall(r'^###\s+\d+\.\d+', synthesis_content, re.MULTILINE))

    validation.stats['source_patterns_total'] = total_patterns
    validation.stats['source_papers_with_patterns'] = papers_with_patterns
    validation.stats['synthesis_patterns_count'] = synthesis_patterns

    if total_patterns > 0:
        coverage = min(synthesis_patterns / total_patterns, 1.0)
        validation.stats['estimated_coverage'] = f"{coverage:.1%}"


def generate_report(validation: ValidationResult, output_path: Optional[Path] = None) -> str:
    """Generate validation report"""

    report = []
    report.append("# Synthesis Validation Report\n")
    report.append(f"**Status**: {'PASSED' if validation.passed else 'FAILED'}\n")

    # Errors
    if validation.errors:
        report.append("\n## Errors\n")
        for error in validation.errors:
            report.append(f"- ❌ {error}\n")

    # Warnings
    if validation.warnings:
        report.append("\n## Warnings\n")
        for warning in validation.warnings:
            report.append(f"- ⚠️ {warning}\n")

    # Stats
    report.append("\n## Statistics\n")
    report.append("| Metric | Value |\n")
    report.append("|--------|-------|\n")
    for key, value in validation.stats.items():
        report.append(f"| {key.replace('_', ' ').title()} | {value} |\n")

    # Spot checks
    if validation.spot_checks:
        report.append("\n## Spot Check Results\n")
        report.append("| Claim | Source | Verified | Reason |\n")
        report.append("|-------|--------|----------|--------|\n")
        for check in validation.spot_checks:
            status = "✅" if check['verified'] else "❌"
            report.append(f"| {check['claim']} | {check['source']} | {status} | {check['reason']} |\n")

    report_text = ''.join(report)

    if output_path:
        output_path.write_text(report_text, encoding='utf-8')

    return report_text


def validate_synthesis(
    project_path: Path,
    spot_check_count: int = 10
) -> ValidationResult:
    """Main validation function"""

    validation = ValidationResult()

    # Find synthesis file
    synthesis_path = project_path / '04-outputs' / '_synthesis.md'
    if not synthesis_path.exists():
        validation.errors.append(f"Synthesis file not found: {synthesis_path}")
        validation.passed = False
        return validation

    # Find papers directory
    papers_dir = project_path / '02-resources' / 'papers'
    if not papers_dir.exists():
        validation.errors.append(f"Papers directory not found: {papers_dir}")
        validation.passed = False
        return validation

    # Read synthesis
    synthesis_content = synthesis_path.read_text(encoding='utf-8')

    # Parse frontmatter
    frontmatter = parse_yaml_frontmatter(synthesis_content)
    if frontmatter:
        validate_frontmatter(frontmatter, validation)
    else:
        validation.warnings.append("No YAML frontmatter found in synthesis")

    # Validate paper references
    validate_paper_references(synthesis_content, papers_dir, validation)

    # Spot check claims
    spot_check_claims(synthesis_content, papers_dir, spot_check_count, validation)

    # Calculate coverage
    calculate_coverage(synthesis_content, papers_dir, validation)

    return validation


def main():
    # Fix Windows console encoding
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    parser = argparse.ArgumentParser(description='Validate synthesis document')
    parser.add_argument('project_path', help='Path to research project')
    parser.add_argument('--spot-check', type=int, default=10, help='Number of claims to spot-check')
    parser.add_argument('--output', help='Output report path')

    args = parser.parse_args()

    project_path = Path(args.project_path)
    if not project_path.exists():
        print(f"Error: Project path does not exist: {project_path}")
        sys.exit(1)

    validation = validate_synthesis(project_path, args.spot_check)

    output_path = Path(args.output) if args.output else None
    report = generate_report(validation, output_path)

    print(report)

    sys.exit(0 if validation.passed else 1)


if __name__ == '__main__':
    main()
