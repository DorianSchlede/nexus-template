"""
XML utilities for Claude Code hooks.

Shared XML escaping, building, and file loading utilities.
Used by session_start.py and other hooks that generate XML context.
"""

import re
import logging
from pathlib import Path
from typing import Optional


def escape_xml_content(content: str) -> str:
    """
    Escape XML special characters while preserving markdown code blocks.

    Handles:
    - < → &lt;
    - > → &gt;
    - & → &amp; (but not already-escaped entities)

    Args:
        content: Raw content to escape

    Returns:
        XML-safe content string
    """
    if not content:
        return ""

    # First, escape & that aren't already part of entities
    # Pattern: & not followed by lt; gt; amp; quot; apos; or #
    content = re.sub(r'&(?!(lt|gt|amp|quot|apos|#\d+|#x[0-9a-fA-F]+);)', '&amp;', content)

    # Then escape < and >
    content = content.replace('<', '&lt;')
    content = content.replace('>', '&gt;')

    return content


def escape_xml_attribute(value: str) -> str:
    """
    Escape for XML attribute values (handles quotes).

    Additional escaping beyond content:
    - " → &quot;
    - ' → &apos;

    Args:
        value: Raw attribute value

    Returns:
        XML-safe attribute value string
    """
    if not value:
        return ""

    # First escape content
    value = escape_xml_content(value)

    # Then escape quotes for attribute safety
    value = value.replace('"', '&quot;')
    value = value.replace("'", '&apos;')

    return value


def build_xml_header(mode: str, session_id: str, source: str, timestamp: str, comment: str) -> str:
    """
    Build standard nexus-context XML header with comment block.

    Args:
        mode: Context mode (startup|compact)
        session_id: Current session UUID
        source: Session source (new|compact|resume)
        timestamp: ISO timestamp
        comment: Custom comment for the header block

    Returns:
        XML header string with opening tag, comment, and session element
    """
    return f'''<nexus-context version="v4" mode="{mode}">
<!--
================================================================================
NEXUS OPERATING SYSTEM - PRIMARY CONTEXT INJECTION
================================================================================
{comment}
================================================================================
-->

  <session id="{escape_xml_attribute(session_id)}" source="{source}" timestamp="{timestamp}"/>'''


def load_file_to_xml(path: Path, tag_name: str, path_label: str, indent: int = 2) -> Optional[str]:
    """
    Load a file and wrap its content in XML tags.

    Args:
        path: Path to the file to load
        tag_name: XML tag name to wrap content in
        path_label: Value for the path attribute
        indent: Number of spaces for indentation (default 2)

    Returns:
        XML string with content, or None if file doesn't exist or can't be read
    """
    if not path.exists():
        return None

    try:
        content = escape_xml_content(path.read_text(encoding='utf-8'))
        spaces = " " * indent
        return f'''{spaces}<{tag_name} path="{escape_xml_attribute(path_label)}">
{content}
{spaces}</{tag_name}>'''
    except Exception as e:
        logging.error(f"Error reading {path}: {e}")
        return None


def open_section(name: str, attrs: Optional[dict] = None, indent: int = 2) -> str:
    """
    Open an XML section with optional attributes.

    Args:
        name: Tag name
        attrs: Optional dict of attribute name -> value
        indent: Number of spaces for indentation

    Returns:
        Opening tag string
    """
    spaces = " " * indent
    if not attrs:
        return f"{spaces}<{name}>"

    attr_str = " ".join([f'{k}="{escape_xml_attribute(str(v))}"' for k, v in attrs.items()])
    return f"{spaces}<{name} {attr_str}>"


def close_section(name: str, indent: int = 2) -> str:
    """
    Close an XML section.

    Args:
        name: Tag name
        indent: Number of spaces for indentation

    Returns:
        Closing tag string
    """
    spaces = " " * indent
    return f"{spaces}</{name}>"
