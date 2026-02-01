#!/usr/bin/env python3
"""
file_analysis.py - SubAgent file analysis orchestration

Handles:
1. KB-based agent assignment (Task 10)
2. Auto-file-splitting for large files (Task 11)
3. Thematic clustering (Task 12)
4. Synthesis of SubAgent results (Task 13)

Used by setup-system skill during Step 1 (Context Upload).

Usage:
    from file_analysis import FileAnalysisOrchestrator

    orchestrator = FileAnalysisOrchestrator(workspace_path)
    orchestrator.scan_input_folder()
    clusters = orchestrator.cluster_files()
    agent_assignments = orchestrator.assign_agents()
    # ... run SubAgents ...
    results = orchestrator.synthesize_results(agent_outputs)
"""

import os
import json
import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field, asdict
from math import ceil


@dataclass
class FileInfo:
    """Information about a file for analysis."""
    path: Path
    filename: str
    size_kb: float
    extension: str
    theme: str = "general"
    is_chunk: bool = False
    chunk_index: int = 0
    total_chunks: int = 1
    original_path: Optional[Path] = None


@dataclass
class ThemeCluster:
    """Group of files with same theme."""
    theme: str
    files: List[FileInfo] = field(default_factory=list)
    total_kb: float = 0.0

    def add_file(self, file_info: FileInfo):
        self.files.append(file_info)
        self.total_kb += file_info.size_kb


@dataclass
class AgentAssignment:
    """Assignment of files to a SubAgent."""
    agent_id: str
    theme: str
    files: List[FileInfo] = field(default_factory=list)
    total_kb: float = 0.0


@dataclass
class FileAnalysisResult:
    """Result from a single SubAgent."""
    agent_id: str
    files_analyzed: int
    total_kb: float
    file_analyses: List[Dict[str, Any]] = field(default_factory=list)
    professional_context: Optional[Dict[str, Any]] = None
    integration_opportunities: List[Dict[str, Any]] = field(default_factory=list)
    workspace_structure_suggestion: Optional[Dict[str, Any]] = None


class FileAnalysisOrchestrator:
    """
    Orchestrates SubAgent file analysis for onboarding.

    Flow:
    1. scan_input_folder() - Find all files to analyze
    2. cluster_files() - Group by theme
    3. assign_agents() - KB-based assignment
    4. (External) Run SubAgents with assigned files
    5. synthesize_results() - Combine all outputs
    """

    # Theme detection patterns
    THEME_PATTERNS = {
        "clients": ["client", "customer", "account"],
        "sales": ["sales", "proposal", "quote", "deal", "pipeline"],
        "research": ["research", "paper", "study", "analysis", "report"],
        "finance": ["financial", "invoice", "budget", "expense", "revenue"],
        "code": [".py", ".js", ".ts", ".jsx", ".tsx", ".go", ".rs", ".java"],
        "marketing": ["marketing", "campaign", "brand", "content"],
        "hr": ["employee", "hiring", "onboard", "review", "perf"],
    }

    # Max file size before splitting (2MB)
    MAX_FILE_SIZE_KB = 2000

    # Target chunk size (1.5MB)
    CHUNK_SIZE_KB = 1500

    # Overlap lines for chunks
    CHUNK_OVERLAP_LINES = 50

    def __init__(self, workspace_path: Path):
        """
        Initialize orchestrator.

        Args:
            workspace_path: Path to Nexus workspace root
        """
        self.workspace = workspace_path
        self.input_folder = workspace_path / "04-workspace" / "input"
        self.output_folder = workspace_path / "02-builds" / "00-onboarding-session" / "02-resources"
        self.files: List[FileInfo] = []
        self.clusters: Dict[str, ThemeCluster] = {}
        self.assignments: List[AgentAssignment] = []

    def scan_input_folder(self) -> List[FileInfo]:
        """
        Scan input folder for files to analyze.

        Returns:
            List of FileInfo objects
        """
        self.files = []

        if not self.input_folder.exists():
            return self.files

        for file_path in self.input_folder.rglob("*"):
            if file_path.is_file() and not file_path.name.startswith("."):
                size_kb = file_path.stat().st_size / 1024
                ext = file_path.suffix.lower()

                # Skip very small files (<1KB)
                if size_kb < 1:
                    continue

                # Detect theme
                theme = self._detect_theme(file_path.name, ext)

                # Check if needs splitting
                if size_kb > self.MAX_FILE_SIZE_KB:
                    chunks = self._split_file(file_path, size_kb)
                    self.files.extend(chunks)
                else:
                    self.files.append(FileInfo(
                        path=file_path,
                        filename=file_path.name,
                        size_kb=size_kb,
                        extension=ext,
                        theme=theme
                    ))

        return self.files

    def _detect_theme(self, filename: str, extension: str) -> str:
        """Detect theme from filename and extension."""
        filename_lower = filename.lower()

        # Check code extensions first
        if extension in self.THEME_PATTERNS["code"]:
            return "code"

        # Check other patterns
        for theme, patterns in self.THEME_PATTERNS.items():
            if theme == "code":
                continue
            for pattern in patterns:
                if pattern in filename_lower:
                    return theme

        return "general"

    def _split_file(self, file_path: Path, total_kb: float) -> List[FileInfo]:
        """
        Split large file into chunks.

        Args:
            file_path: Path to large file
            total_kb: Total file size in KB

        Returns:
            List of FileInfo for chunks
        """
        chunks = []
        num_chunks = ceil(total_kb / self.CHUNK_SIZE_KB)
        theme = self._detect_theme(file_path.name, file_path.suffix.lower())

        # For binary files, just create logical chunks
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            lines = content.split('\n')

            lines_per_chunk = len(lines) // num_chunks
            if lines_per_chunk < 10:
                lines_per_chunk = len(lines)  # Don't split too small

            for i in range(num_chunks):
                start = max(0, i * lines_per_chunk - self.CHUNK_OVERLAP_LINES)
                end = min(len(lines), (i + 1) * lines_per_chunk + self.CHUNK_OVERLAP_LINES)

                chunk_lines = lines[start:end]
                chunk_kb = len('\n'.join(chunk_lines)) / 1024

                chunks.append(FileInfo(
                    path=file_path,
                    filename=f"{file_path.stem}_chunk{i+1}{file_path.suffix}",
                    size_kb=chunk_kb,
                    extension=file_path.suffix.lower(),
                    theme=theme,
                    is_chunk=True,
                    chunk_index=i,
                    total_chunks=num_chunks,
                    original_path=file_path
                ))
        except Exception:
            # For binary files, create single entry
            chunks.append(FileInfo(
                path=file_path,
                filename=file_path.name,
                size_kb=total_kb,
                extension=file_path.suffix.lower(),
                theme=theme
            ))

        return chunks

    def cluster_files(self) -> Dict[str, ThemeCluster]:
        """
        Group files by theme.

        Returns:
            Dict of theme -> ThemeCluster
        """
        self.clusters = {}

        for file_info in self.files:
            theme = file_info.theme
            if theme not in self.clusters:
                self.clusters[theme] = ThemeCluster(theme=theme)
            self.clusters[theme].add_file(file_info)

        return self.clusters

    def calculate_agent_count(self, total_kb: float) -> int:
        """
        Calculate number of agents based on total KB.

        KB-based scaling (from spec):
        - <1000 KB: 1 agent
        - 1000-3000 KB: 2 agents
        - 3000-5000 KB: 3 agents
        - 5000-10000 KB: 5 agents
        - 10000-20000 KB: 8 agents
        - >20000 KB: min(ceil(KB/2500), 10) agents

        Args:
            total_kb: Total file size in KB

        Returns:
            Number of agents to assign
        """
        if total_kb < 1000:
            return 1
        elif total_kb < 3000:
            return 2
        elif total_kb < 5000:
            return 3
        elif total_kb < 10000:
            return 5
        elif total_kb < 20000:
            return 8
        else:
            return min(ceil(total_kb / 2500), 10)

    def assign_agents(self) -> List[AgentAssignment]:
        """
        Assign files to SubAgents based on KB and themes.

        Strategy:
        1. Calculate total KB across all files
        2. Determine number of agents
        3. Distribute files by theme, balancing KB per agent

        Returns:
            List of AgentAssignment objects
        """
        if not self.clusters:
            self.cluster_files()

        total_kb = sum(f.size_kb for f in self.files)
        num_agents = self.calculate_agent_count(total_kb)

        self.assignments = []
        target_kb_per_agent = total_kb / num_agents if num_agents > 0 else total_kb

        agent_id = 0
        current_assignment = AgentAssignment(
            agent_id=f"subagent-{agent_id}",
            theme="mixed"
        )

        # Sort clusters by size (largest first)
        sorted_clusters = sorted(
            self.clusters.values(),
            key=lambda c: c.total_kb,
            reverse=True
        )

        for cluster in sorted_clusters:
            for file_info in cluster.files:
                # If current agent is full, start new one
                if current_assignment.total_kb >= target_kb_per_agent and agent_id < num_agents - 1:
                    if current_assignment.files:
                        self.assignments.append(current_assignment)
                    agent_id += 1
                    current_assignment = AgentAssignment(
                        agent_id=f"subagent-{agent_id}",
                        theme=file_info.theme
                    )

                current_assignment.files.append(file_info)
                current_assignment.total_kb += file_info.size_kb

        # Add final assignment
        if current_assignment.files:
            self.assignments.append(current_assignment)

        return self.assignments

    def get_agent_prompt(self, assignment: AgentAssignment) -> str:
        """
        Generate prompt for a SubAgent.

        Args:
            assignment: The AgentAssignment for this agent

        Returns:
            Formatted prompt string
        """
        files_list = "\n".join([
            f"- {f.path} ({f.size_kb:.1f} KB, theme: {f.theme})"
            for f in assignment.files
        ])

        return f"""# FILE ANALYSIS SUBAGENT - {assignment.agent_id}

You are analyzing user files to understand their context and work patterns.

## FILES TO ANALYZE ({len(assignment.files)} files, {assignment.total_kb:.1f} KB total)

{files_list}

## YOUR TASK

1. Read and analyze each file
2. Extract key information
3. Detect integration opportunities
4. Suggest folder organization

Return your analysis as JSON following the schema in:
00-system/core/nexus/prompts/subagent-file-analysis.md
"""

    def synthesize_results(self, agent_outputs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Combine results from all SubAgents.

        Args:
            agent_outputs: List of JSON outputs from SubAgents

        Returns:
            Synthesized analysis dict
        """
        synthesis = {
            "total_files_analyzed": 0,
            "total_kb_analyzed": 0,
            "file_analyses": [],
            "professional_context": {},
            "integration_opportunities": [],
            "workspace_structure_suggestion": {"folders": []},
        }

        seen_files = set()
        seen_integrations = set()
        all_contexts = []

        for output in agent_outputs:
            # Count files
            synthesis["total_files_analyzed"] += output.get("files_analyzed", 0)
            synthesis["total_kb_analyzed"] += output.get("total_kb", 0)

            # Merge file analyses (dedupe by filename)
            for analysis in output.get("file_analyses", []):
                filename = analysis.get("filename", "")
                if filename not in seen_files:
                    seen_files.add(filename)
                    synthesis["file_analyses"].append(analysis)

            # Collect professional contexts
            ctx = output.get("professional_context")
            if ctx:
                all_contexts.append(ctx)

            # Merge integration opportunities (dedupe by name+type)
            for opp in output.get("integration_opportunities", []):
                key = f"{opp.get('name', '')}|{opp.get('type', '')}"
                if key not in seen_integrations:
                    seen_integrations.add(key)
                    synthesis["integration_opportunities"].append(opp)

            # Merge workspace structure suggestions
            ws = output.get("workspace_structure_suggestion", {})
            for folder in ws.get("folders", []):
                # Dedupe by path
                existing_paths = [f["path"] for f in synthesis["workspace_structure_suggestion"]["folders"]]
                if folder.get("path") not in existing_paths:
                    synthesis["workspace_structure_suggestion"]["folders"].append(folder)

        # Select best professional context (most complete)
        if all_contexts:
            synthesis["professional_context"] = max(
                all_contexts,
                key=lambda c: sum(1 for v in c.values() if v)
            )

        return synthesis

    def save_results(self, synthesis: Dict[str, Any]):
        """
        Save synthesis results to output folder.

        Creates:
        - file-analysis.json (full JSON)
        - file-analysis-summary.md (human-readable)
        """
        self.output_folder.mkdir(parents=True, exist_ok=True)

        # Save JSON
        json_path = self.output_folder / "file-analysis.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(synthesis, f, indent=2)

        # Generate summary markdown
        summary_lines = [
            "# File Analysis Summary",
            "",
            f"**Files Analyzed**: {synthesis['total_files_analyzed']}",
            f"**Total Size**: {synthesis['total_kb_analyzed']:.1f} KB",
            "",
            "## Professional Context",
            "",
        ]

        ctx = synthesis.get("professional_context", {})
        if ctx:
            if ctx.get("role"):
                summary_lines.append(f"- **Role**: {ctx['role']}")
            if ctx.get("domain"):
                summary_lines.append(f"- **Domain**: {ctx['domain']}")
            if ctx.get("skills"):
                summary_lines.append(f"- **Skills**: {', '.join(ctx['skills'])}")

        summary_lines.extend([
            "",
            "## Integration Opportunities",
            "",
        ])

        for opp in synthesis.get("integration_opportunities", []):
            summary_lines.append(f"- **{opp.get('name', 'Unknown')}** ({opp.get('type', '')})")
            if opp.get("suggestion"):
                summary_lines.append(f"  - {opp['suggestion']}")

        summary_lines.extend([
            "",
            "## Suggested Workspace Structure",
            "",
        ])

        for folder in synthesis.get("workspace_structure_suggestion", {}).get("folders", []):
            summary_lines.append(f"- `{folder.get('path', '')}` - {folder.get('purpose', '')}")
            for sub in folder.get("subfolders", []):
                summary_lines.append(f"  - `{sub}`")

        summary_path = self.output_folder / "file-analysis-summary.md"
        summary_path.write_text('\n'.join(summary_lines), encoding='utf-8')

        return json_path, summary_path


def main():
    """CLI for testing file analysis."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python file_analysis.py <workspace_path>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    orchestrator = FileAnalysisOrchestrator(workspace)

    # Scan files
    files = orchestrator.scan_input_folder()
    print(f"Found {len(files)} files to analyze")

    # Cluster
    clusters = orchestrator.cluster_files()
    print(f"Clustered into {len(clusters)} themes:")
    for theme, cluster in clusters.items():
        print(f"  - {theme}: {len(cluster.files)} files, {cluster.total_kb:.1f} KB")

    # Assign agents
    assignments = orchestrator.assign_agents()
    print(f"Assigned to {len(assignments)} agents:")
    for assignment in assignments:
        print(f"  - {assignment.agent_id}: {len(assignment.files)} files, {assignment.total_kb:.1f} KB")


if __name__ == "__main__":
    main()
