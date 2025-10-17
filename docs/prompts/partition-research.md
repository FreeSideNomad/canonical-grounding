# Schema Partitioning Research: Comprehensive Analysis

**Date**: 2025-10-17
**Version**: 1.0
**Purpose**: Research findings on partitioning large YAML/JSON Schema files while maintaining validation and referential integrity

---

## Executive Summary

This document presents comprehensive research on best practices for partitioning large JSON Schema/YAML schema files. Based on analysis of industry patterns from Kubernetes, OpenAPI, and JSON Schema communities, combined with evaluation of this project's specific needs, we recommend a **hybrid bundling approach** with external references for DDD and Agile domain models.

### Key Findings

1. **JSON Schema 2020-12** fully supports external file references via `$ref` with proper `$id` declarations
2. **Python jsonschema 4.x** requires `referencing.Registry` for multi-file validation (replaces deprecated `RefResolver`)
3. **Industry consensus**: Keep schemas modular during development, bundle for distribution
4. **Optimal partition size**: 300-500 lines per file for maintainability
5. **Strategic vs Tactical separation** is a natural boundary for DDD partitioning

---

## Research Question 1: Schema Partitioning Strategies

### Industry Best Practices

#### A. JSON Schema 2020-12 Specification Approach

**Core Principles**:
- Use `$id` keyword for schema identification (not file paths)
- External references via `$ref` with URI format: `"$ref": "./other-schema.yaml#/$defs/ConceptName"`
- Avoid runtime resolution over HTTP - bundle at build time
- Internal-first lookup: schemas check their own `$defs` before external resolution

**Example from JSON Schema Docs**:
```yaml
# base-schema.yaml
$schema: https://json-schema.org/draft/2020-12/schema
$id: https://example.com/schemas/base
$defs:
  address:
    type: object
    properties:
      street: { type: string }
      city: { type: string }

# person-schema.yaml
$schema: https://json-schema.org/draft/2020-12/schema
$id: https://example.com/schemas/person
type: object
properties:
  name: { type: string }
  address:
    $ref: "https://example.com/schemas/base#/$defs/address"
```

**Pros**:
- Standards-compliant
- Clear schema boundaries
- Reusable across projects

**Cons**:
- Requires HTTP-style URIs (can use file:// but not portable)
- Need registry/store for validation
- More complex tooling

#### B. OpenAPI 3.1 Multi-File Pattern

**Organization Strategy**:
```
schemas/
  components/
    schemas/
      User.yaml
      Address.yaml
      Order.yaml
    parameters/
      pagination.yaml
  paths/
    users.yaml
    orders.yaml
  openapi.yaml  # Main file that references all others
```

**Reference Pattern**:
```yaml
# openapi.yaml
components:
  schemas:
    User:
      $ref: './components/schemas/User.yaml'

# paths/users.yaml
get:
  responses:
    '200':
      content:
        application/json:
          schema:
            $ref: '../components/schemas/User.yaml'
```

**Pros**:
- Excellent developer experience
- Clear separation of concerns
- Git-friendly (fewer merge conflicts)
- Easy to navigate

**Cons**:
- Requires bundling tool for distribution
- Relative path management can be tricky
- Some tools require single-file input

**Real-World Example**: Kubernetes API uses this pattern extensively, with ~600 CRD schemas split across multiple files, then bundled for distribution.

#### C. Schema Bundling Approach (Recommended)

**Development Structure**:
```
domains/ddd/
  schemas/
    strategic-ddd.schema.yaml   # Strategic patterns
    tactical-ddd.schema.yaml    # Tactical patterns
  examples/
    strategic-example.yaml
    tactical-example.yaml
```

**Distribution**: Bundle into single file for validation, or use Registry with both schemas loaded.

**Pros**:
- Best of both worlds
- Maintain modularity during development
- Single artifact for validation
- Compatible with existing tools

**Cons**:
- Need bundling step (can be automated)
- Two versions to maintain (dev vs bundled)

### Recommended Strategy for This Project

**Choice**: **Hybrid Bundling Approach** with external references

**Rationale**:
1. DDD schema (771 lines) naturally splits into Strategic (300 lines) and Tactical (450 lines)
2. Agile schema (1972 lines) benefits from 3-way split: Portfolio/Program, Team/Sprint, Work Items
3. Python jsonschema 4.x natively supports multi-file with Registry
4. No distribution requirement - schemas used internally only
5. Maintains backward compatibility via naming convention

---

## Research Question 2: Referential Integrity Maintenance

### Cross-File Reference Resolution

#### How `$ref` Works Across Files

**JSON Schema Resolution Process**:
1. Parser encounters `$ref` keyword
2. Checks if referenced URI matches any schema's `$id` in current document
3. If not found internally, looks up in provided Registry/Store
4. Resolves JSON Pointer fragment (e.g., `#/$defs/BoundedContext`)
5. Validates data against resolved schema

**Key Insight**: The `$id` value is what matters for resolution, not the file path. File paths are for human convenience during development.

#### Python jsonschema Library Resolution

**Modern Approach (v4.18.0+)**: Use `referencing.Registry`

```python
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012
from jsonschema import Draft202012Validator
import yaml

# Load schemas
with open('strategic-ddd.schema.yaml') as f:
    strategic = yaml.safe_load(f)

with open('tactical-ddd.schema.yaml') as f:
    tactical = yaml.safe_load(f)

# Create registry with both schemas
registry = Registry().with_resources([
    (strategic['$id'], DRAFT202012.create_resource(strategic)),
    (tactical['$id'], DRAFT202012.create_resource(tactical)),
])

# Validate using schema that references another
validator = Draft202012Validator(tactical, registry=registry)
validator.validate(data)
```

**Legacy Approach** (pre v4.18.0): RefResolver with schema store

```python
import jsonschema

schema_store = {
    strategic['$id']: strategic,
    tactical['$id']: tactical,
}

resolver = jsonschema.RefResolver.from_schema(
    tactical,
    store=schema_store
)

validator = jsonschema.Draft7Validator(tactical, resolver=resolver)
validator.validate(data)
```

### Maintaining Cross-Domain Grounding References

**Current System**: `research-output/interdomain-map.yaml` contains groundings like:
```yaml
groundings:
  - id: grounding_ux_to_ddd_001
    source: model_ux
    target: model_ddd
    relationships:
      - source_concept: Page
        target_concept: BoundedContext
        relationship_type: implements
```

**Impact of Partitioning**:
- Grounding references point to **concept names**, not file locations
- As long as concept names remain unchanged, groundings remain valid
- Validation tools need to search across multiple schema files

**Solution**: Update validation tools to load all partition files for each domain:

```python
def load_domain_schema(domain_name):
    """Load all schema partitions for a domain."""
    domain_path = base_path / 'domains' / domain_name
    schemas = {}

    # Check for partitioned schemas
    if (domain_path / 'schemas').exists():
        for schema_file in (domain_path / 'schemas').glob('*.schema.yaml'):
            with open(schema_file) as f:
                schema = yaml.safe_load(f)
                schemas[schema_file.stem] = schema
    else:
        # Legacy single-file schema
        schema_path = domain_path / 'model-schema.yaml'
        with open(schema_path) as f:
            schemas['main'] = yaml.safe_load(f)

    return schemas
```

### Circular Dependency Prevention

**Risk**: Tactical patterns reference Strategic patterns, but Strategic should NOT reference Tactical.

**Pattern**: Establish clear dependency layers:
```
Layer 1 (Foundation): Strategic DDD patterns - no external deps
Layer 2 (Tactical): Tactical DDD patterns - references Layer 1
Layer 3 (Application): Specific implementations - references Layer 1 & 2
```

**Validation**: Add circular dependency check to validation tool:
```python
def check_circular_references(schemas):
    """Ensure no circular dependencies between schema files."""
    graph = build_dependency_graph(schemas)
    return not has_cycle(graph)  # DFS-based cycle detection
```

---

## Research Question 3: File Organization Patterns

### Evaluation of Options

#### Option A: Flat with Prefixes (Simple)

```
domains/ddd/
  strategic-ddd-schema.yaml
  tactical-ddd-schema.yaml
  strategic-ddd-example.yaml
  tactical-ddd-example.yaml
  model-schema.yaml  # Legacy - keep during migration
```

**Pros**:
- Simple, flat structure
- Easy to discover files
- Minimal tooling changes

**Cons**:
- All files at same level
- Naming convention critical
- Can get cluttered with many partitions

**Score**: 8/10 - Best for 2-3 partitions

#### Option B: Nested by Concern (Organized)

```
domains/ddd/
  strategic/
    schema.yaml
    example.yaml
    docs/
      domain.md
      bounded-context.md
  tactical/
    schema.yaml
    example.yaml
    docs/
      aggregate.md
      entity.md
  model-schema.yaml  # Legacy
```

**Pros**:
- Clear separation
- Co-locate related docs
- Scales to many partitions

**Cons**:
- Deeper nesting
- Relative path complexity
- More tooling changes

**Score**: 7/10 - Best for many partitions (4+)

#### Option C: Schema Bundler Approach (Flexible)

```
domains/ddd/
  schemas/
    strategic-ddd.schema.yaml
    tactical-ddd.schema.yaml
    index.yaml  # Optional: combines all schemas
  examples/
    strategic-example.yaml
    tactical-example.yaml
  docs/  # Existing docs unchanged
  model-schema.yaml  # Legacy
```

**Pros**:
- Clear intent (schemas/ directory)
- Examples grouped separately
- Existing docs/ unchanged
- Easy to add bundling script

**Cons**:
- Adds one level of nesting
- Need to update tool paths

**Score**: 9/10 - Best balance (RECOMMENDED)

### Recommended: Option C with Enhancements

```
domains/ddd/
  schemas/
    strategic-ddd.schema.yaml      # Strategic patterns
    tactical-ddd.schema.yaml       # Tactical patterns
    # Future: events-ddd.schema.yaml, integration-ddd.schema.yaml
  examples/
    strategic-example.yaml
    tactical-example.yaml
    # Or: job-seeker-example.yaml (comprehensive)
  docs/                            # Unchanged
    bounded-context.md
    aggregate.md
    ...
  model-schema.yaml                # Legacy - deprecate after migration
  README.md                        # Update with partition info
```

**Migration Path**:
1. Create `schemas/` directory
2. Split current `model-schema.yaml` into partitions
3. Create examples in `examples/` directory
4. Keep legacy `model-schema.yaml` for 1 release
5. Update all tools to check `schemas/` first, fall back to legacy
6. Remove legacy file after validation

---

## Research Question 4: Validation Tool Updates

### Tool Inventory and Required Changes

#### 1. `tools/validate-schemas.py` (MAJOR UPDATE)

**Current Behavior**: Loads single `model-schema.yaml` per domain

**Required Changes**:
```python
class SchemaValidator:
    def load_schemas(self) -> bool:
        """Load all canonical domain model schemas."""
        for canon in ["ddd", "data-eng", "ux", "qe", "agile"]:
            schemas = self.load_domain_schemas(canon)
            self.canon_schemas[canon] = schemas

    def load_domain_schemas(self, domain_name):
        """Load all schema files for a domain (supports partitioning)."""
        domain_path = self.domains_path / domain_name
        schemas = []

        # Check for partitioned schemas
        schemas_dir = domain_path / 'schemas'
        if schemas_dir.exists():
            # Load all .schema.yaml files
            for schema_file in sorted(schemas_dir.glob('*.schema.yaml')):
                with open(schema_file) as f:
                    schema = yaml.safe_load(f)
                    schema['_source_file'] = str(schema_file)
                    schemas.append(schema)
        else:
            # Legacy single file
            legacy_paths = [
                domain_path / 'model-schema.yaml',
                domain_path / 'model.schema.yaml'
            ]
            for path in legacy_paths:
                if path.exists():
                    with open(path) as f:
                        schema = yaml.safe_load(f)
                        schema['_source_file'] = str(path)
                        schemas.append(schema)
                    break

        return schemas

    def extract_references(self, schemas, canon):
        """Extract refs from multiple schema files."""
        all_refs = set()
        for schema in schemas:
            refs = self._extract_from_schema(schema, canon)
            all_refs.update(refs)
        return all_refs

    def create_registry(self, schemas):
        """Create referencing.Registry for multi-file validation."""
        from referencing import Registry, Resource
        from referencing.jsonschema import DRAFT202012

        resources = []
        for schema in schemas:
            if '$id' in schema:
                resource = DRAFT202012.create_resource(schema)
                resources.append((schema['$id'], resource))

        return Registry().with_resources(resources)
```

**Testing Strategy**:
- Test with single-file schemas (legacy)
- Test with partitioned schemas (new)
- Test with mixed (some partitioned, some not)
- Verify all existing validations still pass

#### 2. `tools/validate-grounding-references.py` (MINOR UPDATE)

**Current Behavior**: Loads schema and extracts $defs concepts

**Required Changes**:
```python
def load_schema_concepts(domain_path: Path) -> Dict[str, str]:
    """Load all $defs concepts from a domain (handles partitioning)."""
    concepts = {}

    # Check for partitioned schemas
    schemas_dir = domain_path / 'schemas'
    if schemas_dir.exists():
        # Load from all partition files
        for schema_file in schemas_dir.glob('*.schema.yaml'):
            concepts.update(_load_concepts_from_file(schema_file))
    else:
        # Legacy single file
        schema_file = domain_path / 'model-schema.yaml'
        if schema_file.exists():
            concepts.update(_load_concepts_from_file(schema_file))

    return concepts

def _load_concepts_from_file(schema_path: Path) -> Dict[str, str]:
    """Extract concepts from a single schema file."""
    concepts = {}
    with open(schema_path) as f:
        for doc in yaml.safe_load_all(f):
            if doc and isinstance(doc, dict) and '$defs' in doc:
                for concept_name in doc['$defs'].keys():
                    concepts[concept_name.lower()] = concept_name
    return concepts
```

**Impact**: Minimal - just extend to search multiple files per domain

#### 3. `tools/validate-schema-docs-alignment.py` (MINOR UPDATE)

**Current Behavior**: Checks if schema concepts have matching docs

**Required Changes**:
- Extend to load concepts from all partition files
- Same pattern as grounding validation

**Change Type**: Same as #2 above

#### 4. `tools/validate-example.py` (MODERATE UPDATE)

**Current Behavior**: Validates examples against single schema

**Required Changes**:
```python
def validate_example_against_schema(example_file, domain_name):
    """Validate example against domain schema(s)."""
    domain_path = Path(f'domains/{domain_name}')

    # Load all schemas for domain
    schemas = load_domain_schemas(domain_path)

    # Create registry for cross-schema references
    registry = create_registry(schemas)

    # Determine which schema to validate against
    # Strategy 1: Try each schema until one validates
    # Strategy 2: Use example filename hint (strategic-example.yaml -> strategic schema)
    # Strategy 3: Validate against all schemas (if example is comprehensive)

    example_name = example_file.stem

    if 'strategic' in example_name:
        schema = find_schema_by_id(schemas, 'strategic')
    elif 'tactical' in example_name:
        schema = find_schema_by_id(schemas, 'tactical')
    else:
        # Try all schemas, return first successful validation
        schema = schemas[0]  # Default to first

    validator = Draft202012Validator(schema, registry=registry)
    validator.validate(example_data)
```

**Testing**: Validate strategic examples only against strategic schema, tactical against tactical

---

## Research Question 5: Backward Compatibility

### Compatibility Strategies

#### A. Parallel Schemas (Recommended)

**Approach**: Keep both old and new during transition

```
domains/ddd/
  schemas/                    # NEW
    strategic-ddd.schema.yaml
    tactical-ddd.schema.yaml
  model-schema.yaml          # OLD - keep for 1-2 releases
```

**Tool Behavior**:
```python
# Check new location first, fall back to old
schemas_dir = domain_path / 'schemas'
if schemas_dir.exists():
    schemas = load_from_partitions(schemas_dir)
else:
    schemas = [load_legacy(domain_path / 'model-schema.yaml')]
```

**Migration Timeline**:
- **Release 1.0** (Current): Single-file schemas
- **Release 1.1** (Transition): Add partitioned schemas, keep legacy, update tools
- **Release 1.2** (Deprecation): Mark legacy as deprecated, warn on use
- **Release 2.0** (Clean): Remove legacy files

**Pros**:
- Zero breaking changes during transition
- Users can migrate at their own pace
- Easy rollback if issues found

**Cons**:
- Temporary duplication
- Must keep both in sync during transition

#### B. Grounding Reference Paths

**Question**: Do paths change from `ddd:BoundedContext` to `ddd:strategic:BoundedContext`?

**Answer**: NO - Keep concept names stable

**Rationale**:
- Grounding references use concept names, not file locations
- `BoundedContext` is unique within DDD domain
- File organization is implementation detail

**Validation Logic**:
```python
def resolve_grounding_reference(ref_string):
    """Resolve 'ddd:BoundedContext' to schema location."""
    domain, concept = ref_string.split(':')

    # Search all schema partitions for this domain
    schemas = load_domain_schemas(domain)

    for schema in schemas:
        if '$defs' in schema and concept in schema['$defs']:
            return schema['$defs'][concept]

    raise ValueError(f"Concept {concept} not found in domain {domain}")
```

**No Changes Required** to `research-output/interdomain-map.yaml`!

#### C. Documentation References

**Current**: Docs reference concepts by name (e.g., "BoundedContext")

**Impact**: NONE - concept names unchanged

**Update Required**: README.md to explain new file structure:

```markdown
# DDD Domain Model

This domain model is organized into:

- **Strategic Patterns** (`schemas/strategic-ddd.schema.yaml`):
  Domain, BoundedContext, ContextMapping, UbiquitousLanguage

- **Tactical Patterns** (`schemas/tactical-ddd.schema.yaml`):
  Aggregate, Entity, ValueObject, Repository, DomainService,
  DomainEvent, Factory, Specification

See individual concept documentation in `docs/` directory.
```

### Testing Strategy for Compatibility

**Test Suite**:
1. **Validation Continuity**: All existing examples still validate
2. **Grounding Resolution**: All groundings still resolve correctly
3. **Tool Compatibility**: All tools work with both legacy and partitioned schemas
4. **Cross-Domain References**: UX→DDD, QE→DDD references still work
5. **Closure Calculation**: Closure percentages unchanged (or improved)

**Regression Test**:
```bash
# Before migration
python tools/validate-schemas.py > before.txt

# After migration (with parallel schemas)
python tools/validate-schemas.py > after.txt

# Should be identical (or better)
diff before.txt after.txt
```

---

## Research Question 6: Other Domain Models

### Line Count Analysis

| Domain | File | Lines | Status |
|--------|------|-------|--------|
| Agile | model.schema.yaml | 1,972 | **HIGH PRIORITY** - Partition |
| UX | model-schema.yaml | 1,141 | **MEDIUM PRIORITY** - Consider partition |
| QE | model-schema.yaml | 984 | **LOW PRIORITY** - Manageable |
| Data-Eng | model.schema.yaml | 903 | **LOW PRIORITY** - Manageable |
| DDD | model-schema.yaml | 771 | **HIGH PRIORITY** - Partition (proof of concept) |

### Size Threshold Recommendation

**Rule of Thumb**: Partition schemas **> 700 lines**

**Rationale**:
- 700+ lines: Difficult to navigate in single screen
- Cognitive load increases significantly above 500 lines
- Git diffs become unwieldy
- Merge conflicts more likely

**Guideline**:
- **< 500 lines**: Single file is fine
- **500-800 lines**: Consider partition if natural boundaries exist
- **> 800 lines**: Strong candidate for partition

### Agile Domain Partition Strategy

**Current Size**: 1,972 lines - LARGEST schema

**Natural Partition Boundaries**:

**Option 1: By SAFe Level** (Recommended)
```
schemas/
  portfolio-agile.schema.yaml  # ~500 lines
    - Portfolio, ValueStream, StrategicTheme
    - Epic, BusinessEpic, EnablerEpic

  program-agile.schema.yaml    # ~600 lines
    - Program, ProgramIncrement, ARTrain
    - Feature, CapabilityFeature, EnablerFeature
    - ProgramBoard, ProgramBacklog

  team-agile.schema.yaml       # ~700 lines
    - Team, Sprint/Iteration
    - Story, UserStory, EnablerStory
    - Task, Defect
    - TeamBacklog, SprintBoard

  delivery-agile.schema.yaml   # ~170 lines
    - Release, Deployment
    - Metrics, Velocity
```

**Dependencies**:
- Portfolio → (no deps)
- Program → Portfolio (for Value Stream refs)
- Team → Program (for Feature refs)
- Delivery → Team (for Sprint refs)

**Option 2: By Artifact Type** (Alternative)
```
schemas/
  planning-agile.schema.yaml   # Vision, Roadmap, Backlog, Planning
  work-items-agile.schema.yaml # Epic, Feature, Story, Task, Defect
  execution-agile.schema.yaml  # Sprint, PI, Release
  team-agile.schema.yaml       # Team, ART, Roles
```

**Recommendation**: Use **Option 1 (By SAFe Level)** - aligns with how practitioners think about Agile

### UX Domain Partition Strategy

**Current Size**: 1,141 lines - BORDERLINE

**Natural Partition Boundaries**:

**Option: Split if it grows further**
```
schemas/
  information-architecture-ux.schema.yaml  # ~400 lines
    - InformationArchitecture, Navigation, Sitemap

  interaction-ux.schema.yaml              # ~500 lines
    - Workflow, InteractionPattern, Page

  components-ux.schema.yaml               # ~250 lines
    - Component, Pattern, UIElement
```

**Current Recommendation**: Keep single file for now, prepare partition strategy for future

### Data-Eng and QE Domains

**Current Size**: 903 and 984 lines respectively

**Recommendation**: Keep as single files - manageable size

**Monitor**: If either exceeds 1,000 lines, consider partition

---

## Generalizable Pattern for Other Domains

### Step-by-Step Partition Guide

**1. Identify Natural Boundaries**
- Architectural layers (strategic vs tactical)
- Lifecycle stages (planning → execution → delivery)
- Concern separation (data vs behavior vs presentation)
- Domain-specific levels (portfolio → program → team)

**2. Analyze Dependencies**
- Which concepts reference which?
- Can you create a clear hierarchy?
- Are there circular dependencies?

**3. Size Balance**
- Target 300-600 lines per partition
- Avoid partitions < 200 lines (too granular)
- Avoid partitions > 800 lines (defeats purpose)

**4. Naming Convention**
```
{category}-{domain}.schema.yaml

Examples:
- strategic-ddd.schema.yaml
- tactical-ddd.schema.yaml
- portfolio-agile.schema.yaml
- program-agile.schema.yaml
```

**5. Create Partitions**
- Add `$id` to each schema
- Use consistent URI scheme: `https://yourproject.com/schemas/{domain}/{category}`
- Add `$ref` for cross-partition references

**6. Update Examples**
- Create focused examples per partition
- Or create comprehensive example that validates against composed schema

**7. Update Tools**
- Extend validation tools to load from `schemas/` directory
- Create Registry with all partitions
- Test thoroughly

**8. Document**
- Update README.md with new structure
- Explain rationale for partitioning
- Show how concepts map to files

---

## Code Examples

### Example 1: Strategic DDD Schema with $refs

```yaml
# domains/ddd/schemas/strategic-ddd.schema.yaml
$schema: https://json-schema.org/draft/2020-12/schema
$id: https://canonical-grounding/schemas/ddd/strategic
title: DDD Strategic Patterns Schema
description: Strategic patterns for Domain-Driven Design

$defs:
  system:
    type: object
    description: The entire software system being modeled
    required: [id, name, domains]
    properties:
      id: { type: string }
      name: { type: string }
      domains:
        type: array
        items:
          $ref: '#/$defs/domain'
      bounded_contexts:
        type: array
        items:
          $ref: '#/$defs/bounded_context'
      context_mappings:
        type: array
        items:
          $ref: '#/$defs/context_mapping'

  domain:
    type: object
    description: A sphere of knowledge and activity
    required: [id, name, type]
    properties:
      id:
        type: string
        pattern: "^dom_[a-z0-9_]+$"
      name: { type: string }
      type:
        type: string
        enum: [core, supporting, generic]
      bounded_contexts:
        type: array
        items:
          $ref: '#/$defs/bounded_context'

  bounded_context:
    type: object
    description: Explicit boundary within which a domain model is defined
    required: [id, name, domain_ref]
    properties:
      id:
        type: string
        pattern: "^bc_[a-z0-9_]+$"
      name: { type: string }
      domain_ref: { type: string }
      ubiquitous_language:
        type: object
        properties:
          glossary:
            type: array
            items:
              type: object
              properties:
                term: { type: string }
                definition: { type: string }
      # Reference to tactical patterns in other file
      aggregates:
        type: array
        description: Aggregates in this context (defined in tactical schema)
        items:
          type: string
          pattern: "^agg_[a-z0-9_]+$"

  context_mapping:
    type: object
    description: Relationship between two bounded contexts
    required: [id, upstream_context, downstream_context, relationship_type]
    properties:
      id:
        type: string
        pattern: "^cm_[a-z0-9_]+_to_[a-z0-9_]+$"
      upstream_context:
        type: string
        pattern: "^bc_[a-z0-9_]+$"
      downstream_context:
        type: string
        pattern: "^bc_[a-z0-9_]+$"
      relationship_type:
        type: string
        enum:
          - partnership
          - shared_kernel
          - customer_supplier
          - conformist
          - anti_corruption_layer
          - open_host_service
```

### Example 2: Tactical DDD Schema with External $ref

```yaml
# domains/ddd/schemas/tactical-ddd.schema.yaml
$schema: https://json-schema.org/draft/2020-12/schema
$id: https://canonical-grounding/schemas/ddd/tactical
title: DDD Tactical Patterns Schema
description: Tactical patterns for Domain-Driven Design

$defs:
  aggregate:
    type: object
    description: Cluster of entities and value objects with consistency boundary
    required: [id, name, bounded_context_ref, root_ref]
    properties:
      id:
        type: string
        pattern: "^agg_[a-z0-9_]+$"
      name: { type: string }
      # References BoundedContext from strategic schema
      bounded_context_ref:
        type: string
        pattern: "^bc_[a-z0-9_]+$"
        description: "Reference to BoundedContext in strategic schema"
      root_ref:
        $ref: '#/$defs/entity'
      entities:
        type: array
        items:
          $ref: '#/$defs/entity'
      value_objects:
        type: array
        items:
          $ref: '#/$defs/value_object'
      invariants:
        type: array
        items: { type: string }

  entity:
    type: object
    description: Object with unique identity and lifecycle
    required: [id, name, bounded_context_ref, identity_field]
    properties:
      id:
        type: string
        pattern: "^ent_[a-z0-9_]+$"
      name: { type: string }
      bounded_context_ref:
        type: string
        pattern: "^bc_[a-z0-9_]+$"
      is_aggregate_root: { type: boolean }
      identity_field: { type: string }
      attributes:
        type: array
        items:
          type: object
          properties:
            name: { type: string }
            type: { type: string }
            required: { type: boolean }

  value_object:
    type: object
    description: Immutable object defined by its attributes
    required: [id, name, bounded_context_ref]
    properties:
      id:
        type: string
        pattern: "^vo_[a-z0-9_]+$"
      name: { type: string }
      bounded_context_ref:
        type: string
        pattern: "^bc_[a-z0-9_]+$"
      attributes:
        type: array
        items:
          type: object
          properties:
            name: { type: string }
            type: { type: string }
      immutability:
        type: boolean
        default: true

  repository:
    type: object
    description: Persistence abstraction for aggregates
    required: [id, name, aggregate_ref]
    properties:
      id:
        type: string
        pattern: "^repo_[a-z0-9_]+$"
      name: { type: string }
      aggregate_ref:
        type: string
        pattern: "^agg_[a-z0-9_]+$"
      interface_methods:
        type: array
        items:
          type: object
          properties:
            name: { type: string }
            query_type:
              type: string
              enum: [by_id, by_criteria, all, custom]

  domain_service:
    type: object
    description: Stateless operation that doesn't belong to an entity
    required: [id, name, bounded_context_ref]
    properties:
      id:
        type: string
        pattern: "^svc_dom_[a-z0-9_]+$"
      name: { type: string }
      bounded_context_ref:
        type: string
        pattern: "^bc_[a-z0-9_]+$"
      operations:
        type: array
        items:
          type: object
          properties:
            name: { type: string }
            parameters: { type: array }
      stateless:
        type: boolean
        default: true
```

### Example 3: Updated Validation Tool

```python
#!/usr/bin/env python3
"""
Multi-file Schema Validation Tool
Supports both legacy single-file and partitioned multi-file schemas.
"""

import yaml
from pathlib import Path
from typing import Dict, List
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012
from jsonschema import Draft202012Validator

class MultiFileSchemaValidator:
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.domains_path = base_path / "domains"
        self.schemas_by_domain = {}
        self.registries_by_domain = {}

    def load_domain_schemas(self, domain_name: str) -> List[Dict]:
        """Load all schema files for a domain (supports partitioning)."""
        domain_path = self.domains_path / domain_name
        schemas = []

        # Try new partitioned structure first
        schemas_dir = domain_path / 'schemas'
        if schemas_dir.exists() and list(schemas_dir.glob('*.schema.yaml')):
            print(f"  Loading partitioned schemas for {domain_name}...")
            for schema_file in sorted(schemas_dir.glob('*.schema.yaml')):
                schemas.append(self._load_schema_file(schema_file))
        else:
            # Fall back to legacy single file
            legacy_files = [
                domain_path / 'model-schema.yaml',
                domain_path / 'model.schema.yaml'
            ]
            for legacy_file in legacy_files:
                if legacy_file.exists():
                    print(f"  Loading legacy schema for {domain_name}...")
                    schemas.append(self._load_schema_file(legacy_file))
                    break

        if not schemas:
            raise FileNotFoundError(f"No schema files found for domain {domain_name}")

        return schemas

    def _load_schema_file(self, schema_path: Path) -> Dict:
        """Load a single schema file."""
        with open(schema_path) as f:
            schema = yaml.safe_load(f)
            schema['_source_file'] = str(schema_path.name)
            return schema

    def create_registry(self, schemas: List[Dict]) -> Registry:
        """Create a referencing Registry for multi-file validation."""
        resources = []

        for schema in schemas:
            if '$id' in schema:
                resource = DRAFT202012.create_resource(schema)
                resources.append((schema['$id'], resource))

        if not resources:
            # No $id declarations - create registry with schemas by filename
            for schema in schemas:
                source_file = schema.get('_source_file', 'unknown')
                resource = DRAFT202012.create_resource(schema)
                # Use file-based URI
                uri = f"file:///{source_file}"
                resources.append((uri, resource))

        return Registry().with_resources(resources)

    def validate_example(self, example_path: Path, domain_name: str) -> bool:
        """Validate an example against domain schema(s)."""
        # Load example data
        with open(example_path) as f:
            example_data = yaml.safe_load(f)

        # Get schemas and registry for this domain
        if domain_name not in self.schemas_by_domain:
            schemas = self.load_domain_schemas(domain_name)
            registry = self.create_registry(schemas)
            self.schemas_by_domain[domain_name] = schemas
            self.registries_by_domain[domain_name] = registry

        schemas = self.schemas_by_domain[domain_name]
        registry = self.registries_by_domain[domain_name]

        # Determine which schema to validate against
        schema = self._select_schema_for_example(example_path, schemas)

        # Validate
        try:
            validator = Draft202012Validator(schema, registry=registry)
            validator.validate(example_data)
            print(f"✓ {example_path.name} is valid")
            return True
        except Exception as e:
            print(f"✗ {example_path.name} validation failed: {e}")
            return False

    def _select_schema_for_example(self, example_path: Path, schemas: List[Dict]) -> Dict:
        """Select appropriate schema based on example filename."""
        example_name = example_path.stem.lower()

        # Try to match by name hint
        for schema in schemas:
            schema_name = schema.get('_source_file', '').lower()
            if 'strategic' in example_name and 'strategic' in schema_name:
                return schema
            if 'tactical' in example_name and 'tactical' in schema_name:
                return schema

        # Default to first schema
        return schemas[0]

    def extract_concepts(self, domain_name: str) -> Dict[str, List[str]]:
        """Extract all concept names from domain schemas."""
        schemas = self.schemas_by_domain.get(domain_name, [])
        concepts_by_file = {}

        for schema in schemas:
            source_file = schema.get('_source_file', 'unknown')
            concepts = []

            if '$defs' in schema:
                concepts = list(schema['$defs'].keys())

            concepts_by_file[source_file] = concepts

        return concepts_by_file

    def validate_all_domains(self) -> bool:
        """Validate all domain schemas."""
        domains = ['ddd', 'agile', 'ux', 'qe', 'data-eng']
        all_valid = True

        print("\n=== Loading Domain Schemas ===")
        for domain in domains:
            try:
                schemas = self.load_domain_schemas(domain)
                registry = self.create_registry(schemas)
                self.schemas_by_domain[domain] = schemas
                self.registries_by_domain[domain] = registry

                print(f"✓ {domain}: loaded {len(schemas)} schema file(s)")

                # Show concepts per file
                concepts = self.extract_concepts(domain)
                for file, concept_list in concepts.items():
                    print(f"    {file}: {len(concept_list)} concepts")

            except Exception as e:
                print(f"✗ {domain}: {e}")
                all_valid = False

        return all_valid


def main():
    base_path = Path(__file__).parent.parent
    validator = MultiFileSchemaValidator(base_path)

    # Validate all domains
    success = validator.validate_all_domains()

    # Validate examples if schemas loaded successfully
    if success:
        print("\n=== Validating Examples ===")
        examples_dir = base_path / 'domains'
        for domain_dir in examples_dir.iterdir():
            if domain_dir.is_dir():
                domain_name = domain_dir.name

                # Check for examples in new location
                examples_path = domain_dir / 'examples'
                if examples_path.exists():
                    for example_file in examples_path.glob('*.yaml'):
                        validator.validate_example(example_file, domain_name)

                # Check for legacy examples
                for example_file in domain_dir.glob('*example*.yaml'):
                    if 'examples' not in str(example_file):
                        validator.validate_example(example_file, domain_name)

    return 0 if success else 1


if __name__ == '__main__':
    import sys
    sys.exit(main())
```

---

## Recommendations Summary

### Immediate Actions (High Priority)

1. **DDD Domain** (771 lines):
   - Split into `strategic-ddd.schema.yaml` (300 lines) and `tactical-ddd.schema.yaml` (450 lines)
   - Add `$id` declarations to both schemas
   - Create `schemas/` directory structure
   - Keep legacy `model-schema.yaml` for 1 release

2. **Agile Domain** (1,972 lines):
   - Split into 4 schemas: portfolio, program, team, delivery
   - Follow same pattern as DDD
   - Biggest immediate impact on maintainability

3. **Update Validation Tools**:
   - Modify `validate-schemas.py` to support `schemas/` directory
   - Update to use `referencing.Registry` (modern jsonschema 4.x API)
   - Add fallback to legacy single-file schemas

### Medium-Term Actions

4. **UX Domain** (1,141 lines):
   - Monitor growth
   - Prepare partition plan
   - Execute if exceeds 1,200 lines

5. **Create Migration Guide**:
   - Document partition process
   - Provide template for other domains
   - Include testing checklist

### Long-Term Actions

6. **Establish Governance**:
   - Size threshold policy: partition at 700+ lines
   - Naming convention enforcement
   - Regular schema reviews

7. **Tooling Enhancements**:
   - Auto-bundling script (if needed for distribution)
   - Schema visualization (show partition relationships)
   - Concept cross-reference generator

---

## Conclusion

Based on comprehensive research of JSON Schema 2020-12, Python jsonschema 4.x, and industry patterns from Kubernetes and OpenAPI projects, we recommend:

1. **Partition strategy**: Hybrid bundling with external references
2. **File organization**: Option C (schemas/ directory with partition files)
3. **Validation approach**: Python jsonschema Registry with all partitions loaded
4. **Backward compatibility**: Parallel schemas during transition
5. **Partition criteria**: Schemas > 700 lines, natural domain boundaries

This approach provides:
- ✅ Improved maintainability (smaller, focused files)
- ✅ Better collaboration (fewer merge conflicts)
- ✅ Preserved referential integrity (Registry resolves cross-file refs)
- ✅ Backward compatibility (legacy files supported during transition)
- ✅ Standards compliance (JSON Schema 2020-12, Python jsonschema 4.x)

The DDD domain partition serves as proof-of-concept, followed by Agile domain, establishing a repeatable pattern for future schema growth.

---

**Next Step**: See `partition-plan.md` for detailed implementation plan.
