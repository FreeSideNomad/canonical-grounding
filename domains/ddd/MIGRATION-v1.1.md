# Migration Guide: DDD Domain Model v1.0 → v1.1

**Version**: 1.1.0
**Date**: 2025-10-18
**Type**: Minor version (backward compatible)

---

## Overview

This migration guide covers the transition from DDD domain model v1.0.0 to v1.1.0. This is a **minor version** release with **no breaking changes**. All additions are backward compatible.

**What's New**:
- Application Service pattern
- CQRS pattern (Command and Query interfaces)
- BFF pattern (Backend-for-Frontend)
- 10 new grounding relationships
- Enhanced examples and documentation

**Impact**: ⚠️ Low - Additive changes only

---

## Schema Changes

### 1. Tactical DDD Schema (tactical-ddd.schema.yaml)

**Version**: 1.0.0 → 1.1.0

#### Added Concepts

**application_service** (lines 312-633):
```yaml
$defs:
  application_service:
    type: object
    description: "Stateless service orchestrating use case execution"
    required:
      - id
      - name
      - bounded_context_ref
      - implements_commands
      - implements_queries
```

**command_interface** (lines 556-710):
```yaml
$defs:
  command_interface:
    type: object
    description: "Command interface with nested command records"
    required:
      - id
      - name
      - bounded_context_ref
      - command_records
```

**query_interface** (lines 711-906):
```yaml
$defs:
  query_interface:
    type: object
    description: "Query interface with nested result records"
    required:
      - id
      - name
      - bounded_context_ref
      - query_methods
```

#### New Naming Conventions

Add to your naming conventions:
```yaml
naming_conventions:
  application_service_id: "svc_app_<name>"
  command_id: "cmd_<name>"
  query_id: "qry_<name>"
```

#### New Validation Rules

Add validation rules (lines 929-936):
```yaml
validation_rules:
  - rule: "application_service_stateless"
    description: "Application services must be stateless"

  - rule: "one_aggregate_per_transaction"
    description: "Command must modify at most one aggregate per transaction"

  - rule: "queries_no_side_effects"
    description: "Queries must have no side effects"
```

#### New Best Practices

Add to best practices section (lines 949-974):
- Keep application services thin - no business logic
- One aggregate per transaction
- Application service method = one use case
- Commands as nested records (Knight pattern)
- Queries as interface methods with result records
- CQRS selectively where read/write models differ

---

### 2. Strategic DDD Schema (strategic-ddd.schema.yaml)

**Version**: 1.0.0 → 1.1.0

#### Added Concepts

**bff_scope** (lines 230-481):
```yaml
$defs:
  bff_scope:
    type: object
    description: "Backend-for-Frontend scope for client type"
    required:
      - id
      - name
      - client_type
      - serves_interface
      - aggregates_from_contexts
      - owned_by_team
```

**bff_interface** (lines 482-707):
```yaml
$defs:
  bff_interface:
    type: object
    description: "BFF interface implementation"
    required:
      - id
      - name
      - bff_scope_ref
      - primary_bounded_context_ref
      - base_path
```

#### Updated bounded_context

Add application_services field:
```yaml
bounded_context:
  properties:
    application_services:
      type: array
      description: "Application services in this context"
      items:
        type: string
        pattern: "^svc_app_[a-z0-9_]+$"
```

#### New Naming Conventions

```yaml
naming_conventions:
  bff_scope_id: "bff_<client_type>"
  bff_interface_id: "bff_if_<context>_<client_type>"
```

#### New Best Practices

Add to best practices:
- One BFF per client type (web, iOS, Android)
- BFF aggregates from MULTIPLE bounded contexts
- BFF owned by frontend team
- Use hybrid: API Gateway + BFFs
- BFF delegates to application services

---

### 3. UX Schema Updates (v2.0 → v2.1)

#### interaction-ux.schema.yaml

**Version**: 2.0.0 → 2.1.0

Add to `component`:
```yaml
component:
  properties:
    api_endpoints:
      type: array
      description: "BFF interface endpoints this component invokes"
      items:
        type: string
        pattern: "^bff_if_[a-z0-9_]+$"
```

Add to `workflow`:
```yaml
workflow:
  properties:
    application_service:
      type: string
      pattern: "^svc_app_[a-z0-9_]+$"
      description: "DDD application service implementing workflow"
```

#### navigation-ux.schema.yaml

**Version**: 2.0.0 → 2.1.0

Add to `page`:
```yaml
page:
  properties:
    bff_interface_ref:
      type: string
      pattern: "^bff_if_[a-z0-9_]+$"
      description: "Optional BFF interface for this page's data"
```

---

## Migration Steps

### Step 1: Update Schema Files

No action required - schemas are backward compatible. Your existing YAML files remain valid.

**Optional**: Add metadata updates to track version:
```yaml
metadata:
  updated: "2025-10-18"
  version: "1.1.0"
```

### Step 2: Adopt New Patterns (Optional)

If you want to adopt the new patterns:

#### Add Application Services

```yaml
# Example: Add application service to your bounded context
application_services:
  - id: svc_app_user_management
    name: UserApplicationService
    bounded_context_ref: bc_user_management
    implements_commands:
      - cmd_user_commands
    implements_queries:
      - qry_user_queries
    dependencies:
      repositories:
        - repo_user
```

#### Add Command Interfaces

```yaml
command_interfaces:
  - id: cmd_user_commands
    name: UserCommands
    bounded_context_ref: bc_user_management
    command_records:
      - record_name: CreateUserCmd
        intent: createUser
        parameters: [...]
        returns: domain_id
        modifies_aggregate: agg_user
```

#### Add Query Interfaces

```yaml
query_interfaces:
  - id: qry_user_queries
    name: UserQueries
    bounded_context_ref: bc_user_management
    query_methods:
      - method_name: getUserSummary
        parameters: [...]
        result_record_name: UserSummary
```

#### Add BFF Scope

```yaml
bff_scopes:
  - id: bff_web
    name: WebBFF
    client_type: web
    aggregates_from_contexts:
      - bc_user_management
      - bc_order_management
    owned_by_team: Web Frontend Team
```

#### Add BFF Interface

```yaml
bff_interfaces:
  - id: bff_if_user_web
    name: "User Management Web BFF Interface"
    bff_scope_ref: bff_web
    primary_bounded_context_ref: bc_user_management
    base_path: /api/web/users
    endpoints:
      - path: /create
        method: POST
        operation_type: command
        delegates_to_commands:
          - cmd_user_commands
```

### Step 3: Update Grounding References (Optional)

If using interdomain-map.yaml, add new grounding types:

```yaml
groundings:
  - id: grounding_ux_bff_001
    source: model_ux_interaction
    target: model_ddd_strategic
    type: structural
    strength: strong
    description: "UX Component references BFF Interface"
```

See `/grounding-relationships.yaml` for complete list of 10 new groundings.

### Step 4: Update Examples (Optional)

Review new examples for patterns:
- `/domains/ddd/examples/application-service-example.yaml` - Complete User Management
- `/domains/ddd/examples/bff-example.yaml` - Web BFF with multi-context aggregation

---

## Breaking Changes

**None** - This is a backward-compatible release.

---

## Deprecations

**None** - All existing concepts remain valid.

---

## New Validation Rules

If you're validating schemas programmatically, add checks for:

1. **Application Service Stateless**: `application_service.characteristics.stateless === true`
2. **One Aggregate Per Transaction**: `command.modifies_aggregate` has maxItems: 1
3. **Queries No Side Effects**: `query_interface.no_side_effects === true`
4. **BFF No Business Logic**: `bff_scope.responsibilities.business_logic === false`

---

## Updated Dependencies

### Grounding Relationships

Total groundings increased from 32 to 42. New grounding chains:

**UX → Aggregate Complete Chain**:
```
UX:Component
  → BFF:Interface (grounding_ux_bff_001)
  → ApplicationService (grounding_bff_app_svc_001)
  → Command/Query (grounding_bff_cmd_001 or grounding_bff_qry_001)
  → Aggregate (grounding_cmd_agg_001 or grounding_qry_agg_001)
```

**ApplicationService Dependencies**:
```
ApplicationService
  → Repository (grounding_app_svc_repo_001)
  → DomainEvent (grounding_app_svc_evt_001)
  → Command (grounding_app_svc_cmd_001)
  → Query (grounding_app_svc_qry_001)
```

---

## Testing Migration

### Validation Checklist

- [ ] Run schema validation: `python tools/validate-schemas.py`
- [ ] Validate examples: `python tools/validate-example.py`
- [ ] Check grounding references: `python tools/validate-grounding-references.py`
- [ ] Verify closure percentages maintained (DDD: 100%, UX: 100%)

### Example Migration Test

Test with existing files:
```bash
# Should pass without changes
python tools/validate-example.py \
  domains/ddd/examples/order-example.yaml \
  domains/ddd/schemas/tactical-ddd.schema.yaml
```

Test with new patterns:
```bash
# Test new application service example
python tools/validate-example.py \
  domains/ddd/examples/application-service-example.yaml \
  domains/ddd/schemas/tactical-ddd.schema.yaml

# Test new BFF example
python tools/validate-example.py \
  domains/ddd/examples/bff-example.yaml \
  domains/ddd/schemas/strategic-ddd.schema.yaml
```

---

## Rollback Procedure

If you need to rollback:

1. **Schema Version**: Change metadata version back to 1.0.0
2. **Remove New Concepts**: Delete application_service, command_interface, query_interface, bff_scope, bff_interface definitions
3. **Grounding Map**: Revert interdomain-map.yaml to v2.2.0

**Note**: Only necessary if you explicitly adopted v1.1 features. Existing v1.0 files continue to work.

---

## Support and Resources

### Documentation

- **Schema Reference**: `/domains/ddd/schemas/`
- **Examples**: `/domains/ddd/examples/`
- **Research Questions**: `/RESEARCH_QUESTIONS_ANSWERED.md`
- **Grounding Relationships**: `/grounding-relationships.yaml`

### Pattern Guides

- **Application Layer**: `/domains/ddd/docs/ddd-07-application-layer.md`
- **BFF Pattern**: `/domains/ddd/docs/ddd-08-bff-pattern.md`

### Quick Reference

- **Groundings Quick Reference**: `/QUICK_REFERENCE_GROUNDINGS.md`
- **Grounding Chain Diagram**: `/GROUNDING_CHAIN_DIAGRAM.md`

---

## FAQ

### Q: Do I need to update my existing YAML files?

**A**: No. This is a backward-compatible release. Your existing files remain valid.

### Q: Should I adopt the new patterns immediately?

**A**: Only if they fit your use case. The new patterns (ApplicationService, CQRS, BFF) are optional enhancements for specific architectural needs.

### Q: What if I'm already using Application Services?

**A**: You can now formally document them using the new schema definitions. See `/domains/ddd/examples/application-service-example.yaml` for the pattern.

### Q: How does BFF relate to my existing API design?

**A**: BFF is a pattern for client-specific orchestration. You can layer it on top of existing APIs or use it as a new integration pattern. See research question #4 in `/RESEARCH_QUESTIONS_ANSWERED.md`.

### Q: Are Commands and Queries required?

**A**: No. They're part of the CQRS pattern which is optional. Use them when you need clear separation of read and write models.

### Q: What about transaction boundaries?

**A**: The new schemas formalize the "one aggregate per transaction" rule (Vaughn Vernon). This was always a best practice, now it's enforced in validation rules.

---

## Version History

| Version | Date | Type | Changes |
|---------|------|------|---------|
| 1.1.0 | 2025-10-18 | Minor | Added ApplicationService, CQRS, BFF patterns |
| 1.0.0 | 2025-10-13 | Major | Initial release |

---

## Contact

For questions or issues with migration:
- Review `/RESEARCH_QUESTIONS_ANSWERED.md`
- Check examples in `/domains/ddd/examples/`
- Consult grounding relationships in `/grounding-relationships.yaml`
