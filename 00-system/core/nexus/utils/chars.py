"""
OS-aware character constants for terminal output.

Smart detection: Uses Unicode for modern terminals, ASCII only for legacy Windows CMD.

Supports:
- VS Code Extension/Terminal (Unicode)
- Windows Terminal (Unicode)
- iTerm2, Hyper, Warp, etc. (Unicode)
- Mac/Linux terminals (Unicode)
- Legacy Windows CMD (ASCII fallback)

Usage:
    from nexus.utils.chars import OK, ERROR, WARN, ARROW, PROGRESS_FULL, PROGRESS_EMPTY

    print(f"{OK} Task completed")  # ✓ in modern terminals, [OK] in legacy CMD
    print(f"{ARROW} Next step")    # → in modern terminals, -> in legacy CMD
"""

import os
import sys


def _supports_unicode() -> bool:
    """
    Detect if the current terminal supports Unicode.

    Returns True for:
    - VS Code (extension or integrated terminal)
    - Windows Terminal (modern Windows terminal)
    - iTerm2, Hyper, Warp, and other modern terminals
    - Any terminal with UTF-8 encoding
    - All Mac/Linux terminals (they generally support Unicode)

    Returns False only for:
    - Legacy Windows CMD without UTF-8 encoding
    """
    # VS Code environments always support Unicode
    if os.environ.get("TERM_PROGRAM") == "vscode":
        return True
    if os.environ.get("VSCODE_GIT_IPC_HANDLE"):
        return True
    if os.environ.get("VSCODE_PID"):
        return True

    # Windows Terminal (modern) supports Unicode
    if os.environ.get("WT_SESSION"):
        return True

    # Popular modern terminals that support Unicode
    term_program = os.environ.get("TERM_PROGRAM", "").lower()
    if term_program in ("iterm.app", "hyper", "warp", "alacritty", "kitty", "apple_terminal"):
        return True

    # Check stdout encoding - if UTF-8, we're good
    if hasattr(sys.stdout, "encoding") and sys.stdout.encoding:
        if "utf" in sys.stdout.encoding.lower():
            return True

    # Non-Windows platforms generally support Unicode
    if sys.platform != "win32":
        return True

    # Legacy Windows CMD - fall back to ASCII
    return False


# Determine Unicode support once at import time
USE_UNICODE = _supports_unicode()


# Status indicators
if USE_UNICODE:
    OK = "✓"
    ERROR = "✗"
    WARN = "⚠"
    INFO = "ℹ"
    FAIL = "✗"
    STOP = "⏹"
else:
    OK = "[OK]"
    ERROR = "[ERROR]"
    WARN = "[!]"
    INFO = "[INFO]"
    FAIL = "[FAIL]"
    STOP = "[STOP]"


# Arrows and navigation
if USE_UNICODE:
    ARROW = "→"
    ARROW_LEFT = "←"
    ARROW_RIGHT = "→"
    BULLET = "•"
    DOT = "·"
else:
    ARROW = "->"
    ARROW_LEFT = "<-"
    ARROW_RIGHT = "->"
    BULLET = "*"
    DOT = "|"


# Progress bar characters
if USE_UNICODE:
    PROGRESS_FULL = "█"
    PROGRESS_EMPTY = "░"
else:
    PROGRESS_FULL = "#"
    PROGRESS_EMPTY = "-"


# Box drawing (for trees, tables)
if USE_UNICODE:
    BOX_H = "─"
    BOX_V = "│"
    BOX_TL = "┌"
    BOX_TR = "┐"
    BOX_BL = "└"
    BOX_BR = "┘"
    BOX_T = "┬"
    BOX_CROSS = "┼"
    TREE_BRANCH = "├── "
    TREE_LAST = "└── "
    TREE_PIPE = "│   "
    TREE_SPACE = "    "
else:
    BOX_H = "-"
    BOX_V = "|"
    BOX_TL = "+"
    BOX_TR = "+"
    BOX_BL = "+"
    BOX_BR = "+"
    BOX_T = "+"
    BOX_CROSS = "+"
    TREE_BRANCH = "+--"
    TREE_LAST = "+--"
    TREE_PIPE = "|  "
    TREE_SPACE = "   "


# Icons/symbols
if USE_UNICODE:
    ICON_KEY = "🔑"
    ICON_LOCK = "🔒"
    ICON_SEARCH = "🔍"
    ICON_EMAIL = "📧"
    ICON_FOLDER = "📁"
    ICON_FILE = "📄"
    ICON_PACKAGE = "📦"
    ICON_WAIT = "⏳"
    ICON_STAR = "⭐"
    ICON_TIP = "💡"
else:
    ICON_KEY = "[KEY]"
    ICON_LOCK = "[LOCK]"
    ICON_SEARCH = "[SEARCH]"
    ICON_EMAIL = "[EMAIL]"
    ICON_FOLDER = "[DIR]"
    ICON_FILE = "[FILE]"
    ICON_PACKAGE = "[PKG]"
    ICON_WAIT = "[WAIT]"
    ICON_STAR = "[*]"
    ICON_TIP = "[TIP]"


def make_progress_bar(percent: float, width: int = 10) -> str:
    """
    Create a visual progress bar.

    Args:
        percent: Progress percentage (0-100, or 0.0-1.0)
        width: Number of characters for the bar (default 10)

    Returns:
        String like "████████░░" on Mac or "########--" on Windows
    """
    if percent < 0:
        percent = 0
    elif percent > 100:
        percent = 100
    elif 0 < percent <= 1.0:
        percent = percent * 100

    filled = int(round(percent / 100 * width))
    empty = width - filled

    return PROGRESS_FULL * filled + PROGRESS_EMPTY * empty


def build_tree_line(name: str, is_last: bool = False, prefix: str = "") -> str:
    """Build a single line for tree output."""
    connector = TREE_LAST if is_last else TREE_BRANCH
    return f"{prefix}{connector}{name}"


def get_tree_prefix(is_last: bool = False) -> str:
    """Get the prefix for the next level in a tree."""
    return TREE_SPACE if is_last else TREE_PIPE


# =============================================================================
# Generic Output Upgrader
# =============================================================================
# On modern terminals: Automatically upgrades ASCII placeholders to Unicode
# On legacy Windows CMD: Returns string unchanged (ASCII-safe)
# =============================================================================

# Mapping from ASCII-safe to Unicode (only applied when USE_UNICODE is True)
_UPGRADE_MAP = {
    "[OK]": "✓",
    "[ERROR]": "✗",
    "[FAIL]": "✗",
    "[!]": "⚠",
    "[INFO]": "ℹ",
    "[STOP]": "⏹",
    "->": "→",
    "<-": "←",
    "[KEY]": "🔑",
    "[LOCK]": "🔒",
    "[SEARCH]": "🔍",
    "[EMAIL]": "📧",
    "[DIR]": "📁",
    "[FILE]": "📄",
    "[PKG]": "📦",
    "[WAIT]": "⏳",
    "[*]": "⭐",
    "[TIP]": "💡",
}


def prettify(text: str) -> str:
    """
    Upgrade ASCII placeholders to Unicode in modern terminals.

    Modern terminals (VS Code, iTerm2, Windows Terminal, etc.):
        Replaces [OK] with ✓, -> with →, etc.

    Legacy Windows CMD:
        Returns text unchanged (ASCII-safe)

    Usage:
        from nexus.utils.chars import prettify
        print(prettify("[OK] Done -> Next step"))
        # Modern: "✓ Done → Next step"
        # Legacy: "[OK] Done -> Next step"
    """
    if not USE_UNICODE:
        return text

    result = text
    for ascii_ver, unicode_ver in _UPGRADE_MAP.items():
        result = result.replace(ascii_ver, unicode_ver)
    return result


def nprint(*args, **kwargs) -> None:
    """
    Nexus print - auto-prettifies output based on terminal capability.

    Drop-in replacement for print() that upgrades ASCII to Unicode
    in modern terminals (VS Code, iTerm2, Windows Terminal, etc.).

    Usage:
        from nexus.utils.chars import nprint
        nprint("[OK] Task completed -> Next")
        # Modern: "✓ Task completed → Next"
        # Legacy: "[OK] Task completed -> Next"
    """
    prettified = [prettify(str(arg)) for arg in args]
    print(*prettified, **kwargs)
