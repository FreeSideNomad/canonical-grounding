# Enhancement Prompt 3: Terminology Alignment and Research Update

## Context

The current research and documentation uses the term **"canon"** throughout, but the actual implementation and schemas use **"canonical domain model"** where:
- **Canonical** = authoritative, formally specified
- **Domain** = knowledge domain (not DDD domain)
- **Model** = structured representation

This terminology misalignment creates confusion. The research documents refer to "DDD Canon", "QE Canon", etc., but these are actually **canonical domain models** representing different knowledge domains (Domain-Driven Design knowledge, Quality Engineering knowledge, etc.).

## Objective

Update all research documentation to use consistent, accurate terminology while preserving the theoretical foundation and empirical findings. Revalidate closure and grounding metrics based on the enhanced schemas.

---

## Phase 1: Terminology Analysis and Mapping (Steps 1-3)

### Step 1: Create Terminology Mapping Document

**Action:** Create `research-output/terminology-alignment.md`

**Content:**
- **Old Term → New Term mapping:**
  - "Canon" → "Canonical Domain Model"
  - "Canon [Name]" → "[Name] Canonical Model" or "[Name] Knowledge Domain Model"
  - "Canonical Grounding" → "Cross-Domain Model Grounding" (preserve if clearer in context)
- **Preserved Terms:**
  - "Grounding" (philosophical concept remains valid)
  - "Ontology" (graph of models remains valid)
  - "Closure" (mathematical property remains valid)
- **Clarified Concepts:**
  - Domain = Knowledge domain (not DDD bounded context)
  - Model = Formal specification (YAML/JSON Schema)
  - Canonical = Authoritative reference within its knowledge domain

**Rationale:** Each "canon" is actually a **canonical model** for a specific **knowledge domain**:
- DDD Canonical Model = authoritative model of Domain-Driven Design concepts
- QE Canonical Model = authoritative model of Quality Engineering concepts
- Not "religious canons" but "reference models"

### Step 2: Audit All Research Documents

**Action:** Read and catalog terminology usage in each document

**Files to audit:**
```
research-output/
├── canonical-grounding-theory.md (23 pages)
├── final-synthesis.md (28 pages)
├── phase1-conceptual-foundation.md
├── phase2-comparative-analysis.md
├── phase3-empirical-validation.md
├── phase4-formalization-partial.md
├── phase4-formalization-complete.md
├── phase5-synthesis-partial.md
├── phase5-synthesis-complete.md
├── interdomain-map.yaml
└── README.md
```

**Create:** `research-output/audit-log.md` with:
- Document name
- Line count with "canon" term
- Critical sections requiring terminology update
- Sections where "canon" metaphor is intentional vs. implementation mismatch

### Step 3: Define Terminology Standards

**Action:** Create `research-output/terminology-standards.md`

**Standards:**

1. **When to use "Canon":**
   - Historical/philosophical context (Aristotle, Kant, etc.)
   - Metaphorical comparisons (e.g., "like religious canons")
   - Already established academic usage being referenced

2. **When to use "Canonical Domain Model":**
   - Referring to implementation (schemas, YAML files)
   - Technical descriptions of the system
   - Formal definitions and specifications

3. **When to use "Knowledge Domain":**
   - Describing the scope (DDD knowledge, QE knowledge)
   - Distinguishing from DDD's "domain" concept
   - Explaining what each model represents

4. **Hybrid Usage:**
   - "Canonical Model (Canon)" on first mention
   - Can abbreviate to "model" in context
   - Keep "grounding" for relationships

**Example Rewrites:**
- ❌ "Each canon is a formally specified domain model"
- ✅ "Each canonical domain model is a formally specified representation of a knowledge domain"

- ❌ "DDD Canon"
- ✅ "DDD Canonical Model" or "Domain-Driven Design Knowledge Domain Model"

- ❌ "Canon closure"
- ✅ "Model closure" or "Domain model closure"

---

## Phase 2: Update Core Theory Documents (Steps 4-7)

### Step 4: Update canonical-grounding-theory.md

**Action:** Rewrite with consistent terminology

**Key sections to update:**

1. **Section: "What is a Canon?" (Page 2)**
   - Rename to "What is a Canonical Domain Model?"
   - Update definition:
     ```
     OLD: "A canon (Κ) is a formally specified, internally consistent collection..."
     NEW: "A canonical domain model (M) is a formally specified, internally consistent
          collection of concepts, relationships, and constraints representing
          authoritative knowledge within a specific knowledge domain."
     ```

2. **Formal Definitions (Page 3-4)**
   - Canon (Κ) → Model (M) or Domain Model (DM)
   - Update all set notation: C = {c₁, c₂, ..., cₙ} remains but explain c represents "canonical model"
   - Keep Greek symbols for mathematical formalism but update variable names

3. **Four Grounding Types (Page 6-7)**
   - Update examples to use "model" terminology
   - "Canon-to-canon grounding" → "Cross-domain model grounding"

4. **Properties Section (Page 8-9)**
   - "Canon closure" → "Model closure"
   - "Canon coherence" → "Model coherence"

5. **Update all 15+ examples throughout document**

**Validation:** Ensure mathematical rigor is preserved while terminology improves clarity

### Step 5: Update final-synthesis.md

**Action:** Major rewrite with terminology alignment

**Key sections (28 pages):**

1. **Executive Summary**
   - Update "What is Canonical Grounding?" definition
   - Change "Five Canons" → "Five Canonical Domain Models"
   - Update benefit statements to reference models

2. **Part I: Research Journey**
   - Update all 50 questions to use consistent terminology
   - Phase descriptions: "canon" → "canonical model"
   - Keep historical context where "canon" is cited from sources

3. **Part II: Theoretical Framework**
   - Formal model definitions
   - Update ontology graph description (nodes = models, edges = groundings)
   - Closure calculation examples

4. **Part III: Practical Implications**
   - "When to use canonical grounding" → "When to use canonical domain models"
   - Implementation roadmap: update schema references
   - ROI analysis: update terminology in examples

5. **Part IV: Scientific Assessment**
   - Update criteria evaluation to reflect accurate terminology
   - Design science guidelines: ensure model-based language

6. **Part V: Future Research**
   - Update research questions with correct terminology

### Step 6: Update Phase Documents (5 documents)

**Action:** Update each phase document

**phase1-conceptual-foundation.md:**
- Q1-10: Update definitions and comparisons
- "Canon vs. Ontology" → "Canonical Model vs. Ontology"
- Update philosophical foundations to clarify model-based approach

**phase2-comparative-analysis.md:**
- "Canon vs. DDD Bounded Context" → "Canonical Domain Model vs. DDD Bounded Context"
- Update comparisons to Kuhn, MDA, Wand & Weber
- Each canonical model IS a bounded context in meta-system

**phase3-empirical-validation.md:**
- Update experiment descriptions
- "Schema-grounded LLMs" remains valid (schemas define the models)
- Update benefit claims to reference domain models

**phase4-formalization-*.md:**
- Update BNF grammar: Canon → DomainModel
- Update meta-model UML diagrams (if regenerating)
- Keep mathematical notation but update variable semantics

**phase5-synthesis-*.md:**
- Update final specifications
- Readiness assessment: update terminology
- Meta-framework: clarify it's a "framework of canonical domain models"

### Step 7: Update README.md

**Action:** Rewrite README as entry point with correct terminology

**Sections:**
1. **Title:** "Canonical Domain Model Grounding - Research Output"
2. **One-sentence summary:** Use accurate terminology
3. **Quick Start:** Update all references
4. **Navigation:** Update file descriptions
5. **Terminology Note:** Add section explaining the shift from "canon" to "canonical domain model"

---

## Phase 3: Update Implementation Documentation (Steps 8-10)

### Step 8: Update interdomain-map.yaml

**Action:** Update field names and documentation

**Changes:**
```yaml
OLD:
  canons:
    - id: "canon_ddd"
      name: "DDD Canon"

NEW:
  canonical_models:
    - id: "model_ddd"
      name: "DDD Canonical Domain Model"
      knowledge_domain: "Domain-Driven Design"
      description: "Authoritative model of DDD strategic and tactical patterns"
```

**Update all 19 groundings:**
```yaml
OLD:
  - id: "grounding_agile_ddd_001"
    source: "canon_agile"
    target: "canon_ddd"

NEW:
  - id: "grounding_agile_ddd_001"
    source: "model_agile"
    target: "model_ddd"
    description: "Agile canonical model references DDD canonical model"
```

**Add metadata:**
```yaml
metadata:
  terminology_version: "2.0"
  terminology_change: "Canon → Canonical Domain Model (2025-10-14)"
  rationale: "Clarifies that each 'canon' is a formal model of a knowledge domain"
```

### Step 9: Update GROUNDING-REPORT.md

**Action:** Regenerate with correct terminology

**Changes:**
- Title: "Canonical Domain Model Grounding Report"
- "Canon" → "Canonical Model" or "Domain Model" throughout
- Table headers: "Source Model", "Target Model"
- Section: "Canonical Domain Model Closure Metrics"
- Legend: Update graph explanation

**Add section:**
```markdown
## Terminology Note

This report uses "Canonical Domain Model" to refer to what was previously called a "canon".
Each model represents authoritative knowledge within a specific domain:
- **DDD Model**: Domain-Driven Design concepts
- **QE Model**: Quality Engineering concepts
- **UX Model**: User Experience concepts
- **Data-Eng Model**: Data Engineering concepts
- **Agile Model**: Agile methodology concepts
```

### Step 10: Update Validation Tools

**Action:** Update tool comments and output

**Files:**
- `tools/validate-schemas.py`
- `tools/generate-grounding-graph.py`

**Changes:**
- Update docstrings: "canon" → "canonical domain model"
- Update print statements: "Loading Canon Schemas" → "Loading Canonical Domain Model Schemas"
- Update variable names: `canon_schemas` → `domain_model_schemas` (or keep for backward compat with comments)
- Update output messages in validation report

---

## Phase 4: Revalidate Closure and Grounding (Steps 11-14)

### Step 11: Update Closure Calculation

**Action:** Revalidate closure with enhanced schemas

**Process:**
1. Run `tools/validate-schemas.py`
2. Verify all 5 models still achieve 100% closure
3. Check if schema enhancements added new external references
4. Recalculate grounding relationship counts

**Expected Results:**
- DDD Model: 6/6 concepts (100%)
- Data-Eng Model: 0/0 concepts (100%)
- UX Model: 6/6 concepts (100%)
- QE Model: 18/18 concepts (100%)
- Agile Model: 28/28 concepts (100%)

**Action if changed:** Update all closure references in research docs

### Step 12: Revalidate Grounding Relationships

**Action:** Verify all 30 concept-to-concept groundings

**Process:**
1. Run `tools/generate-grounding-graph.py`
2. Verify still 30 relationships (or document new ones)
3. Check grounding strength distribution (should be 96.7% strong)
4. Validate no circular dependencies

**Update if needed:**
- Count of groundings in research docs
- Grounding strength percentages
- Specific relationship examples

### Step 13: Regenerate Empirical Data Tables

**Action:** Update pilot-results.csv if needed

**Review:**
- Do experiment descriptions need terminology updates?
- Should "canon" in experiment notes become "model"?
- Are closure percentages still accurate?

**Update:** `research-output/pilot-results.csv` comments and descriptions

### Step 14: Update Graph Visualization

**Action:** Regenerate grounding-graph.svg with updated terminology

**Process:**
1. Update `generate-grounding-graph.py` to use new terminology in labels
2. Regenerate DOT file
3. Regenerate SVG with `dot -Tsvg`
4. Update graph legend in GROUNDING-REPORT.md

**Changes in graph:**
- Cluster labels: "DDD Canon" → "DDD Canonical Model"
- Node tooltips: Update descriptions
- Legend: Update terminology

---

## Phase 5: Quality Assurance and Consistency (Steps 15-18)

### Step 15: Run Terminology Consistency Check

**Action:** Create automated consistency checker

**Script:** `tools/check-terminology-consistency.py`

```python
# Pseudo-code:
1. Load all .md files in research-output/
2. Search for remaining "canon" usage (case-insensitive)
3. Identify if usage is:
   - Historical/citation context (OK)
   - Implementation reference (needs update)
   - Inconsistent with standards (flag for review)
4. Generate report: terminology-consistency-report.md
```

**Run and review:** Fix any inconsistencies found

### Step 16: Update Cross-References

**Action:** Ensure all internal document links still work

**Check:**
- Links between research documents
- References to specific sections (page numbers may have shifted)
- Links from README to other docs
- Links from GROUNDING-REPORT.md to research docs

**Update:** Any broken or outdated references

### Step 17: Scientific Integrity Check

**Action:** Verify research findings remain valid

**Review:**
1. **Theoretical soundness:** Does terminology change affect formal definitions?
   - Answer: No, mathematical properties unchanged

2. **Empirical validity:** Do experiment results still apply?
   - Answer: Yes, renaming doesn't change measurements

3. **Comparative analysis:** Are comparisons to DDD, MDA, etc. still accurate?
   - Answer: More accurate (clarifies we're comparing models, not canons)

4. **Philosophical grounding:** Is Aristotle → Kant → Quine chain still valid?
   - Answer: Yes, "canonical" concept strengthened

**Document:** Create `research-output/scientific-integrity-statement.md`

### Step 18: Peer Review Preparation

**Action:** Prepare updated research for external review

**Create:** `research-output/CHANGELOG-v2.md`

**Content:**
```markdown
# Research Documentation v2.0 - Terminology Alignment

## Summary of Changes

**Date:** 2025-10-14
**Type:** Terminology clarification (non-breaking)
**Impact:** Improved clarity, no changes to findings

## What Changed

### Terminology
- "Canon" → "Canonical Domain Model"
- Clarified "domain" = knowledge domain (not DDD domain)
- Updated all 13 research documents

### Validation
- ✅ All closure metrics revalidated (100% maintained)
- ✅ All 30 groundings reverified
- ✅ Schema enhancements integrated
- ✅ No circular dependencies

### Documentation
- Updated interdomain-map.yaml with new terminology
- Regenerated GROUNDING-REPORT.md
- Updated validation tool output
- Refreshed graph visualization

## What Didn't Change

- Mathematical formalism (properties, proofs)
- Empirical data (pilot-results.csv)
- Research findings and conclusions
- Implementation schemas (only comments)
- Grounding relationships (30 remain)

## Rationale

Original terminology used "canon" (borrowed from religious/literary tradition)
to emphasize authority and consistency. However, implementation actually uses
"canonical domain models" - formal models representing authoritative knowledge
in specific domains. Updated terminology:

1. **More accurate:** Reflects actual implementation
2. **Less ambiguous:** Avoids religious connotation
3. **Clearer:** "Model" explicitly states what it is
4. **Consistent:** Aligns research with code

## Migration Guide

For readers of v1.0 research:
- Wherever you see "Canon", read "Canonical Domain Model"
- "DDD Canon" = "DDD Canonical Model" = formal model of DDD concepts
- All findings, metrics, and conclusions remain identical
- This is a clarification, not a methodology change
```

---

## Phase 6: Publication and Communication (Steps 19-21)

### Step 19: Update Repository Documentation

**Action:** Update root-level docs

**Files to update:**
- `README.md` (if exists in root)
- `enhance-prompt.md` (mark as superseded)
- `enhance-prompt2.md` (mark as superseded)
- Create new `TERMINOLOGY.md` explaining the system

**TERMINOLOGY.md content:**
```markdown
# Terminology Guide

## Core Concepts

### Canonical Domain Model
A formally specified, authoritative representation of knowledge within a
specific domain. Each model is defined using YAML or JSON Schema.

**Examples:**
- DDD Canonical Model: Authoritative model of DDD concepts (Aggregate, Entity, etc.)
- QE Canonical Model: Authoritative model of QE concepts (TestCase, TestStrategy, etc.)

### Knowledge Domain
The scope of knowledge represented by a canonical model. Distinct from
DDD's concept of "domain" (business domain).

**Examples:**
- Domain-Driven Design (knowledge domain)
- Quality Engineering (knowledge domain)
- Not: "Order Management" (that's a DDD bounded context)

### Grounding Relationship
An explicit, typed dependency between concepts in different canonical models.

**Types:**
- Structural: Direct field references
- Semantic: Meaning alignment
- Procedural: Process dependencies
- Epistemic: Knowledge coordination

### Model Closure
Percentage of all references (internal + external) that are resolved through
explicit grounding relationships. Target: >95%

## Historical Note

Earlier versions of this research used "canon" instead of "canonical domain model".
The terminology was updated for clarity and accuracy, but all findings remain valid.
```

### Step 20: Create Migration Branch and PR

**Action:** Create new branch for terminology updates

**Commands:**
```bash
git checkout -b feature/terminology-alignment
# (After making all updates)
git add research-output/
git commit -m "Update research terminology: canon → canonical domain model"
git push -u origin feature/terminology-alignment
gh pr create --title "Research Terminology Alignment (v2.0)" --body "<detailed description>"
```

**PR Description:** Include:
- Summary of terminology change
- Rationale for change
- Validation that findings unchanged
- Link to CHANGELOG-v2.md
- Before/after examples

### Step 21: Update GROUNDING-REPORT.md with Terminology

**Action:** Final update to grounding report

**Add sections:**
1. **Terminology** (at top, after summary)
2. **Version History** (at bottom)
   - v1.0: Initial research with "canon" terminology
   - v2.0: Terminology alignment to "canonical domain model"

**Regenerate:**
- All tables with "Model" instead of "Canon"
- Graph with updated labels
- Validation report with updated terminology

**Final validation:**
```bash
cd tools
./run-validation.sh
python generate-grounding-graph.py
dot -Tsvg ../grounding-graph.dot -o ../grounding-graph.svg
```

---

## Success Criteria

### Terminology Consistency
- [ ] 0 inconsistent "canon" references in implementation context
- [ ] All research docs use "canonical domain model" consistently
- [ ] Historical/philosophical "canon" usage preserved where appropriate
- [ ] New TERMINOLOGY.md provides clear definitions

### Scientific Integrity
- [ ] All closure metrics revalidated (target: 100% maintained)
- [ ] All 30 grounding relationships reverified
- [ ] Mathematical formalism unchanged
- [ ] Empirical findings remain valid

### Documentation Quality
- [ ] All internal cross-references work
- [ ] CHANGELOG-v2.md documents all changes
- [ ] README.md updated as entry point
- [ ] GROUNDING-REPORT.md regenerated with new terminology

### Tool Updates
- [ ] validate-schemas.py uses updated terminology in output
- [ ] generate-grounding-graph.py produces graphs with "Model" labels
- [ ] Terminology consistency checker passes
- [ ] All validation tests pass

### Deliverables
- [ ] 13 updated research documents in research-output/
- [ ] Updated interdomain-map.yaml with new field names
- [ ] Regenerated GROUNDING-REPORT.md
- [ ] New TERMINOLOGY.md guide
- [ ] CHANGELOG-v2.md documenting changes
- [ ] Updated graph visualization (SVG)
- [ ] Pull request with full diff

---

## Implementation Priority

### High Priority (Do First)
1. Steps 1-3: Terminology analysis and standards
2. Steps 4-7: Update core theory documents (most cited)
3. Steps 11-14: Revalidate metrics (ensure accuracy)
4. Step 21: Update GROUNDING-REPORT.md (most visible)

### Medium Priority
5. Steps 8-10: Update implementation docs
6. Steps 15-18: Quality assurance
7. Step 19: Update repo docs

### Lower Priority (Can defer)
8. Step 20: Create PR (after all updates complete)

---

## Estimated Effort

- **Terminology Analysis (Steps 1-3):** 2-3 hours
- **Core Theory Updates (Steps 4-7):** 6-8 hours (23 + 28 pages + 5 phase docs)
- **Implementation Updates (Steps 8-10):** 2-3 hours
- **Revalidation (Steps 11-14):** 1-2 hours (mostly automated)
- **Quality Assurance (Steps 15-18):** 3-4 hours
- **Documentation (Steps 19-21):** 2-3 hours

**Total:** 16-23 hours (2-3 days)

---

## Risks and Mitigations

### Risk 1: Terminology confusion in academic context
**Mitigation:** Keep historical usage where citing sources, add footnotes explaining alignment

### Risk 2: Breaking existing references
**Mitigation:** Maintain old terminology in comments, add redirects in README

### Risk 3: Validation metrics change
**Mitigation:** Rerun all tools before updating docs, document any changes

### Risk 4: Graph generation breaks
**Mitigation:** Test visualization pipeline at each step, keep old IDs in comments

---

## Output Files

### New Files
- `research-output/terminology-alignment.md`
- `research-output/terminology-standards.md`
- `research-output/audit-log.md`
- `research-output/scientific-integrity-statement.md`
- `research-output/CHANGELOG-v2.md`
- `TERMINOLOGY.md`
- `tools/check-terminology-consistency.py`
- `terminology-consistency-report.md`

### Updated Files (13 research docs)
- `research-output/canonical-grounding-theory.md`
- `research-output/final-synthesis.md`
- `research-output/phase1-conceptual-foundation.md`
- `research-output/phase2-comparative-analysis.md`
- `research-output/phase3-empirical-validation.md`
- `research-output/phase4-formalization-partial.md`
- `research-output/phase4-formalization-complete.md`
- `research-output/phase5-synthesis-partial.md`
- `research-output/phase5-synthesis-complete.md`
- `research-output/README.md`
- `research-output/interdomain-map.yaml`
- `GROUNDING-REPORT.md`
- `tools/validate-schemas.py`
- `tools/generate-grounding-graph.py`

### Regenerated Files
- `grounding-graph.svg`
- `grounding-graph.dot`
- `validation-report.txt`

---

## Validation Commands

```bash
# Phase 4: Revalidation
cd tools
./setup.sh  # Ensure environment ready
./run-validation.sh  # Validate schemas and closure
python generate-grounding-graph.py  # Regenerate graph
python check-terminology-consistency.py  # Check consistency

# Generate visualizations
cd ..
dot -Tsvg grounding-graph.dot -o grounding-graph.svg
dot -Tpng grounding-graph.dot -o grounding-graph.png

# Verify no errors
echo "Exit code: $?"
```

---

## Questions to Address

1. **Q:** Should we update the formal mathematical notation (Κ → M)?
   **A:** Yes, update to M (Model) or DM (Domain Model) for clarity

2. **Q:** Do we need to regenerate the pilot-results.csv?
   **A:** No, data unchanged; only update column headers and notes

3. **Q:** Should interdomain-map.yaml break backward compatibility?
   **A:** Add new fields, keep old as deprecated with comments

4. **Q:** What if closure percentages change?
   **A:** Document in CHANGELOG, update all references, investigate cause

5. **Q:** Should we update the GitHub repo name?
   **A:** No, URL changes break links; "canonical-grounding" is fine as shorthand

---

## Final Notes

This is a **non-breaking terminology alignment** that:
- ✅ Improves clarity and accuracy
- ✅ Aligns research with implementation
- ✅ Preserves all findings and conclusions
- ✅ Maintains scientific integrity
- ✅ Does not change the methodology

The term "canonical domain model" better captures what each "canon" actually is: a formal, authoritative model representing knowledge in a specific domain.

---

**Target Completion:** 2-3 days
**Priority:** High (improves clarity for external readers)
**Risk:** Low (terminology clarification only)
