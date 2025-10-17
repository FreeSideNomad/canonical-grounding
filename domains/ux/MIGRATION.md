# UX Schema Migration Guide

## Overview

The UX schema has been partitioned from a single 1,141-line file (`model-schema.yaml`) into 3 focused schemas organized by architectural layer. This guide helps you understand the changes and migrate existing data.

## What Changed?

### Before: Monolithic Schema (v1.0.0)
- **File**: `model-schema.yaml`
- **Size**: 1,141 lines
- **Concepts**: ~12 concepts in one file
- **Cross-references**: Internal `$ref` pointers
- **Organization**: All UX patterns mixed together

### After: Partitioned Schemas (v2.0.0)
- **Files**: 3 separate schemas
- **Size**: 1,164 lines total (388 lines average per file)
- **Concepts**: ~17 concepts distributed by architectural layer
- **Cross-references**: String pattern ID references
- **Organization**: Structure → Navigation → Interaction layers

### Schema Distribution

| Partition | File | Concepts | Lines | Layer |
|-----------|------|----------|-------|-------|
| Structure | structure-ux.schema.yaml | 5 | 200 | Foundation |
| Navigation | navigation-ux.schema.yaml | 5 | 362 | Wayfinding |
| Interaction | interaction-ux.schema.yaml | 7 | 602 | Action |

## Migration Options

### Option 1: Continue Using Original Schema (No Changes)

The original schema is **preserved** for backward compatibility:

- **File**: `model-schema.yaml`
- **Status**: Maintained, not deprecated
- **Action**: No changes needed
- **Use case**: Existing systems that reference the monolithic schema

**Benefits**: Zero migration effort, no breaking changes

**Limitations**: Doesn't benefit from improved modularity and DDD grounding precision

### Option 2: Migrate to Partitioned Schemas (Recommended)

Adopt the new partitioned structure for better maintainability:

- **Files**: 3 separate schemas
- **Action**: Update data files and validation scripts
- **Use case**: New systems or systems ready for refactoring

**Benefits**:
- Clearer architectural layers
- More precise DDD groundings
- Use only what you need
- Better team collaboration (IA architects vs interaction designers)

**Limitations**: Requires one-time migration effort

## Migration Steps

### Step 1: Identify Your Scope

Determine which schemas you need based on your usage:

| If you work with... | You need... |
|---------------------|-------------|
| Information architecture, taxonomy, search | `structure-ux.schema.yaml` |
| Navigation, pages, breadcrumbs | `structure` + `navigation-ux.schema.yaml` |
| Workflows, components, interactions | `navigation` + `interaction-ux.schema.yaml` |
| Complete UX system | All 3 schemas |

### Step 2: Update Cross-References

Change internal `$ref` pointers to ID string references:

#### Before (Monolithic Schema)
```yaml
page:
  id: page_product_detail
  information_architecture:
    $ref: '#/$defs/information_architecture/ia_products'  # Internal reference
  sections:
    - $ref: '#/$defs/page_section/sect_header'
    - $ref: '#/$defs/page_section/sect_product_info'
```

#### After (Partitioned Schemas)
```yaml
# In navigation data
page:
  id: page_product_detail
  information_architecture_ref: ia_products  # String ID reference to structure
  bounded_context_ref: bc_product_catalog  # DDD grounding
  sections:
    - sect_header
    - sect_product_info
```

### Step 3: Add DDD Grounding References

The partitioned schemas have explicit DDD grounding fields:

#### Pages Ground in Bounded Contexts
```yaml
# In navigation data
page:
  id: page_product_detail
  name: "Product Detail"
  bounded_context_ref: bc_product_catalog  # NEW: Required DDD grounding
  url: "/products/:id"
```

#### Workflows Ground in Aggregates
```yaml
# In interaction data
workflow:
  id: wf_checkout
  name: "Checkout Process"
  aggregate_refs:  # NEW: Required DDD grounding
    - agg_shopping_cart
    - agg_order
    - agg_payment
```

### Step 4: Update Validation Scripts

#### Before
```bash
# Validate against monolithic schema
python3 validate.py --schema model-schema.yaml --data my-ux-data.yaml
```

#### After
```bash
# Validate against multiple schemas
python3 partition-examples/tools/validate_multifile_schema.py \
  domains/ux/schemas/structure-ux.schema.yaml \
  my-structure-data.yaml

python3 partition-examples/tools/validate_multifile_schema.py \
  domains/ux/schemas/navigation-ux.schema.yaml \
  my-navigation-data.yaml

python3 partition-examples/tools/validate_multifile_schema.py \
  domains/ux/schemas/interaction-ux.schema.yaml \
  my-interaction-data.yaml
```

### Step 5: Split Data Files (Optional)

If you have large data files, consider splitting them by layer:

#### Before
```yaml
# my-ux-data.yaml (everything in one file)
information_architecture:
  ia_products:
    organization_scheme: hierarchical
    # ...

pages:
  - id: page_home
    # ...

components:
  - id: cmp_button
    # ...
```

#### After
```yaml
# structure-data.yaml
information_architecture:
  ia_products:
    organization_scheme: hierarchical
    facets:
      - facet_brand
      - facet_price

hierarchy_nodes:
  - id: hn_electronics
    children_refs:
      - hn_laptops

facets:
  - id: facet_brand
    type: multi_select

# navigation-data.yaml
pages:
  - id: page_home
    information_architecture_ref: ia_products  # Reference to structure
    bounded_context_ref: bc_storefront  # DDD grounding
    sections:
      - sect_header

# interaction-data.yaml
workflows:
  - id: wf_checkout
    page_refs:  # Reference to navigation
      - page_cart
      - page_checkout
    aggregate_refs:  # DDD grounding
      - agg_shopping_cart
      - agg_order

components:
  - id: cmp_button
    page_refs:
      - page_home
```

### Step 6: Test Validation

Validate all your data files against the new schemas:

```bash
source venv/bin/activate

# Test structure data
python3 partition-examples/tools/validate_multifile_schema.py \
  domains/ux/schemas/structure-ux.schema.yaml \
  structure-data.yaml

# Test navigation data
python3 partition-examples/tools/validate_multifile_schema.py \
  domains/ux/schemas/navigation-ux.schema.yaml \
  navigation-data.yaml

# Test interaction data
python3 partition-examples/tools/validate_multifile_schema.py \
  domains/ux/schemas/interaction-ux.schema.yaml \
  interaction-data.yaml
```

## Common Migration Patterns

### Pattern 1: Page References IA

**Before**: Nested object
```yaml
page:
  id: page_products
  information_architecture:
    organization_scheme: hierarchical
    facets: [...]
```

**After**: ID reference
```yaml
# In navigation data
page:
  id: page_products
  information_architecture_ref: ia_products  # Reference to structure schema

# In structure data
information_architecture:
  ia_products:
    organization_scheme: hierarchical
    facets: [facet_brand, facet_price]
```

### Pattern 2: Workflow References Pages and Aggregates

**Before**: Mixed references
```yaml
workflow:
  id: wf_checkout
  steps:
    - page: page_cart  # Implicit
      aggregates: [...]  # Implicit
```

**After**: Explicit references with DDD grounding
```yaml
workflow:
  id: wf_checkout
  page_refs:  # Explicit cross-partition reference
    - page_cart
    - page_checkout
  aggregate_refs:  # Explicit DDD grounding
    - agg_shopping_cart
    - agg_order
```

### Pattern 3: Component Uses Design Tokens

**Before**: Inline styles
```yaml
component:
  id: cmp_button
  styles:
    background_color: "#007bff"
    padding: "12px 24px"
```

**After**: Design token references
```yaml
# In interaction data
component:
  id: cmp_button
  design_token_refs:
    - dt_color_primary
    - dt_spacing_button

design_tokens:
  - id: dt_color_primary
    value: "#007bff"
  - id: dt_spacing_button
    value: "12px 24px"
```

## DDD Grounding Migration

### New Required Fields

The partitioned schemas add explicit DDD grounding fields:

| UX Concept | New Field | Target | Schema |
|------------|-----------|--------|--------|
| Page | `bounded_context_ref` | `bc_*` | navigation |
| Workflow | `aggregate_refs` | `agg_*` | interaction |
| HierarchyNode | `bounded_context_ref` | `bc_*` | structure |

### Example: Adding DDD References

```yaml
# Before: No explicit DDD grounding
page:
  id: page_product_detail
  name: "Product Detail"
  url: "/products/:id"

# After: Explicit DDD grounding
page:
  id: page_product_detail
  name: "Product Detail"
  url: "/products/:id"
  bounded_context_ref: bc_product_catalog  # NEW: Required field
```

## Validation Differences

### Monolithic Schema Validation

```python
import jsonschema
import yaml

schema = yaml.safe_load(open('model-schema.yaml'))
data = yaml.safe_load(open('my-ux-data.yaml'))

# Validates entire data structure
jsonschema.validate(data, schema)
```

### Partitioned Schema Validation

```python
from jsonschema import Draft202012Validator, Registry
import yaml

# Load all schemas
schemas = {}
for partition in ['structure', 'navigation', 'interaction']:
    schema_file = f'schemas/{partition}-ux.schema.yaml'
    schema = yaml.safe_load(open(schema_file))
    schemas[schema['$id']] = schema

# Create registry
registry = Registry().with_resources([
    (schema['$id'], schema) for schema in schemas.values()
])

# Validate data against specific partition
data = yaml.safe_load(open('navigation-data.yaml'))
validator = Draft202012Validator(schemas['navigation'], registry=registry)
validator.validate(data)
```

## Benefits of Partitioning

### 1. Clearer Architectural Layers
- **Before**: All concepts mixed together
- **After**: Structure → Navigation → Interaction hierarchy
- **Benefit**: Matches UX professional practice

### 2. More Precise DDD Grounding
- **Before**: Implicit or missing DDD references
- **After**: Explicit `bounded_context_ref` and `aggregate_refs` fields
- **Benefit**: Stronger semantic correctness

### 3. Better Team Collaboration
- **Before**: IA architects and interaction designers edit same file
- **After**: Separate files for different specializations
- **Benefit**: Fewer merge conflicts

### 4. Flexible Usage
- **Before**: Must load entire schema
- **After**: Load only what you need (e.g., just navigation patterns)
- **Benefit**: Reduced complexity for focused work

### 5. Improved Discoverability
- **Before**: 1,141 lines to navigate
- **After**: 200-602 lines per file
- **Benefit**: Easier to find concepts

## Backward Compatibility

The original schema (`model-schema.yaml`) is **preserved** and will continue to be maintained:

- No breaking changes to existing systems
- Both schemas validate the same core concepts
- Examples provided for both approaches
- Migration is optional, not required

## Timeline Recommendation

| Organization Size | Recommended Timeline |
|-------------------|---------------------|
| Small team (< 5) | 1-2 days |
| Medium team (5-20) | 3-5 days |
| Large org (20+) | 1-2 weeks |

## Getting Help

If you encounter issues during migration:

1. Check the [examples/partitioned/](examples/partitioned/) directory for reference
2. Review the [README.md](README.md) for schema details
3. Run validation with verbose output to see specific errors
4. Verify DDD groundings are correct (pages → bounded contexts, workflows → aggregates)

## Checklist

Use this checklist to track your migration:

- [ ] Identified which schemas I need (structure/navigation/interaction)
- [ ] Updated cross-references from `$ref` to string ID references
- [ ] Added DDD grounding fields (`bounded_context_ref`, `aggregate_refs`)
- [ ] Updated validation scripts to use `validate_multifile_schema.py`
- [ ] Split data files by partition (optional)
- [ ] Validated all data files successfully
- [ ] Updated documentation to reference new schemas
- [ ] Trained team on architectural layers
- [ ] Updated CI/CD pipelines for new validation

## Summary

| Aspect | Monolithic | Partitioned |
|--------|-----------|-------------|
| **Files** | 1 | 3 |
| **Size** | 1,141 lines | 1,164 lines (388 avg) |
| **Concepts** | ~12 (mixed) | ~17 (organized) |
| **Cross-refs** | `$ref` | String IDs |
| **DDD Grounding** | Implicit | Explicit |
| **Layers** | Flat | Structure → Navigation → Interaction |
| **Collaboration** | Single file | Separate files by layer |
| **Status** | Maintained | Recommended |

Choose the approach that best fits your needs - both are supported!
