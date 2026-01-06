"""
Convert YAML synthesis files to formatted Markdown reports
"""

import yaml
import os
from pathlib import Path

def convert_yaml_to_md(yaml_file, output_dir):
    """Convert a YAML synthesis file to markdown"""

    with open(yaml_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    # Extract filename without extension
    base_name = Path(yaml_file).stem
    md_filename = f"{base_name}.md"
    md_path = Path(output_dir) / md_filename

    # Determine title from filename
    title = base_name.replace('_synthesis_', '').replace('_', ' ').title()

    with open(md_path, 'w', encoding='utf-8') as md:
        # Write header
        md.write(f"# {title}\n\n")
        md.write(f"**Source**: Project 16 Ontologies Research v3\n\n")
        md.write(f"**Type**: Synthesis Analysis (UDWO-Primed)\n\n")

        # Write metadata if present
        if 'field' in data:
            md.write(f"**Field**: {data['field']}\n\n")
        if 'aggregated_at' in data:
            md.write(f"**Aggregated**: {data['aggregated_at']}\n\n")
        if 'batches_merged' in data:
            md.write(f"**Batches Merged**: {data['batches_merged']}\n\n")

        md.write("---\n\n")
        md.write("## Table of Contents\n\n")

        # Handle different structures
        if 'patterns' in data:
            md.write("- [Patterns](#patterns)\n")
            write_patterns(md, data['patterns'])

        elif 'entities' in data:
            md.write("- [Entities](#entities)\n")
            write_entities(md, data['entities'])

        elif 'relationships' in data:
            md.write("- [Relationships](#relationships)\n")
            write_relationships(md, data['relationships'])

        elif 'entity_types' in data:
            md.write("- [Entity Types](#entity-types)\n")
            write_entity_types(md, data['entity_types'])

        else:
            # Generic structure
            write_generic(md, data)

    print(f"Created: {md_path}")
    return md_path

def write_patterns(md, patterns):
    """Write patterns section"""
    md.write("\n## Patterns\n\n")
    md.write(f"**Total Patterns**: {len(patterns)}\n\n")

    for i, pattern in enumerate(patterns, 1):
        md.write(f"### {i}. {pattern.get('name', 'Unnamed Pattern')}\n\n")

        if 'description' in pattern:
            md.write(f"{pattern['description']}\n\n")

        if 'sources' in pattern:
            md.write("**Sources**:\n\n")
            for source in pattern['sources']:
                if 'chunk_ref' in source:
                    md.write(f"- **{source['chunk_ref']}**\n")
                if 'quote' in source:
                    md.write(f"  > {source['quote']}\n\n")

        md.write("---\n\n")

def write_entities(md, entities):
    """Write entities section"""
    md.write("\n## Entities\n\n")
    md.write(f"**Total Entities**: {len(entities)}\n\n")

    for entity_name, entity_data in entities.items():
        md.write(f"### {entity_name}\n\n")

        if isinstance(entity_data, dict):
            if 'definition' in entity_data:
                md.write(f"**Definition**: {entity_data['definition']}\n\n")

            if 'category' in entity_data:
                md.write(f"**Category**: {entity_data['category']}\n\n")

            if 'sources' in entity_data:
                md.write("**Sources**:\n\n")
                for source in entity_data['sources']:
                    if isinstance(source, dict):
                        if 'paper' in source:
                            md.write(f"- {source['paper']}")
                        if 'quote' in source:
                            md.write(f": _{source['quote']}_")
                        md.write("\n")
                md.write("\n")

            if 'characteristics' in entity_data:
                md.write(f"**Characteristics**: {entity_data['characteristics']}\n\n")

            if 'examples' in entity_data:
                md.write("**Examples**:\n")
                for ex in entity_data['examples']:
                    md.write(f"- {ex}\n")
                md.write("\n")

        md.write("---\n\n")

def write_relationships(md, relationships):
    """Write relationships section"""
    md.write("\n## Relationships\n\n")
    md.write(f"**Total Relationships**: {len(relationships)}\n\n")

    for rel_name, rel_data in relationships.items():
        md.write(f"### {rel_name}\n\n")

        if isinstance(rel_data, dict):
            if 'description' in rel_data:
                md.write(f"{rel_data['description']}\n\n")

            if 'domain' in rel_data:
                md.write(f"**Domain**: {rel_data['domain']}\n\n")

            if 'range' in rel_data:
                md.write(f"**Range**: {rel_data['range']}\n\n")

            if 'examples' in rel_data:
                md.write("**Examples**:\n")
                for ex in rel_data['examples']:
                    md.write(f"- {ex}\n")
                md.write("\n")

        md.write("---\n\n")

def write_entity_types(md, entity_types):
    """Write entity types section"""
    md.write("\n## Entity Types\n\n")

    for type_name, type_data in entity_types.items():
        md.write(f"### {type_name}\n\n")

        if isinstance(type_data, dict):
            if 'definition' in type_data:
                md.write(f"**Definition**: {type_data['definition']}\n\n")

            if 'instances' in type_data:
                md.write(f"**Instances**: {', '.join(type_data['instances'])}\n\n")

            if 'properties' in type_data:
                md.write("**Properties**:\n")
                for prop, val in type_data['properties'].items():
                    md.write(f"- **{prop}**: {val}\n")
                md.write("\n")

        md.write("---\n\n")

def write_generic(md, data):
    """Write generic YAML structure"""
    md.write("\n## Content\n\n")

    for key, value in data.items():
        if key in ['field', 'aggregated_at', 'batches_merged']:
            continue

        md.write(f"### {key.replace('_', ' ').title()}\n\n")

        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    for k, v in item.items():
                        md.write(f"**{k}**: {v}\n\n")
                else:
                    md.write(f"- {item}\n")
            md.write("\n")
        elif isinstance(value, dict):
            for k, v in value.items():
                md.write(f"**{k}**: {v}\n\n")
        else:
            md.write(f"{value}\n\n")

def main():
    workspace_dir = Path(__file__).parent

    # Find all _synthesis_*.yaml files
    yaml_files = list(workspace_dir.glob('_synthesis_*.yaml'))

    print(f"Found {len(yaml_files)} YAML synthesis files\n")

    for yaml_file in yaml_files:
        try:
            convert_yaml_to_md(yaml_file, workspace_dir)
        except Exception as e:
            print(f"Error processing {yaml_file.name}: {e}")

    print(f"\nConversion complete! Created {len(yaml_files)} markdown reports.")

if __name__ == '__main__':
    main()
