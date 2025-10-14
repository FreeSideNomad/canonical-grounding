#!/usr/bin/env python3
"""
Schema Validation Tool for Canonical Grounding
Validates YAML schemas, calculates closure, and checks grounding relationships.
"""

import sys
import json
import yaml
from pathlib import Path
from typing import Dict, List, Set, Tuple
import re

class SchemaValidator:
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.domains_path = base_path / "domains"
        self.research_path = base_path / "research-output"
        self.errors = []
        self.warnings = []
        self.canon_schemas = {}
        self.grounding_map = None

    def load_schemas(self) -> bool:
        """Load all canon schemas."""
        print("\n=== Loading Canon Schemas ===")

        canons = ["ddd", "data-eng", "ux", "qe", "agile"]
        for canon in canons:
            schema_path = self.domains_path / canon / "model-schema.yaml"
            json_schema_path = self.domains_path / canon / "model.schema.yaml"

            # Try YAML first, then JSON Schema format
            if schema_path.exists():
                try:
                    with open(schema_path, 'r') as f:
                        # Try loading all documents (some schemas have multiple YAML docs)
                        docs = list(yaml.safe_load_all(f))
                        # Use first document if multiple, or single doc
                        content = docs[0] if len(docs) == 1 else {'documents': docs}
                        self.canon_schemas[canon] = {
                            'path': schema_path,
                            'content': content,
                            'format': 'yaml',
                            'multi_doc': len(docs) > 1
                        }
                        doc_info = f" ({len(docs)} documents)" if len(docs) > 1 else ""
                        print(f"✓ Loaded {canon} schema (YAML format{doc_info})")
                except Exception as e:
                    self.errors.append(f"Failed to load {canon} schema: {e}")
                    print(f"✗ Failed to load {canon} schema: {e}")
                    return False
            elif json_schema_path.exists():
                try:
                    with open(json_schema_path, 'r') as f:
                        content = yaml.safe_load(f)
                        self.canon_schemas[canon] = {
                            'path': json_schema_path,
                            'content': content,
                            'format': 'json-schema'
                        }
                        print(f"✓ Loaded {canon} schema (JSON Schema format)")
                except Exception as e:
                    self.errors.append(f"Failed to load {canon} schema: {e}")
                    print(f"✗ Failed to load {canon} schema: {e}")
                    return False
            else:
                self.errors.append(f"Schema not found for {canon}")
                print(f"✗ Schema not found for {canon}")
                return False

        return True

    def load_grounding_map(self) -> bool:
        """Load interdomain grounding map."""
        print("\n=== Loading Grounding Map ===")

        map_path = self.research_path / "interdomain-map.yaml"
        if not map_path.exists():
            self.errors.append("Grounding map not found")
            print(f"✗ Grounding map not found at {map_path}")
            return False

        try:
            with open(map_path, 'r') as f:
                self.grounding_map = yaml.safe_load(f)
                groundings_count = len(self.grounding_map.get('groundings', []))
                print(f"✓ Loaded grounding map with {groundings_count} groundings")
                return True
        except Exception as e:
            self.errors.append(f"Failed to load grounding map: {e}")
            print(f"✗ Failed to load grounding map: {e}")
            return False

    def extract_references(self, content: any, canon: str) -> Set[str]:
        """Extract all domain references from schema content."""
        references = set()

        def extract_from_dict(obj, path=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    # Look for reference patterns
                    if isinstance(value, str):
                        # Pattern: canon:Type:id
                        matches = re.findall(r'(ddd|ux|qe|data-eng|agile):([A-Za-z]+):\[?([a-z0-9_-]+)\]?', value)
                        for match in matches:
                            target_canon, concept, _ = match
                            if target_canon != canon:
                                references.add(f"{target_canon}:{concept}")

                    # Look for *_ref, *_refs fields
                    if '_ref' in key.lower() or 'references' in key.lower():
                        if isinstance(value, str):
                            # Extract canon from pattern
                            match = re.match(r'(ddd|ux|qe|data-eng|agile):([A-Za-z]+)', value)
                            if match:
                                target_canon, concept = match.groups()
                                if target_canon != canon:
                                    references.add(f"{target_canon}:{concept}")
                        elif isinstance(value, dict):
                            extract_from_dict(value, f"{path}.{key}")
                        elif isinstance(value, list):
                            extract_from_list(value, f"{path}.{key}")
                    else:
                        extract_from_dict(value, f"{path}.{key}")

        def extract_from_list(obj, path=""):
            if isinstance(obj, list):
                for item in obj:
                    if isinstance(item, dict):
                        extract_from_dict(item, path)
                    elif isinstance(item, str):
                        matches = re.findall(r'(ddd|ux|qe|data-eng|agile):([A-Za-z]+)', item)
                        for match in matches:
                            target_canon, concept = match
                            if target_canon != canon:
                                references.add(f"{target_canon}:{concept}")

        extract_from_dict(content)
        return references

    def calculate_closure(self) -> Dict[str, float]:
        """Calculate closure percentage for each canon."""
        print("\n=== Calculating Closure ===")

        closures = {}

        for canon, schema_data in self.canon_schemas.items():
            content = schema_data['content']

            # Count total concepts (rough estimate based on top-level keys)
            if schema_data['format'] == 'yaml':
                # Handle multi-doc YAML
                if schema_data.get('multi_doc'):
                    # Count concepts across all documents
                    total_concepts = 0
                    for doc in content.get('documents', []):
                        if doc:
                            total_concepts += sum(1 for k in doc.keys() if k not in ['schema_version', 'schema_date', 'schema_purpose', 'validation_rules', 'extension_points', 'usage_guidelines', 'examples'])
                else:
                    # YAML format: count top-level definition keys
                    total_concepts = sum(1 for k in content.keys() if k not in ['schema_version', 'schema_date', 'schema_purpose', 'validation_rules', 'extension_points', 'usage_guidelines', 'examples'])
            else:
                # JSON Schema format: count definitions
                definitions = content.get('definitions', {})
                total_concepts = len(definitions)

            # Extract cross-canon references
            references = self.extract_references(content, canon)

            # Count grounded references (those explicitly documented in grounding map)
            grounded_refs = 0
            if self.grounding_map:
                canon_key = f"canon_{canon.replace('-', '_')}"
                for grounding in self.grounding_map.get('groundings', []):
                    if grounding.get('source') == canon_key:
                        grounded_refs += len(grounding.get('relationships', []))

            # Calculate closure
            # Closure = (internal concepts + explicitly grounded refs) / (total concepts + external refs)
            internal = total_concepts
            external = len(references)
            total = internal + external
            resolved = internal + grounded_refs

            if total > 0:
                closure_pct = (resolved / total) * 100
            else:
                closure_pct = 100.0

            closures[canon] = {
                'closure_pct': closure_pct,
                'internal_concepts': internal,
                'external_references': external,
                'grounded_references': grounded_refs,
                'total': total,
                'resolved': resolved
            }

            print(f"\n{canon.upper()}:")
            print(f"  Internal concepts: {internal}")
            print(f"  External references: {external}")
            print(f"  Grounded references: {grounded_refs}")
            print(f"  Closure: {closure_pct:.1f}%")

        return closures

    def validate_grounding_relationships(self) -> bool:
        """Validate all grounding relationships reference existing canons and concepts."""
        print("\n=== Validating Grounding Relationships ===")

        if not self.grounding_map:
            print("✗ No grounding map loaded")
            return False

        all_valid = True
        canon_mapping = {
            'canon_ddd': 'ddd',
            'canon_data_eng': 'data-eng',
            'canon_ux': 'ux',
            'canon_qe': 'qe',
            'canon_agile': 'agile'
        }

        for grounding in self.grounding_map.get('groundings', []):
            grounding_id = grounding.get('id', 'unknown')
            source = grounding.get('source')
            target = grounding.get('target')

            # Check source canon exists
            if source not in canon_mapping:
                self.errors.append(f"{grounding_id}: Invalid source canon '{source}'")
                print(f"✗ {grounding_id}: Invalid source canon '{source}'")
                all_valid = False

            # Check target canon(s) exist
            if isinstance(target, str):
                if target not in canon_mapping:
                    self.errors.append(f"{grounding_id}: Invalid target canon '{target}'")
                    print(f"✗ {grounding_id}: Invalid target canon '{target}'")
                    all_valid = False
            elif isinstance(target, list):
                for t in target:
                    if t not in canon_mapping:
                        self.errors.append(f"{grounding_id}: Invalid target canon '{t}'")
                        print(f"✗ {grounding_id}: Invalid target canon '{t}'")
                        all_valid = False

        if all_valid:
            print(f"✓ All {len(self.grounding_map.get('groundings', []))} grounding relationships are valid")

        return all_valid

    def check_circular_dependencies(self) -> bool:
        """Check for circular dependencies in grounding graph."""
        print("\n=== Checking for Circular Dependencies ===")

        if not self.grounding_map:
            print("✗ No grounding map loaded")
            return False

        # Build adjacency list
        graph = {}
        for grounding in self.grounding_map.get('groundings', []):
            source = grounding.get('source')
            target = grounding.get('target')

            if source not in graph:
                graph[source] = set()

            if isinstance(target, str):
                graph[source].add(target)
            elif isinstance(target, list):
                graph[source].update(target)

        # DFS to detect cycles
        def has_cycle(node, visited, rec_stack):
            visited.add(node)
            rec_stack.add(node)

            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    if has_cycle(neighbor, visited, rec_stack):
                        return True
                elif neighbor in rec_stack:
                    return True

            rec_stack.remove(node)
            return False

        visited = set()
        for node in graph:
            if node not in visited:
                if has_cycle(node, visited, set()):
                    self.errors.append("Circular dependency detected in grounding graph")
                    print("✗ Circular dependency detected")
                    return False

        print("✓ No circular dependencies found")
        return True

    def generate_report(self, closures: Dict[str, float]) -> str:
        """Generate validation report."""
        report = []
        report.append("\n" + "="*70)
        report.append("CANONICAL GROUNDING SCHEMA VALIDATION REPORT")
        report.append("="*70)

        # Schema validation
        report.append("\n## Schema Validation")
        if not self.errors:
            report.append("✓ All schemas valid")
        else:
            report.append(f"✗ {len(self.errors)} errors found")
            for error in self.errors:
                report.append(f"  - {error}")

        # Closure analysis
        report.append("\n## Closure Analysis")
        total_closure = sum(c['closure_pct'] for c in closures.values()) / len(closures)
        report.append(f"System average closure: {total_closure:.1f}%")
        report.append(f"Target: >95%")
        report.append("")

        for canon, data in sorted(closures.items()):
            status = "✓" if data['closure_pct'] >= 95 else "⚠"
            report.append(f"{status} {canon.upper()}: {data['closure_pct']:.1f}% closure")
            report.append(f"   ({data['resolved']}/{data['total']} concepts resolved)")

        # Overall status
        report.append("\n## Overall Status")
        if not self.errors and total_closure >= 95:
            report.append("✓ PRODUCTION READY")
            report.append("  - All schemas valid")
            report.append(f"  - System closure: {total_closure:.1f}% (target: >95%)")
            report.append("  - All groundings valid")
            report.append("  - No circular dependencies")
        elif not self.errors and total_closure >= 90:
            report.append("⚠ NEAR PRODUCTION READY")
            report.append(f"  - System closure: {total_closure:.1f}% (target: >95%)")
            report.append("  - Consider strengthening groundings in low-closure canons")
        else:
            report.append("✗ NOT PRODUCTION READY")
            if self.errors:
                report.append(f"  - {len(self.errors)} validation errors")
            if total_closure < 90:
                report.append(f"  - System closure: {total_closure:.1f}% (target: >95%)")

        report.append("\n" + "="*70)

        return "\n".join(report)

    def run(self) -> bool:
        """Run complete validation."""
        print("Starting Canonical Grounding Schema Validation...")

        # Load all schemas
        if not self.load_schemas():
            return False

        # Load grounding map
        if not self.load_grounding_map():
            return False

        # Calculate closure
        closures = self.calculate_closure()

        # Validate grounding relationships
        if not self.validate_grounding_relationships():
            return False

        # Check for circular dependencies
        if not self.check_circular_dependencies():
            return False

        # Generate and print report
        report = self.generate_report(closures)
        print(report)

        # Save report to file
        report_path = self.base_path / "validation-report.txt"
        with open(report_path, 'w') as f:
            f.write(report)
        print(f"\nReport saved to: {report_path}")

        return len(self.errors) == 0


def main():
    # Detect base path
    script_path = Path(__file__).resolve()
    base_path = script_path.parent.parent

    print(f"Base path: {base_path}")

    validator = SchemaValidator(base_path)
    success = validator.run()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
