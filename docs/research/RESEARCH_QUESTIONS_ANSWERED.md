# DDD Enhancement: Research Questions Answered

**Version**: 1.1.0
**Date**: 2025-10-18
**Status**: Complete
**Related Enhancement**: Application Services, CQRS, and BFF Pattern

---

## Overview

This document provides definitive answers to 10 critical research questions that emerged during the DDD domain model enhancement. These answers are now codified in the schema definitions and validated through concrete examples.

---

## Research Questions and Answers

### 1. Application Service Granularity

**Question**: Should we have one ApplicationService per BoundedContext or one per Aggregate?

**Answer**: **One ApplicationService per BoundedContext (or bounded context area)**

**Rationale**:
- Application services implement multiple command and query interfaces
- A single application service can orchestrate operations across multiple aggregates within the same bounded context
- The Knight codebase example shows `UserApplicationService` implementing both `UserCommands` and `UserQueries` for all user-related operations
- Granularity at aggregate level would create unnecessary proliferation of services

**Schema Evidence**:
```yaml
application_service:
  bounded_context_ref: bc_user_management  # One service per context
  implements_commands: [cmd_user_commands]  # Multiple commands
  implements_queries: [qry_user_queries]    # Multiple queries
```

**Validation**: See `/domains/ddd/examples/application-service-example.yaml` lines 456-633

---

### 2. CQRS Separation Strategy

**Question**: Should CQRS be implemented as separate interfaces or separate services?

**Answer**: **Separate interfaces, single service implementation (Knight pattern)**

**Rationale**:
- Commands and queries are defined as separate interfaces (`UserCommands`, `UserQueries`)
- A single application service implements both interfaces
- This maintains CQRS benefits (separate read/write models) while avoiding service proliferation
- Allows independent evolution of command and query interfaces
- Knight codebase demonstrates this pattern consistently

**Schema Evidence**:
```yaml
command_interface:
  id: cmd_user_commands
  name: UserCommands
  command_records: [...]  # Nested command record types

query_interface:
  id: qry_user_queries
  name: UserQueries
  query_methods: [...]  # Interface methods with result records

application_service:
  implements_commands: [cmd_user_commands]
  implements_queries: [qry_user_queries]  # Single service, both interfaces
```

**Validation**: See `/domains/ddd/schemas/tactical-ddd.schema.yaml` lines 312-906

---

### 3. BFF Scope Determination

**Question**: Should BFF scope be per UI platform, per bounded context, or per workflow?

**Answer**: **One BFF per client type (UI platform): "One experience, one BFF"**

**Rationale**:
- BFF aggregates data from MULTIPLE bounded contexts for a single client type
- Scope is determined by client characteristics (web, mobile iOS, mobile Android, partner API)
- BFF is owned by the frontend team (Conway's Law)
- Each BFF provides client-specific orchestration, not workflow-specific or context-specific

**Schema Evidence**:
```yaml
bff_scope:
  id: bff_web
  client_type: web  # Exactly one client type
  aggregates_from_contexts:
    - bc_user_management
    - bc_order_management
    - bc_product_catalog  # Multiple contexts
  owned_by_team: Web Frontend Team
```

**Validation**: See `/domains/ddd/examples/bff-example.yaml` lines 9-97

---

### 4. BFF vs API Gateway Distinction

**Question**: How do BFF and API Gateway responsibilities differ?

**Answer**: **API Gateway handles cross-cutting concerns; BFF handles client-specific orchestration**

**Hybrid pattern**: API Gateway upstream + Multiple BFFs downstream

**Separation of Concerns**:

**API Gateway (Upstream)**:
- Authentication/Authorization (OAuth2, JWT)
- Rate limiting
- SSL termination
- Request/response logging
- CORS headers
- API key validation

**BFF (Downstream)**:
- Data aggregation from multiple contexts
- Format transformation for client needs
- Client-specific field selection
- Presentation logic (labels, formatting)
- Client-optimized payloads

**Schema Evidence**:
```yaml
bff_scope:
  upstream_dependencies: [api_gateway]  # API Gateway sits upstream
  responsibilities:
    data_aggregation: true
    client_specific_orchestration: true
    presentation_logic: true
  anti_patterns:
    generic_cross_cutting_concerns: false  # Not BFF responsibility
```

**Validation**: See `/domains/ddd/examples/bff-example.yaml` lines 631-651

---

### 5. OpenAPI Integration Strategy

**Question**: Where and how should OpenAPI specifications be integrated?

**Answer**: **BFF layer exposes OpenAPI specs; Commands/Queries define contracts**

**Strategy**:
- BFF interfaces define REST API endpoints with request/response DTOs
- Commands and queries define domain contracts as nested records
- OpenAPI spec generated from BFF interface definitions
- Separation: BFF DTOs ≠ Command records (translation layer)

**Schema Evidence**:
```yaml
bff_interface:
  endpoints:
    - path: /create
      method: POST
      request_dto: CreateUserRequest   # BFF DTO
      response_dto: CreateUserResult
      delegates_to_commands: [cmd_user_commands]  # Domain command interface

command_interface:
  command_records:
    - record_name: CreateUserCmd  # Domain command record (not directly exposed)
```

**Validation**: See `/domains/ddd/examples/bff-example.yaml` lines 110-141

---

### 6. Transaction Boundaries

**Question**: Should transactions span a single aggregate or multiple aggregates?

**Answer**: **Single aggregate per transaction (Vaughn Vernon rule)**

**Rationale**:
- Strong consistency within aggregate boundary
- Eventual consistency across aggregate boundaries
- Commands modify at most ONE aggregate per transaction
- Multi-aggregate operations use saga pattern or domain events

**Schema Evidence**:
```yaml
command_interface:
  command_records:
    - modifies_aggregate: agg_user  # Exactly one aggregate

application_service:
  operations:
    - transaction_boundary:
        modifies_aggregates: [agg_user]  # maxItems: 1
        consistency_type: transactional
```

**Validation**: See `/domains/ddd/schemas/tactical-ddd.schema.yaml` lines 930-936

---

### 7. UX Grounding Path

**Question**: Must UX components always ground through BFF, or can they access ApplicationService directly for read-only operations?

**Answer**: **Strict via BFF for all operations (read and write)**

**Rationale**:
- Maintains consistent client-specific orchestration
- BFF provides single point for client optimizations
- Prevents bypassing presentation logic
- Read-only operations still benefit from aggregation and formatting

**Complete Chain**:
```
UX:Component → BFF:Interface → ApplicationService → Command/Query → Aggregate
```

**Schema Evidence**:
```yaml
component:
  api_endpoints: [bff_if_user_web]  # Always via BFF

bff_interface:
  delegates_to_services: [svc_app_user_management]
```

**Validation**: See grounding chain in `/grounding-relationships.yaml` lines 381-426

---

### 8. Command/Query as First-Class Concepts

**Question**: Should Commands and Queries be first-class schema concepts or just properties of ApplicationService?

**Answer**: **First-class concepts with dedicated interfaces (Knight pattern)**

**Rationale**:
- Commands are nested record types in command interfaces (API layer)
- Queries are interface methods with nested result records (API layer)
- Application services implement these interfaces (Application layer)
- Clear separation of contract (interface) from implementation (service)
- Enables independent evolution and testing

**Schema Evidence**:
```yaml
$defs:
  command_interface:
    type: object
    layer: api  # First-class concept at API layer

  query_interface:
    type: object
    layer: api  # First-class concept at API layer

  application_service:
    implements_commands: [cmd_*]  # References to command interfaces
    implements_queries: [qry_*]   # References to query interfaces
    layer: application  # Implementation layer
```

**Validation**: See `/domains/ddd/schemas/tactical-ddd.schema.yaml` lines 556-906

---

### 9. BFF Schema Location

**Question**: Should BFF definitions be in strategic schema or a separate integration partition?

**Answer**: **Strategic schema (strategic-ddd.schema.yaml)**

**Rationale**:
- BFF scope is a strategic concern (client type, multi-context aggregation)
- BFF interface is infrastructure implementation (can be in separate partition)
- Current implementation: Both in strategic schema for simplicity
- BFF aggregates across bounded contexts (strategic concern)

**Schema Evidence**:
```yaml
# strategic-ddd.schema.yaml
$defs:
  bff_scope:
    architecture_layer: integration
    aggregates_from_contexts: [multiple]  # Strategic multi-context concern

  bff_interface:
    layer: infrastructure  # Implementation detail
```

**Validation**: See `/domains/ddd/schemas/strategic-ddd.schema.yaml` lines 230-707

---

### 10. Application Service Transaction Coordination

**Question**: How should ApplicationService coordinate transactions across multiple operations?

**Answer**: **Application service manages transaction boundaries; one transaction per command**

**Transaction Management**:
- Application service starts transaction at operation boundary
- Loads aggregate(s) from repository
- Invokes domain operations (which enforce invariants)
- Persists aggregate(s) back to repository
- Publishes events AFTER successful commit
- Uses outbox pattern for reliable event publishing

**Workflow Pattern**:
```
1. Start transaction (@Transactional)
2. Load aggregate(s) via repository
3. Invoke domain operation (aggregate.method())
4. Persist aggregate via repository.save()
5. Publish events (in-memory or outbox)
6. Commit transaction
```

**Schema Evidence**:
```yaml
application_service:
  characteristics:
    manages_transactions: true  # Const: true

  operations:
    - workflow:
        validates_input: true
        loads_aggregates: [agg_user]
        invokes_domain_operations: ["user.activate()"]
        persists_aggregates: true
        publishes_events: [evt_user_activated]  # After commit
```

**Validation**: See `/domains/ddd/examples/application-service-example.yaml` lines 469-591

---

## Summary of Decisions

| Question | Decision | Schema Location |
|----------|----------|-----------------|
| 1. ApplicationService granularity | One per BoundedContext | tactical-ddd.schema.yaml:312-633 |
| 2. CQRS separation | Separate interfaces, single service | tactical-ddd.schema.yaml:556-906 |
| 3. BFF scope | One per client type | strategic-ddd.schema.yaml:230-481 |
| 4. BFF vs API Gateway | Hybrid: Gateway upstream, BFF downstream | bff-example.yaml:631-651 |
| 5. OpenAPI integration | BFF layer with DTO translation | bff-example.yaml:110-295 |
| 6. Transaction boundaries | Single aggregate per transaction | tactical-ddd.schema.yaml:930-936 |
| 7. UX grounding path | Strict via BFF for all operations | grounding-relationships.yaml:870-889 |
| 8. Command/Query concepts | First-class interfaces (API layer) | tactical-ddd.schema.yaml:556-906 |
| 9. BFF schema location | Strategic schema | strategic-ddd.schema.yaml:230-707 |
| 10. Transaction coordination | ApplicationService manages boundaries | application-service-example.yaml:469-633 |

---

## Validation Status

All decisions have been:
- ✓ Codified in schema definitions (tactical-ddd.schema.yaml v1.1.0, strategic-ddd.schema.yaml v1.1.0)
- ✓ Validated through concrete examples (application-service-example.yaml, bff-example.yaml)
- ✓ Cross-referenced in grounding relationships (grounding-relationships.yaml, interdomain-map.yaml v2.3.0)
- ✓ Aligned with Knight codebase patterns

---

## References

1. `/domains/ddd/schemas/tactical-ddd.schema.yaml` v1.1.0
2. `/domains/ddd/schemas/strategic-ddd.schema.yaml` v1.1.0
3. `/domains/ddd/examples/application-service-example.yaml`
4. `/domains/ddd/examples/bff-example.yaml`
5. `/grounding-relationships.yaml` v2.3.0
6. `/research-output/interdomain-map.yaml` v2.3.0
7. Knight Codebase Reference Implementation

---

## Next Steps

These decisions are now locked into the canonical grounding framework. Future enhancements should:
1. Maintain consistency with these decisions
2. Update schemas using semantic versioning
3. Create migration guides for breaking changes
4. Validate new patterns against these foundations
