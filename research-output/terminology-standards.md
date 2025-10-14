# Terminology Standards

**Date:** 2025-10-14
**Version:** 1.0
**Purpose:** Define standards for consistent terminology usage across research documentation

---

## Overview

This document establishes clear standards for when to use specific terminology in the Canonical Grounding research. Following these standards ensures consistency, clarity, and accuracy across all documentation.

---

## Core Terminology Standards

### 1. When to Use "Canon"

Use "canon" ONLY in these contexts:

**Historical/Philosophical Context:**
- When citing historical sources (Aristotle, Kant, biblical canon, etc.)
- When referencing academic literature that uses "canon" terminology
- When discussing etymology or conceptual origins
- When making explicit metaphorical comparisons

**Examples:**
- "The biblical canon established a closed set of authoritative texts"
- "Aristotle's canonical texts on logic..."
- "Like a religious canon, our models establish authority..."

**NOT for:**
- Technical implementation discussions
- Formal definitions in our research
- Schema or YAML file references
- System architecture descriptions

### 2. When to Use "Canonical Domain Model"

Use "canonical domain model" (full form) in these contexts:

**Formal Definitions:**
- First mention in a section or document
- Defining what the system consists of
- Mathematical notation introductions
- Specification documents

**Examples:**
- "A canonical domain model is a formally specified, internally consistent collection..."
- "The five canonical domain models form the ontology..."
- "Each canonical domain model (M) represents authoritative knowledge..."

**Technical Implementation:**
- Referring to YAML/JSON Schema files
- Describing system architecture
- Implementation specifications
- Validation and grounding discussions

**Examples:**
- "The DDD Canonical Domain Model is defined in `canon-ddd.yaml`"
- "Canonical domain models achieve 100% closure through explicit grounding"
- "Load all canonical domain model schemas before validation"

### 3. When to Use "Canonical Model" (Short Form)

Use "canonical model" when the context is clear:

**In-Context Usage:**
- After full form has been introduced in section
- When referring to a specific model by name (e.g., "DDD Canonical Model")
- In tables, diagrams, and figures where space is limited
- When alternating with full form to avoid repetition

**Examples:**
- "The DDD Canonical Model defines strategic patterns..."
- "Each canonical model has explicit closure properties..."
- "Cross-domain model groundings connect canonical models..."

### 4. When to Use "Domain Model" or "Model"

Use "model" alone when the canonical nature is strongly implied:

**Contextual Abbreviation:**
- After establishing "canonical domain model" or "canonical model" in context
- In technical discussions where all models are canonical
- In code comments and variable names
- When discussing model properties that apply to all types

**Examples:**
- "The model achieves 100% closure..." (when discussing canonical models)
- "Model-to-model grounding relationships..." (clearly canonical models)
- `domain_model_schemas = load_models()` (code variable)

**Avoid:**
- Using "model" without prior context (ambiguous)
- Using "domain model" when it could mean DDD domain model vs. canonical model

### 5. When to Use "Knowledge Domain"

Use "knowledge domain" to describe the scope of what a model represents:

**Scope Description:**
- Explaining what each canonical model covers
- Distinguishing from DDD's "domain" concept (business domain)
- Describing the five domains in the system

**Examples:**
- "The DDD knowledge domain includes strategic and tactical patterns..."
- "Each canonical domain model represents a specific knowledge domain"
- "Five knowledge domains: DDD, Data Engineering, UX, QE, Agile"

**NOT:**
- "Business domain" (that's a DDD concept the models might describe)
- "Problem domain" (that's what DDD domains solve)
- Just "domain" without qualifier (ambiguous)

---

## Compound Terms and Phrases

### Model Properties

| Old Term | New Standard Term | Usage Context |
|----------|-------------------|---------------|
| Canon closure | Model closure | Mathematical property |
| Canon coherence | Model coherence | Internal consistency |
| Canon completeness | Model completeness | Coverage metric |
| Canon ontology | Domain model ontology | Graph structure |

### Relationships

| Old Term | New Standard Term | Usage Context |
|----------|-------------------|---------------|
| Canon-to-canon grounding | Cross-domain model grounding | Between models |
| Inter-canon grounding | Cross-domain grounding | Between models |
| Canon-to-canon relationship | Model-to-model relationship | Direct connection |
| Canon dependency | Model dependency | Semantic dependency |

### System References

| Old Term | New Standard Term | Usage Context |
|----------|-------------------|---------------|
| Five canons | Five canonical domain models | Full form |
| The five canons | The five canonical models | Short form |
| Canon system | Canonical model system | System architecture |
| Canon schema | Domain model schema | YAML/JSON files |

### Specific Models

| Old Term | New Standard Term | Notes |
|----------|-------------------|-------|
| DDD Canon | DDD Canonical Model | Or "DDD Canonical Domain Model" |
| QE Canon | QE Canonical Model | Quality Engineering model |
| UX Canon | UX Canonical Model | User Experience model |
| Data-Eng Canon | Data-Eng Canonical Model | Data Engineering model |
| Agile Canon | Agile Canonical Model | Agile Methodology model |

---

## Mathematical Notation Standards

### Variable Names

**Primary Notation:**
- **M** = Canonical Domain Model (singular)
- **M** = {m₁, m₂, ..., mₙ} = Set of canonical models
- **m** = Individual canonical model
- **G** = Grounding relationship
- **C** = Closure (as percentage)

**Alternative Notation (if needed):**
- **DM** = Domain Model (when M could be ambiguous)
- **CDM** = Canonical Domain Model (full form)

**Deprecated (do not use):**
- **Κ** (Kappa) = Old notation for canon
- **C** for canon collection (conflicts with Closure)

### Set Notation

**Standard:**
```
M = {m₁, m₂, m₃, m₄, m₅}
where:
  m₁ = DDD Canonical Model
  m₂ = Data-Eng Canonical Model
  m₃ = UX Canonical Model
  m₄ = QE Canonical Model
  m₅ = Agile Canonical Model
```

**In Formulas:**
```
Closure(m) = |Grounded(m)| / |Total(m)| × 100%
where m ∈ M (m is a canonical model in the set of all models)
```

---

## Section Headings Standards

### Document Titles

**Standard Form:**
- "Canonical Grounding Theory"
- "Canonical Domain Model Specifications"
- "Cross-Domain Model Grounding Analysis"

**Avoid:**
- "Canon Theory" (too informal)
- "Canon Specifications" (outdated terminology)

### Section Headings

**Primary Heading Patterns:**
- "What is a Canonical Domain Model?"
- "Canonical Model Properties"
- "Cross-Domain Model Grounding Types"
- "Model Closure Calculation"

**Secondary Heading Patterns:**
- "DDD Canonical Model"
- "Model Coherence Requirements"
- "Grounding Relationship Types"

---

## Code and Implementation Standards

### Variable Naming

**Python/Script Variables:**
```python
# Preferred
canonical_models = load_models()
domain_model_schemas = read_schemas()
model_closure = calculate_closure(model)
cross_domain_groundings = get_groundings()

# Acceptable (with comments)
canon_schemas = load_schemas()  # Canonical domain model schemas
models = load_models()  # When context is clear

# Avoid
canons = load()  # Ambiguous
c = load()  # Too terse
```

### YAML/JSON Fields

**Standard Field Names:**
```yaml
canonical_models:
  - id: "model_ddd"
    name: "DDD Canonical Domain Model"
    short_name: "DDD Canonical Model"
    knowledge_domain: "Domain-Driven Design"

groundings:
  - id: "grounding_ddd_qe_001"
    source_model: "model_ddd"
    target_model: "model_qe"
    grounding_type: "structural"
```

### Output Messages

**Standard Messages:**
```
Loading canonical domain model schemas...
Validating model closure...
Calculating cross-domain groundings...
Model validation complete: 100% closure achieved
```

**Avoid:**
```
Loading canons...  # Old terminology
Checking canon closure...  # Update to "model"
```

---

## Context-Dependent Examples

### Example 1: Research Document Introduction

**Correct:**
> This research introduces Canonical Grounding, a meta-framework for establishing explicit semantic dependencies between canonical domain models. Each canonical domain model (M) is a formally specified, internally consistent representation of authoritative knowledge within a specific knowledge domain. The framework defines five canonical models covering DDD, Data Engineering, UX, Quality Engineering, and Agile domains.

**Why:** First mention uses full form, then abbreviates to "canonical domain model" and "canonical models" in context.

### Example 2: Technical Implementation

**Correct:**
> The validation tool loads all domain model schemas and calculates closure for each model. Cross-domain model groundings are verified to ensure all external references are explicitly defined. The system achieves 100% model closure through 30 grounding relationships.

**Why:** Context is technical implementation, uses "model" consistently after establishing canonical nature.

### Example 3: Formal Definition

**Correct:**
> **Definition 1 (Canonical Domain Model):** A canonical domain model M is a 4-tuple (C, R, P, G) where:
> - C is the set of concepts in the model
> - R is the set of relationships within the model
> - P is the set of properties and constraints
> - G is the set of groundings to external models

**Why:** Formal definition uses full term, then abbreviates to M in mathematical notation.

### Example 4: Historical Context

**Correct:**
> Like a religious canon that establishes authoritative scripture, canonical domain models establish authoritative specifications. However, unlike historical canons which evolved organically, our canonical models are explicitly designed and formally specified.

**Why:** Uses "canon" appropriately in metaphorical comparison, then switches to "canonical domain models" for our system.

---

## Quality Checklist

Before finalizing any document, verify:

### Terminology Consistency
- [ ] "Canon" only used in historical/metaphorical contexts
- [ ] "Canonical domain model" used for formal definitions
- [ ] "Canonical model" used appropriately in context
- [ ] "Model" abbreviation only used when context is clear
- [ ] "Knowledge domain" used to describe scope

### Technical Accuracy
- [ ] Mathematical notation uses M (not Κ)
- [ ] Variable names follow standards
- [ ] YAML/JSON fields use standard names
- [ ] Output messages use standard terminology

### Readability
- [ ] First mention in section uses full form
- [ ] Appropriate abbreviations in context
- [ ] No mixing of old/new terminology
- [ ] Clear distinction between DDD domain and knowledge domain

### Implementation
- [ ] Code comments use standard terminology
- [ ] Tool output uses standard messages
- [ ] Schema fields use standard names
- [ ] Validation reports use standard terms

---

## Migration Patterns

### Pattern 1: Simple Noun Replacement

**Before:** "Each canon is validated"
**After:** "Each canonical domain model is validated"

### Pattern 2: Compound Terms

**Before:** "Canon closure is calculated"
**After:** "Model closure is calculated"

### Pattern 3: Possessive Forms

**Before:** "The DDD Canon's structure"
**After:** "The DDD Canonical Model's structure"

### Pattern 4: Adjective Usage

**Before:** "Canon-based grounding"
**After:** "Model-based grounding" or "Canonical model grounding"

### Pattern 5: Plural Forms

**Before:** "Five canons form the ontology"
**After:** "Five canonical domain models form the ontology"

### Pattern 6: Mathematical Variables

**Before:** "For each canon Κ ∈ C"
**After:** "For each model m ∈ M"

---

## Exceptions and Edge Cases

### Exception 1: Quoted Sources
If citing a source that uses "canon," preserve the original:
> As Smith (2020) argues, "canons establish normative frameworks" [citation preserved]

Then translate for our context:
> In our terminology, these "canons" are canonical domain models that establish normative specifications.

### Exception 2: Historical Continuity
If referring to earlier versions of this research:
> Version 1.0 of this research used the term "canon" to emphasize authority. Version 2.0 uses "canonical domain model" for greater clarity.

### Exception 3: Code Backward Compatibility
Legacy code may retain old variable names:
```python
canon_schemas = load_schemas()  # Legacy variable name, refers to canonical domain model schemas
```

### Exception 4: Metaphorical Emphasis
When deliberately using canon as metaphor, make it explicit:
> Like canons in religious tradition (authoritative texts), canonical domain models serve as authoritative specifications.

---

## Glossary

**Canonical Domain Model:** A formally specified, internally consistent collection of concepts, relationships, and constraints representing authoritative knowledge within a specific knowledge domain.

**Canonical Model:** Short form of "canonical domain model" used when context is clear.

**Knowledge Domain:** The scope of expertise represented by a canonical model (e.g., Domain-Driven Design, Quality Engineering).

**Model Closure:** The percentage of all references (internal + external) that are resolved through explicit grounding relationships.

**Cross-Domain Model Grounding:** Explicit, typed dependency between concepts in different canonical domain models.

**Model-to-Model Relationship:** Direct semantic connection between two canonical models.

**Domain Model Ontology:** Graph structure where nodes are canonical models and edges are grounding relationships.

---

## References

- **terminology-alignment.md** - Complete terminology mapping
- **audit-log.md** - Document-by-document usage analysis
- **enhance-prompt3.md** - Implementation plan

---

**Status:** Active
**Applies to:** All research documentation, implementation code, and generated reports
**Effective Date:** 2025-10-14
