# Naming Convention Standardization Plan
**Date:** 2025-10-14
**Goal:** Standardize all schemas to snake_case
**Status:** Ready for Execution

---

## Problem Statement

**Current State:**
- DDD, Data-Eng, UX, QE: ✅ Use snake_case (bounded_context, test_case)
- Agile: ❌ Uses PascalCase (NonFunctionalRequirement, TechnicalDebt)

**Impact:**
- Inconsistent grounding references
- Confusing for developers
- Non-standard for JSON Schema

**Solution:** Convert Agile schema from PascalCase → snake_case

---

## Conversion Mapping (35 concepts)

| PascalCase | snake_case |
|------------|------------|
| AgileReleaseTrain | agile_release_train |
| ArchitecturalRunway | architectural_runway |
| Cadence | cadence |
| Ceremony | ceremony |
| DefinitionOfReady | definition_of_ready |
| Enabler | enabler |
| Epic | epic |
| EstimationTechnique | estimation_technique |
| Feature | feature |
| FeedbackLoop | feedback_loop |
| Impediment | impediment |
| Increment | increment |
| Iteration | iteration |
| Metadata | metadata |
| Metric | metric |
| **NonFunctionalRequirement** | **non_functional_requirement** |
| Portfolio | portfolio |
| Product | product |
| ProgramIncrement | program_increment |
| Release | release |
| ReleaseVision | release_vision |
| Risk | risk |
| Roadmap | roadmap |
| Role | role |
| Sprint | sprint |
| Stakeholder | stakeholder |
| Task | task |
| Team | team |
| TeamMember | team_member |
| TeamTopology | team_topology |
| **TechnicalDebt** | **technical_debt** |
| UserStory | user_story |
| ValueStream | value_stream |
| Vision | vision |
| WorkingAgreement | working_agreement |

**Bold** = Referenced in interdomain-map.yaml groundings

---

## Files Requiring Updates

### Priority 1: Schema Files (CRITICAL)
- [x] `domains/agile/model.schema.yaml` (primary schema)
  - 35 $defs concept names
  - All internal $ref references
  - All property names that reference concepts

### Priority 2: Grounding Files (HIGH)
- [x] `research-output/interdomain-map.yaml`
  - `agile:NonFunctionalRequirement` → `agile:non_functional_requirement`
  - `agile:TechnicalDebt` → `agile:technical_debt`
  - Search for other Agile PascalCase references

### Priority 3: Documentation (HIGH)
- [ ] `GLOSSARY.md` (auto-regenerate after schema fix)
- [ ] `GROUNDING-FIX-REPORT.md`
- [ ] `GROUNDING-REPORT.md`
- [ ] `TERMINOLOGY.md`

### Priority 4: Domain Documentation (MEDIUM)
- [ ] `domains/agile/docs/vision.md`
- [ ] `domains/agile/docs/scope-and-nfrs.md`
- [ ] `domains/agile/docs/guide-to-agile.md`
- [ ] `domains/agile/docs/HOW-TO-USE.md`

### Priority 5: Examples (MEDIUM)
- [ ] `domains/agile/examples/safe/art-planning.example.yaml`
- [ ] `domains/agile/examples/scrum/sprint-planning.example.yaml`
- [ ] `domains/agile/examples/safe/release-with-vision.example.yaml`
- [ ] `domains/agile/examples/agile/product-with-releases.example.yaml`
- [ ] `domains/agile/examples/agile/product-with-vision.example.yaml`

### Priority 6: Research Documents (LOW)
- [ ] `research-output/final-synthesis.md` (if mentions specific concepts)
- [ ] `AUTOMATION-REPORT.md` (if mentions specific concepts)

---

## Execution Plan

### Phase 1: Backup & Preparation (5 minutes)

```bash
# Create backup
cp domains/agile/model.schema.yaml domains/agile/model.schema.yaml.pre-snake-case

# Create conversion script
```

**Deliverable:** Backup file + conversion script

---

### Phase 2: Update Agile Schema (30 minutes)

**Automated Script:**
```python
# tools/convert-agile-to-snake-case.py

import yaml
import re
from pathlib import Path

def pascal_to_snake(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def convert_value(value, mappings):
    """Recursively convert PascalCase to snake_case in values"""
    if isinstance(value, str):
        for old, new in mappings.items():
            value = value.replace(f'#{old}', f'#{new}')
            value = value.replace(f'/{old}', f'/{new}')
    elif isinstance(value, dict):
        return {k: convert_value(v, mappings) for k, v in value.items()}
    elif isinstance(value, list):
        return [convert_value(item, mappings) for item in value]
    return value

# Load schema
schema_path = Path('domains/agile/model.schema.yaml')
with open(schema_path) as f:
    schema = yaml.safe_load(f)

# Generate mappings
mappings = {}
if '$defs' in schema:
    for concept in schema['$defs'].keys():
        snake = pascal_to_snake(concept)
        if concept != snake:
            mappings[concept] = snake

# Convert $defs keys
if '$defs' in schema:
    new_defs = {}
    for old_name, definition in schema['$defs'].items():
        new_name = mappings.get(old_name, old_name)
        # Convert references within definition
        new_def = convert_value(definition, mappings)
        new_defs[new_name] = new_def
    schema['$defs'] = new_defs

# Convert references in rest of schema
schema = convert_value(schema, mappings)

# Save updated schema
with open(schema_path, 'w') as f:
    yaml.dump(schema, f, sort_keys=False, allow_unicode=True)

print(f"Converted {len(mappings)} concepts to snake_case")
```

**Manual Review Points:**
- Check that all $ref patterns updated correctly
- Verify required/properties arrays
- Check pattern constraints (regex patterns)

**Deliverable:** Updated domains/agile/model.schema.yaml

---

### Phase 3: Update Grounding References (15 minutes)

**Files to update:**
1. `research-output/interdomain-map.yaml`

**Replacements:**
```bash
# Systematic replacements
sed -i '' 's/agile:NonFunctionalRequirement/agile:non_functional_requirement/g' research-output/interdomain-map.yaml
sed -i '' 's/agile:TechnicalDebt/agile:technical_debt/g' research-output/interdomain-map.yaml

# Verify no other Agile PascalCase remains
grep 'agile:[A-Z]' research-output/interdomain-map.yaml
```

**Manual Verification:**
- Search for any remaining `agile:[A-Z]` patterns
- Update if found

**Deliverable:** Updated interdomain-map.yaml

---

### Phase 4: Regenerate Auto-Generated Files (10 minutes)

```bash
cd tools
source venv/bin/activate

# Regenerate glossary
python3 generate-glossary.py --output ../GLOSSARY.md --format md

# Regenerate grounding graph
python3 generate-grounding-graph.py
cd ..
dot -Tpng grounding-graph.dot -o grounding-graph.png
dot -Tsvg grounding-graph.dot -o grounding-graph.svg
```

**Deliverable:** Updated GLOSSARY.md, grounding-graph.*

---

### Phase 5: Update Documentation (30 minutes)

**Automated Search & Replace:**
```bash
# Update report documents
for file in GROUNDING-FIX-REPORT.md GROUNDING-REPORT.md TERMINOLOGY.md; do
  sed -i '' 's/NonFunctionalRequirement/non_functional_requirement/g' "$file"
  sed -i '' 's/TechnicalDebt/technical_debt/g' "$file"
  sed -i '' 's/UserStory/user_story/g' "$file"
  sed -i '' 's/AgileReleaseTrain/agile_release_train/g' "$file"
  sed -i '' 's/ProgramIncrement/program_increment/g' "$file"
done

# Update domain docs
for file in domains/agile/docs/*.md; do
  # Only update concept references, not prose
  sed -i '' 's/`NonFunctionalRequirement`/`non_functional_requirement`/g' "$file"
  sed -i '' 's/`TechnicalDebt`/`technical_debt`/g' "$file"
  # Add more as needed...
done
```

**Manual Review:**
- Check that prose/narrative text wasn't inappropriately changed
- Some docs might intentionally use PascalCase in explanatory text
- Focus on code blocks, concept references, property names

**Deliverable:** Updated documentation files

---

### Phase 6: Update Examples (20 minutes)

**Example files:**
```bash
# Convert example YAML files
for example in domains/agile/examples/**/*.yaml; do
  # Use conversion script or manual update
  # These likely need careful review since they're user-facing
  echo "Reviewing: $example"
done
```

**Approach:**
- These are example instance data, not schemas
- May reference concept names in type fields
- Careful manual review recommended

**Deliverable:** Updated example files

---

### Phase 7: Validation (20 minutes)

**Validation Checklist:**

1. **Schema Validation**
   ```bash
   cd tools
   source venv/bin/activate
   python3 validate-schemas.py --full-report
   ```
   - ✅ All schemas valid
   - ✅ 100% closure maintained
   - ✅ No YAML syntax errors

2. **Grounding Validation**
   ```bash
   python3 validate-grounding-references.py
   ```
   - ✅ All 28 groundings valid
   - ✅ No broken Agile references
   - ✅ Case matches schema concepts

3. **Documentation Coverage**
   ```bash
   python3 validate-schema-docs-alignment.py agile
   ```
   - ✅ 57.1% coverage maintained (or better)
   - ✅ No new missing concepts

4. **Example Validation**
   ```bash
   for example in ../domains/agile/examples/**/*.yaml; do
     python3 validate-example.py "$example"
   done
   ```
   - ✅ Examples still valid
   - ✅ References resolve correctly

5. **Glossary Check**
   ```bash
   grep -i "nonfunctionalrequirement\|technicaldebt" ../GLOSSARY.md
   ```
   - ✅ Uses snake_case: non_functional_requirement, technical_debt
   - ✅ All 35 Agile concepts present

**Deliverable:** Validation report confirming 100% success

---

### Phase 8: Git Commit (10 minutes)

```bash
git add domains/agile/model.schema.yaml
git add research-output/interdomain-map.yaml
git add GLOSSARY.md grounding-graph.*
git add GROUNDING-FIX-REPORT.md GROUNDING-REPORT.md TERMINOLOGY.md
git add domains/agile/docs/
git add domains/agile/examples/

git commit -m "Standardize Agile schema to snake_case naming convention

Convert all Agile schema concepts from PascalCase to snake_case for consistency
with other domains (DDD, Data-Eng, UX, QE).

Changes:
- Converted 35 concepts: NonFunctionalRequirement → non_functional_requirement, etc.
- Updated interdomain-map.yaml grounding references
- Regenerated GLOSSARY.md with snake_case concepts
- Updated documentation and examples
- Maintained 100% validation (28/28 groundings, 100% schema closure)

Rationale:
- 4 of 5 domains already use snake_case
- JSON Schema standard convention
- Python-friendly naming
- Easier to parse and maintain

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
"
```

---

## Risk Assessment

### Low Risk ✅
- **Schema conversion**: Automated, deterministic
- **Grounding updates**: Only 2 references in interdomain-map.yaml
- **Validation**: Comprehensive test suite

### Medium Risk ⚠️
- **Documentation**: May have mixed use of PascalCase in prose vs. code
  - **Mitigation**: Manual review after automated replacement
- **Examples**: User-facing, need careful review
  - **Mitigation**: Validate each example individually

### High Risk ❌
- None identified

---

## Rollback Plan

If issues arise:

```bash
# Restore from backup
cp domains/agile/model.schema.yaml.pre-snake-case domains/agile/model.schema.yaml

# Revert commit
git revert HEAD

# Or reset
git reset --hard HEAD~1
```

---

## Success Criteria

- ✅ All 35 Agile concepts converted to snake_case
- ✅ All schemas validate successfully
- ✅ 100% grounding validation maintained (28/28)
- ✅ 100% schema closure maintained
- ✅ Glossary regenerated with snake_case
- ✅ All examples validate
- ✅ Documentation updated consistently

---

## Estimated Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| 1. Backup & Preparation | 5m | 5m |
| 2. Update Agile Schema | 30m | 35m |
| 3. Update Grounding Refs | 15m | 50m |
| 4. Regenerate Files | 10m | 60m |
| 5. Update Documentation | 30m | 90m |
| 6. Update Examples | 20m | 110m |
| 7. Validation | 20m | 130m |
| 8. Git Commit | 10m | 140m |

**Total: ~2.5 hours**

---

## Alternatives Considered

### Option A: Convert to kebab-case
- **Pros**: URL-friendly, modern
- **Cons**: Not standard for JSON Schema, would require changing 4 schemas
- **Decision**: ❌ Rejected

### Option B: Convert all to PascalCase
- **Pros**: Matches some OOP conventions
- **Cons**: Not JSON Schema standard, would require changing 4 schemas
- **Decision**: ❌ Rejected

### Option C: Keep mixed (status quo)
- **Pros**: No work required
- **Cons**: Inconsistent, confusing, non-standard
- **Decision**: ❌ Rejected

### Option D: Convert Agile to snake_case ✅
- **Pros**: Matches 80% of codebase, JSON Schema standard, minimal change
- **Cons**: Requires updating Agile schema and references
- **Decision**: ✅ **RECOMMENDED**

---

## Next Steps

1. **Review this plan** - Get approval
2. **Execute phases 1-8** - Systematic conversion
3. **Validate thoroughly** - Ensure 100% success
4. **Commit changes** - Document in git history

---

*Plan Status: Ready for Execution*
*Estimated Effort: 2.5 hours*
*Risk Level: Low*
