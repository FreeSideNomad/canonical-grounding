# ID Naming Convention Synchronization Plan

## Executive Summary

This document outlines the discrepancies in ID naming conventions between the Strategic, Tactical, and Domain Stories schemas, and provides a comprehensive plan to synchronize all schemas, examples, and documentation.

**Status**: Ready for execution
**Created**: 2025-10-24
**Impact**: Low-to-Medium (affects Domain Stories schema and examples)

---

## 1. Current State Analysis

### 1.1 ID Type Comparison Table

| ID Type | Strategic Schema | Tactical Schema | Domain Stories Schema | Status |
|---------|------------------|-----------------|----------------------|--------|
| **Bounded Context** | ✅ `BcId`<br/>`bc_[a-z0-9_]+` | ✅ `BcId`<br/>`bc_[a-z0-9_]+` | N/A | ✅ Consistent |
| **Domain** | ✅ `DomId`<br/>`dom_[a-z0-9_]+` | ✅ `DomId` (reference)<br/>`dom_[a-z0-9_]+` | N/A | ✅ Consistent |
| **Aggregate** | N/A<br/>(reference: `agg_[a-z0-9_]+`) | ✅ `AggId`<br/>`agg_[a-z0-9_]+` | ✅ `AggId`<br/>`agg_[a-z0-9_]+` | ✅ Consistent |
| **Repository** | N/A<br/>(reference: `repo_[a-z0-9_]+`) | ✅ `RepoId`<br/>`repo_[a-z0-9_]+` | ❌ `RepId`<br/>`rep_[a-z0-9_]+` | ❌ **INCONSISTENT** |
| **Application Service** | N/A<br/>(reference: `svc_app_[a-z0-9_]+`) | ✅ `SvcAppId`<br/>`svc_app_[a-z0-9_]+` | ⚠️ `AppSvcId`<br/>`svc_app_[a-z0-9_]+` | ⚠️ **Type name differs** |
| **Domain Service** | N/A<br/>(reference: `svc_dom_[a-z0-9_]+`) | ✅ `SvcDomId`<br/>`svc_dom_[a-z0-9_]+` | ❌ `DomSvcId`<br/>`dom_svc_[a-z0-9_]+` | ❌ **INCONSISTENT** |
| **Command** | N/A | ✅ `CmdId`<br/>`cmd_[a-z0-9_]+` | ✅ `CmdId`<br/>`cmd_[a-z0-9_]+` | ✅ Consistent |
| **Query** | N/A | ✅ `QryId`<br/>`qry_[a-z0-9_]+` | ✅ `QryId`<br/>`qry_[a-z0-9_]+` | ✅ Consistent |
| **Domain Event** | N/A | ✅ `EvtId`<br/>`evt_[a-z0-9_]+` | ✅ `EvtId`<br/>`evt_[a-z0-9_]+` | ✅ Consistent |

### 1.2 Key Findings

**Critical Discrepancies:**
1. **Repository ID**: Domain Stories uses `rep_` instead of `repo_`
2. **Domain Service ID**: Domain Stories uses `dom_svc_` instead of `svc_dom_`

**Minor Discrepancies:**
3. **Application Service ID**: Type name differs (`SvcAppId` vs `AppSvcId`) but pattern is correct

**Impact:**
- Affects domain stories schema validation
- Breaks cross-schema references
- Creates confusion in documentation
- Impacts 8 files using `rep_` pattern
- Impacts 8 files using `dom_svc_` pattern

---

## 2. Canonical Naming Convention

The **Tactical DDD Schema** (`tactical-ddd.schema.yaml`) is the authoritative source for tactical pattern ID types.

### 2.1 Official ID Type Definitions

```yaml
# From tactical-ddd.schema.yaml (lines 58-90)

RepoId:
  type: string
  pattern: "^repo_[a-z0-9_]+$"
  description: "Repository identifier"

SvcDomId:
  type: string
  pattern: "^svc_dom_[a-z0-9_]+$"
  description: "Domain Service identifier"

SvcAppId:
  type: string
  pattern: "^svc_app_[a-z0-9_]+$"
  description: "Application Service identifier"

AggId:
  type: string
  pattern: "^agg_[a-z0-9_]+$"
  description: "Aggregate identifier"

CmdId:
  type: string
  pattern: "^cmd_[a-z0-9_]+$"
  description: "Command interface identifier"

QryId:
  type: string
  pattern: "^qry_[a-z0-9_]+$"
  description: "Query interface identifier"

EvtId:
  type: string
  pattern: "^evt_[a-z0-9_]+$"
  description: "Domain Event identifier"
```

### 2.2 Naming Rationale

**Repository ID** (`repo_` not `rep_`):
- `repo_` is the common abbreviation for "repository"
- Consistent with GitHub naming (repo)
- Already used in 48 files across the codebase
- Referenced correctly in Strategic schema

**Domain Service ID** (`svc_dom_` not `dom_svc_`):
- Follows pattern: `svc_` prefix + service type suffix
- Matches Application Service pattern `svc_app_`
- Creates consistent grouping: all services start with `svc_`
- Enables better sorting and filtering

**Application Service ID** (`SvcAppId` not `AppSvcId`):
- Type name should match pattern structure
- `SvcAppId` aligns with `SvcDomId`
- Pattern `svc_app_` is already correct in Domain Stories

---

## 3. Files Requiring Updates

### 3.1 Schema Files

#### Priority 1: Domain Stories Schema
**File**: `/domain-stories/domain-stories-schema.yaml`

**Changes Required**:

```yaml
# Line 70-73: CHANGE
RepId:                           # ❌ Wrong
  type: string
  pattern: "^rep_[a-z0-9_]+$"   # ❌ Wrong
  description: "Repository ID"

# TO:
RepoId:                          # ✅ Correct
  type: string
  pattern: "^repo_[a-z0-9_]+$"  # ✅ Correct
  description: "Repository ID"
```

```yaml
# Line 75-78: CHANGE
AppSvcId:                        # ⚠️ Inconsistent name
  type: string
  pattern: "^svc_app_[a-z0-9_]+$"  # ✅ Pattern correct
  description: "Application Service ID"

# TO:
SvcAppId:                        # ✅ Consistent name
  type: string
  pattern: "^svc_app_[a-z0-9_]+$"
  description: "Application Service identifier"
```

```yaml
# Line 80-83: CHANGE
DomSvcId:                        # ❌ Wrong
  type: string
  pattern: "^dom_svc_[a-z0-9_]+$"  # ❌ Wrong pattern
  description: "Domain Service ID"

# TO:
SvcDomId:                        # ✅ Correct
  type: string
  pattern: "^svc_dom_[a-z0-9_]+$"  # ✅ Correct pattern
  description: "Domain Service identifier"
```

**Additional References to Update**:
- Line 232: `repository_id: { $ref: "#/$defs/RepId" }` → `RepoId`
- Line 243: `app_service_id: { $ref: "#/$defs/AppSvcId" }` → `SvcAppId`
- Line 249: items: `{ $ref: "#/$defs/AppSvcId" }` → `SvcAppId`
- Line 264: `domain_service_id: { $ref: "#/$defs/DomSvcId" }` → `SvcDomId`
- Line 305: items: `{ $ref: "#/$defs/AppSvcId" }` → `SvcAppId`
- Line 308: items: `{ $ref: "#/$defs/DomSvcId" }` → `SvcDomId`
- Line 366: items: `{ $ref: "#/$defs/AppSvcId" }` → `SvcAppId`
- Line 370: items: `{ $ref: "#/$defs/DomSvcId" }` → `SvcDomId`

### 3.2 Example Files

#### Commercial Banking Domain Stories
**File**: `/domain-stories/commercial-banking-domain-stories.yaml`

**Changes Required** (Lines 92-99):
```yaml
# CHANGE FROM:
repositories:
  - repository_id: rep_user_repository      # ❌
    name: UserRepository
    aggregate_id: agg_user_account
  - repository_id: rep_policy_repository    # ❌
    name: PolicyRepository
    aggregate_id: agg_approval_policy
  - repository_id: rep_audit_repository     # ❌
    name: AuditRepository
    aggregate_id: agg_audit_log

# TO:
repositories:
  - repository_id: repo_user_repository     # ✅
    name: UserRepository
    aggregate_id: agg_user_account
  - repository_id: repo_policy_repository   # ✅
    name: PolicyRepository
    aggregate_id: agg_approval_policy
  - repository_id: repo_audit_repository    # ✅
    name: AuditRepository
    aggregate_id: agg_audit_log
```

**Additional instances** (continue through the file - need to check lines 100+):
- Search and replace all `repository_id: rep_` → `repository_id: repo_`

### 3.3 Documentation Files

Files potentially affected (need content review):

1. `/domain-stories/domain-stories-context.md`
   - Review for `rep_`, `dom_svc_`, `AppSvcId` references

2. `/analysis-outputs/01-current-state-schemas.md`
   - Review ID type references

3. `/analysis-outputs/02-example-analysis.md`
   - Review example ID references

4. `/domains/ddd/docs/ddd-guide.md`
   - Review ID naming convention documentation

5. `/domains/ddd/docs/ddd-09-domain-storytelling.md`
   - Review Domain Stories integration section

6. `/output/ddd-guide.html` and `/domains/ddd/docs/ddd-guide.html`
   - Regenerate after markdown updates

---

## 4. Migration Steps

### Phase 1: Schema Updates (Critical)
**Estimated Time**: 15 minutes

1. ✅ **Update Domain Stories Schema**
   - File: `/domain-stories/domain-stories-schema.yaml`
   - Change `RepId` → `RepoId` with pattern `repo_`
   - Change `DomSvcId` → `SvcDomId` with pattern `svc_dom_`
   - Change `AppSvcId` → `SvcAppId` (type name only)
   - Update all `$ref` references

2. ✅ **Validate Schema**
   - Run schema validation
   - Ensure no syntax errors

### Phase 2: Example Updates (High Priority)
**Estimated Time**: 10 minutes

3. ✅ **Update Commercial Banking Example**
   - File: `/domain-stories/commercial-banking-domain-stories.yaml`
   - Replace all `rep_` → `repo_` in repository_id fields
   - Validate against updated schema

4. ✅ **Search for Additional Examples**
   - Search for files with `rep_` pattern (8 files found)
   - Review and update each file

### Phase 3: Documentation Updates (Medium Priority)
**Estimated Time**: 30 minutes

5. ✅ **Update Domain Stories Context**
   - File: `/domain-stories/domain-stories-context.md`
   - Update ID naming examples
   - Add migration note if needed

6. ✅ **Update Analysis Documents**
   - Files in `/analysis-outputs/`
   - Update ID type references
   - Ensure consistency

7. ✅ **Update DDD Guide**
   - File: `/domains/ddd/docs/ddd-guide.md`
   - Review Domain Storytelling section
   - Update ID naming convention documentation

8. ✅ **Regenerate HTML Documentation**
   - Regenerate HTML from updated markdown files

### Phase 4: Validation and Testing (Critical)
**Estimated Time**: 20 minutes

9. ✅ **Validate All Examples**
   - Run validation tool against all YAML examples
   - Ensure all IDs match schema patterns

10. ✅ **Cross-Schema Reference Check**
    - Verify Strategic → Tactical references work
    - Verify Tactical → Domain Stories references work

11. ✅ **Document Migration**
    - Update CHANGELOG.md
    - Add migration notes for users

---

## 5. Validation Rules

After migration, all files must satisfy:

### 5.1 Schema Validation
```bash
# Validate domain stories schema
python3 tools/validate-v2.py domain-stories/domain-stories-schema.yaml

# Validate all domain stories examples
python3 tools/validate-v2.py domain-stories/*.yaml
```

### 5.2 Pattern Validation

**Repository IDs**:
- ✅ Match pattern: `^repo_[a-z0-9_]+$`
- ❌ Must NOT use: `rep_`, `repository_`, or other variants

**Domain Service IDs**:
- ✅ Match pattern: `^svc_dom_[a-z0-9_]+$`
- ❌ Must NOT use: `dom_svc_`, `domain_svc_`, or other variants

**Application Service IDs**:
- ✅ Match pattern: `^svc_app_[a-z0-9_]+$`
- ❌ Must NOT use: `app_svc_`, `application_svc_`, or other variants

### 5.3 Cross-Schema References

Strategic schema bounded_context references must match tactical IDs:
```yaml
# Strategic schema
bounded_contexts:
  - id: bc_user_management
    repositories:
      - "repo_user"           # ✅ matches tactical RepoId pattern
    domain_services:
      - "svc_dom_validation"  # ✅ matches tactical SvcDomId pattern
    application_services:
      - "svc_app_user"        # ✅ matches tactical SvcAppId pattern
```

---

## 6. Breaking Changes and Compatibility

### 6.1 Breaking Changes

**For Domain Stories Users**:
- ⚠️ All existing domain stories using `rep_*` IDs must be updated to `repo_*`
- ⚠️ All existing domain stories using `dom_svc_*` IDs must be updated to `svc_dom_*`

**For Schema Validators**:
- ⚠️ Domain Stories schema version should be bumped to indicate breaking change
- Current: `version: "2.0.0"`
- Proposed: `version: "2.1.0"` (minor version bump for ID pattern fix)

### 6.2 Migration Path for Existing Files

```bash
# Step 1: Backup existing files
cp domain-stories/commercial-banking-domain-stories.yaml \
   domain-stories/commercial-banking-domain-stories.yaml.backup

# Step 2: Apply automated replacements
sed -i '' 's/repository_id: rep_/repository_id: repo_/g' \
   domain-stories/commercial-banking-domain-stories.yaml

# Step 3: Validate
python3 tools/validate-v2.py \
   domain-stories/commercial-banking-domain-stories.yaml

# Step 4: If validation passes, remove backup
rm domain-stories/commercial-banking-domain-stories.yaml.backup
```

### 6.3 Backwards Compatibility

**Not Backwards Compatible**:
- Domain Stories schema v2.1.0 will reject old `rep_*` and `dom_svc_*` IDs
- Migration is required for all existing files

**Forward Compatible**:
- Strategic and Tactical schemas already use correct patterns
- No changes needed in those schemas

---

## 7. Testing Strategy

### 7.1 Unit Tests
- Schema validation tests for each ID type
- Pattern matching tests
- Cross-reference validation tests

### 7.2 Integration Tests
- Validate all example files against schemas
- Test cross-schema references
- Verify documentation examples

### 7.3 Manual Testing
- Review all updated files visually
- Check for missed instances
- Validate naming makes semantic sense

---

## 8. Rollback Plan

If issues are discovered after migration:

### 8.1 Immediate Rollback
```bash
# Restore from git
git checkout HEAD -- domain-stories/
```

### 8.2 Partial Rollback
- Keep schema changes
- Revert only problematic example files
- Document issues for future resolution

---

## 9. Communication Plan

### 9.1 Stakeholders
- Schema maintainers
- Documentation team
- Domain Stories users
- Integration developers

### 9.2 Communication Channels
- Update CHANGELOG.md with breaking changes
- Add migration guide to documentation
- Include examples of before/after
- Note in schema file metadata

---

## 10. Success Criteria

Migration is complete when:

- ✅ All ID type definitions use canonical naming
- ✅ All example files validate against updated schemas
- ✅ All documentation references correct ID patterns
- ✅ Cross-schema references work correctly
- ✅ No instances of `rep_*` or `dom_svc_*` patterns remain
- ✅ Validation tools pass all tests
- ✅ CHANGELOG.md updated
- ✅ Migration guide added to documentation

---

## 11. Post-Migration Tasks

1. ✅ Archive old schema version
   - Move to `/domains/ddd/schemas/archive/v2.0.0/`

2. ✅ Update schema version metadata
   - Bump to v2.1.0 in schema file

3. ✅ Add migration guide
   - Create `/docs/migration/id-naming-v2.1.md`

4. ✅ Update validation tools
   - Ensure tools use new patterns

5. ✅ Review and close related issues/tickets

---

## Appendix A: Affected Files Summary

### Schemas (1 file)
- `/domain-stories/domain-stories-schema.yaml` - **CRITICAL**

### Examples (1+ files)
- `/domain-stories/commercial-banking-domain-stories.yaml` - **HIGH**
- Other files with `rep_` pattern (7 more files) - **MEDIUM**

### Documentation (5-10 files)
- `/domain-stories/domain-stories-context.md` - **MEDIUM**
- `/domains/ddd/docs/ddd-guide.md` - **MEDIUM**
- `/analysis-outputs/*.md` - **LOW**
- HTML generated files - **AUTO-REGENERATE**

### Total Impact
- **Critical**: 1 file (schema)
- **High**: 1 file (main example)
- **Medium**: 8-12 files (other examples and docs)
- **Low**: 10-15 files (analysis and references)

**Total Estimated Time**: 1.5 - 2 hours

---

## Appendix B: Quick Reference

### Old → New ID Mappings

| Old Pattern | New Pattern | Type Name Old | Type Name New | Files Affected |
|-------------|-------------|---------------|---------------|----------------|
| `rep_*` | `repo_*` | `RepId` | `RepoId` | 8 files |
| `dom_svc_*` | `svc_dom_*` | `DomSvcId` | `SvcDomId` | 8 files |
| N/A | N/A | `AppSvcId` | `SvcAppId` | Schema only |

### Replacement Commands

```bash
# Repository IDs
find . -name "*.yaml" -type f -exec \
  sed -i '' 's/rep_\([a-z0-9_]*\)/repo_\1/g' {} +

# Domain Service IDs
find . -name "*.yaml" -type f -exec \
  sed -i '' 's/dom_svc_\([a-z0-9_]*\)/svc_dom_\1/g' {} +

# Validate all
find . -name "*.yaml" -type f -exec \
  python3 tools/validate-v2.py {} \;
```

---

**Document Status**: ✅ Complete
**Review Status**: Pending
**Approval**: Pending
**Execution**: Ready to start
