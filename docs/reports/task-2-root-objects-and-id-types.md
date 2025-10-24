# Task 2: Root Object Requirements and ID Type Patterns

**Date**: 2025-10-23
**Analyst**: Claude (Sonnet 4.5)
**Scope**: Analyze root object necessity and ID type extraction patterns

---

## Executive Summary

The three schemas have different root object strategies, each with valid use cases. However, all schemas would benefit from consistent ID type extraction following the domain-stories pattern.

### Key Findings

- ✅ **Domain Stories Schema**: Has clear root (`DomainStory` aggregates all concepts) - CORRECT for this use case
- ❌ **Strategic DDD Schema**: No root object - should have `System` or `StrategicModel` as root
- ❌ **Tactical DDD Schema**: No root object - should have `BoundedContext` as root
- ⚠️ **ID Type Extraction**: Only domain-stories follows best practice; others need refactoring

---

## Part 1: Root Object Analysis

### 1.1 Domain Stories Schema

**Current State**: ✅ **HAS ROOT OBJECT**

```yaml
type: object
properties:
  version:
    type: string
  domain_stories:
    type: array
    minItems: 1
    items:
      $ref: "#/$defs/DomainStory"

required: [domain_stories]
```

#### Analysis

**Root Object**: `DomainStory` serves as the natural aggregation point

**Benefits**:
- ✅ Clear document structure
- ✅ DomainStory contains all tactical concepts (actors, aggregates, commands, etc.)
- ✅ Enforces containment hierarchy
- ✅ Easy validation (must have at least 1 domain story)
- ✅ Natural fit for markdown generation

**Scenarios When Root is Beneficial**:
1. **Complete domain story documents** - modeling a full user journey
2. **Story-centric analysis** - when the story is the unit of work
3. **Documentation generation** - stories as chapters/sections

**Scenarios When Root Might Not Be Needed**:
1. **Partial/incremental modeling** - adding one aggregate at a time
2. **Shared actor libraries** - defining actors separately from stories
3. **Aggregate catalogs** - listing aggregates without story context

#### Recommendation

**Keep root object**: `domain_stories` array as root

**Rationale**:
- Domain storytelling is inherently story-centric
- Stories are the primary organizational unit
- Alternative would be unclear (collection of disconnected types?)

**Proposed Enhancement**: Allow optional top-level arrays for shared definitions

```yaml
type: object
properties:
  version:
    type: string

  domain_stories:
    type: array
    minItems: 1
    items:
      $ref: "#/$defs/DomainStory"

  # Optional: Shared definitions used across multiple stories
  shared_actors:
    type: array
    items:
      $ref: "#/$defs/Actor"
    description: "Actors referenced by multiple domain stories"

  shared_aggregates:
    type: array
    items:
      $ref: "#/$defs/Aggregate"
    description: "Aggregates defined once, referenced by ID in stories"

required: [domain_stories]
```

This allows both:
1. **Embedded approach**: Stories contain all their actors/aggregates (current)
2. **Reference approach**: Stories reference shared definitions by ID (v2.0)

---

### 1.2 Strategic DDD Schema

**Current State**: ❌ **NO ROOT OBJECT**

```yaml
$defs:
  system:
    type: object
    # ...

  domain:
    type: object
    # ...

  bounded_context:
    type: object
    # ...

  context_mapping:
    type: object
    # ...

  bff_scope:
    type: object
    # ...

  bff_interface:
    type: object
    # ...

# NO top-level properties!
```

#### Analysis

**Problem**: No clear entry point - user doesn't know what to put at document root

**Current Usage Pattern** (assumed):
```yaml
# User must guess - probably something like:
system:
  id: sys_ecommerce
  name: E-Commerce Platform
  domains:
    - dom_customer
    - dom_order

domains:
  - id: dom_customer
    name: Customer Management
    # ...

  - id: dom_order
    name: Order Processing
    # ...

bounded_contexts:
  - id: bc_customer_profile
    # ...
```

But this isn't enforced or validated!

#### Should Strategic Schema Have a Root?

**YES** - Strong recommendation

**Proposed Root**: `System` as the natural container

**Rationale**:
1. **System is the highest-level concept** in strategic DDD
2. **One system per document** is the typical use case
3. **Clear containment hierarchy**: System → Domains → Bounded Contexts
4. **Matches mental model**: Modeling a software system, not random strategic concepts
5. **Enables validation**: Required fields, referential integrity
6. **Supports markdown generation**: System name = document title

#### Recommended Structure

```yaml
$schema: "https://json-schema.org/draft/2020-12/schema"
title: Strategic DDD Model
type: object

properties:
  system:
    $ref: "#/$defs/System"

  # Alternative: Allow multiple systems (rare but possible)
  # systems:
  #   type: array
  #   items: { $ref: "#/$defs/System" }

required: [system]

$defs:
  System:
    type: object
    required: [id, name, domains]
    properties:
      id: { $ref: "#/$defs/SysId" }
      name:
        type: string
      description:
        type: string
      version:
        type: string

      # Option A: Embed full definitions (current-ish)
      domains:
        type: array
        items: { $ref: "#/$defs/Domain" }

      bounded_contexts:
        type: array
        items: { $ref: "#/$defs/BoundedContext" }

      context_mappings:
        type: array
        items: { $ref: "#/$defs/ContextMapping" }

      bff_scopes:
        type: array
        items: { $ref: "#/$defs/BFFScope" }
```

**Usage Example**:
```yaml
system:
  id: sys_ecommerce
  name: E-Commerce Platform
  version: "1.0.0"
  description: "Our amazing e-commerce system"

  domains:
    - id: dom_customer
      name: Customer Management
      type: core
      bounded_contexts:
        - bc_customer_profile
        - bc_customer_auth

    - id: dom_order
      name: Order Processing
      type: core
      bounded_contexts:
        - bc_order_mgmt

  bounded_contexts:
    - id: bc_customer_profile
      name: Customer Profile
      domain_ref: dom_customer
      # ...

  context_mappings:
    - id: cm_order_to_customer
      upstream_context: bc_customer_profile
      downstream_context: bc_order_mgmt
      relationship_type: customer_supplier

  bff_scopes:
    - id: bff_web
      name: WebBFF
      client_type: web
      aggregates_from_contexts:
        - bc_customer_profile
        - bc_order_mgmt
```

#### Alternative: Multiple Root Options

For flexibility, could allow choosing root:

```yaml
type: object

properties:
  # Option 1: Full system modeling
  system:
    $ref: "#/$defs/System"

  # Option 2: Just domains (partial modeling)
  domains:
    type: array
    items: { $ref: "#/$defs/Domain" }

  # Option 3: Just bounded contexts (partial modeling)
  bounded_contexts:
    type: array
    items: { $ref: "#/$defs/BoundedContext" }

oneOf:
  - required: [system]
  - required: [domains]
  - required: [bounded_contexts]
```

**Scenarios**:
- Use `system` root for complete system modeling (99% case)
- Use `domains` root for domain catalog without full system context
- Use `bounded_contexts` root for BC catalog or partial modeling

#### Recommendation

**Recommended Root**: `system` (single object)

**Rationale**:
- Strategic DDD is about modeling software systems
- One document = one system (typical case)
- Provides clear entry point and validation
- Enables hierarchical documentation

**Scenarios When Root Not Needed**:
- Domain catalog (separate from system)
- Bounded context library/registry
- Context mapping visualization tool input

For these edge cases, **use separate schemas** rather than complicating main schema.

---

### 1.3 Tactical DDD Schema

**Current State**: ❌ **NO ROOT OBJECT**

```yaml
$defs:
  aggregate:
    type: object
    # ...

  entity:
    type: object
    # ...

  # ... etc - just type definitions
```

#### Analysis

**Problem**: Even worse than strategic - no guidance on document structure

**Critical Question**: What is the natural container for tactical concepts?

**Answer**: `BoundedContext`

**Rationale**:
1. **Tactical patterns are scoped to a bounded context** - aggregates, entities, services, etc. all belong to exactly one BC
2. **Bounded context is the consistency boundary** - everything inside shares ubiquitous language
3. **Matches DDD principle**: "All tactical objects belong to one bounded context"
4. **Current schema already acknowledges this**: Every tactical type has `bounded_context_ref` field!

#### Current Anti-Pattern

```yaml
# What users probably do now (unvalidated):
aggregates:
  - id: agg_customer
    name: Customer Aggregate
    bounded_context_ref: bc_customer_profile  # ← References BC
    # ...

  - id: agg_order
    name: Order Aggregate
    bounded_context_ref: bc_order_mgmt  # ← Different BC!
    # ...

entities:
  - id: ent_customer
    bounded_context_ref: bc_customer_profile
    # ...
```

**Problems**:
- Multiple bounded contexts mixed in one document (confusing!)
- No validation that all objects in BC actually declared
- Bounded context is just an ID reference (where is it defined?)
- Can't generate BC-scoped documentation

#### Recommended Structure

**Option A: BoundedContext as Root (Preferred)**

```yaml
$schema: "https://json-schema.org/draft/2020-12/schema"
title: Tactical DDD Model
type: object

properties:
  bounded_context:
    $ref: "#/$defs/BoundedContext"

required: [bounded_context]

$defs:
  BoundedContext:
    type: object
    required: [id, name, domain_ref]
    properties:
      id: { $ref: "#/$defs/BcId" }
      name:
        type: string
      domain_ref: { $ref: "#/$defs/DomId" }
      description:
        type: string

      # All tactical objects scoped to this BC
      aggregates:
        type: array
        items: { $ref: "#/$defs/Aggregate" }

      entities:
        type: array
        items: { $ref: "#/$defs/Entity" }

      value_objects:
        type: array
        items: { $ref: "#/$defs/ValueObject" }

      repositories:
        type: array
        items: { $ref: "#/$defs/Repository" }

      domain_services:
        type: array
        items: { $ref: "#/$defs/DomainService" }

      application_services:
        type: array
        items: { $ref: "#/$defs/ApplicationService" }

      domain_events:
        type: array
        items: { $ref: "#/$defs/DomainEvent" }

      command_interfaces:
        type: array
        items: { $ref: "#/$defs/CommandInterface" }

      query_interfaces:
        type: array
        items: { $ref: "#/$defs/QueryInterface" }

  # Remove bounded_context_ref from child types - it's implicit!
  Aggregate:
    type: object
    required: [id, name, root_ref]
    properties:
      id: { $ref: "#/$defs/AggId" }
      name:
        type: string
      # NO bounded_context_ref needed - parent provides context
      root_ref: { $ref: "#/$defs/EntId" }
      # ...
```

**Usage Example**:
```yaml
bounded_context:
  id: bc_customer_profile
  name: Customer Profile Context
  domain_ref: dom_customer
  description: "Manages customer identity and profile information"

  aggregates:
    - id: agg_customer
      name: Customer Aggregate
      root_ref: ent_customer
      entities:
        - ent_customer
        - ent_address
      value_objects:
        - vo_email
        - vo_phone

  entities:
    - id: ent_customer
      name: Customer
      is_aggregate_root: true
      identity_field: customer_id
      attributes:
        - name: customer_id
          type: ref
          value_object_ref: vo_customer_id
        - name: email
          type: ref
          value_object_ref: vo_email

  value_objects:
    - id: vo_customer_id
      name: CustomerId
      attributes:
        - name: id
          type: uuid

  repositories:
    - id: repo_customer
      name: CustomerRepository
      aggregate_ref: agg_customer

  application_services:
    - id: svc_app_customer_mgmt
      name: CustomerApplicationService
      implements_commands:
        - cmd_customer_commands
      implements_queries:
        - qry_customer_queries
```

**Benefits**:
- ✅ Clear scope: One document = one bounded context
- ✅ Implicit context: No need for `bounded_context_ref` in every type
- ✅ Validation: Can enforce BC-level invariants
- ✅ Documentation: BC = chapter/section
- ✅ Matches DDD mental model

**Option B: Multiple Bounded Contexts (Alternative)**

```yaml
properties:
  bounded_contexts:
    type: array
    minItems: 1
    items: { $ref: "#/$defs/BoundedContext" }

required: [bounded_contexts]
```

**Use Case**: Modeling multiple related BCs in one document (e.g., one domain = multiple BCs)

**Option C: Flexible Root (Most Flexible)**

```yaml
properties:
  # Option 1: Single BC (typical)
  bounded_context:
    $ref: "#/$defs/BoundedContext"

  # Option 2: Multiple BCs
  bounded_contexts:
    type: array
    items: { $ref: "#/$defs/BoundedContext" }

  # Option 3: Just aggregates (partial modeling - rare)
  aggregates:
    type: array
    items: { $ref: "#/$defs/Aggregate" }

oneOf:
  - required: [bounded_context]
  - required: [bounded_contexts]
  - required: [aggregates]
```

#### Recommendation

**Recommended Root**: `bounded_context` (single object)

**Rationale**:
1. **One document = one bounded context** is the natural unit
2. **Matches DDD principle**: Tactical patterns scoped to BC
3. **Removes redundant `bounded_context_ref`** from all child types
4. **Enables BC-level validation** (e.g., one repository per aggregate)
5. **Supports documentation generation** (BC = chapter)

**Scenarios When Root Not Needed**:
- Aggregate catalog across multiple BCs
- Entity library/reference
- Value object shared kernel

For these cases, **create separate schemas** (e.g., `shared-kernel.schema.yaml`)

**Important Note**: This is a **BREAKING CHANGE** from v1.x but essential for v2.0 correctness.

---

## Part 2: ID Type Extraction Analysis

### 2.1 Current State Comparison

| Schema | ID Types Extracted? | Location | Organization | Compliance |
|--------|---------------------|----------|--------------|------------|
| Domain Stories | ✅ YES | Lines 33-101 | Dedicated section with descriptions | 100% |
| Strategic DDD | ❌ NO | Inline everywhere | No organization | 0% |
| Tactical DDD | ❌ NO | Inline everywhere | No organization | 0% |

### 2.2 Domain Stories Pattern (Best Practice)

```yaml
$defs:
  # -----------------------------
  # ID types (lower_snake_case)
  # -----------------------------
  DstId:
    type: string
    pattern: "^dst_[a-z0-9_]+$"
    description: "Domain Story ID"

  ActId:
    type: string
    pattern: "^act_[a-z0-9_]+$"
    description: "Actor ID"

  CmdId:
    type: string
    pattern: "^cmd_[a-z0-9_]+$"
    description: "Command ID"

  # ... etc for all ID types

  # -----------------------------
  # Reusable components
  # -----------------------------
  Attribute:
    type: object
    # ...

  # -----------------------------
  # Core concepts
  # -----------------------------
  Actor:
    type: object
    properties:
      actor_id: { $ref: "#/$defs/ActId" }  # ← Uses ID type
```

**Benefits**:
1. ✅ **Single source of truth** for ID patterns
2. ✅ **Easy to change** pattern globally
3. ✅ **Self-documenting** with descriptions
4. ✅ **Reusable** across multiple properties
5. ✅ **Clear organization** - readers see all IDs at once

### 2.3 Strategic Schema ID Types to Extract

```yaml
$defs:
  # =====================================
  # ID TYPES
  # =====================================

  SysId:
    type: string
    pattern: "^sys_[a-z0-9_]+$"
    description: "System identifier"
    examples:
      - "sys_ecommerce"
      - "sys_crm"

  DomId:
    type: string
    pattern: "^dom_[a-z0-9_]+$"
    description: "Domain identifier"
    examples:
      - "dom_customer"
      - "dom_order"

  BcId:
    type: string
    pattern: "^bc_[a-z0-9_]+$"
    description: "Bounded Context identifier"
    examples:
      - "bc_customer_profile"
      - "bc_order_mgmt"

  CmId:
    type: string
    pattern: "^cm_[a-z0-9_]+_to_[a-z0-9_]+$"
    description: "Context Mapping identifier"
    examples:
      - "cm_order_to_customer"
      - "cm_inventory_to_shipping"

  BffId:
    type: string
    pattern: "^bff_[a-z0-9_]+$"
    description: "BFF Scope identifier"
    examples:
      - "bff_web"
      - "bff_ios"
      - "bff_android"

  BffIfId:
    type: string
    pattern: "^bff_if_[a-z0-9_]+$"
    description: "BFF Interface identifier"
    examples:
      - "bff_if_user_web"
      - "bff_if_order_ios"

  # =====================================
  # COMMON TYPES
  # =====================================
  # (moved from inline definitions - see Task 1)
```

**Current Occurrences to Replace**:

```yaml
# BEFORE (inline pattern - appears ~20 times):
id:
  type: string
  pattern: "^bc_[a-z0-9_]+$"

# AFTER (reference):
id: { $ref: "#/$defs/BcId" }
```

### 2.4 Tactical Schema ID Types to Extract

```yaml
$defs:
  # =====================================
  # ID TYPES
  # =====================================

  BcId:
    type: string
    pattern: "^bc_[a-z0-9_]+$"
    description: "Bounded Context identifier (references strategic schema)"
    examples:
      - "bc_customer_profile"

  AggId:
    type: string
    pattern: "^agg_[a-z0-9_]+$"
    description: "Aggregate identifier"
    examples:
      - "agg_customer"
      - "agg_order"

  EntId:
    type: string
    pattern: "^ent_[a-z0-9_]+$"
    description: "Entity identifier"
    examples:
      - "ent_customer"
      - "ent_order_line"

  VoId:
    type: string
    pattern: "^vo_[a-z0-9_]+$"
    description: "Value Object identifier"
    examples:
      - "vo_email"
      - "vo_customer_id"

  RepoId:
    type: string
    pattern: "^repo_[a-z0-9_]+$"
    description: "Repository identifier"
    examples:
      - "repo_customer"
      - "repo_order"

  SvcDomId:
    type: string
    pattern: "^svc_dom_[a-z0-9_]+$"
    description: "Domain Service identifier"
    examples:
      - "svc_dom_pricing"
      - "svc_dom_credit_check"

  SvcAppId:
    type: string
    pattern: "^svc_app_[a-z0-9_]+$"
    description: "Application Service identifier"
    examples:
      - "svc_app_user_management"
      - "svc_app_order_processing"

  CmdId:
    type: string
    pattern: "^cmd_[a-z0-9_]+$"
    description: "Command Interface identifier"
    examples:
      - "cmd_user_commands"
      - "cmd_order_commands"

  QryId:
    type: string
    pattern: "^qry_[a-z0-9_]+$"
    description: "Query Interface identifier"
    examples:
      - "qry_user_queries"
      - "qry_order_queries"

  EvtId:
    type: string
    pattern: "^evt_[a-z0-9_]+$"
    description: "Domain Event identifier"
    examples:
      - "evt_user_created"
      - "evt_order_placed"

  # =====================================
  # COMMON TYPES
  # =====================================
  # (Parameter, Attribute, Method, etc. - see Task 1)
```

**Current Occurrences to Replace**: ~50+ inline pattern definitions

### 2.5 Recommended Organization Structure

Following domain-stories pattern, each schema should have:

```yaml
$defs:
  # =====================================
  # SECTION 1: ID TYPES (lower_snake_case)
  # =====================================
  # All ID type definitions with:
  # - type, pattern, description, examples

  TypeId:
    type: string
    pattern: "^type_[a-z0-9_]+$"
    description: "Clear description"
    examples:
      - "type_example_1"
      - "type_example_2"

  # =====================================
  # SECTION 2: COMMON/REUSABLE TYPES
  # =====================================
  # Shared types used across multiple domain types
  # - Parameter, Attribute, Method, etc.

  Parameter:
    type: object
    required: [name, type]
    properties:
      # ...

  # =====================================
  # SECTION 3: DOMAIN TYPES (PascalCase or snake_case)
  # =====================================
  # Main domain/tactical/strategic concepts

  Aggregate:
    type: object
    required: [id, name]
    properties:
      id: { $ref: "#/$defs/AggId" }  # ← References ID type
      name:
        type: string
      # ...
```

### 2.6 Benefits of ID Type Extraction

#### Single Source of Truth

**BEFORE** (Strategic schema - BcId pattern appears 15+ times):
```yaml
# In bounded_context definition:
id:
  type: string
  pattern: "^bc_[a-z0-9_]+$"

# In domain.bounded_contexts:
items:
  type: string
  pattern: "^bc_[a-z0-9_]+$"

# In system.bounded_contexts:
items:
  type: string
  pattern: "^bc_[a-z0-9_]+$"

# In context_mapping.upstream_context:
type: string
pattern: "^bc_[a-z0-9_]+$"

# In context_mapping.downstream_context:
type: string
pattern: "^bc_[a-z0-9_]+$"

# In bff_scope.aggregates_from_contexts:
items:
  type: string
  pattern: "^bc_[a-z0-9_]+$"

# ... etc (15+ occurrences)
```

**AFTER** (ID type extracted):
```yaml
# Define once:
BcId:
  type: string
  pattern: "^bc_[a-z0-9_]+$"

# Reference everywhere:
id: { $ref: "#/$defs/BcId" }
items: { $ref: "#/$defs/BcId" }
upstream_context: { $ref: "#/$defs/BcId" }
# ... etc
```

**Impact of Change**:
- **BEFORE**: Need to update pattern in 15+ places
- **AFTER**: Update once, applies everywhere

#### Self-Documentation

```yaml
BcId:
  type: string
  pattern: "^bc_[a-z0-9_]+$"
  description: "Bounded Context identifier - references a context from strategic schema"
  examples:
    - "bc_customer_profile"
    - "bc_order_management"
    - "bc_inventory"
```

Readers immediately understand:
- What this ID represents
- The naming pattern
- Examples of valid IDs

#### Validation Messages

**BEFORE**:
```
Error: Value "customer_profile" does not match pattern "^bc_[a-z0-9_]+$" at /bounded_context/id
```

**AFTER** (some validators show $ref path):
```
Error: Value "customer_profile" does not match BcId pattern at /bounded_context/id
Expected pattern: ^bc_[a-z0-9_]+$
Examples: bc_customer_profile, bc_order_management
```

### 2.7 Naming Convention Consistency

#### Current State (Inconsistent)

Domain stories uses `TitleCase` (e.g., `ActId`, `CmdId`)
Strategic/Tactical have NO ID types, but imply `snake_case` (e.g., would be `bc_id`, `agg_id`)

#### Recommendation

**Use `TitleCase`** for ID type names (matches domain-stories):

```yaml
# ID Types in TitleCase:
BcId       # Bounded Context ID
AggId      # Aggregate ID
EntId      # Entity ID
VoId       # Value Object ID
SvcAppId   # Application Service ID

# Domain Types in snake_case (current):
bounded_context
aggregate
entity
value_object
application_service
```

**Rationale**:
- Distinguishes ID types from domain types visually
- Matches JSON Schema convention for `$defs` (both are allowed)
- Aligns with domain-stories existing pattern
- Easier to read in references: `$ref: "#/$defs/BcId"` vs `$ref: "#/$defs/bc_id"`

---

## Part 3: Recommendations Summary

### 3.1 Root Objects

| Schema | Recommendation | Root Type | Rationale |
|--------|----------------|-----------|-----------|
| Domain Stories | ✅ Keep current | `domain_stories` array | Story-centric, correct model |
| Strategic DDD | ⚠️ Add root | `system` object | System is natural container |
| Tactical DDD | ⚠️ Add root | `bounded_context` object | BC is natural scope for tactical concepts |

### 3.2 ID Type Extraction

| Schema | Action Required | ID Types Count | Priority |
|--------|-----------------|----------------|----------|
| Domain Stories | ✅ None (already done) | 12 types | N/A |
| Strategic DDD | ❌ Extract all | 6 types | HIGH |
| Tactical DDD | ❌ Extract all | 10 types | HIGH |

### 3.3 Organization Structure

All schemas should follow three-section pattern:

1. **ID Types** (TitleCase) - Single source of truth for ID patterns
2. **Common Types** (reusable) - Shared across domain types
3. **Domain Types** (snake_case) - Main concepts

### 3.4 Migration Impact

#### Strategic Schema

**Breaking Change**: YES

```yaml
# v1.x (no root):
domains:
  - id: dom_customer
    # ...

# v2.0 (with root):
system:
  id: sys_ecommerce
  domains:
    - id: dom_customer
      # ...
```

**Migration Strategy**: Wrap existing documents in `system` object

#### Tactical Schema

**Breaking Change**: YES

```yaml
# v1.x (no root, with bounded_context_ref):
aggregates:
  - id: agg_customer
    bounded_context_ref: bc_customer_profile
    # ...

# v2.0 (with root, implicit context):
bounded_context:
  id: bc_customer_profile
  aggregates:
    - id: agg_customer
      # bounded_context_ref removed - implicit
      # ...
```

**Migration Strategy**: Group by bounded_context, create one document per BC

---

## Conclusion

Root objects are essential for v2.0 schemas to provide:
- Clear document structure
- Entry point for validation
- Hierarchical organization
- Support for markdown generation
- Alignment with DDD mental models

ID type extraction is equally critical for:
- Maintainability (single source of truth)
- Consistency (reuse across properties)
- Documentation (examples and descriptions)
- Validation (better error messages)

Both changes are breaking but necessary for a well-structured v2.0.
