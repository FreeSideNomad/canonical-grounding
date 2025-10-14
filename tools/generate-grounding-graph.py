#!/usr/bin/env python3
"""
Generate Graphviz visualization of concept-to-concept grounding relationships.
"""

import sys
import yaml
from pathlib import Path
from typing import Dict, List, Set

class GroundingGraphGenerator:
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.research_path = base_path / "research-output"
        self.grounding_map = None

        # Color scheme for canons
        self.canon_colors = {
            'canon_ddd': '#E8F4F8',
            'canon_data_eng': '#FFF4E6',
            'canon_ux': '#F3E5F5',
            'canon_qe': '#E8F5E9',
            'canon_agile': '#FFF3E0'
        }

        # Edge colors by grounding type
        self.grounding_type_colors = {
            'structural': '#1976D2',    # Blue
            'semantic': '#7B1FA2',      # Purple
            'procedural': '#388E3C',    # Green
            'epistemic': '#F57C00'      # Orange
        }

        # Edge styles by strength
        self.strength_styles = {
            'strong': 'solid',
            'medium': 'dashed',
            'weak': 'dotted'
        }

    def load_grounding_map(self) -> bool:
        """Load interdomain grounding map."""
        map_path = self.research_path / "interdomain-map.yaml"
        if not map_path.exists():
            print(f"✗ Grounding map not found at {map_path}")
            return False

        try:
            with open(map_path, 'r') as f:
                self.grounding_map = yaml.safe_load(f)
                print(f"✓ Loaded grounding map with {len(self.grounding_map.get('groundings', []))} groundings")
                return True
        except Exception as e:
            print(f"✗ Failed to load grounding map: {e}")
            return False

    def extract_concept_relationships(self) -> List[Dict]:
        """Extract all concept-to-concept relationships from grounding map."""
        relationships = []

        for grounding in self.grounding_map.get('groundings', []):
            grounding_id = grounding.get('id')
            source_canon = grounding.get('source')
            target_canon = grounding.get('target')
            grounding_type = grounding.get('type', 'structural')
            strength = grounding.get('strength', 'medium')
            description = grounding.get('description', '')

            # Handle multi-target groundings
            target_canons = target_canon if isinstance(target_canon, list) else [target_canon]

            # Extract individual concept relationships
            for rel in grounding.get('relationships', []):
                source_concept = rel.get('source_concept', '')
                target_concept = rel.get('target_concept', '')
                cardinality = rel.get('cardinality', '')
                reference_field = rel.get('reference_field', '')
                validation = rel.get('validation', '')

                if source_concept and target_concept:
                    relationships.append({
                        'grounding_id': grounding_id,
                        'source_canon': source_canon,
                        'target_canons': target_canons,
                        'source_concept': source_concept,
                        'target_concept': target_concept,
                        'grounding_type': grounding_type,
                        'strength': strength,
                        'cardinality': cardinality,
                        'reference_field': reference_field,
                        'validation': validation,
                        'description': description
                    })

        return relationships

    def generate_dot(self, relationships: List[Dict], filename: str = "grounding-graph.dot"):
        """Generate Graphviz DOT file."""
        output_path = self.base_path / filename

        # Collect all concepts by canon
        canon_concepts = {}
        for rel in relationships:
            source_canon = rel['source_canon']
            source_concept = rel['source_concept']
            target_concept = rel['target_concept']

            if source_canon not in canon_concepts:
                canon_concepts[source_canon] = set()
            canon_concepts[source_canon].add(source_concept)

            for target_canon in rel['target_canons']:
                if target_canon not in canon_concepts:
                    canon_concepts[target_canon] = set()
                canon_concepts[target_canon].add(target_concept)

        with open(output_path, 'w') as f:
            f.write('digraph CanonicalGrounding {\n')
            f.write('  // Graph attributes\n')
            f.write('  rankdir=LR;\n')
            f.write('  node [shape=box, style=rounded];\n')
            f.write('  edge [fontsize=10];\n')
            f.write('  compound=true;\n')
            f.write('  newrank=true;\n')
            f.write('  splines=ortho;\n')
            f.write('  ranksep=1.5;\n')
            f.write('  nodesep=0.8;\n\n')

            # Define subgraphs for each canon
            canon_labels = {
                'canon_ddd': 'DDD Canon',
                'canon_data_eng': 'Data Engineering Canon',
                'canon_ux': 'UX Canon',
                'canon_qe': 'Quality Engineering Canon',
                'canon_agile': 'Agile Canon'
            }

            for canon, concepts in sorted(canon_concepts.items()):
                if not concepts:
                    continue

                color = self.canon_colors.get(canon, '#F5F5F5')
                label = canon_labels.get(canon, canon)

                f.write(f'  subgraph cluster_{canon} {{\n')
                f.write(f'    label="{label}";\n')
                f.write(f'    style=filled;\n')
                f.write(f'    color=lightgrey;\n')
                f.write(f'    fillcolor="{color}";\n')
                f.write(f'    fontsize=14;\n')
                f.write(f'    fontname="Helvetica-Bold";\n\n')

                # Add concept nodes
                for concept in sorted(concepts):
                    # Clean concept name for node ID
                    node_id = concept.replace(':', '_').replace('.', '_').replace('-', '_')
                    # Display name (without canon prefix)
                    display_name = concept.split(':')[1] if ':' in concept else concept

                    f.write(f'    {node_id} [label="{display_name}"];\n')

                f.write('  }\n\n')

            # Add edges for relationships
            f.write('  // Grounding relationships\n')
            for rel in relationships:
                source = rel['source_concept'].replace(':', '_').replace('.', '_').replace('-', '_')
                target = rel['target_concept'].replace(':', '_').replace('.', '_').replace('-', '_')

                # Edge attributes
                color = self.grounding_type_colors.get(rel['grounding_type'], '#666666')
                style = self.strength_styles.get(rel['strength'], 'solid')

                # Create label with details
                label_parts = []
                if rel['reference_field']:
                    label_parts.append(rel['reference_field'])
                if rel['cardinality']:
                    label_parts.append(f"[{rel['cardinality']}]")
                if rel['validation']:
                    label_parts.append(f"({rel['validation']})")

                label = '\\n'.join(label_parts) if label_parts else rel['grounding_type']

                f.write(f'  {source} -> {target} ')
                f.write(f'[label="{label}", ')
                f.write(f'color="{color}", ')
                f.write(f'style={style}, ')
                f.write(f'penwidth=2, ')
                f.write(f'tooltip="{rel["description"]}"];\n')

            # Add legend
            f.write('\n  // Legend\n')
            f.write('  subgraph cluster_legend {\n')
            f.write('    label="Legend";\n')
            f.write('    style=filled;\n')
            f.write('    fillcolor=white;\n')
            f.write('    fontsize=12;\n')
            f.write('    rank=sink;\n\n')

            # Grounding types
            f.write('    legend_structural [label="Structural", shape=plaintext, fontcolor="#1976D2"];\n')
            f.write('    legend_semantic [label="Semantic", shape=plaintext, fontcolor="#7B1FA2"];\n')
            f.write('    legend_procedural [label="Procedural", shape=plaintext, fontcolor="#388E3C"];\n')
            f.write('    legend_epistemic [label="Epistemic", shape=plaintext, fontcolor="#F57C00"];\n\n')

            # Strength styles
            f.write('    legend_strong [label="Strong", shape=plaintext];\n')
            f.write('    legend_medium [label="Medium", shape=plaintext];\n')
            f.write('    legend_weak [label="Weak", shape=plaintext];\n\n')

            # Invisible edges to organize legend
            f.write('    legend_structural -> legend_semantic -> legend_procedural -> legend_epistemic [style=invis];\n')
            f.write('    legend_strong -> legend_medium -> legend_weak [style=invis];\n')

            f.write('  }\n')

            f.write('}\n')

        print(f"✓ Generated DOT file: {output_path}")
        return output_path

    def generate_summary(self, relationships: List[Dict]):
        """Generate text summary of groundings."""
        print("\n" + "="*70)
        print("CONCEPT-TO-CONCEPT GROUNDING RELATIONSHIPS")
        print("="*70)

        # Group by source canon
        by_canon = {}
        for rel in relationships:
            canon = rel['source_canon']
            if canon not in by_canon:
                by_canon[canon] = []
            by_canon[canon].append(rel)

        canon_names = {
            'canon_ddd': 'DDD',
            'canon_data_eng': 'Data-Eng',
            'canon_ux': 'UX',
            'canon_qe': 'QE',
            'canon_agile': 'Agile'
        }

        for canon, rels in sorted(by_canon.items()):
            print(f"\n{canon_names.get(canon, canon)} ({len(rels)} relationships):")
            print("-" * 70)

            for rel in rels:
                source = rel['source_concept']
                target = rel['target_concept']
                field = rel['reference_field']
                strength = rel['strength']
                gtype = rel['grounding_type']

                print(f"  {source}")
                print(f"    → {target}")
                if field:
                    print(f"      via: {field}")
                print(f"      type: {gtype} | strength: {strength}")
                print()

    def run(self):
        """Run grounding graph generation."""
        print("Generating Canonical Grounding Concept Graph...\n")

        if not self.load_grounding_map():
            return False

        # Extract relationships
        relationships = self.extract_concept_relationships()
        print(f"\n✓ Extracted {len(relationships)} concept-to-concept relationships")

        # Generate DOT file
        dot_path = self.generate_dot(relationships)

        # Generate summary
        self.generate_summary(relationships)

        print("\n" + "="*70)
        print("To generate visualization:")
        print(f"  dot -Tpng {dot_path} -o grounding-graph.png")
        print(f"  dot -Tsvg {dot_path} -o grounding-graph.svg")
        print(f"  dot -Tpdf {dot_path} -o grounding-graph.pdf")
        print("="*70)

        return True


def main():
    script_path = Path(__file__).resolve()
    base_path = script_path.parent.parent

    generator = GroundingGraphGenerator(base_path)
    success = generator.run()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
