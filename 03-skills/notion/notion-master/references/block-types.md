# Notion Block Types Reference

> Complete reference for all Notion block types and their schemas.

---

## Block Type Overview

| Category | Block Types |
|----------|-------------|
| **Text** | paragraph, heading_1, heading_2, heading_3, quote, callout |
| **Lists** | bulleted_list_item, numbered_list_item, to_do, toggle |
| **Media** | image, video, file, pdf, bookmark |
| **Embeds** | embed, link_preview |
| **Code** | code, equation |
| **Structure** | divider, table_of_contents, breadcrumb, column_list, column |
| **Database** | child_database, child_page, link_to_page |
| **Advanced** | synced_block, template, table, table_row |

---

## Text Blocks

### Paragraph (`paragraph`)

Basic text content.

```json
{
  "type": "paragraph",
  "paragraph": {
    "rich_text": [{"type": "text", "text": {"content": "Your text here"}}],
    "color": "default"
  }
}
```

**Simple CLI**:
```bash
--type paragraph --text "Your text here"
```

---

### Headings (`heading_1`, `heading_2`, `heading_3`)

Three levels of headings. Can be toggleable (expandable).

```json
{
  "type": "heading_1",
  "heading_1": {
    "rich_text": [{"type": "text", "text": {"content": "Main Heading"}}],
    "is_toggleable": false,
    "color": "default"
  }
}
```

**Simple CLI**:
```bash
--type heading_1 --text "Main Heading"
--type heading_2 --text "Sub Heading"
--type heading_3 --text "Section"
```

---

### Quote (`quote`)

Block quote for citations or highlights.

```json
{
  "type": "quote",
  "quote": {
    "rich_text": [{"type": "text", "text": {"content": "Quoted text"}}],
    "color": "default"
  }
}
```

---

### Callout (`callout`)

Highlighted box with icon for important info.

```json
{
  "type": "callout",
  "callout": {
    "rich_text": [{"type": "text", "text": {"content": "Important note"}}],
    "icon": {"type": "emoji", "emoji": "💡"},
    "color": "yellow_background"
  }
}
```

**Colors**: `default`, `gray`, `brown`, `orange`, `yellow`, `green`, `blue`, `purple`, `pink`, `red` + `_background` variants

---

## List Blocks

### Bulleted List (`bulleted_list_item`)

Unordered list item with bullet.

```json
{
  "type": "bulleted_list_item",
  "bulleted_list_item": {
    "rich_text": [{"type": "text", "text": {"content": "List item"}}],
    "color": "default"
  }
}
```

**Simple CLI**:
```bash
--type bulleted_list_item --text "First item"
```

---

### Numbered List (`numbered_list_item`)

Ordered list item with number.

```json
{
  "type": "numbered_list_item",
  "numbered_list_item": {
    "rich_text": [{"type": "text", "text": {"content": "Step 1"}}],
    "color": "default"
  }
}
```

---

### To-Do (`to_do`)

Checkbox item.

```json
{
  "type": "to_do",
  "to_do": {
    "rich_text": [{"type": "text", "text": {"content": "Task to complete"}}],
    "checked": false,
    "color": "default"
  }
}
```

**Simple CLI**:
```bash
--type to_do --text "Complete this task"
--type to_do --text "Already done" --checked
```

---

### Toggle (`toggle`)

Expandable/collapsible content.

```json
{
  "type": "toggle",
  "toggle": {
    "rich_text": [{"type": "text", "text": {"content": "Click to expand"}}],
    "color": "default"
  }
}
```

**Note**: Toggle content goes inside as children blocks.

---

## Code & Equations

### Code Block (`code`)

Syntax-highlighted code.

```json
{
  "type": "code",
  "code": {
    "rich_text": [{"type": "text", "text": {"content": "console.log('Hello');"}}],
    "language": "javascript",
    "caption": []
  }
}
```

**Languages**: `abap`, `arduino`, `bash`, `basic`, `c`, `clojure`, `coffeescript`, `cpp`, `csharp`, `css`, `dart`, `diff`, `docker`, `elixir`, `elm`, `erlang`, `flow`, `fortran`, `fsharp`, `gherkin`, `glsl`, `go`, `graphql`, `groovy`, `haskell`, `html`, `java`, `javascript`, `json`, `julia`, `kotlin`, `latex`, `less`, `lisp`, `livescript`, `lua`, `makefile`, `markdown`, `markup`, `matlab`, `mermaid`, `nix`, `objective-c`, `ocaml`, `pascal`, `perl`, `php`, `plain text`, `powershell`, `prolog`, `protobuf`, `python`, `r`, `reason`, `ruby`, `rust`, `sass`, `scala`, `scheme`, `scss`, `shell`, `sql`, `swift`, `typescript`, `vb.net`, `verilog`, `vhdl`, `visual basic`, `webassembly`, `xml`, `yaml`, `java/c/c++/c#`

**Simple CLI**:
```bash
--type code --text "def hello(): pass" --language python
```

---

### Equation (`equation`)

LaTeX math expression.

```json
{
  "type": "equation",
  "equation": {
    "expression": "E = mc^2"
  }
}
```

---

## Media Blocks

### Image (`image`)

External or uploaded image.

```json
{
  "type": "image",
  "image": {
    "type": "external",
    "external": {"url": "https://example.com/image.png"},
    "caption": []
  }
}
```

**Note**: For uploaded images, use `"type": "file"` with Notion's file URL.

---

### Video (`video`)

Embedded video.

```json
{
  "type": "video",
  "video": {
    "type": "external",
    "external": {"url": "https://youtube.com/watch?v=..."}
  }
}
```

---

### File (`file`)

File attachment.

```json
{
  "type": "file",
  "file": {
    "type": "external",
    "external": {"url": "https://example.com/document.pdf"},
    "caption": [],
    "name": "document.pdf"
  }
}
```

---

### PDF (`pdf`)

Embedded PDF viewer.

```json
{
  "type": "pdf",
  "pdf": {
    "type": "external",
    "external": {"url": "https://example.com/file.pdf"}
  }
}
```

---

### Bookmark (`bookmark`)

Link preview card.

```json
{
  "type": "bookmark",
  "bookmark": {
    "url": "https://example.com",
    "caption": []
  }
}
```

---

## Structure Blocks

### Divider (`divider`)

Horizontal line separator.

```json
{
  "type": "divider",
  "divider": {}
}
```

**Simple CLI**:
```bash
--type divider --text ""
```

---

### Table of Contents (`table_of_contents`)

Auto-generated table of contents.

```json
{
  "type": "table_of_contents",
  "table_of_contents": {
    "color": "default"
  }
}
```

---

### Breadcrumb (`breadcrumb`)

Navigation breadcrumb.

```json
{
  "type": "breadcrumb",
  "breadcrumb": {}
}
```

---

### Column List & Columns (`column_list`, `column`)

Multi-column layout.

```json
{
  "type": "column_list",
  "column_list": {}
}
```

**Note**: Column list contains column blocks as children. Each column contains content blocks.

---

## Database Blocks

### Child Database (`child_database`)

Inline database.

```json
{
  "type": "child_database",
  "child_database": {
    "title": "My Database"
  }
}
```

**Note**: Database schema created separately via database API.

---

### Child Page (`child_page`)

Nested page reference.

```json
{
  "type": "child_page",
  "child_page": {
    "title": "Subpage Title"
  }
}
```

---

### Link to Page (`link_to_page`)

Reference to another page.

```json
{
  "type": "link_to_page",
  "link_to_page": {
    "type": "page_id",
    "page_id": "page-id-here"
  }
}
```

---

## Advanced Blocks

### Synced Block (`synced_block`)

Content synced across pages.

```json
{
  "type": "synced_block",
  "synced_block": {
    "synced_from": null
  }
}
```

**Note**: Original block has `synced_from: null`. References have `synced_from: {block_id: "..."}`.

---

### Template (`template`)

Reusable content template.

```json
{
  "type": "template",
  "template": {
    "rich_text": [{"type": "text", "text": {"content": "Template button text"}}]
  }
}
```

---

### Table (`table`)

Grid table layout.

```json
{
  "type": "table",
  "table": {
    "table_width": 3,
    "has_column_header": true,
    "has_row_header": false
  }
}
```

**Note**: Table rows are children of table block.

---

### Table Row (`table_row`)

Row within a table.

```json
{
  "type": "table_row",
  "table_row": {
    "cells": [
      [{"type": "text", "text": {"content": "Cell 1"}}],
      [{"type": "text", "text": {"content": "Cell 2"}}],
      [{"type": "text", "text": {"content": "Cell 3"}}]
    ]
  }
}
```

---

## Rich Text Formatting

All text-based blocks use rich_text arrays with formatting:

```json
{
  "rich_text": [
    {
      "type": "text",
      "text": {
        "content": "Plain text",
        "link": null
      },
      "annotations": {
        "bold": false,
        "italic": false,
        "strikethrough": false,
        "underline": false,
        "code": false,
        "color": "default"
      }
    }
  ]
}
```

### Formatted Text Example

```json
{
  "rich_text": [
    {"type": "text", "text": {"content": "Normal text "}},
    {"type": "text", "text": {"content": "bold"}, "annotations": {"bold": true}},
    {"type": "text", "text": {"content": " and "}},
    {"type": "text", "text": {"content": "italic"}, "annotations": {"italic": true}}
  ]
}
```

### Link Example

```json
{
  "rich_text": [
    {
      "type": "text",
      "text": {
        "content": "Click here",
        "link": {"url": "https://example.com"}
      }
    }
  ]
}
```

### Mention (User/Page/Date)

```json
{
  "rich_text": [
    {
      "type": "mention",
      "mention": {
        "type": "user",
        "user": {"id": "user-id-here"}
      }
    }
  ]
}
```

---

## Common Patterns

### Append Multiple Blocks

```bash
python manage_blocks.py append --page <page_id> --content '[
  {"type": "heading_1", "heading_1": {"rich_text": [{"type": "text", "text": {"content": "Section Title"}}]}},
  {"type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "Content here..."}}]}},
  {"type": "divider", "divider": {}}
]'
```

### Create Nested Structure

Blocks with children (toggle, column_list, etc.) require separate append calls:

1. Append parent block
2. Get parent block ID from response
3. Append children to parent block

---

## Read-Only Block Types

These blocks cannot be created via API, only read:

- `unsupported` - Block type not supported by API
- `audio` - Audio files (can be created as file)
- `link_preview` - Link preview cards

---

*For full API documentation: [Notion Block Reference](https://developers.notion.com/reference/block)*
