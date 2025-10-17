# Documentation Remediation Plan
**Version:** 1.0
**Date:** 2025-10-14
**Status:** Ready for Execution
**Goal:** Achieve ≥95% schema-documentation alignment across all 5 domains

---

## Executive Summary

**Current State:**
- 1 of 5 domains at 100% coverage (DDD)
- 4 domains below 70% coverage
- 44 total concepts missing from documentation
- 21 concepts were added in Phase 4 schema enhancements

**Target State:**
- All 5 domains ≥95% coverage
- All 119 schema concepts documented
- All examples validated against schemas

**Total Effort:** 18-24 hours over 2-3 weeks

---

## Phase 1: Data Engineering Documentation (Priority: HIGH)

### 1.1 Missing Concepts (11 total)

**NEW in Phase 4 (2 concepts) - 2-3 hours:**

| Concept | Target Doc | Section | Effort | Priority |
|---------|-----------|---------|--------|----------|
| `data_product` | 30-architecture.md | §3 Data Products | 45m | P0 |
| `data_quality_dimension` | quick-reference.md | Quality Dimensions | 30m | P0 |

**Content Requirements - data_product:**
```markdown
### Data Products

A **data product** is a self-contained, discoverable data asset with:
- **Owner**: Accountable team/person
- **Bounded Context**: DDD alignment
- **Datasets**: Constituent data assets
- **SLOs**: Quality and availability guarantees
- **Contracts**: Consumer agreements

**Schema Pattern:**
- ID format: `dp-<name>`
- Required: owner, datasets
- Optional: bounded_context_ref (DDD grounding)

**Example:**
dp-customer-360: Customer data product owned by CRM team
```

**Content Requirements - data_quality_dimension:**
```markdown
### Data Quality Dimensions

Standard quality measurement dimensions:
- **Accuracy**: Correctness of values
- **Completeness**: No missing required fields
- **Timeliness**: Data freshness/latency
- **Consistency**: Agreement across sources

Used in: quality_rule, dataset.quality_dimensions
```

---

**Utility Concepts (9 concepts) - 3-4 hours:**

| Concept | Target Doc | Section | Effort | Priority |
|---------|-----------|---------|--------|----------|
| `data_access_pattern` | 30-architecture.md | §4 Access Patterns | 20m | P1 |
| `data_catalog_entry` | 30-architecture.md | §5 Cataloging | 20m | P1 |
| `data_monitoring_metric` | quick-reference.md | Observability | 15m | P1 |
| `data_partition_strategy` | 30-architecture.md | §6 Partitioning | 20m | P1 |
| `data_pipeline_template` | 70-how-to-model-systems.md | Templates | 25m | P2 |
| `data_replication_config` | 30-architecture.md | §7 Replication | 20m | P2 |
| `data_retention_tier` | 30-architecture.md | §8 Retention | 15m | P2 |
| `data_transformation_function` | quick-reference.md | Transformations | 20m | P1 |
| `data_validation_rule_type` | quick-reference.md | Validation | 20m | P1 |

**Template for Utility Concepts:**
```markdown
#### <ConceptName>

**Purpose**: <One sentence>
**Used in**: <Parent concepts that reference this>
**Schema fields**: <2-3 key properties>
**Example**: <Concrete instance>
```

---

### 1.2 Deliverables

- [ ] Updated `30-architecture.md` (+8 concepts, 6 new sections)
- [ ] Updated `quick-reference.md` (+5 concepts in existing sections)
- [ ] Updated `70-how-to-model-systems.md` (+1 template pattern)
- [ ] Validation: 26/26 concepts = 100% coverage

**Files to Update:**
```bash
domains/data-eng/docs/30-architecture.md         # +1,200 words
domains/data-eng/docs/quick-reference.md         # +600 words
domains/data-eng/docs/70-how-to-model-systems.md # +400 words
```

---

## Phase 2: UX Documentation (Priority: HIGH)

### 2.1 Missing Concepts (9 total)

**NEW in Phase 4 (4 concepts) - 2-3 hours:**

| Concept | Target Doc | Section | Effort | Priority |
|---------|-----------|---------|--------|----------|
| `hierarchy_node` | ux-01-ia-foundations.md | §2.3 Hierarchy | 40m | P0 |
| `facet_value` | ux-01-ia-foundations.md | §2.4 Facets | 30m | P0 |
| `responsive_config` | ux-05-component-architecture.md | §4 Responsive | 30m | P0 |
| `validation_config` | ux-06-behavior-specifications.md | §3 Validation | 40m | P0 |

**Content Requirements - hierarchy_node:**
```markdown
### 2.3 Hierarchical Navigation

A **hierarchy_node** represents a node in a tree-structured IA:

**Properties:**
- `id`: Unique node identifier (node_<name>)
- `label`: Display text
- `bounded_context`: DDD context alignment (grounding)
- `url`: Navigation target
- `children`: Child node references

**Example:**
node_products → node_electronics → node_laptops

**DDD Grounding:** hierarchy_node.bounded_context → ddd:BoundedContext
Maps IA structure to domain boundaries.
```

**Content Requirements - facet_value:**
```markdown
### 2.4 Faceted Classification

**facet_value** instances for filtering:

**Properties:**
- `value_id`: Unique identifier
- `label`: Display text
- `count`: Number of matching items
- `ddd_value_object_ref`: Maps to domain concept

**Example Facet:**
Brand facet with values: Apple (245), Dell (189), HP (156)

**DDD Grounding:** facet.ddd_value_object_refs → ddd:ValueObject
Filters map to domain value objects.
```

---

**Utility Concepts (5 concepts) - 1.5-2 hours:**

| Concept | Target Doc | Section | Effort | Priority |
|---------|-----------|---------|--------|----------|
| `accessibility_spec` | ux-06-behavior-specifications.md | §5 A11y | 25m | P1 |
| `caching_config` | ux-07-scalability-patterns.md | §2 Caching | 20m | P2 |
| `design_tokens` | ux-05-component-architecture.md | §2 Tokens | 20m | P1 |
| `page_section` | ux-04-page-architecture.md | §3 Sections | 15m | P1 |
| `pagination_config` | ux-04-page-architecture.md | §4 Pagination | 20m | P1 |

---

### 2.2 Deliverables

- [ ] Updated `ux-01-ia-foundations.md` (+2 concepts, 2 sections)
- [ ] Updated `ux-04-page-architecture.md` (+2 concepts)
- [ ] Updated `ux-05-component-architecture.md` (+2 concepts)
- [ ] Updated `ux-06-behavior-specifications.md` (+2 concepts)
- [ ] Updated `ux-07-scalability-patterns.md` (+1 concept)
- [ ] Validation: 18/18 concepts = 100% coverage

**Files to Update:**
```bash
domains/ux/docs/ux-01-ia-foundations.md          # +900 words
domains/ux/docs/ux-04-page-architecture.md       # +400 words
domains/ux/docs/ux-05-component-architecture.md  # +400 words
domains/ux/docs/ux-06-behavior-specifications.md # +600 words
domains/ux/docs/ux-07-scalability-patterns.md    # +200 words
```

---

## Phase 3: QE Documentation (Priority: MEDIUM)

### 3.1 Missing Concepts (9 total)

**NEW in Phase 4 (2 concepts) - 1.5-2 hours:**

| Concept | Target Doc | Section | Effort | Priority |
|---------|-----------|---------|--------|----------|
| `coverage_target` | qe-03-domain-II-ontologies.md | ROoST Metrics | 35m | P0 |
| `test_oracle` | qe-03-domain-II-ontologies.md | ROoST Artifacts | 40m | P0 |

**Content Requirements - coverage_target:**
```markdown
### Coverage Targets (ROoST: Test Metrics)

A **coverage_target** defines testing goals:

**Properties:**
- `target_id`: Unique identifier
- `metric_type`: statement | branch | path | mutation
- `target_percentage`: 0.0-100.0
- `bounded_context_ref`: DDD scope (grounding)
- `aggregate_ref`: DDD aggregate scope (grounding)

**Example:**
coverage_target_payment: 90% branch coverage for Payment aggregate

**DDD Grounding:** coverage_target → ddd:Aggregate
Testing goals map to aggregate boundaries.
```

**Content Requirements - test_oracle:**
```markdown
### Test Oracles (ROoST: Artifacts)

A **test_oracle** determines correctness:

**Types:**
- **Value oracle**: Expected output value
- **State oracle**: Expected system state
- **Behavior oracle**: Expected sequence/interaction

**Properties:**
- `oracle_id`: Unique identifier
- `type`: value | state | behavior
- `expected_outcome`: Assertion definition
- `comparison_method`: Validation strategy

**Example:**
Value oracle: assertEqual(result, 42)
State oracle: assertUserLoggedIn()
Behavior oracle: assertEmailSent()
```

---

**Utility Concepts (7 concepts) - 2-3 hours:**

| Concept | Target Doc | Section | Effort | Priority |
|---------|-----------|---------|--------|----------|
| `test_assertion` | qe-15-qe-knowledge-base.md | Assertions | 20m | P1 |
| `test_coverage_type` | qe-03-domain-II-ontologies.md | Coverage | 15m | P1 |
| `test_execution_order` | qe-15-qe-knowledge-base.md | Execution | 15m | P2 |
| `test_harness` | qe-08-domain-VIII-automation.md | Harness | 25m | P1 |
| `test_priority_scheme` | qe-15-qe-knowledge-base.md | Prioritization | 20m | P2 |
| `test_stakeholder_role` | qe-03-domain-II-ontologies.md | Stakeholders | 20m | P1 |
| `testing_technique_spec` | qe-06-domain-VI-design-techniques.md | Techniques | 25m | P1 |

---

### 3.2 Deliverables

- [ ] Updated `qe-03-domain-II-ontologies.md` (+5 concepts in ROoST)
- [ ] Updated `qe-06-domain-VI-design-techniques.md` (+1 concept)
- [ ] Updated `qe-08-domain-VIII-automation.md` (+1 concept)
- [ ] Updated `qe-15-qe-knowledge-base.md` (+3 concepts)
- [ ] Validation: 27/27 concepts = 100% coverage

**Files to Update:**
```bash
domains/qe/docs/qe-03-domain-II-ontologies.md    # +1,000 words
domains/qe/docs/qe-06-domain-VI-design-techniques.md # +300 words
domains/qe/docs/qe-08-domain-VIII-automation.md  # +300 words
domains/qe/docs/qe-15-qe-knowledge-base.md       # +600 words
```

---

## Phase 4: Agile Documentation (Priority: MEDIUM)

### 4.1 Missing Concepts (15 total)

**NEW in Phase 4 (3 concepts) - 2-3 hours:**

| Concept | Target Doc | Section | Effort | Priority |
|---------|-----------|---------|--------|----------|
| `NonFunctionalRequirement` | scope-and-nfrs.md | §2 NFRs | 50m | P0 |
| `TechnicalDebt` | guide-to-agile.md | §7 Debt | 40m | P0 |
| `EstimationTechnique` | guide-to-agile.md | §5 Estimation | 35m | P0 |

**Content Requirements - NonFunctionalRequirement:**
```markdown
### 2. Non-Functional Requirements (NFRs)

**NonFunctionalRequirement** defines quality attributes:

**Categories:**
- Performance: Response time, throughput
- Security: Authentication, authorization, encryption
- Scalability: Load handling, elasticity
- Usability: Accessibility, learnability
- Reliability: Uptime, fault tolerance
- Maintainability: Code quality, testability

**Schema Pattern:**
- ID format: `NFR-<number>`
- Required: category, description, acceptanceCriteria
- Optional: qualityMetricRefs (QE grounding)

**Example:**
NFR-101: API response time < 200ms at p95 under 1000 req/s

**QE Grounding:** nfr.qualityMetricRefs → qe:quality_metric
NFRs define acceptance criteria for QE validation.
```

**Content Requirements - TechnicalDebt:**
```markdown
### 7. Technical Debt Management

**TechnicalDebt** tracks architectural shortcuts:

**Properties:**
- `debtId`: Unique identifier (DEBT-<number>)
- `description`: What was compromised
- `impact`: business | performance | maintainability | security
- `priority`: critical | high | medium | low
- `boundedContextRef`: DDD scope (grounding)
- `aggregateRef`: Specific aggregate affected (grounding)
- `estimatedEffort`: Hours to remediate

**Example:**
DEBT-045: Payment validation bypassed in checkout flow
Impact: security (high priority)
Context: bc_payments → ddd:BoundedContext

**DDD Grounding:** TechnicalDebt → ddd:BoundedContext
Debt tracked at domain boundary level.
```

---

**SAFe Concepts (12 concepts) - 3-4 hours:**

| Concept | Target Doc | Section | Effort | Priority |
|---------|-----------|---------|--------|----------|
| `UserStory` | guide-to-agile.md | §3 Stories | 25m | P0 |
| `AgileReleaseTrain` | vision.md | §4 ART | 30m | P1 |
| `ProgramIncrement` | vision.md | §5 PI Planning | 25m | P1 |
| `ValueStream` | vision.md | §2 Value Streams | 20m | P1 |
| `ArchitecturalRunway` | guide-to-agile.md | §8 Runway | 25m | P2 |
| `DefinitionOfReady` | guide-to-agile.md | §4 DoR | 20m | P1 |
| `FeedbackLoop` | guide-to-agile.md | §9 Feedback | 20m | P2 |
| `TeamMember` | guide-to-agile.md | §6 Team | 15m | P1 |
| `TeamTopology` | guide-to-agile.md | §6 Topologies | 25m | P2 |
| `ReleaseVision` | vision.md | §3 Vision | 20m | P1 |
| `WorkingAgreement` | guide-to-agile.md | §6 Agreements | 20m | P2 |
| `Metadata` | guide-to-agile.md | Appendix | 10m | P3 |

---

### 4.2 Deliverables

- [ ] Updated `vision.md` (+5 concepts, 3 new sections)
- [ ] Updated `scope-and-nfrs.md` (+1 concept, expanded §2)
- [ ] Updated `guide-to-agile.md` (+9 concepts, 5 new sections)
- [ ] Validation: 35/35 concepts = 100% coverage

**Files to Update:**
```bash
domains/agile/docs/vision.md                     # +1,200 words
domains/agile/docs/scope-and-nfrs.md             # +600 words
domains/agile/docs/guide-to-agile.md             # +2,000 words
```

---

## Phase 5: Example Validation & Update (Priority: LOW)

### 5.1 Example Files to Validate (14 total)

**Domain Examples:**

| Domain | Example Files | Validation Effort | Update Effort |
|--------|--------------|------------------|---------------|
| DDD | ddd-schema-example.yaml | 10m | 0-15m |
| UX | ux-schema-example.yaml | 10m | 0-15m |
| QE | qe-schema-example.yaml | 10m | 0-15m |
| Data-Eng | 4 files (iot, ml-features, payments, retail) | 40m | 0-30m |
| Agile | 5 files (ART, sprints, releases, products) | 50m | 0-45m |

**Total:** 2-3 hours (validation + updates if needed)

---

### 5.2 Validation Script

```bash
#!/bin/bash
# validate-all-examples.sh

for example in domains/*/examples/**/*.yaml domains/*/*-example.yaml; do
  echo "Validating: $example"
  python3 tools/validate-example.py "$example"
done
```

**Deliverables:**
- [ ] Create `tools/validate-example.py` script (30m)
- [ ] Validate all 14 example files (2h)
- [ ] Update examples to use new concepts (0-2h, if needed)
- [ ] Generate example validation report

---

## Phase 6: Research Documentation Updates (Priority: MEDIUM)

### 6.1 Core Research Documents

| Document | Updates Needed | Effort | Priority |
|----------|----------------|--------|----------|
| canonical-grounding-theory.md | Update concept counts, closure metrics | 30m | P1 |
| research-summary.md | Update practical findings | 20m | P1 |
| CHANGELOG-v2.md | Add Phase 4 entry | 15m | P1 |
| phase3-empirical-validation.md | Add schema validation results | 25m | P2 |
| phase4-formalization-complete.md | Add completeness section | 20m | P2 |
| phase5-synthesis-complete.md | Update deliverables | 20m | P2 |

**Total:** 2-2.5 hours

---

### 6.2 Interdomain Map Validation

**Task:** Verify all 28 groundings reference valid schema concepts

**Script:**
```python
# tools/validate-grounding-references.py
# For each grounding in interdomain-map.yaml:
#   1. Extract source_concept and target_concept
#   2. Verify concept exists in source schema $defs
#   3. Verify concept exists in target schema $defs
#   4. Report broken references
```

**Effort:** 1-1.5 hours (script creation + validation)

**Deliverable:**
- [ ] Create validation script
- [ ] Run validation
- [ ] Fix any broken references (if found)
- [ ] Generate grounding validation report

---

## Execution Timeline

### Week 1: High-Priority Domains (12-15 hours)

**Day 1-2: Data-Eng (5-6 hours)**
- Document 2 new Phase 4 concepts (data_product, data_quality_dimension)
- Document 9 utility concepts
- Validate coverage: 26/26 = 100%

**Day 3-4: UX (4-5 hours)**
- Document 4 new Phase 4 concepts (hierarchy_node, facet_value, responsive_config, validation_config)
- Document 5 utility concepts
- Validate coverage: 18/18 = 100%

**Day 5: QE (3-4 hours)**
- Document 2 new Phase 4 concepts (coverage_target, test_oracle)
- Document 7 utility concepts
- Validate coverage: 27/27 = 100%

---

### Week 2: Medium-Priority Tasks (8-10 hours)

**Day 1-2: Agile (5-7 hours)**
- Document 3 new Phase 4 concepts (NFR, TechnicalDebt, EstimationTechnique)
- Document 12 SAFe concepts
- Validate coverage: 35/35 = 100%

**Day 3: Research Docs (2-3 hours)**
- Update 6 research documents
- Validate interdomain-map.yaml groundings

---

### Week 3: Completion & Validation (3-5 hours)

**Day 1: Example Validation (2-3 hours)**
- Create validation script
- Validate all 14 examples
- Update examples if needed

**Day 2: Final Validation (1-2 hours)**
- Run all validation scripts
- Generate final validation report
- Update documentation validation plan status

---

## Success Criteria

### Must-Have (Required for Completion)

- [x] All 5 domains ≥95% schema-documentation alignment
- [x] All 44 missing concepts documented
- [x] All documentation validated with automated scripts
- [x] All examples validate against schemas

### Should-Have (Quality Targets)

- [ ] All new concepts have examples
- [ ] All DDD groundings explained in documentation
- [ ] All cross-references between docs work
- [ ] Consistent formatting across all domains

### Nice-to-Have (Future Enhancements)

- [ ] Glossary with all 119 concepts
- [ ] Comprehensive tutorial using all concepts
- [ ] Mermaid diagrams for complex concepts
- [ ] API documentation for schemas

---

## Effort Summary

| Phase | Hours | Priority | Deliverables |
|-------|-------|----------|--------------|
| Phase 1: Data-Eng | 5-7h | HIGH | 11 concepts, 3 docs |
| Phase 2: UX | 4-5h | HIGH | 9 concepts, 5 docs |
| Phase 3: QE | 3-4h | MEDIUM | 9 concepts, 4 docs |
| Phase 4: Agile | 5-7h | MEDIUM | 15 concepts, 3 docs |
| Phase 5: Examples | 2-3h | LOW | 14 validated examples |
| Phase 6: Research | 3-4h | MEDIUM | 6 docs, grounding validation |
| **TOTAL** | **22-30h** | | **44 concepts, 21 docs** |

---

## Risk Mitigation

### Risk 1: Concept Definitions Unclear
**Likelihood:** Medium
**Impact:** High
**Mitigation:** Reference original schema definitions, use examples from existing code

### Risk 2: Documentation Conflicts
**Likelihood:** Low
**Impact:** Medium
**Mitigation:** Review existing docs before adding, maintain consistent terminology

### Risk 3: Schema Changes During Documentation
**Likelihood:** Low
**Impact:** High
**Mitigation:** Lock schemas during documentation phase, validate frequently

### Risk 4: Time Overrun
**Likelihood:** Medium
**Impact:** Low
**Mitigation:** Prioritize P0/P1 concepts first, defer P2/P3 if needed

---

## Next Steps

### Immediate Actions (Today)

1. **Review and approve this plan** (15m)
2. **Create documentation branches** (10m)
   ```bash
   git checkout -b docs/data-eng-remediation
   git checkout -b docs/ux-remediation
   git checkout -b docs/qe-remediation
   git checkout -b docs/agile-remediation
   ```
3. **Start Phase 1: Data-Eng documentation** (begin Day 1)

### This Week

- Complete Data-Eng documentation (Day 1-2)
- Complete UX documentation (Day 3-4)
- Begin QE documentation (Day 5)

### Next Week

- Complete QE documentation
- Complete Agile documentation
- Update research documents

### Week 3

- Validate all examples
- Final validation pass
- Merge documentation branches
- Update final-synthesis.md with completion status

---

## Automation Opportunities

### Scripts to Create

1. **validate-schema-docs-alignment.py** ✅ (already created)
2. **validate-example.py** (Phase 5)
3. **validate-grounding-references.py** (Phase 6)
4. **generate-glossary.py** (nice-to-have)
5. **validate-cross-references.py** (nice-to-have)

### CI/CD Integration (Future)

```yaml
# .github/workflows/validate-docs.yml
name: Validate Documentation
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Validate schema-docs alignment
        run: |
          for domain in ddd data-eng ux qe agile; do
            python3 tools/validate-schema-docs-alignment.py $domain
          done
      - name: Validate examples
        run: ./tools/validate-all-examples.sh
      - name: Validate groundings
        run: python3 tools/validate-grounding-references.py
```

---

## Appendix A: Documentation Templates

### Template: New Concept (Phase 4 additions)

```markdown
### <ConceptName>

**Purpose:** <One-sentence description>

**Introduced:** Schema v1.0 (Phase 4 enhancement)

**Properties:**
- `<field1>`: <description>
- `<field2>`: <description>
- `<field3>`: <description>

**Schema Pattern:**
<id_format>: `<pattern>`
Required: <fields>
Optional: <fields>

**Example:**
<concrete_instance>

**Cross-Domain Grounding:**
<concept> → <target_domain>:<target_concept>
<explanation_of_relationship>

**Related Concepts:**
- <related_concept_1>
- <related_concept_2>

**Usage:**
<where_and_how_to_use>
```

### Template: Utility Concept

```markdown
#### <ConceptName>

**Purpose**: <One sentence>
**Used in**: <Parent concepts>
**Example**: <Concrete instance>
```

---

## Appendix B: Validation Checklist

After completing each phase, verify:

- [ ] All missing concepts documented
- [ ] All concepts have schema pattern explanation
- [ ] All concepts have at least one example
- [ ] All DDD groundings explained (if applicable)
- [ ] Validation script passes with 100% coverage
- [ ] Cross-references to other docs are valid
- [ ] Consistent formatting with existing docs
- [ ] No typos or grammatical errors
- [ ] Git commit with descriptive message

---

*Plan Status: Ready for Execution*
*Next Review: After Phase 1 completion*
