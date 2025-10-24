# Task 3: Cross-Schema Common Types Feasibility

**Date**: 2025-10-23
**Analyst**: Claude (Sonnet 4.5)
**Scope**: Evaluate feasibility and best practices for sharing common types across schemas

---

## Executive Summary

Cross-schema references via `$ref` are **technically feasible** but come with significant complexity and tooling limitations. The recommendation is to **use controlled duplication with clear documentation** rather than external file references for the v2.0 schemas.

### Key Findings

- ✅ **Technical Feasibility**: Supported by major validators with configuration
- ⚠️ **Tooling Complexity**: Requires manual schema pre-loading or custom loaders
- ❌ **Portability Issues**: Inconsistent `file://` protocol support
- ✅ **Alternative Approach**: Controlled duplication with centralized documentation

### Recommendation

**DO NOT use external `$ref` for v2.0** - Instead use **documented duplication pattern** with:
1. Common types documented in a reference guide
2. Copy-paste pattern across schemas
3. Version management for type definitions
4. Clear attribution in each schema

---

## Part 1: Validator Support Analysis

### 1.1 Technical Feasibility Summary

Based on research into major JSON Schema validators:

| Validator | Language | External $ref Support | Auto-Loading | Pre-Loading Required | YAML Support | Recommendation |
|-----------|----------|----------------------|--------------|----------------------|--------------|----------------|
| **ajv** | JavaScript | ✅ Yes | ❌ No | ✅ Yes | Via parser | Configure with `loadSchema` |
| **jsonschema** | Python | ✅ Yes | ❌ No | ✅ Yes | Yes | Use Registry API (v4.18+) |
| **networknt** | Java | ✅ Yes | ❌ No | ✅ Yes | Via parser | URI-based resolution |
| **json-schema-ref-parser** | JavaScript | ✅ Yes | ✅ Yes | ❌ No | ✅ Yes | **Best for bundling** |

**Key Finding**: **NO validator automatically loads external files by default**

### 1.2 How External References Work

#### Example File Structure
```
/schemas/
  common/
    id-types.yaml
    common-types.yaml
  ddd/
    strategic-ddd.schema.yaml
    tactical-ddd.schema.yaml
  domain-stories/
    domain-stories-schema.yaml
```

#### Common Types File

**/schemas/common/id-types.yaml**:
```yaml
$schema: "https://json-schema.org/draft/2020-12/schema"
$id: "https://canonical-grounding.org/schemas/common/id-types.yaml"

$defs:
  BcId:
    type: string
    pattern: "^bc_[a-z0-9_]+$"
    description: "Bounded Context identifier"
    examples:
      - "bc_customer_profile"
      - "bc_order_mgmt"

  AggId:
    type: string
    pattern: "^agg_[a-z0-9_]+$"
    description: "Aggregate identifier"
    examples:
      - "agg_customer"
      - "agg_order"

  # ... more ID types
```

**/schemas/common/common-types.yaml**:
```yaml
$schema: "https://json-schema.org/draft/2020-12/schema"
$id: "https://canonical-grounding.org/schemas/common/common-types.yaml"

$defs:
  Parameter:
    type: object
    required: [name, type]
    properties:
      name:
        type: string
        pattern: "^[a-z][a-z0-9_]*$"
      type:
        type: string
        enum: [string, integer, number, boolean, date, datetime, uuid, money, enum, json, ref]
      required:
        type: boolean
        default: true
      description:
        type: string

  Attribute:
    type: object
    required: [name, type]
    properties:
      name:
        type: string
        pattern: "^[a-z][a-z0-9_]*$"
      type:
        type: string
        enum: [string, integer, number, boolean, date, datetime, uuid, money, enum, json, ref]
      ref_id:
        type: string
      required:
        type: boolean
        default: false
      description:
        type: string

  Method:
    type: object
    required: [name]
    properties:
      name:
        type: string
        pattern: "^[a-z][a-z0-9_]*$"
      parameters:
        type: array
        items:
          $ref: "#/$defs/Parameter"
      return_type:
        type: string
      description:
        type: string
```

#### Using External References

**/schemas/ddd/tactical-ddd.schema.yaml**:
```yaml
$schema: "https://json-schema.org/draft/2020-12/schema"
$id: "https://canonical-grounding.org/schemas/ddd/tactical-ddd.schema.yaml"

title: Tactical DDD Schema
type: object

$defs:
  # Import ID types from common schema
  BcId:
    $ref: "../common/id-types.yaml#/$defs/BcId"

  AggId:
    $ref: "../common/id-types.yaml#/$defs/AggId"

  # Import common types
  Parameter:
    $ref: "../common/common-types.yaml#/$defs/Parameter"

  Attribute:
    $ref: "../common/common-types.yaml#/$defs/Attribute"

  # Domain-specific types
  Aggregate:
    type: object
    properties:
      id:
        $ref: "#/$defs/AggId"  # ← Uses imported ID type
      attributes:
        type: array
        items:
          $ref: "#/$defs/Attribute"  # ← Uses imported common type
```

### 1.3 Validator Configuration Examples

#### Python (jsonschema with Registry)

```python
from pathlib import Path
import yaml
from referencing import Registry, Resource
from jsonschema.validators import validator_for

# Load all schemas
schema_dir = Path("schemas")

id_types = yaml.safe_load((schema_dir / "common/id-types.yaml").read_text())
common_types = yaml.safe_load((schema_dir / "common/common-types.yaml").read_text())
tactical_schema = yaml.safe_load((schema_dir / "ddd/tactical-ddd.schema.yaml").read_text())

# Create registry with all schemas
registry = (
    Registry()
    .with_resource(id_types["$id"], Resource.from_contents(id_types))
    .with_resource(common_types["$id"], Resource.from_contents(common_types))
)

# Validate using tactical schema
Validator = validator_for(tactical_schema)
validator = Validator(tactical_schema, registry=registry)

# Now validation works with external refs
validator.validate(instance_data)
```

#### JavaScript (ajv with loadSchema)

```javascript
const Ajv = require("ajv");
const fs = require("fs");
const path = require("path");
const yaml = require("js-yaml");

// Custom schema loader
async function loadSchema(uri) {
  // Convert URI to file path
  const filePath = uri.replace("https://canonical-grounding.org/schemas/", "schemas/");
  const content = fs.readFileSync(filePath, "utf8");
  return yaml.load(content);
}

// Create AJV instance with async loading
const ajv = new Ajv({ loadSchema });

// Compile schema (loads external refs automatically)
const validate = await ajv.compileAsync(tacticalSchema);

// Validate
const valid = validate(instanceData);
```

#### JavaScript (json-schema-ref-parser for bundling)

```javascript
const $RefParser = require("@apidevtools/json-schema-ref-parser");

// Bundle all external refs into single schema
const bundledSchema = await $RefParser.bundle("schemas/ddd/tactical-ddd.schema.yaml");

// Now bundledSchema has all refs inlined - no external files needed
// Can distribute this single file
```

---

## Part 2: Pros and Cons Analysis

### 2.1 Advantages of External References

#### ✅ Single Source of Truth

**Scenario**: Change `BcId` pattern from `^bc_[a-z0-9_]+$` to `^bc_[a-z][a-z0-9_]*$`

**With external ref**:
```yaml
# Edit once in common/id-types.yaml
BcId:
  pattern: "^bc_[a-z][a-z0-9_]*$"  # ← Changed here

# Automatically applies to:
# - strategic-ddd.schema.yaml
# - tactical-ddd.schema.yaml
# - domain-stories-schema.yaml
```

**Without external ref**:
- Must edit pattern in 3 files
- Risk of inconsistency if one is missed

#### ✅ DRY Principle

**Common types defined once**:
- `Parameter` appears in all 3 schemas
- `Attribute` appears in domain-stories and tactical
- ID types overlap between schemas

**Impact**:
- ~200 lines of duplicate YAML eliminated
- Easier to maintain consistency

#### ✅ Versioning

```
/schemas/common/
  v1/
    id-types.yaml
    common-types.yaml
  v2/
    id-types.yaml
    common-types.yaml

# Schemas can reference specific versions:
$ref: "../common/v1/id-types.yaml#/$defs/BcId"
```

### 2.2 Disadvantages of External References

#### ❌ Tooling Complexity

**Every user must**:
1. Pre-load all schemas OR configure custom loader
2. Understand `$id` vs file path resolution
3. Deal with validator-specific quirks
4. Handle YAML parsing if validator doesn't support it

**Example pain point**:
```python
# User expects this to work:
with open("tactical-ddd.schema.yaml") as f:
    schema = yaml.safe_load(f)

validate(data, schema)  # ❌ FAILS - external refs not loaded!

# Actually need this:
# ... 20 lines of setup code to configure registry ...
```

#### ❌ Portability Issues

**file:// protocol not standardized**:
- Works differently across validators
- Absolute vs relative path confusion
- Windows vs Unix path separators
- May not work in deployed environments (web, containers)

**$id URI vs file path**:
```yaml
# Which to use?
$ref: "file:../common/id-types.yaml#/$defs/BcId"  # ← File path
$ref: "https://canonical-grounding.org/schemas/common/id-types.yaml#/$defs/BcId"  # ← URI
$ref: "../common/id-types.yaml#/$defs/BcId"  # ← Relative path

# Answer: Depends on validator! 😱
```

#### ❌ Distribution Complexity

**Single-file distribution broken**:
```
# Users can't just download tactical-ddd.schema.yaml
# They need entire schemas/ directory structure:

schemas/
  common/
    id-types.yaml          ← Required
    common-types.yaml      ← Required
  ddd/
    tactical-ddd.schema.yaml  ← Main schema
```

**Workaround**: Bundle before distribution (adds build step)

#### ❌ IDE/Editor Support

**Limited tooling**:
- VSCode YAML extension doesn't auto-resolve external refs
- No autocomplete across files
- Validation errors point to wrong file
- Harder to debug schema issues

#### ❌ Performance

**Multiple file I/O**:
- Each validation loads 3+ files instead of 1
- Network latency if using HTTP URIs
- Caching complexity

### 2.3 Comparison Matrix

| Aspect | External $ref | Inline Duplication |
|--------|---------------|-------------------|
| **Maintainability** | ✅ Excellent (single source) | ⚠️ Moderate (sync manually) |
| **Consistency** | ✅ Guaranteed | ⚠️ Risk of drift |
| **User Experience** | ❌ Complex setup required | ✅ Simple (just load file) |
| **Portability** | ❌ Validator-dependent | ✅ Works everywhere |
| **Distribution** | ❌ Multi-file required | ✅ Single file |
| **IDE Support** | ❌ Limited | ✅ Full support |
| **Performance** | ⚠️ Multiple files | ✅ Single file |
| **Debugging** | ❌ Harder | ✅ Easier |
| **Version Management** | ✅ Explicit | ⚠️ Implicit |

---

## Part 3: Alternative Approaches

### 3.1 Approach A: Controlled Duplication (Recommended)

**Strategy**: Duplicate common types but manage centrally

#### Documentation-Driven Pattern

**/schemas/common/common-type-definitions.md**:
```markdown
# Common Type Definitions

This document contains canonical definitions for types shared across schemas.

**Usage**: Copy-paste into your schema's `$defs` section with attribution comment.

**Versioning**: Each type has version number - update both here and in schemas.

---

## ID Types (v1.0.0)

### BcId

**Version**: 1.0.0
**Last Updated**: 2025-10-23

\`\`\`yaml
BcId:
  type: string
  pattern: "^bc_[a-z0-9_]+$"
  description: "Bounded Context identifier"
  examples:
    - "bc_customer_profile"
    - "bc_order_mgmt"
\`\`\`

**Used In**:
- strategic-ddd.schema.yaml
- tactical-ddd.schema.yaml

---

### AggId

**Version**: 1.0.0

\`\`\`yaml
AggId:
  type: string
  pattern: "^agg_[a-z0-9_]+$"
  description: "Aggregate identifier"
  examples:
    - "agg_customer"
    - "agg_order"
\`\`\`

**Used In**:
- tactical-ddd.schema.yaml
- domain-stories-schema.yaml

---

## Common Types (v1.0.0)

### Parameter

**Version**: 1.0.0

\`\`\`yaml
Parameter:
  type: object
  required: [name, type]
  properties:
    name:
      type: string
      pattern: "^[a-z][a-z0-9_]*$"
    type:
      type: string
      enum: [string, integer, number, boolean, date, datetime, uuid, money, enum, json, ref]
    required:
      type: boolean
      default: true
    description:
      type: string
\`\`\`

**Used In**:
- tactical-ddd.schema.yaml (commands, queries, operations)
- domain-stories-schema.yaml (commands, operations)

---
```

#### Schema Attribution Pattern

**/schemas/ddd/tactical-ddd.schema.yaml**:
```yaml
$defs:
  # =====================================
  # ID TYPES
  # Canonical definitions: /schemas/common/common-type-definitions.md
  # Version: 1.0.0
  # Last synced: 2025-10-23
  # =====================================

  BcId:
    type: string
    pattern: "^bc_[a-z0-9_]+$"
    description: "Bounded Context identifier"
    examples:
      - "bc_customer_profile"

  AggId:
    type: string
    pattern: "^agg_[a-z0-9_]+$"
    description: "Aggregate identifier"
    examples:
      - "agg_customer"

  # =====================================
  # COMMON TYPES
  # Canonical definitions: /schemas/common/common-type-definitions.md
  # Version: 1.0.0
  # Last synced: 2025-10-23
  # =====================================

  Parameter:
    type: object
    required: [name, type]
    properties:
      name:
        type: string
        pattern: "^[a-z][a-z0-9_]*$"
      type:
        type: string
        enum: [string, integer, number, boolean, date, datetime, uuid, money, enum, json, ref]
      required:
        type: boolean
        default: true
      description:
        type: string
```

#### Benefits

✅ **Simple**: No validator configuration needed
✅ **Portable**: Works with all validators
✅ **Debuggable**: Everything in one file
✅ **IDE-friendly**: Full autocomplete and validation
✅ **Distributable**: Single file per schema
✅ **Version-controlled**: Git tracks each schema independently
✅ **Documented**: Clear attribution and sync date

#### Maintenance Process

1. **Update canonical definition** in `common-type-definitions.md`
2. **Bump version number** (e.g., 1.0.0 → 1.1.0)
3. **Update each schema** that uses the type
4. **Update "Last synced" comment** in each schema
5. **Git commit** shows exactly what changed

#### Sync Checking Script

```bash
#!/bin/bash
# check-schema-sync.sh

# Extract version from common definitions
CANONICAL_VERSION=$(grep "Version: " schemas/common/common-type-definitions.md | head -n1 | awk '{print $3}')

# Check each schema's version comment
for schema in schemas/**/*.yaml; do
    SCHEMA_VERSION=$(grep "# Version: " $schema | awk '{print $3}')

    if [ "$SCHEMA_VERSION" != "$CANONICAL_VERSION" ]; then
        echo "⚠️  $schema is out of sync (has $SCHEMA_VERSION, canonical is $CANONICAL_VERSION)"
    fi
done
```

### 3.2 Approach B: External References with Bundling

**Strategy**: Develop with external refs, bundle for distribution

#### Development Setup

```
/schemas/
  src/                           ← Source schemas with external refs
    common/
      id-types.yaml
      common-types.yaml
    ddd/
      strategic-ddd.schema.yaml
      tactical-ddd.schema.yaml

  dist/                          ← Bundled schemas (generated)
    strategic-ddd.schema.yaml   ← All refs inlined
    tactical-ddd.schema.yaml    ← All refs inlined
```

#### Build Script

```javascript
// bundle-schemas.js
const $RefParser = require("@apidevtools/json-schema-ref-parser");
const fs = require("fs");
const path = require("path");

async function bundleSchema(inputPath, outputPath) {
    // Bundle all external refs into single file
    const bundled = await $RefParser.bundle(inputPath);

    // Write to dist/
    fs.writeFileSync(outputPath, JSON.stringify(bundled, null, 2));
    console.log(`✅ Bundled ${inputPath} → ${outputPath}`);
}

// Bundle all schemas
await bundleSchema(
    "schemas/src/ddd/tactical-ddd.schema.yaml",
    "schemas/dist/tactical-ddd.schema.yaml"
);

await bundleSchema(
    "schemas/src/ddd/strategic-ddd.schema.yaml",
    "schemas/dist/strategic-ddd.schema.yaml"
);
```

#### Pros

✅ DRY in development
✅ Simple distribution (single files in `dist/`)
✅ No validator configuration for end users
✅ Automated with build step

#### Cons

❌ Requires build step
❌ Adds tooling dependency (json-schema-ref-parser)
❌ Source ≠ distribution (confusing for contributors)
❌ Need to document which files are canonical

### 3.3 Approach C: Hybrid (Best of Both)

**Strategy**: Use controlled duplication + optional bundling tool

#### Core Principle

Schemas are **standalone and self-contained** (approach A), but provide **optional bundling tool** for those who want external refs (approach B).

#### Setup

```
/schemas/
  strategic-ddd.schema.yaml      ← Standalone (duplicated types)
  tactical-ddd.schema.yaml       ← Standalone (duplicated types)
  domain-stories-schema.yaml     ← Standalone (duplicated types)

  common/
    common-type-definitions.md   ← Documentation (canonical)

  tools/
    extract-common-types.js      ← Tool to extract shared types
    split-schemas.js             ← Tool to create external ref version
```

#### Users Choose Their Approach

**Option 1: Simple (Default)**
```bash
# Just use the schema files directly
validator tactical-ddd.schema.yaml instance.yaml
```

**Option 2: Advanced (External Refs)**
```bash
# Run tool to split into external refs
node tools/split-schemas.js

# Creates schemas-with-refs/ directory
validator schemas-with-refs/tactical-ddd.schema.yaml instance.yaml
```

---

## Part 4: Recommendation

### 4.1 Recommended Approach for v2.0

**Use Approach A: Controlled Duplication**

#### Rationale

1. **User Experience Priority**: Simplicity for users outweighs maintainer convenience
2. **Tool Independence**: Works with all validators without configuration
3. **Single-File Distribution**: Users can download and use immediately
4. **IDE Support**: Full autocomplete and validation
5. **Debuggability**: All schema content visible in one file
6. **Git-Friendly**: Clear change tracking
7. **Low Barrier**: No build tools or complex setup

#### Implementation Plan

1. **Create** `/schemas/common/common-type-definitions.md`
   - Document all shared types with versions
   - Include usage examples
   - List which schemas use each type

2. **Add version comments** to each schema
   ```yaml
   # Common Type Definitions v1.0.0
   # Canonical source: /schemas/common/common-type-definitions.md
   # Last synced: 2025-10-23
   ```

3. **Create sync-check script** in `/tools/check-schema-sync.sh`
   - Warns if schema versions out of date
   - Part of CI/CD pipeline

4. **Document maintenance process** in `/docs/SCHEMA_MAINTENANCE.md`
   - How to update common types
   - How to sync across schemas
   - Version bumping rules

### 4.2 Future Enhancement Option

**Provide opt-in bundling tool** (Approach C) for users who want external refs:

```bash
# Generate external-ref version (advanced users only)
npm run schemas:split

# This creates schemas-external/ with separate common files
# Most users ignore this
```

This gives best of both worlds:
- Default: Simple standalone schemas
- Advanced: External refs for those who want them

---

## Part 5: Shared Types to Document

### 5.1 ID Types (Used by Multiple Schemas)

| ID Type | Strategic | Tactical | Domain Stories | Pattern |
|---------|-----------|----------|----------------|---------|
| BcId | ✅ | ✅ | ❌ | `^bc_[a-z0-9_]+$` |
| AggId | ✅ | ✅ | ✅ | `^agg_[a-z0-9_]+$` |
| CmdId | ❌ | ✅ | ✅ | `^cmd_[a-z0-9_]+$` |
| QryId | ❌ | ✅ | ✅ | `^qry_[a-z0-9_]+$` |
| EvtId | ❌ | ✅ | ✅ | `^evt_[a-z0-9_]+$` |
| SvcAppId | ✅ | ✅ | ✅ | `^svc_app_[a-z0-9_]+$` |
| SvcDomId | ✅ | ✅ | ✅ | `^svc_dom_[a-z0-9_]+$` |
| RepoId | ✅ | ✅ | ✅ | `^repo_[a-z0-9_]+$` |

**Recommendation**: Document all 8 shared ID types in common-type-definitions.md

### 5.2 Common Types (Used by Multiple Schemas)

| Type | Strategic | Tactical | Domain Stories | Lines of YAML |
|------|-----------|----------|----------------|---------------|
| Parameter | ❌ | ✅ | ✅ | ~20 |
| Attribute | ❌ | ✅ | ✅ | ~20 |
| Method/Operation | ❌ | ✅ | ✅ | ~15 |

**Recommendation**: Document these 3 common types

### 5.3 Total Duplication Eliminated

**With external refs**: ~400 lines of YAML saved across schemas
**With documented duplication**: ~0 lines saved, but consistency ensured

**Trade-off Accepted**: Extra ~400 lines of duplicated YAML is acceptable cost for simplicity.

---

## Conclusion

While external `$ref` is technically feasible, the **complexity cost outweighs benefits** for this project.

**v2.0 Approach**:
1. ✅ Use controlled duplication
2. ✅ Document canonical definitions in markdown
3. ✅ Add version comments and sync dates
4. ✅ Provide sync-check tooling
5. ⏸️ Optional: Provide bundling tool (future enhancement)

This approach prioritizes **user experience and tool independence** while still maintaining **consistency through documentation and process**.
