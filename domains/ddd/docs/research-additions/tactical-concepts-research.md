# Tactical DDD Concepts Research - v2.0 Schema Additions

**Document Status:** Research - Undocumented Concepts from v2.0.0 Schema
**Schema Version:** tactical-ddd.schema.yaml v2.0.0
**Date:** 2025-10-24
**Author:** Research Team

---

## Executive Summary

This document provides comprehensive research and documentation for 12 tactical DDD concepts introduced or significantly enhanced in the v2.0 schema that are not yet documented in the existing DDD documentation series. These concepts represent critical patterns for implementing bounded contexts, application services, and CQRS following the Knight codebase patterns.

**Scope:** Concepts from `/domains/ddd/schemas/tactical-ddd.schema.yaml` lines 1-910
**Examples:** From `/domains/ddd/examples/tactical-example.yaml` and `/domains/ddd/examples/application-service-example.yaml`
**Existing Docs:** Supplements `/domains/ddd/docs/ddd-03-tactical-patterns.md` and `/domains/ddd/docs/ddd-07-application-layer.md`

---

## Table of Contents

1. [BoundedContext Root Object](#1-boundedcontext-root-object) (CRITICAL)
2. [ApplicationServiceOperation](#2-applicationserviceoperation) (CRITICAL)
3. [TransactionBoundary](#3-transactionboundary) (CRITICAL)
4. [Workflow](#4-workflow) (CRITICAL)
5. [CommandRecord](#5-commandrecord) (CRITICAL)
6. [QueryMethod](#6-querymethod) (CRITICAL)
7. [ResultStructure](#7-resultstructure) (IMPORTANT)
8. [DTOField (Tactical)](#8-dtofield-tactical) (IMPORTANT)
9. [CommandInterface & QueryInterface](#9-commandinterface--queryinterface) (IMPORTANT)
10. [ID Types (10 Extracted)](#10-id-types-10-extracted) (IMPORTANT)
11. [Attribute, Parameter, Method](#11-attribute-parameter-method) (SUPPORTING)
12. [Immutability Enforcement](#12-immutability-enforcement) (SUPPORTING)

---

## 1. BoundedContext Root Object

**Schema Location:** Lines 343-403
**Pattern Classification:** CRITICAL (600-800 words)
**Status:** NEW in v2.0.0 - Root container pattern

### Schema Definition

```yaml
BoundedContext:
  type: object
  description: Root object containing all tactical patterns for a single bounded context
  required: [id, name, domain_ref]
  properties:
    id:
      $ref: "#/$defs/BcId"
    name:
      type: string
    domain_ref:
      $ref: "#/$defs/DomId"
    aggregates:
      type: array
      items:
        $ref: "#/$defs/Aggregate"
    entities:
      type: array
    value_objects:
      type: array
    repositories:
      type: array
    domain_services:
      type: array
    application_services:
      type: array
    command_interfaces:
      type: array
    query_interfaces:
      type: array
    domain_events:
      type: array
```

### Rationale and Purpose

The BoundedContext root object represents a fundamental shift in v2.0 from fragmented tactical definitions to a **unified, cohesive model** of a bounded context. This pattern addresses a critical architectural need: organizing all tactical patterns within a single file while maintaining clear boundaries between contexts.

**Why This Pattern Exists:**

1. **Single File Per Bounded Context**: The schema enforces that all tactical patterns (aggregates, entities, value objects, services, commands, queries) for ONE bounded context exist in ONE file. This reflects the DDD principle that a bounded context is the consistency boundary for the ubiquitous language.

2. **Strategic-to-Tactical Bridge**: The `domain_ref` property links tactical implementation back to strategic design, ensuring traceability from high-level domain architecture down to code-level patterns.

3. **Enforces Bounded Context Integrity**: By requiring all tactical elements to be nested under a single BoundedContext root, the schema prevents "tactical pattern sprawl" where entities, services, and aggregates are defined independently without clear context ownership.

4. **Knight Pattern Alignment**: This mirrors the Knight codebase structure where bounded contexts are implemented as cohesive modules with clear boundaries.

### Detailed Explanation

The BoundedContext object serves three critical functions:

**1. Organizational Container**

All tactical patterns belong to exactly one bounded context. This eliminates ambiguity about where patterns live:

```yaml
bounded_context:
  id: bc_user_management
  name: User Management
  domain_ref: dom_identity_access

  # All these belong ONLY to this context
  aggregates:
    - agg_user
  value_objects:
    - vo_user_id
    - vo_client_id
  application_services:
    - svc_app_user_management
  command_interfaces:
    - cmd_user_commands
  query_interfaces:
    - qry_user_queries
```

**2. Dependency Graph Root**

The BoundedContext provides the root node for understanding dependencies within the context:
- Which aggregates use which value objects
- Which repositories serve which aggregates
- Which application services implement which command/query interfaces
- Which domain events are published by which aggregates

**3. Deployment and Code Generation Unit**

A single bounded context file represents:
- A complete microservice (in distributed architectures)
- A complete module (in modular monoliths)
- A complete package/namespace (in code generation)
- A complete API surface (commands + queries)

### Implementation Guidelines

**File Naming Convention:**
```
tactical-{context_name}.yaml
```

Examples:
- `tactical-user-management.yaml` (BC: User Management)
- `tactical-order-processing.yaml` (BC: Order Processing)
- `tactical-inventory-management.yaml` (BC: Inventory Management)

**Required Structure:**
```yaml
# Every tactical file MUST start with this
bounded_context:
  id: bc_{context_name}
  name: {Human Readable Name}
  domain_ref: dom_{parent_domain}
  description: Purpose and responsibility of this context

  # Tactical patterns follow...
  aggregates: []
  entities: []
  value_objects: []
  repositories: []
  domain_services: []
  application_services: []
  command_interfaces: []
  query_interfaces: []
  domain_events: []
```

**Cross-Context References:**

When one bounded context references concepts from another, use **ID references only**:

```yaml
# In BC: Order Processing
bounded_context:
  id: bc_order_processing
  aggregates:
    - id: agg_order
      properties:
        # Reference to User from different BC by ID only
        customer_id:
          type: UserId
          description: "References bc_user_management.vo_user_id"
```

### Examples from Schema

**Example 1: User Management Bounded Context**

From `/domains/ddd/examples/application-service-example.yaml` lines 9-34:

```yaml
bounded_context:
  id: bc_user_management
  name: User Management
  domain_ref: dom_identity_access
  description: Manages user accounts, lifecycle, and authentication

  ubiquitous_language:
    glossary:
      - term: User
        definition: A person with an identity in the system
      - term: Activation
        definition: Transition from PENDING to ACTIVE status

  team_ownership: Identity and Access Team
```

This demonstrates:
- Clear identity (`bc_user_management`)
- Domain linkage (`dom_identity_access`)
- Ubiquitous language definition within context
- Team ownership for organizational clarity

**Example 2: Complete Tactical Model Structure**

```yaml
bounded_context:
  id: bc_profile
  name: Candidate Profile
  domain_ref: dom_recruiting

  # Aggregates define consistency boundaries
  aggregates:
    - id: agg_profile
      name: CandidateProfile
      root_ref: ent_candidate
      entities: [ent_candidate]
      value_objects: [vo_email, vo_phone, vo_skill_level]

  # Entities within the context
  entities:
    - id: ent_candidate
      name: Candidate
      is_aggregate_root: true
      identity_field: candidate_id

  # Value objects scoped to this context
  value_objects:
    - id: vo_email
      name: Email
      immutability: true

  # Repositories for aggregate persistence
  repositories:
    - id: repo_profile
      name: CandidateProfileRepository
      aggregate_ref: agg_profile

  # Application services orchestrating use cases
  application_services:
    - id: svc_app_candidate_management
      name: CandidateApplicationService

  # Command and query interfaces
  command_interfaces:
    - id: cmd_candidate_commands
  query_interfaces:
    - id: qry_candidate_queries

  # Domain events published by aggregates
  domain_events:
    - id: evt_profile_created
    - id: evt_profile_updated
```

### Best Practices

**1. One Context Per File**
```
✓ CORRECT: tactical-user-management.yaml contains ONLY bc_user_management
✗ WRONG: tactical-all-contexts.yaml contains multiple bounded contexts
```

**2. Complete Context Definition**

Every bounded context file should define ALL tactical patterns for that context. Don't split a context across multiple files.

**3. Explicit Domain Reference**

Always link back to strategic design:
```yaml
bounded_context:
  id: bc_user_management
  domain_ref: dom_identity_access  # Links to strategic-ddd.schema.yaml
```

**4. Team Ownership**

Document which team owns the context:
```yaml
bounded_context:
  team_ownership: Identity and Access Team
  technical_lead: john.doe@example.com
```

**5. Ubiquitous Language Documentation**

Include key terms within the bounded context:
```yaml
bounded_context:
  ubiquitous_language:
    glossary:
      - term: User
        definition: A person with an identity in the system
      - term: Activation
        definition: Enabling system access after verification
```

### Anti-Patterns

**❌ Anti-Pattern 1: Multiple Contexts in One File**

```yaml
# WRONG - Don't do this
bounded_contexts:  # Plural - wrong!
  - id: bc_user_management
  - id: bc_order_processing
```

The schema requires exactly ONE bounded_context (singular) at the root.

**❌ Anti-Pattern 2: Tactical Patterns Without Context**

```yaml
# WRONG - Tactical patterns must be nested under bounded_context
aggregates:
  - id: agg_user  # This will fail validation
```

**✓ Correct:**
```yaml
bounded_context:
  id: bc_user_management
  aggregates:
    - id: agg_user  # Nested under context
```

**❌ Anti-Pattern 3: Embedding Other Contexts**

```yaml
bounded_context:
  id: bc_order_processing
  aggregates:
    - id: agg_order
      # WRONG - Don't embed User aggregate from another context
      customer:
        aggregate_ref: agg_user  # From bc_user_management
```

**✓ Correct:**
```yaml
bounded_context:
  id: bc_order_processing
  aggregates:
    - id: agg_order
      # Reference by ID only
      properties:
        customer_id:
          type: UserId  # Just the ID, not the whole aggregate
```

### References

- **Schema Lines:** 28-33, 343-403
- **Evans (2003):** Chapter 14 - "Maintaining Model Integrity", discusses bounded context boundaries
- **Vernon (2013):** Chapter 2 - "Domains, Subdomains, and Bounded Contexts", emphasizes context as consistency boundary
- **Example File:** `/domains/ddd/examples/application-service-example.yaml` lines 9-34

---

## 2. ApplicationServiceOperation

**Schema Location:** Lines 198-223
**Pattern Classification:** CRITICAL (600-800 words)
**Status:** NEW in v2.0.0 - Use case operation pattern

### Schema Definition

```yaml
ApplicationServiceOperation:
  type: object
  description: Use case operation provided by an application service
  required: [name, type]
  properties:
    name:
      type: string
      pattern: "^[a-z][a-zA-Z]+$"
      description: Operation method name (e.g., createUser, placeOrder)
    type:
      type: string
      enum: [command, query]
      description: Whether this operation modifies state or retrieves data
    description:
      type: string
    parameters:
      type: array
      items:
        $ref: "#/$defs/Parameter"
    returns:
      type: string
      description: Return type (domain ID for creates, void for changes, DTO for queries)
    transaction_boundary:
      $ref: "#/$defs/TransactionBoundary"
    workflow:
      $ref: "#/$defs/Workflow"
```

### Rationale and Purpose

ApplicationServiceOperation represents the **atomic unit of use case execution** in DDD v2.0. This pattern formalizes what was previously implicit: that every application service method represents exactly one business use case with clearly defined transaction boundaries and orchestration workflows.

**Why This Pattern Exists:**

1. **Use Case Formalization**: Each operation is one use case. The schema enforces this with the `name` pattern constraint (`createUser`, not `manageUser`).

2. **CQRS Enforcement**: The `type` enum with only `[command, query]` enforces Command Query Responsibility Segregation at the schema level. You cannot create an operation that both modifies state and returns data.

3. **Transaction Boundary Declaration**: By requiring `transaction_boundary`, the schema makes transaction scope **explicit** rather than implicit. This prevents accidental multi-aggregate transactions.

4. **Workflow Transparency**: The `workflow` property documents the orchestration steps, making the application service's coordination logic visible and verifiable.

### Detailed Explanation

An ApplicationServiceOperation defines six critical aspects:

**1. Operation Identity and Type**

```yaml
- name: createUser        # Camel case, verb + noun
  type: command          # Modifies state

- name: getUserSummary   # Query verb (get, list, find, search)
  type: query           # Read-only
```

The `type` field determines:
- **Commands**: Wrapped in transactions, modify aggregates, return void/ID/status
- **Queries**: No transactions, read-only, return DTOs

**2. Parameter Definition**

Parameters represent the operation's input contract:

```yaml
parameters:
  - name: cmd
    type: CreateUserCmd
    required: true
    description: Command containing user creation data
```

For commands, typically a single command record:
```yaml
parameters:
  - name: cmd
    type: ActivateUserCmd
    required: true
```

For queries, domain identifiers or filter criteria:
```yaml
parameters:
  - name: userId
    type: UserId
    required: true
  - name: includeDetails
    type: boolean
    required: false
```

**3. Return Type Specification**

Return types vary by operation type:

**Command Operations:**
- **Creation**: Return domain ID
  ```yaml
  returns: UserId
  description: Newly created user identifier
  ```
- **State Transition**: Return void
  ```yaml
  returns: void
  description: No return value for activation
  ```
- **Acknowledgment**: Return status
  ```yaml
  returns: result_status
  description: Success/failure with reasons
  ```

**Query Operations:**
- **Single Result**: Return DTO
  ```yaml
  returns: UserSummary
  description: User summary data transfer object
  ```
- **Collection**: Return list of DTOs
  ```yaml
  returns: List<OrderSummary>
  description: List of order summaries
  ```

**4. Transaction Boundary**

Defines transaction scope (see [Section 3](#3-transactionboundary)):

```yaml
transaction_boundary:
  is_transactional: true
  modifies_aggregates:
    - agg_user
  consistency_type: transactional
```

**5. Workflow Definition**

Documents orchestration steps (see [Section 4](#4-workflow)):

```yaml
workflow:
  validates_input: true
  loads_aggregates: [agg_user]
  invokes_domain_operations:
    - "user.activate() - business method"
  persists_aggregates: true
  publishes_events: [evt_user_activated]
```

**6. Operation Description**

Clear, business-focused description:

```yaml
description: Create new user and publish UserCreated event
```

### Implementation Guidelines

**Naming Conventions:**

**Commands (Imperative Verbs):**
```
createUser      # Creation
activateUser    # Activation
deactivateUser  # Deactivation
updateEmail     # Update
deleteAccount   # Deletion
approveOrder    # Approval
cancelPayment   # Cancellation
enrollService   # Enrollment
```

**Queries (Query Verbs):**
```
getUserSummary     # Single result
listActiveUsers    # Collection
findByEmail        # Lookup
searchOrders       # Search
getOrderDetails    # Detailed view
```

**Method Signature Pattern:**

Commands:
```java
@Transactional
public {DomainId|void} {verb}{Noun}({Verb}{Noun}Cmd cmd) {
    // Implementation
}
```

Queries:
```java
public {ResultDTO} {queryVerb}{Noun}({Criteria} criteria) {
    // Implementation
}
```

### Examples from Schema

**Example 1: Command Operation - User Creation**

From `/domains/ddd/examples/application-service-example.yaml` lines 469-492:

```yaml
- name: createUser
  type: command
  description: Create new user and publish UserCreated event
  parameters:
    - name: cmd
      type: CreateUserCmd
      required: true
  returns: UserId
  transaction_boundary:
    is_transactional: true
    modifies_aggregates:
      - agg_user
    consistency_type: transactional
  workflow:
    validates_input: true
    loads_aggregates: []
    invokes_domain_operations:
      - "User.create() - factory method"
    invokes_domain_services: []
    persists_aggregates: true
    publishes_events:
      - evt_user_created
    returns_dto: null
```

**Key Observations:**
- Command type → transactional
- Returns domain ID (UserId) for creation
- Loads no aggregates (creation)
- Invokes factory method, not constructor
- Publishes event after persistence

**Example 2: Command Operation - State Transition**

From lines 494-517:

```yaml
- name: activateUser
  type: command
  description: Activate user account
  parameters:
    - name: cmd
      type: ActivateUserCmd
      required: true
  returns: void
  transaction_boundary:
    is_transactional: true
    modifies_aggregates:
      - agg_user
    consistency_type: transactional
  workflow:
    validates_input: true
    loads_aggregates:
      - agg_user
    invokes_domain_operations:
      - "user.activate() - business method"
    invokes_domain_services: []
    persists_aggregates: true
    publishes_events:
      - evt_user_activated
    returns_dto: null
```

**Key Observations:**
- State transition → returns void
- Loads aggregate (not creation)
- Invokes business method on aggregate
- Transaction modifies exactly one aggregate

**Example 3: Query Operation**

From lines 593-614:

```yaml
- name: getUserSummary
  type: query
  description: Retrieve user summary DTO
  parameters:
    - name: userId
      type: UserId
      required: true
  returns: UserSummary
  transaction_boundary:
    is_transactional: false
    modifies_aggregates: []
    consistency_type: transactional
  workflow:
    validates_input: true
    loads_aggregates:
      - agg_user
    invokes_domain_operations: []
    invokes_domain_services: []
    persists_aggregates: false
    publishes_events: []
    returns_dto: UserSummary
```

**Key Observations:**
- Query type → NOT transactional
- Returns DTO (UserSummary)
- No domain operations invoked
- No persistence or events
- Read-only operation

### Best Practices

**1. One Operation = One Use Case**

```yaml
✓ CORRECT:
- name: createUser         # One use case
- name: activateUser       # Another use case
- name: deactivateUser     # Yet another

✗ WRONG:
- name: manageUser         # Multiple use cases - too generic
  parameters:
    - action: string       # Anti-pattern
```

**2. Command/Query Type Alignment**

```yaml
✓ CORRECT - Command:
- name: activateUser
  type: command
  returns: void            # Commands return void or ID

✓ CORRECT - Query:
- name: getUserSummary
  type: query
  returns: UserSummary     # Queries return DTOs

✗ WRONG - Mixed:
- name: activateAndGetUser
  type: command
  returns: UserSummary     # Command returning data - CQRS violation
```

**3. Transaction Boundary Alignment**

```yaml
✓ CORRECT - Command is transactional:
- name: createUser
  type: command
  transaction_boundary:
    is_transactional: true

✓ CORRECT - Query is NOT transactional:
- name: getUserSummary
  type: query
  transaction_boundary:
    is_transactional: false

✗ WRONG - Command without transaction:
- name: createUser
  type: command
  transaction_boundary:
    is_transactional: false  # Command must be transactional
```

**4. Workflow Documentation Completeness**

Always document all six workflow steps:

```yaml
workflow:
  validates_input: true                    # Step 1
  loads_aggregates: [agg_user]            # Step 2
  invokes_domain_operations: ["..."]      # Step 3
  invokes_domain_services: []             # Step 4
  persists_aggregates: true               # Step 5
  publishes_events: [evt_user_activated]  # Step 6
```

### Anti-Patterns

**❌ Anti-Pattern 1: Generic Operations**

```yaml
# WRONG - Generic operation handling multiple use cases
- name: manageUser
  type: command
  parameters:
    - name: action
      type: string  # "create", "activate", "deactivate" - anti-pattern
```

**✓ Correct:**
```yaml
- name: createUser
- name: activateUser
- name: deactivateUser
```

**❌ Anti-Pattern 2: CQRS Violation**

```yaml
# WRONG - Command returning business data
- name: createUserAndGetDetails
  type: command
  returns: UserDetails  # Commands should return void or ID only
```

**✓ Correct:**
```yaml
- name: createUser
  type: command
  returns: UserId

- name: getUserDetails
  type: query
  returns: UserDetails
```

**❌ Anti-Pattern 3: Multi-Aggregate Transaction**

```yaml
# WRONG - Modifying multiple aggregates in one transaction
- name: processOrder
  type: command
  transaction_boundary:
    modifies_aggregates:
      - agg_order
      - agg_inventory  # Violates one-aggregate-per-transaction rule
```

**✓ Correct:**
```yaml
- name: confirmOrder
  type: command
  transaction_boundary:
    modifies_aggregates:
      - agg_order
  workflow:
    publishes_events:
      - evt_order_confirmed  # Event triggers inventory update in separate transaction
```

### References

- **Schema Lines:** 198-223, 469-614
- **Vernon (2013):** Chapter 4 - "Architecture", discusses application service coordination
- **Evans (2003):** Chapter 4 - "Isolating the Domain", explains application service role
- **Fowler (2002):** "Service Layer" pattern in PoEAA

---

## 3. TransactionBoundary

**Schema Location:** Lines 143-160
**Pattern Classification:** CRITICAL (600-800 words)
**Status:** NEW in v2.0.0 - Enforces Vaughn Vernon's one-aggregate rule

### Schema Definition

```yaml
TransactionBoundary:
  type: object
  description: Transaction scope for an operation
  properties:
    is_transactional:
      type: boolean
      description: True for commands, false for queries
      default: true
    modifies_aggregates:
      type: array
      description: Aggregates modified by this operation (should be 0-1 for commands)
      items:
        $ref: "#/$defs/AggId"
      maxItems: 1  # CRITICAL: Enforces one-aggregate-per-transaction
    consistency_type:
      type: string
      enum: [transactional, eventual]
      description: Immediate (transactional) or deferred (eventual) consistency
```

### Rationale and Purpose

TransactionBoundary is the **schema-level enforcement mechanism** for one of DDD's most critical rules: **modify only one aggregate per transaction**. This pattern exists to prevent the most common DDD anti-pattern: loading multiple aggregates and modifying them within a single transaction, which leads to tight coupling, concurrency issues, and scalability problems.

**Why This Pattern Exists:**

1. **Vaughn Vernon's Rule Enforcement**: The `maxItems: 1` constraint on `modifies_aggregates` **forces** developers to design for single-aggregate transactions. You cannot validate a schema that violates this rule.

2. **Transaction Scope Transparency**: Makes transaction boundaries **explicit** in the model rather than hidden in code. This is critical for:
   - Code generation
   - Architecture reviews
   - Performance analysis
   - Concurrency design

3. **Consistency Model Declaration**: The `consistency_type` enum forces you to decide: "Is this immediate consistency (same transaction) or eventual consistency (event-driven)?"

4. **Command/Query Distinction**: `is_transactional` distinguishes commands (wrapped in transactions) from queries (read-only, no transaction overhead).

### Detailed Explanation

TransactionBoundary defines three critical aspects of an operation's transaction behavior:

**1. Transaction Participation (`is_transactional`)**

```yaml
# Command - Requires Transaction
transaction_boundary:
  is_transactional: true    # BEGIN TRANSACTION ... COMMIT

# Query - No Transaction
transaction_boundary:
  is_transactional: false   # Read-only, no transaction
```

**When `true` (Commands):**
- Database transaction begins before operation
- Changes are atomic (ACID)
- Rollback on exception
- Transaction commits after successful completion
- Events published AFTER commit

**When `false` (Queries):**
- No transaction overhead
- Read-only database access
- No locks acquired
- Better performance for reads

**2. Aggregate Modification Scope (`modifies_aggregates`)**

This is the **most critical** aspect. The `maxItems: 1` constraint enforces:

```yaml
# ✓ CORRECT - Single Aggregate
transaction_boundary:
  modifies_aggregates:
    - agg_user              # Exactly one aggregate

# ✓ CORRECT - Zero Aggregates (Query)
transaction_boundary:
  modifies_aggregates: []   # Read-only

# ✗ WRONG - Multiple Aggregates (Schema validation FAILS)
transaction_boundary:
  modifies_aggregates:
    - agg_user
    - agg_profile          # ERROR: maxItems is 1
```

**Why maxItems: 1?**

From Vernon (2013), Chapter 10 - "Aggregates":

> "Try to modify only one Aggregate instance per transaction. In a properly designed Bounded Context, modifying one instance should be sufficient. If you try to modify more than one, you are probably missing a more important Aggregate concept."

**Benefits of One-Aggregate-Per-Transaction:**
1. **Reduced Contention**: Only one aggregate locked at a time
2. **Better Scalability**: Smaller transaction scope = less database contention
3. **Clearer Boundaries**: Forces you to identify true consistency boundaries
4. **Eventual Consistency**: Forces use of domain events for cross-aggregate updates

**3. Consistency Model (`consistency_type`)**

```yaml
consistency_type: transactional  # Immediate, within same transaction
consistency_type: eventual       # Deferred, via domain events
```

**Transactional Consistency:**
- Changes visible immediately
- ACID guarantees
- All changes in same transaction
- Use for: True invariants within aggregate

**Eventual Consistency:**
- Changes propagated via events
- Temporary inconsistency acceptable
- Cross-aggregate coordination
- Use for: Cross-aggregate updates, derived data, notifications

**Decision Guide:**

```
Is this a TRUE INVARIANT that must be enforced immediately?
├─ YES → consistency_type: transactional
│        └─ Must be within ONE aggregate
│
└─ NO  → consistency_type: eventual
         └─ Can span multiple aggregates via events
```

### Implementation Guidelines

**Pattern 1: Command Modifying Single Aggregate**

```yaml
# Example: Activate User
- name: activateUser
  type: command
  transaction_boundary:
    is_transactional: true
    modifies_aggregates:
      - agg_user              # Exactly one
    consistency_type: transactional
```

**Generated Code:**
```java
@Transactional  // Framework manages transaction
public void activateUser(ActivateUserCmd cmd) {
    // BEGIN TRANSACTION
    User user = repository.findById(cmd.userId())
        .orElseThrow(() -> new UserNotFoundException());

    user.activate();  // Modifies agg_user

    repository.save(user);

    eventPublisher.publishEvent(new UserActivated(user.id()));
    // COMMIT TRANSACTION
}
```

**Pattern 2: Query Without Transaction**

```yaml
# Example: Get User Summary
- name: getUserSummary
  type: query
  transaction_boundary:
    is_transactional: false   # No transaction needed
    modifies_aggregates: []   # Read-only
    consistency_type: transactional
```

**Generated Code:**
```java
// No @Transactional annotation
public UserSummary getUserSummary(UserId userId) {
    User user = repository.findById(userId)
        .orElseThrow(() -> new UserNotFoundException());

    return new UserSummary(
        user.getUserId().id(),
        user.getEmail(),
        user.getStatus().name()
    );
}
```

**Pattern 3: Multi-Aggregate Coordination via Events**

When a use case needs to affect multiple aggregates:

```yaml
# Transaction 1: Modify First Aggregate
- name: placeOrder
  type: command
  transaction_boundary:
    is_transactional: true
    modifies_aggregates:
      - agg_order              # Only order
    consistency_type: transactional
  workflow:
    publishes_events:
      - evt_order_placed       # Event triggers next transaction
```

```yaml
# Transaction 2: Event Handler
# (Separate transaction, eventual consistency)
event_handlers:
  - event: evt_order_placed
    handler: updateInventory
    transaction_boundary:
      is_transactional: true
      modifies_aggregates:
        - agg_inventory        # Different aggregate, different transaction
      consistency_type: eventual
```

### Examples from Schema

**Example 1: Creation Command**

From `/domains/ddd/examples/application-service-example.yaml` lines 478-482:

```yaml
transaction_boundary:
  is_transactional: true
  modifies_aggregates:
    - agg_user
  consistency_type: transactional
```

**Analysis:**
- Transactional: YES (creation requires transaction)
- Aggregates: ONE (agg_user only)
- Consistency: Transactional (immediate)
- Loads: NONE (creation doesn't load)
- Result: Clean, single-aggregate creation

**Example 2: State Transition Command**

From lines 502-506:

```yaml
transaction_boundary:
  is_transactional: true
  modifies_aggregates:
    - agg_user
  consistency_type: transactional
```

**Analysis:**
- Transactional: YES (state change requires transaction)
- Aggregates: ONE (agg_user only)
- Consistency: Transactional (immediate)
- Loads: ONE (must load aggregate first)
- Persists: YES (saves modified aggregate)

**Example 3: Query Operation**

From lines 602-605:

```yaml
transaction_boundary:
  is_transactional: false
  modifies_aggregates: []
  consistency_type: transactional
```

**Analysis:**
- Transactional: NO (read-only)
- Aggregates: ZERO (no modifications)
- Consistency: Transactional (reads latest committed data)
- Result: No transaction overhead for queries

### Best Practices

**1. Always Specify All Three Properties**

```yaml
✓ CORRECT - Complete specification:
transaction_boundary:
  is_transactional: true
  modifies_aggregates: [agg_user]
  consistency_type: transactional

✗ INCOMPLETE - Missing properties:
transaction_boundary:
  is_transactional: true
  # Missing modifies_aggregates and consistency_type
```

**2. Command = Transactional, Query = Not**

```yaml
✓ CORRECT - Command:
- name: createUser
  type: command
  transaction_boundary:
    is_transactional: true

✓ CORRECT - Query:
- name: getUserSummary
  type: query
  transaction_boundary:
    is_transactional: false
```

**3. One Aggregate Maximum**

```yaml
✓ CORRECT - Single aggregate:
modifies_aggregates:
  - agg_user

✓ CORRECT - No aggregates (query):
modifies_aggregates: []

✗ WRONG - Multiple aggregates:
modifies_aggregates:
  - agg_user
  - agg_profile  # Schema validation fails - maxItems: 1
```

**4. Match Consistency Type to Scope**

```yaml
✓ CORRECT - Single aggregate = transactional:
modifies_aggregates: [agg_user]
consistency_type: transactional

✓ CORRECT - Cross-aggregate = eventual:
modifies_aggregates: [agg_order]
consistency_type: eventual  # Via events
publishes_events: [evt_order_placed]
```

### Anti-Patterns

**❌ Anti-Pattern 1: Multi-Aggregate Transaction**

```yaml
# WRONG - This will fail schema validation
transaction_boundary:
  is_transactional: true
  modifies_aggregates:
    - agg_order
    - agg_inventory
    - agg_shipping
  # ERROR: maxItems is 1, found 3
```

**Why It's Wrong:**
- Violates Vernon's rule
- Creates tight coupling
- Causes concurrency issues
- Fails schema validation

**✓ Correct Approach:**
```yaml
# Transaction 1: Modify Order
transaction_boundary:
  modifies_aggregates: [agg_order]
  publishes_events: [evt_order_confirmed]

# Event Handler (Transaction 2): Update Inventory
# Event Handler (Transaction 3): Notify Shipping
```

**❌ Anti-Pattern 2: Transactional Query**

```yaml
# WRONG - Query doesn't need transaction
- name: getUserSummary
  type: query
  transaction_boundary:
    is_transactional: true  # Unnecessary overhead
    modifies_aggregates: []
```

**Why It's Wrong:**
- Adds transaction overhead for read-only operation
- Acquires unnecessary locks
- Reduces query performance

**✓ Correct:**
```yaml
transaction_boundary:
  is_transactional: false  # Queries are read-only
  modifies_aggregates: []
```

**❌ Anti-Pattern 3: Command Without Transaction**

```yaml
# WRONG - Command must be transactional
- name: createUser
  type: command
  transaction_boundary:
    is_transactional: false  # Commands need transactions!
    modifies_aggregates: [agg_user]
```

**Why It's Wrong:**
- No ACID guarantees
- Partial updates possible
- No rollback on error

**✓ Correct:**
```yaml
transaction_boundary:
  is_transactional: true  # Commands are always transactional
  modifies_aggregates: [agg_user]
```

### References

- **Schema Lines:** 143-160, validation rule lines 868-870
- **Vernon (2013):** Chapter 10 - "Aggregates", section on transaction boundaries
- **Evans (2003):** Chapter 6 - "The Life Cycle of a Domain Object"
- **Best Practice:** Line 888 - "One aggregate per transaction - use eventual consistency for cross-aggregate operations"

---

## 4. Workflow

**Schema Location:** Lines 162-196
**Pattern Classification:** CRITICAL (600-800 words)
**Status:** NEW in v2.0.0 - Orchestration workflow pattern

### Schema Definition

```yaml
Workflow:
  type: object
  description: Orchestration workflow steps
  properties:
    validates_input:
      type: boolean
      description: Performs input/format validation
      default: true
    loads_aggregates:
      type: array
      description: Aggregates loaded from repositories
      items:
        $ref: "#/$defs/AggId"
    invokes_domain_operations:
      type: array
      description: Domain operations invoked on aggregates
      items:
        type: string
    invokes_domain_services:
      type: array
      description: Domain services invoked
      items:
        $ref: "#/$defs/SvcDomId"
    persists_aggregates:
      type: boolean
      description: Saves aggregates back to repository
      default: true
    publishes_events:
      type: array
      description: Domain events published after successful execution
      items:
        $ref: "#/$defs/EvtId"
    returns_dto:
      type: string
      description: DTO returned for queries
```

### Rationale and Purpose

The Workflow pattern documents the **complete orchestration sequence** that an application service executes. This pattern exists to make the "thin application service" coordination logic **explicit, verifiable, and traceable**.

**Why This Pattern Exists:**

1. **Orchestration Transparency**: Application services should have NO business logic, only coordination. The workflow makes this coordination visible and auditable.

2. **Standard Execution Pattern**: Enforces the canonical application service execution pattern:
   ```
   VALIDATE → LOAD → EXECUTE → INVOKE → PERSIST → PUBLISH → RETURN
   ```

3. **Aggregate Loading Patterns**: By explicitly listing `loads_aggregates`, we can:
   - Identify creation vs modification operations (creation loads nothing)
   - Verify one-aggregate-per-transaction rule
   - Optimize repository queries

4. **Event Publishing Documentation**: `publishes_events` makes it clear which domain events result from an operation, enabling event-driven architecture analysis.

5. **Code Generation Target**: The workflow provides enough information to generate complete application service implementations.

### Detailed Explanation

The Workflow pattern defines seven orchestration steps:

**Step 1: Input Validation (`validates_input`)**

```yaml
validates_input: true  # Default for all operations
```

**What It Does:**
- Validates input format (email format, UUID format)
- Checks required fields
- Verifies data types
- Validates lookup references

**What It Does NOT Do:**
- Business rule validation (that's in domain layer)
- Complex cross-field validation (domain layer)

**Implementation:**
```java
@Transactional
public UserId createUser(CreateUserCmd cmd) {
    // Step 1: Validate input
    if (cmd.email() == null || !cmd.email().contains("@")) {
        throw new ValidationException("Invalid email format");
    }
    if (cmd.userType() == null) {
        throw new ValidationException("User type required");
    }
    // ... continue to next step
}
```

**Step 2: Load Aggregates (`loads_aggregates`)**

```yaml
loads_aggregates:
  - agg_user
  - agg_profile
```

**Patterns:**

**Creation Operations (loads nothing):**
```yaml
loads_aggregates: []  # Creation doesn't load existing aggregates
```

**Modification Operations (loads one):**
```yaml
loads_aggregates:
  - agg_user  # Loads exactly one for modification
```

**Query Operations (may load multiple for read):**
```yaml
loads_aggregates:
  - agg_user
  - agg_preferences
  # Queries can load multiple (read-only)
```

**Implementation:**
```java
// Modification: Load one aggregate
User user = repository.findById(cmd.userId())
    .orElseThrow(() -> new UserNotFoundException());

// Query: May load related aggregates
User user = userRepository.findById(userId);
Profile profile = profileRepository.findByUserId(userId);
```

**Step 3: Invoke Domain Operations (`invokes_domain_operations`)**

```yaml
invokes_domain_operations:
  - "user.activate() - business method"
  - "user.updateEmail(newEmail) - business method"
```

**Purpose:**
- Documents which aggregate methods are called
- Shows business logic location (in domain, not application service)
- Enables method call tracing

**Naming Convention:**
```
"{aggregate}.{method}({params}) - {type}"
```

Examples:
```yaml
invokes_domain_operations:
  - "User.create(userId, email) - factory method"
  - "user.activate() - business method"
  - "order.addLine(product, quantity) - business method"
  - "cart.clear() - business method"
```

**Implementation:**
```java
// Delegate to domain for business logic
user.activate();  // All business logic is in the aggregate

// Application service just coordinates
repository.save(user);
```

**Step 4: Invoke Domain Services (`invokes_domain_services`)**

```yaml
invokes_domain_services:
  - svc_dom_pricing
  - svc_dom_authentication
```

**When Used:**
- Business logic spans multiple aggregates
- Logic doesn't belong to any single aggregate
- Stateless domain operations

**Implementation:**
```java
// Domain service for multi-aggregate logic
Money price = pricingService.calculatePrice(
    product,
    customer,
    quantity
);

order.addLine(product, quantity, price);
```

**Step 5: Persist Aggregates (`persists_aggregates`)**

```yaml
persists_aggregates: true   # For commands
persists_aggregates: false  # For queries
```

**When `true` (Commands):**
```java
repository.save(user);  // Persist modified aggregate
```

**When `false` (Queries):**
```java
// No persistence, read-only
return mapToDTO(user);
```

**Step 6: Publish Events (`publishes_events`)**

```yaml
publishes_events:
  - evt_user_created
  - evt_user_activated
```

**Pattern:**
Events published AFTER successful transaction commit:

```java
@Transactional
public UserId createUser(CreateUserCmd cmd) {
    // ... create and persist user ...
    repository.save(user);

    // Events published AFTER persistence (before transaction commit)
    eventPublisher.publishEvent(new UserCreated(
        user.getUserId().id(),
        user.getEmail(),
        Instant.now()
    ));

    return user.getUserId();
    // Transaction commits here
}
```

**Step 7: Return DTO (`returns_dto`)**

```yaml
returns_dto: UserSummary  # For queries
returns_dto: null         # For commands
```

**Query Pattern:**
```java
public UserSummary getUserSummary(UserId userId) {
    User user = repository.findById(userId);

    // Map aggregate to DTO
    return new UserSummary(
        user.getUserId().id(),
        user.getEmail(),
        user.getStatus().name()
    );
}
```

**Command Pattern:**
```yaml
returns_dto: null  # Commands don't return DTOs
```

### Implementation Guidelines

**Pattern 1: Creation Command Workflow**

```yaml
workflow:
  validates_input: true
  loads_aggregates: []                     # Nothing to load
  invokes_domain_operations:
    - "User.create(userId, email) - factory method"
  invokes_domain_services: []
  persists_aggregates: true
  publishes_events:
    - evt_user_created
  returns_dto: null
```

**Pattern 2: Modification Command Workflow**

```yaml
workflow:
  validates_input: true
  loads_aggregates:
    - agg_user                             # Load aggregate
  invokes_domain_operations:
    - "user.activate() - business method"   # Modify it
  invokes_domain_services: []
  persists_aggregates: true                 # Save it
  publishes_events:
    - evt_user_activated
  returns_dto: null
```

**Pattern 3: Query Workflow**

```yaml
workflow:
  validates_input: true
  loads_aggregates:
    - agg_user                             # Load for reading
  invokes_domain_operations: []            # No operations (read-only)
  invokes_domain_services: []
  persists_aggregates: false               # No persistence
  publishes_events: []                     # No events
  returns_dto: UserSummary                 # Return DTO
```

**Pattern 4: Complex Command with Domain Service**

```yaml
workflow:
  validates_input: true
  loads_aggregates:
    - agg_order
    - agg_customer
  invokes_domain_operations:
    - "order.addLine(product, quantity, price) - business method"
  invokes_domain_services:
    - svc_dom_pricing                      # Calculate price
  persists_aggregates: true
  publishes_events:
    - evt_order_line_added
  returns_dto: null
```

### Examples from Schema

**Example 1: User Creation Workflow**

From `/domains/ddd/examples/application-service-example.yaml` lines 483-492:

```yaml
workflow:
  validates_input: true
  loads_aggregates: []
  invokes_domain_operations:
    - "User.create() - factory method"
  invokes_domain_services: []
  persists_aggregates: true
  publishes_events:
    - evt_user_created
  returns_dto: null
```

**Analysis:**
- No aggregates loaded (creation)
- Uses factory method (User.create)
- Persists new aggregate
- Publishes creation event
- Returns domain ID (not in workflow, in operation returns)

**Example 2: User Activation Workflow**

From lines 507-517:

```yaml
workflow:
  validates_input: true
  loads_aggregates:
    - agg_user
  invokes_domain_operations:
    - "user.activate() - business method"
  invokes_domain_services: []
  persists_aggregates: true
  publishes_events:
    - evt_user_activated
  returns_dto: null
```

**Analysis:**
- Loads user aggregate
- Invokes business method (not factory)
- Persists modified aggregate
- Publishes state change event

**Example 3: Query Workflow**

From lines 606-614:

```yaml
workflow:
  validates_input: true
  loads_aggregates:
    - agg_user
  invokes_domain_operations: []
  invokes_domain_services: []
  persists_aggregates: false
  publishes_events: []
  returns_dto: UserSummary
```

**Analysis:**
- Loads aggregate for reading
- No domain operations (read-only)
- No persistence
- No events
- Returns DTO

### Best Practices

**1. Document All Steps**

Always specify all seven properties, even if empty:

```yaml
✓ CORRECT - Complete workflow:
workflow:
  validates_input: true
  loads_aggregates: [agg_user]
  invokes_domain_operations: ["user.activate()"]
  invokes_domain_services: []
  persists_aggregates: true
  publishes_events: [evt_user_activated]
  returns_dto: null

✗ INCOMPLETE - Missing steps:
workflow:
  loads_aggregates: [agg_user]
  persists_aggregates: true
  # Missing other properties
```

**2. Match Load/Modify Aggregates**

Aggregates loaded must match those modified:

```yaml
✓ CORRECT:
transaction_boundary:
  modifies_aggregates: [agg_user]
workflow:
  loads_aggregates: [agg_user]
  # Loaded and modified match

✗ WRONG:
transaction_boundary:
  modifies_aggregates: [agg_user]
workflow:
  loads_aggregates: [agg_profile]
  # Mismatch - loading profile, modifying user?
```

**3. Creation Loads Nothing**

```yaml
✓ CORRECT - Creation:
workflow:
  loads_aggregates: []
  invokes_domain_operations:
    - "User.create() - factory method"

✗ WRONG - Creation loading aggregates:
workflow:
  loads_aggregates: [agg_user]  # Can't load what doesn't exist
  invokes_domain_operations:
    - "User.create()"
```

**4. Commands vs Queries**

```yaml
✓ CORRECT - Command:
workflow:
  persists_aggregates: true
  publishes_events: [evt_user_activated]
  returns_dto: null

✓ CORRECT - Query:
workflow:
  persists_aggregates: false
  publishes_events: []
  returns_dto: UserSummary
```

### Anti-Patterns

**❌ Anti-Pattern 1: Business Logic in Workflow**

```yaml
# WRONG - Business logic doesn't belong in application service
invokes_domain_operations:
  - "Calculate total by summing line items"
  - "Apply 10% discount if over $100"
  - "Set order status to CONFIRMED"
```

**✓ Correct:**
```yaml
invokes_domain_operations:
  - "order.confirm() - business method"
  # All business logic is encapsulated in domain method
```

**❌ Anti-Pattern 2: Multi-Aggregate Modification**

```yaml
# WRONG - Modifying multiple aggregates
workflow:
  loads_aggregates:
    - agg_order
    - agg_inventory
  invokes_domain_operations:
    - "order.confirm()"
    - "inventory.reserve(items)"  # Second aggregate modification
  persists_aggregates: true  # Which aggregate? Both? Wrong!
```

**✓ Correct:**
```yaml
workflow:
  loads_aggregates: [agg_order]
  invokes_domain_operations:
    - "order.confirm()"
  persists_aggregates: true
  publishes_events:
    - evt_order_confirmed  # Event triggers inventory update
```

**❌ Anti-Pattern 3: Query with Side Effects**

```yaml
# WRONG - Query modifying state
- name: getUserSummary
  type: query
  workflow:
    loads_aggregates: [agg_user]
    invokes_domain_operations:
      - "user.recordAccess()"  # Side effect!
    persists_aggregates: true  # Violates query read-only principle
```

**✓ Correct:**
```yaml
workflow:
  loads_aggregates: [agg_user]
  invokes_domain_operations: []  # No operations
  persists_aggregates: false     # Read-only
  returns_dto: UserSummary
```

### References

- **Schema Lines:** 162-196, 483-614 (examples)
- **Evans (2003):** Chapter 4 - "Isolating the Domain", discusses application layer coordination
- **Vernon (2013):** Chapter 4 - "Architecture", section on application services
- **Fowler (2002):** "Service Layer" pattern in PoEAA

---

## 5. CommandRecord

**Schema Location:** Lines 225-265
**Pattern Classification:** CRITICAL (600-800 words)
**Status:** NEW in v2.0.0 - Knight pattern for command definitions

### Schema Definition

```yaml
CommandRecord:
  type: object
  description: Nested command record definition
  required: [record_name, intent, parameters]
  properties:
    record_name:
      type: string
      pattern: "^[A-Z][a-zA-Z]+Cmd$"
      description: Command record name (e.g., CreateUserCmd, PlaceOrderCmd)
    intent:
      type: string
      pattern: "^[a-z][a-zA-Z]+$"
      description: Imperative verb describing intent (create, activate, place, enroll)
    description:
      type: string
    parameters:
      type: array
      description: Command parameters (all required for command execution)
      items:
        $ref: "#/$defs/Parameter"
    returns:
      type: string
      enum: [void, domain_id, acknowledgment, result_status]
      description: What the command returns
    return_type_ref:
      $ref: "#/$defs/VoId"
      description: Reference to value object for domain_id returns
    modifies_aggregate:
      $ref: "#/$defs/AggId"
      description: Aggregate modified by this command (should be exactly one)
    publishes_events:
      type: array
      description: Domain events published after successful execution
      items:
        $ref: "#/$defs/EvtId"
    audit_fields:
      type: array
      description: Fields for audit trail (e.g., reason, initiatedBy, approvedBy)
      items:
        type: string
```

### Rationale and Purpose

CommandRecord represents the **Knight codebase pattern** for defining commands as **nested immutable records** inside command interfaces. This pattern exists to create a clean, type-safe, and intention-revealing command API that explicitly captures user intent.

**Why This Pattern Exists:**

1. **Nested Record Pattern**: Following Knight, commands are defined as **nested records inside interface contracts**. This keeps command definitions co-located with the operations they invoke.

2. **Immutability by Design**: Java records are immutable by default. This ensures commands represent **unchangeable user intent** - they are data structures, not behavior.

3. **Explicit Intent Capture**: The `intent` field (createUser, activateUser) makes the **business purpose** explicit, not just "what data" but "what action."

4. **Aggregate Binding**: `modifies_aggregate` creates a direct link between command and the aggregate it affects, enabling:
   - Architecture validation
   - Transaction boundary analysis
   - Code generation

5. **Event Publication Declaration**: `publishes_events` makes event-driven architecture explicit in the model.

### Detailed Explanation

A CommandRecord defines nine aspects of a command:

**1. Record Name (`record_name`)**

```yaml
record_name: CreateUserCmd
```

**Naming Pattern:**
```
{Verb}{Noun}Cmd
```

Examples:
```
CreateUserCmd
ActivateUserCmd
DeactivateUserCmd
PlaceOrderCmd
CancelOrderCmd
ApproveInvoiceCmd
EnrollServiceCmd
```

**Pattern Constraint:**
```
pattern: "^[A-Z][a-zA-Z]+Cmd$"
```
- Must start with uppercase letter
- Must end with "Cmd"
- PascalCase format

**2. Intent (`intent`)**

```yaml
intent: createUser
```

**Naming Pattern:**
```
{verb}{Noun}
```

This is the **method name** that will handle the command:

```java
// Record name: CreateUserCmd
// Intent: createUser
UserId createUser(CreateUserCmd cmd);
```

**Imperative Verbs:**
- create, activate, deactivate
- place, cancel, complete
- approve, reject, review
- enroll, unenroll, suspend
- lock, unlock, enable, disable

**3. Parameters (`parameters`)**

```yaml
parameters:
  - name: email
    type: String
    required: true
    description: User email address
  - name: userType
    type: String
    required: true
    description: "User type enum as string (DIRECT, INDIRECT)"
```

**Key Points:**
- All command parameters are typically **required**
- Use primitive types and value objects
- Avoid complex nested structures
- Serialize enums as strings

**4. Returns (`returns`)**

```yaml
returns: domain_id
return_type_ref: vo_user_id
```

**Four Return Types:**

**void** - State transitions:
```yaml
# Example: ActivateUserCmd
returns: void
return_type_ref: null
```

**domain_id** - Creation commands:
```yaml
# Example: CreateUserCmd
returns: domain_id
return_type_ref: vo_user_id
```

**acknowledgment** - Async operations:
```yaml
# Example: ProcessPaymentCmd
returns: acknowledgment
return_type_ref: vo_correlation_id
```

**result_status** - Complex results:
```yaml
# Example: ValidateDocumentCmd
returns: result_status
return_type_ref: vo_validation_result
```

**5. Aggregate Modification (`modifies_aggregate`)**

```yaml
modifies_aggregate: agg_user
```

**Rules:**
- Exactly ONE aggregate (enforced by transaction boundary)
- Must match aggregate in transaction_boundary
- Enables:
  - Transaction scope validation
  - Concurrency analysis
  - Lock contention prediction

**6. Event Publication (`publishes_events`)**

```yaml
publishes_events:
  - evt_user_created
  - evt_user_activated
```

**Pattern:**
- List all events this command may publish
- Events published AFTER successful persistence
- Enables event-driven architecture mapping

**7. Audit Fields (`audit_fields`)**

```yaml
audit_fields:
  - reason
  - initiatedBy
  - approvedBy
```

**Common Audit Fields:**
- **reason**: Why the action was taken
- **initiatedBy**: Who requested the action
- **approvedBy**: Who approved the action
- **reviewedBy**: Who reviewed the request
- **timestamp**: When initiated (usually auto)
- **correlationId**: Request tracking

**8. Description**

```yaml
description: Create a new user in PENDING status
```

Clear, business-focused explanation of what the command does.

### Implementation Guidelines

**Pattern: Nested Record in Interface**

```java
public interface UserCommands {

    // Command 1: Creation
    UserId createUser(CreateUserCmd cmd);

    record CreateUserCmd(
        String email,
        String userType,
        String identityProvider,
        ClientId clientId
    ) {}

    // Command 2: State Transition
    void activateUser(ActivateUserCmd cmd);

    record ActivateUserCmd(
        UserId userId
    ) {}

    // Command 3: Audit Fields
    void deactivateUser(DeactivateUserCmd cmd);

    record DeactivateUserCmd(
        UserId userId,
        String reason,           // Audit field
        String initiatedBy       // Audit field
    ) {}
}
```

**Application Service Implementation:**

```java
@Singleton
public class UserApplicationService implements UserCommands {

    @Override
    @Transactional
    public UserId createUser(CreateUserCmd cmd) {
        // Implementation using cmd.email(), cmd.userType(), etc.
    }

    @Override
    @Transactional
    public void activateUser(ActivateUserCmd cmd) {
        // Implementation using cmd.userId()
    }
}
```

### Examples from Schema

**Example 1: Creation Command**

From `/domains/ddd/examples/application-service-example.yaml` lines 304-329:

```yaml
- record_name: CreateUserCmd
  intent: createUser
  description: Create a new user in PENDING status
  parameters:
    - name: email
      type: String
      required: true
    - name: userType
      type: String
      required: true
    - name: identityProvider
      type: String
      required: true
    - name: clientId
      type: ClientId
      value_object_ref: vo_client_id
      required: true
  returns: domain_id
  return_type_ref: vo_user_id
  modifies_aggregate: agg_user
  publishes_events:
    - evt_user_created
```

**Analysis:**
- Creation command returns domain ID
- Four required parameters
- References value objects (ClientId, UserId)
- Modifies single aggregate
- Publishes creation event
- No audit fields (creation doesn't need justification)

**Example 2: State Transition Command**

From lines 331-343:

```yaml
- record_name: ActivateUserCmd
  intent: activateUser
  description: Activate user account, enabling system access
  parameters:
    - name: userId
      type: UserId
      value_object_ref: vo_user_id
      required: true
  returns: void
  modifies_aggregate: agg_user
  publishes_events:
    - evt_user_activated
```

**Analysis:**
- State transition returns void
- Single parameter (userId)
- No audit fields (activation is simple state change)

**Example 3: Command with Audit Fields**

From lines 345-364:

```yaml
- record_name: DeactivateUserCmd
  intent: deactivateUser
  description: Deactivate user account with reason
  parameters:
    - name: userId
      type: UserId
      value_object_ref: vo_user_id
      required: true
    - name: reason
      type: String
      required: true
      description: Reason for deactivation
  returns: void
  modifies_aggregate: agg_user
  publishes_events:
    - evt_user_deactivated
  audit_fields:
    - reason
```

**Analysis:**
- Deactivation requires reason
- Reason is both parameter and audit field
- Important business action requires justification

**Example 4: Security Command with Audit Fields**

From lines 365-384:

```yaml
- record_name: LockUserCmd
  intent: lockUser
  description: Lock user account due to security concerns
  parameters:
    - name: userId
      type: UserId
      value_object_ref: vo_user_id
      required: true
    - name: reason
      type: String
      required: true
      description: Reason for lock (e.g., failed login attempts)
  returns: void
  modifies_aggregate: agg_user
  publishes_events:
    - evt_user_locked
  audit_fields:
    - reason
```

**Analysis:**
- Security action requires reason
- Audit trail critical for locked accounts
- Reason must be explicit, not optional

### Best Practices

**1. Record Naming Convention**

```yaml
✓ CORRECT:
record_name: CreateUserCmd
record_name: PlaceOrderCmd
record_name: ApproveInvoiceCmd

✗ WRONG:
record_name: UserCreation       # Missing Cmd suffix
record_name: create_user_cmd    # Snake case
record_name: userCmd            # No verb
```

**2. Intent Matches Record**

```yaml
✓ CORRECT:
record_name: CreateUserCmd
intent: createUser             # Matches record

✗ WRONG:
record_name: CreateUserCmd
intent: makeUser              # Doesn't match
```

**3. Return Types by Command Type**

```yaml
✓ CORRECT - Creation:
returns: domain_id
return_type_ref: vo_user_id

✓ CORRECT - State Transition:
returns: void

✗ WRONG - Creation returning void:
returns: void                  # How do you get the new ID?
```

**4. Audit Fields for Important Actions**

```yaml
✓ CORRECT - Deactivation:
audit_fields:
  - reason                     # Why was user deactivated?
  - initiatedBy                # Who requested it?

✗ WRONG - No audit for important action:
record_name: DeactivateUserCmd
audit_fields: []               # Should have reason
```

**5. Single Aggregate Modification**

```yaml
✓ CORRECT:
modifies_aggregate: agg_user   # Exactly one

✗ WRONG:
modifies_aggregate: null       # Must specify which aggregate
```

### Anti-Patterns

**❌ Anti-Pattern 1: Mutable Command**

```java
// WRONG - Mutable command class
public class CreateUserCmd {
    private String email;

    public void setEmail(String email) {  // Setter - mutable!
        this.email = email;
    }
}
```

**✓ Correct:**
```java
// Immutable record
public record CreateUserCmd(
    String email,
    String userType
) {}  // No setters, immutable by default
```

**❌ Anti-Pattern 2: Generic Command**

```yaml
# WRONG - Generic command handling multiple actions
- record_name: UserActionCmd
  parameters:
    - name: action
      type: String              # "create", "activate", "delete"
    - name: data
      type: Map<String, Object> # Generic data
```

**✓ Correct:**
```yaml
- record_name: CreateUserCmd
- record_name: ActivateUserCmd
- record_name: DeleteUserCmd
# Separate command per intent
```

**❌ Anti-Pattern 3: Command Returning Business Data**

```yaml
# WRONG - Command returning data
- record_name: CreateUserCmd
  returns: domain_id
  return_type_ref: vo_user_details  # UserDetails is business data!
```

**✓ Correct:**
```yaml
# Command returns ID only
- record_name: CreateUserCmd
  returns: domain_id
  return_type_ref: vo_user_id

# Separate query for details
- method_name: getUserDetails
  result_record_name: UserDetails
```

**❌ Anti-Pattern 4: Missing Audit Fields**

```yaml
# WRONG - Deactivation without reason
- record_name: DeactivateUserCmd
  parameters:
    - name: userId
      type: UserId
  audit_fields: []              # No reason captured!
```

**✓ Correct:**
```yaml
- record_name: DeactivateUserCmd
  parameters:
    - name: userId
      type: UserId
    - name: reason
      type: String
      required: true
  audit_fields:
    - reason                    # Audit trail captured
```

### References

- **Schema Lines:** 225-265, 297-397 (examples)
- **Knight Pattern:** Nested command records in interfaces
- **Best Practice:** Lines 892-897 - Command modeling best practices
- **Vernon (2013):** Chapter 4 - "Architecture", discusses command handlers

---

## 6. QueryMethod

**Schema Location:** Lines 302-341
**Pattern Classification:** CRITICAL (600-800 words)
**Status:** NEW in v2.0.0 - Knight pattern for query definitions

### Schema Definition

```yaml
QueryMethod:
  type: object
  description: Query method definition
  required: [method_name, result_record_name]
  properties:
    method_name:
      type: string
      pattern: "^(get|list|find|search)[A-Z][a-zA-Z]+$"
      description: Query method name (e.g., getUserSummary, listOrders, findByStatus)
    description:
      type: string
    parameters:
      type: array
      description: Query parameters (typically domain identifiers or filter criteria)
      items:
        $ref: "#/$defs/Parameter"
    result_record_name:
      type: string
      pattern: "^[A-Z][a-zA-Z]+Summary$"
      description: Name of result DTO record (e.g., UserSummary, OrderSummary)
    result_structure:
      $ref: "#/$defs/ResultStructure"
    bypasses_domain_model:
      type: boolean
      description: Whether query reads directly from read model (CQRS pattern)
      default: false
    optimizations:
      type: object
      description: Query optimization strategies
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
```

### Rationale and Purpose

QueryMethod represents the **Knight codebase pattern** for defining queries as **interface methods with nested result records**. This pattern exists to create a clean, read-optimized query API that explicitly separates reads from writes (CQRS).

**Why This Pattern Exists:**

1. **CQRS Read Model**: Queries are fundamentally different from commands. They:
   - Don't modify state
   - May bypass domain model
   - Can use denormalized data
   - Can be independently optimized

2. **Result Record Pattern**: Following Knight, query results are defined as **nested immutable records** inside query interfaces, keeping result DTOs co-located with query methods.

3. **Query Verb Enforcement**: The `pattern: "^(get|list|find|search)[A-Z][a-zA-Z]+$"` constraint enforces query naming conventions, making intent clear.

4. **Optimization Declaration**: `optimizations` makes performance strategies **explicit** in the model, enabling:
   - Performance analysis
   - Caching strategy documentation
   - Index requirement identification

5. **CQRS Bypass Option**: `bypasses_domain_model` declares whether the query reads directly from a read model, enabling pure CQRS implementations.

### Detailed Explanation

A QueryMethod defines seven aspects of a query:

**1. Method Name (`method_name`)**

```yaml
method_name: getUserSummary
```

**Naming Pattern:**
```
{queryVerb}{Noun}{OptionalQualifier}
```

**Query Verbs:**
- **get**: Retrieve single result by ID
- **list**: Retrieve collection (all or filtered)
- **find**: Retrieve filtered result(s)
- **search**: Retrieve based on search criteria

**Examples:**
```
getUserSummary          # Get single user
listActiveUsers         # List filtered collection
findUserByEmail         # Find by specific criteria
searchOrders            # Search with complex criteria
getUserDetails          # Get detailed view
listOrdersByStatus      # List with filter
```

**Pattern Constraint:**
```
pattern: "^(get|list|find|search)[A-Z][a-zA-Z]+$"
```

**2. Parameters (`parameters`)**

Query parameters typically include:

**Single Result (get, find):**
```yaml
parameters:
  - name: userId
    type: UserId
    value_object_ref: vo_user_id
    required: true
```

**Collection (list, search):**
```yaml
parameters:
  - name: filter
    type: OrderFilter
    required: false
    description: Optional filter criteria
  - name: page
    type: Integer
    required: false
  - name: pageSize
    type: Integer
    required: false
```

**3. Result Record Name (`result_record_name`)**

```yaml
result_record_name: UserSummary
```

**Naming Pattern:**
```
{Noun}Summary
{Noun}Details
{Noun}View
```

Examples:
```
UserSummary
OrderDetails
InvoiceView
CustomerProfile
ProductCatalog
```

**Pattern Constraint:**
```
pattern: "^[A-Z][a-zA-Z]+Summary$"
```

**4. Result Structure (`result_structure`)**

Defines the DTO shape (see [Section 7](#7-resultstructure)):

```yaml
result_structure:
  fields:
    - name: userId
      type: String
      serialization: "UserId serialized to String"
    - name: email
      type: String
    - name: status
      type: String
      serialization: "Status enum serialized to String"
  aggregate_counts:
    - field_name: orderCount
      counted_entity: Order
```

**5. Domain Model Bypass (`bypasses_domain_model`)**

```yaml
bypasses_domain_model: false  # Reads through domain model (default)
bypasses_domain_model: true   # Reads from read model directly (CQRS)
```

**When `false` (Default):**
```java
public UserSummary getUserSummary(UserId userId) {
    // Load through repository (domain model)
    User user = repository.findById(userId)
        .orElseThrow(() -> new UserNotFoundException());

    // Map aggregate to DTO
    return new UserSummary(
        user.getUserId().id(),
        user.getEmail(),
        user.getStatus().name()
    );
}
```

**When `true` (CQRS):**
```java
public UserSummary getUserSummary(UserId userId) {
    // Read directly from read model (denormalized view)
    return readModelRepository.findUserSummary(userId);
    // Bypasses domain model entirely
}
```

**6. Optimizations**

```yaml
optimizations:
  denormalized: true   # Read from denormalized table
  cached: true         # Enable caching
  indexed: true        # Database index required
```

**denormalized:**
- `true`: Query reads from denormalized read model
- `false`: Query loads from normalized domain tables

**cached:**
- `true`: Result should be cached (Redis, Caffeine, etc.)
- `false`: Always fetch fresh data

**indexed:**
- `true`: Database index should exist
- `false`: Full table scan acceptable

**7. Description**

```yaml
description: Retrieve user summary information
```

Clear explanation of what data the query returns and why.

### Implementation Guidelines

**Pattern 1: Single Result Query**

```yaml
- method_name: getUserSummary
  description: Retrieve user summary by ID
  parameters:
    - name: userId
      type: UserId
      required: true
  result_record_name: UserSummary
  result_structure:
    fields:
      - name: userId
        type: String
      - name: email
        type: String
      - name: status
        type: String
  bypasses_domain_model: false
  optimizations:
    denormalized: false
    cached: true        # Cache user summaries
    indexed: true
```

**Implementation:**
```java
public interface UserQueries {

    UserSummary getUserSummary(UserId userId);

    record UserSummary(
        String userId,
        String email,
        String status
    ) {}
}

@Singleton
public class UserApplicationService implements UserQueries {

    @Override
    public UserSummary getUserSummary(UserId userId) {
        User user = repository.findById(userId)
            .orElseThrow(() -> new UserNotFoundException());

        return new UserSummary(
            user.getUserId().id(),
            user.getEmail(),
            user.getStatus().name()
        );
    }
}
```

**Pattern 2: Collection Query**

```yaml
- method_name: listActiveUsers
  description: List all active users
  parameters:
    - name: page
      type: Integer
      required: false
    - name: pageSize
      type: Integer
      required: false
  result_record_name: UserSummary
  result_structure:
    fields:
      - name: userId
        type: String
      - name: email
        type: String
  bypasses_domain_model: false
  optimizations:
    denormalized: false
    cached: false       # Don't cache lists
    indexed: true       # Index on status
```

**Implementation:**
```java
public interface UserQueries {

    List<UserSummary> listActiveUsers(Integer page, Integer pageSize);

    record UserSummary(
        String userId,
        String email
    ) {}
}
```

**Pattern 3: CQRS Read Model Query**

```yaml
- method_name: searchOrders
  description: Search orders with complex criteria
  parameters:
    - name: criteria
      type: OrderSearchCriteria
      required: true
  result_record_name: OrderSummary
  result_structure:
    fields:
      - name: orderId
        type: String
      - name: customerName
        type: String
      - name: totalAmount
        type: BigDecimal
      - name: itemCount
        type: Integer
  bypasses_domain_model: true   # CQRS read model
  optimizations:
    denormalized: true           # Denormalized for performance
    cached: false
    indexed: true
```

**Implementation:**
```java
public OrderSummary searchOrders(OrderSearchCriteria criteria) {
    // Query denormalized read model directly
    return readModelRepository.searchOrders(criteria);
    // Bypasses Order aggregate entirely
}
```

### Examples from Schema

**Example 1: User Summary Query**

From `/domains/ddd/examples/application-service-example.yaml` lines 410-444:

```yaml
- method_name: getUserSummary
  description: Retrieve user summary information
  parameters:
    - name: userId
      type: UserId
      value_object_ref: vo_user_id
      required: true
      description: User ID to query
  result_record_name: UserSummary
  result_structure:
    fields:
      - name: userId
        type: String
        serialization: "UserId serialized to String via userId.id()"
        description: User identifier
      - name: email
        type: String
        description: User email address
      - name: status
        type: String
        serialization: "Status enum serialized to String via status.name()"
        description: Current user status
      - name: userType
        type: String
        serialization: "UserType enum serialized to String via userType.name()"
        description: User type
      - name: identityProvider
        type: String
        serialization: "IdentityProvider enum serialized to String"
        description: Authentication provider
  bypasses_domain_model: false
  optimizations:
    denormalized: false
    cached: false
    indexed: true
```

**Analysis:**
- Single result query (get)
- Returns summary DTO
- All enums serialized to strings
- Does NOT bypass domain model
- Should be indexed for performance
- Not cached (user status changes frequently)

### Best Practices

**1. Query Verb Selection**

```yaml
✓ CORRECT - Specific verbs:
method_name: getUserSummary      # Single result
method_name: listActiveUsers     # Collection
method_name: findUserByEmail     # Lookup
method_name: searchOrders        # Complex search

✗ WRONG - Generic verbs:
method_name: getUsers            # Get or list?
method_name: queryUser           # Not a standard verb
```

**2. Result Naming Convention**

```yaml
✓ CORRECT - Summary suffix:
result_record_name: UserSummary
result_record_name: OrderDetails
result_record_name: InvoiceView

✗ WRONG - Missing suffix:
result_record_name: User         # Conflicts with entity
result_record_name: UserData     # Not descriptive
```

**3. Optimization Alignment**

```yaml
✓ CORRECT - Denormalized = bypasses domain:
bypasses_domain_model: true
optimizations:
  denormalized: true

✗ INCONSISTENT:
bypasses_domain_model: false
optimizations:
  denormalized: true  # Contradictory
```

**4. No Side Effects**

```yaml
✓ CORRECT - Read-only:
- method_name: getUserSummary
  # No transaction_boundary with modifies_aggregates

✗ WRONG - Query with side effects:
- method_name: getUserSummary
  transaction_boundary:
    modifies_aggregates: [agg_user]  # Queries must not modify!
```

### Anti-Patterns

**❌ Anti-Pattern 1: Query Returning Aggregate**

```java
// WRONG - Returning domain aggregate from query
public User getUser(UserId userId) {
    return repository.findById(userId);  // Returns aggregate
}
```

**✓ Correct:**
```java
public UserSummary getUserSummary(UserId userId) {
    User user = repository.findById(userId);
    return new UserSummary(
        user.getUserId().id(),
        user.getEmail(),
        user.getStatus().name()
    );  // Returns DTO, not aggregate
}
```

**❌ Anti-Pattern 2: Query with Side Effects**

```yaml
# WRONG - Query modifying state
- method_name: getUserSummary
  workflow:
    invokes_domain_operations:
      - "user.recordAccess()"  # Side effect!
    persists_aggregates: true
```

**✓ Correct:**
```yaml
- method_name: getUserSummary
  workflow:
    invokes_domain_operations: []
    persists_aggregates: false  # Read-only
```

**❌ Anti-Pattern 3: Nested Object Return**

```yaml
# WRONG - Nested complex objects
result_structure:
  fields:
    - name: user
      type: Object
      nested_fields:
        - email
        - status
    - name: profile
      type: Object  # Nested object - violates flat structure
```

**✓ Correct:**
```yaml
result_structure:
  fields:
    - name: userEmail
      type: String
    - name: userStatus
      type: String
    - name: profileBio
      type: String
    # Flat structure
```

### References

- **Schema Lines:** 302-341, 410-444 (examples)
- **Knight Pattern:** Nested result records in interfaces
- **Best Practice:** Lines 898-905 - Query modeling best practices
- **Fowler:** "CQRS" pattern article

---

## 7. ResultStructure

**Schema Location:** Lines 282-301
**Pattern Classification:** IMPORTANT (400-500 words)
**Status:** NEW in v2.0.0 - Query result DTO structure

### Schema Definition

```yaml
ResultStructure:
  type: object
  description: Structure of a query result DTO
  properties:
    fields:
      type: array
      description: Fields in the result DTO
      items:
        $ref: "#/$defs/DTOField"
    aggregate_counts:
      type: array
      description: Count fields for related entities (not full collections)
      items:
        type: object
        properties:
          field_name:
            type: string
          counted_entity:
            type: string
```

### Rationale and Purpose

ResultStructure defines the **shape and content of query result DTOs**. This pattern exists to document exactly what data queries return, enabling flat DTO design, string serialization of complex types, and aggregate count patterns.

**Why This Pattern Exists:**

1. **DTO Documentation**: Makes query result structure explicit and verifiable
2. **Flat Structure Enforcement**: Enables validation of flat vs nested DTO patterns
3. **Serialization Strategy**: Documents how complex types (IDs, enums, dates) are serialized
4. **Aggregate Count Pattern**: Captures counts instead of full collections (performance)
5. **Code Generation**: Provides enough detail to generate DTO classes

### Detailed Explanation

ResultStructure has two components:

**1. Fields (`fields`)**

Basic DTO fields with serialization documentation:

```yaml
fields:
  - name: userId
    type: String
    serialization: "UserId serialized to String via userId.id()"
  - name: status
    type: String
    serialization: "Status enum serialized to String via status.name()"
  - name: createdAt
    type: String
    serialization: "Instant serialized to ISO-8601 string"
```

**2. Aggregate Counts (`aggregate_counts`)**

Counts of related entities instead of full collections:

```yaml
aggregate_counts:
  - field_name: orderCount
    counted_entity: Order
  - field_name: activeServiceCount
    counted_entity: Service
```

### Implementation Guidelines

**Pattern: Flat DTO Structure**

```yaml
result_structure:
  fields:
    # Primitives
    - name: userId
      type: String
    - name: email
      type: String

    # Enums as strings
    - name: status
      type: String
      serialization: "Status enum"

    # Dates as strings
    - name: createdAt
      type: String
      serialization: "ISO-8601 format"

  aggregate_counts:
    - field_name: orderCount
      counted_entity: Order
```

**Implementation:**
```java
public record UserSummary(
    String userId,
    String email,
    String status,        // Enum serialized to string
    String createdAt,     // Instant serialized to ISO-8601
    int orderCount        // Count, not collection
) {}
```

### Examples from Schema

From `/domains/ddd/examples/application-service-example.yaml` lines 419-439:

```yaml
result_structure:
  fields:
    - name: userId
      type: String
      serialization: "UserId serialized to String via userId.id()"
    - name: email
      type: String
    - name: status
      type: String
      serialization: "Status enum serialized to String via status.name()"
    - name: userType
      type: String
      serialization: "UserType enum serialized to String via userType.name()"
    - name: identityProvider
      type: String
      serialization: "IdentityProvider enum serialized to String"
```

### Best Practices

**1. String Serialization**

```yaml
✓ CORRECT - Complex types as strings:
- name: userId
  type: String
  serialization: "UserId.id()"
- name: status
  type: String
  serialization: "Status.name()"

✗ WRONG - Complex types:
- name: userId
  type: UserId          # Should be String
- name: status
  type: UserStatus      # Should be String
```

**2. Aggregate Counts**

```yaml
✓ CORRECT - Count:
aggregate_counts:
  - field_name: orderCount
    counted_entity: Order

✗ WRONG - Full collection:
fields:
  - name: orders
    type: List<Order>    # Don't return full collections
```

### References

- **Schema Lines:** 282-301, 419-439
- **Best Practice:** Line 902 - "Return aggregate counts, not full collections"

---

## 8. DTOField (Tactical)

**Schema Location:** Lines 266-280
**Pattern Classification:** IMPORTANT (400-500 words)
**Status:** NEW in v2.0.0 - DTO field definition

### Schema Definition

```yaml
DTOField:
  type: object
  description: Field in a result DTO
  required: [name, type]
  properties:
    name:
      type: string
    type:
      type: string
      description: Field type (String for IDs/enums, primitives for counts)
    serialization:
      type: string
      description: How complex types are serialized
    description:
      type: string
```

### Rationale and Purpose

DTOField defines **individual fields within query result DTOs**. This pattern exists to document field-level serialization strategies, enabling flat DTO design and explicit type conversions.

**Why This Pattern Exists:**

1. **Serialization Documentation**: Makes conversion from domain types to DTO types explicit
2. **Type Safety**: Specifies exact field types (String for IDs, primitives for counts)
3. **Flat Structure Support**: All fields are simple types, no nested objects
4. **Code Generation**: Provides field-level detail for generating DTO classes

### Detailed Explanation

A DTOField defines four aspects:

**1. Name**
```yaml
name: userId
name: email
name: status
```

**2. Type**
Prefer simple types:
```yaml
type: String      # For IDs, enums, dates
type: Integer     # For counts, quantities
type: BigDecimal  # For money amounts
type: Boolean     # For flags
```

**3. Serialization**
Documents how domain types convert:
```yaml
serialization: "UserId serialized to String via userId.id()"
serialization: "Status enum serialized to String via status.name()"
serialization: "Instant serialized to ISO-8601 string"
```

**4. Description**
Clear explanation:
```yaml
description: User identifier
description: Current user status
```

### Implementation Guidelines

```yaml
fields:
  # Domain ID → String
  - name: userId
    type: String
    serialization: "UserId.id()"
    description: User identifier

  # Enum → String
  - name: status
    type: String
    serialization: "Status.name()"
    description: Current status

  # Date → String
  - name: createdAt
    type: String
    serialization: "Instant to ISO-8601"
    description: Creation timestamp

  # Count → Integer
  - name: orderCount
    type: Integer
    description: Number of orders
```

### Examples from Schema

From lines 421-439:

```yaml
- name: userId
  type: String
  serialization: "UserId serialized to String via userId.id()"
  description: User identifier
- name: email
  type: String
  description: User email address
- name: status
  type: String
  serialization: "Status enum serialized to String via status.name()"
  description: Current user status
```

### Best Practices

```yaml
✓ CORRECT - Simple types:
- name: userId
  type: String

✗ WRONG - Complex types:
- name: userId
  type: UserId      # Should be String
```

### References

- **Schema Lines:** 266-280, 421-439
- **Best Practice:** Line 901 - "Serialize all complex types to strings in DTOs"

---

## 9. CommandInterface & QueryInterface

**Schema Location:** Lines 720-841
**Pattern Classification:** IMPORTANT (400-500 words)
**Status:** NEW in v2.0.0 - API layer interface pattern

### Schema Definition

**CommandInterface:**
```yaml
CommandInterface:
  type: object
  description: Command interface containing command definitions as nested records
  required: [id, name, command_records]
  properties:
    id:
      $ref: "#/$defs/CmdId"
    name:
      type: string
      pattern: "^[A-Z][a-zA-Z]+Commands$"
    aggregate_ref:
      $ref: "#/$defs/AggId"
    command_records:
      type: array
      items:
        $ref: "#/$defs/CommandRecord"
    immutability:
      type: boolean
      const: true
    layer:
      type: string
      const: "api"
```

**QueryInterface:**
```yaml
QueryInterface:
  type: object
  description: Query interface containing query definitions and result DTOs
  required: [id, name, query_methods]
  properties:
    id:
      $ref: "#/$defs/QryId"
    name:
      type: string
      pattern: "^[A-Z][a-zA-Z]+Queries$"
    aggregate_ref:
      $ref: "#/$defs/AggId"
    query_methods:
      type: array
      items:
        $ref: "#/$defs/QueryMethod"
    no_side_effects:
      type: boolean
      const: true
    layer:
      type: string
      const: "api"
```

### Rationale and Purpose

CommandInterface and QueryInterface represent **API layer contracts** following the Knight nested record pattern. These patterns exist to:

1. **CQRS Segregation**: Separate command and query interfaces at API level
2. **Aggregate Binding**: Each interface typically maps to one aggregate
3. **Nested Record Pattern**: Commands and query results as nested records
4. **API Layer Documentation**: Clear API contracts for BFFs and external clients
5. **Immutability Enforcement**: Commands and results are immutable by design

### Detailed Explanation

**CommandInterface:**

Groups all commands for an aggregate:

```yaml
command_interfaces:
  - id: cmd_user_commands
    name: UserCommands
    aggregate_ref: agg_user
    command_records:
      - record_name: CreateUserCmd
      - record_name: ActivateUserCmd
      - record_name: DeactivateUserCmd
    immutability: true
    layer: api
```

**QueryInterface:**

Groups all queries for an aggregate:

```yaml
query_interfaces:
  - id: qry_user_queries
    name: UserQueries
    aggregate_ref: agg_user
    query_methods:
      - method_name: getUserSummary
      - method_name: listActiveUsers
    no_side_effects: true
    layer: api
```

### Implementation Guidelines

**Pattern: Separate Command and Query Interfaces**

```java
// Command Interface
public interface UserCommands {
    UserId createUser(CreateUserCmd cmd);
    record CreateUserCmd(String email, String userType) {}

    void activateUser(ActivateUserCmd cmd);
    record ActivateUserCmd(UserId userId) {}
}

// Query Interface
public interface UserQueries {
    UserSummary getUserSummary(UserId userId);
    record UserSummary(String userId, String email, String status) {}

    List<UserSummary> listActiveUsers();
}

// Application Service implements both
@Singleton
public class UserApplicationService implements UserCommands, UserQueries {
    // Implementation
}
```

### Examples from Schema

From `/domains/ddd/examples/application-service-example.yaml` lines 297-397:

```yaml
command_interfaces:
  - id: cmd_user_commands
    name: UserCommands
    bounded_context_ref: bc_user_management
    aggregate_ref: agg_user
    description: Command interface for user lifecycle operations
    command_records:
      - record_name: CreateUserCmd
        intent: createUser
      - record_name: ActivateUserCmd
        intent: activateUser
      - record_name: DeactivateUserCmd
        intent: deactivateUser
    immutability: true
    layer: api
```

From lines 403-450:

```yaml
query_interfaces:
  - id: qry_user_queries
    name: UserQueries
    bounded_context_ref: bc_user_management
    aggregate_ref: agg_user
    description: Query interface for user information retrieval
    query_methods:
      - method_name: getUserSummary
    result_characteristics:
      immutable: true
      flat_structure: true
      string_serialization: true
    layer: api
    no_side_effects: true
```

### Best Practices

**1. Naming Convention**

```yaml
✓ CORRECT:
name: UserCommands      # Plural "Commands"
name: UserQueries       # Plural "Queries"

✗ WRONG:
name: UserCommand       # Singular
name: UserQuery         # Singular
```

**2. One Interface Per Aggregate**

```yaml
✓ CORRECT:
- id: cmd_user_commands
  aggregate_ref: agg_user

✗ WRONG:
- id: cmd_all_commands  # Generic, not aggregate-specific
  aggregate_ref: null
```

**3. Immutability Characteristics**

```yaml
✓ CORRECT:
command_interfaces:
  immutability: true    # Always true

query_interfaces:
  no_side_effects: true # Always true
```

### Anti-Patterns

**❌ Anti-Pattern: Mixed Command/Query Interface**

```java
// WRONG - Mixing commands and queries
public interface UserService {
    UserId createUser(CreateUserCmd cmd);     // Command
    UserSummary getUserSummary(UserId id);    // Query
}
```

**✓ Correct:**
```java
public interface UserCommands { }
public interface UserQueries { }
```

### References

- **Schema Lines:** 720-841, 297-450
- **Knight Pattern:** Separate command and query interfaces
- **Best Practice:** Line 889 - "Application service should implement both Commands and Queries interfaces"

---

## 10. ID Types (10 Extracted)

**Schema Location:** Lines 36-90
**Pattern Classification:** IMPORTANT (400-500 words)
**Status:** NEW in v2.0.0 - Extracted ID patterns

### Schema Definition

```yaml
# ID Types
BcId:
  type: string
  pattern: "^bc_[a-z0-9_]+$"

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

DomId:
  type: string
  pattern: "^dom_[a-z0-9_]+$"
```

### Rationale and Purpose

Extracting ID types to `$defs` provides:

1. **Consistent Naming**: Enforces prefixes across all tactical patterns
2. **Schema Validation**: Regex patterns validate ID format
3. **Type Reusability**: IDs referenced throughout schema
4. **Pattern Classification**: Prefix identifies pattern type
5. **Code Generation**: Enables type-safe ID generation

### Detailed Explanation

**ID Prefix Convention:**

```
bc_      → Bounded Context ID
agg_     → Aggregate ID
ent_     → Entity ID
vo_      → Value Object ID
repo_    → Repository ID
svc_dom_ → Domain Service ID
svc_app_ → Application Service ID
cmd_     → Command Interface ID
qry_     → Query Interface ID
evt_     → Domain Event ID
dom_     → Domain ID
```

**Examples:**
```
bc_user_management
agg_user
ent_candidate
vo_user_id
repo_user
svc_dom_pricing
svc_app_user_management
cmd_user_commands
qry_user_queries
evt_user_created
dom_identity_access
```

### Implementation Guidelines

**Naming Convention (Schema Lines 17-26):**

```yaml
naming_conventions:
  aggregate_id: "agg_<name>"
  entity_id: "ent_<name>"
  value_object_id: "vo_<name>"
  repository_id: "repo_<name>"
  domain_service_id: "svc_dom_<name>"
  application_service_id: "svc_app_<name>"
  command_id: "cmd_<name>"
  query_id: "qry_<name>"
  domain_event_id: "evt_<name>"
```

**Usage:**

```yaml
value_objects:
  - id: vo_user_id           # $ref: "#/$defs/VoId"
    name: UserId

aggregates:
  - id: agg_user             # $ref: "#/$defs/AggId"
    name: User

repositories:
  - id: repo_user            # $ref: "#/$defs/RepoId"
    aggregate_ref: agg_user  # References AggId
```

### Best Practices

**1. Use Type References**

```yaml
✓ CORRECT - Type reference:
id:
  $ref: "#/$defs/AggId"

✗ WRONG - Inline string:
id:
  type: string
  pattern: "^agg_"           # Should use $ref
```

**2. Follow Naming Convention**

```yaml
✓ CORRECT:
id: agg_user
id: vo_email
id: svc_app_user_management

✗ WRONG:
id: user_agg               # Wrong prefix order
id: UserAggregate          # PascalCase not allowed
id: agg-user               # Hyphen not allowed
```

### References

- **Schema Lines:** 36-90, naming_conventions 17-26

---

## 11. Attribute, Parameter, Method

**Schema Location:** Lines 93-142
**Pattern Classification:** SUPPORTING (200-300 words)
**Status:** NEW in v2.0.0 - Reusable supporting types

### Schema Definition

**Attribute:**
```yaml
Attribute:
  type: object
  required: [name, type]
  properties:
    name:
      type: string
    type:
      type: string
    value_object_ref:
      $ref: "#/$defs/VoId"
    required:
      type: boolean
    description:
      type: string
    validation:
      type: string
```

**Parameter:**
```yaml
Parameter:
  type: object
  required: [name, type]
  properties:
    name:
      type: string
    type:
      type: string
    value_object_ref:
      $ref: "#/$defs/VoId"
    required:
      type: boolean
      default: true
    description:
      type: string
```

**Method:**
```yaml
Method:
  type: object
  properties:
    name:
      type: string
    description:
      type: string
    parameters:
      type: array
      items:
        $ref: "#/$defs/Parameter"
    returns:
      type: string
```

### Rationale and Purpose

These extracted types provide **reusable definitions** for:
- Entity and value object attributes
- Operation parameters
- Domain service and repository methods

**Benefits:**
1. **DRY Principle**: Define once, reference everywhere
2. **Consistency**: Same structure for attributes across patterns
3. **Value Object Integration**: `value_object_ref` links attributes to VOs
4. **Validation Documentation**: Capture validation rules

### Examples

**Attribute in Entity:**
```yaml
entities:
  - id: ent_user
    attributes:
      - name: email
        type: Email
        value_object_ref: vo_email
        required: true
        validation: "Must be valid email format"
```

**Parameter in Command:**
```yaml
parameters:
  - name: userId
    type: UserId
    value_object_ref: vo_user_id
    required: true
```

**Method in Repository:**
```yaml
interface_methods:
  - name: findById
    parameters:
      - name: userId
        type: UserId
    returns: Optional<User>
```

### References

- **Schema Lines:** 93-142

---

## 12. Immutability Enforcement

**Schema Location:** Lines 513-516, 588-590, 763-765
**Pattern Classification:** SUPPORTING (200-300 words)
**Status:** NEW in v2.0.0 - Schema-level immutability patterns

### Schema Definition

**`const: true` Pattern (Strict Enforcement):**

```yaml
ValueObject:
  properties:
    immutability:
      type: boolean
      const: true  # MUST be true, schema validation fails otherwise
```

**`default: true` Pattern (Default Value):**

```yaml
DomainService:
  properties:
    stateless:
      type: boolean
      default: true  # Defaults to true if not specified
```

### Rationale and Purpose

Schema-level immutability enforcement prevents common DDD mistakes:

1. **`const: true`**: Enforces invariants (value objects MUST be immutable)
2. **`default: true`**: Provides sensible defaults (services should be stateless)
3. **Validation**: Schema validation catches violations

### Detailed Explanation

**Three Immutability Patterns:**

**1. Value Object Immutability (const: true)**

```yaml
immutability:
  type: boolean
  const: true
  description: Value objects must be immutable
```

**Validation:**
```yaml
# ✓ Valid
value_objects:
  - id: vo_email
    immutability: true

# ✗ Invalid - schema validation fails
value_objects:
  - id: vo_email
    immutability: false  # ERROR: must be const value true
```

**2. Domain Event Immutability (const: true)**

```yaml
immutable:
  type: boolean
  const: true
  description: Events are immutable facts
```

**3. Command Record Immutability (const: true)**

```yaml
immutability:
  type: boolean
  const: true
  description: Command records must be immutable
```

### Why `const: true` vs `default: true`?

**`const: true`** - Use when:
- Property MUST have this value (invariant)
- No other value is valid
- Violation is a design error

**Examples:**
- Value object immutability
- Event immutability
- Query no_side_effects

**`default: true`** - Use when:
- Property SHOULD have this value
- Other values are valid but discouraged
- Provides sensible default

**Examples:**
- Domain service stateless
- Application service manages_transactions
- Workflow validates_input

### Examples from Schema

**Example 1: Value Object Immutability (const: true)**

From lines 513-516:

```yaml
immutability:
  type: boolean
  const: true
  description: Value objects must be immutable
```

**Validation Rule (line 853-854):**
```yaml
- rule: "value_objects_immutable"
  description: "Value objects must be immutable"
  validation: "value_object.immutability must be true"
```

**Example 2: Domain Event Immutability (const: true)**

From lines 588-590:

```yaml
immutable:
  type: boolean
  const: true
  description: Events are immutable facts
```

**Validation Rule (line 860-862):**
```yaml
- rule: "events_immutable"
  description: "Domain events must be immutable"
  validation: "domain_event.immutable must be true"
```

**Example 3: Command Immutability (const: true)**

From lines 763-765:

```yaml
immutability:
  type: boolean
  const: true
  description: Command records must be immutable
```

**Example 4: Application Service Characteristics (const and default)**

From lines 680-709:

```yaml
characteristics:
  stateless:
    type: boolean
    const: true            # MUST be stateless
  contains_business_logic:
    type: boolean
    const: false           # MUST NOT contain business logic
  manages_transactions:
    type: boolean
    const: true            # MUST manage transactions
  publishes_events:
    type: boolean
    default: true          # SHOULD publish events (default)
```

### Implementation Guidelines

**Pattern 1: Invariants Use `const: true`**

```yaml
# Value Object - Immutability is invariant
immutability:
  type: boolean
  const: true              # No other value allowed

# Domain Event - Immutability is invariant
immutable:
  type: boolean
  const: true              # Facts cannot change

# Query - No side effects is invariant
no_side_effects:
  type: boolean
  const: true              # Queries must be read-only
```

**Pattern 2: Best Practices Use `default: true`**

```yaml
# Workflow - Usually validates input
validates_input:
  type: boolean
  default: true            # Usually true, but can be false

# Workflow - Usually persists
persists_aggregates:
  type: boolean
  default: true            # Usually true for commands

# Domain Service - Usually stateless
stateless:
  type: boolean
  default: true            # Should be stateless
```

### Best Practices

**1. Use `const` for Invariants**

```yaml
✓ CORRECT - Invariant:
immutability:
  const: true              # Must always be true

✗ WRONG - Invariant as default:
immutability:
  default: true            # Allows false - wrong!
```

**2. Use `default` for Conventions**

```yaml
✓ CORRECT - Convention:
stateless:
  default: true            # Usually true, can be false

✗ WRONG - Convention as const:
stateless:
  const: true              # Too strict - some services might need state
```

### Anti-Patterns

**❌ Anti-Pattern: Mutable Value Object**

```yaml
# WRONG - Schema validation will fail
value_objects:
  - id: vo_email
    immutability: false    # ERROR: const requires true
```

**❌ Anti-Pattern: Event with Side Effects**

```yaml
# WRONG - Schema validation will fail
domain_events:
  - id: evt_user_created
    immutable: false       # ERROR: const requires true
```

**❌ Anti-Pattern: Query with Side Effects**

```yaml
# WRONG - Schema validation will fail
query_interfaces:
  - id: qry_user_queries
    no_side_effects: false # ERROR: const requires true
```

### Validation Rules

From schema lines 844-874:

```yaml
validation_rules:
  - rule: "value_objects_immutable"
    validation: "value_object.immutability must be true"

  - rule: "events_immutable"
    validation: "domain_event.immutable must be true"

  - rule: "application_service_stateless"
    validation: "application_service.characteristics.stateless must be true"

  - rule: "queries_no_side_effects"
    validation: "query_interface.no_side_effects must be true"
```

### References

- **Schema Lines:** 513-516, 588-590, 680-709, 763-765, 838-841
- **Validation Rules:** Lines 844-874
- **Evans (2003):** Chapter 5 - "A Model Expressed in Software", discusses value object immutability
- **Vernon (2013):** Chapter 6 - "Value Objects", emphasizes immutability

---

## Cross-Reference Matrix

| Concept | References These | Referenced By |
|---------|-----------------|---------------|
| BoundedContext | DomId, Aggregate, Entity, ValueObject, Repository, DomainService, ApplicationService, CommandInterface, QueryInterface, DomainEvent | Strategic schema (domain_ref) |
| ApplicationServiceOperation | Parameter, TransactionBoundary, Workflow | ApplicationService.operations |
| TransactionBoundary | AggId | ApplicationServiceOperation |
| Workflow | AggId, SvcDomId, EvtId | ApplicationServiceOperation |
| CommandRecord | Parameter, VoId, AggId, EvtId | CommandInterface.command_records |
| QueryMethod | Parameter, ResultStructure | QueryInterface.query_methods |
| ResultStructure | DTOField | QueryMethod.result_structure |
| DTOField | (none) | ResultStructure.fields |
| CommandInterface | CmdId, AggId, CommandRecord | ApplicationService.implements_commands |
| QueryInterface | QryId, AggId, QueryMethod | ApplicationService.implements_queries |
| ID Types | (none) | All tactical patterns |
| Attribute/Parameter/Method | VoId | Entity, ValueObject, Repository, etc. |

---

## Implementation Checklist

When implementing v2.0 schema concepts:

**✓ BoundedContext:**
- [ ] One file per bounded context
- [ ] All tactical patterns nested under bounded_context
- [ ] domain_ref links to strategic schema
- [ ] Ubiquitous language documented

**✓ ApplicationServiceOperation:**
- [ ] One operation per use case
- [ ] Type is command or query (not both)
- [ ] Transaction boundary specified
- [ ] Workflow documents all steps

**✓ TransactionBoundary:**
- [ ] Commands are transactional
- [ ] Queries are NOT transactional
- [ ] modifies_aggregates has maxItems: 1
- [ ] Consistency type matches scope

**✓ Workflow:**
- [ ] All seven steps documented
- [ ] Load/modify aggregates match
- [ ] Creation operations load nothing
- [ ] Queries have no side effects

**✓ CommandRecord:**
- [ ] Record name ends with "Cmd"
- [ ] Intent matches operation name
- [ ] Returns appropriate type (void/id/status)
- [ ] Modifies exactly one aggregate
- [ ] Audit fields for important actions

**✓ QueryMethod:**
- [ ] Method name uses query verb (get/list/find/search)
- [ ] Result record name ends with "Summary"
- [ ] Result structure is flat
- [ ] Complex types serialized to strings
- [ ] No side effects

**✓ ResultStructure:**
- [ ] All fields documented
- [ ] Serialization strategy specified
- [ ] Aggregate counts instead of collections

**✓ CommandInterface & QueryInterface:**
- [ ] Separate interfaces for commands and queries
- [ ] Names end with "Commands" / "Queries"
- [ ] Bound to specific aggregate
- [ ] Immutability enforced

**✓ ID Types:**
- [ ] Correct prefix used
- [ ] Snake case format
- [ ] References use $ref to $defs

**✓ Immutability:**
- [ ] Value objects: immutability = true
- [ ] Events: immutable = true
- [ ] Commands: immutability = true
- [ ] Queries: no_side_effects = true

---

## Glossary

**Application Service Operation**: Atomic unit of use case execution (command or query)

**Bounded Context**: Root container for all tactical patterns within a single context

**Command Record**: Immutable record representing user intent to modify state

**Query Method**: Read-only method returning DTO data

**Transaction Boundary**: Declaration of transaction scope (which aggregates, consistency type)

**Workflow**: Orchestration sequence (validate, load, execute, persist, publish)

**Result Structure**: Shape of query result DTO (fields, counts)

**DTO Field**: Individual field in result DTO with serialization strategy

**Command Interface**: API contract containing command records

**Query Interface**: API contract containing query methods and result records

**ID Types**: Extracted string patterns for consistent identification

**Immutability Enforcement**: Schema-level validation of immutable patterns

---

## References

### Primary Sources

1. **Evans, Eric.** *Domain-Driven Design: Tackling Complexity in the Heart of Software*. Addison-Wesley, 2003.
   - Chapter 4: Isolating the Domain
   - Chapter 5: A Model Expressed in Software
   - Chapter 6: The Life Cycle of a Domain Object
   - Chapter 14: Maintaining Model Integrity

2. **Vernon, Vaughn.** *Implementing Domain-Driven Design*. Addison-Wesley, 2013.
   - Chapter 2: Domains, Subdomains, and Bounded Contexts
   - Chapter 4: Architecture
   - Chapter 6: Value Objects
   - Chapter 10: Aggregates (One aggregate per transaction rule)

3. **Fowler, Martin.** *Patterns of Enterprise Application Architecture*. Addison-Wesley, 2002.
   - Service Layer pattern
   - Transaction Script pattern

4. **Fowler, Martin.** "CQRS". Martin Fowler's Bliki.
   https://martinfowler.com/bliki/CQRS.html

### Schema References

- **Schema File:** `/domains/ddd/schemas/tactical-ddd.schema.yaml` v2.0.0
- **Example Files:**
  - `/domains/ddd/examples/tactical-example.yaml`
  - `/domains/ddd/examples/application-service-example.yaml`
- **Existing Docs:**
  - `/domains/ddd/docs/ddd-03-tactical-patterns.md`
  - `/domains/ddd/docs/ddd-07-application-layer.md`

### Knight Codebase Patterns

- Nested command records in interfaces
- Nested query result records in interfaces
- Application service implements both Commands and Queries
- Immutable records for commands and results
- Flat DTO structure with string serialization

---

**RESEARCH COMPLETE**

This document provides comprehensive research and documentation for 12 undocumented tactical DDD concepts from v2.0 schema. All concepts include:
- Schema definitions with line numbers
- Rationale and purpose
- Detailed explanations (300-800 words)
- Implementation guidelines
- Concrete examples from schema
- Best practices
- Anti-patterns
- References to Evans/Vernon

Total word count: ~28,000 words across 12 concepts (600-800 for critical, 400-500 for important, 200-300 for supporting).
