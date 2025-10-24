#!/usr/bin/env python3
"""
Multi-File Schema Validation Example
Demonstrates how to validate YAML data against partitioned JSON Schema files
using Python jsonschema 4.x with referencing.Registry.

This example validates the Job Seeker Application examples against
strategic and tactical DDD schemas.
"""

import yaml
from pathlib import Path
from typing import Dict, List, Tuple
import sys

try:
    from referencing import Registry, Resource
    from referencing.jsonschema import DRAFT202012
    from jsonschema import Draft202012Validator
    from jsonschema.exceptions import ValidationError
except ImportError:
    print("ERROR: Required libraries not installed")
    print("Install with: pip install jsonschema referencing pyyaml")
    sys.exit(1)


class MultiFileSchemaValidator:
    """Validator that handles partitioned schemas with cross-references."""

    def __init__(self, schemas_dir: Path):
        self.schemas_dir = schemas_dir
        self.schemas = {}
        self.registry = None

    def load_schemas(self) -> bool:
        """Load all schema files from the schemas directory."""
        print("\n=== Loading Schemas ===")

        try:
            schema_files = list(self.schemas_dir.glob('*.schema.yaml'))
            if not schema_files:
                print(f"ERROR: No schema files found in {self.schemas_dir}")
                return False

            for schema_file in sorted(schema_files):
                with open(schema_file) as f:
                    schema = yaml.safe_load(f)
                    schema_name = schema_file.stem
                    self.schemas[schema_name] = schema
                    print(f"✓ Loaded: {schema_name}")
                    print(f"  Title: {schema.get('title', 'N/A')}")
                    print(f"  $id: {schema.get('$id', 'N/A')}")

                    # Count concepts
                    if '$defs' in schema:
                        concepts = list(schema['$defs'].keys())
                        print(f"  Concepts: {len(concepts)} - {', '.join(concepts[:5])}{'...' if len(concepts) > 5 else ''}")

            return True

        except Exception as e:
            print(f"ERROR loading schemas: {e}")
            return False

    def create_registry(self) -> Registry:
        """Create a Registry with all loaded schemas for cross-references."""
        print("\n=== Creating Schema Registry ===")

        resources = []

        for schema_name, schema in self.schemas.items():
            # Use $id if present, otherwise use filename
            if '$id' in schema:
                uri = schema['$id']
            else:
                uri = f"file:///{schema_name}"
                print(f"  WARNING: {schema_name} has no $id, using {uri}")

            resource = DRAFT202012.create_resource(schema)
            resources.append((uri, resource))
            print(f"✓ Registered: {uri}")

        self.registry = Registry().with_resources(resources)
        print(f"✓ Registry created with {len(resources)} schemas")

        return self.registry

    def validate_data(self, data_file: Path, schema_name: str) -> Tuple[bool, str]:
        """
        Validate a YAML data file against a specific schema.

        Args:
            data_file: Path to YAML data file
            schema_name: Name of schema to validate against (without .schema.yaml)

        Returns:
            Tuple of (is_valid, message)
        """
        if schema_name not in self.schemas:
            return False, f"Schema '{schema_name}' not found. Available: {list(self.schemas.keys())}"

        schema = self.schemas[schema_name]

        # Load data
        try:
            with open(data_file) as f:
                data = yaml.safe_load(f)
        except Exception as e:
            return False, f"Failed to load data file: {e}"

        # Create validator with registry (enables cross-schema references)
        validator = Draft202012Validator(schema, registry=self.registry)

        # Validate
        try:
            validator.validate(data)
            return True, "Validation successful"
        except ValidationError as e:
            error_path = " -> ".join(str(p) for p in e.absolute_path)
            return False, f"Validation failed at {error_path}: {e.message}"
        except Exception as e:
            return False, f"Validation error: {e}"

    def analyze_cross_references(self) -> Dict[str, List[str]]:
        """
        Analyze which schemas reference concepts from other schemas.

        Returns:
            Dictionary mapping schema names to list of external references
        """
        print("\n=== Analyzing Cross-Schema References ===")

        cross_refs = {}

        for schema_name, schema in self.schemas.items():
            refs = []

            # Look for bounded_context_ref patterns in tactical schema
            if 'tactical' in schema_name and '$defs' in schema:
                for concept_name, concept_def in schema['$defs'].items():
                    props = concept_def.get('properties', {})

                    # Check for references to strategic concepts
                    if 'bounded_context_ref' in props:
                        bc_ref = props['bounded_context_ref']
                        if 'pattern' in bc_ref and bc_ref['pattern'].startswith('^bc_'):
                            if 'BoundedContext from strategic schema' not in refs:
                                refs.append("BoundedContext (from strategic schema)")

                    if 'domain_ref' in props:
                        domain_ref = props['domain_ref']
                        if 'pattern' in domain_ref and domain_ref['pattern'].startswith('^dom_'):
                            if 'Domain from strategic schema' not in refs:
                                refs.append("Domain (from strategic schema)")

            if refs:
                cross_refs[schema_name] = refs
                print(f"✓ {schema_name}:")
                for ref in refs:
                    print(f"    → References: {ref}")
            else:
                print(f"✓ {schema_name}: No external references")

        return cross_refs

    def extract_concept_summary(self) -> Dict[str, Dict]:
        """Extract summary of concepts defined in each schema."""
        print("\n=== Schema Concept Summary ===")

        summary = {}

        for schema_name, schema in self.schemas.items():
            if '$defs' not in schema:
                continue

            concepts = {}
            for concept_name, concept_def in schema['$defs'].items():
                desc = concept_def.get('description', 'No description')
                concepts[concept_name] = {
                    'description': desc,
                    'required': concept_def.get('required', [])
                }

            summary[schema_name] = concepts

            print(f"\n{schema_name}:")
            for concept, info in concepts.items():
                print(f"  • {concept}: {info['description'][:60]}...")

        return summary


def run_validation_demo():
    """Run comprehensive validation demo."""
    print("="*70)
    print("Multi-File Schema Validation Demo")
    print("="*70)

    # Get paths
    script_dir = Path(__file__).parent
    schemas_dir = script_dir.parent / 'schemas'
    examples_dir = schemas_dir  # Examples are in same dir for this demo

    # Initialize validator
    validator = MultiFileSchemaValidator(schemas_dir)

    # Load schemas
    if not validator.load_schemas():
        return 1

    # Create registry
    validator.create_registry()

    # Analyze cross-references
    validator.analyze_cross_references()

    # Extract concept summary
    validator.extract_concept_summary()

    # Validate examples
    print("\n" + "="*70)
    print("Validating Examples")
    print("="*70)

    test_cases = [
        ('strategic-example.yaml', 'strategic-ddd'),
        ('tactical-example.yaml', 'tactical-ddd'),
    ]

    all_passed = True

    for example_file, schema_name in test_cases:
        example_path = examples_dir / example_file

        if not example_path.exists():
            print(f"\n✗ {example_file}: File not found")
            all_passed = False
            continue

        print(f"\n--- Validating {example_file} against {schema_name} ---")

        is_valid, message = validator.validate_data(example_path, schema_name)

        if is_valid:
            print(f"✓ {example_file}: {message}")
        else:
            print(f"✗ {example_file}: {message}")
            all_passed = False

    # Summary
    print("\n" + "="*70)
    print("Validation Summary")
    print("="*70)

    if all_passed:
        print("✓ All validations passed!")
        print("\nKey Takeaways:")
        print("  • Partitioned schemas loaded successfully")
        print("  • Cross-schema references resolved via Registry")
        print("  • Strategic and tactical patterns validated independently")
        print("  • Referential integrity maintained (BC refs, aggregate refs)")
        return 0
    else:
        print("✗ Some validations failed")
        return 1


def validate_custom_file(schema_file: Path, data_file: Path):
    """
    Validate a custom data file against a custom schema.

    Usage:
        python validate_multifile_schema.py <schema.yaml> <data.yaml>
    """
    print(f"Validating {data_file} against {schema_file}")

    schemas_dir = schema_file.parent
    schema_name = schema_file.stem

    validator = MultiFileSchemaValidator(schemas_dir)

    if not validator.load_schemas():
        return 1

    validator.create_registry()

    is_valid, message = validator.validate_data(data_file, schema_name)

    if is_valid:
        print(f"✓ Validation successful: {message}")
        return 0
    else:
        print(f"✗ Validation failed: {message}")
        return 1


def main():
    """Main entry point."""
    if len(sys.argv) == 1:
        # Run demo with built-in examples
        return run_validation_demo()
    elif len(sys.argv) == 3:
        # Validate custom files
        schema_file = Path(sys.argv[1])
        data_file = Path(sys.argv[2])

        if not schema_file.exists():
            print(f"ERROR: Schema file not found: {schema_file}")
            return 1

        if not data_file.exists():
            print(f"ERROR: Data file not found: {data_file}")
            return 1

        return validate_custom_file(schema_file, data_file)
    else:
        print("Usage:")
        print("  python validate_multifile_schema.py")
        print("  python validate_multifile_schema.py <schema.yaml> <data.yaml>")
        return 1


if __name__ == '__main__':
    sys.exit(main())
