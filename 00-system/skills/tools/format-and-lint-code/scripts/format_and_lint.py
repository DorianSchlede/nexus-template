#!/usr/bin/env python3
"""
Format and Lint Code - Main Execution Script

Handles formatting and linting for multiple languages and tools.
Supports Python, JavaScript, TypeScript, Go, Rust, JSON, YAML, Markdown, Shell.
"""

import os
import json
import yaml
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict


@dataclass
class FileFinding:
    """Represents a formatting/linting issue found in a file."""
    file_path: str
    line_number: int
    column: int
    severity: str  # error, warning, info
    tool: str
    rule_code: str
    message: str
    suggested_fix: Optional[str] = None
    auto_fixable: bool = False


@dataclass
class ToolResult:
    """Results from running a single tool."""
    tool_name: str
    language: str
    success: bool
    findings: List[FileFinding]
    files_modified: int = 0
    errors_count: int = 0
    warnings_count: int = 0
    info_count: int = 0


class LanguageDetector:
    """Detects languages and available tools in build."""

    LANGUAGE_EXTENSIONS = {
        'python': ['.py'],
        'javascript': ['.js', '.jsx', '.mjs'],
        'typescript': ['.ts', '.tsx'],
        'go': ['.go'],
        'rust': ['.rs'],
        'json': ['.json'],
        'yaml': ['.yaml', '.yml'],
        'markdown': ['.md', '.markdown'],
        'shell': ['.sh', '.bash'],
    }

    TOOLS = {
        'python': {
            'formatters': ['black', 'autopep8'],
            'linters': ['flake8', 'pylint', 'pyright'],
            'import_sorters': ['isort'],
        },
        'javascript': {
            'formatters': ['prettier'],
            'linters': ['eslint'],
        },
        'typescript': {
            'formatters': ['prettier'],
            'linters': ['eslint'],
        },
        'go': {
            'formatters': ['gofmt'],
            'linters': ['golangci-lint'],
        },
        'rust': {
            'formatters': ['rustfmt'],
            'linters': ['clippy'],
        },
        'json': {
            'formatters': ['prettier'],
            'linters': ['jsonlint'],
        },
        'yaml': {
            'formatters': ['prettier'],
            'linters': ['yamllint'],
        },
        'markdown': {
            'formatters': ['prettier'],
            'linters': ['markdownlint'],
        },
        'shell': {
            'formatters': ['shfmt'],
            'linters': ['shellcheck'],
        },
    }

    def __init__(self, project_root: Path = None):
        self.project_root = project_root or Path.cwd()
        self.detected_languages = {}
        self.detected_files = defaultdict(list)

    def detect(self, file_patterns: List[str] = None, exclude_patterns: List[str] = None) -> Dict:
        """
        Detect languages and files in build.

        Args:
            file_patterns: List of glob patterns to include
            exclude_patterns: List of glob patterns to exclude

        Returns:
            Dict with detected languages and file counts
        """
        if file_patterns is None:
            file_patterns = ['**/*']
        if exclude_patterns is None:
            exclude_patterns = []

        for pattern in file_patterns:
            for file_path in self.project_root.glob(pattern):
                # Skip excluded patterns
                if any(file_path.match(exclude) for exclude in exclude_patterns):
                    continue

                # Skip non-files
                if not file_path.is_file():
                    continue

                # Match extension to language
                suffix = file_path.suffix.lower()
                for lang, extensions in self.LANGUAGE_EXTENSIONS.items():
                    if suffix in extensions:
                        self.detected_files[lang].append(file_path)
                        break

        # Create detection summary
        result = {}
        for lang, files in self.detected_files.items():
            result[lang] = {
                'count': len(files),
                'files': [str(f) for f in files[:5]],  # Show first 5
                'tools': self.TOOLS.get(lang, {})
            }

        return result

    def get_available_tools(self, language: str) -> Dict[str, List[str]]:
        """Get tools available for a language."""
        return self.TOOLS.get(language, {})


class ToolRunner:
    """Runs formatting and linting tools."""

    def __init__(self, project_root: Path = None):
        self.project_root = project_root or Path.cwd()

    def run_formatter(self, tool: str, files: List[Path]) -> ToolResult:
        """Run a formatter on files."""
        result = ToolResult(
            tool_name=tool,
            language=self._tool_to_language(tool),
            success=False,
            findings=[],
        )

        try:
            if tool == 'black':
                return self._run_black(files, result)
            elif tool == 'prettier':
                return self._run_prettier(files, result)
            elif tool == 'gofmt':
                return self._run_gofmt(files, result)
            elif tool == 'rustfmt':
                return self._run_rustfmt(files, result)
            elif tool == 'shfmt':
                return self._run_shfmt(files, result)
            else:
                result.success = False
                return result
        except Exception as e:
            print(f"Error running {tool}: {e}")
            result.success = False
            return result

    def run_linter(self, tool: str, files: List[Path]) -> ToolResult:
        """Run a linter on files."""
        result = ToolResult(
            tool_name=tool,
            language=self._tool_to_language(tool),
            success=False,
            findings=[],
        )

        try:
            if tool == 'flake8':
                return self._run_flake8(files, result)
            elif tool == 'eslint':
                return self._run_eslint(files, result)
            elif tool == 'pylint':
                return self._run_pylint(files, result)
            elif tool == 'yamllint':
                return self._run_yamllint(files, result)
            else:
                result.success = False
                return result
        except Exception as e:
            print(f"Error running {tool}: {e}")
            result.success = False
            return result

    def _run_black(self, files: List[Path], result: ToolResult) -> ToolResult:
        """Run black formatter."""
        try:
            cmd = ['black', '--line-length=100', '--diff'] + [str(f) for f in files]
            output = subprocess.run(cmd, capture_output=True, text=True)
            result.success = output.returncode == 0
            # In real implementation, parse diff output and apply changes
            return result
        except FileNotFoundError:
            print("⚠️  black not found. Install with: pip install black")
            return result

    def _run_prettier(self, files: List[Path], result: ToolResult) -> ToolResult:
        """Run prettier formatter."""
        try:
            cmd = ['prettier', '--write', '--print-width=100'] + [str(f) for f in files]
            output = subprocess.run(cmd, capture_output=True, text=True)
            result.success = output.returncode == 0
            return result
        except FileNotFoundError:
            print("⚠️  prettier not found. Install with: npm install -g prettier")
            return result

    def _run_gofmt(self, files: List[Path], result: ToolResult) -> ToolResult:
        """Run gofmt formatter."""
        try:
            cmd = ['gofmt', '-w'] + [str(f) for f in files]
            output = subprocess.run(cmd, capture_output=True, text=True)
            result.success = output.returncode == 0
            return result
        except FileNotFoundError:
            print("⚠️  gofmt not found. Install with: go install golang.org/x/tools/cmd/goimports@latest")
            return result

    def _run_rustfmt(self, files: List[Path], result: ToolResult) -> ToolResult:
        """Run rustfmt formatter."""
        try:
            cmd = ['rustfmt'] + [str(f) for f in files]
            output = subprocess.run(cmd, capture_output=True, text=True)
            result.success = output.returncode == 0
            return result
        except FileNotFoundError:
            print("⚠️  rustfmt not found. Install with: rustup component add rustfmt")
            return result

    def _run_shfmt(self, files: List[Path], result: ToolResult) -> ToolResult:
        """Run shfmt formatter."""
        try:
            cmd = ['shfmt', '-i=2', '-w'] + [str(f) for f in files]
            output = subprocess.run(cmd, capture_output=True, text=True)
            result.success = output.returncode == 0
            return result
        except FileNotFoundError:
            print("⚠️  shfmt not found. Install with: GO111MODULE=on go install mvdan.cc/sh/v3/cmd/shfmt@latest")
            return result

    def _run_flake8(self, files: List[Path], result: ToolResult) -> ToolResult:
        """Run flake8 linter."""
        try:
            cmd = ['flake8', '--format=json', '--max-line-length=100'] + [str(f) for f in files]
            output = subprocess.run(cmd, capture_output=True, text=True)

            if output.stdout:
                findings = json.loads(output.stdout)
                for finding in findings:
                    result.findings.append(FileFinding(
                        file_path=finding.get('filename', ''),
                        line_number=finding.get('line_number', 0),
                        column=finding.get('column_number', 0),
                        severity='error' if finding.get('type') == 'E' else 'warning',
                        tool='flake8',
                        rule_code=finding.get('code', ''),
                        message=finding.get('text', ''),
                    ))
                    result.warnings_count += 1

            result.success = True
            return result
        except FileNotFoundError:
            print("⚠️  flake8 not found. Install with: pip install flake8")
            return result

    def _run_eslint(self, files: List[Path], result: ToolResult) -> ToolResult:
        """Run eslint linter."""
        try:
            cmd = ['eslint', '--format=json'] + [str(f) for f in files]
            output = subprocess.run(cmd, capture_output=True, text=True)

            if output.stdout:
                findings_list = json.loads(output.stdout)
                for file_findings in findings_list:
                    for finding in file_findings.get('messages', []):
                        result.findings.append(FileFinding(
                            file_path=file_findings.get('filePath', ''),
                            line_number=finding.get('line', 0),
                            column=finding.get('column', 0),
                            severity=finding.get('severity', 'info'),
                            tool='eslint',
                            rule_code=finding.get('ruleId', ''),
                            message=finding.get('message', ''),
                            auto_fixable=finding.get('fix') is not None,
                        ))
                        if finding.get('severity') == 2:
                            result.errors_count += 1
                        else:
                            result.warnings_count += 1

            result.success = True
            return result
        except FileNotFoundError:
            print("⚠️  eslint not found. Install with: npm install -g eslint")
            return result

    def _run_pylint(self, files: List[Path], result: ToolResult) -> ToolResult:
        """Run pylint linter."""
        try:
            cmd = ['pylint', '--output-format=json'] + [str(f) for f in files]
            output = subprocess.run(cmd, capture_output=True, text=True)

            if output.stdout:
                findings = json.loads(output.stdout)
                for finding in findings:
                    result.findings.append(FileFinding(
                        file_path=finding.get('path', ''),
                        line_number=finding.get('line', 0),
                        column=finding.get('column', 0),
                        severity=finding.get('type', 'info').lower(),
                        tool='pylint',
                        rule_code=finding.get('symbol', ''),
                        message=finding.get('message', ''),
                    ))
                    if finding.get('type') in ['error', 'fatal']:
                        result.errors_count += 1
                    else:
                        result.warnings_count += 1

            result.success = True
            return result
        except FileNotFoundError:
            print("⚠️  pylint not found. Install with: pip install pylint")
            return result

    def _run_yamllint(self, files: List[Path], result: ToolResult) -> ToolResult:
        """Run yamllint linter."""
        try:
            cmd = ['yamllint', '-f', 'parsable'] + [str(f) for f in files]
            output = subprocess.run(cmd, capture_output=True, text=True)

            if output.stdout:
                for line in output.stdout.strip().split('\n'):
                    if ':' in line:
                        parts = line.split(':')
                        if len(parts) >= 4:
                            result.findings.append(FileFinding(
                                file_path=parts[0],
                                line_number=int(parts[1]) if parts[1].isdigit() else 0,
                                column=int(parts[2]) if parts[2].isdigit() else 0,
                                severity=parts[3].strip().split('[')[0].strip().lower(),
                                tool='yamllint',
                                rule_code=parts[3].split('[')[-1].rstrip(']'),
                                message=' '.join(parts[4:]),
                            ))

            result.success = True
            return result
        except FileNotFoundError:
            print("⚠️  yamllint not found. Install with: pip install yamllint")
            return result

    def _tool_to_language(self, tool: str) -> str:
        """Map tool name to language."""
        tool_lang_map = {
            'black': 'python',
            'flake8': 'python',
            'pylint': 'python',
            'isort': 'python',
            'prettier': 'javascript',
            'eslint': 'javascript',
            'gofmt': 'go',
            'golangci-lint': 'go',
            'rustfmt': 'rust',
            'clippy': 'rust',
            'yamllint': 'yaml',
            'shfmt': 'shell',
        }
        return tool_lang_map.get(tool, 'unknown')


def generate_summary(results: List[ToolResult]) -> str:
    """Generate human-readable summary of results."""
    summary = []
    summary.append("\n" + "="*60)
    summary.append("Format & Lint Summary")
    summary.append("="*60)

    total_errors = 0
    total_warnings = 0
    total_info = 0

    for result in results:
        if result.findings:
            summary.append(f"\n{result.tool_name.upper()}:")
            summary.append(f"  Errors: {result.errors_count}")
            summary.append(f"  Warnings: {result.warnings_count}")
            summary.append(f"  Info: {result.info_count}")
            total_errors += result.errors_count
            total_warnings += result.warnings_count
            total_info += result.info_count

    summary.append(f"\n{'─'*60}")
    summary.append(f"Total Errors: {total_errors}")
    summary.append(f"Total Warnings: {total_warnings}")
    summary.append(f"Total Info: {total_info}")
    summary.append("="*60 + "\n")

    return "\n".join(summary)


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='Format and lint code')
    parser.add_argument('--files', nargs='+', help='Files to process')
    parser.add_argument('--directory', default='.', help='Directory to scan')
    parser.add_argument('--format-only', action='store_true', help='Only run formatters')
    parser.add_argument('--lint-only', action='store_true', help='Only run linters')
    parser.add_argument('--config', help='Path to config file')

    args = parser.parse_args()

    project_root = Path(args.directory)
    detector = LanguageDetector(project_root)

    # Detect languages
    detection = detector.detect()
    print("Detected languages and file counts:")
    for lang, info in detection.items():
        print(f"  {lang}: {info['count']} files")

    print("\nScan complete. Ready to format and lint.")


if __name__ == '__main__':
    main()
