#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pyyaml",
#     "pathlib",
# ]
# ///

"""
Architech Universal Shortcut Resolver
Resolves ~shortcuts to actual file paths using registry
"""

import argparse
import json
import os
import sys
from pathlib import Path
import subprocess
from typing import Dict, Optional, Tuple

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. Install with: uv add pyyaml", file=sys.stderr)
    sys.exit(1)


class ShortcutResolver:
    """Universal shortcut resolver for Architech framework."""
    
    def __init__(self, registry_path: str = ".architech/navigation/shortcut-registry.yaml"):
        self.registry_path = self._find_registry_path(registry_path)
        self.registry = self._load_registry()
        self.repo_context = self._detect_repository()
        self.cache = {}
    
    def _find_registry_path(self, registry_path: str) -> Path:
        """Find the registry path, walking up directories if necessary."""
        current_path = Path.cwd()
        
        # Try current directory first
        if (current_path / registry_path).exists():
            return current_path / registry_path
            
        # Walk up directories looking for Architech root
        for parent in current_path.parents:
            candidate = parent / registry_path
            if candidate.exists():
                return candidate
                
        # Fallback to original path
        return Path(registry_path)
    
    def _load_registry(self) -> Dict:
        """Load the shortcut registry YAML file."""
        try:
            if not self.registry_path.exists():
                raise FileNotFoundError(f"Shortcut registry not found: {self.registry_path}")
                
            with open(self.registry_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"ERROR: Failed to load shortcut registry: {e}", file=sys.stderr)
            return {"static_shortcuts": {}, "repo_aware_shortcuts": {}}
    
    def _detect_repository(self) -> str:
        """Detect current repository context using git and directory patterns."""
        try:
            # Method 1: Git remote origin
            result = subprocess.run(
                ["git", "config", "--get", "remote.origin.url"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                origin_url = result.stdout.strip()
                for repo_name in ["agent-backend", "agent-dashboard", "agent-framework", "claude-agent-tracer"]:
                    if repo_name in origin_url:
                        return repo_name
            
            # Method 2: Directory pattern matching
            current_path = Path.cwd()
            path_str = str(current_path)
            
            known_repos = self.registry.get("repo_detection", {}).get("known_repositories", {})
            for repo_name, config in known_repos.items():
                patterns = config.get("patterns", [])
                for pattern in patterns:
                    # Simple pattern matching (replace * with any chars)
                    pattern_regex = pattern.replace("*", ".*")
                    if pattern.replace("*", "") in path_str:
                        # Verify with indicators if available
                        indicators = config.get("indicators", [])
                        if not indicators or any((current_path / ind.strip(".")).exists() for ind in indicators):
                            return repo_name
            
            return "top_level"  # Fallback to top-level context
            
        except Exception:
            return "top_level"
    
    def resolve(self, shortcut: str, feature: Optional[str] = None) -> str:
        """
        Resolve a shortcut to actual file path.
        
        Args:
            shortcut: The ~shortcut to resolve
            feature: Optional feature name for feature-specific shortcuts
            
        Returns:
            Resolved file path or original shortcut if not found
        """
        # Return non-shortcuts as-is
        if not shortcut.startswith('~'):
            return shortcut
            
        # Check cache first
        cache_key = f"{shortcut}:{self.repo_context}:{feature}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        resolved_path = self._resolve_shortcut(shortcut, feature)
        
        # Cache the result
        self.cache[cache_key] = resolved_path
        return resolved_path
    
    def _resolve_shortcut(self, shortcut: str, feature: Optional[str] = None) -> str:
        """Internal resolution logic following registry specification."""
        
        # Step 2: Check static shortcuts first
        static_shortcuts = self.registry.get("static_shortcuts", {})
        if shortcut in static_shortcuts:
            return static_shortcuts[shortcut]
        
        # Step 3-5: Check repo-aware shortcuts
        repo_aware = self.registry.get("repo_aware_shortcuts", {})
        if shortcut in repo_aware:
            spec = repo_aware[shortcut]
            
            # Step 4: Resolve variables
            primary = spec.get("primary", "")
            fallback = spec.get("fallback", "")
            
            # Substitute variables
            primary = primary.replace("{current_repo}", self.repo_context)
            if feature:
                primary = primary.replace("{feature}", feature)
                fallback = fallback.replace("{feature}", feature)
            
            # Step 5: Try primary path, fallback to secondary
            if Path(primary).exists():
                return primary
            else:
                return fallback
        
        # Step 7: Return original if not found
        return shortcut
    
    def validate_shortcut(self, shortcut: str) -> Tuple[bool, str]:
        """Validate that a shortcut exists in registry."""
        if not shortcut.startswith('~'):
            return True, "Not a shortcut"
            
        static_shortcuts = self.registry.get("static_shortcuts", {})
        repo_aware = self.registry.get("repo_aware_shortcuts", {})
        
        if shortcut in static_shortcuts:
            return True, "Static shortcut found"
        elif shortcut in repo_aware:
            return True, "Repo-aware shortcut found"
        else:
            return False, f"Shortcut '{shortcut}' not found in registry"
    
    def load_content(self, shortcut: str, feature: Optional[str] = None, warn_large_files: bool = True) -> Tuple[str, Optional[str]]:
        """
        Resolve shortcut and load file content.
        
        Args:
            shortcut: The ~shortcut to resolve
            feature: Optional feature name for feature-specific shortcuts  
            warn_large_files: Show warnings for large files (default: True)
        
        Returns:
            Tuple of (resolved_path, content) where content is None if file doesn't exist
        """
        resolved_path = self.resolve(shortcut, feature)
        
        try:
            # Handle both resolved paths and original shortcuts
            file_path = Path(resolved_path)
            
            if not file_path.exists():
                return resolved_path, None
                
            # Check file size and warn about large files
            file_size = file_path.stat().st_size
            if warn_large_files and file_size > 100000:  # 100KB threshold
                print(f"⚠️  WARNING: Large file detected ({file_size:,} bytes)", file=sys.stderr)
                print(f"⚠️  LOADING ENTIRE FILE CONTENT - NO TRUNCATION!", file=sys.stderr)
                if file_size > 1000000:  # 1MB threshold
                    print(f"🚨 VERY LARGE FILE: {file_size:,} bytes will be loaded!", file=sys.stderr)
                    
            # Read file content with UTF-8 encoding and fallback handling
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                # Fallback to latin-1 for binary-ish files
                with open(file_path, 'r', encoding='latin-1') as f:
                    content = f.read()
                    
            return resolved_path, content
            
        except Exception as e:
            return resolved_path, f"ERROR reading file: {e}"


def main():
    """CLI interface for shortcut resolver."""
    parser = argparse.ArgumentParser(description="Resolve Architech universal shortcuts")
    parser.add_argument("shortcut", help="Shortcut to resolve (e.g., ~architect)")
    parser.add_argument("--feature", help="Feature name for feature-specific shortcuts")
    parser.add_argument("--validate", action="store_true", help="Validate shortcut exists")
    parser.add_argument("--content", action="store_true", help="Return file content instead of just path")
    parser.add_argument("--content-only", action="store_true", help="Return only content, no path info")
    parser.add_argument("--json", action="store_true", help="Return JSON with path, content, and metadata")
    parser.add_argument("--max-size", type=int, help="Maximum file size to load (bytes). Files larger will show error.")
    parser.add_argument("--quiet", action="store_true", help="Suppress file size warnings")
    parser.add_argument("--registry", default=".architech/navigation/shortcut-registry.yaml",
                       help="Path to shortcut registry")
    parser.add_argument("--repo-context", help="Override repository context detection")
    
    args = parser.parse_args()
    
    try:
        resolver = ShortcutResolver(args.registry)
        
        # Override repo context if specified
        if args.repo_context:
            resolver.repo_context = args.repo_context
        
        if args.validate:
            is_valid, reason = resolver.validate_shortcut(args.shortcut)
            if is_valid:
                print(f"✅ VALID: {reason}", file=sys.stderr)
                resolved = resolver.resolve(args.shortcut, args.feature)
                print(resolved)
                sys.exit(0)
            else:
                print(f"❌ INVALID: {reason}", file=sys.stderr)
                sys.exit(1)
                
        elif args.json:
            # JSON output with path, content, and metadata
            import json
            
            # Check max-size before loading
            resolved_path = resolver.resolve(args.shortcut, args.feature)
            if Path(resolved_path).exists() and args.max_size:
                file_size = Path(resolved_path).stat().st_size
                if file_size > args.max_size:
                    result = {
                        "shortcut": args.shortcut,
                        "resolved_path": resolved_path,
                        "exists": True,
                        "repo_context": resolver.repo_context,
                        "error": f"File too large ({file_size:,} bytes) - exceeds max-size limit ({args.max_size:,} bytes)",
                        "file_size": file_size,
                        "content": None,
                        "content_length": 0
                    }
                    print(json.dumps(result, indent=2))
                    sys.exit(1)
            
            resolved_path, content = resolver.load_content(args.shortcut, args.feature, warn_large_files=not args.quiet)
            
            result = {
                "shortcut": args.shortcut,
                "resolved_path": resolved_path,
                "exists": content is not None,
                "repo_context": resolver.repo_context,
                "content": content,
                "content_length": len(content) if content else 0
            }
            
            if content is not None and not args.quiet:
                result["file_size_bytes"] = len(content.encode('utf-8')) if content else 0
                if result["file_size_bytes"] > 100000:
                    print(f"⚠️  NOTICE: Loaded {result['file_size_bytes']:,} bytes - ENTIRE FILE CONTENT!", file=sys.stderr)
            
            print(json.dumps(result, indent=2))
            sys.exit(0)
            
        elif args.content or args.content_only:
            # Content loading modes with size checking
            resolved_path = resolver.resolve(args.shortcut, args.feature)
            if Path(resolved_path).exists() and args.max_size:
                file_size = Path(resolved_path).stat().st_size
                if file_size > args.max_size:
                    print(f"ERROR: File too large ({file_size:,} bytes) - exceeds max-size limit ({args.max_size:,} bytes)", file=sys.stderr)
                    print(f"🚨 USE --max-size parameter to increase limit or load without size checking", file=sys.stderr)
                    sys.exit(1)
            
            resolved_path, content = resolver.load_content(args.shortcut, args.feature, warn_large_files=not args.quiet)
            
            if content is None:
                print(f"ERROR: File not found: {resolved_path}", file=sys.stderr)
                sys.exit(1)
            
            if args.content_only:
                # Only content, no path info - but still show size warning
                if not args.quiet and len(content) > 10000:
                    print(f"⚠️  LOADING ENTIRE FILE: {len(content):,} characters - NO TRUNCATION!", file=sys.stderr)
                print(content)
            else:
                # Both path and content
                print(f"# RESOLVED PATH: {resolved_path}", file=sys.stderr)
                print(f"# CONTENT LENGTH: {len(content)} chars - ENTIRE FILE LOADED!", file=sys.stderr)
                if not args.quiet and len(content) > 50000:
                    print(f"⚠️  LARGE FILE WARNING: {len(content):,} characters loaded completely!", file=sys.stderr)
                print(content)
            
            sys.exit(0)
            
        else:
            # Default: just resolve path
            resolved = resolver.resolve(args.shortcut, args.feature)
            print(resolved)
            sys.exit(0)
            
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()