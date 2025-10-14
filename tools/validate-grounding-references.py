#!/usr/bin/env python3
"""
Validate that all grounding relationships in interdomain-map.yaml reference valid schema concepts.

Usage: python3 validate-grounding-references.py
"""

import yaml
from pathlib import Path
from typing import Dict, Set, List
import sys

def load_schema_concepts(schema_path: Path) -> Dict[str, str]:
    """Load all $defs concepts from a schema, with case-insensitive lookup."""
    concepts = {}  # lowercase_name -> actual_name
    if not schema_path.exists():
        return concepts

    with open(schema_path) as f:
        for doc in yaml.safe_load_all(f):
            if doc and isinstance(doc, dict) and '$defs' in doc:
                for concept_name in doc['$defs'].keys():
                    concepts[concept_name.lower()] = concept_name
    return concepts

def load_all_schemas(base_path: Path) -> Dict[str, Set[str]]:
    """Load all domain schemas and extract concepts."""
    schemas = {
        'ddd': base_path / 'domains/ddd/model-schema.yaml',
        'data-eng': base_path / 'domains/data-eng/model.schema.yaml',
        'ux': base_path / 'domains/ux/model-schema.yaml',
        'qe': base_path / 'domains/qe/model-schema.yaml',
        'agile': base_path / 'domains/agile/model.schema.yaml'
    }

    domain_concepts = {}
    for domain, schema_path in schemas.items():
        domain_concepts[domain] = load_schema_concepts(schema_path)

    return domain_concepts

def parse_concept_reference(ref: str) -> tuple:
    """Parse concept reference like 'ux:Page' or 'agile:Feature.nfrRefs' into (domain, concept, field)."""
    if ':' not in ref:
        return (None, None, None)

    domain_part, concept_part = ref.split(':', 1)
    domain = domain_part.lower()

    # Handle field references like Feature.nfrRefs
    if '.' in concept_part:
        parts = concept_part.split('.')
        concept = parts[0]
        field = '.'.join(parts[1:])
    else:
        concept = concept_part
        field = None

    return (domain, concept, field)

def extract_concept_from_path(path: str) -> str:
    """Extract concept name from nested paths like 'ux_artifact_refs.page_refs'."""
    # Return last part before _refs or _ref suffix
    parts = path.split('.')
    for part in parts:
        if part.endswith('_refs') or part.endswith('_ref'):
            # Extract concept name (remove _refs/_ref suffix)
            base = part.replace('_refs', '').replace('_ref', '')
            return base
    return parts[-1] if parts else path

def validate_groundings(base_path: Path) -> Dict:
    """Validate all grounding relationships."""
    interdomain_map_path = base_path / 'research-output/interdomain-map.yaml'

    if not interdomain_map_path.exists():
        return {'error': f'Interdomain map not found: {interdomain_map_path}'}

    # Load domain concepts
    domain_concepts = load_all_schemas(base_path)

    # Load interdomain map
    with open(interdomain_map_path) as f:
        interdomain_map = yaml.safe_load(f)

    metadata = interdomain_map.get('metadata', {})
    groundings = interdomain_map.get('groundings', [])

    # Validation results
    valid_groundings = []
    invalid_groundings = []
    warnings = []

    for grounding in groundings:
        grounding_id = grounding.get('id', 'unknown')
        source_model = grounding.get('source', '')
        target_model = grounding.get('target', '')
        relationships = grounding.get('relationships', [])
        via = grounding.get('via', '')

        errors = []

        # Get domain from model name (model_ux -> ux, model_data_eng -> data-eng)
        source_domain = source_model.replace('model_', '').replace('_', '-') if source_model.startswith('model_') else None
        if isinstance(target_model, list):
            # Handle multiple targets
            target_domains = [t.replace('model_', '').replace('_', '-') for t in target_model if t.startswith('model_')]
        else:
            target_domain = target_model.replace('model_', '').replace('_', '-') if target_model.startswith('model_') else None
            target_domains = [target_domain] if target_domain else []

        # Validate relationships (the actual concept references)
        for rel in relationships:
            source_concept_ref = rel.get('source_concept', '')
            target_concept_ref = rel.get('target_concept', '')

            # Parse source concept
            source_domain_from_ref, source_concept, source_field = parse_concept_reference(source_concept_ref)
            if source_concept and source_domain_from_ref:
                if source_domain_from_ref not in domain_concepts:
                    errors.append(f"Unknown source domain in ref: '{source_domain_from_ref}'")
                elif source_concept.lower() not in domain_concepts[source_domain_from_ref]:
                    errors.append(f"Source concept '{source_concept}' not found in {source_domain_from_ref} schema (ref: {source_concept_ref})")

            # Parse target concept
            target_domain_from_ref, target_concept, target_field = parse_concept_reference(target_concept_ref)
            if target_concept and target_domain_from_ref:
                if target_domain_from_ref not in domain_concepts:
                    errors.append(f"Unknown target domain in ref: '{target_domain_from_ref}'")
                elif target_concept.lower() not in domain_concepts[target_domain_from_ref]:
                    errors.append(f"Target concept '{target_concept}' not found in {target_domain_from_ref} schema (ref: {target_concept_ref})")

        # Validate 'via' field if present
        if via:
            # 'via' often contains field paths like 'bounded_context_ref' or 'ux_artifact_refs.page_refs'
            # These are harder to validate without full schema introspection, so we just check for basic patterns
            if not any(c.isalnum() or c in ['_', '.'] for c in via):
                warnings.append(f"{grounding_id}: Suspicious 'via' field: '{via}'")

        grounding_result = {
            'id': grounding_id,
            'source': source_model,
            'target': target_model,
            'via': via,
            'type': grounding.get('type', ''),
            'strength': grounding.get('strength', ''),
            'relationships_count': len(relationships),
            'errors': errors
        }

        if errors:
            invalid_groundings.append(grounding_result)
        else:
            valid_groundings.append(grounding_result)

    return {
        'interdomain_map_path': str(interdomain_map_path),
        'metadata': metadata,
        'domain_concepts': {domain: len(concepts) for domain, concepts in domain_concepts.items()},
        'total_groundings': len(groundings),
        'valid_groundings': len(valid_groundings),
        'invalid_groundings': len(invalid_groundings),
        'warnings': len(warnings),
        'valid_grounding_details': valid_groundings,
        'invalid_grounding_details': invalid_groundings,
        'warning_details': warnings,
        'all_valid': len(invalid_groundings) == 0
    }

def main():
    base_path = Path(__file__).parent.parent

    result = validate_groundings(base_path)

    if 'error' in result:
        print(f"❌ {result['error']}")
        sys.exit(1)

    print(f"\n{'='*70}")
    print(f"GROUNDING REFERENCE VALIDATION")
    print(f"{'='*70}\n")

    print(f"Interdomain Map: {result['interdomain_map_path']}")
    print(f"Metadata Version: {result['metadata'].get('version', 'unknown')}")

    print(f"\n{'─'*70}")
    print(f"Domain Schemas Loaded:")
    for domain, count in result['domain_concepts'].items():
        print(f"  {domain.upper()}: {count} concepts")
    print(f"{'─'*70}\n")

    print(f"Total Groundings: {result['total_groundings']}")
    print(f"Valid: {result['valid_groundings']}")
    print(f"Invalid: {result['invalid_groundings']}")
    print(f"Warnings: {result['warnings']}")
    print(f"{'─'*70}\n")

    if result['invalid_groundings'] > 0:
        print("❌ INVALID GROUNDINGS:")
        for grounding in result['invalid_grounding_details']:
            print(f"\n  ID: {grounding['id']}")
            print(f"  Source: {grounding['source']}")
            print(f"  Target: {grounding['target']}")
            print(f"  Type: {grounding['type']} | Strength: {grounding['strength']}")
            print(f"  Errors:")
            for error in grounding['errors']:
                print(f"    ✗ {error}")
        print()

    if result['warning_details']:
        print("⚠️  WARNINGS:")
        for warning in result['warning_details']:
            print(f"  ⚠ {warning}")
        print()

    if result['valid_groundings'] > 0:
        print(f"✓ VALID GROUNDINGS ({result['valid_groundings']}):")

        # Group by type
        by_type = {}
        for grounding in result['valid_grounding_details']:
            gtype = grounding['type']
            if gtype not in by_type:
                by_type[gtype] = []
            by_type[gtype].append(grounding)

        for gtype, groundings in sorted(by_type.items()):
            print(f"\n  {gtype.upper()} ({len(groundings)}):")
            for grounding in groundings:
                strength_icon = "●" if grounding['strength'] == 'strong' else "○"
                print(f"    {strength_icon} {grounding['id']}: {grounding['source']} → {grounding['target']}")
        print()

    # Final status
    if result['all_valid']:
        print("✅ STATUS: ALL GROUNDINGS VALID")
        print("   - All source concepts exist in schemas")
        print("   - All target concepts exist in schemas")
        print("   - No broken references detected")
        sys.exit(0)
    else:
        print("❌ STATUS: INVALID GROUNDINGS DETECTED")
        print(f"   - {result['invalid_groundings']} grounding(s) have broken references")
        print("   - Fix schema definitions or update interdomain-map.yaml")
        sys.exit(1)

if __name__ == '__main__':
    main()
