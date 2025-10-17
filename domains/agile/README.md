# Agile/SAFe Canonical Domain Model

## Overview

The Agile canonical domain model provides patterns for agile software development at multiple scales - from individual teams to enterprise portfolios. It covers both Scrum patterns and SAFe (Scaled Agile Framework) patterns.

## Schema Organization

The Agile domain schema is **partitioned into 5 schemas** for better maintainability and clarity:

### Schemas

1. **portfolio-agile.schema.yaml** - Portfolio-level patterns
   - **Concepts**: portfolio, value_stream, epic, roadmap, stakeholder, metric, non_functional_requirement, risk
   - **Use for**: Strategic planning, portfolio management, lean portfolio management
   - **Scale**: Organization level (months to years)

2. **program-agile.schema.yaml** - Program-level patterns
   - **Concepts**: Program, program_increment, architectural_runway, enabler, release, release_vision, technical_debt
   - **Use for**: PI planning, program coordination, Agile Release Train (ART) management
   - **Scale**: Program level (8-12 week PIs)

3. **team-agile.schema.yaml** - Team-level patterns
   - **Concepts**: team, team_member, team_topology, role, sprint, iteration, ceremony, working_agreement, impediment, feedback_loop
   - **Use for**: Team organization, sprint planning, daily standup, retrospectives
   - **Scale**: Team level (2-week sprints)

4. **delivery-agile.schema.yaml** - Delivery patterns
   - **Concepts**: product, vision, feature, user_story, task, increment, product_backlog, sprint_backlog, definition_of_ready, estimation_technique
   - **Use for**: Backlog management, product delivery, story mapping
   - **Scale**: Product level (ongoing)

5. **safe-agile.schema.yaml** - SAFe extensions
   - **Concepts**: agile_release_train, cadence
   - **Use for**: SAFe-specific patterns (ART, PI planning cadences, Inspect & Adapt)
   - **Scale**: Enterprise level (SAFe ceremonies and structures)

### Examples

The domain includes both original (monolithic) and new (partitioned) examples:

#### Original Examples (backward compatibility)
- `examples/safe/art-planning.example.yaml` - SAFe PI planning
- `examples/safe/release-with-vision.example.yaml` - Release planning
- `examples/scrum/sprint-planning.example.yaml` - Sprint planning
- `examples/agile/product-with-releases.example.yaml` - Product with releases
- `examples/agile/product-with-vision.example.yaml` - Product with vision

#### Partitioned Examples (demonstrating new structure)
- `examples/partitioned/portfolio-example.yaml` - E-commerce platform portfolio
- `examples/partitioned/program-example.yaml` - Mobile platform program
- `examples/partitioned/team-example.yaml` - iOS development team
- `examples/partitioned/delivery-example.yaml` - iOS app product delivery
- `examples/partitioned/safe-example.yaml` - Mobile platform ART

## Cross-References

Schemas use **string pattern references** (not JSON Schema `$ref`) for loose coupling across partitions:

### ID Naming Conventions
- Portfolio IDs: `pf_<name>` (e.g., `pf_ecommerce`)
- Value Stream IDs: `vs_<name>` (e.g., `vs_customer_experience`)
- Epic IDs: `epic_<name>` (e.g., `epic_mobile_app`)
- Program IDs: `prg_<name>` (e.g., `prg_mobile_platform`)
- Program Increment IDs: `pi_<number>` (e.g., `pi_2025_q1`)
- Team IDs: `tm_<name>` (e.g., `tm_ios`)
- Sprint IDs: `sp_<number>` (e.g., `sp_2025_01`)
- Feature IDs: `feat_<name>` (e.g., `feat_ios_app`)
- User Story IDs: `us_<name>` (e.g., `us_login_screen`)
- Task IDs: `tsk_<name>` (e.g., `tsk_ui_design`)

### Example Cross-Reference

```yaml
# In program-agile.schema.yaml
Program:
  properties:
    portfolio_ref:
      type: string
      pattern: "^pf_[a-z0-9_]+$"  # References portfolio schema
    team_refs:
      type: array
      items:
        type: string
        pattern: "^tm_[a-z0-9_]+$"  # References team schema
```

This approach provides loose coupling while maintaining validation capabilities.

## Grounding Relationships

The Agile model grounds in all other canonical domain models:

- **Agile → DDD**: Features map to bounded contexts, epics align with domains
- **Agile → UX**: User stories implement UX pages/components/workflows
- **Agile → QE**: Definition of done references test criteria, sprints include testing
- **Agile → Data-Eng**: Features include data pipeline work, stories track transforms

For complete grounding specifications, see `research-output/interdomain-map.yaml`.

## Usage

### Validation

Validate schemas and examples:

```bash
# Validate all partitions
cd /path/to/canonical-grounding
source venv/bin/activate

# Validate portfolio
python3 partition-examples/tools/validate_multifile_schema.py \
  domains/agile/schemas/portfolio-agile.schema.yaml \
  domains/agile/examples/partitioned/portfolio-example.yaml

# Validate program
python3 partition-examples/tools/validate_multifile_schema.py \
  domains/agile/schemas/program-agile.schema.yaml \
  domains/agile/examples/partitioned/program-example.yaml

# Validate team
python3 partition-examples/tools/validate_multifile_schema.py \
  domains/agile/schemas/team-agile.schema.yaml \
  domains/agile/examples/partitioned/team-example.yaml

# Validate delivery
python3 partition-examples/tools/validate_multifile_schema.py \
  domains/agile/schemas/delivery-agile.schema.yaml \
  domains/agile/examples/partitioned/delivery-example.yaml

# Validate SAFe
python3 partition-examples/tools/validate_multifile_schema.py \
  domains/agile/schemas/safe-agile.schema.yaml \
  domains/agile/examples/partitioned/safe-example.yaml
```

### Integration

When building systems that reference Agile patterns:

1. **Identify your scale level**: Portfolio, Program, Team, or Delivery
2. **Load relevant schemas**: You don't need all 5 - just what you use
3. **Use ID references**: Reference concepts by ID (e.g., `pf_ecommerce`)
4. **Validate cross-references**: Use pattern validation to ensure IDs are well-formed

## Migration Guide

See [MIGRATION.md](MIGRATION.md) for guidance on migrating from the original monolithic schema to the partitioned schemas.

## Statistics

- **Original schema**: 1,972 lines, 35 concepts
- **Partitioned schemas**: 2,526 lines (5 files), 35 concepts
- **Partition overhead**: +28% (due to metadata duplication)
- **Average partition size**: 505 lines
- **Largest partition**: delivery (659 lines)
- **Smallest partition**: safe (183 lines)

## References

- **SAFe 6.0**: [Scaled Agile Framework](https://www.scaledagileframework.com/)
- **Scrum Guide**: [Scrum.org](https://www.scrum.org/resources/scrum-guide)
- **Story Mapping**: Jeff Patton - User Story Mapping (2014)
- **Agile Estimating**: Mike Cohn - Agile Estimating and Planning (2005)

## Changelog

### Version 2.0.0 (2025-10-17)
- Partitioned schema into 5 focused schemas
- Created 5 new partitioned examples
- Updated interdomain-map.yaml with partition groundings
- Added 4 new Agile → Data-Eng groundings
- Achieved 100% closure (up from 72%)

### Version 1.0.0 (2025-10-13)
- Initial monolithic schema
- 5 original examples (SAFe, Scrum, Agile)
- Core concepts: 35
