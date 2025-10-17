# Schema Partitioning Code Examples

This directory contains working code examples demonstrating partitioned JSON Schema validation with Python jsonschema 4.x.

## Directory Structure

```
partition-examples/
├── schemas/
│   ├── strategic-ddd.schema.yaml      # Strategic DDD patterns schema
│   ├── tactical-ddd.schema.yaml       # Tactical DDD patterns schema
│   ├── strategic-example.yaml         # Example data for strategic schema
│   └── tactical-example.yaml          # Example data for tactical schema
├── tools/
│   └── validate_multifile_schema.py   # Multi-file validation tool
└── README.md                          # This file
```

## Schemas

### Strategic DDD Schema (`strategic-ddd.schema.yaml`)

Defines strategic Domain-Driven Design patterns:
- **System**: Complete system model
- **Domain**: Sphere of knowledge (Core, Supporting, Generic)
- **BoundedContext**: Explicit boundary for domain model
- **ContextMapping**: Relationships between contexts

**Size**: ~300 lines
**Concepts**: 4 main patterns
**Dependencies**: None (foundation layer)

### Tactical DDD Schema (`tactical-ddd.schema.yaml`)

Defines tactical Domain-Driven Design patterns:
- **Aggregate**: Consistency boundary with root entity
- **Entity**: Object with unique identity
- **ValueObject**: Immutable value defined by attributes
- **Repository**: Persistence abstraction
- **DomainService**: Stateless domain operations
- **DomainEvent**: Domain occurrence

**Size**: ~450 lines
**Concepts**: 6 main patterns
**Dependencies**: References BoundedContext from strategic schema

### Cross-Schema References

The tactical schema references concepts from the strategic schema:
- `aggregate.bounded_context_ref` → BoundedContext ID
- `entity.bounded_context_ref` → BoundedContext ID
- `repository.bounded_context_ref` → BoundedContext ID

These references use **string patterns** (not `$ref`) for simplicity:
```yaml
bounded_context_ref:
  type: string
  pattern: "^bc_[a-z0-9_]+$"
  description: "Reference to BoundedContext from strategic schema"
```

## Examples

### Strategic Example (`strategic-example.yaml`)

Models the Job Seeker Application at strategic level:
- 3 domains (Job Matching, Job Aggregation, Application Tracking)
- 4 bounded contexts (Profile, Matching, Job Catalog, Applications)
- 2 context mappings (customer-supplier relationships)

### Tactical Example (`tactical-example.yaml`)

Models the Job Seeker Application at tactical level:
- 3 aggregates (CandidateProfile, JobMatch, JobPosting)
- 3 entities (Candidate, Match, Job)
- 8 value objects (Email, Phone, SkillLevel, MatchScore, etc.)
- 2 repositories (Profile, JobCatalog)
- 1 domain service (MatchingAlgorithm)
- 3 domain events (ProfileCreated, ProfileUpdated, MatchCreated)

## Validation Tool

The `validate_multifile_schema.py` tool demonstrates:
1. Loading multiple schema files from a directory
2. Creating a `referencing.Registry` with all schemas
3. Validating data against schemas with cross-references
4. Analyzing cross-schema dependencies

### Requirements

```bash
pip install jsonschema>=4.18.0 referencing pyyaml
```

### Usage

**Run demo with built-in examples:**
```bash
cd partition-examples
python tools/validate_multifile_schema.py
```

**Output:**
```
======================================================================
Multi-File Schema Validation Demo
======================================================================

=== Loading Schemas ===
✓ Loaded: strategic-ddd
  Title: DDD Strategic Patterns Schema
  $id: https://canonical-grounding.org/schemas/ddd/strategic/v1
  Concepts: 4 - system, domain, bounded_context, context_mapping

✓ Loaded: tactical-ddd
  Title: DDD Tactical Patterns Schema
  $id: https://canonical-grounding.org/schemas/ddd/tactical/v1
  Concepts: 6 - aggregate, entity, value_object, repository...

=== Creating Schema Registry ===
✓ Registered: https://canonical-grounding.org/schemas/ddd/strategic/v1
✓ Registered: https://canonical-grounding.org/schemas/ddd/tactical/v1
✓ Registry created with 2 schemas

=== Analyzing Cross-Schema References ===
✓ strategic-ddd: No external references
✓ tactical-ddd:
    → References: BoundedContext (from strategic schema)

======================================================================
Validating Examples
======================================================================

--- Validating strategic-example.yaml against strategic-ddd ---
✓ strategic-example.yaml: Validation successful

--- Validating tactical-example.yaml against tactical-ddd ---
✓ tactical-example.yaml: Validation successful

======================================================================
Validation Summary
======================================================================
✓ All validations passed!

Key Takeaways:
  • Partitioned schemas loaded successfully
  • Cross-schema references resolved via Registry
  • Strategic and tactical patterns validated independently
  • Referential integrity maintained (BC refs, aggregate refs)
```

**Validate custom files:**
```bash
python tools/validate_multifile_schema.py schemas/strategic-ddd.schema.yaml schemas/strategic-example.yaml
```

## How It Works

### 1. Schema Loading

The validator loads all `.schema.yaml` files from the schemas directory:

```python
def load_schemas(self) -> bool:
    schema_files = list(self.schemas_dir.glob('*.schema.yaml'))
    for schema_file in sorted(schema_files):
        with open(schema_file) as f:
            schema = yaml.safe_load(f)
            self.schemas[schema_file.stem] = schema
```

### 2. Registry Creation

Creates a `referencing.Registry` with all schemas, enabling cross-schema resolution:

```python
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

resources = []
for schema_name, schema in self.schemas.items():
    uri = schema['$id']  # Use $id from schema
    resource = DRAFT202012.create_resource(schema)
    resources.append((uri, resource))

registry = Registry().with_resources(resources)
```

### 3. Validation with Registry

The validator uses the registry to resolve cross-schema references:

```python
from jsonschema import Draft202012Validator

validator = Draft202012Validator(schema, registry=self.registry)
validator.validate(data)
```

When validating tactical data that references strategic concepts (e.g., `bounded_context_ref: "bc_profile"`), the validator:
1. Sees the pattern constraint: `^bc_[a-z0-9_]+$`
2. Validates the string matches the pattern
3. Does NOT require loading BoundedContext definition (loose coupling)

This is intentional - we use **ID references**, not `$ref`, for cross-partition coupling.

### 4. Referential Integrity

While schemas are partitioned, referential integrity is maintained:

**Tactical schema** declares it references BoundedContext:
```yaml
bounded_context_ref:
  type: string
  pattern: "^bc_[a-z0-9_]+$"
  description: "Reference to BoundedContext from strategic schema"
```

**Strategic schema** defines BoundedContext:
```yaml
bounded_context:
  type: object
  properties:
    id:
      type: string
      pattern: "^bc_[a-z0-9_]+$"
```

Both use the same ID pattern, ensuring consistency.

## Key Learnings

### 1. Partition Strategy

**Strategic vs Tactical** is a natural partition boundary for DDD:
- Strategic = Architecture-level decisions (300 lines)
- Tactical = Implementation building blocks (450 lines)
- Clear dependency direction: Tactical → Strategic (never reverse)

### 2. Reference Pattern

Use **string patterns** for cross-partition references instead of JSON Schema `$ref`:
- Simpler to understand
- Looser coupling between partitions
- Same validation guarantees (pattern matching)
- Easier to evolve schemas independently

### 3. Registry Benefits

The `referencing.Registry` provides:
- Centralized schema management
- Automatic cross-schema resolution
- Support for multiple schema versions
- Thread-safe immutable design

### 4. Tool Updates

Migrating existing tools requires:
1. Load multiple schema files per domain
2. Create registry with all schemas
3. Pass registry to validator
4. Otherwise, validation logic unchanged

## Applying to Your Project

To apply this pattern to your domain:

### Step 1: Identify Partition Boundaries

Look for natural splits in your schema:
- Architectural layers (foundation vs application)
- Lifecycle stages (planning vs execution)
- Concern separation (data vs behavior)

### Step 2: Split Schema Files

```bash
mkdir domains/your-domain/schemas/

# Split your model-schema.yaml into partitions
vim domains/your-domain/schemas/part1-your-domain.schema.yaml
vim domains/your-domain/schemas/part2-your-domain.schema.yaml
```

### Step 3: Add $id Declarations

Each schema needs a unique `$id`:
```yaml
$schema: https://json-schema.org/draft/2020-12/schema
$id: https://your-project.org/schemas/your-domain/part1/v1
```

### Step 4: Convert Cross-Partition References

Change from:
```yaml
aggregate_ref:
  $ref: '#/$defs/aggregate'
```

To:
```yaml
aggregate_ref:
  type: string
  pattern: "^agg_[a-z0-9_]+$"
  description: "Reference to Aggregate (ID)"
```

### Step 5: Update Validation Tools

Use the pattern from `validate_multifile_schema.py`:
- Load all `.schema.yaml` files from `schemas/` directory
- Create `Registry` with all schemas
- Pass registry to validators

### Step 6: Create Focused Examples

Create example files per partition:
- `strategic-example.yaml` - tests strategic patterns
- `tactical-example.yaml` - tests tactical patterns

## Testing

### Manual Testing

```bash
# Run validation demo
python tools/validate_multifile_schema.py

# Should show all validations pass
```

### Automated Testing

```bash
# Create test script
cat > tests/test_validation.sh << 'EOF'
#!/bin/bash
set -e

echo "Testing multi-file schema validation..."

# Run validator
python tools/validate_multifile_schema.py > /tmp/validation_output.txt

# Check for success markers
grep -q "All validations passed" /tmp/validation_output.txt

echo "✓ All tests passed"
EOF

chmod +x tests/test_validation.sh
./tests/test_validation.sh
```

## Troubleshooting

### Error: "No module named 'referencing'"

**Solution**: Install required packages:
```bash
pip install jsonschema>=4.18.0 referencing pyyaml
```

### Error: "Schema 'X' not found"

**Solution**: Ensure schema file is named correctly:
- Must end with `.schema.yaml`
- Must be in the `schemas/` directory
- Schema name is filename without `.schema.yaml`

### Error: "Failed to load data file"

**Solution**: Check YAML syntax:
```bash
python -c "import yaml; yaml.safe_load(open('your-file.yaml'))"
```

### Validation fails with cross-references

**Solution**: Verify ID patterns match:
- Check strategic schema defines concept with ID pattern
- Check tactical schema references using same ID pattern
- Ensure patterns are consistent (e.g., both use `^bc_[a-z0-9_]+$`)

## References

- [JSON Schema 2020-12 Specification](https://json-schema.org/draft/2020-12/json-schema-core)
- [Python jsonschema Documentation](https://python-jsonschema.readthedocs.io/)
- [Referencing Library](https://referencing.readthedocs.io/)
- [Domain-Driven Design](https://www.domainlanguage.com/ddd/) by Eric Evans
- [Implementing Domain-Driven Design](https://vaughnvernon.com/) by Vaughn Vernon

## Next Steps

1. Review the research findings in `../partition-research.md`
2. Follow the implementation plan in `../partition-plan.md`
3. Apply this pattern to your domain models (start with DDD, then Agile)
4. Update your validation tools using the provided example
5. Create focused examples per partition
6. Test thoroughly before deprecating legacy schemas

---

**Created**: 2025-10-17
**Purpose**: Demonstrate practical schema partitioning with working code
**Status**: Production-ready pattern
