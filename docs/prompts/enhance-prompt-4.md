# DDD Schema Enhancement Prompt 4: Application Services, CQRS, and BFF Pattern

## Objective

Research and extend the DDD canonical domain model to include:
1. **Application Service** pattern with Command/Query separation (CQRS)
2. **Backend for Frontend (BFF)** pattern as the integration layer between UX and domain
3. **BFF Interface** specification (REST/HTTP resources and operations)
4. Updated **UX-to-DDD grounding** that routes through BFF layer

This enhancement addresses the architectural gap where UX currently references DDD bounded contexts and aggregates directly, rather than through a well-defined integration boundary.

## Governance and Contribution Standards

This enhancement follows the **Data Engineering Taxonomy Contribution Methodology** (ref: `/Users/igor/code/data-eng-schema/CONTRIBUTING.md`):

### Semantic Versioning (SemVer)

All schema changes MUST follow **Semantic Versioning 2.0.0**:

```
MAJOR.MINOR.PATCH
```

- **MAJOR**: Breaking changes (remove concepts, change required fields, modify UID patterns)
- **MINOR**: Backward-compatible additions (new concepts, optional fields, new groundings)
- **PATCH**: Bug fixes (typos, clarifications, documentation corrections)

#### Version Impact Analysis for This Enhancement

**Current Versions**:
- `model_ddd`: v1.0.0 (strategic-ddd.schema.yaml, tactical-ddd.schema.yaml)
- `model_ux`: v2.0.0 (structure-ux, navigation-ux, interaction-ux schemas)
- `interdomain-map.yaml`: metadata.version = 2.2.0

**Expected Changes**:
- **DDD Tactical Schema**: v1.0.0 → **v1.1.0** (MINOR)
  - Reason: Adding new concepts (application_service, command, query) without breaking existing concepts
  - Change: Add `$defs.application_service`, `$defs.command`, `$defs.query`
  - Update: `naming_conventions` (add command_id, query_id patterns)
  - Impact: Backward compatible - existing models remain valid

- **DDD Strategic Schema** OR **New Integration Schema**: v1.0.0 → **v1.1.0** OR **v0.1.0** (MINOR or NEW)
  - Reason: Adding BFF concepts (bff_scope, bff_interface)
  - Options:
    * Option A: Add to strategic-ddd.schema.yaml (MINOR bump to v1.1.0)
    * Option B: Create integration-ddd.schema.yaml (NEW schema at v0.1.0)
  - Impact: Backward compatible if Option A; new schema if Option B

- **UX Interaction Schema**: v2.0.0 → **v2.1.0** (MINOR)
  - Reason: Add optional `api_endpoints` field to Component concept for BFF grounding
  - Impact: Backward compatible - field is optional

- **Interdomain Map**: v2.2.0 → **v2.3.0** (MINOR)
  - Reason: Add 6+ new grounding relationships (non-breaking)
  - Change: Add UX→BFF, BFF→AppSvc, AppSvc→Aggregate groundings
  - Impact: Backward compatible - only additions

**Breaking Change Check**: ❌ NO BREAKING CHANGES
- All existing concepts remain unchanged
- All new fields are optional
- All new concepts are additions (not replacements)
- **Verdict**: All changes are MINOR version bumps

### Grounding Schema Compliance

All groundings MUST validate against `/Users/igor/code/canonical-grounding/research-output/grounding-schema.json`:

**Required Grounding Properties** (from meta-schema):
```json
{
  "target_canon": "canon_[a-z_]+",
  "grounding_type": ["structural" | "semantic" | "procedural" | "epistemic"],
  "strength": "strong" | "weak" | "optional",
  "relationships": [
    {
      "source_concept": "string",
      "target_concept": "string (canon.concept format)",
      "mapping_type": "reference" | "alignment" | "constraint" | "equivalence",
      "cardinality": "one-to-one" | "one-to-many" | "many-to-one" | "many-to-many",
      "reference_field": "string",
      "validation_level": "required" | "optional" | "recommended"
    }
  ]
}
```

**New Groundings for This Enhancement** (must conform to schema):

1. `grounding_ux_bff_001`: UX Component → BFF Interface
2. `grounding_bff_app_svc_001`: BFF Interface → Application Service
3. `grounding_app_svc_agg_001`: Command → Aggregate
4. `grounding_app_svc_repo_001`: Application Service → Repository
5. `grounding_app_svc_evt_001`: Application Service → Domain Event
6. `grounding_ux_ddd_*_updated`: Revise existing UX→DDD groundings to route through BFF

### Interdomain Map Maintenance

**File**: `/Users/igor/code/canonical-grounding/research-output/interdomain-map.yaml`

**Required Updates**:

1. **Update Metadata**:
   ```yaml
   metadata:
     version: "2.3.0"  # MINOR bump
     last_updated: "2025-10-18"
     change_note: "Add Application Services, CQRS, and BFF pattern with 6+ new groundings"
   ```

2. **Update DDD Model Entry**:
   ```yaml
   canonical_models:
     - id: "model_ddd"
       version: "1.1.0"  # Tactical v1.1.0, Strategic v1.1.0 or new integration partition
       core_concepts:
         - Domain
         - BoundedContext
         - Aggregate
         - Entity
         - ValueObject
         - Repository
         - DomainService
         - ApplicationService  # NEW
         - Command            # NEW
         - Query              # NEW
         - BFFScope           # NEW (if in strategic schema)
         - BFFInterface       # NEW (if in strategic schema)
         - DomainEvent
         - Factory
   ```

3. **Add Partition Structure** (if BFF added to strategic or new integration schema):
   ```yaml
   - id: "model_ddd"
     partitions:
       - id: "model_ddd_strategic"
         schema_file: "schemas/strategic-ddd.schema.yaml"
         version: "1.1.0"
         concepts: [domain, bounded_context, context_mapping, bff_scope, bff_interface]
       - id: "model_ddd_tactical"
         schema_file: "schemas/tactical-ddd.schema.yaml"
         version: "1.1.0"
         concepts: [aggregate, entity, value_object, repository, domain_service, application_service, command, query, domain_event]
   ```

4. **Update Grounding Statistics**:
   ```yaml
   metadata:
     total_groundings: 38  # 32 existing + 6 new

   grounding_type_distribution:
     structural: 12  # +3 new (BFF→AppSvc, AppSvc→Agg, AppSvc→Repo)
     semantic: 10    # +1 new (UX terminology alignment)
     procedural: 8   # +2 new (Command orchestration, BFF routing)
     epistemic: 8    # unchanged

   grounding_strength_distribution:
     strong: 33      # +6 new (all new groundings are strong)
     weak: 5         # unchanged
   ```

5. **Update Closure Percentages**:
   ```yaml
   - id: "model_ddd"
     closure_percentage: 100  # Maintain 100% by grounding all new concepts

   - id: "model_ux"
     closure_percentage: 100  # Maintain 100% with BFF grounding
   ```

### UID and Naming Conventions

Follow the **UID Format Rules** from CONTRIBUTING.md:

| Entity Type          | Type Code | Pattern                 | Example                      |
|----------------------|-----------|-------------------------|------------------------------|
| Application Service  | `svc_app_`| `^svc_app_[a-z0-9_]+$`  | `svc_app_user_management`    |
| Command              | `cmd_`    | `^cmd_[a-z0-9_]+$`      | `cmd_create_user`            |
| Query                | `qry_`    | `^qry_[a-z0-9_]+$`      | `qry_find_user_by_id`        |
| BFF Scope            | `bff_`    | `^bff_[a-z0-9_]+$`      | `bff_web_app`                |
| BFF Interface        | `bff_if_` | `^bff_if_[a-z0-9_]+$`   | `bff_if_create_user`         |

**Validation**:
- All IDs MUST match the regex pattern
- IDs MUST be globally unique within the schema
- Use kebab-case (hyphens), NOT snake_case (underscores) or camelCase
- IDs MUST be descriptive, not abbreviations (avoid `cmd_cu`, use `cmd_create_user`)

### Testing and Validation Requirements

Before submitting changes:

1. **Schema Validation** (JSON Schema 2020-12):
   ```bash
   python tools/validate_multifile_schema.py
   # Expect: ✓ All schemas valid
   ```

2. **Grounding Validation**:
   ```bash
   python tools/validate_groundings.py
   # Checks:
   # - All target_canon references exist
   # - All source_concept and target_concept are defined
   # - No circular dependencies
   # - Cardinality constraints are satisfiable
   ```

3. **Closure Calculation**:
   ```bash
   python tools/calculate_closure.py
   # Target: DDD ≥100%, UX ≥100%, System ≥95%
   ```

4. **Example Validation**:
   ```bash
   python tools/validate_multifile_schema.py --examples
   # Validate all example YAML files against schemas
   ```

5. **Cross-Reference Check**:
   ```bash
   grep -r "svc_app_" domains/
   grep -r "cmd_" domains/
   grep -r "qry_" domains/
   grep -r "bff_" domains/
   # Ensure all references resolve
   ```

### Documentation Standards

**Required Documentation** (following CONTRIBUTING.md):

1. **Pattern YAML Files** (if patterns are formalized):
   - Create `domains/ddd/patterns/application-service-pattern.yaml`
   - Create `domains/ddd/patterns/bff-pattern.yaml`
   - Follow pattern template with: intent, context, problem, solution, structure, consequences

2. **Glossary Updates**:
   - Add terms to `docs/GLOSSARY.md`: Application Service, Command, Query, BFF, BFF Interface
   - Format: Definition + Examples + Context + Pattern References + Model Schema

3. **CHANGELOG Entry**:
   ```markdown
   ### Added (v1.1.0 - 2025-10-18)
   - **DDD Tactical Schema**: Application Service concept with Command/Query separation (CQRS)
   - **DDD Tactical Schema**: Command concept (write operations)
   - **DDD Tactical Schema**: Query concept (read operations)
   - **DDD Strategic Schema**: BFF Scope concept (UI-specific aggregation layer)
   - **DDD Strategic Schema**: BFF Interface concept (REST/HTTP operations)
   - **Groundings**: 6 new grounding relationships (UX→BFF→AppSvc→Aggregate chain)
   - **Documentation**: ddd-07-application-layer.md, ddd-08-bff-pattern.md
   - **Examples**: application-service-example.yaml, bff-example.yaml
   ```

4. **Migration Guide**:
   - Create `domains/ddd/MIGRATION-v1.1.md` documenting:
     * What's new in v1.1.0
     * How to adopt new concepts
     * Example migrations (old vs new)
     * Backward compatibility notes

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

**CRITICAL**: Update metadata.version to v2.3.0 and increment total_groundings count

#### 6.4 Cross-Domain Impact Analysis

Analyze impact on ALL applicable domains following grounding relationships in `interdomain-map.yaml`:

**Domains Requiring Updates**:

1. **DDD Domain** (PRIMARY - Direct Changes):
   - **Tactical Schema**: Add application_service, command, query (v1.0.0 → v1.1.0)
   - **Strategic Schema**: Add bff_scope, bff_interface OR create integration partition (v1.0.0 → v1.1.0 or v0.1.0)
   - **Documentation**: Add ddd-07-application-layer.md, ddd-08-bff-pattern.md
   - **Examples**: Add application-service-example.yaml, bff-example.yaml
   - **Grounding Impact**: 6+ new outbound groundings (to UX, Agile, QE)

2. **UX Domain** (SECONDARY - Grounding Changes):
   - **Interaction Schema**: Add optional `api_endpoints` array to Component (v2.0.0 → v2.1.0)
   - **Navigation Schema**: Add optional `bff_interface_ref` to Page (v2.0.0 → v2.1.0)
   - **Documentation**: Update ux/README.md to document BFF integration pattern
   - **Grounding Impact**: Update grounding_ux_ddd_001, grounding_ux_ddd_002 to route through BFF
   - **Examples**: Update existing UX examples to show BFF references

3. **QE Domain** (TERTIARY - Optional Test Coverage):
   - **Schema**: Consider adding `application_service_test` or `integration_test` concept (optional)
   - **Grounding Impact**: Add grounding_qe_ddd_005 (QE tests validate ApplicationService orchestration)
   - **Documentation**: Update qe/docs to include BFF and ApplicationService testing patterns
   - **Examples**: Add example showing how to test BFF endpoints and ApplicationService commands

4. **Agile Domain** (TERTIARY - Work Tracking):
   - **Delivery Schema**: Consider adding `technical_story_type` enum value for BFF/integration work (optional)
   - **Grounding Impact**: Agile stories may reference BFF interfaces being developed
   - **Documentation**: Update agile/docs to include BFF development in delivery planning
   - **Examples**: Add example story that delivers BFF endpoint

5. **Data-Eng Domain** (NO CHANGES - No Direct Grounding):
   - No schema changes required
   - Grounding remains indirect: UX → BFF → DDD ← Data-Eng
   - **Monitor**: If BFF aggregates data from multiple bounded contexts including data products, consider future grounding

**Grounding Dependency Chain** (must be updated in order):

```
1. DDD (foundation) - Add application_service, command, query, bff_scope, bff_interface
   ↓
2. UX (grounds_in: DDD) - Add api_endpoints field, update groundings to reference BFF
   ↓
3. QE (grounds_in: DDD, UX) - Add test concepts for ApplicationService/BFF validation
   ↓
4. Agile (grounds_in: all) - Reference new concepts in work tracking
```

**Interdomain Map Updates Required**:

1. Update `canonical_models.model_ddd`:
   - Bump version to v1.1.0
   - Add core_concepts: ApplicationService, Command, Query, BFFScope, BFFInterface
   - Update grounded_by list (unchanged, but validate completeness)

2. Update `canonical_models.model_ux`:
   - Bump version to v2.1.0
   - Update grounds_in to include specific DDD partition references
   - Validate closure_percentage remains 100%

3. Update `canonical_models.model_qe` (if test concepts added):
   - Bump version to v1.1.0
   - Add core_concepts: ApplicationServiceTest, BFFTest (if added)
   - Update closure_percentage (target: 75% → 80%+)

4. Update `canonical_models.model_agile` (if story types extended):
   - Bump version to v2.1.0 (if schema changes) or keep v2.0.0 (if no schema changes)
   - Validate closure_percentage remains 100%

5. Update `groundings` section:
   - Add grounding_ux_bff_001 (UX → BFF)
   - Add grounding_bff_app_svc_001 (BFF → ApplicationService)
   - Add grounding_app_svc_agg_001 (Command → Aggregate)
   - Add grounding_app_svc_repo_001 (ApplicationService → Repository)
   - Add grounding_app_svc_evt_001 (ApplicationService → DomainEvent)
   - Revise grounding_ux_ddd_001, grounding_ux_ddd_002 (add BFF intermediary)
   - Add grounding_qe_ddd_005 (if QE updated)

6. Update `graph_analysis`:
   - Recalculate centrality scores (DDD may increase due to new concepts)
   - Update grounding_type_distribution
   - Update grounding_strength_distribution
   - Recalculate semantic_distance (unchanged, but validate)

**Validation Checklist** (cross-domain):

- [ ] All new concepts in DDD have corresponding groundings
- [ ] UX references to DDD route through BFF (no direct Aggregate refs in new models)
- [ ] QE can test all new DDD concepts (ApplicationService, Command, Query, BFF)
- [ ] Agile can track work for all new concepts (stories for BFF endpoints, commands)
- [ ] No circular dependencies introduced
- [ ] Closure percentages maintained or improved for all domains
- [ ] All grounding relationships are bidirectionally documented
- [ ] Partition references in interdomain-map match actual schema files

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

**CRITICAL**: All deliverables must include proper semantic versioning metadata

1. **Research Documents** (in `domains/ddd/docs/`):
   - `ddd-07-application-layer.md` (6-10 pages)
     * Include version: 1.0.0, status: final, last_updated: YYYY-MM-DD
   - `ddd-08-bff-pattern.md` (6-10 pages)
     * Include version: 1.0.0, status: final, last_updated: YYYY-MM-DD
   - Updates to `ddd-03-tactical-patterns.md` (bump version to 1.1.0)
   - Updates to `ddd-02-strategic-patterns.md` (bump version to 1.1.0)

2. **Schema Updates**:
   - `domains/ddd/schemas/tactical-ddd.schema.yaml`
     * Version: 1.0.0 → 1.1.0 (MINOR bump)
     * Updated: metadata.updated field to current date
     * Change: Add application_service, command, query concepts
   - Strategic schema OR new integration schema
     * Option A: `strategic-ddd.schema.yaml` v1.0.0 → v1.1.0
     * Option B: NEW `integration-ddd.schema.yaml` v0.1.0
     * Change: Add bff_scope, bff_interface concepts

3. **Cross-Domain Schema Updates**:
   - `domains/ux/schemas/interaction-ux.schema.yaml`
     * Version: 2.0.0 → 2.1.0 (MINOR bump)
     * Change: Add optional `api_endpoints` array to Component
   - `domains/ux/schemas/navigation-ux.schema.yaml`
     * Version: 2.0.0 → 2.1.0 (MINOR bump)
     * Change: Add optional `bff_interface_ref` to Page
   - `domains/qe/model-schema.yaml` (if updated)
     * Version: 1.0.0 → 1.1.0 (MINOR bump)
     * Change: Add application_service_test, bff_test concepts (optional)
   - `domains/agile/schemas/delivery-agile.schema.yaml` (if updated)
     * Version: 2.0.0 → 2.1.0 (MINOR bump)
     * Change: Add technical_story_type enum values (optional)

4. **Examples** (with validation):
   - `domains/ddd/examples/application-service-example.yaml`
     * Must validate against tactical-ddd.schema.yaml v1.1.0
   - `domains/ddd/examples/bff-example.yaml`
     * Must validate against strategic or integration schema v1.1.0
   - Update `domains/ddd/examples/tactical-ddd-example.yaml` with commands/queries
   - Update `domains/ux/examples/partitioned/interaction-example.yaml` with BFF refs
     * Must validate against interaction-ux.schema.yaml v2.1.0

5. **Grounding Updates** (CRITICAL - Maintains interdomain-map.yaml integrity):
   - `research-output/interdomain-map.yaml`
     * Version: 2.2.0 → 2.3.0 (MINOR bump)
     * Updated: metadata.last_updated to current date
     * Change: Add 6+ new grounding relationships
     * Validation: All grounding IDs must be unique
     * Validation: All source/target must reference existing canonical_models
     * Format: Follow grounding-schema.json specification exactly
   - Updated grounding visualization `grounding-graph.svg` (regenerate if tooling exists)

6. **Validation Report** (validation-report.txt):
   ```
   Schema Validation: ✓ All schemas valid (JSON Schema 2020-12)

   Closure Analysis:
   - DDD: 100% (13 concepts, all grounded)
   - UX: 100% (17 concepts, all grounded)
   - QE: 75%+ (target: 80% if updated)
   - Agile: 100%
   - Data-Eng: 100%
   - System Average: 95%+

   Grounding Validation:
   - ✓ All target_canon references exist
   - ✓ All source_concept and target_concept defined
   - ✓ No circular dependencies (DAG maintained)
   - ✓ All cardinality constraints satisfiable
   - ✓ Total groundings: 32 → 38 (+6)

   Version Integrity:
   - ✓ All version bumps follow SemVer 2.0.0
   - ✓ No breaking changes (all MINOR/PATCH bumps)
   - ✓ metadata.updated fields current
   - ✓ interdomain-map.yaml version incremented

   Cross-Domain Validation:
   - ✓ UX→BFF→DDD grounding chain complete
   - ✓ All new DDD concepts have groundings
   - ✓ No orphaned concepts (100% closure maintained)

   Status: PRODUCTION READY ✓
   ```

7. **Knight Codebase Analysis** (knight-analysis.md):
   - Document of patterns found in `/Users/igor/code/knight/contexts`
   - Mapping table: Knight implementation ↔ Schema concepts
   - Code examples extracted from actual Java files
   - Pattern validations (confirm schema matches reality)

8. **CHANGELOG.md** (project root):
   ```markdown
   ## [1.1.0] - 2025-10-18

   ### Added - DDD Domain
   - **Tactical Schema** (v1.1.0): Application Service, Command, Query concepts
   - **Strategic Schema** (v1.1.0): BFF Scope, BFF Interface concepts
   - **Documentation**: ddd-07-application-layer.md, ddd-08-bff-pattern.md
   - **Examples**: application-service-example.yaml, bff-example.yaml
   - **Patterns**: Application Service pattern, BFF pattern

   ### Added - UX Domain
   - **Interaction Schema** (v2.1.0): Component.api_endpoints field
   - **Navigation Schema** (v2.1.0): Page.bff_interface_ref field
   - **Documentation**: Updated ux/README.md with BFF integration

   ### Added - Groundings
   - grounding_ux_bff_001: UX Component → BFF Interface
   - grounding_bff_app_svc_001: BFF Interface → Application Service
   - grounding_app_svc_agg_001: Command → Aggregate
   - grounding_app_svc_repo_001: Application Service → Repository
   - grounding_app_svc_evt_001: Application Service → Domain Event
   - grounding_qe_ddd_005: QE → Application Service (optional)

   ### Changed
   - **Interdomain Map** (v2.3.0): Updated grounding statistics (32 → 38)
   - **grounding_ux_ddd_001**: Revised to route through BFF layer
   - **grounding_ux_ddd_002**: Revised to route through BFF layer

   ### Migration
   - See `domains/ddd/MIGRATION-v1.1.md` for adoption guide
   - All changes backward compatible (MINOR version bumps)
   ```

9. **Migration Guide** (domains/ddd/MIGRATION-v1.1.md):
   ```markdown
   # DDD Schema Migration Guide: v1.0.0 → v1.1.0

   ## Summary
   Version 1.1.0 adds Application Services, CQRS, and BFF patterns.
   **Backward Compatible**: Existing v1.0.0 models remain valid.

   ## What's New

   ### Tactical Schema (v1.1.0)
   - application_service: Orchestrates use cases
   - command: Write operations (mutate state)
   - query: Read operations (no side effects)

   ### Strategic Schema (v1.1.0)
   - bff_scope: Backend for Frontend aggregation layer
   - bff_interface: REST/HTTP operations

   ## Migration Steps

   ### Step 1: Review New Concepts (Optional)
   Your existing models continue to work without changes.

   ### Step 2: Adopt Application Services (Recommended)
   Before (v1.0.0):
   ```yaml
   bounded_context:
     id: bc_user_management
     aggregates: [agg_user]
     repositories: [repo_user]
   ```

   After (v1.1.0):
   ```yaml
   bounded_context:
     id: bc_user_management
     aggregates: [agg_user]
     repositories: [repo_user]
     application_services: [svc_app_user_management]

   application_service:
     id: svc_app_user_management
     name: UserApplicationService
     bounded_context_ref: bc_user_management
     commands: [cmd_create_user, cmd_activate_user]
     queries: [qry_find_user_by_id]
   ```

   ### Step 3: Adopt BFF Pattern (For UX Integration)
   ... (detailed examples)
   ```

10. **Glossary Updates** (docs/GLOSSARY.md):
    - Add entries for: Application Service, Command, Query, BFF, BFF Interface
    - Format per CONTRIBUTING.md: Definition + Examples + Context + Pattern Refs

11. **Cross-Domain Updates**:
    - `domains/ux/README.md`: Document BFF integration pattern
    - `domains/qe/README.md`: Document testing ApplicationService and BFF (if applicable)
    - `domains/agile/README.md`: Document tracking BFF/integration work (if applicable)

## Success Criteria

### Research and Analysis
- [ ] All 10 research questions answered with citations
- [ ] Knight codebase analysis complete with mapping table
- [ ] Literature synthesis from 5 sources (BFF, Fowler, Evans, Vernon, REST/OpenAPI)

### Schema Changes
- [ ] 5 new DDD concepts defined with complete JSON Schema 2020-12 definitions
  - [ ] application_service (tactical-ddd.schema.yaml v1.1.0)
  - [ ] command (tactical-ddd.schema.yaml v1.1.0)
  - [ ] query (tactical-ddd.schema.yaml v1.1.0)
  - [ ] bff_scope (strategic-ddd.schema.yaml v1.1.0 OR integration-ddd.schema.yaml v0.1.0)
  - [ ] bff_interface (strategic-ddd.schema.yaml v1.1.0 OR integration-ddd.schema.yaml v0.1.0)
- [ ] All schema metadata.version fields updated following SemVer
- [ ] All schema metadata.updated fields set to current date

### Cross-Domain Updates
- [ ] UX interaction schema updated (v2.0.0 → v2.1.0)
- [ ] UX navigation schema updated (v2.0.0 → v2.1.0)
- [ ] QE schema updated (optional, v1.0.0 → v1.1.0)
- [ ] Agile schema updated (optional, v2.0.0 → v2.1.0)

### Grounding Relationships
- [ ] 6+ new grounding relationships documented in interdomain-map.yaml
  - [ ] grounding_ux_bff_001: UX Component → BFF Interface
  - [ ] grounding_bff_app_svc_001: BFF Interface → Application Service
  - [ ] grounding_app_svc_agg_001: Command → Aggregate
  - [ ] grounding_app_svc_repo_001: Application Service → Repository
  - [ ] grounding_app_svc_evt_001: Application Service → Domain Event
  - [ ] grounding_ux_ddd_001_revised: Updated to route through BFF
  - [ ] grounding_ux_ddd_002_revised: Updated to route through BFF
  - [ ] grounding_qe_ddd_005 (optional): QE → Application Service
- [ ] interdomain-map.yaml version updated (v2.2.0 → v2.3.0)
- [ ] All groundings validate against grounding-schema.json
- [ ] Grounding statistics updated (total_groundings, distribution)

### Examples and Validation
- [ ] 2+ comprehensive examples based on Knight codebase patterns
  - [ ] application-service-example.yaml (validates against tactical v1.1.0)
  - [ ] bff-example.yaml (validates against strategic v1.1.0 or integration v0.1.0)
- [ ] Updated existing examples with new concepts
- [ ] All examples validate without errors
- [ ] Closure percentage maintained: DDD ≥100%, UX ≥100%, System ≥95%
- [ ] No circular dependencies (DAG integrity maintained)

### Documentation
- [ ] 2 new documentation files created
  - [ ] ddd-07-application-layer.md (6-10 pages, v1.0.0)
  - [ ] ddd-08-bff-pattern.md (6-10 pages, v1.0.0)
- [ ] 2 existing documentation files updated
  - [ ] ddd-03-tactical-patterns.md (v1.0.0 → v1.1.0)
  - [ ] ddd-02-strategic-patterns.md (v1.0.0 → v1.1.0)
- [ ] CHANGELOG.md updated with v1.1.0 entry
- [ ] MIGRATION-v1.1.md created with adoption guide
- [ ] GLOSSARY.md updated with 5 new terms
- [ ] Cross-domain README files updated (UX, QE, Agile as applicable)

### Validation and Quality
- [ ] Schema validation: ✓ All schemas valid (JSON Schema 2020-12)
- [ ] Grounding validation: ✓ All references resolve
- [ ] Cross-reference validation: ✓ All IDs unique, all refs exist
- [ ] Version integrity: ✓ All bumps follow SemVer
- [ ] Closure validation: ✓ DDD 100%, System 95%+
- [ ] UID format validation: ✓ All IDs match regex patterns
- [ ] Validation report generated (validation-report.txt)

### Integration and Grounding Path
- [ ] Clear UX→BFF→ApplicationService→Aggregate grounding path established
- [ ] BFF layer correctly positioned between UX and DDD
- [ ] No direct UX→Aggregate references in new examples
- [ ] OpenAPI integration strategy documented
- [ ] Command/Query separation pattern clearly defined

### Deliverables Completeness
- [ ] 11 deliverable categories complete (Research, Schemas, Cross-Domain, Examples, Groundings, Validation, Analysis, CHANGELOG, Migration, Glossary, Cross-Domain Updates)
- [ ] All files follow CONTRIBUTING.md standards
- [ ] All files include proper version metadata
- [ ] Knight codebase analysis document delivered

## Timeline Estimate

- Phase 1 (Literature Research): 3-4 hours
- Phase 2 (Knight Analysis): 2-3 hours
- Phase 3 (Concept Definition): 2 hours
- Phase 4 (Grounding Design): 1-2 hours
- Phase 5 (Documentation): 4-5 hours
- Phase 6 (Schema Implementation): 3-4 hours (updated: includes cross-domain)
- Phase 7 (Examples): 2-3 hours
- Phase 8-9 (Validation): 1-2 hours (updated: comprehensive validation)
- Phase 10 (Research Questions): 1-2 hours
- Phase 11 (Final Deliverables): 2-3 hours (updated: CHANGELOG, Migration, Glossary)

**Total**: 21-31 hours of focused research and implementation (updated from 19-26 to account for governance requirements)

## Summary

This enhancement extends the canonical grounding framework with Application Services (CQRS) and BFF patterns, establishing a complete UX→BFF→ApplicationService→Aggregate integration chain. Following the Data Engineering Taxonomy contribution methodology, all changes adhere to Semantic Versioning 2.0.0 with no breaking changes (MINOR version bumps only).

**Key Governance Requirements**:
- **SemVer Compliance**: All schemas bump to MINOR versions (v1.0.0 → v1.1.0, v2.0.0 → v2.1.0)
- **Grounding Schema Compliance**: All 6+ new groundings validate against grounding-schema.json
- **Interdomain Map Maintenance**: Version bump to v2.3.0 with updated statistics and closure analysis
- **Cross-Domain Impact**: Ripple updates across DDD, UX, QE (optional), Agile (optional)
- **UID Format Validation**: All new IDs follow CONTRIBUTING.md regex patterns
- **Backward Compatibility**: Existing v1.0.0/v2.0.0 models remain valid

**Research Foundation**:
- **Primary Source**: Sam Newman (BFF pattern) → Fowler (Application Service) → Evans (Application Layer) → Vernon (CQRS) → REST/OpenAPI
- **Validation**: Knight codebase analysis confirms practical applicability

**Expected Impact**:
- **DDD Closure**: Maintain 100% (13 concepts, all grounded)
- **UX Closure**: Maintain 100% (17 concepts, all grounded)
- **System Closure**: Maintain ≥95% average
- **Total Groundings**: 32 → 38 (+6)
- **Grounding Strength**: 27 → 33 strong groundings (+6)

**Critical Success Factors**:
1. All 5 new concepts have complete schema definitions (application_service, command, query, bff_scope, bff_interface)
2. All 6+ groundings validate and reference existing canonical models
3. No circular dependencies (DAG topology maintained)
4. Version metadata consistently updated across all affected schemas
5. Comprehensive validation report confirms PRODUCTION READY status

## Notes

- This enhancement is critical for production readiness as it addresses the integration layer between UX and domain
- BFF pattern is increasingly standard in microservices architectures following Sam Newman's work
- Command/Query separation improves schema clarity and supports CQRS evolution
- Research validates against Knight codebase (`/Users/igor/code/knight/contexts`) to ensure practical applicability
- BFF concepts added to Strategic DDD schema (Option A - v1.1.0) OR new Integration DDD partition (Option B - v0.1.0) based on research findings
- All changes maintain backward compatibility - existing models continue to validate
- Interdomain map serves as the single source of truth for all grounding relationships
- Cross-domain updates follow the dependency chain: DDD → UX → QE → Agile
- OpenAPI specifications remain external (referenced via `api_specification_ref` field)
- Timeline: 21-31 hours accounts for comprehensive governance, validation, and documentation requirements
