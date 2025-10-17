# Agile Schema Partition - Concept Mapping

## Overview
This document maps all 35 concepts from the original monolithic schema to their new partitioned schema locations.

---

## Partition 1: Portfolio Schema (8 concepts)

| Original Concept | New Location | Lines | Description |
|-----------------|--------------|-------|-------------|
| `portfolio` | portfolio-agile.schema.yaml | ~40 | Portfolio management and governance |
| `value_stream` | portfolio-agile.schema.yaml | ~30 | End-to-end value delivery flow |
| `epic` | portfolio-agile.schema.yaml | ~100 | Large initiatives spanning programs |
| `roadmap` | portfolio-agile.schema.yaml | ~130 | Strategic view of deliverables over time |
| `stakeholder` | portfolio-agile.schema.yaml | ~35 | Key stakeholders in portfolio/product |
| `metric` | portfolio-agile.schema.yaml | ~30 | Business or product metrics |
| `non_functional_requirement` | portfolio-agile.schema.yaml | ~40 | Quality attributes and constraints (NFRs) |
| `risk` | portfolio-agile.schema.yaml | ~35 | Portfolio or program risks |

**Total:** 8 concepts, 477 lines

---

## Partition 2: Program Schema (7 concepts)

| Original Concept | New Location | Lines | Description |
|-----------------|--------------|-------|-------------|
| `Program` | program-agile.schema.yaml | ~50 | Program or Agile Release Train |
| `program_increment` | program-agile.schema.yaml | ~120 | Time-boxed planning increment (8-12 weeks) |
| `architectural_runway` | program-agile.schema.yaml | ~45 | Technical foundation for future functionality |
| `enabler` | program-agile.schema.yaml | ~45 | Work item extending architectural runway |
| `release` | program-agile.schema.yaml | ~150 | Time-boxed delivery of value |
| `release_vision` | program-agile.schema.yaml | ~120 | Focused vision for specific release |
| `technical_debt` | program-agile.schema.yaml | ~45 | Technical debt requiring remediation |

**Total:** 7 concepts, 586 lines

---

## Partition 3: Team Schema (10 concepts)

| Original Concept | New Location | Lines | Description |
|-----------------|--------------|-------|-------------|
| `team` | team-agile.schema.yaml | ~90 | Agile team (5-11 people) |
| `team_member` | team-agile.schema.yaml | ~30 | Individual team member |
| `team_topology` | team-agile.schema.yaml | ~30 | Team type and interaction patterns |
| `role` | team-agile.schema.yaml | ~35 | Agile role with defined responsibilities |
| `sprint` | team-agile.schema.yaml | ~150 | Time-boxed iteration in Scrum (1-4 weeks) |
| `iteration` | team-agile.schema.yaml | ~50 | Time-boxed iteration in SAFe (2 weeks) |
| `ceremony` | team-agile.schema.yaml | ~35 | Agile ceremony or event |
| `working_agreement` | team-agile.schema.yaml | ~35 | Team norms and practices |
| `impediment` | team-agile.schema.yaml | ~40 | Blocker or obstacle preventing progress |
| `feedback_loop` | team-agile.schema.yaml | ~35 | Mechanism for gathering feedback |

**Total:** 10 concepts, 621 lines

---

## Partition 4: Delivery Schema (8 concepts)

| Original Concept | New Location | Lines | Description |
|-----------------|--------------|-------|-------------|
| `product` | delivery-agile.schema.yaml | ~70 | Primary organizational unit (solution) |
| `vision` | delivery-agile.schema.yaml | ~130 | Comprehensive product vision |
| `feature` | delivery-agile.schema.yaml | ~120 | Service provided by system (PI-sized) |
| `user_story` | delivery-agile.schema.yaml | ~140 | Small, vertical slice of functionality |
| `task` | delivery-agile.schema.yaml | ~35 | Technical task for implementing story |
| `increment` | delivery-agile.schema.yaml | ~30 | Potentially shippable product increment |
| `definition_of_ready` | delivery-agile.schema.yaml | ~25 | Criteria for work items before sprint |
| `estimation_technique` | delivery-agile.schema.yaml | ~30 | Technique for estimating work items |

**Total:** 8 concepts, 659 lines

---

## Partition 5: SAFe Extensions Schema (2 concepts)

| Original Concept | New Location | Lines | Description |
|-----------------|--------------|-------|-------------|
| `agile_release_train` | safe-agile.schema.yaml | ~70 | Long-lived team of agile teams (50-125 people) |
| `cadence` | safe-agile.schema.yaml | ~70 | Regular rhythm for team/ART activities |

**Total:** 2 concepts, 183 lines

---

## Cross-Partition Reference Patterns

### Portfolio → Program
```yaml
epic:
  program_refs:  # "^prg_[a-z0-9_]+$"
```

### Portfolio → Delivery
```yaml
epic:
  feature_refs:  # "^feat_[a-z0-9_]+$"
```

### Program → Portfolio
```yaml
Program:
  portfolio_ref:  # "^pf_[a-z0-9_]+$"
```

### Program → Team
```yaml
Program:
  team_refs:  # "^tm_[a-z0-9_]+$"
```

### Team → Program
```yaml
team:
  program_ref:  # "^prg_[a-z0-9_]+$"
```

### Team → Delivery
```yaml
sprint:
  committed_story_refs:  # "^us_[a-z0-9_]+$"
```

### Delivery → Portfolio
```yaml
product:
  portfolio_ref:  # "^pf_[a-z0-9_]+$"
```

### Delivery → Program
```yaml
feature:
  pi_ref:  # "^pi_[a-z0-9_]+$"
```

### Delivery → Team
```yaml
user_story:
  sprint_ref:  # "^sp_[a-z0-9_]+$"
```

### SAFe → Program
```yaml
agile_release_train:
  program_ref:  # "^prg_[a-z0-9_]+$"
```

### SAFe → Team
```yaml
agile_release_train:
  team_refs:  # "^tm_[a-z0-9_]+$"
```

---

## Cross-Domain Groundings

### To DDD Domain
**Location:** delivery-agile.schema.yaml
```yaml
feature:
  bounded_context_ref:  # "^ddd:BoundedContext:[a-z0-9_-]+$"

enabler:
  bounded_context_ref:  # "^ddd:BoundedContext:[a-z0-9_-]+$"

technical_debt:
  bounded_context_ref:  # "^ddd:BoundedContext:[a-z0-9_-]+$"
  aggregate_ref:        # "^ddd:Aggregate:[a-z0-9_-]+$"
```

### To UX Domain
**Location:** delivery-agile.schema.yaml
```yaml
user_story:
  ux_artifact_refs:
    page_refs:       # "^ux:Page:[a-z0-9_-]+$"
    component_refs:  # "^ux:Component:[a-z0-9_-]+$"
    workflow_refs:   # "^ux:Workflow:[a-z0-9_-]+$"
```

### To QE Domain
**Location:** team-agile.schema.yaml
```yaml
sprint:
  definitionOfDone:
    test_criteria_refs:  # "^qe:TestCriteria:[a-z0-9_-]+$"
    checklist:
      qe_validation_ref: # "^qe:(TestCase|TestSuite|TestStrategy):[a-z0-9_-]+$"
```

---

## Migration Path

### For Existing References

**Before (Monolithic):**
```yaml
epic:
  program:
    $ref: '#/$defs/Program'
```

**After (Partitioned):**
```yaml
epic:
  program_ref: "prg_mobile_platform"  # String ID reference
```

---

## Naming Convention Summary

| Partition | Prefix Examples |
|-----------|----------------|
| Portfolio | `pf_`, `vs_`, `epic_`, `rm_`, `sh_`, `met_`, `nfr_`, `risk_` |
| Program | `prg_`, `pi_`, `ar_`, `enb_`, `rel_`, `rv_`, `td_` |
| Team | `tm_`, `mbr_`, `tt_`, `role_`, `sp_`, `it_`, `cer_`, `wa_`, `imp_`, `fb_` |
| Delivery | `prod_`, `vis_`, `feat_`, `us_`, `tsk_`, `inc_`, `dor_`, `est_` |
| SAFe | `art_`, `cad_` |

---

## Concept Count by Partition

```
Portfolio:  ████████  8 concepts (23%)
Program:    ███████   7 concepts (20%)
Team:       ██████████ 10 concepts (29%)
Delivery:   ████████  8 concepts (23%)
SAFe:       ██        2 concepts (5%)
            ─────────────────────────
Total:                35 concepts
```

---

## Verification Checklist

- [x] All 35 concepts extracted from original schema
- [x] Each concept placed in appropriate partition
- [x] No concept duplicated across partitions
- [x] All cross-partition references use string patterns
- [x] All cross-domain groundings preserved
- [x] Naming conventions defined for each partition
- [x] Metadata included in each schema
- [x] Validation rules defined
- [x] Best practices documented

---

**Document Version:** 1.0  
**Generated:** 2025-10-17  
**Status:** Complete
