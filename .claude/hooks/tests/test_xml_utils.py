"""
Tests for utils/xml.py - XML escaping and building utilities.
"""

import pytest
from pathlib import Path

from utils.xml import (
    escape_xml_content,
    escape_xml_attribute,
    load_file_to_xml,
    open_section,
    close_section,
)


class TestEscapeXmlContent:
    """Tests for escape_xml_content()"""

    def test_empty_string(self):
        assert escape_xml_content("") == ""

    def test_plain_text_unchanged(self):
        assert escape_xml_content("Hello World") == "Hello World"

    def test_escapes_less_than(self):
        assert escape_xml_content("a < b") == "a &lt; b"

    def test_escapes_greater_than(self):
        assert escape_xml_content("a > b") == "a &gt; b"

    def test_escapes_ampersand(self):
        assert escape_xml_content("a & b") == "a &amp; b"

    def test_preserves_already_escaped_lt(self):
        assert escape_xml_content("a &lt; b") == "a &lt; b"

    def test_preserves_already_escaped_gt(self):
        assert escape_xml_content("a &gt; b") == "a &gt; b"

    def test_preserves_already_escaped_amp(self):
        assert escape_xml_content("a &amp; b") == "a &amp; b"

    def test_preserves_numeric_entities(self):
        assert escape_xml_content("&#60;") == "&#60;"
        assert escape_xml_content("&#x3C;") == "&#x3C;"

    def test_mixed_escaped_and_unescaped(self):
        result = escape_xml_content("a & b &amp; c < d &lt; e")
        assert result == "a &amp; b &amp; c &lt; d &lt; e"

    def test_html_like_content(self):
        result = escape_xml_content("<div>Hello</div>")
        assert result == "&lt;div&gt;Hello&lt;/div&gt;"

    def test_markdown_with_angle_brackets(self):
        result = escape_xml_content("Use `git diff` to see changes")
        assert result == "Use `git diff` to see changes"

    def test_code_block_preserved(self):
        code = """```python
if a < b:
    print("less")
```"""
        result = escape_xml_content(code)
        assert "&lt;" in result
        assert "```python" in result


class TestEscapeXmlAttribute:
    """Tests for escape_xml_attribute()"""

    def test_empty_string(self):
        assert escape_xml_attribute("") == ""

    def test_plain_text_unchanged(self):
        assert escape_xml_attribute("hello") == "hello"

    def test_escapes_double_quote(self):
        assert escape_xml_attribute('say "hello"') == "say &quot;hello&quot;"

    def test_escapes_single_quote(self):
        assert escape_xml_attribute("it's") == "it&apos;s"

    def test_escapes_all_special_chars(self):
        result = escape_xml_attribute('<tag attr="val">')
        assert "&lt;" in result
        assert "&gt;" in result
        assert "&quot;" in result

    def test_path_with_special_chars(self):
        result = escape_xml_attribute("path/to/file's \"name\".txt")
        assert "&apos;" in result
        assert "&quot;" in result


class TestLoadFileToXml:
    """Tests for load_file_to_xml()"""

    def test_file_exists(self, tmp_path):
        test_file = tmp_path / "test.txt"
        test_file.write_text("Hello World")

        result = load_file_to_xml(test_file, "content", "test.txt")

        assert result is not None
        assert "<content" in result
        assert 'path="test.txt"' in result
        assert "Hello World" in result
        assert "</content>" in result

    def test_file_missing_returns_none(self, tmp_path):
        missing = tmp_path / "missing.txt"
        result = load_file_to_xml(missing, "content", "missing.txt")
        assert result is None

    def test_escapes_content(self, tmp_path):
        test_file = tmp_path / "test.txt"
        test_file.write_text("a < b & c > d")

        result = load_file_to_xml(test_file, "content", "test.txt")

        assert "&lt;" in result
        assert "&amp;" in result
        assert "&gt;" in result

    def test_custom_indent(self, tmp_path):
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")

        result = load_file_to_xml(test_file, "tag", "path", indent=4)

        assert result.startswith("    <tag")

    def test_special_chars_in_path_label(self, tmp_path):
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")

        result = load_file_to_xml(test_file, "tag", 'path/with"quotes')

        assert "&quot;" in result


class TestOpenSection:
    """Tests for open_section()"""

    def test_simple_tag(self):
        result = open_section("projects")
        assert result == "  <projects>"

    def test_with_attributes(self):
        result = open_section("project", {"id": "test", "status": "active"})
        assert "<project" in result
        assert 'id="test"' in result
        assert 'status="active"' in result

    def test_custom_indent(self):
        result = open_section("tag", indent=4)
        assert result == "    <tag>"

    def test_escapes_attribute_values(self):
        result = open_section("tag", {"name": 'test"value'})
        assert "&quot;" in result


class TestCloseSection:
    """Tests for close_section()"""

    def test_simple_tag(self):
        assert close_section("projects") == "  </projects>"

    def test_custom_indent(self):
        assert close_section("tag", indent=4) == "    </tag>"
