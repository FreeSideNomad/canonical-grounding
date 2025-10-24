# Task 6: Hierarchical Markdown Generation Requirements

**Date**: 2025-10-23
**Analyst**: Claude (Sonnet 4.5)
**Scope**: Design schema requirements to support automatic markdown documentation generation

---

## Executive Summary

The v2.0 schemas must support simple, rule-based transformation from YAML/JSON instances to hierarchical markdown documentation. This requires consistent field naming (`id`, `name`, `description`), clear parent-child relationships, and optional display metadata.

### Key Findings

- ✅ **Current State**: Domain stories schema ~80% ready for markdown generation
- ❌ **Problem**: Strategic and tactical schemas lack consistent display fields
- ✅ **Solution**: Enforce `id`, `name`, `description` pattern + add hierarchy metadata

### Recommendation

**Hybrid Approach (Option C)**: Keep schemas normalized (flat with $refs) but add optional `name` field to ID references for denormalized display data.

---

## Part 1: Markdown Generation Requirements

### 1.1 Use Case

**Input**: YAML instance conforming to strategic-ddd.schema.yaml

```yaml
system:
  id: sys_ecommerce
  name: E-Commerce Platform
  description: "Our e-commerce system handling customer orders"

  domains:
    - id: dom_customer
      name: Customer Management
      type: core
      description: "Manages customer identity and profiles"

      bounded_contexts:
        - bc_customer_profile
        - bc_customer_auth
```

**Desired Output**: Well-structured markdown

```markdown
# E-Commerce Platform

**System ID**: `sys_ecommerce`

Our e-commerce system handling customer orders

---

## Domains

### Customer Management (Core Domain)

**Domain ID**: `dom_customer`

Manages customer identity and profiles

#### Bounded Contexts

- Customer Profile (`bc_customer_profile`)
- Customer Auth (`bc_customer_auth`)
```

### 1.2 Core Challenges

**Challenge 1**: Deriving hierarchy from flat schemas
- Schemas use $ref which breaks visual hierarchy
- Need to know: System → Domain → BoundedContext → Aggregate → Entity

**Challenge 2**: Resolving ID references to names
- `bounded_contexts: [bc_customer_profile]` is just an ID
- Need to look up actual name: "Customer Profile"

**Challenge 3**: Determining heading levels
- No explicit metadata about heading depth
- Must infer from type (System=H1, Domain=H2, etc.)

**Challenge 4**: Handling cross-references
- Circular references (BC → Aggregate, Aggregate → BC)
- Cross-schema references (Strategic → Tactical)

---

## Part 2: Schema Design Requirements

### 2.1 Required Display Fields

**Every major type must have**:

```yaml
TypeName:
  type: object
  required: [id, name]  # ← MANDATORY
  properties:
    id:
      type: string
      description: "Unique identifier"

    name:
      type: string
      description: "Human-readable name"  # ← For display

    description:
      type: string  # ← Optional but recommended
      description: "Detailed description for documentation"
```

### 2.2 Current Compliance Check

| Schema | Type | Has `id` | Has `name` | Has `description` | Compliant |
|--------|------|----------|------------|-------------------|-----------|
| **Strategic** | system | ✅ | ✅ | ✅ | ✅ |
| | domain | ✅ | ✅ | ✅ | ✅ |
| | bounded_context | ✅ | ✅ | ✅ | ✅ |
| | context_mapping | ✅ | ❌ | ✅ | ❌ |
| | bff_scope | ✅ | ✅ | ✅ | ✅ |
| | bff_interface | ✅ | ✅ | ✅ | ✅ |
| **Tactical** | aggregate | ✅ | ✅ | ❌ | ⚠️ |
| | entity | ✅ | ✅ | ❌ | ⚠️ |
| | value_object | ✅ | ✅ | ✅ | ✅ |
| | repository | ✅ | ✅ | ❌ | ⚠️ |
| | domain_service | ✅ | ✅ | ✅ | ✅ |
| | application_service | ✅ | ✅ | ✅ | ✅ |
| | domain_event | ✅ | ✅ | ✅ | ✅ |
| | command_interface | ✅ | ✅ | ✅ | ✅ |
| | query_interface | ✅ | ✅ | ✅ | ✅ |
| **Domain Stories** | DomainStory | ✅ | ✅ (title) | ✅ | ✅ |
| | Actor | ✅ | ✅ | ❌ | ⚠️ |
| | Aggregate | ✅ | ✅ | ✅ | ✅ |

**Missing `description` fields**:
- aggregate (tactical)
- entity (tactical)
- repository (tactical)
- Actor (domain stories)

**Recommendation**: Add optional `description` field to all types

### 2.3 Proposed Schema Changes

#### Strategic Schema

```yaml
# BEFORE (v1.x):
context_mapping:
  properties:
    id:
      type: string
      pattern: "^cm_[a-z0-9_]+_to_[a-z0-9_]+$"
    # NO name field!
    upstream_context: ...
    downstream_context: ...

# AFTER (v2.0):
context_mapping:
  properties:
    id: { $ref: "#/$defs/CmId" }

    name:
      type: string
      description: "Human-readable name for this mapping"
      examples:
        - "Order to Customer Mapping"
        - "Inventory to Shipping Integration"

    description:
      type: string
      description: "Details about this integration"
```

#### Tactical Schema

```yaml
# BEFORE (v1.x):
aggregate:
  properties:
    id: ...
    name: ...
    # NO description field

# AFTER (v2.0):
aggregate:
  properties:
    id: { $ref: "#/$defs/AggId" }
    name:
      type: string
    description:
      type: string
      description: "What this aggregate represents and its responsibilities"

entity:
  properties:
    id: { $ref: "#/$defs/EntId" }
    name:
      type: string
    description:
      type: string
      description: "What this entity represents"

repository:
  properties:
    id: { $ref: "#/$defs/RepoId" }
    name:
      type: string
    description:
      type: string
      description: "Purpose of this repository"
```

---

## Part 3: Hierarchy Derivation

### 3.1 Mapping Rules

**Rule 1: Type to Heading Level**

```yaml
type_to_heading:
  # Strategic
  System: 1          # # H1
  Domain: 2          # ## H2
  BoundedContext: 3  # ### H3

  # Tactical (within BC)
  Aggregate: 4       # #### H4
  Entity: 5          # ##### H5
  ValueObject: 5     # ##### H5
  Repository: 4      # #### H4
  DomainService: 4   # #### H4
  ApplicationService: 4  # #### H4

  # Domain Stories
  DomainStory: 1     # # H1
  Actor: 2           # ## H2
  Aggregate: 3       # ### H3 (in story context)
```

**Rule 2: Required Display Fields**

```yaml
every_type:
  required: [id, name]
  properties:
    id: { type: string }
    name: { type: string }  # ← Used for heading
    description: { type: string }  # ← Used for paragraph under heading
```

**Rule 3: Reference Resolution**

When encountering array of IDs:
```yaml
bounded_contexts:
  - bc_customer_profile
  - bc_order_mgmt
```

Generator must:
1. Find bounded_context definitions
2. Extract `name` field
3. Render as list with ID in parentheses

Output:
```markdown
#### Bounded Contexts
- Customer Profile (`bc_customer_profile`)
- Order Management (`bc_order_mgmt`)
```

**Rule 4: List Items**

```yaml
# Arrays of IDs → Markdown bulleted list
aggregates: [agg_customer, agg_order]

# Renders as:
- Customer Aggregate (`agg_customer`)
- Order Aggregate (`agg_order`)
```

```yaml
# Arrays of objects → Markdown nested sections
aggregates:
  - id: agg_customer
    name: Customer Aggregate
    description: "Manages customer identity"

# Renders as:
#### Customer Aggregate
**ID**: `agg_customer`

Manages customer identity
```

**Rule 5: Metadata Fields**

```yaml
# Enum fields → Bold labels
type: core

# Renders as:
**Type**: Core Domain
```

```yaml
# Boolean fields → Checkboxes/badges
immutability: true

# Renders as:
**Immutable**: ✅ Yes
```

### 3.2 Example Transformation

#### Input YAML (Strategic)

```yaml
system:
  id: sys_ecommerce
  name: E-Commerce Platform
  version: "2.0.0"

  domains:
    - id: dom_customer
      name: Customer Management
      type: core
      description: "Handles all customer-related functionality"

      bounded_contexts:
        - bc_customer_profile
        - bc_customer_auth

# Bounded context definitions
bounded_contexts:
  - id: bc_customer_profile
    name: Customer Profile
    domain_ref: dom_customer
    description: "Manages customer personal information and preferences"

    tactical_summary:
      aggregate_count: 2
      key_aggregates:
        - agg_customer
        - agg_preferences
```

#### Output Markdown

```markdown
# E-Commerce Platform

**System ID**: `sys_ecommerce`
**Version**: 2.0.0

---

## Domains

### Customer Management

**Domain ID**: `dom_customer`
**Type**: Core Domain

Handles all customer-related functionality

#### Bounded Contexts

##### Customer Profile

**Context ID**: `bc_customer_profile`
**Domain**: Customer Management

Manages customer personal information and preferences

**Tactical Summary**:
- **Aggregate Count**: 2
- **Key Aggregates**:
  - agg_customer
  - agg_preferences
```

---

## Part 4: Reference vs Embed Trade-offs

### Option A: Reference by ID (Flat Schema) ❌

**Current approach in v2.0 recommendation**:

```yaml
bounded_context:
  id: bc_customer_profile
  aggregates:
    - agg_customer  # ← Just ID
    - agg_preferences
```

**Markdown Generation Challenge**:
- Need to resolve `agg_customer` → "Customer Aggregate"
- Requires ID lookup table
- Multiple passes needed

**Lookup Process**:
```python
def resolve_aggregate_name(agg_id, tactical_model):
    for agg in tactical_model['bounded_context']['aggregates']:
        if agg['id'] == agg_id:
            return agg['name']
    return agg_id  # Fallback to ID if not found
```

**Pros**:
✅ Aligns with flat schema principle
✅ No duplication
✅ Single source of truth

**Cons**:
❌ Complex markdown generation (multi-pass)
❌ Requires loading multiple files
❌ Slower generation

---

### Option B: Embedded Summary ❌

**Approach**: Denormalize minimal display data

```yaml
bounded_context:
  id: bc_customer_profile
  aggregates:
    - id: agg_customer
      name: Customer Aggregate  # ← Duplicated for display
      # Full details stored elsewhere in tactical.aggregates
```

**Markdown Generation**: Simple, single-pass

**Pros**:
✅ Easy markdown generation
✅ Single pass
✅ No ID resolution needed

**Cons**:
❌ Duplication (name appears twice)
❌ Violates flat schema principle
❌ Can get out of sync

---

### Option C: Hybrid (ID + Optional Name) ✅

**Approach**: ID required, name optional for convenience

```yaml
$defs:
  AggregateReference:
    oneOf:
      # Option 1: Just ID (minimal)
      - type: string
        pattern: "^agg_[a-z0-9_]+$"

      # Option 2: ID + name (convenient)
      - type: object
        required: [id]
        properties:
          id:
            type: string
            pattern: "^agg_[a-z0-9_]+$"
          name:
            type: string
            description: "Optional: denormalized name for display"

bounded_context:
  properties:
    aggregates:
      type: array
      items: { $ref: "#/$defs/AggregateReference" }
```

**Usage**:

```yaml
# Minimal (requires lookup):
bounded_context:
  id: bc_customer
  aggregates:
    - agg_customer
    - agg_preferences

# OR with names (self-documenting):
bounded_context:
  id: bc_customer
  aggregates:
    - id: agg_customer
      name: Customer Aggregate
    - id: agg_preferences
      name: Customer Preferences
```

**Markdown Generation Logic**:

```python
def render_aggregate_list(aggregates, tactical_model=None):
    items = []
    for agg in aggregates:
        if isinstance(agg, str):
            # Just ID - need lookup
            agg_id = agg
            agg_name = resolve_name(agg_id, tactical_model) if tactical_model else agg_id
        else:
            # Object with name
            agg_id = agg['id']
            agg_name = agg.get('name', agg_id)

        items.append(f"- {agg_name} (`{agg_id}`)")

    return "\n".join(items)
```

**Pros**:
✅ Flexible: supports both minimal and verbose
✅ Backwards compatible
✅ Optional denormalization (user choice)
✅ Falls back to ID if name not provided

**Cons**:
⚠️ Inconsistent: Some documents have names, some don't
⚠️ Optional duplication

**Mitigation**:
- Tooling can auto-populate names from tactical schema
- Validation warns if names don't match canonical definitions

**Verdict**: ✅ **RECOMMENDED** - Best balance

---

## Part 5: Proposed Mapping Implementation

### 5.1 Schema Additions

#### Add Display Hints (x-markdown)

```yaml
$defs:
  BoundedContext:
    type: object
    x-markdown:
      heading_level: 3
      title_field: name
      id_field: id
      sections:
        - field: description
          render_as: paragraph
        - field: aggregates
          render_as: list
          heading: "Aggregates"
        - field: repositories
          render_as: list
          heading: "Repositories"

    properties:
      id: { $ref: "#/$defs/BcId" }
      name: { type: string }
      description: { type: string }
      aggregates:
        type: array
        items: { $ref: "#/$defs/AggregateReference" }
```

**Benefits**:
- Explicit markdown generation rules
- Self-documenting schema
- Generator reads hints to produce correct output

**Concerns**:
- `x-` extensions not validated by JSON Schema
- Schema becomes verbose
- Couples schema to specific output format

**Recommendation**: ⚠️ Optional enhancement, not required

---

### 5.2 Simple Convention-Based Approach (Recommended)

**Instead of metadata, use conventions**:

1. **Convention 1**: Types with `id`, `name`, `description` are renderable
2. **Convention 2**: Array field name determines section heading (pluralize)
3. **Convention 3**: Heading level based on type hierarchy (hard-coded map)
4. **Convention 4**: Enum fields render as "**FieldName**: Value"

**Implementation**:

```python
# Simple mapping rules
TYPE_HEADING_LEVELS = {
    "System": 1,
    "Domain": 2,
    "BoundedContext": 3,
    "Aggregate": 4,
    "Entity": 5,
}

def generate_markdown(obj, obj_type):
    level = TYPE_HEADING_LEVELS.get(obj_type, 2)
    heading = "#" * level

    # Title from 'name' field
    md = f"{heading} {obj['name']}\n\n"

    # ID badge
    if 'id' in obj:
        md += f"**ID**: `{obj['id']}`\n\n"

    # Description paragraph
    if 'description' in obj:
        md += f"{obj['description']}\n\n"

    # Enum fields as metadata
    for field, value in obj.items():
        if field in ['type', 'kind', 'status']:
            md += f"**{field.title()}**: {value.replace('_', ' ').title()}\n"

    return md
```

---

## Part 6: Sample Transformations

### 6.1 Strategic Schema → Markdown

#### Input

```yaml
system:
  id: sys_ecommerce
  name: E-Commerce Platform
  version: "2.0.0"
  description: "Our e-commerce system"

  domains:
    - id: dom_customer
      name: Customer Management
      type: core
      strategic_importance: critical
      description: "Manages customer identity"

      bounded_contexts:
        - id: bc_customer_profile
          name: Customer Profile
        - id: bc_customer_auth
          name: Customer Authentication
```

#### Output

```markdown
# E-Commerce Platform

**System ID**: `sys_ecommerce`
**Version**: 2.0.0

Our e-commerce system

---

## Domains

### Customer Management

**Domain ID**: `dom_customer`
**Type**: Core Domain
**Strategic Importance**: Critical

Manages customer identity

#### Bounded Contexts

- Customer Profile (`bc_customer_profile`)
- Customer Authentication (`bc_customer_auth`)
```

### 6.2 Tactical Schema → Markdown

#### Input

```yaml
bounded_context:
  id: bc_customer_profile
  name: Customer Profile
  description: "Manages customer personal information"

  aggregates:
    - id: agg_customer
      name: Customer Aggregate
      description: "Customer identity and contact info"
      root_ref: ent_customer
      size_estimate: small
      invariants:
        - "Email must be unique"
        - "Must have at least one contact method"
```

#### Output

```markdown
### Customer Profile

**Bounded Context ID**: `bc_customer_profile`

Manages customer personal information

---

#### Aggregates

##### Customer Aggregate

**Aggregate ID**: `agg_customer`
**Root Entity**: `ent_customer`
**Size Estimate**: Small

Customer identity and contact info

**Invariants**:
- Email must be unique
- Must have at least one contact method
```

### 6.3 Domain Story → Markdown

#### Input

```yaml
domain_stories:
  - domain_story_id: dst_customer_registration
    title: "Customer Self-Registration"
    description: "New customer creates account"

    actors:
      - actor_id: act_customer
        name: New Customer
        kind: person

    narrative:
      steps:
        - sequence: 1
          actor_id: act_customer
          action: "Fills out registration form"
        - sequence: 2
          actor_id: act_customer
          action: "Submits form"
          invokes_command: cmd_create_customer
```

#### Output

```markdown
# Customer Self-Registration

**Story ID**: `dst_customer_registration`

New customer creates account

---

## Actors

- **New Customer** (Person) - `act_customer`

---

## Story Flow

1. New Customer: Fills out registration form

2. New Customer: Submits form
   - **Invokes**: `cmd_create_customer`
```

---

## Part 7: Implementation Strategy

### 7.1 Schema Changes Required

**Priority 1 (High)**: Ensure all major types have `id`, `name`, `description`

Add missing fields:
- `context_mapping.name`
- `aggregate.description`
- `entity.description`
- `repository.description`
- `Actor.description`

**Priority 2 (Medium)**: Support hybrid ID references (Option C)

```yaml
AggregateReference:
  oneOf:
    - type: string  # Just ID
    - type: object  # ID + name
      required: [id]
      properties:
        id: { type: string }
        name: { type: string }
```

**Priority 3 (Low)**: Add x-markdown hints (optional)

Only if needed for complex rendering rules

### 7.2 Generator Implementation

```python
# tools/generate_markdown.py

class MarkdownGenerator:
    def __init__(self, schema_type):
        self.type_levels = TYPE_HEADING_LEVELS
        self.schema_type = schema_type  # strategic, tactical, or domain_stories

    def generate(self, instance):
        """Generate markdown from YAML instance"""
        if self.schema_type == "strategic":
            return self.render_strategic(instance['system'])
        elif self.schema_type == "tactical":
            return self.render_tactical(instance['bounded_context'])
        elif self.schema_type == "domain_stories":
            return self.render_stories(instance['domain_stories'])

    def render_strategic(self, system):
        md = f"# {system['name']}\n\n"
        md += f"**System ID**: `{system['id']}`\n\n"
        if 'description' in system:
            md += f"{system['description']}\n\n"

        md += "---\n\n## Domains\n\n"
        for domain_id in system.get('domains', []):
            domain = self.find_domain(domain_id)
            md += self.render_domain(domain)

        return md

    def render_domain(self, domain):
        md = f"### {domain['name']}\n\n"
        md += f"**Domain ID**: `{domain['id']}`\n"
        md += f"**Type**: {domain['type'].title()} Domain\n\n"
        # ... etc

    def resolve_reference(self, ref_id, ref_type):
        """Resolve ID to name (if needed)"""
        # Implementation depends on whether hybrid references used
        pass
```

### 7.3 Validation

```python
# Validate all major types have required display fields
def validate_display_fields(schema):
    errors = []

    for type_name, type_def in schema['$defs'].items():
        if type_def['type'] == 'object':
            props = type_def.get('properties', {})

            if 'id' not in props:
                errors.append(f"{type_name} missing 'id' field")

            if 'name' not in props and 'title' not in props:
                errors.append(f"{type_name} missing 'name' or 'title' field")

    return errors
```

---

## Conclusion

### Recommended Approach

**Use Option C: Hybrid ID + Optional Name**

**Schema Requirements**:
1. ✅ All major types have `id`, `name`, `description` (required: id + name, optional: description)
2. ✅ Support both ID strings and ID+name objects in references
3. ✅ Convention-based heading levels (no x-markdown metadata needed)
4. ✅ Consistent field naming across all schemas

**Benefits**:
- ✅ Balances flat schema principle with markdown generation simplicity
- ✅ Single-pass generation when names included
- ✅ Fallback to multi-pass when names omitted
- ✅ No duplication required (names optional)
- ✅ User chooses verbosity level

**Implementation Effort**:
- Schema changes: Small (add missing description fields, hybrid references)
- Generator tool: Medium (~500 lines of Python)
- Validation: Small (check required fields present)

This approach enables automatic markdown generation while preserving schema quality principles.
