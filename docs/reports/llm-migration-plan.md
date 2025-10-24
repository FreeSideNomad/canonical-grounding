# LLM Migration Plan: v1.x to v2.0 (One-Off Execution)

**Date**: 2025-10-24
**Executor**: Claude (LLM)
**Context**: One-time migration of this specific repo only
**Scope**: DDD schemas and examples in canonical-grounding repo

---

## Simplified Context

Since this is:
- ✅ One-off migration (not building reusable tools)
- ✅ Single repo (known structure)
- ✅ LLM-executed (I have Read, Edit, Write tools)
- ✅ No external model files to migrate (just examples)

**Key Simplifications**:
- No need for generic migration scripts
- No need for validator configuration
- Can directly edit files in place
- Focus on correctness over automation
- **Parallel execution where possible** (LLM can make multiple tool calls in single message)

---

## Inventory: What Actually Exists

### Schemas (3 files)
```
/domains/ddd/schemas/strategic-ddd.schema.yaml    (735 lines)
/domains/ddd/schemas/tactical-ddd.schema.yaml     (975 lines)
/domain-stories/domain-stories-schema.yaml        (503 lines)
```

### Examples (4 files)
```
/domains/ddd/examples/strategic-example.yaml
/domains/ddd/examples/tactical-example.yaml
/domains/ddd/examples/bff-example.yaml
/domains/ddd/examples/application-service-example.yaml
```

### Archive Location
```
/docs/examples/partitions/schemas/
  - strategic-ddd.schema.yaml (old copy)
  - tactical-ddd.schema.yaml (old copy)
```

**Total Workload**: 7 files to migrate

---

## Parallel Execution Strategy

### What Can Run in Parallel

**Phase 1 - Reading** (FULLY PARALLEL):
- ✅ Read all 7 files at once (3 schemas + 4 examples)
- Single message with 7 Read tool calls
- Load full context in one shot

**Phase 2 - Schema Migration** (MOSTLY PARALLEL):
- ✅ All 3 schemas are independent - no cross-dependencies for structural changes
- Can migrate strategic, tactical, and domain-stories simultaneously
- Each schema: Extract IDs → Flatten nesting → Add fields
- **Approach**: Read all 3 → Analyze each → Edit all 3 in parallel batches

**Phase 3 - Example Migration** (PARTIALLY PARALLEL):
- ⚠️ Examples have cross-references (need to coordinate IDs)
- ✅ Can read all 4 examples in parallel
- ⚠️ Strategic example independent, but tactical/bff/app-service reference each other
- **Approach**: Migrate strategic first, then tactical + bff + app-service together

**Phase 4 - Validation** (FULLY PARALLEL):
- ✅ Read all migrated files in parallel
- ✅ Check syntax independently
- ⚠️ Cross-reference validation sequential (needs all data)

**Phase 5 - Git Operations** (SEQUENTIAL):
- ❌ Must run sequentially (git add → commit → tag)

### Execution Time Reduction

**Sequential Approach**: ~2-3 days (16-24 hours)
**Parallel Approach**: ~4-6 hours (active work time)

**Time Savings**:
- Phase 1: 30 min → 5 min (read all at once)
- Phase 2: 3-4 hours → 1-2 hours (edit schemas in parallel)
- Phase 3: 2-3 hours → 1 hour (coordinate, but parallelize where possible)
- Phase 4: 2 hours → 30 min (validate in parallel)

**Total Active Time**: 4-6 hours instead of 2-3 days

---

## Phase 1: Preparation (Pre-Migration)

### Task 1.1: Create Backup
- [x] Already have git tag v1.1.0-final (from git status)
- [ ] Create archive directory
- [ ] Copy current schemas to archive

```bash
mkdir -p domains/ddd/schemas/archive/v1.1.0
cp domains/ddd/schemas/strategic-ddd.schema.yaml domains/ddd/schemas/archive/v1.1.0/
cp domains/ddd/schemas/tactical-ddd.schema.yaml domains/ddd/schemas/archive/v1.1.0/
cp domain-stories/domain-stories-schema.yaml domains/ddd/schemas/archive/v1.1.0/
```

### Task 1.2: Read All Current Files (PARALLEL EXECUTION)

**Execute in single message with 7 Read tool calls**:
- [ ] Read strategic-ddd.schema.yaml
- [ ] Read tactical-ddd.schema.yaml
- [ ] Read domain-stories-schema.yaml
- [ ] Read strategic-example.yaml
- [ ] Read tactical-example.yaml
- [ ] Read bff-example.yaml
- [ ] Read application-service-example.yaml

**Purpose**: Load full context in one shot before making changes

**Time**: ~5 minutes (vs 30 min sequential)

### Task 1.3: Create Common Definitions Documentation
- [ ] Create `/schemas/common/common-type-definitions.md`
- [ ] Document all ID types with patterns
- [ ] Document shared types (Parameter, Attribute, Method)
- [ ] Include version numbers (v2.0.0)

**Output**: Single source of truth for documentation

---

## Phase 2: Schema Migration

### Task 2.1: Migrate Strategic Schema

**File**: `/domains/ddd/schemas/strategic-ddd.schema.yaml`

**Steps** (execute in order):

1. **Add metadata section**
   ```yaml
   metadata:
     version: "2.0.0"
     partition: "strategic"
     last_updated: "2025-10-24"
   ```

2. **Add System root object**
   ```yaml
   type: object
   properties:
     system:
       $ref: "#/$defs/System"
   required: [system]
   ```

3. **Extract ID types to $defs section** (create new section at top of $defs)
   - Extract: SysId, DomId, BcId, CmId, BffId, BffIfId
   - Add patterns, descriptions, examples
   - Replace all inline patterns with $ref

4. **Flatten BFF structures** (extract to $defs)
   - Extract: BFFProvides → separate type
   - Extract: BFFEndpoint → separate type
   - Extract: DataTransformation → separate type
   - Replace inline definitions with $refs

5. **Add missing fields**
   - Add `context_mapping.name` (required)
   - Add `context_mapping.description`
   - Keep everything else

6. **Reorganize $defs into three sections**
   ```yaml
   $defs:
     # SECTION 1: ID TYPES
     # SECTION 2: COMMON TYPES
     # SECTION 3: DOMAIN TYPES
   ```

7. **Update System definition to contain domains**
   ```yaml
   System:
     properties:
       domains:
         type: array
         items: { $ref: "#/$defs/Domain" }
   ```

8. **Nest BoundedContext under Domain**
   ```yaml
   Domain:
     properties:
       bounded_contexts:
         type: array
         items: { $ref: "#/$defs/BoundedContext" }
   ```

**Validation**: Read the modified file, check syntax

### Task 2.2: Migrate Tactical Schema

**File**: `/domains/ddd/schemas/tactical-ddd.schema.yaml`

**Steps** (execute in order):

1. **Add metadata section**

2. **Add BoundedContext root object**
   ```yaml
   type: object
   properties:
     bounded_context:
       $ref: "#/$defs/BoundedContext"
   required: [bounded_context]
   ```

3. **Extract ID types to $defs** (top section)
   - Extract: BcId, DomId, AggId, EntId, VoId, RepoId, SvcDomId, SvcAppId, CmdId, QryId, EvtId
   - Add patterns, descriptions, examples
   - Replace all inline patterns with $ref

4. **Extract common types to $defs**
   - Extract: Parameter → separate type
   - Extract: Attribute → separate type
   - Extract: Method → separate type
   - Extract: TransactionBoundary → separate type
   - Extract: WorkflowDefinition → separate type
   - Extract: ApplicationServiceOperation → separate type
   - Extract: CommandRecord → separate type
   - Extract: QueryMethod → separate type
   - Replace all inline definitions with $refs

5. **Restructure BoundedContext as container**
   ```yaml
   BoundedContext:
     type: object
     required: [id, name, domain_ref]
     properties:
       id: { $ref: "#/$defs/BcId" }
       name: string
       domain_ref: { $ref: "#/$defs/DomId" }
       aggregates: { type: array, items: { $ref: "#/$defs/Aggregate" } }
       entities: { type: array, items: { $ref: "#/$defs/Entity" } }
       # ... all other collections
   ```

6. **Remove bounded_context_ref from all child types**
   - Aggregate: remove `bounded_context_ref` property
   - Entity: remove `bounded_context_ref` property
   - ValueObject: remove `bounded_context_ref` property
   - Repository: remove `bounded_context_ref` property
   - (all other types)

7. **Fix immutability enforcement**
   - ValueObject: change `immutability: { type: boolean, default: true }`
     to `immutability: { type: boolean, const: true }`
   - DomainEvent: change `immutable: { type: boolean, default: true }`
     to `immutable: { type: boolean, const: true }`

8. **Add event past tense pattern**
   ```yaml
   DomainEvent:
     properties:
       name:
         pattern: "^[A-Z][a-zA-Z]+(ed|Created|Updated|Deleted|Activated|Deactivated|Approved|Rejected|Completed|Failed|Sent|Received)$"
   ```

9. **Add missing description fields**
   - Aggregate: add `description` property
   - Entity: add `description` property
   - Repository: add `description` property

10. **Add entity behavior requirement**
    ```yaml
    Entity:
      properties:
        business_methods:
          type: array
          minItems: 1
    ```

11. **Reorganize $defs into three sections**
    ```yaml
    $defs:
      # SECTION 1: ID TYPES
      # SECTION 2: COMMON TYPES
      # SECTION 3: DOMAIN TYPES
    ```

**Validation**: Read the modified file, check syntax

### Task 2.3: Migrate Domain Stories Schema

**File**: `/domain-stories/domain-stories-schema.yaml`

**Steps** (execute in order):

1. **Add metadata section**

2. **Keep root object** (already correct - no change)
   ```yaml
   type: object
   properties:
     domain_stories:
       type: array
       items: { $ref: "#/$defs/DomainStory" }
   ```

3. **Update ID types** (already extracted, but standardize)
   - Ensure all tactical ID types present: BcId, AggId, CmdId, QryId, EvtId, SvcAppId
   - Keep story-specific: DstId, ActId, ActvId, PolId, RuleId

4. **Restructure DomainStory to use references**
   ```yaml
   DomainStory:
     properties:
       domain_story_id: { $ref: "#/$defs/DstId" }
       title: string
       description: string

       # NEW: Scope
       bounded_contexts:
         type: array
         items: { $ref: "#/$defs/BcId" }
         minItems: 1

       # NEW: Reference pattern
       aggregates_involved:
         type: array
         items: { $ref: "#/$defs/AggId" }

       commands_invoked:
         type: array
         items: { $ref: "#/$defs/CmdId" }

       queries_executed:
         type: array
         items: { $ref: "#/$defs/QryId" }

       events_published:
         type: array
         items: { $ref: "#/$defs/EvtId" }

       application_services_called:
         type: array
         items: { $ref: "#/$defs/SvcAppId" }

       # NEW: Narrative structure
       narrative:
         type: object
         properties:
           steps:
             type: array
             items: { $ref: "#/$defs/StoryStep" }
   ```

5. **Remove embedded tactical definitions**
   - Remove: Aggregate definition (use AggId reference)
   - Remove: Repository definition
   - Remove: Command definition (use CmdId reference)
   - Remove: Query definition (use QryId reference)
   - Remove: WorkObject definition (will use Entity from tactical)

6. **Keep story-specific types**
   - Keep: Actor
   - Keep: Activity
   - Keep: Policy
   - Keep: BusinessRule

7. **Add StoryStep definition**
   ```yaml
   StoryStep:
     type: object
     required: [sequence, actor_id, action]
     properties:
       sequence: { type: integer, minimum: 1 }
       actor_id: { $ref: "#/$defs/ActId" }
       action: { type: string }
       invokes_command: { $ref: "#/$defs/CmdId" }
       executes_query: { $ref: "#/$defs/QryId" }
       triggers_events: { type: array, items: { $ref: "#/$defs/EvtId" } }
   ```

8. **Add Actor.description field**
   ```yaml
   Actor:
     properties:
       description: { type: string }
   ```

**Validation**: Read the modified file, check syntax

---

## Phase 3: Example Migration

### Task 3.1: Migrate Strategic Example

**File**: `/domains/ddd/examples/strategic-example.yaml`

**Steps**:

1. **Read current file** to understand structure

2. **Wrap in system root**
   ```yaml
   system:
     id: sys_example  # ADD
     name: Example System  # ADD
     version: "2.0.0"  # ADD

     domains:  # MOVE existing domains here
       - id: dom_example
         # ... existing content
   ```

3. **Nest bounded_contexts under domains**
   ```yaml
   domains:
     - id: dom_example
       bounded_contexts:  # MOVE BCs here
         - id: bc_example
           # ... existing content
   ```

4. **Add context_mapping.name** for all context mappings
   ```yaml
   context_mappings:
     - id: cm_example_to_other
       name: "Example to Other Integration"  # ADD
       # ... existing content
   ```

5. **Add tactical_summary** to each bounded_context
   ```yaml
   bounded_contexts:
     - id: bc_example
       tactical_summary:  # ADD
         aggregate_count: 2
         key_aggregates: [agg_example1, agg_example2]
       tactical_model:  # ADD
         file_path: "tactical/bc_example.yaml"
   ```

**Validation**: YAML syntax check

### Task 3.2: Migrate Tactical Example

**File**: `/domains/ddd/examples/tactical-example.yaml`

**Current Challenge**: Likely has multiple BCs mixed together

**Steps**:

1. **Read current file** and identify bounded_context_ref values

2. **Option A**: If single BC
   - Wrap in bounded_context root
   - Remove all bounded_context_ref properties

3. **Option B**: If multiple BCs (e.g., bc_example1, bc_example2)
   - Split into separate files: tactical-example-bc1.yaml, tactical-example-bc2.yaml
   - Each file wraps in its own bounded_context root
   - Remove all bounded_context_ref properties

4. **For each BC file**, wrap structure:
   ```yaml
   bounded_context:
     id: bc_example
     name: Example Context
     domain_ref: dom_example

     aggregates:  # MOVE existing aggregates here
       - id: agg_example
         # ... existing content (remove bounded_context_ref)

     entities:  # MOVE existing entities here
       - id: ent_example
         # ... existing content (remove bounded_context_ref)

     # ... all other collections
   ```

5. **Add missing descriptions**
   - aggregates: add description field
   - entities: add description field
   - repositories: add description field

6. **Fix immutability** (if value_object or domain_event exists)
   - Change immutability/immutable from true value to schema requirement

**Validation**: YAML syntax check

### Task 3.3: Migrate BFF Example

**File**: `/domains/ddd/examples/bff-example.yaml`

**Steps**:

1. **Read current file** to understand structure

2. **If standalone BFF**: Likely needs to be part of strategic example
   - Could move into strategic-example.yaml under system.bff_scopes
   - Or keep separate but ensure references are valid

3. **Update structure** to match v2.0 flattened BFF schema
   - Ensure endpoints use BFFEndpoint structure
   - Ensure transformations use DataTransformation structure

4. **Validate references**
   - Check all bc_* references exist in strategic example
   - Check all agg_* references exist in tactical example

**Validation**: YAML syntax check

### Task 3.4: Migrate Application Service Example

**File**: `/domains/ddd/examples/application-service-example.yaml`

**Steps**:

1. **Read current file** to understand structure

2. **Move into tactical example** as part of bounded_context
   - Application services belong in tactical schema
   - Should be under bounded_context.application_services array

3. **Or keep standalone** with note that it's a fragment
   - Add comment explaining it's part of a larger tactical model

4. **Flatten operations structure**
   - Ensure transaction_boundary is reference to extracted type
   - Ensure workflow uses extracted WorkflowDefinition type

5. **Add bounded_context context** if standalone
   ```yaml
   # Fragment: application_service for bc_example
   # Include in tactical/bc_example.yaml under application_services array

   - id: svc_app_example
     name: ExampleApplicationService
     # ... existing content
   ```

**Validation**: YAML syntax check

---

## Phase 4: Validation & Cleanup

### Task 4.0: Python Schema Validation Setup

**Prerequisites**:
- [ ] Check Python 3.x installed
- [ ] Install jsonschema library: `pip install jsonschema pyyaml`
- [ ] Create validation script

**Validation Script**: `/tools/validate-v2.py`

```python
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
    print(f"\n{'='*60}")
    print(f"Validating: {example_path}")
    print(f"Against schema: {schema_path}")
    print(f"{'='*60}\n")

    try:
        # Load schema and example
        schema = load_yaml(schema_path)
        example = load_yaml(example_path)

        # Create validator
        validator = Draft202012Validator(schema)

        # Validate
        errors = list(validator.iter_errors(example))

        if errors:
            print(f"❌ VALIDATION FAILED: {len(errors)} error(s) found\n")
            for i, error in enumerate(errors, 1):
                print(f"Error {i}:")
                print(f"  Path: {' -> '.join(str(p) for p in error.path)}")
                print(f"  Message: {error.message}")
                print(f"  Schema path: {' -> '.join(str(p) for p in error.schema_path)}")
                print()
            return False
        else:
            print("✅ VALIDATION PASSED\n")
            return True

    except Exception as e:
        print(f"❌ ERROR: {e}\n")
        return False


def validate_all():
    """Validate all examples against their schemas."""
    validations = [
        # (schema_path, example_path)
        ("domains/ddd/schemas/strategic-ddd.schema.yaml",
         "domains/ddd/examples/strategic-example.yaml"),
        ("domains/ddd/schemas/tactical-ddd.schema.yaml",
         "domains/ddd/examples/tactical-example.yaml"),
        ("domain-stories/domain-stories-schema.yaml",
         "domains/ddd/examples/domain-story-example.yaml"),  # if exists
    ]

    results = []
    for schema_path, example_path in validations:
        if Path(example_path).exists():
            passed = validate_example(schema_path, example_path)
            results.append((example_path, passed))
        else:
            print(f"⚠️  Example not found: {example_path}\n")

    # Summary
    print(f"\n{'='*60}")
    print("VALIDATION SUMMARY")
    print(f"{'='*60}\n")

    passed = sum(1 for _, p in results if p)
    total = len(results)

    for example_path, passed_validation in results:
        status = "✅ PASS" if passed_validation else "❌ FAIL"
        print(f"{status}: {example_path}")

    print(f"\nTotal: {passed}/{total} passed")

    return all(p for _, p in results)


if __name__ == "__main__":
    if len(sys.argv) == 3:
        # Validate single file
        schema_path = sys.argv[1]
        example_path = sys.argv[2]
        success = validate_example(schema_path, example_path)
        sys.exit(0 if success else 1)
    else:
        # Validate all
        success = validate_all()
        sys.exit(0 if success else 1)
```

**Create Script** (execute once):
```bash
mkdir -p tools
# Write the script above to tools/validate-v2.py
chmod +x tools/validate-v2.py
```

### Task 4.1: Python Schema Validation (CRITICAL)

**Execute After Schema and Example Migration**:

```bash
# Install dependencies
pip install jsonschema pyyaml

# Validate strategic example
python tools/validate-v2.py \
  domains/ddd/schemas/strategic-ddd.schema.yaml \
  domains/ddd/examples/strategic-example.yaml

# Validate tactical example
python tools/validate-v2.py \
  domains/ddd/schemas/tactical-ddd.schema.yaml \
  domains/ddd/examples/tactical-example.yaml

# Validate BFF example (if standalone)
python tools/validate-v2.py \
  domains/ddd/schemas/strategic-ddd.schema.yaml \
  domains/ddd/examples/bff-example.yaml

# Or validate all at once
python tools/validate-v2.py
```

**Expected Output**:
```
============================================================
Validating: domains/ddd/examples/strategic-example.yaml
Against schema: domains/ddd/schemas/strategic-ddd.schema.yaml
============================================================

✅ VALIDATION PASSED

============================================================
VALIDATION SUMMARY
============================================================

✅ PASS: domains/ddd/examples/strategic-example.yaml
✅ PASS: domains/ddd/examples/tactical-example.yaml

Total: 2/2 passed
```

**If Validation Fails**:
- Read error output to identify issues
- Common issues:
  - Missing required fields (id, name)
  - Invalid ID patterns
  - Wrong data types
  - Missing $ref targets
  - Extra properties not in schema
- Fix the example or schema
- Re-run validation

### Task 4.2: Cross-File Validation

**Manual Checks** (I can do with Read tool):

1. **ID Consistency**
   - [ ] All bc_* IDs in tactical examples exist in strategic example
   - [ ] All dom_* refs in tactical examples exist in strategic example
   - [ ] All agg_*, cmd_*, evt_* IDs are unique across tactical examples

2. **Reference Validity**
   - [ ] Strategic example's tactical_summary.key_aggregates match tactical example
   - [ ] BFF example's aggregates_from_contexts reference valid BCs
   - [ ] Context mappings reference valid BCs

3. **Schema Compliance**
   - [ ] All IDs follow correct patterns
   - [ ] All required fields present (id, name)
   - [ ] description fields added where required

### Task 4.3: Create Common Type Definitions Document

**File**: `/schemas/common/common-type-definitions.md`

**Content**:

```markdown
# Common Type Definitions v2.0.0

Last Updated: 2025-10-24

## ID Types

### BcId (v2.0.0)
Pattern: `^bc_[a-z0-9_]+$`
Used in: strategic, tactical, domain-stories

[... document all ID types ...]

## Common Types

### Parameter (v2.0.0)
Used in: tactical, domain-stories

[... document all common types ...]
```

### Task 4.4: Update Archive

- [ ] Copy old schemas from docs/examples/partitions/schemas/ to archive
- [ ] Update docs/examples/partitions/schemas/ with v2.0 versions
- [ ] Ensure docs/examples/partitions/ examples are updated

### Task 4.5: Update Documentation

- [ ] Update README files if they reference schema structure
- [ ] Check if any other docs reference old schema patterns
- [ ] Add v2.0 migration notes

---

## Phase 5: Testing

### Task 5.1: Manual Schema Validation

For each schema file:
1. **Read file** completely
2. **Check YAML syntax** is valid
3. **Verify $ref targets exist** in $defs
4. **Check for duplicate keys**
5. **Verify required fields** present

### Task 5.2: Example Validation

For each example file:
1. **Read file** completely
2. **Check YAML syntax** is valid
3. **Verify structure** matches new schema
4. **Check ID patterns** match new ID type patterns
5. **Verify references** point to valid IDs

### Task 5.3: Cross-Schema Validation

1. **Check ID consistency** across examples
2. **Verify domain_ref** in tactical match strategic domains
3. **Verify aggregate references** in strategic summaries exist in tactical
4. **Check bounded_context** IDs consistent across all files

---

## Phase 6: Finalization

### Task 6.1: Git Commit Strategy

**Option A: Single Commit** (simpler)
```bash
git add domains/ddd/schemas/
git add domain-stories/
git add domains/ddd/examples/
git commit -m "Migrate to v2.0 schemas

- Add System root to strategic schema
- Add BoundedContext root to tactical schema
- Extract ID types to $defs across all schemas
- Flatten deep nesting (BFF, operations, queries)
- Enforce DDD best practices (immutability, past tense events)
- Migrate examples to v2.0 structure

Breaking changes:
- Strategic: wrapped in system root
- Tactical: wrapped in bounded_context root, removed bounded_context_ref
- Domain stories: reference by ID instead of embedding

BREAKING CHANGE
"
```

**Option B: Multi-Commit** (more granular)
- Commit 1: Schema structure changes
- Commit 2: Schema validation improvements
- Commit 3: Example migrations
- Commit 4: Documentation updates

### Task 6.2: Create Migration Summary

**File**: `/docs/reports/MIGRATION_COMPLETE.md`

Document:
- What was changed
- File-by-file changes
- Breaking changes list
- How to update any external references
- v2.0 improvements summary

### Task 6.3: Tag Release

```bash
git tag v2.0.0
```

---

## Execution Order Summary

### Parallel Execution Timeline (4-6 hours total)

**Block 1: Preparation** (10 minutes)
1. Create backups (bash operations)
2. **PARALLEL**: Read all 7 files at once (single message with 7 Read calls)
3. Analyze structure and plan changes

**Block 2: Schema Migration** (1-2 hours)
4. **PARALLEL BATCH 1**: Start strategic schema migration
   - Extract ID types + Add System root + Flatten BFF
5. **PARALLEL BATCH 2**: Start tactical schema migration
   - Extract ID types + Add BC root + Flatten operations
6. **PARALLEL BATCH 3**: Start domain stories migration
   - Update to reference pattern + Add narrative
7. Validate all 3 schemas in parallel
8. Create common-type-definitions.md

**Block 3: Example Migration** (1 hour)
9. **SEQUENTIAL**: Migrate strategic-example.yaml (establishes BC/domain IDs)
10. **PARALLEL**: Read all examples to check current IDs
11. **PARALLEL BATCH**: Migrate tactical + bff + app-service together
    - All wrap in roots, remove refs, coordinate IDs
12. Validate all examples

**Block 4: Validation & Finalization** (1 hour)
13. **SETUP**: Create Python validation script (tools/validate-v2.py)
14. **CRITICAL**: Run Python schema validation on all examples
    - `python tools/validate-v2.py` (validates all)
    - Fix any validation errors found
    - Re-run until all pass
15. **PARALLEL**: Read all migrated files for manual checks
16. **PARALLEL**: Syntax validation of all files
17. **SEQUENTIAL**: Cross-reference validation (needs all data)
18. Update documentation
19. Git operations (sequential: add → commit → tag)

**Total Effort**: 4-6 hours active work (vs 2-3 days sequential)

---

## Key Differences from Generic Migration Plan

**What we DON'T need** (because it's LLM-executed, one-off):
- ❌ Generic migration scripts (just do it directly)
- ❌ Validator tool setup (validate manually)
- ❌ Automated test suite (manual validation)
- ❌ CI/CD pipeline updates (not in scope)
- ❌ Team training materials (no team)
- ❌ Rollback automation (git revert is enough)
- ❌ Migration tool distribution (not reused)

**What we DO need** (LLM execution focus):
- ✅ Clear, sequential steps
- ✅ One file at a time approach
- ✅ Read-Edit-Read cycle for each file
- ✅ **Python schema validation** (jsonschema library)
- ✅ Manual validation checklist
- ✅ Git commit strategy
- ✅ Documentation of what changed

---

## Success Criteria

**Schema Migration Complete When**:
- ✅ All 3 schemas have v2.0 structure
- ✅ All ID types extracted to $defs
- ✅ Max nesting depth ≤ 3 levels
- ✅ All required fields added
- ✅ DDD best practices enforced
- ✅ Schemas are valid JSON Schema Draft 2020-12

**Example Migration Complete When**:
- ✅ **CRITICAL: Python validation passes** (`python tools/validate-v2.py` returns success)
- ✅ All examples validate against v2.0 schemas (zero errors)
- ✅ All cross-references valid
- ✅ All IDs follow v2.0 patterns
- ✅ All files have required root objects

**Overall Success**:
- ✅ Can read any file without YAML errors
- ✅ **Python schema validation passes for all examples**
- ✅ Manual validation passes all checks
- ✅ Git history clean with good commit messages
- ✅ Documentation updated
- ✅ v2.0.0 tag created

**Validation is Non-Negotiable**:
- ❌ Cannot commit without passing Python validation
- ❌ Cannot tag release without all validations passing
- ✅ Must fix all validation errors before proceeding

---

## Risk Mitigation

**Risk 1**: Break YAML syntax
- **Mitigation**: Read file after each edit, validate syntax

**Risk 2**: Break cross-references
- **Mitigation**: Track all ID changes, validate references at end

**Risk 3**: Lose information during migration
- **Mitigation**: Compare before/after, ensure all fields migrated

**Risk 4**: Can't revert if needed
- **Mitigation**: Git backups, archive directory, can always reset

---

## Notes for Execution

**When editing large files**:
- Use Edit tool with specific old_string/new_string
- Make one logical change at a time
- Read file after each significant edit
- If file too large, edit in sections

**When creating new types**:
- Add to $defs first
- Then replace inline definitions with $ref
- Verify all $refs resolve

**When restructuring**:
- Extract types bottom-up (leaf nodes first)
- Then replace references top-down
- Validate after each level

**When in doubt**:
- Read the comprehensive analysis report
- Check the v2.0 schema design (task 8)
- Follow the patterns from domain-stories (already good)

---

## Practical Parallel Execution Tactics

### Single Message with Multiple Tool Calls

**Example: Read all files at once**
```
Single message with 7 Read tool calls:
- Read strategic-ddd.schema.yaml
- Read tactical-ddd.schema.yaml
- Read domain-stories-schema.yaml
- Read strategic-example.yaml
- Read tactical-example.yaml
- Read bff-example.yaml
- Read application-service-example.yaml

All results returned in one response → Full context loaded
```

**Example: Edit multiple schemas in parallel batches**
```
After reading and analyzing all schemas, execute edits:

Batch 1 - Extract ID types:
- Edit strategic: Add $defs section with ID types
- Edit tactical: Add $defs section with ID types
- Edit domain-stories: Standardize ID types

Batch 2 - Add root objects:
- Edit strategic: Wrap in System root
- Edit tactical: Wrap in BoundedContext root
- Edit domain-stories: Keep current root (already correct)

Batch 3 - Flatten nesting:
- Edit strategic: Extract BFF types
- Edit tactical: Extract operation types
- Edit domain-stories: Remove embedded types

Each batch: Make related changes together
```

### Parallelization Benefits

**Speed**: 4-6 hours vs 2-3 days
**Reduced Context Switching**: Work on related changes together
**Consistency**: Apply patterns uniformly across schemas
**Validation**: Check all files together after each batch

### When to Parallelize vs Sequential

**Parallelize**:
- ✅ Reading files (always - no dependencies)
- ✅ Independent schema changes (structural)
- ✅ Validation checks (syntax, patterns)
- ✅ Documentation updates

**Sequential**:
- ❌ Changes with dependencies (example IDs must exist before referencing)
- ❌ Git operations (add → commit → tag)
- ❌ Cross-reference validation (needs all data loaded)
- ❌ When one edit depends on result of previous edit

---

## Ready to Execute

This plan is designed for LLM execution with my available tools:
- Read: Load file contents
- Edit: Modify specific sections
- Write: Create new files
- Bash: Git operations, file moves
- Glob: Find files

Each task is concrete and executable. No external tools required. No theoretical abstractions. Just step-by-step file modifications to get from v1.x to v2.0.

**Parallel execution reduces total time from 2-3 days to 4-6 hours.**

---

## Python Validation: Critical Success Factor

### Why Python Validation is Essential

**Manual validation alone is insufficient**:
- ❌ Easy to miss validation errors in large files
- ❌ Can't verify complex schema constraints (patterns, conditionals, $refs)
- ❌ No guarantee examples actually conform to schemas

**Python validation with jsonschema library**:
- ✅ Validates against JSON Schema Draft 2020-12 specification
- ✅ Checks all required fields, types, patterns
- ✅ Validates $ref resolution
- ✅ Catches conditional validation (if/then/else)
- ✅ Provides detailed error messages with paths
- ✅ Industry standard tool (used by OpenAPI, AsyncAPI, etc.)

### Validation Workflow

```
1. Migrate schema files
   ↓
2. Migrate example files
   ↓
3. **RUN: python tools/validate-v2.py**
   ↓
4. Validation passes? ✅
   ├─ Yes → Proceed to git commit
   └─ No → Fix errors and go back to step 3
```

**Do not skip validation. It's the only way to guarantee correctness.**

### Common Validation Errors to Expect

After migration, expect to find:
1. **Missing required fields** - Forgot to add `description` to aggregate
2. **Invalid ID patterns** - ID doesn't match `^bc_[a-z0-9_]+$` pattern
3. **Unresolved $refs** - Reference to non-existent type in $defs
4. **Type mismatches** - String where integer expected
5. **Extra properties** - Field not defined in schema (if additionalProperties: false)
6. **Enum violations** - Value not in allowed enum list
7. **Conditional validation failures** - `if/then` constraints not met

**Each error message shows**:
- Path to the error (e.g., `system -> domains -> 0 -> bounded_contexts`)
- Error message (e.g., "Required field 'name' is missing")
- Schema path (shows which schema rule was violated)

**Fix iteratively until validation passes.**

---

**Next Step**: Start with Phase 1, Task 1.1 when user approves this plan.
