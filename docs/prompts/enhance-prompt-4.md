# DDD Schema Enhancement Prompt 4: Application Services, CQRS, and BFF Pattern

## Objective

Research and extend the DDD canonical domain model to include:
1. **Application Service** pattern with Command/Query separation (CQRS)
2. **Backend for Frontend (BFF)** pattern as the integration layer between UX and domain
3. **BFF Interface** specification (REST/HTTP resources and operations)
4. Updated **UX-to-DDD grounding** that routes through BFF layer

This enhancement addresses the architectural gap where UX currently references DDD bounded contexts and aggregates directly, rather than through a well-defined integration boundary.

## Research Methodology

Follow the canonical grounding research methodology established in previous phases:

### Phase 1: Literature Research (Sources in Priority Order)

1. **BFF Pattern** (Primary - Start Here)
   - Sam Newman - "Building Microservices" (BFF pattern chapter)
   - ThoughtWorks articles on BFF pattern
   - Phil Calçado - "The Back-end for Front-end Pattern (BFF)" (original article)
   - Microservices.io - BFF pattern documentation
   - Key questions:
     * What is the scope of a BFF (single UI vs multiple bounded contexts)?
     * How does BFF aggregate data from multiple bounded contexts?
     * What are the key responsibilities of BFF vs application services?

2. **Martin Fowler - Patterns of Enterprise Application Architecture (PoEAA)**
   - Application Service / Service Layer pattern
   - Command/Query separation principles
   - https://martinfowler.com/eaaCatalog/serviceLayer.html
   - Key questions:
     * What operations belong in application services vs domain services?
     * How do application services coordinate transactions?
     * What is the relationship between service layer and domain model?

3. **Eric Evans - Domain-Driven Design (2003)**
   - Chapter on Application Layer
   - Relationship between application services and aggregates
   - Transaction boundaries and use cases
   - Key questions:
     * Where do application services fit in layered architecture?
     * How do application services differ from domain services?
     * What is the granularity of application service operations?

4. **Vaughn Vernon - Implementing Domain-Driven Design (2013)**
   - Application Services chapter
   - CQRS pattern implementation
   - Application service orchestration of aggregates
   - Repository coordination
   - Key questions:
     * How do application services handle command validation?
     * How do queries differ from commands in application services?
     * What events should application services publish?

5. **REST/OpenAPI Patterns** (Supporting)
   - RESTful Web Services best practices
   - OpenAPI 3.0 specification structure
   - Resource modeling and HTTP verb semantics
   - Key questions:
     * How do REST resources map to domain aggregates?
     * What is the relationship between HTTP operations and commands/queries?

### Phase 2: Knight Codebase Analysis

Analyze the existing implementation in `/Users/igor/code/knight/contexts` to identify:

#### 2.1 Command/Query Pattern Discovery
- **Commands**: Search for `*Command*.java`, `*Commands.java` files
- **Queries**: Search for `*Query*.java`, `*Queries.java` files
- **Application Services**: Search for `*ApplicationService.java` files

Example files found:
- `/Users/igor/code/knight/contexts/users/users/api/commands/UserCommands.java`
- `/Users/igor/code/knight/contexts/users/users/app/service/UserApplicationService.java`

Extract patterns:
1. Command structure (record types with parameters)
2. Query structure (return types, filtering)
3. Application service orchestration (transaction boundaries, event publishing)
4. Relationship to aggregates and repositories

#### 2.2 BFF Pattern Discovery
- Search for REST controllers: `*Controller.java`, `*Resource.java`
- Search for API specifications: `*.yaml`, `*.yml` (OpenAPI/Swagger)
- Search for DTO/model mappings between domain and API layers

Example files found:
- `/Users/igor/code/knight/contexts/users/users/infra/rest/UserCommandController.java`

Extract patterns:
1. How controllers expose bounded context functionality
2. HTTP verb mapping to commands/queries
3. JSON schema/DTO structure
4. Multi-context aggregation (if any BFF examples exist)
5. Error handling and validation at integration boundary

#### 2.3 Integration Patterns
- Identify if Knight has examples of:
  * Single BFF serving multiple bounded contexts
  * Separate API layer per bounded context
  * Shared kernel for API models
  * Event-driven integration between contexts

### Phase 3: Concept Definition

Based on research and Knight analysis, define the following concepts:

#### 3.1 Application Service (Tactical DDD Schema)
```yaml
application_service:
  type: object
  description: Orchestrates use cases by coordinating aggregates, repositories, and domain services
  required: [id, name, bounded_context_ref]
  properties:
    id:
      pattern: "^svc_app_[a-z0-9_]+$"
    name:
      type: string
    bounded_context_ref:
      pattern: "^bc_[a-z0-9_]+$"
    commands:
      type: array
      description: Write operations (mutate state)
      items:
        # Command schema TBD based on research
    queries:
      type: array
      description: Read operations (no side effects)
      items:
        # Query schema TBD based on research
    transaction_boundary:
      type: string
      enum: [single_aggregate, multi_aggregate, saga]
    publishes_events:
      type: array
      pattern: "^evt_[a-z0-9_]+$"
```

#### 3.2 Command (Tactical DDD Schema - New Concept)
```yaml
command:
  type: object
  description: Write operation that changes system state
  required: [id, name, application_service_ref]
  properties:
    id:
      pattern: "^cmd_[a-z0-9_]+$"
    name:
      type: string
      description: "Command name (imperative verb form, e.g., CreateUser, PlaceOrder)"
    application_service_ref:
      pattern: "^svc_app_[a-z0-9_]+$"
    target_aggregate_refs:
      type: array
      description: "Aggregates this command operates on"
      items:
        pattern: "^agg_[a-z0-9_]+$"
    parameters:
      type: array
      description: "Command input parameters"
    return_type:
      type: string
      description: "What the command returns (often aggregate ID or void)"
    validation_rules:
      type: array
      description: "Pre-conditions that must be met"
    idempotent:
      type: boolean
      description: "Can command be safely retried?"
```

#### 3.3 Query (Tactical DDD Schema - New Concept)
```yaml
query:
  type: object
  description: Read operation with no side effects
  required: [id, name, application_service_ref]
  properties:
    id:
      pattern: "^qry_[a-z0-9_]+$"
    name:
      type: string
      description: "Query name (e.g., FindUserById, ListActiveOrders)"
    application_service_ref:
      pattern: "^svc_app_[a-z0-9_]+$"
    source_aggregate_refs:
      type: array
      description: "Aggregates queried"
      items:
        pattern: "^agg_[a-z0-9_]+$"
    parameters:
      type: array
      description: "Query filters/criteria"
    return_type:
      type: string
      description: "What the query returns (DTO, projection, aggregate)"
    pagination:
      type: boolean
      description: "Does this query support pagination?"
    read_model:
      type: string
      description: "Optional: CQRS read model name if different from aggregate"
```

#### 3.4 BFF Scope (Strategic DDD Schema or New Schema)
```yaml
bff_scope:
  type: object
  description: Backend for Frontend aggregation layer serving specific UI needs
  required: [id, name, target_ui_platform]
  properties:
    id:
      pattern: "^bff_[a-z0-9_]+$"
    name:
      type: string
      description: "BFF name (e.g., WebAppBFF, MobileAppBFF)"
    target_ui_platform:
      type: string
      enum: [web, mobile_ios, mobile_android, desktop, multi_platform]
      description: "Which UI platform this BFF serves"
    bounded_context_refs:
      type: array
      description: "Bounded contexts this BFF aggregates"
      items:
        pattern: "^bc_[a-z0-9_]+$"
    application_service_refs:
      type: array
      description: "Application services exposed through this BFF"
      items:
        pattern: "^svc_app_[a-z0-9_]+$"
    aggregation_strategy:
      type: string
      enum: [single_context, multi_context_composition, api_gateway]
      description: "How this BFF aggregates backend services"
    api_specification_ref:
      type: string
      description: "Reference to OpenAPI YAML file (external)"
```

#### 3.5 BFF Interface (Strategic DDD Schema or New Schema)
```yaml
bff_interface:
  type: object
  description: REST/HTTP interface definition within a BFF
  required: [id, name, bff_scope_ref, resource_path, http_method]
  properties:
    id:
      pattern: "^bff_if_[a-z0-9_]+$"
    name:
      type: string
      description: "Interface operation name"
    bff_scope_ref:
      pattern: "^bff_[a-z0-9_]+$"
      description: "Parent BFF scope"
    resource_path:
      type: string
      description: "REST resource path (e.g., /api/users/{id})"
    http_method:
      type: string
      enum: [GET, POST, PUT, PATCH, DELETE]
    command_ref:
      pattern: "^cmd_[a-z0-9_]+$"
      description: "Command this interface invokes (for POST/PUT/PATCH/DELETE)"
    query_ref:
      pattern: "^qry_[a-z0-9_]+$"
      description: "Query this interface invokes (for GET)"
    request_schema:
      type: object
      description: "JSON schema of request body (simplified, full spec in OpenAPI)"
    response_schema:
      type: object
      description: "JSON schema of response body (simplified, full spec in OpenAPI)"
    openapi_operation_id:
      type: string
      description: "Reference to OpenAPI operationId for full specification"
```

### Phase 4: Grounding Relationship Updates

#### 4.1 New Grounding: UX → BFF
```yaml
- id: "grounding_ux_bff_001"
  source: "model_ux_interaction"
  target: "model_ddd"  # or model_bff if BFF is separate domain
  type: "structural"
  strength: "strong"
  description: "UX components invoke BFF interfaces instead of direct domain access"
  relationships:
    - source_concept: "ux:Component"
      target_concept: "bff:bff_interface"
      cardinality: "many-to-many"
      reference_field: "api_endpoints"
      validation: "recommended"
  rationale: "BFF provides stable integration boundary between UX and domain"
  examples:
    - "UserProfileComponent → GET /api/users/{id} (bff_if_get_user)"
    - "CheckoutComponent → POST /api/orders (bff_if_create_order)"
```

#### 4.2 New Grounding: BFF → Application Service
```yaml
- id: "grounding_bff_app_svc_001"
  source: "model_ddd"  # or model_bff
  target: "model_ddd"
  type: "structural"
  strength: "strong"
  description: "BFF interfaces delegate to application services"
  relationships:
    - source_concept: "bff:bff_interface"
      target_concept: "ddd:application_service"
      cardinality: "many-to-one"
      reference_field: "application_service_ref"
      validation: "required"
  rationale: "BFF is thin layer; business logic remains in application services"
  constraint: "BFF should not contain domain logic, only orchestration and DTO mapping"
```

#### 4.3 Updated Grounding: Application Service → Aggregate
```yaml
- id: "grounding_app_svc_agg_001"
  source: "model_ddd"
  target: "model_ddd"
  type: "structural"
  strength: "strong"
  description: "Application service commands operate on aggregates"
  relationships:
    - source_concept: "ddd:command"
      target_concept: "ddd:aggregate"
      cardinality: "many-to-many"
      reference_field: "target_aggregate_refs"
      validation: "required"
  rationale: "Commands encapsulate aggregate mutations as transactions"
```

#### 4.4 Revised UX → DDD Grounding (via BFF)
Update existing `grounding_ux_ddd_001` and `grounding_ux_ddd_002`:
- Change from direct UX→DDD to UX→BFF→ApplicationService→Aggregate path
- Document the full chain: `ux:Page → bff:bff_interface → ddd:application_service → ddd:command → ddd:aggregate`

### Phase 5: Documentation Updates

Update the following DDD documentation files in `/Users/igor/code/canonical-grounding/domains/ddd/docs/`:

#### 5.1 Create `ddd-07-application-layer.md`
Document:
- Application service responsibilities (use case orchestration)
- Command/Query separation (CQRS principles)
- Transaction management
- Event publishing
- Difference from domain services
- Examples from Knight codebase

#### 5.2 Create `ddd-08-bff-pattern.md`
Document:
- BFF scope and purpose
- When to use BFF (web vs mobile vs multi-platform)
- BFF vs API Gateway differences
- BFF interface design (REST resources)
- Integration with application services
- OpenAPI specification role
- Examples from Knight codebase (if available)

#### 5.3 Update `ddd-03-tactical-patterns.md`
Add sections:
- Application Services (reference ddd-07)
- Commands and Queries
- Integration with existing tactical patterns (aggregates, repositories)

#### 5.4 Update `ddd-02-strategic-patterns.md`
Add sections:
- BFF as integration pattern
- BFF scope in multi-bounded-context systems
- Context mapping through BFF layer

### Phase 6: Schema Implementation

#### 6.1 Update Tactical DDD Schema
File: `/Users/igor/code/canonical-grounding/domains/ddd/schemas/tactical-ddd.schema.yaml`

Add to `$defs`:
- `command` (as defined in Phase 3.2)
- `query` (as defined in Phase 3.3)

Update `application_service`:
- Add `commands` array referencing command IDs
- Add `queries` array referencing query IDs
- Add `transaction_boundary` field
- Add `publishes_events` array

Update `naming_conventions`:
```yaml
command_id: "cmd_<name>"
query_id: "qry_<name>"
bff_scope_id: "bff_<name>"
bff_interface_id: "bff_if_<name>"
```

#### 6.2 Decide on BFF Schema Location
Research should determine:

**Option A**: Add BFF to Strategic DDD Schema
- `bff_scope` and `bff_interface` go in `strategic-ddd.schema.yaml`
- Rationale: BFF is about context integration (strategic concern)

**Option B**: Create Integration DDD Partition
- New file: `domains/ddd/schemas/integration-ddd.schema.yaml`
- Contains: `bff_scope`, `bff_interface`, `api_gateway`, `context_translation`
- Rationale: Separation of integration patterns from core DDD

**Option C**: Create Separate BFF Canonical Domain
- New domain: `domains/bff/`
- Rationale: BFF is architectural pattern, not pure DDD
- **Recommendation**: Only if BFF scope expands beyond DDD integration

#### 6.3 Update Grounding Map
File: `/Users/igor/code/canonical-grounding/research-output/interdomain-map.yaml`

Add groundings as defined in Phase 4.1-4.4

### Phase 7: Examples

Create comprehensive examples in `/Users/igor/code/canonical-grounding/domains/ddd/examples/`:

#### 7.1 Update Tactical Example
File: `tactical-ddd-example.yaml` (or create partitioned examples)

Add:
- Application service example (e.g., `UserApplicationService`)
- 3-5 command examples (e.g., `CreateUser`, `ActivateUser`, `DeactivateUser`)
- 2-3 query examples (e.g., `FindUserById`, `ListActiveUsers`)
- Show relationship to existing aggregates (`User`)

Based on Knight codebase pattern:
```yaml
application_service:
  id: svc_app_user_management
  name: UserApplicationService
  bounded_context_ref: bc_user_management
  commands:
    - cmd_create_user
    - cmd_activate_user
    - cmd_deactivate_user
  queries:
    - qry_find_user_by_id
    - qry_list_active_users
  transaction_boundary: single_aggregate
  publishes_events:
    - evt_user_created
    - evt_user_activated

command:
  id: cmd_create_user
  name: CreateUser
  application_service_ref: svc_app_user_management
  target_aggregate_refs:
    - agg_user
  parameters:
    - name: email
      type: string
      validation: "email format"
    - name: userType
      type: enum
      values: [admin, regular]
  return_type: UserId
  idempotent: true
```

#### 7.2 Create BFF Example
File: `bff-example.yaml` (location TBD based on 6.2 decision)

Example: Web application BFF serving user management
```yaml
bff_scope:
  id: bff_web_app
  name: WebApplicationBFF
  target_ui_platform: web
  bounded_context_refs:
    - bc_user_management
    - bc_order_management
  application_service_refs:
    - svc_app_user_management
    - svc_app_order_management
  aggregation_strategy: multi_context_composition
  api_specification_ref: "specs/web-api.openapi.yaml"

bff_interface:
  id: bff_if_create_user
  name: CreateUserEndpoint
  bff_scope_ref: bff_web_app
  resource_path: "/api/users"
  http_method: POST
  command_ref: cmd_create_user
  request_schema:
    type: object
    properties:
      email: {type: string}
      userType: {type: string}
  response_schema:
    type: object
    properties:
      userId: {type: string}
      createdAt: {type: string, format: date-time}
  openapi_operation_id: "createUser"
```

### Phase 8: Validation

Run validation to ensure:
1. All new concepts are syntactically valid (JSON Schema 2020-12)
2. Cross-references resolve correctly:
   - `command.target_aggregate_refs` → existing aggregates
   - `bff_interface.command_ref` → defined commands
   - `application_service.bounded_context_ref` → strategic schema
3. Grounding relationships are bidirectional and complete
4. Closure percentage increases (target: maintain >95%)

Use existing validation script:
```bash
source venv/bin/activate
python tools/validate_multifile_schema.py
```

### Phase 9: Closure Analysis

Calculate closure impact:

**Before Enhancement**:
- DDD domain: 100% closure (9 concepts fully grounded)
- UX domain: 100% closure (17 concepts)
- Total groundings: 32

**After Enhancement**:
- DDD domain: Add 4 new concepts (application_service, command, query, bff_scope/bff_interface)
- Expected new groundings: +6 (UX→BFF, BFF→AppSvc, AppSvc→Aggregate, etc.)
- Target closure: Maintain 100% for DDD, increase system integration completeness

Document in closure report how BFF layer improves architectural clarity.

### Phase 10: Research Questions to Answer

The research must definitively answer:

1. **Granularity**: Should application services be coarse-grained (one per bounded context) or fine-grained (one per aggregate)?

2. **CQRS Separation**: Should commands and queries be:
   - Separate interfaces implemented by same service? (Knight pattern)
   - Separate services entirely? (full CQRS)
   - Modeled as first-class concepts or just as properties of application_service?

3. **BFF Scope**: What determines BFF boundaries?
   - One BFF per UI platform (web, mobile)?
   - One BFF per bounded context?
   - One BFF per user journey/workflow?

4. **BFF vs API Gateway**: Clear distinction needed:
   - BFF: UI-specific aggregation, can contain presentation logic
   - API Gateway: Generic routing/auth, no business logic
   - When to use which?

5. **OpenAPI Integration**: Should we:
   - Just reference external OpenAPI files?
   - Import OpenAPI and validate against schema?
   - Generate OpenAPI from schema?

6. **Transaction Boundaries**: How do application services handle:
   - Single aggregate updates (simple)
   - Multi-aggregate transactions (sagas, eventual consistency)
   - Cross-context operations (through BFF)

7. **UX Grounding Path**: Is the path:
   - `ux:Component → bff:interface → ddd:command → ddd:aggregate` (strict)
   - OR can UX still directly reference domain concepts for read-only views?

### Phase 11: Deliverables

1. **Research Documents** (in `domains/ddd/docs/`):
   - `ddd-07-application-layer.md` (6-10 pages)
   - `ddd-08-bff-pattern.md` (6-10 pages)
   - Updates to `ddd-03-tactical-patterns.md` and `ddd-02-strategic-patterns.md`

2. **Schema Updates**:
   - `domains/ddd/schemas/tactical-ddd.schema.yaml` (add application_service, command, query)
   - Strategic schema or new integration schema (add bff_scope, bff_interface)

3. **Examples**:
   - `domains/ddd/examples/application-service-example.yaml`
   - `domains/ddd/examples/bff-example.yaml` (or in appropriate location)
   - Update existing tactical example with commands/queries

4. **Grounding Updates**:
   - `research-output/interdomain-map.yaml` (add 6+ new groundings)
   - Updated grounding visualization (if graph is regenerated)

5. **Validation Report**:
   - Schema validation: ✓ All schemas valid
   - Closure analysis: DDD 100%, System >95%
   - Grounding validation: ✓ All references resolve
   - Status: PRODUCTION READY ✓

6. **Knight Codebase Analysis**:
   - Document of patterns found in `/Users/igor/code/knight/contexts`
   - Mapping between Knight implementation and schema concepts
   - Examples extracted from actual code

## Success Criteria

- [ ] All 10 research questions answered with citations
- [ ] 4 new DDD concepts defined with complete JSON Schema 2020-12 definitions
- [ ] 6+ new grounding relationships documented in interdomain-map.yaml
- [ ] 2 comprehensive examples based on Knight codebase patterns
- [ ] Documentation updated (2 new files, 2 updated files)
- [ ] Schemas validate without errors
- [ ] Closure percentage: DDD ≥100%, System ≥95%
- [ ] Clear UX→BFF→ApplicationService→Aggregate grounding path established
- [ ] OpenAPI integration strategy documented

## Timeline Estimate

- Phase 1 (Literature Research): 3-4 hours
- Phase 2 (Knight Analysis): 2-3 hours
- Phase 3 (Concept Definition): 2 hours
- Phase 4 (Grounding Design): 1-2 hours
- Phase 5 (Documentation): 4-5 hours
- Phase 6 (Schema Implementation): 2-3 hours
- Phase 7 (Examples): 2-3 hours
- Phase 8-9 (Validation): 1 hour
- Phase 10 (Research Questions): 1-2 hours
- Phase 11 (Final Deliverables): 1 hour

**Total**: 19-26 hours of focused research and implementation

## Notes

- This enhancement is critical for production readiness as it addresses the integration layer between UX and domain
- BFF pattern is increasingly standard in microservices architectures
- Command/Query separation improves schema clarity and supports CQRS evolution
- Research should validate against Knight codebase to ensure practical applicability
- Consider whether BFF should be DDD partition or separate canonical domain model
