# Agile Schema Partitioning Implementation Plan

**Date**: 2025-10-17
**Version**: 1.0
**Status**: Ready for Implementation
**Estimated Effort**: 4-5 days

---

## Overview

This plan details the partitioning of the Agile domain model (1,972 lines) into 5 logical schemas following the SAFe scale levels plus a dedicated SAFe Extensions schema. The partition follows the proven pattern established by the DDD domain partition.

**Current State**:
- Single monolithic schema: `domains/agile/model.schema.yaml` (1,972 lines)
- 35 concepts covering portfolio, program, team, and delivery concerns
- 5 existing example files (SAFe and Scrum)

**Target State**:
- 5 partitioned schemas (~300-500 lines each)
- Clear separation by scale level (Portfolio → Program → Team → Delivery)
- SAFe-specific concepts isolated in dedicated schema
- Backward compatible (original files preserved)
- 5 new partitioned examples + 5 original examples kept

---

## Partition Strategy: Option A (By Scale Level)

### 1. Portfolio Schema (~400 lines)
**File**: `domains/agile/schemas/portfolio-agile.schema.yaml`

**Concepts** (8):
- `portfolio` - Portfolio management
- `value_stream` - Value stream mapping
- `epic` - Portfolio epics
- `roadmap` - Product roadmap
- `stakeholder` - Key stakeholders
- `metric` - Business metrics
- `non_functional_requirement` - System-wide NFRs
- `risk` - Portfolio risks

**Purpose**: Strategic planning and portfolio-level coordination

**ID Patterns**:
```yaml
naming_conventions:
  portfolio_id: "pf_<name>"
  value_stream_id: "vs_<name>"
  epic_id: "epic_<name>"
  roadmap_id: "rm_<name>"
  stakeholder_id: "sh_<name>"
```

---

### 2. Program Schema (~450 lines)
**File**: `domains/agile/schemas/program-agile.schema.yaml`

**Concepts** (7):
- `Program` - Program/ART definition
- `program_increment` - PI planning and execution
- `architectural_runway` - Technical enablement
- `enabler` - Enabler features/stories
- `release` - Program releases
- `release_vision` - Release-level vision
- `technical_debt` - Technical debt tracking

**Purpose**: Program-level coordination and PI planning

**ID Patterns**:
```yaml
naming_conventions:
  program_id: "prg_<name>"
  program_increment_id: "pi_<number>"
  architectural_runway_id: "ar_<name>"
  enabler_id: "enb_<name>"
  release_id: "rel_<name>"
```

**Cross-References** (string patterns):
- `Program.portfolio_ref`: `"^pf_[a-z0-9_]+$"` → Portfolio schema
- `epic.portfolio_ref`: `"^pf_[a-z0-9_]+$"` → Portfolio schema

---

### 3. Team Schema (~350 lines)
**File**: `domains/agile/schemas/team-agile.schema.yaml`

**Concepts** (10):
- `team` - Agile team definition
- `team_member` - Team member roles
- `team_topology` - Team structure
- `role` - Team roles
- `sprint` - Sprint/iteration
- `iteration` - Iteration details
- `ceremony` - Agile ceremonies
- `working_agreement` - Team agreements
- `impediment` - Team impediments
- `feedback_loop` - Team feedback mechanisms

**Purpose**: Team-level organization and execution

**ID Patterns**:
```yaml
naming_conventions:
  team_id: "tm_<name>"
  team_member_id: "mbr_<name>"
  sprint_id: "sp_<number>"
  iteration_id: "it_<number>"
  ceremony_id: "cer_<type>"
  impediment_id: "imp_<number>"
```

**Cross-References** (string patterns):
- `team.program_ref`: `"^prg_[a-z0-9_]+$"` → Program schema
- `sprint.team_ref`: `"^tm_[a-z0-9_]+$"` → Team schema

---

### 4. Delivery Schema (~450 lines)
**File**: `domains/agile/schemas/delivery-agile.schema.yaml`

**Concepts** (8):
- `product` - Product definition
- `vision` - Product vision
- `feature` - Features
- `user_story` - User stories
- `task` - Tasks
- `increment` - Product increments
- `definition_of_ready` - DoR criteria
- `estimation_technique` - Estimation methods

**Purpose**: Product delivery and backlog management

**ID Patterns**:
```yaml
naming_conventions:
  product_id: "prod_<name>"
  vision_id: "vis_<name>"
  feature_id: "feat_<name>"
  user_story_id: "us_<number>"
  task_id: "tsk_<number>"
  increment_id: "inc_<number>"
```

**Cross-References** (string patterns):
- `product.portfolio_ref`: `"^pf_[a-z0-9_]+$"` → Portfolio schema
- `feature.epic_ref`: `"^epic_[a-z0-9_]+$"` → Portfolio schema
- `user_story.feature_ref`: `"^feat_[a-z0-9_]+$"` → Delivery schema
- `task.user_story_ref`: `"^us_[a-z0-9_]+$"` → Delivery schema

---

### 5. SAFe Extensions Schema (~300 lines)
**File**: `domains/agile/schemas/safe-agile.schema.yaml`

**Concepts** (2):
- `agile_release_train` - ART-specific patterns
- `cadence` - SAFe cadence patterns

**Purpose**: SAFe-specific extensions and patterns

**ID Patterns**:
```yaml
naming_conventions:
  art_id: "art_<name>"
  cadence_id: "cad_<name>"
```

**Cross-References** (string patterns):
- `agile_release_train.program_ref`: `"^prg_[a-z0-9_]+$"` → Program schema
- `agile_release_train.teams_refs`: Array of `"^tm_[a-z0-9_]+$"` → Team schema

---

## Cross-Partition Reference Strategy

Following the DDD pattern, we use **string patterns with ID references** instead of JSON Schema `$ref`:

### Example from Portfolio → Program
```yaml
# In portfolio-agile.schema.yaml
epic:
  properties:
    program_refs:
      type: array
      description: "Programs implementing this epic (ID references)"
      items:
        type: string
        pattern: "^prg_[a-z0-9_]+$"
```

### Example from Team → Program
```yaml
# In team-agile.schema.yaml
team:
  properties:
    program_ref:
      type: string
      pattern: "^prg_[a-z0-9_]+$"
      description: "Program this team belongs to (ID reference)"
```

**Benefits**:
- ✅ Loose coupling between schemas
- ✅ No circular dependencies
- ✅ Can validate each schema independently
- ✅ Pattern validation ensures correct ID format

---

## Phase 1: Directory Setup and Backup

**Duration**: 30 minutes
**Risk**: Low

### Step 1.1: Create Directory Structure

```bash
cd /Users/igor/code/canonical-grounding/domains/agile

# Create new directories
mkdir -p schemas
mkdir -p examples/partitioned

# Backup existing files
cp model.schema.yaml model.schema.yaml.backup
```

**Validation**:
```bash
ls -la schemas/
ls -la examples/partitioned/
ls -la model.schema.yaml.backup
```

---

## Phase 2: Create Portfolio Schema

**Duration**: 2-3 hours
**Risk**: Low

### Step 2.1: Extract Portfolio Concepts

**File**: `domains/agile/schemas/portfolio-agile.schema.yaml`

**Content Structure**:
```yaml
$schema: https://json-schema.org/draft/2020-12/schema
$id: https://canonical-grounding.org/schemas/agile/portfolio/v1
title: Agile Portfolio Patterns Schema
description: Portfolio-level patterns for agile at scale - portfolios, value streams, epics, roadmaps

metadata:
  author: "Igor Music"
  created: "2025-10-17"
  updated: "2025-10-17"
  license: "MIT"
  version: "1.0.0"
  partition: "portfolio"
  references:
    - "SAFe 6.0 - Portfolio Level"
    - "Lean Portfolio Management"

naming_conventions:
  portfolio_id: "pf_<name>"
  value_stream_id: "vs_<name>"
  epic_id: "epic_<name>"
  roadmap_id: "rm_<name>"
  stakeholder_id: "sh_<name>"
  metric_id: "met_<name>"
  nfr_id: "nfr_<name>"
  risk_id: "risk_<name>"

$defs:
  portfolio:
    type: object
    description: Portfolio management and governance
    required: [id, name]
    properties:
      id:
        type: string
        pattern: "^pf_[a-z0-9_]+$"
        description: Unique portfolio identifier
      name:
        type: string
        description: Portfolio name
      value_stream_refs:
        type: array
        description: "Value streams in this portfolio (ID references)"
        items:
          type: string
          pattern: "^vs_[a-z0-9_]+$"
      epic_refs:
        type: array
        description: "Portfolio epics (ID references)"
        items:
          type: string
          pattern: "^epic_[a-z0-9_]+$"
      # ... (rest of portfolio definition from original schema)

  value_stream:
    type: object
    description: End-to-end value delivery flow
    required: [id, name, portfolio_ref]
    properties:
      id:
        type: string
        pattern: "^vs_[a-z0-9_]+$"
      portfolio_ref:
        type: string
        pattern: "^pf_[a-z0-9_]+$"
        description: "Portfolio this value stream belongs to (ID reference)"
      # ... (rest from original)

  epic:
    type: object
    description: Large initiative spanning multiple programs
    required: [id, name, portfolio_ref]
    properties:
      id:
        type: string
        pattern: "^epic_[a-z0-9_]+$"
      portfolio_ref:
        type: string
        pattern: "^pf_[a-z0-9_]+$"
        description: "Portfolio this epic belongs to (ID reference)"
      feature_refs:
        type: array
        description: "Features implementing this epic (ID references)"
        items:
          type: string
          pattern: "^feat_[a-z0-9_]+$"
      # ... (rest from original)

  roadmap:
    # ... (extract from original)

  stakeholder:
    # ... (extract from original)

  metric:
    # ... (extract from original)

  non_functional_requirement:
    # ... (extract from original)

  risk:
    # ... (extract from original)

validation_rules:
  - rule: "epic_has_portfolio"
    description: "Every epic must belong to a portfolio"
  - rule: "value_stream_has_portfolio"
    description: "Every value stream must belong to a portfolio"

best_practices:
  portfolio:
    - "Align portfolio epics with business strategy"
    - "Establish clear value streams"
    - "Track portfolio-level metrics and risks"
```

**Actions**:
1. Copy portfolio, value_stream, epic, roadmap, stakeholder, metric, non_functional_requirement, risk from original
2. Convert internal `$ref` to string patterns for cross-partition references
3. Add metadata and naming conventions
4. Validate YAML syntax

**Validation**:
```bash
python3 -c "import yaml; yaml.safe_load(open('schemas/portfolio-agile.schema.yaml'))"
```

---

## Phase 3: Create Program Schema

**Duration**: 2-3 hours
**Risk**: Low

### Step 3.1: Extract Program Concepts

**File**: `domains/agile/schemas/program-agile.schema.yaml`

**Content Structure**:
```yaml
$schema: https://json-schema.org/draft/2020-12/schema
$id: https://canonical-grounding.org/schemas/agile/program/v1
title: Agile Program Patterns Schema
description: Program-level patterns for agile at scale - programs, PIs, releases, architectural runway

metadata:
  author: "Igor Music"
  created: "2025-10-17"
  updated: "2025-10-17"
  license: "MIT"
  version: "1.0.0"
  partition: "program"
  references:
    - "SAFe 6.0 - Program Level"
    - "Program Increment Planning"

naming_conventions:
  program_id: "prg_<name>"
  program_increment_id: "pi_<number>"
  architectural_runway_id: "ar_<name>"
  enabler_id: "enb_<name>"
  release_id: "rel_<name>"
  release_vision_id: "rv_<name>"
  technical_debt_id: "td_<number>"

$defs:
  Program:
    type: object
    description: Program or Agile Release Train
    required: [id, name]
    properties:
      id:
        type: string
        pattern: "^prg_[a-z0-9_]+$"
      portfolio_ref:
        type: string
        pattern: "^pf_[a-z0-9_]+$"
        description: "Portfolio this program belongs to (ID reference)"
      team_refs:
        type: array
        description: "Teams in this program (ID references)"
        items:
          type: string
          pattern: "^tm_[a-z0-9_]+$"
      # ... (rest from original)

  program_increment:
    type: object
    description: Fixed timebox for planning and execution
    required: [id, program_ref]
    properties:
      id:
        type: string
        pattern: "^pi_[a-z0-9_]+$"
      program_ref:
        type: string
        pattern: "^prg_[a-z0-9_]+$"
      # ... (rest from original)

  architectural_runway:
    # ... (extract from original)

  enabler:
    # ... (extract from original)

  release:
    type: object
    description: Program or product release
    required: [id, name, program_ref]
    properties:
      id:
        type: string
        pattern: "^rel_[a-z0-9_]+$"
      program_ref:
        type: string
        pattern: "^prg_[a-z0-9_]+$"
      feature_refs:
        type: array
        description: "Features in this release (ID references)"
        items:
          type: string
          pattern: "^feat_[a-z0-9_]+$"
      # ... (rest from original)

  release_vision:
    # ... (extract from original)

  technical_debt:
    # ... (extract from original)
```

**Actions**:
1. Copy Program, program_increment, architectural_runway, enabler, release, release_vision, technical_debt from original
2. Convert cross-partition references to string patterns
3. Add metadata and naming conventions
4. Validate YAML syntax

---

## Phase 4: Create Team Schema

**Duration**: 2-3 hours
**Risk**: Low

### Step 4.1: Extract Team Concepts

**File**: `domains/agile/schemas/team-agile.schema.yaml`

**Content Structure**:
```yaml
$schema: https://json-schema.org/draft/2020-12/schema
$id: https://canonical-grounding.org/schemas/agile/team/v1
title: Agile Team Patterns Schema
description: Team-level patterns for agile execution - teams, sprints, ceremonies, impediments

metadata:
  author: "Igor Music"
  created: "2025-10-17"
  updated: "2025-10-17"
  license: "MIT"
  version: "1.0.0"
  partition: "team"
  references:
    - "Scrum Guide"
    - "SAFe 6.0 - Team Level"

naming_conventions:
  team_id: "tm_<name>"
  team_member_id: "mbr_<name>"
  team_topology_id: "tt_<name>"
  role_id: "role_<name>"
  sprint_id: "sp_<number>"
  iteration_id: "it_<number>"
  ceremony_id: "cer_<type>"
  working_agreement_id: "wa_<name>"
  impediment_id: "imp_<number>"
  feedback_loop_id: "fb_<name>"

$defs:
  team:
    type: object
    description: Agile team definition
    required: [id, name]
    properties:
      id:
        type: string
        pattern: "^tm_[a-z0-9_]+$"
      program_ref:
        type: string
        pattern: "^prg_[a-z0-9_]+$"
        description: "Program this team belongs to (ID reference)"
      member_refs:
        type: array
        description: "Team members (ID references)"
        items:
          type: string
          pattern: "^mbr_[a-z0-9_]+$"
      # ... (rest from original)

  team_member:
    # ... (extract from original)

  team_topology:
    # ... (extract from original)

  role:
    # ... (extract from original)

  sprint:
    type: object
    description: Fixed timebox for team iteration
    required: [id, team_ref]
    properties:
      id:
        type: string
        pattern: "^sp_[a-z0-9_]+$"
      team_ref:
        type: string
        pattern: "^tm_[a-z0-9_]+$"
      user_story_refs:
        type: array
        description: "User stories in this sprint (ID references)"
        items:
          type: string
          pattern: "^us_[a-z0-9_]+$"
      # ... (rest from original)

  iteration:
    # ... (extract from original)

  ceremony:
    # ... (extract from original)

  working_agreement:
    # ... (extract from original)

  impediment:
    # ... (extract from original)

  feedback_loop:
    # ... (extract from original)
```

---

## Phase 5: Create Delivery Schema

**Duration**: 2-3 hours
**Risk**: Low

### Step 5.1: Extract Delivery Concepts

**File**: `domains/agile/schemas/delivery-agile.schema.yaml`

**Content Structure**:
```yaml
$schema: https://json-schema.org/draft/2020-12/schema
$id: https://canonical-grounding.org/schemas/agile/delivery/v1
title: Agile Delivery Patterns Schema
description: Product delivery patterns - products, features, stories, tasks, increments

metadata:
  author: "Igor Music"
  created: "2025-10-17"
  updated: "2025-10-17"
  license: "MIT"
  version: "1.0.0"
  partition: "delivery"
  references:
    - "Scrum Guide"
    - "SAFe 6.0 - Product Management"

naming_conventions:
  product_id: "prod_<name>"
  vision_id: "vis_<name>"
  feature_id: "feat_<name>"
  user_story_id: "us_<number>"
  task_id: "tsk_<number>"
  increment_id: "inc_<number>"
  dor_id: "dor_<name>"
  estimation_id: "est_<name>"

$defs:
  product:
    type: object
    description: Product being developed
    required: [id, name, vision]
    properties:
      id:
        type: string
        pattern: "^prod_[a-z0-9_]+$"
      portfolio_ref:
        type: string
        pattern: "^pf_[a-z0-9_]+$"
        description: "Portfolio this product belongs to (ID reference)"
      program_refs:
        type: array
        description: "Programs delivering this product (ID references)"
        items:
          type: string
          pattern: "^prg_[a-z0-9_]+$"
      # ... (rest from original)

  vision:
    # ... (extract from original)

  feature:
    type: object
    description: Product feature
    required: [id, name]
    properties:
      id:
        type: string
        pattern: "^feat_[a-z0-9_]+$"
      epic_ref:
        type: string
        pattern: "^epic_[a-z0-9_]+$"
        description: "Epic this feature belongs to (ID reference)"
      user_story_refs:
        type: array
        description: "User stories implementing this feature (ID references)"
        items:
          type: string
          pattern: "^us_[a-z0-9_]+$"
      # ... (rest from original)

  user_story:
    type: object
    description: User story
    required: [id, name]
    properties:
      id:
        type: string
        pattern: "^us_[a-z0-9_]+$"
      feature_ref:
        type: string
        pattern: "^feat_[a-z0-9_]+$"
      task_refs:
        type: array
        description: "Tasks for this story (ID references)"
        items:
          type: string
          pattern: "^tsk_[a-z0-9_]+$"
      # ... (rest from original)

  task:
    # ... (extract from original)

  increment:
    # ... (extract from original)

  definition_of_ready:
    # ... (extract from original)

  estimation_technique:
    # ... (extract from original)
```

---

## Phase 6: Create SAFe Extensions Schema

**Duration**: 1-2 hours
**Risk**: Low

### Step 6.1: Extract SAFe-Specific Concepts

**File**: `domains/agile/schemas/safe-agile.schema.yaml`

**Content Structure**:
```yaml
$schema: https://json-schema.org/draft/2020-12/schema
$id: https://canonical-grounding.org/schemas/agile/safe/v1
title: SAFe Extensions Schema
description: SAFe-specific patterns and extensions - ARTs, cadence patterns

metadata:
  author: "Igor Music"
  created: "2025-10-17"
  updated: "2025-10-17"
  license: "MIT"
  version: "1.0.0"
  partition: "safe"
  references:
    - "SAFe 6.0 - Agile Release Train"
    - "SAFe 6.0 - Cadence and Synchronization"

naming_conventions:
  art_id: "art_<name>"
  cadence_id: "cad_<name>"

$defs:
  agile_release_train:
    type: object
    description: Agile Release Train (ART) pattern from SAFe
    required: [id, name, program_ref]
    properties:
      id:
        type: string
        pattern: "^art_[a-z0-9_]+$"
      program_ref:
        type: string
        pattern: "^prg_[a-z0-9_]+$"
        description: "Program this ART belongs to (ID reference)"
      team_refs:
        type: array
        description: "Teams in this ART (ID references)"
        items:
          type: string
          pattern: "^tm_[a-z0-9_]+$"
      # ... (rest from original)

  cadence:
    type: object
    description: SAFe cadence and synchronization patterns
    required: [id, name]
    properties:
      id:
        type: string
        pattern: "^cad_[a-z0-9_]+$"
      program_ref:
        type: string
        pattern: "^prg_[a-z0-9_]+$"
      # ... (rest from original)
```

---

## Phase 7: Create Partitioned Examples

**Duration**: 2-3 hours
**Risk**: Low

### Step 7.1: Create Portfolio Example

**File**: `domains/agile/examples/partitioned/portfolio-example.yaml`

```yaml
# Portfolio-level example: E-commerce platform portfolio
portfolio:
  id: pf_ecommerce
  name: "E-Commerce Platform Portfolio"
  value_stream_refs: ["vs_online_sales", "vs_fulfillment"]
  epic_refs: ["epic_mobile_app", "epic_ai_recommendations"]

value_streams:
  - id: vs_online_sales
    name: "Online Sales Value Stream"
    portfolio_ref: pf_ecommerce

epics:
  - id: epic_mobile_app
    name: "Mobile App Platform"
    portfolio_ref: pf_ecommerce
    feature_refs: ["feat_ios_app", "feat_android_app"]

roadmap:
  id: rm_ecommerce_2025
  portfolio_ref: pf_ecommerce
  # ... (rest of roadmap)
```

### Step 7.2: Create Program Example

**File**: `domains/agile/examples/partitioned/program-example.yaml`

```yaml
# Program-level example: Mobile platform program
Program:
  id: prg_mobile_platform
  name: "Mobile Platform Program"
  portfolio_ref: pf_ecommerce
  team_refs: ["tm_ios", "tm_android", "tm_backend"]

program_increments:
  - id: pi_2025_q1
    program_ref: prg_mobile_platform
    # ... (rest of PI)

releases:
  - id: rel_mobile_1_0
    name: "Mobile App v1.0"
    program_ref: prg_mobile_platform
    feature_refs: ["feat_ios_app", "feat_android_app"]
```

### Step 7.3: Create Team Example

**File**: `domains/agile/examples/partitioned/team-example.yaml`

```yaml
# Team-level example: iOS team
teams:
  - id: tm_ios
    name: "iOS Development Team"
    program_ref: prg_mobile_platform
    member_refs: ["mbr_john", "mbr_jane"]

team_members:
  - id: mbr_john
    name: "John Doe"
    role: "iOS Developer"

sprints:
  - id: sp_2025_01
    team_ref: tm_ios
    user_story_refs: ["us_login_screen", "us_product_list"]
```

### Step 7.4: Create Delivery Example

**File**: `domains/agile/examples/partitioned/delivery-example.yaml`

```yaml
# Delivery-level example: iOS app product
products:
  - id: prod_ios_app
    name: "E-Commerce iOS App"
    portfolio_ref: pf_ecommerce
    program_refs: ["prg_mobile_platform"]

features:
  - id: feat_ios_app
    name: "iOS Native App"
    epic_ref: epic_mobile_app
    user_story_refs: ["us_login_screen", "us_product_list"]

user_stories:
  - id: us_login_screen
    name: "User Login Screen"
    feature_ref: feat_ios_app
    task_refs: ["tsk_ui_design", "tsk_auth_integration"]

tasks:
  - id: tsk_ui_design
    name: "Design login UI"
    user_story_ref: us_login_screen
```

### Step 7.5: Create SAFe Example

**File**: `domains/agile/examples/partitioned/safe-example.yaml`

```yaml
# SAFe-specific example: ART configuration
agile_release_trains:
  - id: art_mobile_platform
    name: "Mobile Platform ART"
    program_ref: prg_mobile_platform
    team_refs: ["tm_ios", "tm_android", "tm_backend"]

cadences:
  - id: cad_pi_planning
    name: "PI Planning Cadence"
    program_ref: prg_mobile_platform
    cycle_length_weeks: 10
```

### Step 7.6: Keep Original Examples

**Actions**:
- Keep all 5 existing examples in `domains/agile/examples/` (unchanged)
- Original examples:
  - `safe/art-planning.example.yaml`
  - `safe/release-with-vision.example.yaml`
  - `scrum/sprint-planning.example.yaml`
  - `agile/product-with-releases.example.yaml`
  - `agile/product-with-vision.example.yaml`

**Result**: 10 total examples (5 original + 5 new partitioned)

---

## Phase 8: Update Validation Tools

**Duration**: 2-3 hours
**Risk**: Medium

### Step 8.1: Test with Existing Validation Tool

```bash
cd /Users/igor/code/canonical-grounding

# Validate portfolio schema
source venv/bin/activate
python3 partition-examples/tools/validate_multifile_schema.py \
  domains/agile/schemas/portfolio-agile.schema.yaml \
  domains/agile/examples/partitioned/portfolio-example.yaml

# Validate program schema
python3 partition-examples/tools/validate_multifile_schema.py \
  domains/agile/schemas/program-agile.schema.yaml \
  domains/agile/examples/partitioned/program-example.yaml

# Validate team schema
python3 partition-examples/tools/validate_multifile_schema.py \
  domains/agile/schemas/team-agile.schema.yaml \
  domains/agile/examples/partitioned/team-example.yaml

# Validate delivery schema
python3 partition-examples/tools/validate_multifile_schema.py \
  domains/agile/schemas/delivery-agile.schema.yaml \
  domains/agile/examples/partitioned/delivery-example.yaml

# Validate SAFe schema
python3 partition-examples/tools/validate_multifile_schema.py \
  domains/agile/schemas/safe-agile.schema.yaml \
  domains/agile/examples/partitioned/safe-example.yaml
```

### Step 8.2: Create Agile-Specific Validation Script

**File**: `tools/validate-agile-partitions.sh`

```bash
#!/bin/bash
# Validate all Agile partitioned schemas

set -e

AGILE_DIR="domains/agile"
SCHEMAS_DIR="$AGILE_DIR/schemas"
EXAMPLES_DIR="$AGILE_DIR/examples/partitioned"

echo "=== Validating Agile Partitioned Schemas ==="

# Activate venv
source venv/bin/activate

# Validate each partition
for partition in portfolio program team delivery safe; do
  echo ""
  echo "--- Validating ${partition} ---"
  python3 partition-examples/tools/validate_multifile_schema.py \
    "$SCHEMAS_DIR/${partition}-agile.schema.yaml" \
    "$EXAMPLES_DIR/${partition}-example.yaml"
done

echo ""
echo "=== All Agile Partitions Validated Successfully ==="
```

---

## Phase 9: Update Grounding References

**Duration**: 1-2 hours
**Risk**: Medium

### Step 9.1: Update interdomain-map.yaml

**File**: `research-output/interdomain-map.yaml`

The Agile schema partition affects cross-domain grounding references. Update the interdomain map to reflect the new partition structure.

**Current Agile Model Entry**:
```yaml
  - id: "model_agile"
    name: "Agile/SAFe"
    version: "1.0.0"
    layer: "meta"
    closure_percentage: 72
    description: "Work organization and coordination patterns"
    core_concepts:
      - Vision
      - Epic
      - Feature
      - Story
      - Task
      - Sprint
      - PI
      - Team
      - ART
    grounds_in:
      - model_ddd
      - model_ux
      - model_qe
      - model_data_eng
```

**Updated Entry After Partition**:
```yaml
  - id: "model_agile"
    name: "Agile/SAFe"
    version: "2.0.0"  # Updated for partition
    layer: "meta"
    closure_percentage: 95  # Expected improvement after partition
    description: "Work organization and coordination patterns (partitioned by scale)"
    partition_note: "Schema partitioned into 5 schemas: portfolio, program, team, delivery, safe"
    partitions:
      - id: "model_agile_portfolio"
        name: "Agile Portfolio"
        schema_file: "schemas/portfolio-agile.schema.yaml"
        concepts: ["portfolio", "value_stream", "epic", "roadmap", "stakeholder", "metric", "non_functional_requirement", "risk"]
        layer: "strategic"
      - id: "model_agile_program"
        name: "Agile Program"
        schema_file: "schemas/program-agile.schema.yaml"
        concepts: ["Program", "program_increment", "architectural_runway", "enabler", "release", "release_vision", "technical_debt"]
        layer: "program"
      - id: "model_agile_team"
        name: "Agile Team"
        schema_file: "schemas/team-agile.schema.yaml"
        concepts: ["team", "team_member", "team_topology", "role", "sprint", "iteration", "ceremony", "working_agreement", "impediment", "feedback_loop"]
        layer: "execution"
      - id: "model_agile_delivery"
        name: "Agile Delivery"
        schema_file: "schemas/delivery-agile.schema.yaml"
        concepts: ["product", "vision", "feature", "user_story", "task", "increment", "definition_of_ready", "estimation_technique"]
        layer: "delivery"
      - id: "model_agile_safe"
        name: "SAFe Extensions"
        schema_file: "schemas/safe-agile.schema.yaml"
        concepts: ["agile_release_train", "cadence"]
        layer: "framework_extension"
    core_concepts:
      - Vision
      - Epic
      - Feature
      - Story
      - Task
      - Sprint
      - PI
      - Team
      - ART
      - Portfolio
      - Program
    key_patterns:
      - ScrumPattern
      - SAFePattern
      - StoryMapping
      - PortfolioKanban
    grounds_in:
      - model_ddd
      - model_ux
      - model_qe
      - model_data_eng
    grounded_by: []
```

### Step 9.2: Update Specific Grounding Relationships

Update grounding entries to reference specific Agile partitions where applicable:

#### Update UX → Agile Groundings
```yaml
# In groundings section
- id: "g_ux_agile_workflow_story"
  source_model: "model_ux"
  target_model: "model_agile_delivery"  # Now specific to delivery partition
  source_concept: "Workflow"
  target_concept: "user_story"
  grounding_type: "semantic"
  strength: "weak"
  description: "UX workflows can be decomposed into user stories"
  validation_rule: "workflow_story_alignment"
```

#### Update QE → Agile Groundings
```yaml
- id: "g_qe_agile_test_story"
  source_model: "model_qe"
  target_model: "model_agile_delivery"  # Now specific to delivery partition
  source_concept: "TestCase"
  target_concept: "user_story"
  grounding_type: "procedural"
  strength: "strong"
  description: "Test cases validate user story acceptance criteria"
  validation_rule: "test_story_coverage"

- id: "g_qe_agile_test_sprint"
  source_model: "model_qe"
  target_model: "model_agile_team"  # Now specific to team partition
  source_concept: "TestSuite"
  target_concept: "sprint"
  grounding_type: "procedural"
  strength: "strong"
  description: "Test suites executed during sprint"
  validation_rule: "test_suite_sprint_alignment"
```

#### Update DDD → Agile Groundings
```yaml
- id: "g_ddd_agile_feature_context"
  source_model: "model_agile_delivery"  # Now specific to delivery partition
  target_model: "model_ddd"
  source_concept: "feature"
  target_concept: "BoundedContext"
  grounding_type: "structural"
  strength: "strong"
  description: "Features map to bounded contexts"
  validation_rule: "feature_context_alignment"

- id: "g_ddd_agile_epic_domain"
  source_model: "model_agile_portfolio"  # Now specific to portfolio partition
  target_model: "model_ddd"
  source_concept: "epic"
  target_concept: "Domain"
  grounding_type: "structural"
  strength: "strong"
  description: "Epics typically align with domain boundaries"
  validation_rule: "epic_domain_alignment"
```

#### Add New Grounding: Agile → Data-Eng
```yaml
- id: "g_agile_dataeng_feature_pipeline"
  source_model: "model_agile_delivery"
  target_model: "model_data_eng"
  source_concept: "feature"
  target_concept: "Pipeline"
  grounding_type: "procedural"
  strength: "weak"
  description: "Data pipeline features tracked as agile features"
  validation_rule: "feature_pipeline_tracking"

- id: "g_agile_dataeng_story_transform"
  source_model: "model_agile_delivery"
  target_model: "model_data_eng"
  source_concept: "user_story"
  target_concept: "Transform"
  grounding_type: "procedural"
  strength: "weak"
  description: "Transform implementations tracked as user stories"
  validation_rule: "story_transform_tracking"
```

### Step 9.3: Update Grounding Count

Update metadata section:
```yaml
metadata:
  version: "2.1.0"  # Increment version
  total_groundings: 32  # Updated: 28 + 4 new agile-data-eng groundings
  last_updated: "2025-10-17"
  change_note: "Agile schema partitioned into 5 schemas; grounding references updated to specific partitions"
```

### Step 9.4: Add Partition Reference Format

Add documentation section explaining partition references:

```yaml
# ============================================================================
# PARTITION REFERENCE FORMAT
# ============================================================================
#
# For partitioned domains, grounding references use the format:
#   model_<domain>_<partition>
#
# Examples:
#   - model_agile_portfolio  (Agile portfolio partition)
#   - model_agile_program    (Agile program partition)
#   - model_agile_team       (Agile team partition)
#   - model_agile_delivery   (Agile delivery partition)
#   - model_agile_safe       (Agile SAFe extensions)
#   - model_ddd_strategic    (DDD strategic partition) [future]
#   - model_ddd_tactical     (DDD tactical partition) [future]
#
# For non-partitioned domains, continue using:
#   model_<domain>
#
# Examples:
#   - model_ddd      (DDD - monolithic, or references all partitions)
#   - model_ux       (UX - not yet partitioned)
#   - model_qe       (QE - not yet partitioned)
#
# ============================================================================
```

### Step 9.5: Validate Updated Grounding Map

```bash
# Validate YAML syntax
python3 -c "import yaml; yaml.safe_load(open('research-output/interdomain-map.yaml'))"

# Count groundings
grep -c "^- id: \"g_" research-output/interdomain-map.yaml

# Verify all agile partition references exist
grep "model_agile_" research-output/interdomain-map.yaml | sort | uniq
```

**Expected Output**:
- YAML validates successfully
- Grounding count matches metadata (32)
- All 5 agile partitions referenced: portfolio, program, team, delivery, safe

### Step 9.6: Update Grounding Visualization

If grounding graphs exist, regenerate them:

```bash
# Regenerate grounding graph
python3 tools/generate-grounding-graph.py

# Check output
ls -la grounding-graph.{dot,png,svg}
```

This will show Agile as 5 separate nodes (partitions) instead of one monolithic node.

---

## Phase 10: Documentation and Cleanup

**Duration**: 1-2 hours
**Risk**: Low

### Step 10.1: Update README

Add to `domains/agile/README.md`:

```markdown
## Schema Organization

The Agile domain schema is partitioned into 5 schemas for better maintainability:

### Schemas

1. **portfolio-agile.schema.yaml** - Portfolio-level patterns
   - Concepts: portfolio, value_stream, epic, roadmap, stakeholder, metric, NFR, risk
   - Use for: Strategic planning, portfolio management

2. **program-agile.schema.yaml** - Program-level patterns
   - Concepts: Program, program_increment, architectural_runway, enabler, release, release_vision, technical_debt
   - Use for: PI planning, program coordination

3. **team-agile.schema.yaml** - Team-level patterns
   - Concepts: team, team_member, team_topology, role, sprint, iteration, ceremony, working_agreement, impediment, feedback_loop
   - Use for: Team organization, sprint planning

4. **delivery-agile.schema.yaml** - Delivery patterns
   - Concepts: product, vision, feature, user_story, task, increment, definition_of_ready, estimation_technique
   - Use for: Backlog management, product delivery

5. **safe-agile.schema.yaml** - SAFe extensions
   - Concepts: agile_release_train, cadence
   - Use for: SAFe-specific patterns

### Examples

- **Original examples** (backward compatibility): `examples/safe/`, `examples/scrum/`, `examples/agile/`
- **Partitioned examples**: `examples/partitioned/`

### Cross-References

Schemas use string pattern references (not `$ref`) for loose coupling:
- Portfolio IDs: `pf_<name>`
- Program IDs: `prg_<name>`
- Team IDs: `tm_<name>`
- Feature IDs: `feat_<name>`
- User Story IDs: `us_<number>`

Example:
```yaml
# In program-agile.schema.yaml
Program:
  properties:
    portfolio_ref:
      type: string
      pattern: "^pf_[a-z0-9_]+$"  # References portfolio schema
```
```

### Step 9.2: Create Migration Guide

**File**: `domains/agile/MIGRATION.md`

```markdown
# Agile Schema Migration Guide

## Overview

The Agile schema has been partitioned from a single 1,972-line file into 5 focused schemas. This guide helps you migrate existing data.

## For Existing Users

### Option 1: Continue Using Original Schema
- File: `model.schema.yaml`
- Status: Preserved for backward compatibility
- No changes needed

### Option 2: Migrate to Partitioned Schemas

#### Step 1: Identify Your Scope
Determine which schemas you need:
- **Portfolio only**: Use `portfolio-agile.schema.yaml`
- **Program/PI planning**: Use `program-agile.schema.yaml` + `portfolio-agile.schema.yaml`
- **Team/Sprint**: Use `team-agile.schema.yaml` + `program-agile.schema.yaml`
- **Full stack**: Use all 5 schemas

#### Step 2: Update References
Change internal `$ref` to ID references with patterns:

**Before** (monolithic):
```yaml
epic:
  program:
    $ref: '#/$defs/Program'
```

**After** (partitioned):
```yaml
epic:
  program_ref: prg_mobile_platform  # String ID reference
```

#### Step 3: Validate
```bash
./tools/validate-agile-partitions.sh
```

## Benefits of Partitioning

1. **Smaller files**: 300-500 lines each vs. 1,972 lines
2. **Clearer boundaries**: Portfolio → Program → Team → Delivery
3. **Easier navigation**: Find concepts faster
4. **Better collaboration**: Less merge conflicts
5. **Flexible usage**: Use only what you need

## SAFe Extensions

SAFe-specific concepts (ART, cadence) are now in `safe-agile.schema.yaml`. If you don't use SAFe, you can skip this schema entirely.

## Questions?

See `README.md` for schema organization details.
```


---

## Final Directory Structure

```
domains/agile/
├── schemas/
│   ├── portfolio-agile.schema.yaml    (~400 lines)
│   ├── program-agile.schema.yaml      (~450 lines)
│   ├── team-agile.schema.yaml         (~350 lines)
│   ├── delivery-agile.schema.yaml     (~450 lines)
│   └── safe-agile.schema.yaml         (~300 lines)
├── examples/
│   ├── partitioned/                    (NEW)
│   │   ├── portfolio-example.yaml
│   │   ├── program-example.yaml
│   │   ├── team-example.yaml
│   │   ├── delivery-example.yaml
│   │   └── safe-example.yaml
│   ├── safe/                           (KEPT)
│   │   ├── art-planning.example.yaml
│   │   └── release-with-vision.example.yaml
│   ├── scrum/                          (KEPT)
│   │   └── sprint-planning.example.yaml
│   └── agile/                          (KEPT)
│       ├── product-with-releases.example.yaml
│       └── product-with-vision.example.yaml
├── docs/                               (KEPT)
│   └── (all existing docs)
├── model.schema.yaml                   (KEPT - backward compatibility)
├── model.schema.yaml.backup            (NEW)
├── README.md                           (UPDATED)
└── MIGRATION.md                        (NEW)
```

---

## Success Criteria

- ✅ All 5 schemas validate as proper YAML
- ✅ All 5 schemas are valid JSON Schema 2020-12
- ✅ All 5 partitioned examples validate against their schemas
- ✅ Original 5 examples still work (backward compatibility)
- ✅ Cross-partition references use string patterns correctly
- ✅ All schemas <500 lines
- ✅ Documentation updated
- ✅ Validation tools work with partitioned schemas

---

## Rollback Plan

If issues arise:

1. **Restore original schema**:
   ```bash
   cp model.schema.yaml.backup model.schema.yaml
   ```

2. **Remove partitioned files**:
   ```bash
   rm -rf schemas/
   rm -rf examples/partitioned/
   ```

3. **Revert documentation**:
   ```bash
   git checkout README.md MIGRATION.md
   ```

---

## Timeline

| Phase | Duration | Dependencies |
|-------|----------|--------------|
| Phase 1: Setup | 30 min | None |
| Phase 2: Portfolio Schema | 2-3 hours | Phase 1 |
| Phase 3: Program Schema | 2-3 hours | Phase 1 |
| Phase 4: Team Schema | 2-3 hours | Phase 1 |
| Phase 5: Delivery Schema | 2-3 hours | Phase 1 |
| Phase 6: SAFe Schema | 1-2 hours | Phase 1 |
| Phase 7: Examples | 2-3 hours | Phases 2-6 |
| Phase 8: Validation | 2-3 hours | Phase 7 |
| Phase 9: Grounding Updates | 1-2 hours | Phase 8 |
| Phase 10: Documentation | 1-2 hours | Phase 9 |
| **Total** | **4-5 days** | |

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Cross-reference errors | Medium | High | Validate patterns carefully, test examples |
| Breaking existing tools | Low | Medium | Keep original schema, test all tools |
| Incomplete migration | Low | Medium | Follow checklist, validate all concepts |
| SAFe concepts misplaced | Low | Low | Review with SAFe expert |

---

## Next Steps

1. **Review this plan** - Ensure partition strategy matches your needs
2. **Execute Phase 1** - Set up directories and backups
3. **Implement Phases 2-6** - Create partitioned schemas
4. **Validate** - Test all schemas and examples
5. **Document** - Update README and create migration guide
6. **Commit** - Version control the changes

---

**Status**: ✅ Ready for Implementation
**Approach**: Proven (DDD partition success)
**Risk**: Low (backward compatible)
**Effort**: 4-5 days

---

*Created: 2025-10-17*
*Based on: DDD partition pattern, partition-research.md findings*
*For: Agile domain model partitioning (1,972 lines → 5 schemas)*
