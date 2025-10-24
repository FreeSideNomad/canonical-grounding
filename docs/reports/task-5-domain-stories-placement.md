# Task 5: Domain Stories Placement Analysis

**Date**: 2025-10-23
**Analyst**: Claude (Sonnet 4.5)
**Scope**: Evaluate where DomainStory should reside in v2.0 schema architecture

---

## Executive Summary

Domain stories currently exist in a standalone schema with their own definitions of Aggregate, Command, Event, etc., creating significant duplication with tactical schema. After evaluating three placement options, the recommendation is to **keep domain stories standalone but refactor to reference tactical types by ID**.

### Key Findings

- ❌ **Current State**: Domain stories duplicate ~15 tactical type definitions
- ✅ **Recommended**: Standalone schema with reference-by-ID pattern
- ❌ **Rejected**: Moving to tactical (breaks cross-BC stories)
- ❌ **Rejected**: Moving to strategic (wrong abstraction level)

### Recommendation

**Option A (Enhanced): Standalone Schema with Tactical References** - Keep domain stories independent but reference tactical objects by ID instead of embedding definitions.

---

## Part 1: Current State Analysis

### 1.1 Domain Stories Schema Overview

```yaml
# domain-stories-schema.yaml (current)
properties:
  domain_stories:
    type: array
    items: { $ref: "#/$defs/DomainStory" }

$defs:
  DomainStory:
    properties:
      domain_story_id: { $ref: "#/$defs/DstId" }
      title: string
      description: string

      # EMBEDS FULL DEFINITIONS (not references)
      actors:
        type: array
        items: { $ref: "#/$defs/Actor" }  # ← Full Actor object

      aggregates:
        type: array
        items: { $ref: "#/$defs/Aggregate" }  # ← Full Aggregate object

      commands:
        type: array
        items: { $ref: "#/$defs/Command" }  # ← Full Command object

      queries:
        type: array
        items: { $ref: "#/$defs/Query" }  # ← Full Query object

      events:
        type: array
        items: { $ref: "#/$defs/Event" }  # ← Full Event object

      # ... plus repositories, services, etc.
```

### 1.2 Type Overlap Analysis

Domain stories schema defines its own versions of types that also exist in tactical schema:

| Type | Domain Stories | Tactical DDD | Overlap % | Issues |
|------|----------------|--------------|-----------|--------|
| **Aggregate** | ✅ Lines 205-222 | ✅ Lines 29-75 | 80% | Different structure |
| **Repository** | ✅ Lines 223-235 | ✅ Lines 193-232 | 70% | Similar purpose |
| **ApplicationService** | ✅ Lines 236-256 | ✅ Lines 312-555 | 60% | Simpler in domain stories |
| **DomainService** | ✅ Lines 257-275 | ✅ Lines 234-270 | 75% | Similar structure |
| **Command** | ✅ Lines 277-311 | ✅ command_interface Lines 556-710 | 50% | Different patterns |
| **Query** | ✅ Lines 312-330 | ✅ query_interface Lines 711-906 | 50% | Different patterns |
| **Event** | ✅ Lines 371-406 | ✅ domain_event Lines 272-310 | 70% | Similar structure |

**Total Duplication**: ~350 lines of YAML

#### Structural Differences Example

**Domain Stories Aggregate**:
```yaml
Aggregate:
  properties:
    aggregate_id: { $ref: "#/$defs/AggId" }
    name: string
    root_work_object_id: { $ref: "#/$defs/WobjId" }  # ← References WorkObject
    work_object_ids: [WobjId]
    invariants: [string]
```

**Tactical Aggregate**:
```yaml
aggregate:
  properties:
    id: { $ref: "#/$defs/AggId" }
    name: string
    bounded_context_ref: { $ref: "#/$defs/BcId" }
    root_ref: { $ref: "#/$defs/EntId" }  # ← References Entity
    entities: [EntId]
    value_objects: [VoId]
    invariants: [string]
```

**Differences**:
- Domain stories uses `WorkObject`, tactical uses `Entity`
- Domain stories no `bounded_context_ref`
- Field names differ (`aggregate_id` vs `id`)
- Domain stories simpler (fewer fields)

### 1.3 Current Issues

**Issue 1: Duplication Without Consistency**
- Two different `Aggregate` definitions that mean similar things
- Changes to tactical patterns don't propagate to domain stories
- Risk of divergence over time

**Issue 2: No Referential Integrity**
- Domain stories define their own aggregates
- No link to tactical schema definitions
- Can't validate that story references actual tactical objects

**Issue 3: WorkObject vs Entity Confusion**
- Domain stories introduce `WorkObject` concept
- Similar to `Entity` in tactical schema
- Not clear when to use which

**Issue 4: Scaling Problem**
- Each domain story embeds complete aggregate definitions
- Same aggregate in multiple stories = duplicated definition
- No single source of truth for aggregate structure

---

## Part 2: Placement Option Analysis

### Option A: Standalone Schema (Current - Enhanced) ✅

**Approach**: Keep domain stories separate but refactor to reference tactical types by ID

#### Proposed Structure

```yaml
# domain-stories-schema.yaml (v2.0)
properties:
  domain_stories:
    type: array
    items: { $ref: "#/$defs/DomainStory" }

$defs:
  # =====================================
  # ID TYPES (shared with tactical)
  # =====================================
  BcId:
    type: string
    pattern: "^bc_[a-z0-9_]+$"

  AggId:
    type: string
    pattern: "^agg_[a-z0-9_]+$"

  # ... other tactical ID types

  # =====================================
  # DOMAIN STORY SPECIFIC TYPES
  # =====================================
  DstId:
    type: string
    pattern: "^dst_[a-z0-9_]+$"

  ActId:
    type: string
    pattern: "^act_[a-z0-9_]+$"

  # =====================================
  # CORE TYPES
  # =====================================
  Actor:
    type: object
    required: [actor_id, name, kind]
    properties:
      actor_id: { $ref: "#/$defs/ActId" }
      name: string
      kind:
        type: string
        enum: [person, system, role]

  DomainStory:
    type: object
    required: [domain_story_id, title, actors]
    properties:
      domain_story_id: { $ref: "#/$defs/DstId" }
      title: string
      description: string

      # SCOPE: Which bounded context(s) this story spans
      bounded_contexts:
        type: array
        description: "Bounded contexts involved in this story"
        items: { $ref: "#/$defs/BcId" }
        minItems: 1

      # ACTORS: Define actors (story-specific concept)
      actors:
        type: array
        items: { $ref: "#/$defs/Actor" }
        minItems: 1

      # REFERENCES: Link to tactical objects by ID
      aggregates_involved:
        type: array
        description: "Aggregates used in this story (reference tactical schema)"
        items: { $ref: "#/$defs/AggId" }

      commands_invoked:
        type: array
        description: "Commands executed in this story"
        items: { $ref: "#/$defs/CmdId" }

      queries_executed:
        type: array
        description: "Queries executed in this story"
        items: { $ref: "#/$defs/QryId" }

      events_published:
        type: array
        description: "Events published during this story"
        items: { $ref: "#/$defs/EvtId" }

      repositories_accessed:
        type: array
        description: "Repositories accessed"
        items: { $ref: "#/$defs/RepoId" }

      application_services_called:
        type: array
        description: "Application services orchestrating this story"
        items: { $ref: "#/$defs/SvcAppId" }

      # NARRATIVE: Story-specific concepts
      narrative:
        type: object
        properties:
          steps:
            type: array
            items: { $ref: "#/$defs/StoryStep" }

  StoryStep:
    type: object
    required: [sequence, actor_id, action]
    properties:
      sequence:
        type: integer
        minimum: 1

      actor_id:
        $ref: "#/$defs/ActId"
        description: "Which actor performs this step"

      action:
        type: string
        description: "What the actor does (in domain language)"

      invokes_command:
        $ref: "#/$defs/CmdId"
        description: "Command triggered by this action"

      triggers_events:
        type: array
        items: { $ref: "#/$defs/EvtId" }
        description: "Events published as result"
```

#### Example Usage

```yaml
# models/domain-stories/customer-registration-story.yaml

domain_stories:
  - domain_story_id: dst_customer_registration
    title: "Customer Self-Registration"
    description: "New customer registers account via web interface"

    bounded_contexts:
      - bc_customer_profile
      - bc_notification

    actors:
      - actor_id: act_new_customer
        name: "New Customer"
        kind: person

      - actor_id: act_email_service
        name: "Email Service"
        kind: system

    aggregates_involved:
      - agg_customer  # ← References tactical/bc_customer_profile.yaml
      - agg_notification  # ← References tactical/bc_notification.yaml

    commands_invoked:
      - cmd_create_customer  # ← References tactical schema
      - cmd_send_welcome_email

    events_published:
      - evt_customer_created
      - evt_welcome_email_sent

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

        - sequence: 3
          actor_id: act_email_service
          action: "Sends welcome email"
          invokes_command: cmd_send_welcome_email
          triggers_events:
            - evt_welcome_email_sent
```

#### Pros

✅ **Clear separation**: Domain stories for narrative, tactical for implementation
✅ **No duplication**: References tactical objects, doesn't redefine them
✅ **Referential integrity**: Can validate story references actual tactical objects
✅ **Cross-BC stories**: Can reference objects from multiple BCs
✅ **Independence**: Can evolve domain stories without touching tactical
✅ **Reusability**: Same aggregate can appear in multiple stories (no duplication)
✅ **Single source of truth**: Tactical schema owns aggregate definitions

#### Cons

⚠️ **Two files needed**: Domain story + tactical schema(s) for validation
⚠️ **ID dependencies**: Must know tactical object IDs
⚠️ **Breaking change**: Completely different structure from v1.x

#### Feasibility Assessment

**Containment Hierarchy**: ✅ **Flexible** - Stories can reference objects from one or multiple BCs

**Strategic or Tactical**: ✅ **Neither** - Domain stories operate at narrative/analysis level, above tactical details

**Reference vs Embed**: ✅ **Reference by ID** - Aligns with flat schema principle and DDD

**Multi-BC Stories**: ✅ **Easily handled** - Story lists involved BCs and references objects by ID

#### Impact on Existing Types

| Type | Current (Domain Stories) | Proposed (v2.0) | Rationale |
|------|-------------------------|-----------------|-----------|
| **Actor** | Keep in domain stories | Keep in domain stories | Story-specific concept |
| **WorkObject** | Remove | Remove | Use tactical Entity/ValueObject |
| **Aggregate** | Defined in schema | Reference by ID | Use tactical definition |
| **Repository** | Defined in schema | Reference by ID | Use tactical definition |
| **Command** | Defined in schema | Reference by ID | Use tactical definition |
| **Query** | Defined in schema | Reference by ID | Use tactical definition |
| **Event** | Defined in schema | Reference by ID | Use tactical definition |
| **Activity** | Keep in domain stories | Keep in domain stories | Story-specific concept |
| **Policy** | Keep in domain stories | Keep in domain stories | Story-specific concept |
| **BusinessRule** | Keep in domain stories | Keep in domain stories | Story-specific concept |
| **ReadModel** | Defined in schema | Reference by ID | Use tactical definition |

**Summary**: Keep story-specific concepts (Actor, Activity, Policy, BusinessRule), reference tactical types by ID

**Verdict**: ✅ **RECOMMENDED**

---

### Option B: DomainStory as Tactical Type Under BoundedContext ❌

**Approach**: Move DomainStory into tactical schema as a type contained within BoundedContext

#### Proposed Structure

```yaml
# tactical-ddd.schema.yaml (with domain stories)
$defs:
  BoundedContext:
    properties:
      id: { $ref: "#/$defs/BcId" }
      name: string

      # Tactical objects
      aggregates: [...]
      entities: [...]

      # Domain stories within this BC
      domain_stories:
        type: array
        items: { $ref: "#/$defs/DomainStory" }

  DomainStory:
    properties:
      id: { $ref: "#/$defs/DstId" }
      title: string

      # References tactical objects in SAME BC
      actors:
        type: array
        items: { $ref: "#/$defs/ActId" }

      aggregates_involved:
        type: array
        items: { $ref: "#/$defs/AggId" }  # ← Must be in same BC
```

#### Pros

✅ Direct references to tactical objects (same file)
✅ Clear containment: Stories belong to BC
✅ Single schema file

#### Cons

❌ **Cannot model cross-BC stories** - Critical failure!
❌ **Couples domain storytelling to tactical schema** - Wrong abstraction
❌ **BC-scoped stories only** - Many stories span multiple BCs
❌ **Duplicate stories** - If story involves BC1 and BC2, must copy to both?

#### Example Problem: Cross-BC Story

**Story**: "Customer places order"
- Involves `bc_customer_profile` (validate customer)
- Involves `bc_order_mgmt` (create order)
- Involves `bc_inventory` (check stock)
- Involves `bc_payment` (process payment)

**Question**: Which BC owns this story?
- **Answer**: None! It's a cross-BC orchestration.

**With Option B**: Would need to duplicate story in 4 BCs (terrible!)

**Verdict**: ❌ **REJECTED** - Cannot handle cross-BC stories

---

### Option C: Domain Stories Operating on Strategic Types ❌

**Approach**: Domain stories reference strategic types (domains, BCs, context mappings)

#### Proposed Structure

```yaml
# domain-stories-schema.yaml (strategic references)
$defs:
  DomainStory:
    properties:
      id: { $ref: "#/$defs/DstId" }
      title: string

      # References to STRATEGIC schema
      domains_involved:
        type: array
        items: { $ref: "#/$defs/DomId" }  # ← Strategic level

      bounded_contexts_involved:
        type: array
        items: { $ref: "#/$defs/BcId" }  # ← Strategic level

      context_mappings_used:
        type: array
        items: { $ref: "#/$defs/CmId" }  # ← Strategic level

      # NO reference to aggregates, commands, etc.
```

#### Pros

✅ Can show cross-BC choreography
✅ Strategic-level view

#### Cons

❌ **Wrong abstraction level** - Domain stories are about user actions, not BC relationships
❌ **Too high-level** - Can't reference specific commands/aggregates
❌ **Not useful** - Stories need tactical details (what command, which aggregate)
❌ **Doesn't solve duplication** - Still need to define tactical concepts somewhere

**Verdict**: ❌ **REJECTED** - Wrong abstraction level for domain storytelling

---

## Part 3: Recommended Approach (Option A Enhanced)

### 3.1 Architecture

```
┌─────────────────────────────────────────────┐
│ STRATEGIC SCHEMA                            │
│ System → Domain → BoundedContext            │
│ (Strategic concerns)                        │
└─────────────────────────────────────────────┘
                    ▲
                    │ references BC IDs
                    │
┌─────────────────────────────────────────────┐
│ DOMAIN STORIES SCHEMA                       │
│ DomainStory (narrative/analysis)            │
│   ├─ bounded_contexts: [bc_*]              │◄─┐
│   ├─ actors: [Actor]                        │  │
│   ├─ aggregates_involved: [agg_*]          │  │ References
│   ├─ commands_invoked: [cmd_*]             │  │ by ID
│   ├─ events_published: [evt_*]             │  │
│   └─ narrative: [StoryStep]                 │  │
│                                             │  │
└─────────────────────────────────────────────┘  │
                    │                            │
                    │ references tactical IDs    │
                    ▼                            │
┌─────────────────────────────────────────────┐  │
│ TACTICAL SCHEMA                             │  │
│ BoundedContext (implementation)             │  │
│   ├─ aggregates: [Aggregate]               │──┘
│   ├─ commands: [CommandInterface]          │──┘
│   ├─ events: [DomainEvent]                 │──┘
│   └─ ... (full tactical details)           │
└─────────────────────────────────────────────┘
```

### 3.2 Three-Schema Relationship

**Strategic Schema**:
- Purpose: System boundaries, BC relationships, context mappings
- Granularity: Coarse (system-level)
- Users: Architects, product managers

**Domain Stories Schema**:
- Purpose: User journeys, workflows, narrative analysis
- Granularity: Medium (user story level)
- Users: Domain experts, business analysts, UX designers

**Tactical Schema**:
- Purpose: Implementation details, aggregate design, invariants
- Granularity: Fine (code-level)
- Users: Developers, software architects

### 3.3 Type Ownership

| Type | Owned By | Referenced By | Notes |
|------|----------|---------------|-------|
| **System** | Strategic | Domain Stories (via BC) | Top-level container |
| **Domain** | Strategic | Domain Stories (via BC) | High-level grouping |
| **BoundedContext** | Strategic + Tactical | Domain Stories | Different details each |
| **ContextMapping** | Strategic | Domain Stories | BC relationships |
| **Aggregate** | Tactical | Domain Stories | Implementation details |
| **Entity** | Tactical | Domain Stories | Implementation details |
| **ValueObject** | Tactical | Domain Stories | Implementation details |
| **Command** | Tactical | Domain Stories | User intents |
| **Query** | Tactical | Domain Stories | Data retrieval |
| **Event** | Tactical | Domain Stories | State changes |
| **Actor** | Domain Stories | - | Narrative concept |
| **Activity** | Domain Stories | - | Narrative concept |
| **StoryStep** | Domain Stories | - | Narrative concept |
| **Policy** | Domain Stories | - | Business rule narrative |

### 3.4 File Structure

```
/schemas/
  strategic-ddd.schema.yaml       # Strategic patterns
  tactical-ddd.schema.yaml        # Tactical patterns
  domain-stories.schema.yaml      # Domain storytelling

/models/
  strategic-model.yaml            # System-wide strategic view

  tactical/
    bc_customer_profile.yaml      # Tactical implementation
    bc_order_mgmt.yaml
    bc_inventory.yaml

  domain-stories/
    customer-registration.yaml    # User journey
    order-placement.yaml
    returns-processing.yaml
```

### 3.5 Example: Cross-Schema References

#### Domain Story Document

```yaml
# models/domain-stories/order-placement.yaml

domain_stories:
  - domain_story_id: dst_order_placement
    title: "Customer Places Order"
    description: "Registered customer browses catalog and places order"

    # Strategic reference: Which BCs involved
    bounded_contexts:
      - bc_customer_profile
      - bc_catalog
      - bc_order_mgmt
      - bc_inventory
      - bc_payment

    # Story-specific: Actors
    actors:
      - actor_id: act_customer
        name: "Registered Customer"
        kind: person

      - actor_id: act_payment_gateway
        name: "Payment Gateway"
        kind: system

    # Tactical references: What objects involved
    aggregates_involved:
      - agg_customer       # from bc_customer_profile
      - agg_product        # from bc_catalog
      - agg_order          # from bc_order_mgmt
      - agg_inventory_item # from bc_inventory
      - agg_payment        # from bc_payment

    commands_invoked:
      - cmd_validate_customer        # from bc_customer_profile
      - cmd_check_product_availability  # from bc_catalog
      - cmd_reserve_inventory        # from bc_inventory
      - cmd_create_order             # from bc_order_mgmt
      - cmd_process_payment          # from bc_payment

    events_published:
      - evt_customer_validated
      - evt_inventory_reserved
      - evt_order_created
      - evt_payment_processed
      - evt_order_confirmed

    narrative:
      steps:
        - sequence: 1
          actor_id: act_customer
          action: "Views product details"
          invokes_command: cmd_check_product_availability

        - sequence: 2
          actor_id: act_customer
          action: "Adds product to cart"

        - sequence: 3
          actor_id: act_customer
          action: "Proceeds to checkout"
          invokes_command: cmd_validate_customer

        - sequence: 4
          actor_id: act_customer
          action: "Confirms order"
          invokes_command: cmd_create_order
          triggers_events:
            - evt_inventory_reserved
            - evt_order_created

        - sequence: 5
          actor_id: act_payment_gateway
          action: "Processes payment"
          invokes_command: cmd_process_payment
          triggers_events:
            - evt_payment_processed
            - evt_order_confirmed
```

#### Validation

**Check 1**: Do referenced BCs exist in strategic model?
```python
# Validate bc_customer_profile exists in strategic-model.yaml
assert "bc_customer_profile" in strategic_model.bounded_contexts
```

**Check 2**: Do referenced aggregates exist in tactical models?
```python
# Validate agg_customer exists in tactical/bc_customer_profile.yaml
bc_customer = load_tactical("bc_customer_profile.yaml")
assert "agg_customer" in bc_customer.aggregates
```

**Check 3**: Do referenced commands exist in tactical models?
```python
# Validate cmd_create_order exists in tactical/bc_order_mgmt.yaml
bc_order = load_tactical("bc_order_mgmt.yaml")
assert "cmd_create_order" in bc_order.command_interfaces
```

### 3.6 Benefits Summary

#### For Domain Experts
✅ Write stories in natural language (narrative.steps)
✅ Link to actual system objects (aggregates, commands)
✅ See cross-BC interactions clearly
✅ Independent from implementation details

#### For Developers
✅ Understand user context for tactical objects
✅ See which stories use which aggregates
✅ Validate story references point to real objects
✅ Generate traceability matrix (story ↔ aggregate ↔ code)

#### For Architects
✅ See which BCs collaborate in workflows
✅ Identify cross-BC dependencies
✅ Spot missing context mappings
✅ Validate BC boundaries

---

## Part 4: Migration Strategy

### 4.1 Current to v2.0 Transformation

**Step 1**: Extract story metadata

```yaml
# v1.x (embedded):
domain_stories:
  - domain_story_id: dst_example
    aggregates:
      - aggregate_id: agg_customer
        name: "Customer Aggregate"
        root_work_object_id: wobj_customer
        # ... full definition

# v2.0 (referenced):
domain_stories:
  - domain_story_id: dst_example
    aggregates_involved:
      - agg_customer  # ← Just ID
```

**Step 2**: Move aggregate definitions to tactical schema

```yaml
# Create tactical/bc_customer_profile.yaml:
bounded_context:
  id: bc_customer_profile
  aggregates:
    - id: agg_customer
      name: "Customer Aggregate"
      # ... full definition from domain story
```

**Step 3**: Map WorkObject → Entity

```yaml
# v1.x concept:
work_object_id: wobj_customer

# v2.0 equivalent:
entity_id: ent_customer
```

**Step 4**: Add BC scope to story

```yaml
# v2.0: Explicitly list involved BCs
bounded_contexts:
  - bc_customer_profile
```

### 4.2 Migration Tool

```python
# tools/migrate_domain_stories_to_v2.py

def migrate_story(v1_story):
    """Convert v1.x embedded story to v2.0 reference-based"""

    v2_story = {
        "domain_story_id": v1_story["domain_story_id"],
        "title": v1_story["title"],
        "description": v1_story.get("description"),

        # Extract BCs from embedded objects
        "bounded_contexts": extract_bounded_contexts(v1_story),

        # Keep actors (story-specific)
        "actors": v1_story["actors"],

        # Convert embedded to references
        "aggregates_involved": [agg["aggregate_id"] for agg in v1_story.get("aggregates", [])],
        "commands_invoked": [cmd["command_id"] for cmd in v1_story.get("commands", [])],
        "events_published": [evt["event_id"] for evt in v1_story.get("events", [])],

        # TODO: Build narrative from activities
        "narrative": build_narrative(v1_story),
    }

    # Extract embedded tactical objects to separate files
    for agg in v1_story.get("aggregates", []):
        bc_id = determine_bounded_context(agg)
        add_to_tactical_file(bc_id, "aggregate", agg)

    return v2_story
```

---

## Conclusion

**Recommended Approach**: **Option A Enhanced - Standalone Schema with Tactical References**

### Key Decisions

1. **Keep domain stories separate** - Different purpose than strategic/tactical
2. **Reference by ID, not embed** - Aligns with flat schema and DDD principles
3. **Support cross-BC stories** - Essential for real-world workflows
4. **Remove WorkObject** - Use Entity from tactical schema
5. **Keep story-specific concepts** - Actor, Activity, StoryStep, Policy

### Implementation

```yaml
# Domain Stories Schema v2.0
- Standalone schema
- References tactical objects by ID
- Supports multi-BC stories
- Story-specific narrative structure
- ~200 lines (vs 500+ in v1.x)
```

### Migration Impact

- **Breaking change**: YES - complete restructure
- **Data migration**: Required - extract embedded to references
- **Effort**: Medium - tooling can automate most of it
- **Benefit**: Eliminates duplication, enables traceability

This approach provides the best balance of independence, reusability, and integration with tactical schemas.
