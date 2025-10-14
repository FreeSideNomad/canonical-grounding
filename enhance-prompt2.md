# Schema Enhancement Prompt: Addressing Negative Findings

**Objective:** Address the identified gaps and negative findings from the canonical grounding research by improving schema completeness, explicit grounding relationships, and cross-canon integration.

**Target:** Achieve >95% closure for all canons (currently QE: 75%, Agile: 72%) and make all implicit domain references explicit.

**Total Steps:** 21 (includes automated validation with Python script in virtual environment)

---

## Context: Key Negative Findings from Research

Based on comprehensive research analysis, the following critical gaps were identified:

### Primary Issues

1. **Incomplete Closure** (High Priority)
   - QE Canon: 75% closure (needs +20% to reach target)
   - Agile Canon: 72% closure (needs +23% to reach target)
   - Target: >95% for production readiness

2. **Missing Grounding Relationships** (High Priority)
   - Agile → DDD: Currently implicit, needs explicit structural/epistemic grounding
   - Agile → UX: Currently implicit, needs explicit epistemic grounding
   - Agile → QE: Weak grounding, needs strengthening
   - Agile → Data-Eng: Not formalized, needs explicit grounding
   - QE → Data-Eng: Missing contract validation grounding

3. **Implicit Domain References** (Medium Priority)
   - Agile features reference bounded contexts but not formally declared
   - Agile stories reference UX pages/workflows but not in schema
   - QE test strategies reference domain patterns but implicitly
   - 28% of Agile references lack explicit grounding
   - 25% of QE references lack explicit grounding

4. **Schema Limitations** (Medium Priority)
   - Not production-ready due to incomplete schemas
   - Limits automated validation capabilities
   - Reduces LLM accuracy potential (currently achieving 80-90%, could reach 92-96%)

---

## Available Resources

### Domain Directory Structure

Each domain contains:
- `model.schema.yaml` or `model-schema.yaml` - Primary schema definition
- `docs/` - Comprehensive documentation (varies by domain)
- `examples/` - Concrete examples (some domains)
- Guide documents (agile, data-eng, ux)

**Data-Eng:** Most complete documentation (15 docs including architecture, governance, conformance, patterns)
**DDD:** Comprehensive theory (8 docs covering strategic, tactical, ubiquitous language, POEAA integration)
**UX:** Well-documented terminology and examples
**QE:** 20 documentation files (good foundation)
**Agile:** Guide document and examples available

---

## Enhancement Steps (21 Steps)

### Phase 1: Analysis and Inventory (Steps 1-4)

#### Step 1: Audit Current QE Schema for Missing Groundings
**Action:** Analyze `/domains/qe/model-schema.yaml` to identify all concepts that reference external domains
**Output:** List of QE concepts with:
- Concept name
- External reference (implicit or explicit)
- Target canon
- Grounding status (missing, weak, implicit)
**Validation:** Compare against interdomain-map.yaml to find gaps

#### Step 2: Audit Current Agile Schema for Missing Groundings
**Action:** Analyze `/domains/agile/model.schema.yaml` to identify all concepts that should reference domain concepts
**Output:** List of Agile concepts with:
- Concept name (Epic, Feature, Story, Sprint, PI, Team, ART)
- Implicit domain references (e.g., Feature → BoundedContext)
- Required grounding relationships
- Current status (implicit, missing, weak)
**Validation:** Cross-reference with agile/guide-to-agile.md for terminology usage

#### Step 3: Analyze Domain Documentation for Grounding Clues
**Action:** Review documentation in:
- `/domains/qe/docs/` - Test strategies, patterns, quality attributes
- `/domains/agile/docs/` - Agile patterns, workflows
- `/domains/ux/docs/` - UX patterns that may reference tests
- `/domains/ddd/docs/` - Domain concepts referenced by agile/qe
**Output:** Mapping of implicit cross-references found in documentation
**Example:** If QE docs mention "aggregate invariants," document QE → DDD grounding need

#### Step 4: Review Existing Examples for Cross-Canon Patterns
**Action:** Examine example files:
- `/domains/agile/examples/` - Look for domain references in sprint planning, backlogs
- `/domains/data-eng/examples/` - Check pipeline references to domains
- `/domains/ddd/ddd-schema-example.yaml` - See how DDD expects to be referenced
**Output:** List of actual usage patterns showing how canons reference each other in practice
**Validation:** These patterns inform grounding relationship design

### Phase 2: QE Schema Enhancement (Steps 5-8)

#### Step 5: Add QE → Data-Eng Contract Validation Grounding
**Action:** Enhance QE schema to explicitly reference data engineering contracts
**Specific Changes:**
```yaml
# Add to QE schema under Test or ContractTest definition
contract_validates:
  type: string
  description: "Reference to data-eng:Contract being validated"
  pattern: "^data_eng:Contract:[a-z0-9_-]+$"
  grounding:
    target_canon: "data_eng"
    target_concept: "Contract"
    grounding_type: "procedural"
    strength: "strong"
    rationale: "Contract tests ensure schema stability"
```
**Documentation:** Add to interdomain-map.yaml under groundings
**Validation:** Closure calculation should increase (currently 75% → target 80%+)

#### Step 6: Strengthen QE → DDD Invariant Validation
**Action:** Enhance existing QE → DDD grounding with explicit test-to-invariant mapping
**Specific Changes:**
```yaml
# Enhance Test definition in QE schema
validates_invariants:
  type: array
  items:
    type: string
    pattern: "^ddd:Aggregate:[a-z0-9_-]+:invariant:[a-z0-9_-]+$"
  description: "DDD aggregate invariants this test validates"
  grounding:
    target_canon: "ddd"
    target_concept: "Aggregate.invariants"
    grounding_type: "procedural"
    strength: "strong"
    constraint: "Every documented invariant should have at least one test"
    coverage_target: "100%"
```
**Impact:** Makes QE role as validator explicit in schema structure

#### Step 7: Add QE → UX Workflow Validation Grounding
**Action:** Create explicit grounding from QE tests to UX workflows
**Specific Changes:**
```yaml
# Add UITest or E2ETest definition in QE schema
validates_workflow:
  type: string
  description: "Reference to ux:Workflow being tested"
  pattern: "^ux:Workflow:[a-z0-9_-]+$"
  grounding:
    target_canon: "ux"
    target_concept: "Workflow"
    grounding_type: "procedural"
    strength: "strong"
    constraint: "Critical workflows should have E2E test coverage"
```
**Documentation:** Update interdomain-map.yaml grounding_qe_ux_001
**Validation:** Check closure improvement (target: 75% → 85%)

#### Step 8: Add QE Test Strategy → Domain Pattern References
**Action:** Create explicit links from test strategies to domain patterns they validate
**Specific Changes:**
```yaml
# Add TestStrategy definition
TestStrategy:
  type: object
  properties:
    targets_pattern:
      type: string
      description: "Domain pattern this strategy validates"
      examples:
        - "ddd:AggregatePattern"
        - "data_eng:MedallionArchitecture"
        - "ux:WorkflowPattern"
      grounding:
        target_canon: ["ddd", "data_eng", "ux"]
        target_concept: "Pattern"
        grounding_type: "epistemic"
        strength: "strong"
```
**Impact:** QE closure should reach 90%+

### Phase 3: Agile Schema Enhancement (Steps 9-14)

#### Step 9: Add Agile Feature → DDD BoundedContext Grounding
**Action:** Make implicit Feature → BoundedContext mapping explicit in schema
**Specific Changes:**
```yaml
# Enhance Feature definition in Agile schema
Feature:
  type: object
  required:
    - id
    - name
    - bounded_context_ref  # NEW: Make this required
  properties:
    bounded_context_ref:
      type: string
      description: "DDD bounded context this feature belongs to"
      pattern: "^ddd:BoundedContext:[a-z0-9_-]+$"
      grounding:
        target_canon: "ddd"
        target_concept: "BoundedContext"
        grounding_type: "epistemic"
        strength: "strong"
        rationale: "Features typically align with domain boundaries"

    affects_aggregates:
      type: array
      items:
        type: string
        pattern: "^ddd:Aggregate:[a-z0-9_-]+$"
      description: "DDD aggregates modified by this feature"
      grounding:
        target_canon: "ddd"
        target_concept: "Aggregate"
        grounding_type: "structural"
        strength: "weak"
```
**Impact:** Major closure improvement, makes domain alignment explicit

#### Step 10: Add Agile Story → UX Implementation Grounding
**Action:** Create explicit links from user stories to UX artifacts they implement
**Specific Changes:**
```yaml
# Enhance Story definition in Agile schema
Story:
  type: object
  properties:
    implements_page:
      type: string
      description: "UX page this story implements or modifies"
      pattern: "^ux:Page:[a-z0-9_-]+$"
      grounding:
        target_canon: "ux"
        target_concept: "Page"
        grounding_type: "epistemic"
        strength: "weak"

    implements_workflow:
      type: string
      description: "UX workflow this story implements or modifies"
      pattern: "^ux:Workflow:[a-z0-9_-]+$"
      grounding:
        target_canon: "ux"
        target_concept: "Workflow"
        grounding_type: "epistemic"
        strength: "weak"

    implements_component:
      type: array
      items:
        type: string
        pattern: "^ux:Component:[a-z0-9_-]+$"
      description: "UX components this story implements or modifies"
      grounding:
        target_canon: "ux"
        target_concept: "Component"
        grounding_type: "epistemic"
        strength: "weak"
```
**Note:** Weak strength because not all stories are UX-focused

#### Step 11: Add Agile → QE Definition of Done Grounding
**Action:** Strengthen existing weak grounding between Agile DoD and QE coverage
**Specific Changes:**
```yaml
# Enhance Story and Sprint definitions
Story:
  properties:
    definition_of_done:
      type: object
      properties:
        test_coverage_requirement:
          type: object
          grounding:
            target_canon: "qe"
            target_concept: "Coverage"
            grounding_type: "epistemic"
            strength: "strong"
          properties:
            minimum_unit_coverage:
              type: number
              minimum: 0
              maximum: 100
              description: "Minimum unit test coverage percentage"
            requires_integration_tests:
              type: boolean
            requires_e2e_tests:
              type: boolean
            references_test_suites:
              type: array
              items:
                type: string
                pattern: "^qe:TestSuite:[a-z0-9_-]+$"
```
**Impact:** Makes quality gates explicit, strengthens Agile → QE relationship

#### Step 12: Add Agile → Data-Eng Pipeline Work Grounding
**Action:** Create explicit grounding for data pipeline work tracked in Agile
**Specific Changes:**
```yaml
# Enhance Feature and Story definitions
Feature:
  properties:
    includes_pipelines:
      type: array
      items:
        type: string
        pattern: "^data_eng:Pipeline:[a-z0-9_-]+$"
      description: "Data pipelines created or modified by this feature"
      grounding:
        target_canon: "data_eng"
        target_concept: "Pipeline"
        grounding_type: "epistemic"
        strength: "weak"
        rationale: "Features may require new data pipelines"

    affects_datasets:
      type: array
      items:
        type: string
        pattern: "^data_eng:Dataset:[a-z0-9_-]+$"
      description: "Datasets created or modified by this feature"
      grounding:
        target_canon: "data_eng"
        target_concept: "Dataset"
        grounding_type: "epistemic"
        strength: "weak"
```

#### Step 13: Add Agile Epic → DDD Domain Grounding
**Action:** Map epics to DDD domains for strategic alignment
**Specific Changes:**
```yaml
# Enhance Epic definition
Epic:
  type: object
  properties:
    targets_domain:
      type: string
      description: "DDD domain this epic primarily targets"
      pattern: "^ddd:Domain:[a-z0-9_-]+$"
      grounding:
        target_canon: "ddd"
        target_concept: "Domain"
        grounding_type: "epistemic"
        strength: "strong"
        rationale: "Epics typically align with domain boundaries"

    spans_contexts:
      type: array
      items:
        type: string
        pattern: "^ddd:BoundedContext:[a-z0-9_-]+$"
      description: "Bounded contexts affected by this epic"
      grounding:
        target_canon: "ddd"
        target_concept: "BoundedContext"
        grounding_type: "epistemic"
        strength: "strong"
```
**Impact:** Strategic alignment becomes explicit

#### Step 14: Add Agile Team → Domain Ownership Grounding
**Action:** Link teams to domains they own
**Specific Changes:**
```yaml
# Enhance Team definition
Team:
  type: object
  properties:
    owns_contexts:
      type: array
      items:
        type: string
        pattern: "^ddd:BoundedContext:[a-z0-9_-]+$"
      description: "Bounded contexts this team owns"
      grounding:
        target_canon: "ddd"
        target_concept: "BoundedContext"
        grounding_type: "epistemic"
        strength: "strong"
        rationale: "Teams typically own specific bounded contexts"

    owns_pipelines:
      type: array
      items:
        type: string
        pattern: "^data_eng:Pipeline:[a-z0-9_-]+$"
      description: "Data pipelines this team owns"
      grounding:
        target_canon: "data_eng"
        target_concept: "Pipeline"
        grounding_type: "epistemic"
        strength: "weak"
```
**Impact:** Organizational alignment with domain structure

### Phase 4: Cross-Canon Integration (Steps 15-17)

#### Step 15: Add Grounding Metadata to All Schemas
**Action:** Add explicit grounding section to each schema header
**Specific Changes:**
```yaml
# Add to top of each schema file after metadata
grounding:
  schema_version: "1.0.0"
  grounds_in:
    - canon: "ddd"
      types: ["structural", "semantic", "procedural"]
      strength: "strong"
      relationships: 5
      closure_contribution: "45%"
    - canon: "data_eng"
      types: ["structural", "semantic"]
      strength: "strong"
      relationships: 2
      closure_contribution: "15%"
  closure_percentage: 96
  target_closure: 95
  validation:
    all_references_resolve: true
    no_circular_dependencies: true
    grounding_types_valid: true
```
**Impact:** Makes grounding explicit in schema itself, not just external documentation

#### Step 16: Create Grounding Validation Rules in Schemas
**Action:** Add validation rules section to enforce grounding constraints
**Specific Changes:**
```yaml
# Add to each schema
validation_rules:
  - rule_id: "grounding_001"
    description: "All external references must use qualified names"
    pattern: "^[a-z_]+:[A-Z][a-zA-Z0-9]+:[a-z0-9_-]+$"
    severity: "error"
    examples:
      valid:
        - "ddd:BoundedContext:order-management"
        - "ux:Page:checkout"
      invalid:
        - "BoundedContext:order" # Missing canon prefix
        - "order-management" # No canon or concept type

  - rule_id: "grounding_002"
    description: "Referenced canons must be declared in grounds_in"
    validator: "check_declared_grounding"
    severity: "error"

  - rule_id: "grounding_003"
    description: "Strong groundings must have >80% reference coverage"
    validator: "check_coverage"
    severity: "warning"
```

#### Step 17: Update Interdomain-Map.yaml with New Groundings
**Action:** Add all newly created grounding relationships to interdomain-map.yaml
**Specific Changes:**
```yaml
# Add new groundings section for Agile
groundings:
  # ... existing groundings ...

  # NEW: Agile → DDD Groundings
  - id: "grounding_agile_ddd_001"
    source: "canon_agile"
    target: "canon_ddd"
    type: "epistemic"
    strength: "strong"
    description: "Agile features map to DDD bounded contexts"
    # ... (detailed as in Step 9)

  # NEW: Agile → UX Groundings
  - id: "grounding_agile_ux_001"
    source: "canon_agile"
    target: "canon_ux"
    type: "epistemic"
    strength: "weak"
    description: "Agile stories implement UX artifacts"
    # ... (detailed as in Step 10)

  # NEW: QE → Data-Eng Grounding
  - id: "grounding_qe_data_001"
    source: "canon_qe"
    target: "canon_data_eng"
    type: "procedural"
    strength: "strong"
    description: "QE contract tests validate data contracts"
    # ... (detailed as in Step 5)
```
**Update closure calculations to reflect improvements**

### Phase 5: Validation and Documentation (Steps 18-21)

#### Step 18: Create Python Validation Script with Virtual Environment
**Action:** Create automated validation tool to verify schema changes and calculate closure
**Location:** `tools/validate-schemas.py`
**Setup:**
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install pyyaml jsonschema
```
**Script Requirements:**
1. **YAML Schema Validation:** Validate all .yaml schemas are syntactically correct
2. **JSON Schema Validation:** Validate grounding-schema.json against JSON Schema spec
3. **Closure Calculation:** Calculate closure percentage for each canon
4. **Grounding Validation:** Verify all referenced canons exist and are declared
5. **Circular Dependency Check:** Ensure no cycles in grounding graph
6. **Reference Resolution:** Verify all cross-canon references resolve
**Expected Output:**
```
Schema Validation Results:
✓ domains/ddd/model-schema.yaml: Valid YAML
✓ domains/data-eng/model.schema.yaml: Valid YAML
✓ domains/ux/model-schema.yaml: Valid YAML
✓ domains/qe/model-schema.yaml: Valid YAML
✓ domains/agile/model.schema.yaml: Valid YAML
✓ research-output/grounding-schema.json: Valid JSON Schema

Closure Analysis:
✓ DDD: 100.0% closure (48/48 references resolved)
✓ Data-Eng: 100.0% closure (52/52 references resolved)
✓ UX: 96.0% closure (72/75 references resolved)
✓ QE: 95.2% closure (80/84 references resolved) [TARGET ACHIEVED]
✓ Agile: 94.8% closure (89/94 references resolved) [TARGET ACHIEVED]

System Average: 97.2% closure

Grounding Validation:
✓ All grounding targets exist
✓ No circular dependencies detected
✓ All referenced canons declared in grounds_in

Status: PRODUCTION READY ✓
```
**Acceptance Criteria:**
- All schemas pass YAML/JSON validation
- QE closure ≥95%
- Agile closure ≥95%
- No validation errors

#### Step 19: Run Closure Validation on Enhanced Schemas
**Action:** Execute validation script to verify enhancements
**Command:**
```bash
cd /Users/igor/code/canonical-grounding
source venv/bin/activate
python tools/validate-schemas.py
```
**Expected Results:**
- QE: 75% → 95%+ (target achieved)
- Agile: 72% → 95%+ (target achieved)
- System average: 89% → 97%+
**Acceptance Criteria:** Script exits with code 0 (success), all targets met

#### Step 20: Update Research Documentation with Improvements
**Action:** Update research-output documents to reflect enhancements
**Files to Update:**
1. `research-output/interdomain-map.yaml` - Add new groundings, update closure stats
2. `research-output/final-synthesis.md` - Update limitations section, remove "incomplete schemas"
3. `research-output/canonical-grounding-theory.md` - Update practical contributions section
4. `research-output/README.md` - Update status from "not production-ready" to "production-ready"
**Key Message:** "Schemas enhanced to >95% closure, now production-ready"

#### Step 21: Create Enhancement Summary and Migration Guide
**Action:** Document all changes made and provide migration guidance
**Create File:** `domains/ENHANCEMENT-SUMMARY.md`
**Contents:**
```markdown
# Schema Enhancement Summary

## Overview
Enhanced QE and Agile schemas from 75% and 72% closure to >95% closure by making implicit domain references explicit.

## Changes by Canon

### QE Canon Enhancements
- Added QE → Data-Eng contract validation grounding
- Strengthened QE → DDD invariant validation
- Added QE → UX workflow validation
- Added test strategy → domain pattern references
- Result: 75% → 95% closure (+20%)

### Agile Canon Enhancements
- Added Feature → BoundedContext grounding (required field)
- Added Story → UX artifact implementation grounding
- Strengthened DoD → QE coverage grounding
- Added Feature → Pipeline work grounding
- Added Epic → Domain grounding
- Added Team → Context ownership grounding
- Result: 72% → 95% closure (+23%)

### New Groundings Added
- grounding_qe_data_001: QE contract tests validate data contracts
- grounding_agile_ddd_001: Features map to bounded contexts
- grounding_agile_ux_001: Stories implement UX artifacts
- grounding_agile_qe_001: DoD references test coverage
- grounding_agile_data_001: Features include pipeline work
- grounding_agile_ddd_002: Epics target domains
- grounding_agile_ddd_003: Teams own contexts

## Migration Guide

### For Existing Agile Artifacts
1. Add `bounded_context_ref` to all Feature definitions
2. Optionally add `implements_page/workflow` to Stories
3. Update DoD with explicit QE test suite references

### For Existing QE Tests
1. Add `validates_invariants` references to DDD tests
2. Add `contract_validates` to contract tests
3. Add `validates_workflow` to E2E tests

## Impact
- Both schemas now >95% closure (production-ready)
- Automated validation now possible
- Expected LLM accuracy improvement: +5-10% (85% → 92-95%)
- Integration effort reduction: additional 10-15%
- Architectural alignment made explicit
```

---

## Expected Outcomes

### Quantitative Improvements
1. **Closure Rates:**
   - QE: 75% → 95% (+20 percentage points)
   - Agile: 72% → 95% (+23 percentage points)
   - System average: 89% → 97% (+8 percentage points)

2. **Grounding Relationships:**
   - Current: 15 groundings
   - After enhancement: 22 groundings (+7 new)
   - Agile groundings: 3 weak → 7 strong (+4, upgraded strength)
   - QE groundings: 4 → 7 (+3)

3. **Production Readiness:**
   - Before: Not production-ready (schemas incomplete)
   - After: Production-ready (all schemas >95% closure)

### Qualitative Improvements
1. **Explicit Domain Alignment:** Agile work now explicitly mapped to domain structure
2. **Quality Gates Clear:** QE relationship to all domains formalized
3. **Architectural Traceability:** Can trace from epic → domain → context → aggregate
4. **Team Alignment:** Team ownership of domains made explicit
5. **Automated Validation:** Can now validate cross-domain consistency automatically

### Research Impact
1. **Limitation Removed:** "Incomplete schemas" no longer a limitation
2. **Production Deployment:** Unblocked for production use
3. **LLM Performance:** Expected +5-10% additional improvement (total: 92-96% conformance)
4. **Case Studies:** Now ready for real practitioner validation

---

## Success Criteria

### Must Achieve (Required)
- [ ] QE schema closure ≥95%
- [ ] Agile schema closure ≥95%
- [ ] All new groundings added to interdomain-map.yaml
- [ ] Grounding validation rules in all schemas
- [ ] No circular dependencies introduced

### Should Achieve (Important)
- [ ] Agile Feature → BoundedContext made required field
- [ ] QE test → DDD invariant mapping explicit
- [ ] Agile DoD → QE coverage strengthened to "strong"
- [ ] Documentation updated (research-output files)
- [ ] Enhancement summary created

### Could Achieve (Nice to Have)
- [ ] Example files updated with new grounding references
- [ ] Visual grounding diagram generated
- [ ] Migration scripts for existing artifacts
- [ ] Automated validation tool implementation

---

## Implementation Priority

**High Priority (Complete First):**
- Steps 9-11: Agile → DDD, UX, QE groundings (biggest closure impact)
- Steps 5-6: QE → Data-Eng, DDD groundings (completes QE foundation)
- Step 17: Update interdomain-map.yaml (documents changes formally)

**Medium Priority (Complete Second):**
- Steps 12-14: Additional Agile groundings (refines relationships)
- Steps 7-8: Additional QE groundings (achieves >95% target)
- Steps 18-20: Validation and documentation (proves success)

**Lower Priority (Complete Last):**
- Steps 1-4: Analysis (use for validation, not blocking)
- Steps 15-16: Metadata and validation rules (improves automation)
- Step 21: Migration guide (helps adoption)

---

## Notes for Implementation

1. **Use Existing Patterns:** Reference interdomain-map.yaml existing groundings as templates for new ones
2. **Preserve Backward Compatibility:** Make new fields optional where possible, use deprecation for breaking changes
3. **Follow Naming Conventions:** Use canonical prefixes (`ddd:`, `ux:`, `qe:`, `data_eng:`, `agile:`)
4. **Document Rationale:** Each grounding should have clear rationale in comments
5. **Reference Documentation:** Use existing docs/ directories to inform grounding decisions
6. **Test with Examples:** Update example files to demonstrate new groundings in practice

---

## Success Metrics

**Before Enhancement:**
- QE closure: 75%
- Agile closure: 72%
- Total groundings: 15
- Status: Not production-ready
- LLM conformance: 80-90%

**After Enhancement (Target):**
- QE closure: ≥95%
- Agile closure: ≥95%
- Total groundings: ≥22
- Status: Production-ready
- LLM conformance: 92-96%

**Validation:** Run closure calculation algorithm on enhanced schemas to verify targets achieved.
