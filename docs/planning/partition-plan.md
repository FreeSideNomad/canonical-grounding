# Schema Partitioning Implementation Plan

**Date**: 2025-10-17
**Version**: 1.0
**Status**: Ready for Implementation
**Estimated Effort**: 3-4 days

---

## Overview

This plan details the step-by-step migration of the DDD domain model from a monolithic schema to partitioned schemas, establishing a repeatable pattern for other domains. The implementation follows a phased approach with backward compatibility preserved throughout.

---

## Phase 1: DDD Domain Partition (Proof of Concept)

**Goal**: Split DDD model-schema.yaml into strategic and tactical schemas
**Duration**: 1-2 days
**Risk**: Low (can revert easily)

### Step 1.1: Prepare Directory Structure

**Actions**:
```bash
cd /Users/igor/code/canonical-grounding/domains/ddd

# Create new directories
mkdir -p schemas
mkdir -p examples

# Backup existing files
cp model-schema.yaml model-schema.yaml.backup
cp ddd-schema-example.yaml ddd-schema-example.yaml.backup
```

**Validation**: Verify directories created, backups exist

### Step 1.2: Create Strategic Schema

**File**: `domains/ddd/schemas/strategic-ddd.schema.yaml`

**Content Extraction** from current `model-schema.yaml` (lines 1-237):
- Metadata and naming conventions
- `$defs` section:
  - `system`
  - `domain`
  - `bounded_context`
  - `context_mapping`

**New Schema Structure**:
```yaml
$schema: https://json-schema.org/draft/2020-12/schema
$id: https://canonical-grounding.org/schemas/ddd/strategic/v1
title: DDD Strategic Patterns Schema
description: Strategic patterns for Domain-Driven Design - domains, bounded contexts, context mappings

metadata:
  author: "Marina Music"
  created: "2025-10-04"
  updated: "2025-10-17"
  license: "MIT"
  version: "1.0.0"
  partition: "strategic"
  references:
    - "Eric Evans - Domain-Driven Design (2003)"
    - "Vaughn Vernon - Implementing Domain-Driven Design (2013)"

naming_conventions:
  domain_id: "dom_<name>"
  bounded_context_id: "bc_<name>"
  context_mapping_id: "cm_<source>_to_<target>"

$defs:
  system:
    # ... (copy from original)

  domain:
    # ... (copy from original)

  bounded_context:
    # ... (copy from original, modify references)
    # Change aggregate references from $ref to simple string patterns
    properties:
      aggregates:
        type: array
        description: "Aggregate IDs from tactical schema"
        items:
          type: string
          pattern: "^agg_[a-z0-9_]+$"

  context_mapping:
    # ... (copy from original)

validation_rules:
  - rule: "bounded_context_has_domain"
    description: "Every bounded context must belong to exactly one domain"
  - rule: "context_mapping_different_contexts"
    description: "Context mapping must connect two different bounded contexts"

best_practices:
  strategic:
    - "Start by identifying domains and subdomains"
    - "Define bounded contexts based on linguistic boundaries"
    - "Use context mapping to make integration explicit"
```

**Validation**:
```bash
# Validate YAML syntax
python3 -c "import yaml; yaml.safe_load(open('schemas/strategic-ddd.schema.yaml'))"
```

### Step 1.3: Create Tactical Schema

**File**: `domains/ddd/schemas/tactical-ddd.schema.yaml`

**Content Extraction** from current `model-schema.yaml` (lines 238-662):
- `$defs` section:
  - `aggregate`
  - `entity`
  - `value_object`
  - `repository`
  - `domain_service`
  - `application_service`
  - `domain_event`
  - `factory`
  - `specification`

**New Schema Structure**:
```yaml
$schema: https://json-schema.org/draft/2020-12/schema
$id: https://canonical-grounding.org/schemas/ddd/tactical/v1
title: DDD Tactical Patterns Schema
description: Tactical patterns for Domain-Driven Design - aggregates, entities, value objects, services

metadata:
  author: "Marina Music"
  created: "2025-10-04"
  updated: "2025-10-17"
  license: "MIT"
  version: "1.0.0"
  partition: "tactical"
  references:
    - "Eric Evans - Domain-Driven Design (2003)"
    - "Vaughn Vernon - Implementing Domain-Driven Design (2013)"

naming_conventions:
  aggregate_id: "agg_<name>"
  entity_id: "ent_<name>"
  value_object_id: "vo_<name>"
  repository_id: "repo_<name>"
  domain_service_id: "svc_dom_<name>"
  application_service_id: "svc_app_<name>"
  factory_id: "factory_<name>"
  domain_event_id: "evt_<name>"
  specification_id: "spec_<name>"

$defs:
  aggregate:
    # ... (copy from original)
    # Keep bounded_context_ref as string reference
    properties:
      bounded_context_ref:
        type: string
        pattern: "^bc_[a-z0-9_]+$"
        description: "Reference to BoundedContext from strategic schema"

  entity:
    # ... (copy from original)

  value_object:
    # ... (copy from original)

  repository:
    # ... (copy from original)

  domain_service:
    # ... (copy from original)

  application_service:
    # ... (copy from original)

  domain_event:
    # ... (copy from original)

  factory:
    # ... (copy from original)

  specification:
    # ... (copy from original)

validation_rules:
  - rule: "aggregate_root_is_entity"
    description: "Every aggregate must have exactly one root, which must be an entity"
  - rule: "repository_per_aggregate_root"
    description: "Repository must reference an aggregate, not individual entities"
  - rule: "value_objects_immutable"
    description: "Value objects must be immutable"
  - rule: "domain_service_stateless"
    description: "Domain services must be stateless"

best_practices:
  tactical:
    - "Design small aggregates (Vaughn Vernon's rule)"
    - "Protect true invariants in consistency boundaries"
    - "Reference other aggregates by identity only"
    - "Use eventual consistency outside aggregate boundaries"
```

**Validation**:
```bash
python3 -c "import yaml; yaml.safe_load(open('schemas/tactical-ddd.schema.yaml'))"
```

### Step 1.4: Create Partitioned Examples

**File**: `domains/ddd/examples/strategic-example.yaml`

Extract strategic-focused content from `ddd-schema-example.yaml`:
```yaml
# Job Seeker Application - DDD Strategic Model
# Focuses on domains, bounded contexts, and context mappings

system:
  id: "sys_job_seeker"
  name: "Job Seeker Application"
  version: "1.0.0"

domains:
  - id: "dom_job_matching"
    name: "Job Matching"
    type: "core"
    strategic_importance: "critical"
    bounded_contexts: ["bc_profile", "bc_matching"]

  - id: "dom_job_aggregation"
    name: "Job Aggregation"
    type: "supporting"
    bounded_contexts: ["bc_scrapers", "bc_job_catalog"]

bounded_contexts:
  - id: "bc_profile"
    name: "Candidate Profile Context"
    domain_ref: "dom_job_matching"
    ubiquitous_language:
      glossary:
        - term: "Profile"
          definition: "Complete professional representation"
        - term: "SkillSet"
          definition: "Collection of candidate skills"

  - id: "bc_matching"
    name: "Job Matching Context"
    domain_ref: "dom_job_matching"
    # Reference to aggregates (IDs only)
    aggregates: ["agg_match", "agg_recommendation"]

context_mappings:
  - id: "cm_job_catalog_to_matching"
    upstream_context: "bc_job_catalog"
    downstream_context: "bc_matching"
    relationship_type: "customer_supplier"
```

**File**: `domains/ddd/examples/tactical-example.yaml`

Extract tactical-focused content:
```yaml
# Job Seeker Application - DDD Tactical Model
# Focuses on aggregates, entities, value objects, and services

aggregates:
  - id: "agg_profile"
    name: "CandidateProfile"
    bounded_context_ref: "bc_profile"
    root_ref: "ent_candidate"
    entities: ["ent_candidate"]
    value_objects: ["vo_email", "vo_phone", "vo_skill_level"]
    consistency_rules:
      - "Email must be unique across system"
      - "Profile must have at least one contact method"

entities:
  - id: "ent_candidate"
    name: "Candidate"
    bounded_context_ref: "bc_profile"
    is_aggregate_root: true
    identity_field: "candidate_id"
    identity_generation: "auto_generated"
    attributes:
      - name: "candidate_id"
        type: "UUID"
        required: true
      - name: "email"
        type: "Email"
        value_object_ref: "vo_email"
        required: true

value_objects:
  - id: "vo_email"
    name: "Email"
    bounded_context_ref: "bc_profile"
    attributes:
      - name: "address"
        type: "string"
        validation: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
    validation_rules:
      - "Must be valid email format"
      - "Must not be disposable email domain"

repositories:
  - id: "repo_profile"
    name: "CandidateProfileRepository"
    aggregate_ref: "agg_profile"
    bounded_context_ref: "bc_profile"
    interface_methods:
      - name: "findById"
        query_type: "by_id"
      - name: "findByEmail"
        query_type: "by_criteria"
```

**Validation**: Verify examples are valid YAML

### Step 1.5: Keep Legacy Schema (Backward Compatibility)

**Action**: Keep `model-schema.yaml` unchanged for now

**Reasoning**:
- Tools still expect this file
- Provides fallback during transition
- Will be deprecated in next release

**Add Deprecation Notice**:
```yaml
# model-schema.yaml (add at top)
# DEPRECATED: This monolithic schema is being replaced by partitioned schemas.
# See schemas/strategic-ddd.schema.yaml and schemas/tactical-ddd.schema.yaml
# This file will be removed in version 2.0
```

### Step 1.6: Update Domain README

**File**: `domains/ddd/README.md` (create if doesn't exist)

```markdown
# DDD Domain Model

Version: 1.0.0
Last Updated: 2025-10-17

## Overview

This domain model defines strategic and tactical patterns for Domain-Driven Design (DDD).

## Schema Organization

The DDD schema is partitioned into two files for better maintainability:

### Strategic Patterns (`schemas/strategic-ddd.schema.yaml`)

Covers high-level architecture and domain organization:
- **System**: Complete system model
- **Domain**: Sphere of knowledge (Core, Supporting, Generic)
- **BoundedContext**: Explicit boundary for domain model
- **ContextMapping**: Relationships between contexts

**Use when**: Planning architecture, defining domain boundaries

### Tactical Patterns (`schemas/tactical-ddd.schema.yaml`)

Covers implementation building blocks:
- **Aggregate**: Consistency boundary (Aggregate Root + Entities + VOs)
- **Entity**: Object with identity
- **ValueObject**: Immutable value defined by attributes
- **Repository**: Persistence abstraction for aggregates
- **DomainService**: Stateless domain operations
- **ApplicationService**: Use case orchestration
- **DomainEvent**: Something that happened
- **Factory**: Complex object creation
- **Specification**: Encapsulated business rule

**Use when**: Implementing domain logic, designing aggregates

## Examples

- **Strategic Example** (`examples/strategic-example.yaml`): System, domains, contexts, mappings
- **Tactical Example** (`examples/tactical-example.yaml`): Aggregates, entities, services
- **Comprehensive Example** (`ddd-schema-example.yaml`): Complete system (legacy)

## References

- Eric Evans - Domain-Driven Design (2003)
- Vaughn Vernon - Implementing Domain-Driven Design (2013)
- Vaughn Vernon - Domain-Driven Design Distilled (2016)

## Documentation

See `docs/` directory for detailed documentation on each pattern:
- [Domain](docs/domain.md)
- [Bounded Context](docs/bounded-context.md)
- [Aggregate](docs/aggregate.md)
- [Entity](docs/entity.md)
- And more...
```

---

## Phase 2: Update Validation Tools

**Goal**: Modify tools to support partitioned schemas
**Duration**: 1 day
**Risk**: Medium (test thoroughly)

### Step 2.1: Update `validate-schemas.py`

**Changes Required**:

1. **Add multi-file schema loading**:
```python
def load_domain_schemas(self, domain_name):
    """Load all schema files for a domain (supports partitioning)."""
    domain_path = self.domains_path / domain_name
    schemas = []

    # Try new partitioned structure first
    schemas_dir = domain_path / 'schemas'
    if schemas_dir.exists() and list(schemas_dir.glob('*.schema.yaml')):
        print(f"  Loading partitioned schemas for {domain_name}...")
        for schema_file in sorted(schemas_dir.glob('*.schema.yaml')):
            with open(schema_file) as f:
                schema = yaml.safe_load(f)
                schema['_source_file'] = str(schema_file.name)
                schemas.append(schema)
                print(f"    ✓ {schema_file.name}")
    else:
        # Fall back to legacy single file
        # ... (existing logic)

    return schemas
```

2. **Update concept extraction to search all partitions**:
```python
def extract_references(self, schemas, canon):
    """Extract references from multiple schema files."""
    all_refs = set()
    for schema in schemas:
        refs = self._extract_from_single_schema(schema, canon)
        all_refs.update(refs)
    return all_refs
```

3. **Update closure calculation**:
```python
def calculate_closure(self):
    # Count concepts across all schema partitions
    total_concepts = 0
    for schema in schemas:
        if '$defs' in schema:
            total_concepts += len([k for k in schema['$defs'].keys()
                                  if not k.startswith('_')])
```

**Testing**:
```bash
# Test with DDD (partitioned)
python tools/validate-schemas.py

# Should show:
# DDD:
#   Loading partitioned schemas for ddd...
#     ✓ strategic-ddd.schema.yaml
#     ✓ tactical-ddd.schema.yaml
#   Internal concepts: 13
#   Closure: XX.X%
```

### Step 2.2: Update `validate-grounding-references.py`

**Changes Required**:

```python
def load_schema_concepts(domain_path: Path) -> Dict[str, str]:
    """Load all $defs concepts from a domain (handles partitioning)."""
    concepts = {}

    # Check for partitioned schemas
    schemas_dir = domain_path / 'schemas'
    if schemas_dir.exists():
        # Load from all partition files
        for schema_file in schemas_dir.glob('*.schema.yaml'):
            file_concepts = _load_concepts_from_file(schema_file)
            # Check for duplicates
            for concept_lower, concept_actual in file_concepts.items():
                if concept_lower in concepts and concepts[concept_lower] != concept_actual:
                    print(f"WARNING: Duplicate concept {concept_actual} in {schema_file}")
                concepts[concept_lower] = concept_actual
    else:
        # Legacy single file
        schema_file = domain_path / 'model-schema.yaml'
        if not schema_file.exists():
            schema_file = domain_path / 'model.schema.yaml'
        if schema_file.exists():
            concepts = _load_concepts_from_file(schema_file)

    return concepts
```

**Testing**:
```bash
python tools/validate-grounding-references.py

# Should show all groundings still valid
# DDD concepts found across strategic + tactical schemas
```

### Step 2.3: Update `validate-schema-docs-alignment.py`

**Changes Required**: Same pattern as grounding validation

**Testing**:
```bash
python tools/validate-schema-docs-alignment.py

# Should find all docs still aligned
# Concepts discovered across multiple schema files
```

### Step 2.4: Create New Example Validation Tool

**File**: `tools/validate-example-v2.py`

```python
#!/usr/bin/env python3
"""
Example validation tool with multi-file schema support.
Uses modern jsonschema 4.x with referencing.Registry.
"""

import yaml
from pathlib import Path
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012
from jsonschema import Draft202012Validator
import sys

def load_domain_schemas(domain_path: Path):
    """Load all schema files for a domain."""
    schemas = []

    schemas_dir = domain_path / 'schemas'
    if schemas_dir.exists():
        for schema_file in sorted(schemas_dir.glob('*.schema.yaml')):
            with open(schema_file) as f:
                schema = yaml.safe_load(f)
                schemas.append(schema)
    else:
        # Legacy
        for legacy_file in ['model-schema.yaml', 'model.schema.yaml']:
            legacy_path = domain_path / legacy_file
            if legacy_path.exists():
                with open(legacy_path) as f:
                    schemas.append(yaml.safe_load(f))
                break

    return schemas

def create_registry(schemas):
    """Create Registry for cross-schema validation."""
    resources = []
    for idx, schema in enumerate(schemas):
        if '$id' in schema:
            uri = schema['$id']
        else:
            uri = f"schema_{idx}"

        resource = DRAFT202012.create_resource(schema)
        resources.append((uri, resource))

    return Registry().with_resources(resources)

def validate_example(example_path: Path, domain_name: str):
    """Validate example against domain schema(s)."""
    domain_path = Path('domains') / domain_name

    # Load schemas and create registry
    schemas = load_domain_schemas(domain_path)
    if not schemas:
        print(f"✗ No schemas found for domain {domain_name}")
        return False

    registry = create_registry(schemas)

    # Load example
    with open(example_path) as f:
        example_data = yaml.safe_load(f)

    # Determine which schema to validate against
    example_name = example_path.stem
    schema = schemas[0]  # Default

    if len(schemas) > 1:
        # Try to match by name
        for s in schemas:
            schema_name = s.get('title', '').lower()
            if 'strategic' in example_name and 'strategic' in schema_name:
                schema = s
                break
            elif 'tactical' in example_name and 'tactical' in schema_name:
                schema = s
                break

    # Validate
    try:
        validator = Draft202012Validator(schema, registry=registry)
        validator.validate(example_data)
        print(f"✓ {example_path.name} is valid against {schema.get('title', 'schema')}")
        return True
    except Exception as e:
        print(f"✗ {example_path.name}: {e}")
        return False

def main():
    base_path = Path(__file__).parent.parent

    # Validate DDD examples
    ddd_path = base_path / 'domains' / 'ddd'
    examples_dir = ddd_path / 'examples'

    all_valid = True

    if examples_dir.exists():
        for example_file in examples_dir.glob('*.yaml'):
            valid = validate_example(example_file, 'ddd')
            all_valid = all_valid and valid

    # Legacy example
    legacy_example = ddd_path / 'ddd-schema-example.yaml'
    if legacy_example.exists():
        valid = validate_example(legacy_example, 'ddd')
        all_valid = all_valid and valid

    return 0 if all_valid else 1

if __name__ == '__main__':
    sys.exit(main())
```

**Testing**:
```bash
python tools/validate-example-v2.py

# Should validate:
# ✓ strategic-example.yaml
# ✓ tactical-example.yaml
# ✓ ddd-schema-example.yaml (legacy)
```

---

## Phase 3: Testing and Validation

**Goal**: Ensure all functionality preserved
**Duration**: 0.5 days
**Risk**: Low (verification phase)

### Step 3.1: Create Test Checklist

```markdown
## Schema Loading Tests

- [ ] Legacy single-file schemas still load (data-eng, ux, qe)
- [ ] Partitioned DDD schemas load correctly
- [ ] Both strategic and tactical schemas discovered
- [ ] All concepts found across partitions

## Validation Tests

- [ ] validate-schemas.py runs without errors
- [ ] Closure percentages unchanged (or improved)
- [ ] validate-grounding-references.py finds all concepts
- [ ] All existing groundings still valid
- [ ] validate-schema-docs-alignment.py works
- [ ] All docs still aligned to concepts

## Example Validation Tests

- [ ] Strategic example validates against strategic schema
- [ ] Tactical example validates against tactical schema
- [ ] Legacy comprehensive example still validates
- [ ] Cross-partition references work (e.g., bounded_context_ref)

## Backward Compatibility Tests

- [ ] No changes to research-output/interdomain-map.yaml required
- [ ] Grounding paths (e.g., ddd:BoundedContext) still resolve
- [ ] Docs reference concepts by name (no file path changes)
- [ ] External consumers not affected

## Tool Compatibility Tests

- [ ] All 4 validation tools work with partitioned schemas
- [ ] All 4 validation tools still work with legacy schemas
- [ ] Mixed environment (some partitioned, some not) works
```

### Step 3.2: Run Full Validation Suite

```bash
#!/bin/bash
# test-partition-migration.sh

echo "=== Testing Schema Partition Migration ==="

echo -e "\n1. Schema Validation"
python tools/validate-schemas.py || exit 1

echo -e "\n2. Grounding Validation"
python tools/validate-grounding-references.py || exit 1

echo -e "\n3. Schema-Docs Alignment"
python tools/validate-schema-docs-alignment.py || exit 1

echo -e "\n4. Example Validation"
python tools/validate-example-v2.py || exit 1

echo -e "\n✓ All tests passed!"
```

### Step 3.3: Compare Before/After

```bash
# Before partition
git stash  # Save partitioned changes
python tools/validate-schemas.py > before-partition.txt
git stash pop

# After partition
python tools/validate-schemas.py > after-partition.txt

# Compare
diff before-partition.txt after-partition.txt

# Expected: No material differences (closure should be same or better)
```

---

## Phase 4: Documentation and Cleanup

**Goal**: Update documentation, clean up legacy
**Duration**: 0.5 days
**Risk**: Low

### Step 4.1: Update Project README

**File**: `/Users/igor/code/canonical-grounding/README.md`

Add section:
```markdown
## Schema Organization

As of version 1.1, domain models may be partitioned into multiple schema files for better maintainability:

```
domains/{domain}/
  schemas/              # Partitioned schema files (if applicable)
    {category}-{domain}.schema.yaml
  examples/             # Example files
    {category}-example.yaml
  docs/                 # Documentation
  model-schema.yaml     # Legacy monolithic schema (deprecated)
```

### Partitioned Domains

- **DDD**: Strategic patterns + Tactical patterns
- **Agile**: Portfolio + Program + Team + Delivery (planned)

### Single-File Domains

- **Data-Eng**: Single file (< 1000 lines)
- **UX**: Single file (may partition in future)
- **QE**: Single file

## Validation Tools

All validation tools support both partitioned and single-file schemas transparently.
```

### Step 4.2: Create ADR (Architecture Decision Record)

**File**: `docs/adr/003-schema-partitioning.md`

```markdown
# ADR 003: Schema Partitioning Strategy

## Status

Accepted - 2025-10-17

## Context

Large monolithic schema files (>700 lines) create maintenance challenges:
- Difficult to navigate
- Merge conflicts in team collaboration
- Cognitive overload for new contributors
- Harder to reuse specific patterns

The DDD model (771 lines) and Agile model (1,972 lines) are prime candidates.

## Decision

We will partition large domain schemas (>700 lines) into multiple files based on natural domain boundaries:

1. **File Organization**: Use `schemas/` directory with descriptive filenames
2. **Schema Format**: JSON Schema 2020-12 with `$id` declarations
3. **References**: Use string patterns (not $ref) for cross-partition references
4. **Validation**: Python jsonschema 4.x with referencing.Registry
5. **Backward Compatibility**: Keep legacy files during transition

## Consequences

### Positive

- Smaller, focused files easier to understand
- Reduced merge conflicts
- Better reusability
- Scalable pattern for future growth
- Standards-compliant (JSON Schema 2020-12)

### Negative

- More files to manage
- Tool updates required
- Learning curve for contributors
- Temporary duplication during migration

### Neutral

- Grounding references unchanged (concept names stable)
- Documentation unchanged (concept names stable)

## Alternatives Considered

1. **Keep monolithic**: Simple but doesn't scale
2. **Bundle approach**: Requires build step, extra complexity
3. **Nested directories**: Too deep, harder to navigate

## References

- JSON Schema 2020-12 specification
- OpenAPI 3.1 multi-file patterns
- Python jsonschema 4.x documentation
```

### Step 4.3: Update Tool Documentation

**File**: `tools/README.md`

```markdown
# Validation Tools

## Multi-File Schema Support

As of v1.1, all validation tools support both single-file and partitioned schemas.

### Schema Discovery

Tools automatically detect schema organization:

1. Check for `domains/{domain}/schemas/` directory
2. If exists: Load all `*.schema.yaml` files
3. If not: Fall back to `model-schema.yaml` or `model.schema.yaml`

### Example Usage

```bash
# Validates all domains (single-file and partitioned)
python tools/validate-schemas.py

# Validates examples against appropriate schemas
python tools/validate-example-v2.py

# Validates grounding references across partitions
python tools/validate-grounding-references.py
```

### For Tool Developers

When adding new validation tools, use this pattern:

```python
def load_domain_schemas(domain_path: Path) -> List[Dict]:
    """Load schemas (handles partitioning transparently)."""
    schemas = []

    # Try partitioned first
    schemas_dir = domain_path / 'schemas'
    if schemas_dir.exists():
        for file in schemas_dir.glob('*.schema.yaml'):
            schemas.append(yaml.safe_load(open(file)))
    else:
        # Legacy fallback
        for legacy in ['model-schema.yaml', 'model.schema.yaml']:
            if (domain_path / legacy).exists():
                schemas.append(yaml.safe_load(open(domain_path / legacy)))
                break

    return schemas
```
```

### Step 4.4: Tag Release

```bash
git add .
git commit -m "feat(ddd): Partition schema into strategic and tactical

- Split model-schema.yaml into strategic-ddd and tactical-ddd schemas
- Create schemas/ directory structure
- Add partitioned examples
- Update all validation tools for multi-file support
- Maintain backward compatibility with legacy schema
- Add comprehensive documentation

BREAKING CHANGE: None - legacy schema maintained for compatibility
Relates to partition-prompt.md research"

git tag -a v1.1.0 -m "Release 1.1.0: Schema partitioning support"
```

---

## Phase 5: Agile Domain Partition (Apply Pattern)

**Goal**: Apply proven pattern to Agile domain
**Duration**: 1 day
**Risk**: Low (pattern established)

### Step 5.1: Create Agile Partitions

Based on 1,972 lines, split into 4 schemas:

**Portfolio** (`portfolio-agile.schema.yaml`) - ~500 lines:
- Portfolio, ValueStream, StrategicTheme
- Epic, BusinessEpic, EnablerEpic
- OKR, Vision, Roadmap

**Program** (`program-agile.schema.yaml`) - ~600 lines:
- Program, ProgramIncrement, ARTrain
- Feature, CapabilityFeature, EnablerFeature
- ProgramBoard, ProgramBacklog, PIObjective

**Team** (`team-agile.schema.yaml`) - ~700 lines:
- Team, Sprint, Iteration
- Story, UserStory, EnablerStory, TechnicalStory
- Task, Defect, Spike
- TeamBacklog, SprintBoard, Retrospective

**Delivery** (`delivery-agile.schema.yaml`) - ~172 lines:
- Release, Deployment, ReleaseTrain
- Metrics, Velocity, BurndownChart
- DevOpsMetrics, DORA

**Implementation**: Follow same steps as DDD Phase 1

### Step 5.2: Update Agile Examples

Create focused examples:
- `portfolio-example.yaml`
- `program-example.yaml`
- `team-example.yaml`
- `delivery-example.yaml`

### Step 5.3: Validate and Test

Run same test suite as DDD partition

---

## Phase 6: Deprecation and Cleanup (Future)

**Goal**: Remove legacy files after transition period
**Duration**: 0.5 days (in future release)
**Timeline**: Release 2.0 (6-12 months after 1.1)

### Step 6.1: Deprecation Warnings

**Release 1.2** (3 months after 1.1):
- Add deprecation warnings when loading legacy schemas
- Update all documentation to reference partitioned schemas
- Notify users of upcoming removal

```python
def load_domain_schemas(self, domain_name):
    schemas_dir = domain_path / 'schemas'
    if not schemas_dir.exists():
        # Legacy path
        print(f"WARNING: {domain_name} using deprecated single-file schema.")
        print(f"         This will be removed in v2.0")
        print(f"         Please migrate to schemas/ directory structure")
```

### Step 6.2: Remove Legacy Files

**Release 2.0** (6+ months after 1.1):
- Remove all legacy `model-schema.yaml` files
- Remove legacy loading code from tools
- Update all references in documentation

```bash
# Cleanup script
rm domains/ddd/model-schema.yaml
rm domains/agile/model.schema.yaml
# Update tool code to remove legacy paths
```

---

## Migration Checklist

### Pre-Migration

- [ ] Backup all schema files
- [ ] Backup all example files
- [ ] Document current validation results (baseline)
- [ ] Review partition boundaries with team

### DDD Partition (Phase 1)

- [ ] Create `domains/ddd/schemas/` directory
- [ ] Create `domains/ddd/examples/` directory
- [ ] Create `strategic-ddd.schema.yaml`
- [ ] Create `tactical-ddd.schema.yaml`
- [ ] Create `strategic-example.yaml`
- [ ] Create `tactical-example.yaml`
- [ ] Add deprecation notice to legacy schema
- [ ] Create/update `domains/ddd/README.md`

### Tool Updates (Phase 2)

- [ ] Update `validate-schemas.py`
- [ ] Update `validate-grounding-references.py`
- [ ] Update `validate-schema-docs-alignment.py`
- [ ] Create `validate-example-v2.py`
- [ ] Test all tools with DDD partitioned schemas
- [ ] Test all tools with other single-file schemas

### Testing (Phase 3)

- [ ] Run complete test checklist
- [ ] Compare before/after validation results
- [ ] Verify grounding references still work
- [ ] Verify docs alignment still works
- [ ] Test with mixed environment

### Documentation (Phase 4)

- [ ] Update project README
- [ ] Create ADR 003
- [ ] Update tool documentation
- [ ] Update domain-specific documentation
- [ ] Commit and tag release v1.1.0

### Agile Partition (Phase 5)

- [ ] Create Agile schemas directory
- [ ] Create 4 partition files (portfolio, program, team, delivery)
- [ ] Create focused examples
- [ ] Update Agile README
- [ ] Run full test suite
- [ ] Commit changes

---

## Rollback Plan

If issues discovered during migration:

### Immediate Rollback (During Development)

```bash
# Restore from backup
cp domains/ddd/model-schema.yaml.backup domains/ddd/model-schema.yaml

# Remove new directories
rm -rf domains/ddd/schemas
rm -rf domains/ddd/examples

# Revert tool changes
git checkout tools/validate-schemas.py
git checkout tools/validate-grounding-references.py
```

### Post-Release Rollback (After v1.1.0)

```bash
# Revert to v1.0
git revert <commit-hash>

# Or cherry-pick fixes
git cherry-pick <fix-commits>

# Release hotfix v1.1.1
```

**Risk Mitigation**: Keep legacy schemas for minimum 2 releases (6 months)

---

## Success Criteria

### Technical Success

- [ ] All validation tools work with partitioned schemas
- [ ] All validation tools still work with single-file schemas
- [ ] No regressions in validation results
- [ ] Closure percentages unchanged or improved
- [ ] All grounding references resolve correctly

### User Experience Success

- [ ] Schemas easier to navigate (feedback from team)
- [ ] Fewer merge conflicts (measurable in git)
- [ ] Faster onboarding for new contributors
- [ ] Clear documentation for migration

### Maintainability Success

- [ ] File sizes < 800 lines per partition
- [ ] Clear separation of concerns
- [ ] Repeatable pattern for other domains
- [ ] Sustainable long-term

---

## Timeline Summary

| Phase | Duration | Dependencies |
|-------|----------|--------------|
| Phase 1: DDD Partition | 1-2 days | None |
| Phase 2: Tool Updates | 1 day | Phase 1 |
| Phase 3: Testing | 0.5 days | Phase 2 |
| Phase 4: Documentation | 0.5 days | Phase 3 |
| Phase 5: Agile Partition | 1 day | Phase 4 |
| Phase 6: Cleanup | 0.5 days | 6-12 months later |

**Total Initial Implementation**: 4-5 days
**Release**: v1.1.0
**Future Cleanup**: v2.0 (6-12 months later)

---

## Questions and Risks

### Open Questions

1. **Granularity**: Is 2 partitions enough for DDD, or should we split further?
   - **Answer**: Start with 2, can always split further if needed

2. **Validation Strategy**: Validate partitions independently or as bundle?
   - **Answer**: As bundle using Registry (allows cross-partition refs)

3. **Example Strategy**: Focused examples per partition or comprehensive?
   - **Answer**: Both - focused for learning, comprehensive for validation

### Risk Mitigation

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Tool breakage | High | Low | Extensive testing, backward compatibility |
| User confusion | Medium | Medium | Clear documentation, migration guide |
| Performance impact | Low | Low | Minimal - loading multiple files trivial |
| Grounding resolution | High | Low | Keep concept names stable, test thoroughly |

---

## Next Steps

1. **Review this plan** with team
2. **Approve architecture** decision (ADR 003)
3. **Execute Phase 1** (DDD partition)
4. **Execute Phase 2** (tool updates)
5. **Execute Phase 3** (testing)
6. **Execute Phase 4** (documentation)
7. **Release v1.1.0**
8. **Execute Phase 5** (Agile partition)
9. **Monitor feedback** and iterate

---

**Status**: Ready for implementation
**Approver**: [To be assigned]
**Start Date**: TBD
**Target Completion**: TBD
