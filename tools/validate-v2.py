#!/usr/bin/env python3
"""
Validate YAML examples against JSON Schema v2.0 schemas.
Usage: python tools/validate-v2.py <schema.yaml> <example.yaml>
"""

import sys
import yaml
import json
from jsonschema import Draft202012Validator, exceptions
from pathlib import Path

def load_yaml(file_path):
    """Load YAML file and convert to dict."""
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)

def validate_example(schema_path, example_path):
    """Validate example against schema."""
    print(f"\n{'='*80}")
    print(f"Validating: {example_path}")
    print(f"Against schema: {schema_path}")
    print(f"{'='*80}\n")

    try:
        # Load schema and example
        schema = load_yaml(schema_path)
        example = load_yaml(example_path)

        # Create validator
        validator = Draft202012Validator(schema)

        # Validate
        errors = list(validator.iter_errors(example))

        if not errors:
            print(f"✅ VALID: {Path(example_path).name}")
            return True
        else:
            print(f"❌ INVALID: {Path(example_path).name}")
            print(f"\nFound {len(errors)} validation error(s):\n")

            for i, error in enumerate(errors, 1):
                print(f"Error {i}:")
                print(f"  Path: {' -> '.join(str(p) for p in error.path) or 'root'}")
                print(f"  Message: {error.message}")
                print(f"  Schema path: {' -> '.join(str(p) for p in error.schema_path)}")
                print()

            return False

    except FileNotFoundError as e:
        print(f"❌ ERROR: File not found - {e}")
        return False
    except yaml.YAMLError as e:
        print(f"❌ ERROR: YAML parsing failed - {e}")
        return False
    except Exception as e:
        print(f"❌ ERROR: Unexpected error - {e}")
        return False

def main():
    if len(sys.argv) != 3:
        print("Usage: python tools/validate-v2.py <schema.yaml> <example.yaml>")
        print("\nExample:")
        print("  python tools/validate-v2.py domains/ddd/schemas/strategic-ddd.schema.yaml domains/ddd/examples/strategic-example.yaml")
        sys.exit(1)

    schema_path = sys.argv[1]
    example_path = sys.argv[2]

    success = validate_example(schema_path, example_path)

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
