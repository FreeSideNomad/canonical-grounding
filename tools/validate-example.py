#!/usr/bin/env python3
"""
Validate example YAML files against their domain schemas.

Usage: python3 validate-example.py <example_file>
Example: python3 validate-example.py ../domains/ddd/ddd-schema-example.yaml
"""

import sys
import yaml
from pathlib import Path
from typing import Dict, List, Set, Any
import re

def load_schema(schema_path: Path) -> Dict:
    """Load schema and extract $defs."""
    schema = {'$defs': {}}
    with open(schema_path) as f:
        for doc in yaml.safe_load_all(f):
            if doc and isinstance(doc, dict):
                if '$defs' in doc:
                    schema['$defs'].update(doc['$defs'])
    return schema

def load_example(example_path: Path) -> Any:
    """Load example YAML file (handles multi-document)."""
    with open(example_path) as f:
        docs = list(yaml.safe_load_all(f))
        # Return first document if multiple, otherwise single doc
        return docs[0] if docs else None

def detect_domain_from_path(example_path: Path) -> str:
    """Detect domain from file path."""
    path_str = str(example_path)
    if '/ddd/' in path_str:
        return 'ddd'
    elif '/data-eng/' in path_str:
        return 'data-eng'
    elif '/ux/' in path_str:
        return 'ux'
    elif '/qe/' in path_str:
        return 'qe'
    elif '/agile/' in path_str:
        return 'agile'
    return None

def get_schema_path(domain: str, base_path: Path) -> Path:
    """Get schema path for domain."""
    schema_paths = {
        'ddd': base_path / 'domains/ddd/model-schema.yaml',
        'data-eng': base_path / 'domains/data-eng/model.schema.yaml',
        'ux': base_path / 'domains/ux/model-schema.yaml',
        'qe': base_path / 'domains/qe/model-schema.yaml',
        'agile': base_path / 'domains/agile/model.schema.yaml'
    }
    return schema_paths.get(domain)

def extract_type_references(obj: Any, refs: Set[str]):
    """Recursively extract type references from example."""
    if isinstance(obj, dict):
        # Check for explicit type references
        if 'type' in obj and isinstance(obj['type'], str):
            # Handle patterns like "reference" or direct type names
            if obj['type'] == 'reference' and 'ref_type' in obj:
                refs.add(obj['ref_type'])
            elif obj['type'] not in ['object', 'array', 'string', 'integer', 'boolean', 'enum']:
                refs.add(obj['type'])

        # Look for $ref patterns
        if '$ref' in obj:
            ref_value = obj['$ref']
            if isinstance(ref_value, str) and '#/$defs/' in ref_value:
                concept = ref_value.split('#/$defs/')[-1]
                refs.add(concept)

        # Recurse into all values
        for value in obj.values():
            extract_type_references(value, refs)
    elif isinstance(obj, list):
        for item in obj:
            extract_type_references(item, refs)

def validate_required_fields(obj: Any, schema_def: Dict, concept_name: str) -> List[str]:
    """Validate required fields are present."""
    errors = []
    if not isinstance(obj, dict) or not isinstance(schema_def, dict):
        return errors

    required = schema_def.get('required', [])
    if required:
        for field in required:
            if field not in obj:
                errors.append(f"Missing required field '{field}' in {concept_name}")

    return errors

def validate_pattern_constraints(obj: Any, schema_def: Dict, concept_name: str, field_path: str = "") -> List[str]:
    """Validate pattern constraints on string fields."""
    errors = []

    if not isinstance(obj, dict) or not isinstance(schema_def, dict):
        return errors

    properties = schema_def.get('properties', {})

    for key, value in obj.items():
        current_path = f"{field_path}.{key}" if field_path else key

        if key in properties:
            prop_def = properties[key]

            # Check pattern constraints
            if isinstance(value, str) and 'pattern' in prop_def:
                pattern = prop_def['pattern']
                if not re.match(pattern, value):
                    errors.append(f"Field '{current_path}' in {concept_name} does not match pattern {pattern}: '{value}'")

            # Check enum constraints
            if 'enum' in prop_def or (isinstance(prop_def.get('type'), dict) and 'enum' in prop_def['type']):
                enum_values = prop_def.get('enum') or prop_def.get('type', {}).get('values', [])
                if enum_values and value not in enum_values:
                    errors.append(f"Field '{current_path}' in {concept_name} has invalid enum value '{value}'. Valid: {enum_values}")

    return errors

def validate_example(example_path: Path) -> Dict:
    """Validate an example file against its schema."""
    # Get base path from script location
    base_path = Path(__file__).parent.parent.resolve()

    # Verify it's the canonical-grounding directory
    if not (base_path / 'domains').exists():
        return {'error': f'Could not find canonical-grounding root directory. Base: {base_path}'}

    # Detect domain
    domain = detect_domain_from_path(example_path)
    if not domain:
        return {'error': f'Could not detect domain from path: {example_path}'}

    # Get schema path
    schema_path = get_schema_path(domain, base_path)
    if not schema_path or not schema_path.exists():
        return {'error': f'Schema not found: {schema_path}'}

    # Load schema and example
    try:
        schema = load_schema(schema_path)
        example = load_example(example_path)
    except Exception as e:
        return {'error': f'Failed to load files: {str(e)}'}

    # Extract concept references from example
    referenced_concepts = set()
    extract_type_references(example, referenced_concepts)

    # Validate references exist in schema
    schema_concepts = set(schema['$defs'].keys())
    undefined_concepts = referenced_concepts - schema_concepts

    # Validate structure and constraints
    validation_errors = []

    # If example is a dict, try to validate its structure
    if isinstance(example, dict):
        # Try to detect root concept type
        if 'type' in example and 'ref_type' in example:
            root_type = example['ref_type']
        elif len(referenced_concepts) == 1:
            root_type = list(referenced_concepts)[0]
        else:
            root_type = None

        if root_type and root_type in schema_concepts:
            schema_def = schema['$defs'][root_type]
            validation_errors.extend(validate_required_fields(example, schema_def, root_type))
            validation_errors.extend(validate_pattern_constraints(example, schema_def, root_type))

    return {
        'example_path': str(example_path),
        'domain': domain.upper(),
        'schema_path': str(schema_path),
        'referenced_concepts': sorted(referenced_concepts),
        'undefined_concepts': sorted(undefined_concepts),
        'validation_errors': validation_errors,
        'total_concepts_referenced': len(referenced_concepts),
        'schema_concepts_available': len(schema_concepts),
        'valid': len(undefined_concepts) == 0 and len(validation_errors) == 0
    }

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 validate-example.py <example_file>")
        print("Example: python3 validate-example.py ../domains/ddd/ddd-schema-example.yaml")
        sys.exit(1)

    example_path = Path(sys.argv[1])

    if not example_path.exists():
        print(f"❌ Example file not found: {example_path}")
        sys.exit(1)

    result = validate_example(example_path)

    if 'error' in result:
        print(f"❌ {result['error']}")
        sys.exit(1)

    print(f"\n{'='*70}")
    print(f"{result['domain']} EXAMPLE VALIDATION")
    print(f"{'='*70}\n")

    print(f"Example: {result['example_path']}")
    print(f"Schema:  {result['schema_path']}")

    print(f"\n{'─'*70}")
    print(f"Concepts Referenced: {result['total_concepts_referenced']}")
    print(f"Schema Concepts Available: {result['schema_concepts_available']}")
    print(f"{'─'*70}\n")

    if result['referenced_concepts']:
        print("✓ CONCEPTS USED IN EXAMPLE:")
        for concept in result['referenced_concepts']:
            status = "✓" if concept not in result['undefined_concepts'] else "✗"
            print(f"  {status} {concept}")
        print()

    if result['undefined_concepts']:
        print("❌ UNDEFINED CONCEPTS (not in schema):")
        for concept in result['undefined_concepts']:
            print(f"  ✗ {concept}")
        print()

    if result['validation_errors']:
        print("❌ VALIDATION ERRORS:")
        for error in result['validation_errors']:
            print(f"  ✗ {error}")
        print()

    if result['valid']:
        print("✅ STATUS: VALID")
        print("   - All referenced concepts exist in schema")
        print("   - No validation errors detected")
        sys.exit(0)
    else:
        print("❌ STATUS: INVALID")
        if result['undefined_concepts']:
            print(f"   - {len(result['undefined_concepts'])} undefined concept(s)")
        if result['validation_errors']:
            print(f"   - {len(result['validation_errors'])} validation error(s)")
        sys.exit(1)

if __name__ == '__main__':
    main()
