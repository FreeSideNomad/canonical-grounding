# DDD-09: Domain Storytelling

**Version:** 2.0.0
**Status:** draft
**Last Updated:** 2025-01-24
**Part of:** DDD Documentation Series

---

## Table of Contents

1. [Overview](#1-overview)
2. [What is Domain Storytelling](#2-what-is-domain-storytelling)
3. [Core Notation](#3-core-notation)
4. [Workshop Facilitation](#4-workshop-facilitation)
5. [From Stories to Bounded Contexts](#5-from-stories-to-bounded-contexts)
6. [Integration with DDD](#6-integration-with-ddd)
7. [Domain Stories Schema](#7-domain-stories-schema)
8. [Examples](#8-examples)
9. [Best Practices](#9-best-practices)
10. [References](#10-references)

---

## 1. Overview

### 1.1 Definition

> "Domain Storytelling is a collaborative Domain-Driven Design technique used to capture and visualize business processes as stories involving actors, activities, and work objects."
> — Domain Stories Schema Context

**Domain Storytelling** is a discovery technique that helps teams understand and document business processes through storytelling. It sits at the intersection of:
- Event Storming (Alberto Brandolini)
- User Story Mapping (Jeff Patton)
- Domain-Driven Design (Eric Evans)

### 1.2 Purpose

Domain Storytelling serves as the **discovery phase** of DDD, occurring **before** tactical modeling:

```
Discovery → Strategic → Tactical
   ↓
Domain Storytelling → Bounded Contexts → Aggregates/Entities
```

**Key Benefits:**
- Reveals hidden domain knowledge
- Identifies actors and their interactions
- Surfaces business processes
- Discovers bounded context boundaries
- Captures events and commands naturally
- Creates shared understanding between experts and developers

### 1.3 When to Use

**Use Domain Storytelling when:**
- ✓ Starting a new DDD project (discovery phase)
- ✓ Entering an unfamiliar domain
- ✓ Domain experts are available for workshops
- ✓ Need to identify bounded context boundaries
- ✓ Want to validate existing models against real processes
- ✓ Documenting business processes for stakeholders

**Skip or minimize when:**
- ✗ Domain is well-understood by the team
- ✗ Domain experts unavailable
- ✗ Time pressure requires jumping to tactical patterns
- ✗ Domain is purely technical (no business process)

---

## 2. What is Domain Storytelling

### 2.1 The Storytelling Approach

Domain Storytelling uses natural narrative to explore the domain:

**Traditional Requirements:**
```
"The system shall allow users to submit orders with validation."
```

**Domain Storytelling:**
```
"A Customer selects products, adds them to a shopping cart,
reviews the order, submits it to the System, which validates
inventory, reserves products, and sends a confirmation email."
```

The narrative reveals:
- **Actors**: Customer, System
- **Activities**: selects, adds, reviews, submits, validates, reserves, sends
- **Work Objects**: products, shopping cart, order, inventory, email
- **Sequence**: natural flow of events

### 2.2 Core Philosophy

**Principles:**
1. **Start with Actors**: Who is performing actions?
2. **Follow Activities**: What are they doing?
3. **Identify Work Objects**: What are they manipulating?
4. **Capture Sequence**: What happens in what order?
5. **Surface Events**: What triggers next steps?
6. **Discover Rules**: What constraints exist?

### 2.3 Output Artifacts

Domain Storytelling produces:
- **Domain Stories**: Structured narratives with actors, activities, work objects
- **Story Maps**: Visual flow diagrams
- **Concept Glossary**: Ubiquitous language terms discovered
- **Event Catalog**: Domain events identified
- **Command List**: Actions users can initiate
- **Boundary Candidates**: Potential bounded contexts

---

## 3. Core Notation

### 3.1 Actor-Activity-Work Object Pattern

**Basic Pattern:**
```
[Actor] → [Activity] → [Work Object]
```

**Example:**
```
Customer → submits → Order
   ↓
System → validates → Order
   ↓
System → reserves → Inventory
   ↓
System → sends → ConfirmationEmail
```

### 3.2 Actor Types

From schema: `kind: [person, system, role]`

**Person:**
- Individual humans
- Examples: Customer, Manager, Operator
- Characteristics: Makes decisions, has discretion

**System:**
- Automated actors
- Examples: PaymentSystem, NotificationService, Warehouse
- Characteristics: Deterministic, rule-based

**Role:**
- Generic actor type
- Examples: Administrator, User, Guest
- Characteristics: Permission-based, multiple people

### 3.3 Activities

**Activities** represent actions that change state or produce results.

**Naming Convention:**
- Verb or verb phrase
- Present tense
- Active voice
- Examples: "submits order", "approves loan", "calculates price"

**Activity Properties (from schema):**
```yaml
activity_id: actv_submit_order
name: "Submit Order"
initiated_by_command_id: cmd_submit_order
uses_work_object_ids: [wobj_shopping_cart, wobj_order]
results_in_event_ids: [evt_order_submitted]
calls_app_service_ids: [svc_app_order_management]
```

### 3.4 Work Objects

**Work Objects** are domain artifacts manipulated by activities.

**Characteristics:**
- Nouns from ubiquitous language
- Can become Entities or Value Objects
- May map to Aggregates
- Examples: Order, Invoice, Contract, Product

**Work Object Properties (from schema):**
```yaml
work_object_id: wobj_order
name: "Order"
attributes:
  - name: order_id
    type: uuid
  - name: total_amount
    type: money
aggregate_id: agg_order  # May reference aggregate
```

### 3.5 Commands and Queries

**Commands** express user intent (state-changing):
```yaml
command_id: cmd_submit_order
name: "Submit Order"
actor_ids: [act_customer]
target_aggregate_id: agg_order
emits_events: [evt_order_submitted]
```

**Queries** request information (no side effects):
```yaml
query_id: qry_get_order_status
name: "Get Order Status"
actor_ids: [act_customer]
returns_read_model_id: rmdl_order_summary
```

### 3.6 Events and Policies

**Events** represent facts (past tense):
```yaml
event_id: evt_order_submitted
name: "Order Submitted"
caused_by:
  command_id: cmd_submit_order
affected_aggregate_id: agg_order
policies_triggered: [pol_send_confirmation]
```

**Policies** create reactive rules:
```yaml
policy_id: pol_send_confirmation
name: "Send Order Confirmation"
when_event_id: evt_order_submitted
issues_command_id: cmd_send_email
```

**Policy Pattern:** "When [Event] happens, do [Command]"

---

## 4. Workshop Facilitation

### 4.1 Workshop Setup

**Duration:** 2-4 hours per domain area
**Participants:**
- Domain experts (2-3)
- Developers (2-4)
- Facilitator (1)
- Stakeholders (optional, 1-2)

**Materials:**
- Whiteboard or digital board
- Sticky notes (3 colors: actors, activities, work objects)
- Markers
- Camera for documentation

### 4.2 Workshop Flow

**Phase 1: Warm-up (15 minutes)**
1. Explain notation
2. Pick simple example story
3. Practice together

**Phase 2: Story Discovery (60-90 minutes)**
1. Pick business scenario
2. Ask: "Who starts this process?"
3. Follow the flow:
   - "What does [Actor] do first?"
   - "What happens to [Work Object]?"
   - "Then what?"
4. Capture on board as you go
5. Clarify terminology
6. Ask about variations and exceptions

**Phase 3: Refinement (30-45 minutes)**
1. Review story flow
2. Add missing actors/activities
3. Clarify work object definitions
4. Identify events
5. Discover policies/rules
6. Name concepts consistently

**Phase 4: Analysis (30-45 minutes)**
1. Identify linguistic boundaries
2. Look for context candidates
3. Find natural seams
4. Discuss groupings

### 4.3 Facilitation Tips

**DO:**
- Let domain experts lead
- Focus on real scenarios
- Use exact terminology
- Ask "then what?" repeatedly
- Capture exceptions
- Look for event triggers

**DON'T:**
- Jump to implementation
- Use technical jargon
- Rush the process
- Ignore edge cases
- Impose your model
- Skip variations

### 4.4 Questions to Ask

**Discovery Questions:**
- "Who can initiate this?"
- "What happens first?"
- "What does [actor] need to do that?"
- "When does [event] trigger?"
- "What are the exceptions?"
- "Who needs to know about this?"

**Refinement Questions:**
- "Is [term] the right word?"
- "Does [term] mean the same thing here as over there?"
- "What makes [work object] valid?"
- "When can this NOT happen?"

---

## 5. From Stories to Bounded Contexts

### 5.1 Linguistic Boundaries

**Signs of Different Contexts:**
- Same word, different meanings
- Different words, same concept
- Experts disagree on terminology
- Natural organizational boundaries

**Example:**
```
In Sales: "Order" = customer purchase request
In Fulfillment: "Order" = packing/shipping instruction
→ Two different bounded contexts!
```

### 5.2 Mapping Process

**Step 1: Group Related Stories**
```
Stories about customer purchases → Sales Context
Stories about inventory → Warehouse Context
Stories about shipping → Fulfillment Context
```

**Step 2: Identify Aggregate Candidates**
```
Work objects that change together → Aggregate
Work object that's always entry point → Aggregate Root
```

**Step 3: Extract Events**
```
Activity results → Domain Events
Cross-boundary triggers → Integration Events
```

**Step 4: Define Context Boundaries**
```
Linguistic + Organizational + Technical boundaries
→ Bounded Context definitions
```

### 5.3 Example Transformation

**Domain Story:**
```
Customer → selects → Product
Customer → adds → ShoppingCart
Customer → submits → Order
System → validates → Order
System → reserves → Inventory
System → publishes → OrderPlaced
```

**To Strategic DDD:**
```yaml
bounded_contexts:
  - id: bc_shopping
    domain_ref: dom_sales
    aggregates: [agg_shopping_cart]

  - id: bc_order_management
    domain_ref: dom_sales
    aggregates: [agg_order]

  - id: bc_inventory
    domain_ref: dom_warehouse
    aggregates: [agg_inventory]

context_mappings:
  - id: cm_order_to_inventory
    upstream_context: bc_order_management
    downstream_context: bc_inventory
    relationship_type: customer_supplier
```

**To Tactical DDD:**
```yaml
aggregates:
  - id: agg_order
    name: Order
    root_ref: ent_order
    entities: [ent_order, ent_line_item]
    value_objects: [vo_money, vo_address]
    invariants:
      - "Order total must equal sum of line items"
      - "Order must have at least one line item"

domain_events:
  - id: evt_order_placed
    name: OrderPlaced
    aggregate_ref: agg_order
```

---

## 6. Integration with DDD

### 6.1 Relationship to Strategic Patterns

**Domain Storytelling feeds Strategic DDD:**

```
Domain Stories
   ↓ (linguistic analysis)
Bounded Contexts
   ↓ (relationship analysis)
Context Mappings
   ↓ (aggregation analysis)
BFF Scopes (client-specific aggregations)
```

### 6.2 Relationship to Tactical Patterns

**Work Objects become:**
- Aggregates (consistency boundaries)
- Entities (with identity)
- Value Objects (without identity)

**Activities become:**
- Commands (state-changing)
- Queries (information retrieval)
- Domain Events (facts)

**Actors become:**
- Use case initiators
- Security principals
- BFF clients

### 6.3 Relationship to Application Layer

**Story Flow → Application Service Workflow:**

```
Story: Customer submits order
   ↓
Application Service Operation:
  1. Validate input (customer, items)
  2. Load aggregate (Order.create())
  3. Execute domain logic (order.addItems())
  4. Persist aggregate (orderRepo.save())
  5. Publish events (OrderPlaced)
  6. Return result (OrderId)
```

### 6.4 Integration with Event Storming

**Complementary Techniques:**

| Domain Storytelling | Event Storming |
|---------------------|----------------|
| Actor-focused | Event-focused |
| Sequential flow | Temporal flow |
| Narrative format | Post-it chaos |
| Work objects explicit | Aggregates emerge |
| Good for processes | Good for events |

**Combined Approach:**
1. Start with Domain Storytelling (structure)
2. Use Event Storming for complex flows
3. Validate stories against events
4. Refine both iteratively

---

## 7. Domain Stories Schema

### 7.1 Schema Overview

The domain-stories-schema.yaml formalizes Domain Storytelling artifacts for:
- **Validation**: Ensure story structure is correct
- **Tool Support**: Enable LLM reasoning about stories
- **Documentation**: Machine-readable domain knowledge
- **Generation**: Generate code from stories

### 7.2 Schema Structure

```yaml
domain_stories:
  - domain_story_id: dst_checkout_process
    title: "E-commerce Checkout Process"
    actors: [...]        # Actor definitions
    work_objects: [...]  # Work object definitions
    commands: [...]      # Command definitions
    queries: [...]       # Query definitions
    activities: [...]    # Activity definitions
    events: [...]        # Event definitions
    policies: [...]      # Policy definitions
    aggregates: [...]    # Aggregate mappings
    repositories: [...]  # Repository references
    application_services: [...]  # Service references
    domain_services: [...] # Domain service references
    read_models: [...]   # Query model references
    business_rules: [...] # Rule definitions
```

### 7.3 ID Conventions

All IDs follow consistent patterns:

| Type | Prefix | Example |
|------|--------|---------|
| Domain Story | `dst_` | `dst_checkout_process` |
| Actor | `act_` | `act_customer` |
| Work Object | `wobj_` | `wobj_order` |
| Activity | `actv_` | `actv_submit_order` |
| Command | `cmd_` | `cmd_place_order` |
| Query | `qry_` | `qry_get_order_status` |
| Event | `evt_` | `evt_order_placed` |
| Policy | `pol_` | `pol_send_confirmation` |
| Business Rule | `rle_` | `rle_order_minimum` |

### 7.4 Causal Chain in Schema

The schema captures the complete causal flow:

```
Actor → Command → Activity → Event → Policy → Command
  ↓        ↓          ↓         ↓        ↓
Initiates  Triggers   Uses      Results  Reactive
           Work       Work       In      Automation
           Objects    Objects    Facts
```

---

## 8. Examples

### 8.1 Simple Checkout Story

*[To be populated with example from schema]*

### 8.2 Loan Approval Process

*[To be populated with complex example]*

### 8.3 Real Workshop Output

*[To be populated with annotated workshop photos/diagrams]*

---

## 9. Best Practices

### 9.1 Story Discovery

✅ **DO:**
- Start with happy path
- Add variations incrementally
- Use real examples
- Capture exact terminology
- Note exceptions
- Follow complete flows

❌ **DON'T:**
- Jump to edge cases first
- Use hypotheticals
- Translate terminology
- Skip "obvious" steps
- Ignore variations

### 9.2 Notation

✅ **DO:**
- Keep it simple
- Use color coding
- Show sequence clearly
- Label relationships
- Capture both actors and systems

❌ **DON'T:**
- Over-complicate notation
- Use technical UML
- Skip intermediate steps
- Hide system actors

### 9.3 Workshop Dynamics

✅ **DO:**
- Let experts lead
- Ask clarifying questions
- Pause for deep discussions
- Validate understanding
- Capture glossary terms

❌ **DON'T:**
- Dominate conversation
- Rush experts
- Impose solutions
- Argue about terms
- Skip edge cases

---

## 10. References

### Books and Articles
- *Domain Storytelling* by Stefan Hofer and Henning Schwentner (2021)
- *Introducing EventStorming* by Alberto Brandolini (2021)
- *Domain-Driven Design* by Eric Evans (2003) - Chapter on Knowledge Crunching
- "The Back-end for Front-end Pattern (BFF)" by Phil Calçado (2015) - BFF concept origins

### Schema References
- `/domain-stories/domain-stories-schema.yaml` v2.0
- `/domain-stories/domain-stories-context.md`

### Related DDD Documentation
- ddd-01-ddd-foundations.md (Ubiquitous Language)
- ddd-02-strategic-patterns.md (Bounded Contexts)
- ddd-03-tactical-patterns.md (Aggregates, Events)
- ddd-04-ubiquitous-language.md (Language Development)

---

**Note:** This chapter is a DRAFT structure. Content will be fully populated during ddd-guide.md assembly from research and schema definitions.
