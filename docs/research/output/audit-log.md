# Terminology Audit Log

**Date:** 2025-10-14
**Auditor:** Claude Code (automated)
**Purpose:** Document "canon" term usage across all research documents

---

## Summary

**Total Documents:** 12 markdown files (excluding terminology-alignment.md)
**Total Lines:** 6,058 lines
**Total "Canon" Occurrences:** ~550 (excluding new terminology-alignment.md)

---

## Document-by-Document Analysis

### 1. phase5-synthesis-complete.md
- **Line Count:** 1,668 lines
- **Canon Occurrences:** 132
- **Priority:** HIGH (most occurrences, comprehensive synthesis)
- **Critical Sections:**
  - Formal definitions and properties
  - Canon closure calculations
  - Canon-to-canon grounding examples
  - Meta-framework descriptions
- **Update Strategy:** Systematic find-replace with manual review
- **Estimated Effort:** 3-4 hours

### 2. canonical-grounding-theory.md
- **Line Count:** 867 lines
- **Canon Occurrences:** 56
- **Priority:** CRITICAL (core theory document, most cited)
- **Critical Sections:**
  - "What is a Canon?" definition section
  - Formal mathematical notation (Κ notation)
  - Four grounding types
  - Canon closure properties
  - Example scenarios
- **Update Strategy:** Manual rewrite of definitions, careful notation updates
- **Estimated Effort:** 2-3 hours

### 3. final-synthesis.md
- **Line Count:** 931 lines
- **Canon Occurrences:** 44
- **Priority:** HIGH (28-page executive summary)
- **Critical Sections:**
  - Executive summary
  - "What is Canonical Grounding?" definition
  - Five Canons introduction
  - Theoretical framework
  - Practical implications
- **Update Strategy:** Section-by-section rewrite
- **Estimated Effort:** 2-3 hours

### 4. phase5-synthesis-partial.md
- **Line Count:** 471 lines
- **Canon Occurrences:** 61
- **Priority:** MEDIUM (partial version, less used)
- **Critical Sections:**
  - Research questions involving canons
  - Formal specifications
  - Implementation guidance
- **Update Strategy:** Automated with spot checks
- **Estimated Effort:** 1 hour

### 5. phase4-formalization-partial.md
- **Line Count:** 363 lines
- **Canon Occurrences:** 48
- **Priority:** MEDIUM
- **Critical Sections:**
  - BNF grammar (Canon → DomainModel)
  - Meta-model descriptions
  - Formal notation
- **Update Strategy:** Update grammar definitions, notation
- **Estimated Effort:** 1-1.5 hours

### 6. phase4-formalization-complete.md
- **Line Count:** 380 lines
- **Canon Occurrences:** 33
- **Priority:** MEDIUM
- **Critical Sections:**
  - Complete formalization
  - Mathematical proofs
  - Implementation specifications
- **Update Strategy:** Careful notation updates
- **Estimated Effort:** 1-1.5 hours

### 7. README.md
- **Line Count:** 401 lines
- **Canon Occurrences:** 29
- **Priority:** CRITICAL (entry point for all readers)
- **Critical Sections:**
  - Overview and introduction
  - Navigation guide
  - Quick reference
  - File descriptions
- **Update Strategy:** Complete rewrite with terminology note
- **Estimated Effort:** 1 hour

### 8. phase1-conceptual-foundation.md
- **Line Count:** 166 lines
- **Canon Occurrences:** 30
- **Priority:** MEDIUM
- **Critical Sections:**
  - Q1-10 conceptual questions
  - Canon vs. Ontology comparison
  - Philosophical foundations
- **Update Strategy:** Update Q&A format
- **Estimated Effort:** 45 minutes

### 9. research-summary.md
- **Line Count:** 248 lines
- **Canon Occurrences:** 30
- **Priority:** MEDIUM
- **Critical Sections:**
  - Research overview
  - Key findings
  - Canon system description
- **Update Strategy:** Automated with review
- **Estimated Effort:** 30 minutes

### 10. phase2-comparative-analysis.md
- **Line Count:** 213 lines
- **Canon Occurrences:** 18
- **Priority:** LOW
- **Critical Sections:**
  - Canon vs. DDD comparison
  - Canon vs. MDA comparison
  - Canon vs. Ontology comparison
- **Update Strategy:** Update comparison tables
- **Estimated Effort:** 30 minutes

### 11. phase3-empirical-validation.md
- **Line Count:** 350 lines
- **Canon Occurrences:** 11
- **Priority:** LOW
- **Critical Sections:**
  - Experiment descriptions mentioning canons
  - Schema-grounded LLM validation
  - Benefit claims
- **Update Strategy:** Minor updates to experiment notes
- **Estimated Effort:** 20 minutes

---

## Implementation Files

### 12. interdomain-map.yaml
- **Canon Occurrences:** ~60+ (field names and values)
- **Priority:** HIGH (technical specification)
- **Critical Sections:**
  - `canons:` section → `canonical_models:`
  - `canon_ddd`, `canon_qe`, etc. IDs
  - Grounding source/target fields
- **Update Strategy:** Structural changes with backward compatibility
- **Estimated Effort:** 45 minutes

---

## Update Priority Matrix

### Immediate Priority (Steps 4-7)
1. **canonical-grounding-theory.md** - Core theory, most cited
2. **final-synthesis.md** - Executive summary, high visibility
3. **README.md** - Entry point, first impression
4. **phase5-synthesis-complete.md** - Comprehensive, most occurrences

**Subtotal Effort:** 7-11 hours

### Secondary Priority (Step 6)
5. phase4-formalization-partial.md
6. phase4-formalization-complete.md
7. phase5-synthesis-partial.md
8. phase1-conceptual-foundation.md
9. research-summary.md

**Subtotal Effort:** 4-5.5 hours

### Lower Priority
10. phase2-comparative-analysis.md
11. phase3-empirical-validation.md

**Subtotal Effort:** 50 minutes

### Implementation Updates (Steps 8-10)
12. interdomain-map.yaml
13. GROUNDING-REPORT.md
14. Validation tools

**Subtotal Effort:** 2-3 hours

---

## Terminology Context Analysis

### Appropriate "Canon" Usage (Preserve)

These contexts use "canon" correctly and should be PRESERVED:

1. **Historical Citations:**
   - "Aristotle's canonical texts"
   - "Kant's critical canon"
   - "Biblical canon"

2. **Metaphorical Comparisons:**
   - "Like a religious canon, it establishes authority"
   - "Canon in the literary sense"

3. **Academic References:**
   - Citing papers that use "canon" terminology

### Incorrect "Canon" Usage (Update)

These contexts should use "canonical domain model":

1. **Technical Descriptions:**
   - ❌ "Each canon is a YAML schema"
   - ✅ "Each canonical domain model is defined in a YAML schema"

2. **Implementation References:**
   - ❌ "The DDD Canon implements..."
   - ✅ "The DDD Canonical Model implements..."

3. **Architectural Discussions:**
   - ❌ "Canon-to-canon grounding"
   - ✅ "Cross-domain model grounding"

4. **Mathematical Definitions:**
   - ❌ "Canon closure (Κ)"
   - ✅ "Model closure (M)"

5. **System Descriptions:**
   - ❌ "Five canons form the ontology"
   - ✅ "Five canonical domain models form the ontology"

---

## Automated vs. Manual Updates

### Safe for Automated Find-Replace

- "Five canons" → "Five canonical domain models"
- "Canon closure" → "Model closure"
- "Canon coherence" → "Model coherence"
- "Canon schema" → "Domain model schema"
- "Inter-canon" → "Cross-domain model"
- "Canon-to-canon" → "Model-to-model"

### Require Manual Review

- "Canon" in formal definitions (need full sentence rewrite)
- "Canon" in mathematical notation (Κ → M)
- "Canon" in headings and titles
- "Canon" in quotes or citations
- "Canon" in philosophical discussions
- First occurrences in sections (need expanded form)

---

## Risk Assessment

### High Risk Sections (Extra Caution)

1. **Mathematical Formalism:**
   - Changing Κ → M requires updating all dependent notation
   - Proofs must remain valid after terminology change
   - Risk: Breaking mathematical arguments

2. **Empirical Data References:**
   - pilot-results.csv column headers
   - Experiment descriptions
   - Risk: Invalidating data references

3. **External Citations:**
   - Papers that cite our work using "canon"
   - Historical references
   - Risk: Breaking academic continuity

### Mitigation Strategies

1. **Version Documentation:**
   - CHANGELOG-v2.md explains all changes
   - Terminology alignment document provides mapping
   - README includes terminology note

2. **Backward Compatibility:**
   - Keep old field names in comments
   - Add "formerly known as" notes
   - Preserve URLs and IDs

3. **Validation:**
   - Re-run all validation tools
   - Check all internal links
   - Verify closure calculations unchanged

---

## Next Steps

1. ✅ Complete this audit (DONE)
2. → Create terminology-standards.md (Step 3)
3. → Begin updates starting with highest priority docs
4. → Validate after each major document update
5. → Run consistency checker before finalizing

---

## Audit Completion

**Status:** ✅ Complete
**Total Documents to Update:** 12 markdown + 1 YAML + 2 tools
**Estimated Total Effort:** 14-20 hours
**Recommended Approach:** Batch by priority, validate incrementally

**Key Finding:** Terminology change is extensive (550+ occurrences) but straightforward. Most usage is in technical contexts where "canonical domain model" is more accurate. Very few occurrences are in historical/philosophical contexts where "canon" should be preserved.
