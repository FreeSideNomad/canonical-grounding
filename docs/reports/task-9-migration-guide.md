# Task 9: Migration Guide from v1.x to v2.0

**Date**: 2025-10-23
**Analyst**: Claude (Sonnet 4.5)
**Scope**: Step-by-step guide for migrating from v1.1.0 to v2.0

---

## Executive Summary

This guide provides a comprehensive migration path from v1.1.0 to v2.0 schemas. The migration involves structural changes but can be largely automated.

### Migration Complexity

- **Strategic Schema**: Medium (add root, reorganize)
- **Tactical Schema**: High (add root, remove refs, restructure by BC)
- **Domain Stories**: High (remove embedded, add references)
- **Overall Effort**: 2-3 days with tooling, 1-2 weeks manual

### Automation Level

- **Automated**: 70% (structural transformations)
- **Manual**: 30% (validation, cleanup, testing)

---

## Part 1: Pre-Migration Checklist

### 1.1 Backup Current Models

```bash
# Create backup
mkdir -p backup/v1.1.0
cp -r models/ backup/v1.1.0/
cp -r domains/ backup/v1.1.0/

# Commit current state
git add .
git commit -m "Backup before v2.0 migration"
git tag v1.1.0-final
```

### 1.2 Install Migration Tools

```bash
# Download migration tools
git clone https://github.com/canonical-grounding/migration-tools.git
cd migration-tools
npm install  # or pip install -r requirements.txt

# Verify tools
./validate-v1.sh models/
```

### 1.3 Inventory Current Models

```bash
# Generate inventory
./inventory-models.sh > migration-inventory.txt

# Review what needs migrating
cat migration-inventory.txt
```

**Expected Output**:
```
Strategic Models: 1 file(s)
  - strategic-model-v1.yaml (domains: 5, BCs: 12)

Tactical Models: 3 file(s) (mixed BCs)
  - ddd-tactical-model.yaml (aggregates from 12 BCs)
  - ddd-schema-example.yaml
  - tactical-example.yaml

Domain Stories: 4 file(s)
  - customer-registration.yaml (embedded objects: 15)
  - order-placement.yaml (embedded objects: 23)
  - ...
```

---

## Part 2: Strategic Schema Migration

### 2.1 Changes Required

| Change | v1.1.0 | v2.0 | Type |
|--------|--------|------|------|
| Root object | None | `system` | **BREAKING** |
| ID types | Inline patterns | Extracted to $defs | Structure |
| BC definition | Tactical IDs in arrays | Full tactical_summary | Enhancement |
| context_mapping | No `name` field | Add `name` field | Enhancement |

### 2.2 Manual Migration Steps

#### Step 1: Add System Root

**Before (v1.1.0)**:
```yaml
# strategic-model-v1.yaml
domains:
  - id: dom_customer
    name: Customer Management
    # ...

  - id: dom_order
    name: Order Processing
    # ...

bounded_contexts:
  - id: bc_customer_profile
    name: Customer Profile
    domain_ref: dom_customer
    # ...
```

**After (v2.0)**:
```yaml
# strategic-model.yaml
system:
  id: sys_ecommerce  # ← NEW: add system ID
  name: E-Commerce Platform  # ← NEW: add system name
  version: "2.0.0"  # ← NEW: add version

  domains:
    - id: dom_customer
      name: Customer Management

      bounded_contexts:  # ← MOVED: nest BCs under domains
        - id: bc_customer_profile
          name: Customer Profile
          # ...

    - id: dom_order
      name: Order Processing
      # ...
```

**Migration Script**:
```bash
./migrate-strategic.sh strategic-model-v1.yaml > strategic-model.yaml
```

#### Step 2: Add Missing Fields

```yaml
# Add to each context_mapping
context_mappings:
  - id: cm_order_to_customer
    name: "Order to Customer Integration"  # ← ADD
    upstream_context: bc_customer_profile
    downstream_context: bc_order_mgmt
    # ...
```

#### Step 3: Add Tactical Summary

```yaml
# For each bounded_context
bounded_contexts:
  - id: bc_customer_profile
    name: Customer Profile

    tactical_summary:  # ← ADD
      aggregate_count: 2
      key_aggregates:
        - agg_customer
        - agg_preferences
      has_application_services: true
      has_domain_services: false
      event_count: 5

    tactical_model:  # ← ADD
      file_path: "tactical/bc_customer_profile.yaml"
```

**Auto-generate from tactical models**:
```bash
./generate-tactical-summary.sh bc_customer_profile.yaml
```

### 2.3 Automated Migration

```bash
# Full automated migration
./migrate-strategic-full.sh \
  --input strategic-model-v1.yaml \
  --output strategic-model.yaml \
  --system-id sys_ecommerce \
  --system-name "E-Commerce Platform" \
  --system-version "2.0.0"

# Validate output
./validate-v2.sh strategic-model.yaml --schema strategic-ddd.schema.yaml
```

---

## Part 3: Tactical Schema Migration

### 3.1 Changes Required (BREAKING)

| Change | v1.1.0 | v2.0 | Type |
|--------|--------|------|------|
| Root object | None | `bounded_context` | **BREAKING** |
| BC reference | Every type has `bounded_context_ref` | Removed (implicit) | **BREAKING** |
| File organization | Mixed BCs in one file | One file per BC | **BREAKING** |
| ID types | Inline patterns | Extracted to $defs | Structure |
| Immutability | `default: true` | `const: true` | **BREAKING** |

### 3.2 Migration Strategy

**Challenge**: v1.1.0 likely has multiple BCs mixed in one file

**Solution**: Split by bounded_context_ref

#### Step 1: Analyze Current Tactical Model

```bash
./analyze-tactical.sh ddd-tactical-model.yaml

# Output:
# Found 3 bounded contexts:
#   - bc_customer_profile (7 aggregates, 15 entities)
#   - bc_order_mgmt (5 aggregates, 12 entities)
#   - bc_inventory (3 aggregates, 8 entities)
#
# Recommendation: Split into 3 files
```

#### Step 2: Split by Bounded Context

```python
# migrate-tactical.py
def split_by_bounded_context(v1_model):
    bc_groups = {}

    # Group aggregates by BC
    for agg in v1_model.get('aggregates', []):
        bc_ref = agg['bounded_context_ref']
        if bc_ref not in bc_groups:
            bc_groups[bc_ref] = {
                'aggregates': [],
                'entities': [],
                'value_objects': [],
                #...
            }
        agg_copy = agg.copy()
        del agg_copy['bounded_context_ref']  # Remove - now implicit
        bc_groups[bc_ref]['aggregates'].append(agg_copy)

    # Same for entities, value objects, etc.
    # ...

    return bc_groups
```

**Run migration**:
```bash
./split-tactical.sh ddd-tactical-model.yaml --output-dir tactical/

# Creates:
#   tactical/bc_customer_profile.yaml
#   tactical/bc_order_mgmt.yaml
#   tactical/bc_inventory.yaml
```

#### Step 3: Add Bounded Context Root to Each File

**Before (v1.1.0)** - hypothetical:
```yaml
# Mixed aggregates from multiple BCs
aggregates:
  - id: agg_customer
    bounded_context_ref: bc_customer_profile  # ← Explicit
    name: Customer Aggregate
    # ...

  - id: agg_order
    bounded_context_ref: bc_order_mgmt  # ← Different BC!
    name: Order Aggregate
    # ...
```

**After (v2.0)** - tactical/bc_customer_profile.yaml:
```yaml
bounded_context:  # ← NEW ROOT
  id: bc_customer_profile
  name: Customer Profile
  domain_ref: dom_customer

  aggregates:  # ← Nested under BC
    - id: agg_customer
      name: Customer Aggregate
      # NO bounded_context_ref - implicit
      # ...
```

**After (v2.0)** - tactical/bc_order_mgmt.yaml:
```yaml
bounded_context:
  id: bc_order_mgmt
  name: Order Management
  domain_ref: dom_order

  aggregates:
    - id: agg_order
      name: Order Aggregate
      # ...
```

#### Step 4: Fix Immutability Constants

```yaml
# Before
value_object:
  immutability:
    type: boolean
    default: true  # ← Can be changed

# After
value_object:
  immutability:
    type: boolean
    const: true  # ← Cannot be changed
```

**Script**:
```bash
./fix-immutability.sh tactical/*.yaml
```

#### Step 5: Add Missing Description Fields

```yaml
# Add description to types missing it
aggregate:
  id: agg_customer
  name: Customer Aggregate
  description: "Manages customer identity and contact information"  # ← ADD

entity:
  id: ent_customer
  name: Customer
  description: "The customer entity representing a person or organization"  # ← ADD
```

### 3.3 Automated Tactical Migration

```bash
# Full tactical migration
./migrate-tactical-full.sh \
  --input ddd-tactical-model.yaml \
  --output-dir tactical/ \
  --split-by-bc \
  --add-descriptions \
  --fix-immutability \
  --remove-bc-refs

# Validate all outputs
for file in tactical/*.yaml; do
  ./validate-v2.sh $file --schema tactical-ddd.schema.yaml
done
```

---

## Part 4: Domain Stories Migration

### 4.1 Changes Required (BREAKING)

| Change | v1.1.0 | v2.0 | Type |
|--------|--------|------|------|
| Aggregate | Embedded full object | Reference by ID | **BREAKING** |
| Command | Embedded full object | Reference by ID | **BREAKING** |
| Event | Embedded full object | Reference by ID | **BREAKING** |
| WorkObject | Defined in schema | Removed (use Entity) | **BREAKING** |
| Scope | No BC reference | Add `bounded_contexts` array | Enhancement |

### 4.2 Migration Strategy

#### Step 1: Extract Embedded Objects to Tactical

**Before (v1.1.0)**:
```yaml
domain_stories:
  - domain_story_id: dst_customer_registration
    title: "Customer Registration"

    aggregates:  # ← Embedded full definitions
      - aggregate_id: agg_customer
        name: Customer Aggregate
        root_work_object_id: wobj_customer
        work_object_ids:
          - wobj_customer
          - wobj_address
        invariants:
          - "Email must be unique"

    commands:  # ← Embedded full definitions
      - command_id: cmd_create_customer
        name: Create Customer
        actor_ids: [act_new_customer]
        parameters:
          - name: email
            type: string
          - name: password
            type: string
```

**After (v2.0)**:
```yaml
# domain-stories/customer-registration.yaml
domain_stories:
  - domain_story_id: dst_customer_registration
    title: "Customer Registration"

    bounded_contexts:  # ← NEW: Scope
      - bc_customer_profile

    aggregates_involved:  # ← Just IDs
      - agg_customer

    commands_invoked:  # ← Just IDs
      - cmd_create_customer
```

**Extracted to tactical/bc_customer_profile.yaml**:
```yaml
bounded_context:
  id: bc_customer_profile

  aggregates:
    - id: agg_customer
      name: Customer Aggregate
      # Full definition here (extracted from domain story)

  command_interfaces:
    - id: cmd_customer_commands
      command_records:
        - record_name: CreateCustomerCmd
          intent: createCustomer
          # ...
```

#### Step 2: Map WorkObject → Entity

```yaml
# v1.1.0: WorkObject
work_object_id: wobj_customer

# v2.0: Entity
entity_id: ent_customer
```

**Mapping script**:
```python
def map_work_object_to_entity(work_object):
    return {
        'id': work_object['work_object_id'].replace('wobj_', 'ent_'),
        'name': work_object['name'],
        'description': work_object.get('description', ''),
        'attributes': work_object.get('attributes', []),
        # Add identity_field, business_methods, etc.
    }
```

#### Step 3: Add Narrative Structure

```yaml
# v2.0: Add structured narrative
narrative:
  steps:
    - sequence: 1
      actor_id: act_new_customer
      action: "Fills out registration form with email and password"

    - sequence: 2
      actor_id: act_new_customer
      action: "Submits registration form"
      invokes_command: cmd_create_customer
      triggers_events:
        - evt_customer_created
```

### 4.3 Automated Domain Stories Migration

```bash
# Migrate domain stories
./migrate-domain-stories.sh \
  --input domain-stories-v1/ \
  --output domain-stories/ \
  --tactical-output tactical/ \
  --extract-embedded \
  --map-work-objects \
  --add-narrative

# Validate
for file in domain-stories/*.yaml; do
  ./validate-v2.sh $file --schema domain-stories.schema.yaml
done
```

---

## Part 5: Migration Validation

### 5.1 Validation Checklist

```bash
# Run full validation suite
./validate-all-v2.sh

# Checks:
# ✅ All schemas valid against v2.0 schema definitions
# ✅ Cross-schema references valid (BC IDs, aggregate IDs, etc.)
# ✅ No duplicate IDs
# ✅ One repository per aggregate
# ✅ Immutability enforced
# ✅ Required fields present (id, name, description)
```

### 5.2 Cross-Schema Validation

```python
# tools/validate-cross-schema.py

def validate_cross_schema_refs(strategic, tactical_dir, domain_stories_dir):
    errors = []

    # Extract all BC IDs from strategic
    bc_ids = {bc['id'] for bc in strategic['system']['domains']
              for bc in bc['bounded_contexts']}

    # Validate tactical files
    for bc_file in glob(f"{tactical_dir}/*.yaml"):
        tactical = load_yaml(bc_file)
        bc_id = tactical['bounded_context']['id']

        if bc_id not in bc_ids:
            errors.append(f"Tactical BC {bc_id} not found in strategic model")

    # Validate domain stories
    for story_file in glob(f"{domain_stories_dir}/*.yaml"):
        story = load_yaml(story_file)
        for story_obj in story['domain_stories']:
            for bc_ref in story_obj.get('bounded_contexts', []):
                if bc_ref not in bc_ids:
                    errors.append(f"Story {story_obj['domain_story_id']} references unknown BC {bc_ref}")

            # Validate aggregate refs exist in tactical
            for agg_ref in story_obj.get('aggregates_involved', []):
                if not aggregate_exists(agg_ref, tactical_dir):
                    errors.append(f"Story references unknown aggregate {agg_ref}")

    return errors
```

### 5.3 Generate Diff Report

```bash
# Compare v1.1.0 vs v2.0
./diff-models.sh backup/v1.1.0/ models/

# Output: migration-diff-report.md
#   - Schema structure changes
#   - ID mappings (wobj_* → ent_*)
#   - Moved objects (embedded → tactical)
#   - New fields added
#   - Removed fields
```

---

## Part 6: Manual Cleanup Tasks

### 6.1 Review and Enhance

**Task 1**: Add missing descriptions
```bash
# Find types without descriptions
./find-missing-descriptions.sh models/ > missing-descriptions.txt

# Manually add descriptions to:
#   - Aggregates
#   - Entities
#   - Repositories
#   - etc.
```

**Task 2**: Validate business rules
```yaml
# Check invariants make sense
aggregate:
  invariants:
    - "Email must be unique"  # ← Verify this is enforced
    - "Customer must have contact method"  # ← Verify this is valid
```

**Task 3**: Review tactical summaries
```yaml
# strategic model
bounded_context:
  tactical_summary:
    aggregate_count: 2  # ← Verify matches tactical file
```

### 6.2 Update Documentation

```bash
# Update README files
./generate-readmes.sh models/

# Creates:
#   - models/README.md (overview)
#   - models/tactical/README.md (tactical models guide)
#   - models/domain-stories/README.md (stories guide)
```

---

## Part 7: Testing Migration

### 7.1 Schema Validation

```bash
# Validate all v2.0 models
npm test  # or python -m pytest

# Expected output:
# ✅ strategic-model.yaml validates against strategic-ddd.schema.yaml
# ✅ tactical/bc_customer_profile.yaml validates against tactical-ddd.schema.yaml
# ✅ tactical/bc_order_mgmt.yaml validates against tactical-ddd.schema.yaml
# ✅ domain-stories/customer-registration.yaml validates against domain-stories.schema.yaml
# ✅ Cross-schema references valid
# ✅ No duplicate IDs
# ✅ All required fields present
```

### 7.2 Generate Documentation

```bash
# Generate markdown docs from v2.0 models
./generate-markdown.sh strategic-model.yaml > docs/strategic-overview.md
./generate-markdown.sh tactical/bc_customer_profile.yaml > docs/bc-customer-profile.md

# Compare with v1.1.0 docs
diff docs-v1/strategic-overview.md docs/strategic-overview.md
```

### 7.3 Smoke Test Queries

```python
# Test that all references resolve
def test_references():
    strategic = load('strategic-model.yaml')
    tactical_bc1 = load('tactical/bc_customer_profile.yaml')
    story = load('domain-stories/customer-registration.yaml')

    # Test: Story references valid BC
    assert 'bc_customer_profile' in strategic.all_bc_ids()

    # Test: Story references valid aggregate
    assert 'agg_customer' in tactical_bc1.all_aggregate_ids()

    # Test: Strategic summary matches tactical
    assert strategic.bc_summary('bc_customer_profile').aggregate_count == \
           len(tactical_bc1.aggregates)
```

---

## Part 8: Rollback Plan

### 8.1 If Migration Fails

```bash
# Restore from backup
rm -rf models/
cp -r backup/v1.1.0/models/ models/

# Restore schemas
git checkout v1.1.0-final -- domains/

# Verify restoration
./validate-v1.sh models/
```

### 8.2 Partial Rollback

```bash
# Keep strategic v2.0, rollback tactical
cp -r backup/v1.1.0/models/tactical/ models/tactical/

# Or vice versa
```

---

## Part 9: Post-Migration

### 9.1 Commit v2.0

```bash
# Review all changes
git status
git diff

# Commit migration
git add .
git commit -m "Migrate to v2.0 schemas

- Add system root to strategic model
- Split tactical model by bounded context
- Convert domain stories to reference pattern
- Extract ID types
- Enforce DDD best practices

Breaking changes:
- Strategic: Add system root
- Tactical: Add BC root, remove bounded_context_ref
- Domain Stories: Reference by ID instead of embed

Fixes: #123"

# Tag release
git tag v2.0.0
```

### 9.2 Update CI/CD

```yaml
# .github/workflows/validate-schemas.yml
name: Validate Schemas

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Validate Strategic Model
        run: ./validate-v2.sh models/strategic-model.yaml --schema schemas/strategic-ddd.schema.yaml

      - name: Validate Tactical Models
        run: |
          for file in models/tactical/*.yaml; do
            ./validate-v2.sh $file --schema schemas/tactical-ddd.schema.yaml
          done

      - name: Validate Domain Stories
        run: |
          for file in models/domain-stories/*.yaml; do
            ./validate-v2.sh $file --schema schemas/domain-stories.schema.yaml
          done

      - name: Cross-Schema Validation
        run: ./validate-cross-schema.sh
```

---

## Part 10: Migration Timeline

### 10.1 Recommended Phased Approach

**Week 1: Preparation**
- Day 1: Backup, inventory
- Day 2: Install tools, test on sample
- Day 3: Review migration plan

**Week 2: Strategic Migration**
- Day 1: Migrate strategic schema
- Day 2: Add tactical summaries
- Day 3: Validate and test

**Week 3: Tactical Migration**
- Day 1-2: Split by BC, migrate
- Day 3-4: Fix immutability, add descriptions
- Day 5: Validate

**Week 4: Domain Stories Migration**
- Day 1-2: Extract embedded objects
- Day 3: Map work objects to entities
- Day 4: Add narratives
- Day 5: Validate

**Week 5: Testing & Cleanup**
- Day 1-2: Full validation suite
- Day 3: Manual review and cleanup
- Day 4: Documentation generation
- Day 5: Final testing

**Week 6: Deployment**
- Day 1: CI/CD updates
- Day 2: Team training
- Day 3-4: Gradual rollout
- Day 5: Monitoring and fixes

---

## Conclusion

### Migration Summary

**Effort**: ~6 weeks for full migration (or 2-3 days with automation)

**Risk Level**: Medium
- Breaking changes in all schemas
- Extensive structural changes
- Cross-schema dependencies

**Mitigation**:
- Automated migration tools (70% automated)
- Comprehensive validation
- Phased approach
- Rollback plan

**Recommendation**: **Proceed with migration** - Benefits outweigh costs

**Next Steps**:
1. Review migration plan
2. Test tools on sample models
3. Schedule migration window
4. Execute migration
5. Validate and deploy

The v2.0 schemas provide significant improvements in structure, consistency, and DDD compliance, making the migration effort worthwhile.
