#!/usr/bin/env python3
"""
Convert Agile schema from PascalCase to snake_case naming convention.

Usage: python3 convert-agile-to-snake-case.py
"""

import yaml
import re
import json
from pathlib import Path

def pascal_to_snake(name):
    """Convert PascalCase to snake_case."""
    # Insert underscore before uppercase letters (except first)
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    # Insert underscore before uppercase letters preceded by lowercase
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def convert_string_value(value, mappings):
    """Convert PascalCase references in string values."""
    if not isinstance(value, str):
        return value

    # Convert $ref patterns: #/$defs/PascalCase → #/$defs/snake_case
    for old, new in mappings.items():
        value = value.replace(f'#/$defs/{old}', f'#/$defs/{new}')
        value = value.replace(f'#{old}', f'#{new}')
        # Pattern references
        if old in value and 'pattern' not in value.lower():
            value = value.replace(old, new)

    return value

def convert_value(value, mappings):
    """Recursively convert PascalCase to snake_case in all values."""
    if isinstance(value, str):
        return convert_string_value(value, mappings)
    elif isinstance(value, dict):
        return {k: convert_value(v, mappings) for k, v in value.items()}
    elif isinstance(value, list):
        return [convert_value(item, mappings) for item in value]
    return value

def main():
    base_path = Path(__file__).parent.parent
    schema_path = base_path / 'domains/agile/model.schema.yaml'

    print(f"Loading schema: {schema_path}")

    # Load schema
    with open(schema_path) as f:
        schema = yaml.safe_load(f)

    # Generate mappings for $defs
    mappings = {}
    if '$defs' in schema:
        for concept in schema['$defs'].keys():
            snake = pascal_to_snake(concept)
            if concept != snake:
                mappings[concept] = snake
                print(f"  {concept} → {snake}")

    print(f"\nConverting {len(mappings)} concepts...")

    # Convert $defs keys
    if '$defs' in schema:
        new_defs = {}
        for old_name, definition in schema['$defs'].items():
            new_name = mappings.get(old_name, old_name)
            # Convert references within definition
            new_def = convert_value(definition, mappings)
            new_defs[new_name] = new_def
        schema['$defs'] = new_defs

    # Convert references in rest of schema
    for key in schema.keys():
        if key != '$defs':
            schema[key] = convert_value(schema[key], mappings)

    # Save updated schema
    print(f"\nSaving updated schema...")
    with open(schema_path, 'w') as f:
        yaml.dump(schema, f, sort_keys=False, allow_unicode=True, default_flow_style=False)

    print(f"✓ Conversion complete!")
    print(f"✓ Converted {len(mappings)} concepts to snake_case")

    # Save mapping for reference
    mapping_path = base_path / 'tools/pascal-to-snake-mapping.json'
    with open(mapping_path, 'w') as f:
        json.dump(mappings, f, indent=2)
    print(f"✓ Mapping saved to: {mapping_path}")

if __name__ == '__main__':
    main()
