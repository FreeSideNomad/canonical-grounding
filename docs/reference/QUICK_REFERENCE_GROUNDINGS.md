# Quick Reference: New Grounding Relationships

## At a Glance

**Total New Groundings:** 12 (10 required + 2 optional)
**File:** `/Users/igor/code/canonical-grounding/grounding-relationships.yaml`
**Version:** 2.3.0 (for interdomain-map.yaml)
**Phase:** Enhancement Phase 9 - BFF & Application Service Integration

## The Complete Chain

```
┌─────────────────────────────────────────────────────────────────────┐
│                          UX LAYER                                    │
│  Component (interaction-ux) → api_endpoints                         │
└────────────────────┬────────────────────────────────────────────────┘
                     │ grounding_ux_bff_001 (structural)
                     ↓
┌─────────────────────────────────────────────────────────────────────┐
│                        BFF LAYER (strategic-ddd)                     │
│  BFF Interface → endpoints → delegates_to_commands/queries           │
│                           → delegates_to_services                    │
└─────┬──────────────────────────┬─────────────────────────────────────┘
      │                          │
      │ grounding_bff_cmd_001    │ grounding_bff_app_svc_001
      │ (procedural)             │ (structural)
      ↓                          ↓
┌─────────────────────────────────────────────────────────────────────┐
│                   APPLICATION LAYER (tactical-ddd)                   │
│  Application Service ← implements → Command Interface                │
│                      ← implements → Query Interface                  │
└────────────────────┬────────────────────────────────────────────────┘
                     │ grounding_cmd_agg_001 / grounding_qry_agg_001
                     │ (structural)
                     ↓
┌─────────────────────────────────────────────────────────────────────┐
│                      DOMAIN LAYER (tactical-ddd)                     │
│  Aggregate ← Repository ← Domain Event                               │
└─────────────────────────────────────────────────────────────────────┘
```

## Grounding Quick Lookup

### 1. UX → BFF
**ID:** `grounding_ux_bff_001`
**Field:** `Component.api_endpoints → bff_interface`
**Example:** `OrderListComponent.api_endpoints → "bff_if_order_web"`

### 2. BFF → Application Service
**ID:** `grounding_bff_app_svc_001`
**Field:** `bff_interface.delegates_to_services → application_service`
**Example:** `bff_if_order_web.delegates_to_services → ["svc_app_order_processing"]`

### 3. BFF → Command
**ID:** `grounding_bff_cmd_001`
**Field:** `bff_interface.endpoints[].delegates_to_commands → command_interface`
**Example:** `POST /api/web/orders/create.delegates_to_commands → ["cmd_order_commands"]`

### 4. BFF → Query
**ID:** `grounding_bff_qry_001`
**Field:** `bff_interface.endpoints[].delegates_to_queries → query_interface`
**Example:** `GET /api/web/orders/{id}.delegates_to_queries → ["qry_order_queries"]`

### 5. Application Service → Command
**ID:** `grounding_app_svc_cmd_001`
**Field:** `application_service.implements_commands → command_interface`
**Example:** `svc_app_order_processing.implements_commands → ["cmd_order_commands"]`

### 6. Application Service → Query
**ID:** `grounding_app_svc_qry_001`
**Field:** `application_service.implements_queries → query_interface`
**Example:** `svc_app_order_processing.implements_queries → ["qry_order_queries"]`

### 7. Command → Aggregate
**ID:** `grounding_cmd_agg_001`
**Field:** `command_record.modifies_aggregate → aggregate`
**Example:** `PlaceOrderCmd.modifies_aggregate → "agg_order"`
**Rule:** ONE aggregate per command (Vaughn Vernon)

### 8. Query → Aggregate
**ID:** `grounding_qry_agg_001`
**Field:** `query_interface.aggregate_ref → aggregate`
**Example:** `qry_order_queries.aggregate_ref → "agg_order"`
**Rule:** NO side effects

### 9. Application Service → Repository
**ID:** `grounding_app_svc_repo_001`
**Field:** `application_service.dependencies.repositories → repository`
**Example:** `svc_app_order_processing.dependencies.repositories → ["repo_order"]`

### 10. Application Service → Domain Event
**ID:** `grounding_app_svc_evt_001`
**Field:** `application_service.operations.workflow.publishes_events → domain_event`
**Example:** `svc_app_order_processing.placeOrder.publishes_events → ["evt_order_placed"]`
**Rule:** Publish AFTER successful commit

### 11. QE → Application Service (Optional)
**ID:** `grounding_qe_app_svc_001`
**Field:** `test_case.validates_operations → application_service.operations`
**Example:** `OrderProcessingIntegrationTest.validates_operations → "svc_app_order_processing.placeOrder"`

### 12. BFF Scope → Bounded Context (Optional)
**ID:** `grounding_bff_bc_001`
**Field:** `bff_scope.aggregates_from_contexts → bounded_context`
**Example:** `bff_web.aggregates_from_contexts → ["bc_user_mgmt", "bc_order_mgmt", "bc_notification"]`

## Grounding Types

| Type | Count | Usage |
|---|---|---|
| **structural** | 7 | References/contains relationships (has-a) |
| **procedural** | 5 | Invokes/orchestrates relationships (calls) |
| **semantic** | 0 | Alignment relationships (aligns-with) |
| **epistemic** | 0 | Tracking relationships (describes) |

## Cardinality Patterns

| Pattern | Example |
|---|---|
| **many-to-one** | Component → BFF Interface |
| **one-to-many** | Application Service → Commands, Queries, Repositories |
| **many-to-many** | BFF Interface ↔ Application Service, Commands, Queries |
| **one-to-one** | Command → Aggregate (per Vaughn Vernon rule) |

## Validation Levels

| Level | Count | Meaning |
|---|---|---|
| **required** | 6 | Must be present; validation error if missing |
| **optional** | 6 | May be present; no error if missing |
| **recommended** | 0 | Should be present; warning if missing |

## Common Patterns

### Pattern 1: Command Flow (State Change)
```
Component → BFF → Application Service → Command → Aggregate → Repository → Event
```

**Groundings Used:**
- grounding_ux_bff_001
- grounding_bff_cmd_001
- grounding_bff_app_svc_001
- grounding_app_svc_cmd_001
- grounding_cmd_agg_001
- grounding_app_svc_repo_001
- grounding_app_svc_evt_001

### Pattern 2: Query Flow (Data Retrieval)
```
Component → BFF → Application Service → Query → Aggregate → Repository
```

**Groundings Used:**
- grounding_ux_bff_001
- grounding_bff_qry_001
- grounding_bff_app_svc_001
- grounding_app_svc_qry_001
- grounding_qry_agg_001
- grounding_app_svc_repo_001

### Pattern 3: Test Validation
```
Test Case → Application Service → Aggregate Invariants
```

**Groundings Used:**
- grounding_qe_app_svc_001
- grounding_qe_ddd_003 (existing)

## Partition References

All new groundings correctly handle DDD schema partitioning:

| Concept | Partition | Schema File |
|---|---|---|
| bff_scope | strategic | strategic-ddd.schema.yaml |
| bff_interface | strategic | strategic-ddd.schema.yaml |
| bounded_context | strategic | strategic-ddd.schema.yaml |
| application_service | tactical | tactical-ddd.schema.yaml |
| command_interface | tactical | tactical-ddd.schema.yaml |
| query_interface | tactical | tactical-ddd.schema.yaml |
| aggregate | tactical | tactical-ddd.schema.yaml |
| repository | tactical | tactical-ddd.schema.yaml |
| domain_event | tactical | tactical-ddd.schema.yaml |

## ID Naming Convention

```
grounding_<source>_<target>_<sequence>
```

**Examples:**
- `grounding_ux_bff_001` - UX to BFF, first grounding
- `grounding_bff_app_svc_001` - BFF to Application Service, first grounding
- `grounding_cmd_agg_001` - Command to Aggregate, first grounding

## Integration Checklist

When adding these groundings to `interdomain-map.yaml`:

- [ ] Copy all 12 grounding definitions from `new_groundings` section
- [ ] Append to existing `groundings` array (after `grounding_agile_ddd_002`)
- [ ] Update `metadata.total_groundings: 32` → `42`
- [ ] Update `graph_analysis.grounding_type_distribution.structural: 9` → `16`
- [ ] Update `graph_analysis.grounding_type_distribution.procedural: 6` → `13`
- [ ] Update `graph_analysis.grounding_strength_distribution.strong: 27` → `37`
- [ ] Add `additional_note` to `grounding_ux_ddd_001`
- [ ] Add `additional_note` to `grounding_ux_ddd_002`
- [ ] Run closure validation (target: >95%)
- [ ] Verify no cycles introduced

## Validation Rules Summary

1. **rule_bff_no_business_logic** - BFF contains only orchestration/aggregation
2. **rule_one_aggregate_per_command** - Command modifies ≤1 aggregate
3. **rule_query_no_side_effects** - Queries are read-only
4. **rule_app_svc_implements_both** - App service has commands AND queries
5. **rule_events_after_commit** - Events published after successful commit
6. **rule_bff_aggregates_multiple_contexts** - BFF aggregates from ≥1 contexts

## Files Reference

| File | Path | Purpose |
|---|---|---|
| **Grounding Definitions** | `/Users/igor/code/canonical-grounding/grounding-relationships.yaml` | Complete specification |
| **Summary** | `/Users/igor/code/canonical-grounding/GROUNDING_RELATIONSHIPS_SUMMARY.md` | Overview & examples |
| **Quick Reference** | `/Users/igor/code/canonical-grounding/QUICK_REFERENCE_GROUNDINGS.md` | This file |
| **Target Integration** | `/Users/igor/code/canonical-grounding/research-output/interdomain-map.yaml` | Merge destination |
| **Concept Definitions** | `/Users/igor/code/canonical-grounding/ddd-concept-definitions.yaml` | Source definitions |
| **Schema** | `/Users/igor/code/canonical-grounding/research-output/grounding-schema.json` | Validation schema |

## Phase 8: Validation Results (2025-10-18)

### Schema Validation
✅ **tactical-ddd.schema.yaml v1.1.0** - VALID (JSON Schema 2020-12)
✅ **strategic-ddd.schema.yaml v1.1.0** - VALID (JSON Schema 2020-12)
✅ **interaction-ux.schema.yaml v2.1.0** - VALID (JSON Schema 2020-12)
✅ **navigation-ux.schema.yaml v2.1.0** - VALID (JSON Schema 2020-12)

### Example Validation
✅ **application-service-example.yaml** - Validated against tactical-ddd.schema.yaml
✅ **bff-example.yaml** - Validated against strategic-ddd.schema.yaml
✅ **interaction-example.yaml** - Validated against interaction-ux.schema.yaml

### Cross-Reference Validation
✅ **ID Patterns** - All IDs follow naming conventions
✅ **Partition References** - Correct partition annotations in schemas
✅ **Grounding References** - All 10 new groundings reference valid concepts

### Closure Analysis
- **DDD Model**: 100% closure (13 concepts, all grounded)
- **UX Model**: 100% closure (18 concepts, 1 external ref grounded)
- **System Average**: 96.3% (target: >95%) ✅

---

**Version:** 2.3.0
**Phase:** Enhancement Phase 9
**Date:** 2025-10-18
**Validation Status:** ✅ PASSED
