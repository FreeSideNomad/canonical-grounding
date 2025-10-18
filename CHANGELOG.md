# Changelog

All notable changes to the Canonical Grounding framework will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.1.0] - 2025-10-18

### Added

#### DDD Domain Model Enhancement

**New Concepts (4)**:
- `application_service` - Stateless orchestration service implementing use cases (tactical schema)
- `command_interface` - Command definitions as nested records in API layer (tactical schema)
- `query_interface` - Query methods with result DTOs in API layer (tactical schema)
- `bff_scope` - Backend-for-Frontend scope for client-specific orchestration (strategic schema)
- `bff_interface` - BFF interface implementation (strategic schema)

**New Patterns**:
- CQRS Pattern (Command Query Responsibility Segregation)
- BFF Pattern (Backend-for-Frontend)
- Application Service Pattern
- Repository Pattern enhancements

#### Schema Files

**Updated Schemas** (v1.0.0 → v1.1.0):
- `domains/ddd/schemas/tactical-ddd.schema.yaml` v1.1.0
  - Added `application_service` definition (lines 312-633)
  - Added `command_interface` definition (lines 556-710)
  - Added `query_interface` definition (lines 711-906)
  - Added validation rules for CQRS and transaction boundaries

- `domains/ddd/schemas/strategic-ddd.schema.yaml` v1.1.0
  - Added `bff_scope` definition (lines 230-481)
  - Added `bff_interface` definition (lines 482-707)
  - Updated `bounded_context` to include application_services array

**Updated UX Schemas** (v2.0.0 → v2.1.0):
- `domains/ux/schemas/interaction-ux.schema.yaml` v2.1.0
  - Added `api_endpoints` field to `component` (line 206-209)
  - Added `application_service` field to `workflow` (line 57-60)

- `domains/ux/schemas/navigation-ux.schema.yaml` v2.1.0
  - Added `bff_interface_ref` field to `page` (line 202-205)

#### Example Files

**New Examples**:
- `domains/ddd/examples/application-service-example.yaml`
  - Complete User Management example
  - Demonstrates ApplicationService implementing Commands and Queries
  - Shows transaction management and event publishing
  - 667 lines of comprehensive documentation

- `domains/ddd/examples/bff-example.yaml`
  - Web BFF example aggregating from multiple contexts
  - Shows BFF interface delegation to application services
  - Demonstrates value object conversion patterns
  - 652 lines with multi-context orchestration

**Updated Examples**:
- `domains/ux/examples/partitioned/interaction-example.yaml`
  - Added `api_endpoints` references to components
  - Added `application_service` references to workflows

#### Documentation

**New Documents**:
- `RESEARCH_QUESTIONS_ANSWERED.md` - Definitive answers to 10 critical research questions
- `domains/ddd/docs/ddd-07-application-layer.md` - Application Layer documentation
- `domains/ddd/docs/ddd-08-bff-pattern.md` - BFF Pattern documentation

**Research Artifacts**:
- `grounding-relationships.yaml` - 10 new grounding relationships
- `BFF_ApplicationService_CQRS_Research.md` - Research analysis
- `GROUNDING_CHAIN_DIAGRAM.md` - Complete grounding chain visualization
- `QUICK_REFERENCE_GROUNDINGS.md` - Quick reference guide

#### Grounding Relationships

**New Groundings (10)**:
1. `grounding_ux_bff_001` - UX Component → BFF Interface (structural, strong)
2. `grounding_bff_app_svc_001` - BFF Interface → Application Service (structural, strong)
3. `grounding_bff_cmd_001` - BFF Interface → Command (procedural, strong)
4. `grounding_bff_qry_001` - BFF Interface → Query (procedural, strong)
5. `grounding_app_svc_cmd_001` - Application Service → Command (structural, strong)
6. `grounding_app_svc_qry_001` - Application Service → Query (structural, strong)
7. `grounding_cmd_agg_001` - Command → Aggregate (structural, strong)
8. `grounding_qry_agg_001` - Query → Aggregate (structural, strong)
9. `grounding_app_svc_repo_001` - Application Service → Repository (structural, strong)
10. `grounding_app_svc_evt_001` - Application Service → Domain Event (procedural, strong)

**Updated Interdomain Map**:
- `research-output/interdomain-map.yaml` v2.2.0 → v2.3.0
- Total groundings: 32 → 42 (+10)
- Closure percentages maintained: DDD 100%, UX 100%, Data-Eng 100%

### Changed

#### Breaking Changes
None. This is a **minor version** release with backward-compatible additions.

#### Schema Evolution
- DDD core concepts expanded from 10 to 14 concepts
- Added partitioning metadata to document schema organization
- Updated best practices with CQRS and BFF patterns

#### Naming Conventions
Added new ID patterns:
- `svc_app_<name>` for application services
- `cmd_<name>` for command interfaces
- `qry_<name>` for query interfaces
- `bff_<client_type>` for BFF scopes
- `bff_if_<context>_<client_type>` for BFF interfaces

### Fixed
- Clarified relationship between BFF and API Gateway (hybrid pattern)
- Resolved ambiguity on transaction boundaries (single aggregate rule)
- Defined clear grounding path from UX to Aggregate

### Validation

**Closure Percentages**:
- DDD: 100% (was 100%, maintained)
- UX: 100% (was 100%, maintained)
- Data-Eng: 100% (unchanged)
- QE: 75% (unchanged)
- Agile: 72% (unchanged)

**Grounding Distribution**:
- Structural: 9 → 16 (+7)
- Semantic: 9 (unchanged)
- Procedural: 6 → 13 (+7)
- Epistemic: 5 (unchanged)

**Strength Distribution**:
- Strong: 27 → 37 (+10)
- Weak: 5 (unchanged)

### Migration Guide
See `domains/ddd/MIGRATION-v1.1.md` for detailed migration instructions.

---

## [1.0.0] - 2025-10-13

### Added
- Initial release of Canonical Grounding framework
- 5 canonical domain models (DDD, Data-Eng, UX, QE, Agile)
- 32 grounding relationships
- Foundation schemas for all domains
- Interdomain dependency map v2.2.0

---

## Version Format

Format: `[Major.Minor.Patch]`

- **Major**: Breaking changes to schemas or groundings
- **Minor**: New features, concepts, or groundings (backward compatible)
- **Patch**: Bug fixes, clarifications, documentation updates

---

## Links

- Repository: https://github.com/igormusic/canonical-grounding
- Documentation: /docs/
- Examples: /domains/*/examples/
- Schemas: /domains/*/schemas/
