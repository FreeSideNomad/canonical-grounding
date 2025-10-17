# Agile Schema Partition Summary

**Date**: 2025-10-17
**Status**: ✅ Complete
**Original Schema**: 1,972 lines (model.schema.yaml)
**Partitioned Into**: 5 schemas (2,526 lines total)

---

## Created Schemas

### 1. Portfolio Schema (477 lines)
**File**: `schemas/portfolio-agile.schema.yaml`
**$id**: `https://canonical-grounding.org/schemas/agile/portfolio/v1`

**Concepts** (8):
- `portfolio` - Portfolio management and governance
- `value_stream` - End-to-end value flow
- `epic` - Large body of work spanning multiple features
- `roadmap` - Strategic view of deliverables over time
- `stakeholder` - Key stakeholders
- `metric` - Business or product metrics
- `non_functional_requirement` - Quality attributes and constraints
- `risk` - Portfolio or program risks

**Purpose**: Strategic planning and portfolio-level coordination

---

### 2. Program Schema (586 lines)
**File**: `schemas/program-agile.schema.yaml`
**$id**: `https://canonical-grounding.org/schemas/agile/program/v1`

**Concepts** (7):
- `Program` - Program or Agile Release Train
- `program_increment` - Time-boxed planning increment (8-12 weeks)
- `architectural_runway` - Technical foundation for future functionality
- `enabler` - Work item that extends architectural runway
- `release` - Time-boxed delivery of value
- `release_vision` - Focused vision for a specific release
- `technical_debt` - Technical debt requiring remediation

**Purpose**: Program-level coordination and PI planning

---

### 3. Team Schema (621 lines)
**File**: `schemas/team-agile.schema.yaml`
**$id**: `https://canonical-grounding.org/schemas/agile/team/v1`

**Concepts** (10):
- `team` - Agile team (5-11 people)
- `team_member` - Individual team member
- `team_topology` - Team type and interaction patterns
- `role` - Agile role with defined responsibilities
- `sprint` - Time-boxed iteration (1-4 weeks)
- `iteration` - Time-boxed iteration in SAFe (typically 2 weeks)
- `ceremony` - Agile ceremony or event
- `working_agreement` - Team norms and practices
- `impediment` - Blocker or obstacle preventing progress
- `feedback_loop` - Mechanism for gathering and acting on feedback

**Purpose**: Team-level organization and execution

---

### 4. Delivery Schema (659 lines)
**File**: `schemas/delivery-agile.schema.yaml`
**$id**: `https://canonical-grounding.org/schemas/agile/delivery/v1`

**Concepts** (8):
- `product` - Primary organizational unit representing the solution
- `vision` - Comprehensive product vision
- `feature` - Service provided by the system
- `user_story` - Small, vertical slice of functionality
- `task` - Technical task for implementing a story
- `increment` - Potentially shippable product increment
- `definition_of_ready` - Criteria for work items before sprint
- `estimation_technique` - Technique for estimating work items

**Purpose**: Product delivery and backlog management

---

### 5. SAFe Extensions Schema (183 lines)
**File**: `schemas/safe-agile.schema.yaml`
**$id**: `https://canonical-grounding.org/schemas/agile/safe/v1`

**Concepts** (2):
- `agile_release_train` - Long-lived team of agile teams (50-125 people)
- `cadence` - Regular rhythm for team and ART activities

**Purpose**: SAFe-specific extensions and patterns

---

## Key Features

### Cross-Partition References
All schemas use **string pattern references** instead of JSON Schema `$ref` for loose coupling:

```yaml
# Portfolio → Program
epic:
  properties:
    program_refs:
      type: array
      items:
        type: string
        pattern: "^prg_[a-z0-9_]+$"

# Program → Portfolio
Program:
  properties:
    portfolio_ref:
      type: string
      pattern: "^pf_[a-z0-9_]+$"
```

### Naming Conventions
Each schema defines clear ID patterns:
- Portfolio: `pf_<name>`, `vs_<name>`, `epic_<name>`
- Program: `prg_<name>`, `pi_<number>`, `rel_<name>`
- Team: `tm_<name>`, `sp_<number>`, `it_<number>`
- Delivery: `prod_<name>`, `feat_<name>`, `us_<number>`
- SAFe: `art_<name>`, `cad_<name>`

### Cross-Domain Groundings
Schemas include explicit cross-domain groundings:
- **DDD**: `bounded_context_ref` in features
- **UX**: `ux_artifact_refs` in user stories
- **QE**: `test_criteria_refs` in sprint definition of done

### Metadata
Each schema includes:
- Author, creation date, version
- License (MIT)
- Partition identifier
- References to SAFe/Scrum guides
- Validation rules
- Best practices

---

## Statistics

| Schema | Lines | Concepts | Avg Lines/Concept |
|--------|-------|----------|-------------------|
| Portfolio | 477 | 8 | 60 |
| Program | 586 | 7 | 84 |
| Team | 621 | 10 | 62 |
| Delivery | 659 | 8 | 82 |
| SAFe | 183 | 2 | 92 |
| **Total** | **2,526** | **35** | **72** |

**Original Schema**: 1,972 lines, 35 concepts (56 lines/concept)
**Growth**: +554 lines (+28%) due to added metadata, validation rules, and best practices

---

## Validation

All schemas validated successfully:
- ✅ Valid YAML syntax
- ✅ JSON Schema 2020-12 format
- ✅ Pattern-based cross-references
- ✅ Required fields defined
- ✅ Metadata sections complete

---

## Benefits

1. **Smaller Files**: 183-659 lines vs. 1,972 lines
2. **Clear Boundaries**: Portfolio → Program → Team → Delivery
3. **Easier Navigation**: Find concepts faster
4. **Better Collaboration**: Less merge conflicts
5. **Flexible Usage**: Use only what you need
6. **SAFe Isolation**: SAFe patterns separated from core Scrum

---

## Next Steps

1. ✅ Create partitioned schemas - **COMPLETE**
2. ⏭️ Create partitioned examples
3. ⏭️ Update validation tools
4. ⏭️ Update grounding references in interdomain-map.yaml
5. ⏭️ Create documentation (README, MIGRATION guide)

---

**Implementation Notes**:
- Original schema preserved at `model.schema.yaml` (backward compatibility)
- Backup created at `model.schema.yaml.backup`
- All 35 concepts successfully extracted and partitioned
- Cross-references converted to string patterns
- Explicit groundings to DDD, UX, and QE domains maintained
