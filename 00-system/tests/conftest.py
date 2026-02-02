"""
pytest configuration for nexus tests

Adds 00-system/core to Python path so tests can import nexus modules.
"""

import sys
from pathlib import Path

# Add 00-system/core to Python path for nexus module imports
core_dir = Path(__file__).parent.parent / "core"
sys.path.insert(0, str(core_dir))
