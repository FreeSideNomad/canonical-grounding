# Terminology Alignment Document

**Date:** 2025-10-14
**Version:** 2.0
**Purpose:** Clarify terminology shift from "canon" to "canonical domain model"

---

## Overview

This document maps the terminology evolution in the Canonical Grounding research and implementation. The original research used **"canon"** as a metaphor borrowed from religious/literary tradition to emphasize authority and consistency. However, the actual implementation uses **"canonical domain models"** - formal models representing authoritative knowledge in specific knowledge domains.

This alignment improves clarity, reduces ambiguity, and ensures research terminology matches implementation.

---

## Terminology Mapping

### Primary Term Changes

| Old Term | New Term | Context |
|----------|----------|---------|
| **Canon** | **Canonical Domain Model** | When referring to implementation, schemas, or formal specifications |
| **Canon [Name]** | **[Name] Canonical Model** | Short form (e.g., "DDD Canonical Model") |
| **Canon [Name]** | **[Name] Knowledge Domain Model** | Long form emphasizing domain scope |
| **Canon closure** | **Model closure** or **Domain model closure** | Mathematical property |
| **Canon coherence** | **Model coherence** | Internal consistency property |
| **Canon ontology** | **Domain model ontology** | Graph of models |
| **Inter-canon grounding** | **Cross-domain model grounding** | Relationships between models |
| **Canon-to-canon** | **Model-to-model** | Direct relationships |
| **Five Canons** | **Five Canonical Domain Models** | The complete system |

### Preserved Terms

These terms remain unchanged as they are conceptually accurate:

- **Grounding** - philosophical concept of establishing connections
- **Ontology** - graph structure of models and relationships
- **Closure** - mathematical property (percentage of resolved references)
- **Coherence** - internal consistency
- **Canonical** - authoritative, formally specified
- **Schema** - YAML/JSON Schema implementation files

### Context-Dependent Usage

**Use "Canon"** when:
- Citing historical/philosophical sources (Aristotle, Kant, etc.)
- Referencing academic literature using this term
- Making metaphorical comparisons (e.g., "like religious canons")
- Discussing the etymology or conceptual origins

**Use "Canonical Domain Model"** when:
- Referring to implementation (YAML files, schemas)
- Describing technical architecture
- Explaining formal definitions
- Writing specification documents
- Generating validation reports

---

## Concept Clarifications

### What is a Canonical Domain Model?

**Definition:** A formally specified, internally consistent collection of concepts, relationships, and constraints representing authoritative knowledge within a specific knowledge domain.

**Key Properties:**
1. **Canonical** = Authoritative reference within its domain
2. **Domain** = Knowledge domain (NOT DDD bounded context)
3. **Model** = Formal specification (YAML/JSON Schema)

**Example:**
- **DDD Canonical Model** is the authoritative model of Domain-Driven Design concepts (Aggregate, Entity, BoundedContext, etc.)
- It represents the **DDD knowledge domain** (what DDD practitioners know)
- NOT a "DDD bounded context" (that's something the DDD model defines)

### Knowledge Domain vs. DDD Domain

**Knowledge Domain (our usage):**
- Scope of expertise: DDD knowledge, QE knowledge, UX knowledge
- Abstract: concepts, patterns, terminology
- Example: "Quality Engineering" as a field of knowledge

**DDD Domain (DDD concept):**
- Business problem space: Order Management, Inventory, etc.
- Concrete: business rules, workflows, entities
- Example: "Order Management Domain" in an e-commerce system

**The Five Knowledge Domains:**
1. **Domain-Driven Design** - Strategic and tactical patterns
2. **Data Engineering** - Schemas, pipelines, quality rules
3. **User Experience** - Information architecture, workflows, components
4. **Quality Engineering** - Test strategies, contracts, metrics
5. **Agile Methodology** - Features, sprints, stories, velocity

---

## Specific Terminology Examples

### Research Documents

**Before (v1.0):**
> "Each canon is a formally specified domain model with explicit closure properties."

**After (v2.0):**
> "Each canonical domain model is a formally specified representation of authoritative knowledge within a knowledge domain, with explicit closure properties."

---

**Before:**
> "The DDD Canon defines strategic and tactical patterns."

**After:**
> "The DDD Canonical Model defines strategic and tactical patterns from Domain-Driven Design."

---

**Before:**
> "Canon-to-canon groundings establish semantic dependencies."

**After:**
> "Cross-domain model groundings establish semantic dependencies between canonical models."

### Technical Documentation

**Before:**
```yaml
canons:
  - id: "canon_ddd"
    name: "DDD Canon"
```

**After:**
```yaml
canonical_models:
  - id: "model_ddd"
    name: "DDD Canonical Domain Model"
    knowledge_domain: "Domain-Driven Design"
```

### Mathematical Notation

**Before:**
- Κ (Kappa) = Canon
- C = {c₁, c₂, ..., cₙ} where c = canon

**After:**
- M (Model) or DM (Domain Model)
- M = {m₁, m₂, ..., mₙ} where m = canonical model
- Or preserve C but note C represents "canonical model collection"

---

## Rationale for Change

### 1. Accuracy
- **Old:** "Canon" implies religious/literary authority
- **New:** "Canonical domain model" explicitly states it's a formal model

### 2. Clarity
- **Old:** Ambiguous - "canon of what?"
- **New:** Clear - model of a knowledge domain

### 3. Consistency
- **Old:** Research used "canon", implementation used "model"
- **New:** Aligned terminology throughout

### 4. Professionalism
- **Old:** Metaphorical term might confuse non-native speakers
- **New:** Technical term with precise meaning

### 5. Searchability
- **Old:** "Canon" has many unrelated meanings
- **New:** "Canonical domain model" is unique and specific

---

## Migration Path

### For Documentation Authors

When updating documents:

1. **Search and Replace with Context:**
   - Find: "canon" (case-insensitive)
   - Replace with appropriate term based on context
   - Don't auto-replace in citations or quotes

2. **Check These Phrases:**
   - "five canons" → "five canonical domain models"
   - "canon schema" → "domain model schema"
   - "canon closure" → "model closure"
   - "inter-canon" → "cross-domain model"

3. **Preserve Historical Context:**
   - Keep "canon" in quotes when citing sources
   - Add footnotes explaining terminology evolution

### For Code Maintainers

When updating code:

1. **Variable Names:**
   - `canon_schemas` → `domain_model_schemas` (or keep with comment)
   - `canon_key` → `model_key`
   - Can keep old names for backward compatibility

2. **Output Messages:**
   - "Loading Canon Schemas" → "Loading Canonical Domain Model Schemas"
   - "Canon Validation" → "Domain Model Validation"

3. **File Names:**
   - Keep existing file names (breaking change)
   - Update comments and documentation

### For Readers of v1.0 Research

- Wherever you see "canon" in v1.0, read "canonical domain model" in v2.0
- All findings, metrics, and conclusions remain identical
- This is clarification, not methodology change

---

## Impact Analysis

### What Changed
✅ Terminology in documentation
✅ Variable names in tools (optional)
✅ Output messages and reports
✅ Field names in YAML files (with backward compat)

### What Didn't Change
✅ Mathematical properties and proofs
✅ Empirical data and measurements
✅ Research findings and conclusions
✅ Schema structures (only comments)
✅ Grounding relationships (still 30)
✅ Closure calculations (still 100%)

### Breaking Changes
❌ None - this is a non-breaking terminology alignment

---

## Terminology Standards Summary

**Use consistently:**
- Canonical Domain Model (full form)
- Canonical Model (short form in context)
- Domain Model (when "canonical" is implied)
- Cross-domain grounding (between models)
- Model closure (mathematical property)

**Avoid:**
- "Canon" in technical/implementation contexts
- Mixing "canon" and "model" inconsistently
- Using "domain" without clarifying knowledge vs. business

**Preserve:**
- "Canon" in historical/philosophical citations
- "Canonical" as adjective (authoritative)
- "Grounding" for relationships

---

## References

- Original research: v1.0 (2025-10-04) used "canon" terminology
- Implementation: Always used "model" in schemas
- This alignment: v2.0 (2025-10-14) unified terminology

---

**Status:** ✅ Approved for implementation
**Next Steps:** Update all research documents following this mapping
