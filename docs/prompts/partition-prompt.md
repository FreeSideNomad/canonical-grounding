# Partition Prompt: Schema and Example File Organization Strategy

## Context

The canonical grounding project has grown to include complex domain models with large YAML schemas and example files. The DDD (Domain-Driven Design) model, in particular, contains both strategic patterns (domains, bounded contexts, context maps) and tactical patterns (aggregates, entities, value objects, repositories, domain services).

Currently:
- Single monolithic schema file: `domains/ddd/model-schema.yaml`
- Single monolithic example file: `domains/ddd/examples/model-example.yaml`
- Schema validation works via: `tools/validate-schemas.py` using `jsonschema` library
- Cross-domain grounding references maintained in: `research-output/interdomain-map.yaml`

## Problem Statement

Large monolithic files create several challenges:

1. **Cognitive Load**: Files with 500+ lines are difficult to navigate and understand
2. **Maintenance**: Changes to one pattern require loading entire file
3. **Reusability**: Cannot easily reference just strategic or just tactical patterns
4. **Collaboration**: Multiple people editing same large file causes merge conflicts
5. **Learning Curve**: New users overwhelmed by size and complexity

## Desired Outcome

**Goal**: Partition the DDD model (and potentially other large domain models) into logical, manageable pieces while maintaining:

- ✅ Schema validation integrity (all references resolve correctly)
- ✅ Cross-domain grounding relationships (other domains can still reference DDD concepts)
- ✅ Documentation alignment (docs still map to schema concepts)
- ✅ Tool compatibility (existing validation tools continue to work)

### Specific Example: DDD Partition

**Strategic Model** (`strategic-ddd-schema.yaml` + `strategic-ddd-example.yaml`):
- Domain
- Subdomain (Core, Supporting, Generic)
- BoundedContext
- ContextMap
- ContextMapRelationship (SharedKernel, CustomerSupplier, Conformist, etc.)
- UbiquitousLanguage

**Tactical Model** (`tactical-ddd-schema.yaml` + `tactical-ddd-example.yaml`):
- Aggregate
- Entity
- ValueObject
- Repository
- DomainService
- DomainEvent
- Invariant

**Cross-Partition References**:
- Tactical patterns reference BoundedContext from strategic model
- Context maps reference BoundedContexts
- Aggregates belong to BoundedContexts

## Research Questions

### 1. Schema Partitioning Strategies

**Question**: What are industry best practices for partitioning large JSON Schema / YAML schema files?

Research areas:
- JSON Schema composition: `$ref`, `$defs`, `allOf`, `anyOf`
- External schema references: `$ref: "./other-schema.yaml#/definitions/Concept"`
- Schema bundling vs. splitting
- OpenAPI schema organization patterns
- Kubernetes CRD multi-file strategies

**Desired output**:
- Recommend 2-3 partitioning strategies with pros/cons
- Show concrete examples of how to split schemas with references
- Explain validation implications for each approach

### 2. Referential Integrity Maintenance

**Question**: How do we maintain referential integrity across partitioned schemas?

Scenarios to address:
- Tactical model references `BoundedContext` from strategic model
- Cross-domain groundings (e.g., UX Page → DDD BoundedContext) still work
- Validation tools can resolve references across files
- Documentation tooling can find concepts across partitions

**Desired output**:
- Explain how `$ref` resolution works across files
- Show how to validate multi-file schemas with `jsonschema` library
- Provide patterns for "anchor" concepts that multiple files reference
- Address circular dependency risks

### 3. File Organization Patterns

**Question**: What directory structure best supports partitioned schemas?

Options to evaluate:
```
Option A: Flat with prefixes
domains/ddd/
  strategic-ddd-schema.yaml
  tactical-ddd-schema.yaml
  strategic-ddd-example.yaml
  tactical-ddd-example.yaml

Option B: Nested by concern
domains/ddd/
  strategic/
    schema.yaml
    example.yaml
  tactical/
    schema.yaml
    example.yaml

Option C: Schema bundler approach
domains/ddd/
  schemas/
    strategic.yaml
    tactical.yaml
    index.yaml  # Combines all schemas
  examples/
    strategic-example.yaml
    tactical-example.yaml
```

**Desired output**:
- Recommend file organization with justification
- Show how validation tools discover schemas
- Explain impact on grounding references
- Consider future expansion (adding more partitions)

### 4. Validation Tool Updates

**Question**: What changes are needed to existing validation tools?

Current tools to consider:
- `tools/validate-schemas.py` - JSON Schema validation
- `tools/validate-grounding-references.py` - Cross-domain reference validation
- `tools/validate-schema-docs-alignment.py` - Schema-documentation alignment
- `tools/validate-example.py` - Example validation against schema

**Desired output**:
- Identify which tools need modification
- Show code changes needed for multi-file schema support
- Explain how to resolve `$ref` across files in Python
- Provide validation strategy (validate individually vs. as bundle)

### 5. Backward Compatibility

**Question**: How do we maintain backward compatibility during transition?

Considerations:
- Existing grounding references in `interdomain-map.yaml` use paths like `ddd:BoundedContext`
- Documentation references concepts by name
- External consumers may depend on current schema structure

**Desired output**:
- Migration strategy (parallel schemas vs. hard cutover)
- Path resolution strategy (do paths change? e.g., `ddd:strategic:BoundedContext`?)
- Deprecation timeline if breaking changes needed
- Testing strategy to ensure no regressions

### 6. Other Domain Models

**Question**: Which other domain models would benefit from partitioning?

Review:
- `domains/agile/model.schema.yaml` (~1700 lines) - Candidate for partition?
- `domains/qe/model-schema.yaml` (~800 lines) - Manageable size?
- `domains/ux/model-schema.yaml` (~600 lines) - Manageable size?
- `domains/data-eng/model.schema.yaml` (~350 lines) - Fine as-is?

**Desired output**:
- Size threshold recommendation (>500 lines = partition?)
- Identify natural partition boundaries for Agile model
- Generalize DDD partitioning approach to other domains

## Success Criteria

The research and resulting implementation should:

1. ✅ **Reduce file sizes** - No single schema or example file >400 lines
2. ✅ **Maintain validation** - All existing validation passes without modification to validation logic
3. ✅ **Preserve grounding** - Cross-domain references resolve correctly
4. ✅ **Keep tool compatibility** - Existing Python tools work with minimal changes
5. ✅ **Clear documentation** - Partition rationale and structure documented
6. ✅ **Extensible pattern** - Can apply same approach to other domains

## Deliverables

1. **Research Document** (`partition-research.md`):
   - Summary of industry best practices
   - Recommended partitioning strategy with justification
   - File organization pattern
   - Code examples for validation

2. **Partition Plan** (`partition-plan.md`):
   - Step-by-step migration plan for DDD model
   - File structure before/after
   - Tool modification checklist
   - Testing strategy

3. **Implementation Example**:
   - Partitioned DDD schema (strategic + tactical)
   - Partitioned DDD examples
   - Updated validation tools (if needed)
   - Proof that all validations still pass

4. **Documentation Updates**:
   - Update `README.md` to explain partition approach
   - Update tool documentation with multi-file schema usage
   - Add ADR (Architecture Decision Record) explaining partition decision

## Constraints

- Must work with JSON Schema 2020-12 specification
- Must be compatible with Python `jsonschema` library (version 4.x)
- Must not break existing grounding references in `research-output/interdomain-map.yaml`
- Should minimize changes to documentation files in `domains/*/docs/`
- Should follow industry standards (prefer widely-used patterns over custom solutions)

## Resources

Relevant existing files:
- `domains/ddd/model-schema.yaml` - Current monolithic DDD schema (~600 lines)
- `tools/validate-schemas.py` - Current validation tool
- `research-output/interdomain-map.yaml` - Grounding relationships
- JSON Schema 2020-12 specification: https://json-schema.org/specification.html

## Task for AI Assistant

Please conduct thorough research on the questions above and produce:

1. A comprehensive research document answering all 6 research questions
2. A concrete recommendation for partitioning strategy
3. A detailed partition plan for the DDD model
4. Code examples showing:
   - How to structure partitioned schemas with `$ref`
   - How to validate multi-file schemas in Python
   - Any necessary tool modifications

The research should prioritize **practical, proven patterns** over theoretical approaches. Include real-world examples from popular projects (Kubernetes, OpenAPI, etc.) where applicable.

Focus on creating a **repeatable pattern** that can be applied to other domain models beyond just DDD.

---

**Created**: 2025-10-17
**Purpose**: Guide research and implementation of schema/example file partitioning strategy
**Status**: Ready for research phase
