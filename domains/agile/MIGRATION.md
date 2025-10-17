# Agile Schema Migration Guide

## Overview

The Agile schema has been partitioned from a single 1,972-line file (`model.schema.yaml`) into 5 focused schemas. This guide helps you understand the changes and migrate existing data.

## What Changed?

### Before: Monolithic Schema (v1.0.0)
- **File**: `model.schema.yaml`
- **Size**: 1,972 lines
- **Concepts**: 35 concepts in one file
- **Cross-references**: Internal `$ref` pointers

### After: Partitioned Schemas (v2.0.0)
- **Files**: 5 separate schemas
- **Size**: 2,526 lines total (505 lines average per file)
- **Concepts**: 35 concepts distributed by scale level
- **Cross-references**: String pattern ID references

### Schema Distribution

| Partition | File | Concepts | Lines |
|-----------|------|----------|-------|
| Portfolio | portfolio-agile.schema.yaml | 8 | 477 |
| Program | program-agile.schema.yaml | 7 | 586 |
| Team | team-agile.schema.yaml | 10 | 621 |
| Delivery | delivery-agile.schema.yaml | 8 | 659 |
| SAFe | safe-agile.schema.yaml | 2 | 183 |

## Migration Options

### Option 1: Continue Using Original Schema (No Changes)

The original schema is **preserved** for backward compatibility:

- **File**: `model.schema.yaml`
- **Status**: Maintained, not deprecated
- **Action**: No changes needed
- **Use case**: Existing systems that reference the monolithic schema

**Benefits**: Zero migration effort, no breaking changes

**Limitations**: Doesn't benefit from improved modularity and clarity

### Option 2: Migrate to Partitioned Schemas (Recommended)

Adopt the new partitioned structure for better maintainability:

- **Files**: 5 separate schemas
- **Action**: Update data files and validation scripts
- **Use case**: New systems or systems ready for refactoring

**Benefits**:
- Smaller, more focused files
- Clearer boundaries between scale levels
- Easier navigation and collaboration
- Use only what you need

**Limitations**: Requires one-time migration effort

## Migration Steps

### Step 1: Identify Your Scope

Determine which schemas you need based on your usage:

| If you work with... | You need... |
|---------------------|-------------|
| Portfolio planning, epics, value streams | `portfolio-agile.schema.yaml` |
| PI planning, program coordination | `portfolio` + `program-agile.schema.yaml` |
| Sprint planning, team ceremonies | `program` + `team-agile.schema.yaml` |
| Backlog management, user stories | `team` + `delivery-agile.schema.yaml` |
| SAFe ARTs, cadences | All 5 schemas |

### Step 2: Update Cross-References

Change internal `$ref` pointers to ID string references:

#### Before (Monolithic Schema)
```yaml
epic:
  id: epic_mobile_app
  program:
    $ref: '#/$defs/Program'  # Internal JSON Schema reference
  features:
    - $ref: '#/$defs/feature/feat_ios'
    - $ref: '#/$defs/feature/feat_android'
```

#### After (Partitioned Schemas)
```yaml
epic:
  id: epic_mobile_app
  program_ref: prg_mobile_platform  # String ID reference
  feature_refs:
    - feat_ios
    - feat_android
```

### Step 3: Update Validation Scripts

#### Before
```bash
# Validate against monolithic schema
python3 validate.py --schema model.schema.yaml --data my-data.yaml
```

#### After
```bash
# Validate against multiple schemas
python3 partition-examples/tools/validate_multifile_schema.py \
  domains/agile/schemas/portfolio-agile.schema.yaml \
  my-portfolio-data.yaml

python3 partition-examples/tools/validate_multifile_schema.py \
  domains/agile/schemas/delivery-agile.schema.yaml \
  my-delivery-data.yaml
```

### Step 4: Split Data Files (Optional)

If you have large data files, consider splitting them by scale level:

#### Before
```yaml
# my-agile-data.yaml (everything in one file)
portfolio:
  id: pf_ecommerce
  epics: [...]

programs:
  - id: prg_mobile
    program_increments: [...]

teams:
  - id: tm_ios
    sprints: [...]
```

#### After
```yaml
# portfolio-data.yaml
portfolio:
  id: pf_ecommerce
  epic_refs: [epic_mobile_app, ...]

# program-data.yaml
programs:
  - id: prg_mobile
    portfolio_ref: pf_ecommerce
    program_increment_refs: [pi_2025_q1, ...]

# team-data.yaml
teams:
  - id: tm_ios
    program_ref: prg_mobile
    sprint_refs: [sp_2025_01, ...]
```

### Step 5: Test Validation

Validate all your data files against the new schemas:

```bash
source venv/bin/activate

# Test portfolio data
python3 partition-examples/tools/validate_multifile_schema.py \
  domains/agile/schemas/portfolio-agile.schema.yaml \
  portfolio-data.yaml

# Test program data
python3 partition-examples/tools/validate_multifile_schema.py \
  domains/agile/schemas/program-agile.schema.yaml \
  program-data.yaml

# Test team data
python3 partition-examples/tools/validate_multifile_schema.py \
  domains/agile/schemas/team-agile.schema.yaml \
  team-data.yaml

# Test delivery data
python3 partition-examples/tools/validate_multifile_schema.py \
  domains/agile/schemas/delivery-agile.schema.yaml \
  delivery-data.yaml

# Test SAFe data
python3 partition-examples/tools/validate_multifile_schema.py \
  domains/agile/schemas/safe-agile.schema.yaml \
  safe-data.yaml
```

## Common Migration Patterns

### Pattern 1: Epic to Feature Reference

**Before**: Internal `$ref`
```yaml
epic:
  id: epic_mobile
  features:
    - $ref: '#/$defs/feature/feat_ios'
```

**After**: String array reference
```yaml
epic:
  id: epic_mobile
  feature_refs:
    - feat_ios
```

### Pattern 2: Program to Team Reference

**Before**: Nested objects
```yaml
program:
  id: prg_mobile
  teams:
    - id: tm_ios
      members: [...]
    - id: tm_android
      members: [...]
```

**After**: ID references (teams defined separately)
```yaml
# In program data
program:
  id: prg_mobile
  team_refs:
    - tm_ios
    - tm_android

# In team data
teams:
  - id: tm_ios
    program_ref: prg_mobile
    members: [...]
  - id: tm_android
    program_ref: prg_mobile
    members: [...]
```

### Pattern 3: Cross-Partition References

**Before**: Everything in one schema
```yaml
user_story:
  id: us_login
  sprint: sp_2025_01  # Same schema
  feature: feat_auth  # Same schema
```

**After**: References across partitions
```yaml
# In delivery data (user_story)
user_story:
  id: us_login
  feature_ref: feat_auth  # References delivery partition
  sprint_ref: sp_2025_01  # References team partition
```

## Validation Differences

### Monolithic Schema Validation

```python
import jsonschema
import yaml

schema = yaml.safe_load(open('model.schema.yaml'))
data = yaml.safe_load(open('my-data.yaml'))

# Validates entire data structure
jsonschema.validate(data, schema)
```

### Partitioned Schema Validation

```python
from jsonschema import Draft202012Validator, Registry
import yaml

# Load all schemas
schemas = {}
for partition in ['portfolio', 'program', 'team', 'delivery', 'safe']:
    schema_file = f'schemas/{partition}-agile.schema.yaml'
    schema = yaml.safe_load(open(schema_file))
    schemas[schema['$id']] = schema

# Create registry
registry = Registry().with_resources([
    (schema['$id'], schema) for schema in schemas.values()
])

# Validate data against specific partition
data = yaml.safe_load(open('portfolio-data.yaml'))
validator = Draft202012Validator(schemas['portfolio'], registry=registry)
validator.validate(data)
```

## Benefits of Partitioning

### 1. Smaller Files
- **Before**: 1,972 lines in one file
- **After**: 183-659 lines per file (avg 505)
- **Benefit**: Easier to navigate, faster to load

### 2. Clearer Boundaries
- **Before**: All 35 concepts mixed together
- **After**: Organized by scale level (Portfolio → Program → Team → Delivery)
- **Benefit**: Clear separation of concerns

### 3. Flexible Usage
- **Before**: Must load entire schema even if only using sprints
- **After**: Load only what you need (e.g., just team + delivery)
- **Benefit**: Reduced memory footprint, faster validation

### 4. Better Collaboration
- **Before**: Multiple teams editing the same 1,972-line file
- **After**: Teams work on separate files (portfolio team, program team, etc.)
- **Benefit**: Fewer merge conflicts

### 5. Improved Clarity
- **Before**: Hard to understand relationships between concepts
- **After**: Clear partition boundaries show scale levels
- **Benefit**: Better onboarding, easier to learn

## Backward Compatibility

The original schema (`model.schema.yaml`) is **preserved** and will continue to be maintained:

- No breaking changes to existing systems
- Both schemas validate the same concepts
- Examples provided for both approaches
- Migration is optional, not required

## Timeline Recommendation

| Organization Size | Recommended Timeline |
|-------------------|---------------------|
| Small team (< 10) | 1-2 days |
| Medium team (10-50) | 1 week |
| Large org (50+) | 2-4 weeks |
| Enterprise (1000+) | 1-2 months (phased) |

## Getting Help

If you encounter issues during migration:

1. Check the [examples/partitioned/](examples/partitioned/) directory for reference
2. Review the [README.md](README.md) for schema details
3. Run validation with verbose output to see specific errors
4. Open an issue if you find gaps or problems

## Checklist

Use this checklist to track your migration:

- [ ] Identified which schemas I need (portfolio/program/team/delivery/safe)
- [ ] Updated cross-references from `$ref` to string ID references
- [ ] Updated validation scripts to use `validate_multifile_schema.py`
- [ ] Split data files by partition (optional)
- [ ] Validated all data files successfully
- [ ] Updated documentation to reference new schemas
- [ ] Trained team on new structure
- [ ] Updated CI/CD pipelines for new validation

## Summary

| Aspect | Monolithic | Partitioned |
|--------|-----------|-------------|
| **Files** | 1 | 5 |
| **Size** | 1,972 lines | 2,526 lines (505 avg) |
| **Concepts** | 35 (mixed) | 35 (organized) |
| **Cross-refs** | `$ref` | String IDs |
| **Scope** | All or nothing | Use what you need |
| **Collaboration** | Single file | Separate files |
| **Status** | Maintained | Recommended |

Choose the approach that best fits your needs - both are supported!
