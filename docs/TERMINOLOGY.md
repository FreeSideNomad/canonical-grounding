# Terminology Guide

**Version:** 2.0
**Date:** 2025-10-14
**Purpose:** Quick reference for canonical domain model grounding terminology

---

## Core Concepts

### Canonical Domain Model

A formally specified, authoritative representation of knowledge within a specific domain. Each model is defined using YAML or JSON Schema and contains concepts, relationships, and constraints.

**Key Properties:**
- **Canonical**: Authoritative reference within its domain
- **Domain**: Knowledge domain (NOT DDD bounded context)
- **Model**: Formal specification with explicit semantics

**Examples:**
- **DDD Canonical Model**: Authoritative model of Domain-Driven Design concepts (Aggregate, Entity, BoundedContext, etc.)
- **QE Canonical Model**: Authoritative model of Quality Engineering concepts (TestCase, TestStrategy, ContractTest, etc.)
- **UX Canonical Model**: Authoritative model of User Experience concepts (Page, Workflow, Component, etc.)
- **Data-Eng Canonical Model**: Authoritative model of Data Engineering concepts (Pipeline, Dataset, Contract, etc.)
- **Agile Canonical Model**: Authoritative model of Agile methodology concepts (Feature, Story, Sprint, etc.)

### Knowledge Domain

The scope of knowledge represented by a canonical model. This is distinct from DDD's concept of "domain" (business problem space).

**Knowledge Domains (our usage):**
- Domain-Driven Design (DDD knowledge)
- Quality Engineering (QE knowledge)
- User Experience (UX knowledge)
- Data Engineering (Data-Eng knowledge)
- Agile Methodology (Agile knowledge)

**NOT Knowledge Domains:**
- "Order Management" (that's a DDD bounded context)
- "Customer Relations" (that's a business domain)
- "Inventory" (that's a business subdomain)

### Grounding Relationship

An explicit, typed dependency between concepts in different canonical models. Groundings make cross-domain references formal and machine-verifiable.

**Grounding Types:**
- **Structural**: Direct field references (e.g., `ux:Page.bounded_context_ref → ddd:BoundedContext`)
- **Semantic**: Meaning alignment (e.g., `ux:Navigation` aligns with `ddd:Domain` structure)
- **Procedural**: Process dependencies (e.g., `qe:Test` validates `ddd:Aggregate.invariants`)
- **Epistemic**: Knowledge coordination (e.g., `agile:Feature` maps to `ddd:BoundedContext`)

**Example:**
```yaml
- id: "grounding_ux_ddd_001"
  source: "model_ux"
  target: "model_ddd"
  type: "structural"
  strength: "strong"
  relationships:
    - source_concept: "ux:Page"
      target_concept: "ddd:BoundedContext"
      reference_field: "bounded_context_ref"
      validation: "required"
```

### Model Closure

Percentage of all references (internal + external) that are explicitly resolved through grounding relationships or internal definitions.

**Formula:**
```
Closure = (Internal Concepts + Grounded External Refs) / (Internal Concepts + Total External Refs) × 100%
```

**Example:**
- UX Model: 11 internal concepts + 1 external reference (to DDD)
- External reference is grounded: `ux:Page → ddd:BoundedContext`
- Closure: (11 + 1) / (11 + 1) = 12/12 = **100%**

**Target:** >95% closure for production readiness

**Status:** All 5 canonical models achieve 100% closure ✅

---

## The Five Canonical Domain Models

### 1. DDD Canonical Model (Foundation)
- **Layer:** Foundation
- **Concepts:** 13
- **External Dependencies:** 0
- **Closure:** 100%
- **Purpose:** Defines strategic and tactical patterns for domain modeling

**Key Concepts:** Domain, BoundedContext, Aggregate, Entity, ValueObject, Repository, DomainService, ApplicationService, DomainEvent, Factory, Specification, ContextMapping

### 2. Data-Eng Canonical Model (Foundation)
- **Layer:** Foundation
- **Concepts:** 14
- **External Dependencies:** 0
- **Closure:** 100%
- **Purpose:** Defines data pipeline, quality, and governance patterns

**Key Concepts:** System, Domain, Pipeline, Stage, Transform, Dataset, Contract, Check, Lineage, Governance, Schema, QualityRule

### 3. UX Canonical Model (Derived)
- **Layer:** Derived
- **Concepts:** 12 (11 internal + 1 external)
- **External Dependencies:** DDD, Data-Eng
- **Closure:** 100%
- **Purpose:** Defines user interface and interaction patterns

**Key Concepts:** InformationArchitecture, Navigation, Workflow, Page, Component, PageSection, Behavior, PaginationConfig, CachingConfig, AccessibilitySpec, DesignTokens

### 4. QE Canonical Model (Derived)
- **Layer:** Derived
- **Concepts:** 18 (12 internal + 6 external)
- **External Dependencies:** DDD, UX, Data-Eng
- **Closure:** 100%
- **Purpose:** Defines testing and quality assurance patterns

**Key Concepts:** TestSuite, TestCase, ContractTest, TestData, TestScenario, TestAutomation, TestStrategy, TestExecutionPlan, Defect, TestMetrics, TestEnvironment, QualityCharacteristics

### 5. Agile Canonical Model (Meta)
- **Layer:** Meta
- **Concepts:** 28 (21 internal + 7 external)
- **External Dependencies:** DDD, UX, QE, Data-Eng
- **Closure:** 100%
- **Purpose:** Defines work organization and coordination patterns

**Key Concepts:** Product, Vision, Roadmap, Epic, Capability, Feature, UserStory, Task, Bug, Spike, Sprint, PI, Release, Team, ART, BusinessOwner, ProductOwner, ScrumMaster, ReleaseTrainEngineer, SystemArchitect, Velocity

---

## Historical Note

### Version 1.0 → Version 2.0 Terminology Change

**Previous Terminology (v1.0):**
- "Canon" to refer to each domain model
- "Five Canons" system
- "Canon closure", "Canon-to-canon grounding"
- IDs: `canon_ddd`, `canon_qe`, etc.

**Current Terminology (v2.0):**
- "Canonical Domain Model" (or "Canonical Model")
- "Five Canonical Domain Models" system
- "Model closure", "Cross-domain model grounding"
- IDs: `model_ddd`, `model_qe`, etc.

**Rationale for Change:**
1. **More Accurate:** "Model" explicitly states what it is
2. **Less Ambiguous:** Avoids religious/literary connotation of "canon"
3. **Clearer:** "Domain model" clarifies scope (knowledge domain)
4. **Consistent:** Aligns research terminology with implementation

**Impact:**
- ✅ No changes to research findings or empirical data
- ✅ No changes to mathematical properties or proofs
- ✅ No changes to implementation schemas (only comments)
- ✅ All grounding relationships remain identical
- ✅ 100% closure maintained across all models

---

## Quick Reference

### Common Terms

| Term | Definition |
|------|------------|
| **Canonical Domain Model** | Formally specified authoritative knowledge representation |
| **Knowledge Domain** | Scope of expertise (DDD knowledge, QE knowledge, etc.) |
| **Grounding** | Explicit cross-domain dependency |
| **Model Closure** | Percentage of references that are resolved |
| **Foundation Model** | No external dependencies (DDD, Data-Eng) |
| **Derived Model** | Depends on foundation models (UX, QE) |
| **Meta Model** | Coordinates all other models (Agile) |

### File Locations

| Model | Schema File |
|-------|-------------|
| DDD | `domains/ddd/model-schema.yaml` |
| Data-Eng | `domains/data-eng/model.schema.yaml` |
| UX | `domains/ux/model-schema.yaml` |
| QE | `domains/qe/model-schema.yaml` |
| Agile | `domains/agile/model.schema.yaml` |

**Grounding Map:** `research-output/interdomain-map.yaml`
**Validation Tool:** `tools/validate-schemas.py`
**Graph Generator:** `tools/generate-grounding-graph.py`

### Validation Status

```
✓ All schemas valid
✓ System closure: 100.0% (target: >95%)
✓ All groundings valid (19 relationships, 30 concept pairs)
✓ No circular dependencies
✓ PRODUCTION READY
```

---

## For Developers

### Using Canonical Models in Code

**Load relevant models:**
```python
# Load models relevant to your task
models = load_models(['ddd', 'ux', 'qe'])

# Validate cross-domain references
validate_groundings(models, interdomain_map)
```

**Reference concepts:**
```
Format: <model>:<Concept>:[id]

Examples:
- ddd:BoundedContext:bc_order_management
- ux:Page:page_checkout
- qe:TestCase:tc_unit_001_email_validation
- data-eng:Pipeline:pipeline_customer_etl
- agile:Feature:feat_payment_integration
```

### Validation Commands

```bash
# Validate all schemas and calculate closure
cd tools
./run-validation.sh

# Generate grounding graph
python generate-grounding-graph.py
dot -Tsvg ../grounding-graph.dot -o ../grounding-graph.svg
```

---

## For Researchers

### Citing This Work

When referencing this system in academic work:

**v2.0 (Current):**
> "We use canonical domain models with explicit cross-domain grounding relationships..."

**v1.0 (Legacy):**
> "Earlier versions of this work used 'canon' terminology (v1.0), now updated to 'canonical domain model' (v2.0) for clarity."

### Key Publications

- **Theoretical Foundation:** `research-output/canonical-grounding-theory.md`
- **Complete Synthesis:** `research-output/final-synthesis.md`
- **Grounding Analysis:** `GROUNDING-REPORT.md`
- **Terminology Alignment:** `research-output/terminology-alignment.md`

---

## Support

- **Issues:** https://github.com/FreeSideNomad/canonical-grounding/issues
- **Documentation:** `research-output/README.md`
- **Migration Guide:** `research-output/terminology-alignment.md`

---

**Last Updated:** 2025-10-14
**Version:** 2.0
**Status:** Production Ready ✅
