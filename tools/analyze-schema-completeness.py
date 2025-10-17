#!/usr/bin/env python3
"""
Analyze schema completeness by comparing schemas to ontological taxonomies.
"""
import yaml
import json
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple

def extract_concepts_from_taxonomy(taxonomy_path: Path) -> Set[str]:
    """Extract concept names from ontological taxonomy markdown."""
    with open(taxonomy_path) as f:
        content = f.read()

    concepts = set()

    # Pattern 1: Hierarchy nodes (├── ConceptName, └── ConceptName)
    for match in re.finditer(r'[├└]── ([A-Z][a-zA-Z\s]+(?:\([^)]+\))?)', content):
        concept = match.group(1).strip()
        # Clean up parenthetical descriptions
        concept = re.sub(r'\s*\([^)]+\)', '', concept)
        concepts.add(concept)

    # Pattern 2: Bold concepts (**Concept**)
    for match in re.finditer(r'\*\*([A-Z][a-zA-Z\s]+)\*\*', content):
        concept = match.group(1).strip()
        if len(concept) > 2 and not concept.isupper():
            concepts.add(concept)

    # Pattern 3: List items with concepts
    for match in re.finditer(r'^[\s]*-\s+\*\*([A-Z][a-zA-Z\s]+)\*\*:', content, re.MULTILINE):
        concept = match.group(1).strip()
        concepts.add(concept)

    return concepts

def extract_concepts_from_schema(schema_path: Path) -> Set[str]:
    """Extract $defs concept names from YAML schema."""
    concepts = set()

    with open(schema_path) as f:
        # Handle multiple YAML documents
        try:
            for schema in yaml.safe_load_all(f):
                if schema and isinstance(schema, dict):
                    if '$defs' in schema:
                        concepts.update(schema['$defs'].keys())
                    elif 'definitions' in schema:
                        concepts.update(schema['definitions'].keys())
        except yaml.YAMLError:
            # Try single document
            f.seek(0)
            schema = yaml.safe_load(f)
            if schema and isinstance(schema, dict):
                if '$defs' in schema:
                    concepts.update(schema['$defs'].keys())
                elif 'definitions' in schema:
                    concepts.update(schema['definitions'].keys())

    return concepts

def normalize_concept_name(name: str) -> str:
    """Normalize concept name for comparison."""
    # Convert spaces to underscores, remove special chars, lowercase
    normalized = name.lower()
    normalized = re.sub(r'[^a-z0-9_\s]', '', normalized)
    normalized = re.sub(r'\s+', '_', normalized)
    return normalized

def find_missing_concepts(taxonomy_concepts: Set[str], schema_concepts: Set[str]) -> List[Tuple[str, str]]:
    """Find concepts in taxonomy but not in schema."""
    missing = []

    taxonomy_normalized = {normalize_concept_name(c): c for c in taxonomy_concepts}
    schema_normalized = set(normalize_concept_name(c) for c in schema_concepts)

    for norm_name, original_name in taxonomy_normalized.items():
        if norm_name not in schema_normalized:
            missing.append((original_name, norm_name))

    return sorted(missing)

def analyze_domain(domain_name: str, domain_path: Path) -> Dict:
    """Analyze completeness for a single domain."""

    # Find taxonomy file
    taxonomy_files = list(domain_path.glob('docs/*taxonomy*.md')) + \
                     list(domain_path.glob('docs/*ontolog*.md'))

    if not taxonomy_files:
        return {
            'domain': domain_name,
            'status': 'NO_TAXONOMY',
            'message': 'No ontological taxonomy file found'
        }

    # Find schema file
    schema_files = list(domain_path.glob('model*.yaml')) + \
                   list(domain_path.glob('*.schema.yaml'))

    if not schema_files:
        return {
            'domain': domain_name,
            'status': 'NO_SCHEMA',
            'message': 'No schema file found'
        }

    # Extract concepts
    taxonomy_concepts = extract_concepts_from_taxonomy(taxonomy_files[0])
    schema_concepts = extract_concepts_from_schema(schema_files[0])

    # Find gaps
    missing = find_missing_concepts(taxonomy_concepts, schema_concepts)

    coverage = len(schema_concepts) / len(taxonomy_concepts) * 100 if taxonomy_concepts else 0

    return {
        'domain': domain_name,
        'status': 'ANALYZED',
        'taxonomy_file': taxonomy_files[0].name,
        'schema_file': schema_files[0].name,
        'taxonomy_concepts_count': len(taxonomy_concepts),
        'schema_concepts_count': len(schema_concepts),
        'coverage_percent': round(coverage, 1),
        'missing_concepts': missing[:20],  # Top 20 missing
        'total_missing': len(missing)
    }

def main():
    """Main analysis function."""
    base_path = Path('../domains')

    results = []
    for domain_dir in sorted(base_path.iterdir()):
        if domain_dir.is_dir() and not domain_dir.name.startswith('.'):
            result = analyze_domain(domain_dir.name, domain_dir)
            results.append(result)

    # Print report
    print("=" * 80)
    print("SCHEMA COMPLETENESS ANALYSIS")
    print("=" * 80)
    print()

    for result in results:
        print(f"Domain: {result['domain']}")
        print(f"Status: {result['status']}")

        if result['status'] == 'ANALYZED':
            print(f"  Taxonomy: {result['taxonomy_file']}")
            print(f"  Schema: {result['schema_file']}")
            print(f"  Taxonomy concepts: {result['taxonomy_concepts_count']}")
            print(f"  Schema concepts: {result['schema_concepts_count']}")
            print(f"  Coverage: {result['coverage_percent']}%")
            print(f"  Missing concepts: {result['total_missing']}")

            if result['missing_concepts']:
                print(f"  Top missing:")
                for orig, norm in result['missing_concepts'][:10]:
                    print(f"    - {orig} ({norm})")
        else:
            print(f"  {result['message']}")

        print()

    # Save JSON report
    with open('schema-completeness-report.json', 'w') as f:
        json.dump(results, f, indent=2)

    print(f"Full report saved to: schema-completeness-report.json")

if __name__ == '__main__':
    main()
