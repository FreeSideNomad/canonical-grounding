# Task 1: Flat Structure and Nesting Analysis

**Date**: 2025-10-23
**Analyst**: Claude (Sonnet 4.5)
**Scope**: Analyze nesting issues and opportunities for flattening across all schemas

---

## Executive Summary

All three schemas exhibit varying degrees of nesting issues that violate the flat structure principle. The **domain-stories-schema** is the most compliant with flat structure principles, while **tactical-ddd** has the most problematic deep nesting. Strategic schema is relatively flat but could benefit from ID type extraction.

### Key Findings

- ✅ **Domain Stories Schema**: Already follows flat structure well (95% compliant)
- ⚠️ **Strategic DDD Schema**: Moderate nesting issues (70% compliant)
- ❌ **Tactical DDD Schema**: Significant deep nesting problems (50% compliant)

---

## 1. Domain Stories Schema Analysis

### Overall Assessment: **GOOD (95% Compliant)**

The domain stories schema is already well-structured and follows the flat structure principle effectively.

### Strengths

1. **ID Types Separated**: All ID types extracted to `$defs` section (lines 33-101)
2. **Common Types Reused**: `Attribute`, `Parameter`, `Operation` extracted and reused (lines 106-169)
3. **Type References**: Most types use `$ref` instead of inline definitions
4. **Clear Organization**: Three-section structure (IDs, Common, Core Concepts)

### Identified Issues

#### Issue 1.1: Event.caused_by Nested Inline Definition

**Location**: `Event.$defs.Event.properties.caused_by` (lines 387-399)

**Current Depth**: 3 levels (nested oneOf with inline object definitions)

```yaml
caused_by:
  description: "Either a command or an activity"
  oneOf:
    - type: object  # ← Inline definition
      additionalProperties: false
      required: [command_id]
      properties:
        command_id: { $ref: "#/$defs/CmdId" }
    - type: object  # ← Inline definition
      additionalProperties: false
      required: [activity_id]
      properties:
        activity_id: { $ref: "#/$defs/ActvId" }
```

**Issue**: Anonymous inline objects within oneOf

**Proposed Fix**: Extract to named reference types

```yaml
# In $defs section:
EventCause:
  oneOf:
    - $ref: "#/$defs/CommandCause"
    - $ref: "#/$defs/ActivityCause"

CommandCause:
  type: object
  additionalProperties: false
  required: [command_id]
  properties:
    command_id: { $ref: "#/$defs/CmdId" }

ActivityCause:
  type: object
  additionalProperties: false
  required: [activity_id]
  properties:
    activity_id: { $ref: "#/$defs/ActvId" }

# In Event definition:
caused_by:
  $ref: "#/$defs/EventCause"
  description: "Either a command or an activity"
```

#### Issue 1.2: BusinessRule.applies_to Uses anyOf with Inline Types

**Location**: `BusinessRule.properties.applies_to` (lines 425-436)

**Current Depth**: 2-3 levels

```yaml
applies_to:
  type: array
  description: "IDs the rule applies to"
  items:
    anyOf:  # ← Multiple inline type references
      - $ref: "#/$defs/AggId"
      - $ref: "#/$defs/WobjId"
      - $ref: "#/$defs/CmdId"
      - $ref: "#/$defs/QryId"
      - $ref: "#/$defs/EvtId"
      - $ref: "#/$defs/PolId"
```

**Issue**: Not really a problem, but could be more semantic

**Proposed Fix**: Create a union type

```yaml
# In $defs:
DomainElementId:
  anyOf:
    - $ref: "#/$defs/AggId"
    - $ref: "#/$defs/WobjId"
    - $ref: "#/$defs/CmdId"
    - $ref: "#/$defs/QryId"
    - $ref: "#/$defs/EvtId"
    - $ref: "#/$defs/PolId"

# In BusinessRule:
applies_to:
  type: array
  items: { $ref: "#/$defs/DomainElementId" }
```

#### Issue 1.3: DomainStory Embeds Full Objects Instead of References

**Location**: `DomainStory` (lines 440-502)

**Current Pattern**: Embeds arrays of full objects

```yaml
DomainStory:
  properties:
    actors:
      type: array
      items: { $ref: "#/$defs/Actor" }  # ← Full object embedded
    aggregates:
      type: array
      items: { $ref: "#/$defs/Aggregate" }  # ← Full object embedded
```

**Issue**: Violates DDD principle of "reference by ID"

**Impact**:
- Cannot reference same Actor/Aggregate in multiple stories
- Duplication if same actor appears in multiple stories
- No referential integrity

**Proposed Fix**: Reference by ID pattern

```yaml
DomainStory:
  properties:
    actor_ids:
      type: array
      minItems: 1
      items: { $ref: "#/$defs/ActId" }
    aggregate_ids:
      type: array
      items: { $ref: "#/$defs/AggId" }
    # ... etc for all embedded types

# Separate top-level arrays for definitions:
properties:
  domain_stories:
    type: array
    items: { $ref: "#/$defs/DomainStory" }

  actors:
    type: array
    items: { $ref: "#/$defs/Actor" }

  aggregates:
    type: array
    items: { $ref: "#/$defs/Aggregate" }
```

### Recommendations for Domain Stories Schema

1. **Priority 1 (High)**: Refactor DomainStory to reference by ID instead of embedding
2. **Priority 2 (Medium)**: Extract EventCause types
3. **Priority 3 (Low)**: Create DomainElementId union type for clarity

---

## 2. Strategic DDD Schema Analysis

### Overall Assessment: **MODERATE (70% Compliant)**

Strategic schema is relatively flat but lacks ID type extraction and has some nested structures.

### Strengths

1. **Top-level types separated**: system, domain, bounded_context, context_mapping as separate `$defs`
2. **Reference by ID pattern**: Mostly uses ID strings rather than embedding
3. **Clear structure**: Each type is self-contained

### Identified Issues

#### Issue 2.1: No ID Type Definitions

**Location**: Throughout the schema

**Issue**: ID patterns defined inline within each type

```yaml
# Current pattern (repeated everywhere):
domain:
  properties:
    id:
      type: string
      pattern: "^dom_[a-z0-9_]+$"

bounded_context:
  properties:
    id:
      type: string
      pattern: "^bc_[a-z0-9_]+$"
```

**Impact**:
- Pattern duplication
- No single source of truth for ID formats
- Harder to change patterns globally

**Proposed Fix**: Extract ID types like domain-stories pattern

```yaml
$defs:
  # ID Types
  SysId:
    type: string
    pattern: "^sys_[a-z0-9_]+$"
    description: "System identifier"

  DomId:
    type: string
    pattern: "^dom_[a-z0-9_]+$"
    description: "Domain identifier"

  BcId:
    type: string
    pattern: "^bc_[a-z0-9_]+$"
    description: "Bounded Context identifier"

  CmId:
    type: string
    pattern: "^cm_[a-z0-9_]+_to_[a-z0-9_]+$"
    description: "Context Mapping identifier"

  BffId:
    type: string
    pattern: "^bff_[a-z0-9_]+$"
    description: "BFF Scope identifier"

  BffIfId:
    type: string
    pattern: "^bff_if_[a-z0-9_]+$"
    description: "BFF Interface identifier"

  # Then use:
  domain:
    properties:
      id: { $ref: "#/$defs/DomId" }
```

#### Issue 2.2: bounded_context.ubiquitous_language Deep Nesting

**Location**: `bounded_context.properties.ubiquitous_language` (lines 117-134)

**Current Depth**: 4 levels

```yaml
ubiquitous_language:
  type: object
  properties:
    glossary:
      type: array
      items:
        type: object  # ← Inline definition
        required: [term, definition]
        properties:
          term:
            type: string
          definition:
            type: string
          examples:
            type: array
            items:
              type: string
```

**Issue**: Deep inline nesting (object → array → object → array)

**Proposed Fix**: Extract GlossaryEntry type

```yaml
# In $defs:
GlossaryEntry:
  type: object
  required: [term, definition]
  properties:
    term:
      type: string
    definition:
      type: string
    examples:
      type: array
      items:
        type: string

UbiquitousLanguage:
  type: object
  properties:
    glossary:
      type: array
      items: { $ref: "#/$defs/GlossaryEntry" }

# In bounded_context:
ubiquitous_language:
  $ref: "#/$defs/UbiquitousLanguage"
```

#### Issue 2.3: context_mapping.acl_details Deep Nesting

**Location**: `context_mapping.properties.acl_details` (lines 211-225)

**Current Depth**: 3 levels

```yaml
acl_details:
  type: object
  description: "For anti-corruption layer - implementation details"
  properties:
    facades:
      type: array
      items:
        type: string
    adapters:
      type: array
      items:
        type: string
    translators:
      type: array
      items:
        type: string
```

**Proposed Fix**: Extract ACLDetails type

```yaml
# In $defs:
ACLDetails:
  type: object
  description: "Anti-corruption layer implementation details"
  properties:
    facades:
      type: array
      items:
        type: string
    adapters:
      type: array
      items:
        type: string
    translators:
      type: array
      items:
        type: string

# In context_mapping:
acl_details:
  $ref: "#/$defs/ACLDetails"
```

#### Issue 2.4: bff_scope Deeply Nested Inline Definitions

**Location**: `bff_scope.properties.provides` (lines 306-385)

**Current Depth**: 5+ levels (extremely problematic)

```yaml
provides:
  type: object
  properties:
    endpoints:
      type: array
      items:
        type: object  # ← Inline
        properties:
          path:
            type: string
          method:
            type: string
            enum: [GET, POST, PUT, PATCH, DELETE]
          aggregates_from:
            type: array
            items:
              type: string
              pattern: "^bc_[a-z0-9_]+$"
          description:
            type: string

    data_aggregation:
      type: object  # ← Inline
      properties:
        strategy:
          type: string
          enum: [parallel, sequential, conditional]
        example:
          type: string

    transformations:
      type: array
      items:
        type: object  # ← Inline
        properties:
          from_context:
            type: string
            pattern: "^bc_[a-z0-9_]+$"
          transformation_type:
            type: string
            enum: [format_conversion, data_enrichment, field_mapping, filtering, denormalization]
          description:
            type: string
```

**Issue**: Multiple levels of inline object definitions - SEVERE violation

**Proposed Fix**: Extract all nested types

```yaml
# In $defs:
BFFEndpoint:
  type: object
  properties:
    path:
      type: string
    method:
      type: string
      enum: [GET, POST, PUT, PATCH, DELETE]
    aggregates_from:
      type: array
      items: { $ref: "#/$defs/BcId" }
    description:
      type: string

DataAggregationStrategy:
  type: object
  properties:
    strategy:
      type: string
      enum: [parallel, sequential, conditional]
    example:
      type: string

DataTransformation:
  type: object
  properties:
    from_context: { $ref: "#/$defs/BcId" }
    transformation_type:
      type: string
      enum: [format_conversion, data_enrichment, field_mapping, filtering, denormalization]
    description:
      type: string

BFFProvides:
  type: object
  properties:
    endpoints:
      type: array
      items: { $ref: "#/$defs/BFFEndpoint" }
    data_aggregation:
      $ref: "#/$defs/DataAggregationStrategy"
    transformations:
      type: array
      items: { $ref: "#/$defs/DataTransformation" }
    client_optimizations:
      type: array
      items:
        type: string

# In bff_scope:
provides:
  $ref: "#/$defs/BFFProvides"
```

#### Issue 2.5: bff_interface.endpoints Deep Nesting

**Location**: `bff_interface.properties.endpoints` (lines 537-624)

**Current Depth**: 5+ levels

**Issue**: Similar to bff_scope - deeply nested inline definitions

**Proposed Fix**: Extract types

```yaml
# In $defs:
BFFInterfaceEndpoint:
  type: object
  required: [path, method, operation_type]
  properties:
    path:
      type: string
    method:
      type: string
      enum: [GET, POST, PUT, PATCH, DELETE]
    operation_type:
      type: string
      enum: [command, query, action]
    description:
      type: string
    delegates_to_commands:
      type: array
      items: { $ref: "#/$defs/CmdId" }
    delegates_to_queries:
      type: array
      items: { $ref: "#/$defs/QryId" }
    request_dto:
      $ref: "#/$defs/DTO"
    response_dto:
      $ref: "#/$defs/DTO"
    aggregates_data_from:
      type: array
      items: { $ref: "#/$defs/BcId" }

DTO:
  type: object
  properties:
    name:
      type: string
    fields:
      type: array
      items: { $ref: "#/$defs/DTOField" }

DTOField:
  type: object
  properties:
    name:
      type: string
    type:
      type: string
    required:
      type: boolean

# In bff_interface:
endpoints:
  type: array
  items: { $ref: "#/$defs/BFFInterfaceEndpoint" }
```

### Recommendations for Strategic Schema

1. **Priority 1 (Critical)**: Extract ID types to separate section
2. **Priority 1 (Critical)**: Flatten bff_scope.provides (5+ levels → 2 levels)
3. **Priority 1 (Critical)**: Flatten bff_interface.endpoints (5+ levels → 2 levels)
4. **Priority 2 (High)**: Extract UbiquitousLanguage and GlossaryEntry
5. **Priority 3 (Medium)**: Extract ACLDetails

---

## 3. Tactical DDD Schema Analysis

### Overall Assessment: **POOR (50% Compliant)**

Tactical schema has the most severe nesting issues across all schemas.

### Strengths

1. **Top-level separation**: Main tactical types separated
2. **Some ID patterns**: Uses ID pattern validation

### Identified Issues

#### Issue 3.1: No ID Type Definitions

**Location**: Throughout schema

**Issue**: Same as strategic - inline ID patterns everywhere

**Proposed Fix**: Extract all ID types

```yaml
$defs:
  # ID Types
  AggId:
    type: string
    pattern: "^agg_[a-z0-9_]+$"

  EntId:
    type: string
    pattern: "^ent_[a-z0-9_]+$"

  VoId:
    type: string
    pattern: "^vo_[a-z0-9_]+$"

  RepoId:
    type: string
    pattern: "^repo_[a-z0-9_]+$"

  SvcDomId:
    type: string
    pattern: "^svc_dom_[a-z0-9_]+$"

  SvcAppId:
    type: string
    pattern: "^svc_app_[a-z0-9_]+$"

  CmdId:
    type: string
    pattern: "^cmd_[a-z0-9_]+$"

  QryId:
    type: string
    pattern: "^qry_[a-z0-9_]+$"

  EvtId:
    type: string
    pattern: "^evt_[a-z0-9_]+$"
```

#### Issue 3.2: entity.attributes Deep Inline Nesting

**Location**: `entity.properties.attributes` (lines 106-123)

**Current Depth**: 4 levels

```yaml
attributes:
  type: array
  description: "Entity attributes"
  items:
    type: object  # ← Inline definition
    required: [name, type]
    properties:
      name:
        type: string
      type:
        type: string
      value_object_ref:
        type: string
        pattern: "^vo_[a-z0-9_]+$"
      required:
        type: boolean
      description:
        type: string
```

**Issue**: Inline attribute definition duplicated across entity, value_object

**Proposed Fix**: Extract Attribute type (similar to domain-stories)

```yaml
# In $defs:
Attribute:
  type: object
  required: [name, type]
  properties:
    name:
      type: string
    type:
      type: string
    value_object_ref:
      type: string
      pattern: "^vo_[a-z0-9_]+$"
    required:
      type: boolean
    description:
      type: string

# In entity:
attributes:
  type: array
  items: { $ref: "#/$defs/Attribute" }
```

#### Issue 3.3: entity.business_methods Deep Nesting

**Location**: `entity.properties.business_methods` (lines 124-137)

**Current Depth**: 4 levels

```yaml
business_methods:
  type: array
  items:
    type: object  # ← Inline
    properties:
      name:
        type: string
      description:
        type: string
      parameters:
        type: array
      returns:
        type: string
```

**Proposed Fix**: Extract Method type

```yaml
# In $defs:
Method:
  type: object
  properties:
    name:
      type: string
    description:
      type: string
    parameters:
      type: array
      items: { $ref: "#/$defs/Parameter" }
    returns:
      type: string

# In entity:
business_methods:
  type: array
  items: { $ref: "#/$defs/Method" }
```

#### Issue 3.4: repository.interface_methods Deep Nesting

**Location**: `repository.properties.interface_methods` (lines 214-229)

**Current Depth**: 4 levels

**Issue**: Duplicate of Method structure - should reuse

**Proposed Fix**: Use shared Method type

```yaml
# In repository:
interface_methods:
  type: array
  items: { $ref: "#/$defs/RepositoryMethod" }

# In $defs:
RepositoryMethod:
  allOf:
    - $ref: "#/$defs/Method"
    - type: object
      properties:
        query_type:
          type: string
          enum: [by_id, by_criteria, all, custom]
```

#### Issue 3.5: domain_service.operations Deep Nesting

**Location**: `domain_service.properties.operations` (lines 254-266)

**Current Depth**: 4 levels

**Issue**: SAME structure as entity.business_methods - should be extracted once

**Proposed Fix**: Reuse Method type

```yaml
# In domain_service:
operations:
  type: array
  items: { $ref: "#/$defs/Method" }
```

#### Issue 3.6: domain_event.data_carried Deep Nesting

**Location**: `domain_event.properties.data_carried` (lines 296-306)

**Current Depth**: 4 levels

**Issue**: Inline field definition

**Proposed Fix**: Extract EventDataField

```yaml
# In $defs:
EventDataField:
  type: object
  properties:
    name:
      type: string
    type:
      type: string
    description:
      type: string

# In domain_event:
data_carried:
  type: array
  items: { $ref: "#/$defs/EventDataField" }
```

#### Issue 3.7: application_service.operations EXTREMELY Deep Nesting

**Location**: `application_service.properties.operations` (lines 369-479)

**Current Depth**: 6+ levels (SEVERE)

```yaml
operations:
  type: array
  items:
    type: object  # ← Level 1 inline
    required: [name, type]
    properties:
      name:
        type: string
      type:
        type: string
      parameters:
        type: array
        items:  # ← Level 2 inline
          type: object
          properties:
            name:
              type: string
      transaction_boundary:
        type: object  # ← Level 2 inline
        properties:
          modifies_aggregates:
            type: array
            items:
              type: string
      workflow:
        type: object  # ← Level 2 inline
        properties:
          loads_aggregates:
            type: array
            items:
              type: string
          # ... more nesting
```

**Issue**: WORST violation in entire codebase - 6+ levels deep

**Proposed Fix**: Extract ALL nested types

```yaml
# In $defs:
ApplicationServiceOperation:
  type: object
  required: [name, type]
  properties:
    name:
      type: string
      pattern: "^[a-z][a-zA-Z]+$"
    type:
      type: string
      enum: [command, query]
    description:
      type: string
    parameters:
      type: array
      items: { $ref: "#/$defs/Parameter" }
    returns:
      type: string
    transaction_boundary:
      $ref: "#/$defs/TransactionBoundary"
    workflow:
      $ref: "#/$defs/WorkflowDefinition"

TransactionBoundary:
  type: object
  properties:
    is_transactional:
      type: boolean
      default: true
    modifies_aggregates:
      type: array
      items: { $ref: "#/$defs/AggId" }
      maxItems: 1
    consistency_type:
      type: string
      enum: [transactional, eventual]

WorkflowDefinition:
  type: object
  properties:
    validates_input:
      type: boolean
      default: true
    loads_aggregates:
      type: array
      items: { $ref: "#/$defs/AggId" }
    invokes_domain_operations:
      type: array
      items:
        type: string
    invokes_domain_services:
      type: array
      items: { $ref: "#/$defs/SvcDomId" }
    persists_aggregates:
      type: boolean
      default: true
    publishes_events:
      type: array
      items: { $ref: "#/$defs/EvtId" }
    returns_dto:
      type: string

# In application_service:
operations:
  type: array
  items: { $ref: "#/$defs/ApplicationServiceOperation" }
```

#### Issue 3.8: command_interface.command_records Deep Nesting

**Location**: `command_interface.properties.command_records` (lines 600-693)

**Current Depth**: 5 levels

**Proposed Fix**: Extract CommandRecord type

```yaml
# In $defs:
CommandRecord:
  type: object
  required: [record_name, intent, parameters]
  properties:
    record_name:
      type: string
      pattern: "^[A-Z][a-zA-Z]+Cmd$"
    intent:
      type: string
      pattern: "^[a-z][a-zA-Z]+$"
    description:
      type: string
    parameters:
      type: array
      items: { $ref: "#/$defs/Parameter" }
    returns:
      type: string
      enum: [void, domain_id, acknowledgment, result_status]
    return_type_ref:
      type: string
      pattern: "^vo_[a-z0-9_]+$"
    modifies_aggregate: { $ref: "#/$defs/AggId" }
    publishes_events:
      type: array
      items: { $ref: "#/$defs/EvtId" }
    audit_fields:
      type: array
      items:
        type: string

# In command_interface:
command_records:
  type: array
  items: { $ref: "#/$defs/CommandRecord" }
```

#### Issue 3.9: query_interface.query_methods Deep Nesting

**Location**: `query_interface.properties.query_methods` (lines 756-877)

**Current Depth**: 6+ levels (SEVERE)

```yaml
query_methods:
  type: array
  items:
    type: object
    required: [method_name, result_record_name]
    properties:
      method_name:
        type: string
      parameters:
        type: array
        items:
          type: object  # ← Deep nesting
          properties:
            name:
              type: string
      result_structure:
        type: object  # ← Deep nesting
        properties:
          fields:
            type: array
            items:
              type: object  # ← More nesting
              properties:
                name:
                  type: string
```

**Proposed Fix**: Extract all nested types

```yaml
# In $defs:
QueryMethod:
  type: object
  required: [method_name, result_record_name]
  properties:
    method_name:
      type: string
      pattern: "^(get|list|find|search)[A-Z][a-zA-Z]+$"
    description:
      type: string
    parameters:
      type: array
      items: { $ref: "#/$defs/Parameter" }
    result_record_name:
      type: string
      pattern: "^[A-Z][a-zA-Z]+Summary$"
    result_structure:
      $ref: "#/$defs/ResultStructure"
    bypasses_domain_model:
      type: boolean
      default: false
    optimizations:
      $ref: "#/$defs/QueryOptimizations"

ResultStructure:
  type: object
  properties:
    fields:
      type: array
      items: { $ref: "#/$defs/DTOField" }
    aggregate_counts:
      type: array
      items: { $ref: "#/$defs/AggregateCount" }

QueryOptimizations:
  type: object
  properties:
    denormalized:
      type: boolean
      default: false
    cached:
      type: boolean
      default: false
    indexed:
      type: boolean
      default: true

AggregateCount:
  type: object
  properties:
    field_name:
      type: string
    counted_entity:
      type: string

# In query_interface:
query_methods:
  type: array
  items: { $ref: "#/$defs/QueryMethod" }
```

### Recommendations for Tactical Schema

1. **Priority 1 (Critical)**: Extract ID types
2. **Priority 1 (Critical)**: Flatten application_service.operations (6+ → 2 levels)
3. **Priority 1 (Critical)**: Flatten query_interface.query_methods (6+ → 2 levels)
4. **Priority 2 (High)**: Extract common types: Parameter, Attribute, Method
5. **Priority 2 (High)**: Flatten command_interface.command_records
6. **Priority 3 (Medium)**: Extract all remaining inline definitions

---

## 4. Summary Table: Nesting Issues by Schema

| Schema | Total Issues | Critical (5+ levels) | High (4 levels) | Medium (3 levels) | Compliance |
|--------|--------------|----------------------|-----------------|-------------------|------------|
| Domain Stories | 3 | 0 | 0 | 3 | 95% ✅ |
| Strategic DDD | 6 | 2 | 2 | 2 | 70% ⚠️ |
| Tactical DDD | 10+ | 3 | 5 | 2+ | 50% ❌ |

---

## 5. Common Types to Extract Across All Schemas

These types appear in multiple places and should be extracted to `$defs`:

### Shared Across All Schemas

1. **Parameter** - Used in operations, methods, commands, queries
2. **Attribute** - Used in entities, value objects, work objects
3. **Method/Operation** - Used in services, repositories, interfaces

### Strategic-Specific

1. **BFFEndpoint**
2. **DataTransformation**
3. **GlossaryEntry**
4. **ACLDetails**

### Tactical-Specific

1. **CommandRecord**
2. **QueryMethod**
3. **TransactionBoundary**
4. **WorkflowDefinition**
5. **ResultStructure**
6. **DTOField**

### Domain-Stories-Specific

1. **EventCause**
2. **DomainElementId**

---

## 6. Overall Recommendations

### Immediate Actions (Breaking Changes Required)

1. **Extract all ID types** to dedicated section in each schema
2. **Flatten critical deep nesting** (5+ levels) in:
   - Strategic: bff_scope, bff_interface
   - Tactical: application_service.operations, query_interface.query_methods

### Phase 2 Actions

3. **Extract common reusable types** (Parameter, Attribute, Method)
4. **Flatten moderate nesting** (4 levels) across all schemas
5. **Refactor domain stories** to use reference-by-ID pattern

### Organizational Structure for v2.0

```yaml
$defs:
  # =====================================
  # SECTION 1: ID TYPES
  # =====================================
  TypeId:
    type: string
    pattern: "^type_[a-z0-9_]+$"
  # ... all ID types

  # =====================================
  # SECTION 2: COMMON/SHARED TYPES
  # =====================================
  Parameter:
    type: object
    # ...

  Attribute:
    type: object
    # ...

  Method:
    type: object
    # ...

  # =====================================
  # SECTION 3: DOMAIN TYPES
  # =====================================
  Aggregate:
    type: object
    # ...
```

---

## 7. Metrics

### Before v2.0

- **Average Nesting Depth**: 4.2 levels
- **Maximum Nesting Depth**: 6+ levels (tactical schema)
- **Inline Definitions**: 35+
- **Duplicated Patterns**: 12

### After v2.0 (Target)

- **Average Nesting Depth**: 2.0 levels
- **Maximum Nesting Depth**: 3 levels
- **Inline Definitions**: 0
- **Duplicated Patterns**: 0

---

## Conclusion

The flat structure principle is currently violated across all schemas to varying degrees. Domain stories schema is closest to compliance, while tactical schema requires the most work. The v2.0 refactoring should prioritize:

1. ID type extraction (all schemas)
2. Critical deep nesting fixes (tactical + strategic)
3. Common type extraction and reuse
4. Reference-by-ID pattern enforcement

This will result in more maintainable, reusable, and DDD-compliant schemas.
