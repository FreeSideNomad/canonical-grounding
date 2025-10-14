# Phase 4 — Formalization and Modeling (Questions 31-40, Complete)

## 38. Mapping to ArchiMate or UML Metamodel

**Objective:** Enable interoperability with standard enterprise architecture frameworks.

**ArchiMate Mapping:**

ArchiMate 3.1 has three layers matching canonical grounding structure:

**Business Layer → Foundation Canons (DDD, Agile)**
```
ArchiMate Business Layer          Canonical Grounding
─────────────────────────────    ──────────────────────
Business Actor                 →  DDD: Domain Expert, Stakeholder
Business Role                  →  Agile: Product Owner, Scrum Master
Business Process               →  DDD: Domain Service (process)
Business Object                →  DDD: Aggregate, Entity
Business Event                 →  DDD: Domain Event
Value                          →  Agile: Business Value, Epic Outcome
```

**Application Layer → Derived Canons (UX, QE)**
```
ArchiMate Application Layer       Canonical Grounding
─────────────────────────────    ──────────────────────
Application Component          →  UX: Page, Component
Application Function           →  UX: Workflow, Behavior
Application Interface          →  UX: Navigation, API endpoints
Application Service            →  DDD: Application Service
Data Object                    →  DDD: Value Object, Entity state
```

**Technology Layer → Data Engineering**
```
ArchiMate Technology Layer        Canonical Grounding
─────────────────────────────    ──────────────────────
Technology Service             →  Data-Eng: Pipeline
Node                           →  Data-Eng: Compute cluster
Artifact                       →  Data-Eng: Dataset
Communication Network          →  Data-Eng: Data flow, Lineage
```

**ArchiMate Relationships → Grounding Relationships**
```
ArchiMate Relationship            Canonical Grounding
─────────────────────────────    ──────────────────────
Realization                    →  Implementation (UX realizes DDD)
Serving                        →  Grounding (Data-Eng serves DDD)
Access (read/write)            →  References (UX accesses DDD concepts)
Influence                      →  Semantic grounding
Flow                           →  Procedural grounding
Association                    →  Structural grounding
Specialization                 →  Canon versioning/evolution
Composition                    →  Canon contains concepts
Aggregation                    →  Pattern aggregates concepts
```

**UML Metamodel Mapping:**

**Package → Canon**
```
<<canon>> DDD
  <<concept>> Aggregate
  <<concept>> Entity
  <<pattern>> Repository
```

**Dependency → Grounding Relationship**
```
UX ──<<grounds_in>>──> DDD
  stereotype: structural
  strength: strong
```

**Class → Concept**
```
class Aggregate {
  +id: AggregateId
  +root: Entity
  +invariants: Constraint[]
}
```

**Constraint → Validation Rule**
```
context Aggregate
  inv: self.root.isAggregateRoot = true
  inv: self.entities->forAll(e | e.aggregate = self)
```

**UML Profile Extension:**

Create UML profile for Canonical Grounding:
```
<<stereotype>> Canon extends Package
  attributes:
    layer: {foundation, derived, meta}
    version: String

<<stereotype>> GroundingLink extends Dependency
  attributes:
    type: {structural, semantic, procedural, epistemic}
    strength: {strong, weak, optional}
```

**Cross-Tool Interoperability:**

Canonical grounding can export to:
- ArchiMate XML for Archi, BiZZdesign
- UML XMI for Enterprise Architect, MagicDraw
- RDF/OWL for Protégé, semantic reasoning tools
- BPMN for process modeling (Agile workflows)
- DMN for decision modeling (validation rules)

**Value of Mapping:**
1. Tool Integration: Use existing EA tools
2. Visualization: Leverage mature visualization
3. Analysis: Use EA analysis (impact, dependency, gap)
4. Communication: Standard notation
5. Governance: EA governance processes apply

**Limitation:** Standard frameworks lack explicit grounding relationship types, evolution tracking, cross-metamodel constraints.

## 39. Formalize Reasoning Protocol

**Objective:** Define how LLM uses canonical schemas to constrain generation.

**Canon-Guided Generation Protocol:**

**Phase 1: Schema Loading**
```
INPUT: Task description + relevant canons
OUTPUT: Active schema context

STEPS:
1. Identify required canons from task
2. Load canon schemas with dependencies (follow grounding transitively)
3. Construct active schema context (merge vocabularies, patterns, constraints)
4. Validate schema consistency (no cycles, references resolve, no contradictions)
```

**Phase 2: Constrained Generation**
```
INPUT: Active schema context + task
OUTPUT: Schema-conformant artifact

GENERATION STRATEGY:

1. Top-Down Structural Generation
   - Schema defines required fields → generate in order
   - Patterns provide templates → instantiate with specifics
   - Constraints guide valid values → exclude invalid choices

2. Beam Search with Schema Validation
   For each generation step:
   a) Generate k candidate continuations
   b) Validate each against active constraints
   c) Prune invalid candidates
   d) Select highest-probability valid continuation

3. Grounding-Aware Cross-Reference
   - Check grounding link exists
   - Verify target concept available
   - Use qualified reference (canon.concept_id)
   - Validate cardinality constraints

4. Constraint Satisfaction
   - Hard constraints: Must satisfy (block if violated)
   - Soft constraints: Prefer satisfaction (guide)
   - Validate incrementally throughout
```

**Phase 3: Validation and Refinement**
```
INPUT: Generated artifact + schema
OUTPUT: Validated artifact or error report

VALIDATION LEVELS:
1. Syntactic: Parse, check fields, verify types, validate naming
2. Semantic: Resolve references, check constraints, verify patterns, validate invariants
3. Cross-Domain Consistency: Validate references, check alignment, verify propagation
4. Refinement Loop: If validation fails, identify violations, propose corrections, re-generate
```

**Phase 4: Explanation Generation**
```
INPUT: Validated artifact + schema
OUTPUT: Justification trace

TRACEABILITY PROTOCOL:
1. Decision Logging: Record what, why, source, alternatives
2. Hierarchical Justification: Build justification tree
3. Counterfactual Analysis: Explain rejected alternatives
4. Reference Citations: Explicit schema citations
```

**Formal Reasoning Rules:**

**Rule 1: Concept Introduction**
```
To introduce concept C from canon Κ:
  IF C ∈ Κ.concepts
  THEN generate(C) respecting C.properties and C.relationships
  ELSE error("Concept not in canon")
```

**Rule 2: Grounding Reference**
```
To reference concept C_ext from external canon Κ_ext:
  IF ∃γ ∈ current_canon.grounds_in: γ.target = Κ_ext
  AND C_ext ∈ Κ_ext.concepts
  THEN generate_reference(Κ_ext.C_ext)
  ELSE error("No grounding to external canon")
```

**Rule 3: Constraint Propagation**
```
When generating concept C that grounds in concept B:
  constraints(C) := C.local_constraints ∪ B.inherited_constraints
  FOR each constraint IN constraints(C):
    ENSURE constraint.satisfied(current_artifact)
```

**Rule 4: Pattern Instantiation**
```
To use pattern P:
  1. Verify P.applicability matches context
  2. Instantiate P.participants with domain concepts
  3. Generate P.structure with actual relationships
  4. Document P.consequences
```

**Protocol Properties:**
- **Soundness:** Only generates schema-conformant artifacts
- **Completeness:** Can generate any valid artifact
- **Termination:** Always terminates (finite search, max iterations)
- **Traceability:** Every decision has justification

## 40. Canon → Prompt → Artifact Procedure

**Complete Procedure Documentation:**

**STEP 1: Task Analysis**
```
INPUT: User task description
OUTPUT: Task requirements specification

PROCEDURE:
1.1 Parse task natural language
    - Extract domain
    - Identify artifact type
    - Determine scope

1.2 Identify required canons
    RULES:
    - "design aggregate" → canon_ddd
    - "design workflow" → canon_ux + canon_ddd
    - "design pipeline" → canon_data_eng + canon_ddd
    - "complete feature" → all canons

1.3 Determine constraints from task
```

**STEP 2: Schema Preparation**
```
INPUT: Required canons list
OUTPUT: Prepared schema context

PROCEDURE:
2.1 Load primary canons
2.2 Resolve grounding dependencies
2.3 Extract relevant schema elements
2.4 Build unified vocabulary
2.5 Validate schema consistency
```

**STEP 3: Prompt Construction**
```
INPUT: Prepared schema context + task
OUTPUT: LLM prompt with schema grounding

PROCEDURE:
3.1 Select prompt template
3.2 Inject schema information
    COMPONENTS:
    a) Schema Overview (100-200 tokens)
    b) Relevant Concepts (500-1000 tokens)
    c) Applicable Patterns (300-500 tokens)
    d) Constraints (200-400 tokens)
    e) Examples (1000-2000 tokens)

3.3 Add task-specific instructions
3.4 Include validation checklist
```

**STEP 4: LLM Generation**
```
INPUT: Constructed prompt
OUTPUT: Raw LLM response

PROCEDURE:
4.1 Submit prompt (temp: 0.3-0.5)
4.2 Monitor generation
4.3 Capture raw output
```

**STEP 5: Validation**
```
INPUT: Raw output + schema context
OUTPUT: Validation report + refined artifact

PROCEDURE:
5.1 Syntactic Validation
5.2 Semantic Validation
5.3 Grounding Validation
5.4 Constraint Checking
5.5 Generate validation report
```

**STEP 6: Refinement (if needed)**
```
INPUT: Validation report + raw artifact
OUTPUT: Refined artifact

IF validation status = INVALID:
  6.1 Analyze errors
  6.2 Generate correction prompt
  6.3 Re-generate with corrections
  6.4 Re-validate
  6.5 Escalate if unresolvable
```

**STEP 7: Documentation Generation**
```
INPUT: Validated artifact + context + logs
OUTPUT: Complete documentation package

PROCEDURE:
7.1 Generate design rationale
7.2 Create traceability matrix
7.3 Document assumptions
7.4 Add usage guidance
7.5 Include validation evidence
```

**STEP 8: Artifact Delivery**
```
OUTPUT: Deliverable artifact

COMPONENTS:
1. Primary Artifact (schema-conformant design)
2. Documentation (rationale, traceability, assumptions, usage)
3. Metadata (schemas used, timestamp, validation status)
4. Provenance (original task, versions, validation history)
```

**Procedure Properties:**
- **Repeatability:** Same task + schemas → consistent artifacts
- **Traceability:** Every decision traceable to schema
- **Validity:** Guaranteed conformance through validation
- **Efficiency:** Automated validation faster than manual
- **Transparency:** Complete provenance and rationale

**Example End-to-End:**
```
TASK: "Design UX workflow for checkout"

STEP 1: Analysis → Type: UX workflow, Required: [ux, ddd]
STEP 2: Schema Prep → Loaded ux v1.0, ddd v1.0, grounding: ux→ddd
STEP 3: Prompt → 12K tokens with schema + examples
STEP 4: Generation → Claude 3.5, 800 tokens, 15 seconds
STEP 5: Validation → ✓ All checks passed
STEP 6: Refinement → Skipped (valid)
STEP 7: Documentation → Rationale + traceability generated
STEP 8: Delivery → Complete package with provenance

Total time: 45 seconds
Quality: Schema-conformant, production-ready
```
