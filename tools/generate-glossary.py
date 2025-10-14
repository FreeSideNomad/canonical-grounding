#!/usr/bin/env python3
"""
Generate a comprehensive glossary of all concepts across all canonical domain models.

Usage: python3 generate-glossary.py [--output <file>] [--format md|yaml|json]
"""

import yaml
import json
import sys
from pathlib import Path
from typing import Dict, List
import argparse

def load_schema_with_metadata(schema_path: Path, domain: str) -> Dict:
    """Load schema and extract concept definitions with metadata."""
    concepts = {}

    if not schema_path.exists():
        return concepts

    with open(schema_path) as f:
        for doc in yaml.safe_load_all(f):
            if doc and isinstance(doc, dict) and '$defs' in doc:
                for concept_name, concept_def in doc['$defs'].items():
                    description = concept_def.get('description', 'No description available')
                    concept_type = concept_def.get('type', 'object')
                    required_fields = concept_def.get('required', [])
                    properties = concept_def.get('properties', {})

                    # Extract key properties
                    key_properties = []
                    for prop_name, prop_def in list(properties.items())[:5]:  # First 5 properties
                        prop_desc = prop_def.get('description', '')
                        prop_type = prop_def.get('type', 'unknown')
                        key_properties.append({
                            'name': prop_name,
                            'type': prop_type,
                            'description': prop_desc,
                            'required': prop_name in required_fields
                        })

                    concepts[concept_name] = {
                        'domain': domain,
                        'name': concept_name,
                        'description': description,
                        'type': concept_type,
                        'required_fields': required_fields,
                        'total_properties': len(properties),
                        'key_properties': key_properties
                    }

    return concepts

def load_all_concepts(base_path: Path) -> Dict[str, Dict]:
    """Load all concepts from all domain schemas."""
    schemas = {
        'DDD': base_path / 'domains/ddd/model-schema.yaml',
        'Data-Eng': base_path / 'domains/data-eng/model.schema.yaml',
        'UX': base_path / 'domains/ux/model-schema.yaml',
        'QE': base_path / 'domains/qe/model-schema.yaml',
        'Agile': base_path / 'domains/agile/model.schema.yaml'
    }

    all_concepts = {}
    domain_stats = {}

    for domain, schema_path in schemas.items():
        concepts = load_schema_with_metadata(schema_path, domain)
        all_concepts.update(concepts)
        domain_stats[domain] = len(concepts)

    return all_concepts, domain_stats

def generate_markdown_glossary(concepts: Dict, domain_stats: Dict) -> str:
    """Generate glossary in Markdown format."""
    lines = []

    lines.append("# Canonical Domain Model Glossary")
    lines.append("")
    lines.append(f"**Total Concepts:** {len(concepts)}")
    lines.append(f"**Domains:** {len(domain_stats)}")
    lines.append("")
    lines.append("## Concepts by Domain")
    lines.append("")
    for domain, count in sorted(domain_stats.items()):
        lines.append(f"- **{domain}**: {count} concepts")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Group by domain
    by_domain = {}
    for concept_name, concept in concepts.items():
        domain = concept['domain']
        if domain not in by_domain:
            by_domain[domain] = []
        by_domain[domain].append(concept)

    # Generate entries by domain
    for domain in sorted(by_domain.keys()):
        lines.append(f"## {domain} Domain")
        lines.append("")

        for concept in sorted(by_domain[domain], key=lambda x: x['name']):
            lines.append(f"### {concept['name']}")
            lines.append("")
            lines.append(f"**Domain:** {concept['domain']}")
            lines.append("")
            lines.append(f"**Description:** {concept['description']}")
            lines.append("")

            if concept['required_fields']:
                lines.append(f"**Required Fields:** {', '.join(concept['required_fields'])}")
                lines.append("")

            lines.append(f"**Total Properties:** {concept['total_properties']}")
            lines.append("")

            if concept['key_properties']:
                lines.append("**Key Properties:**")
                lines.append("")
                for prop in concept['key_properties']:
                    req_marker = "*(required)*" if prop['required'] else ""
                    lines.append(f"- `{prop['name']}` ({prop['type']}) {req_marker}")
                    if prop['description']:
                        lines.append(f"  - {prop['description']}")
                lines.append("")

            lines.append("---")
            lines.append("")

    # Add index
    lines.insert(len(lines), "## Alphabetical Index")
    lines.insert(len(lines), "")

    all_concepts_sorted = sorted(concepts.items(), key=lambda x: x[0])
    for concept_name, concept in all_concepts_sorted:
        lines.insert(len(lines), f"- **{concept_name}** ({concept['domain']})")

    return "\n".join(lines)

def generate_yaml_glossary(concepts: Dict, domain_stats: Dict) -> str:
    """Generate glossary in YAML format."""
    output = {
        'glossary': {
            'metadata': {
                'total_concepts': len(concepts),
                'total_domains': len(domain_stats),
                'concepts_by_domain': domain_stats
            },
            'concepts': []
        }
    }

    for concept_name, concept in sorted(concepts.items()):
        output['glossary']['concepts'].append(concept)

    return yaml.dump(output, sort_keys=False, allow_unicode=True)

def generate_json_glossary(concepts: Dict, domain_stats: Dict) -> str:
    """Generate glossary in JSON format."""
    output = {
        'glossary': {
            'metadata': {
                'total_concepts': len(concepts),
                'total_domains': len(domain_stats),
                'concepts_by_domain': domain_stats
            },
            'concepts': [concept for concept in sorted(concepts.values(), key=lambda x: x['name'])]
        }
    }

    return json.dumps(output, indent=2)

def main():
    parser = argparse.ArgumentParser(description='Generate canonical domain model glossary')
    parser.add_argument('--output', '-o', type=str, help='Output file (default: stdout)')
    parser.add_argument('--format', '-f', choices=['md', 'yaml', 'json'], default='md',
                        help='Output format (default: md)')

    args = parser.parse_args()

    base_path = Path(__file__).parent.parent

    # Load all concepts
    print("Loading schemas...", file=sys.stderr)
    concepts, domain_stats = load_all_concepts(base_path)

    print(f"Loaded {len(concepts)} concepts from {len(domain_stats)} domains", file=sys.stderr)

    # Generate glossary
    if args.format == 'md':
        output = generate_markdown_glossary(concepts, domain_stats)
    elif args.format == 'yaml':
        output = generate_yaml_glossary(concepts, domain_stats)
    elif args.format == 'json':
        output = generate_json_glossary(concepts, domain_stats)

    # Write output
    if args.output:
        output_path = Path(args.output)
        with open(output_path, 'w') as f:
            f.write(output)
        print(f"✅ Glossary written to: {output_path}", file=sys.stderr)
    else:
        print(output)

if __name__ == '__main__':
    main()
