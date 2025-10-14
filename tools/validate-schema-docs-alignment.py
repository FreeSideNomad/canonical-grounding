#!/usr/bin/env python3
"""
Validate that domain documentation covers all schema concepts.

Usage: python3 validate-schema-docs-alignment.py <domain>
Example: python3 validate-schema-docs-alignment.py ddd
"""

import sys
import yaml
from pathlib import Path
import re
from typing import Set, Dict, List

def extract_schema_concepts(schema_path: Path) -> Set[str]:
    """Extract $defs concept names from schema."""
    concepts = set()
    with open(schema_path) as f:
        for doc in yaml.safe_load_all(f):
            if doc and isinstance(doc, dict) and '$defs' in doc:
                concepts.update(doc['$defs'].keys())
    return concepts

def extract_doc_concepts(doc_path: Path) -> Set[str]:
    """Extract concept mentions from documentation (case-insensitive)."""
    concepts = set()
    with open(doc_path) as f:
        content = f.read().lower()
        # Look for patterns like "**Entity**", "- Entity", "Entity:", etc.
        # Convert underscores to spaces for matching
        return content
    return concepts

def validate_domain(domain: str, base_path: Path) -> Dict:
    """Validate a domain's schema against documentation."""

    domain_paths = {
        'ddd': {
            'schema': base_path / 'domains/ddd/model-schema.yaml',
            'docs': [
                base_path / 'domains/ddd/docs/ddd-06-ontological-taxonomy.md',
                base_path / 'domains/ddd/docs/ddd-02-strategic-patterns.md',
                base_path / 'domains/ddd/docs/ddd-03-tactical-patterns.md'
            ]
        },
        'data-eng': {
            'schema': base_path / 'domains/data-eng/model.schema.yaml',
            'docs': [
                base_path / 'domains/data-eng/docs/30-architecture.md',
                base_path / 'domains/data-eng/docs/quick-reference.md',
                base_path / 'domains/data-eng/docs/70-how-to-model-systems.md'
            ]
        },
        'ux': {
            'schema': base_path / 'domains/ux/model-schema.yaml',
            'docs': [
                base_path / 'domains/ux/docs/ux-08-ux-ontological-taxonomy.md',
                base_path / 'domains/ux/docs/ux-01-ia-foundations.md',
                base_path / 'domains/ux/docs/ux-05-component-architecture.md',
                base_path / 'domains/ux/docs/ux-06-behavior-specifications.md'
            ]
        },
        'qe': {
            'schema': base_path / 'domains/qe/model-schema.yaml',
            'docs': [
                base_path / 'domains/qe/docs/qe-03-domain-II-ontologies.md',
                base_path / 'domains/qe/docs/qe-15-qe-knowledge-base.md',
                base_path / 'domains/qe/docs/qe-comprehensive-summary.md'
            ]
        },
        'agile': {
            'schema': base_path / 'domains/agile/model.schema.yaml',
            'docs': [
                base_path / 'domains/agile/docs/vision.md',
                base_path / 'domains/agile/docs/scope-and-nfrs.md',
                base_path / 'domains/agile/docs/guide-to-agile.md'
            ]
        }
    }

    if domain not in domain_paths:
        return {'error': f'Unknown domain: {domain}'}

    paths = domain_paths[domain]

    # Extract schema concepts
    schema_concepts = extract_schema_concepts(paths['schema'])

    # Read all documentation
    all_doc_content = ""
    missing_docs = []
    for doc_path in paths['docs']:
        if doc_path.exists():
            with open(doc_path) as f:
                all_doc_content += f.read().lower() + "\n"
        else:
            missing_docs.append(str(doc_path))

    # Check coverage
    covered = set()
    not_covered = set()

    for concept in schema_concepts:
        # Convert snake_case to various forms for matching
        variants = [
            concept,  # snake_case
            concept.replace('_', ' '),  # space separated
            concept.replace('_', ''),  # no separators
            ''.join(word.capitalize() for word in concept.split('_'))  # PascalCase
        ]

        found = any(variant.lower() in all_doc_content for variant in variants)

        if found:
            covered.add(concept)
        else:
            not_covered.add(concept)

    return {
        'domain': domain.upper(),
        'schema_path': str(paths['schema']),
        'doc_paths': [str(p) for p in paths['docs']],
        'missing_doc_files': missing_docs,
        'total_concepts': len(schema_concepts),
        'concepts': sorted(schema_concepts),
        'covered_concepts': sorted(covered),
        'not_covered': sorted(not_covered),
        'coverage_percentage': (len(covered) / len(schema_concepts) * 100) if schema_concepts else 0
    }

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 validate-schema-docs-alignment.py <domain>")
        print("Domains: ddd, data-eng, ux, qe, agile")
        sys.exit(1)

    domain = sys.argv[1].lower()
    base_path = Path(__file__).parent.parent

    result = validate_domain(domain, base_path)

    if 'error' in result:
        print(f"❌ {result['error']}")
        sys.exit(1)

    print(f"\n{'='*70}")
    print(f"{result['domain']} SCHEMA-DOCUMENTATION ALIGNMENT VALIDATION")
    print(f"{'='*70}\n")

    print(f"Schema: {result['schema_path']}")
    print(f"Documentation files ({len(result['doc_paths'])}):")
    for doc in result['doc_paths']:
        status = "✓" if doc not in result['missing_doc_files'] else "✗ MISSING"
        print(f"  {status} {doc}")

    print(f"\n{'─'*70}")
    print(f"Total Schema Concepts: {result['total_concepts']}")
    print(f"Covered in Docs: {len(result['covered_concepts'])}")
    print(f"Not Covered: {len(result['not_covered'])}")
    print(f"Coverage: {result['coverage_percentage']:.1f}%")
    print(f"{'─'*70}\n")

    if result['not_covered']:
        print("❌ CONCEPTS NOT FOUND IN DOCUMENTATION:")
        for concept in result['not_covered']:
            print(f"  - {concept}")
        print()

    if result['covered_concepts']:
        print("✓ CONCEPTS DOCUMENTED:")
        for concept in result['covered_concepts']:
            print(f"  ✓ {concept}")
        print()

    # Status
    if result['coverage_percentage'] >= 95:
        print("✅ STATUS: EXCELLENT (≥95% coverage)")
        sys.exit(0)
    elif result['coverage_percentage'] >= 80:
        print("⚠️  STATUS: GOOD (≥80% coverage, but below 95% target)")
        sys.exit(0)
    else:
        print("❌ STATUS: NEEDS IMPROVEMENT (<80% coverage)")
        sys.exit(1)

if __name__ == '__main__':
    main()
