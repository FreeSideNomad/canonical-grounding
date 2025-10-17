# UX Schema Partition Plan

## Executive Summary

**Purpose**: Partition the UX (User Experience) canonical domain model schema from a single 1,141-line file into 3 focused schemas organized by architectural layer.

**Current State**:
- File: `domains/ux/model-schema.yaml`
- Size: 1,141 lines
- Concepts: ~12 core concepts
- Structure: Monolithic schema with all UX patterns

**Target State**:
- Files: 3 partitioned schemas
- Organization: By architectural layer (Structure → Navigation → Interaction)
- Cross-references: String pattern ID references
- Backward compatibility: Original schema preserved

**Rationale**: The UX domain naturally divides into three architectural layers:
1. **Information Architecture** - How information is organized and structured
2. **Navigation & Wayfinding** - How users move through the system
3. **Interaction & Components** - How users interact with UI elements

This partition aligns with established UX practice (Information Architecture → Interaction Design → Visual Design) and improves maintainability.

## Research: DDD Grounding Analysis

### Current UX → DDD Groundings

Based on `research-output/interdomain-map.yaml`, UX has 5 strong groundings to DDD:

1. **grounding_ux_ddd_001**: Pages reference DDD bounded contexts
   - `ux:Page → ddd:bounded_context` (many-to-one, required)
   - Pages exist within domain contexts

2. **grounding_ux_ddd_002**: Workflows reference DDD aggregates
   - `ux:Workflow → ddd:Aggregate` (many-to-many, required)
   - Workflows manipulate domain aggregates

3. **grounding_ux_ddd_003**: Navigation mirrors DDD domain structure
   - `ux:Navigation → ddd:Domain` (alignment)
   - Navigation follows domain decomposition

4. **grounding_ux_ddd_004**: Component labels use DDD ubiquitous language
   - `ux:component → ddd:domain` (alignment)
   - UI terminology matches domain terminology

5. **grounding_ux_ddd_005**: Workflows respect DDD aggregate boundaries
   - `ux:Workflow.steps → ddd:Aggregate.invariants` (constraint)
   - Multi-step workflows require saga pattern

### Concept-to-Partition Mapping for DDD Grounding

| UX Concept | Target Partition | DDD Grounding | Reason |
|------------|------------------|---------------|---------|
| Page | structure | Page → BoundedContext | Pages are structural elements scoped to contexts |
| Workflow | interaction | Workflow → Aggregate | Workflows are interaction sequences manipulating aggregates |
| Navigation | navigation | Navigation → Domain | Navigation is wayfinding across domains |
| Component | interaction | Component → Domain | Components are interaction elements using ubiquitous language |
| InformationArchitecture | structure | IA → Domain | IA organizes content by domain structure |

### Grounding Updates Required

After partitioning, update groundings to reference specific partitions:

- `grounding_ux_ddd_001`: `model_ux` → `model_ux_structure` (Page concept)
- `grounding_ux_ddd_002`: `model_ux` → `model_ux_interaction` (Workflow concept)
- `grounding_ux_ddd_003`: `model_ux` → `model_ux_navigation` (Navigation concept)
- `grounding_ux_ddd_004`: `model_ux` → `model_ux_interaction` (Component concept)
- `grounding_ux_ddd_005`: `model_ux` → `model_ux_interaction` (Workflow.steps concept)

## Partition Strategy

### Option A: By Architectural Layer (RECOMMENDED)

Organize by the natural layers of UX design:

1. **structure-ux.schema.yaml** - Information Architecture & Structure
   - Concepts: InformationArchitecture, HierarchyNode, Facet, SearchSystem, LabelingSystem
   - Size estimate: ~350 lines
   - Focus: How information is organized, structured, and categorized

2. **navigation-ux.schema.yaml** - Navigation & Wayfinding
   - Concepts: Navigation, Page, Breadcrumbs, Sitemap
   - Size estimate: ~400 lines
   - Focus: How users navigate and find their way through the system

3. **interaction-ux.schema.yaml** - Interaction & Components
   - Concepts: Workflow, Component, Behavior, Animation, ValidationConfig, DesignTokens, Accessibility
   - Size estimate: ~500 lines
   - Focus: How users interact with UI elements and components

**Benefits**:
- Aligns with UX professional practice (IA → Navigation → Interaction)
- Clear separation of concerns by abstraction level
- Natural progression: Structure → Wayfinding → Action
- Matches typical UX team specializations

**DDD Grounding Alignment**: ✅ Excellent
- Structure layer grounds pages in bounded contexts
- Navigation layer grounds navigation in domain structure
- Interaction layer grounds workflows/components in aggregates and ubiquitous language

### Option B: By User Journey Phase

1. **discovery-ux.schema.yaml** - Discovery & Search
2. **engagement-ux.schema.yaml** - Content & Navigation
3. **transaction-ux.schema.yaml** - Forms & Workflows

**Benefits**: Aligns with user journey stages

**Drawbacks**: Less clear technical boundaries, concepts span multiple phases

**Recommendation**: Option A (Architectural Layer) is preferred.

## Detailed Partition Specification

### Partition 1: structure-ux.schema.yaml

**Purpose**: Define how information is organized, structured, and made findable

**Concepts** (5 concepts, ~350 lines):
1. `information_architecture` - Overall IA structure and organization schemes
2. `hierarchy_node` - Nodes in hierarchical organization
3. `facet` - Faceted classification dimensions
4. `facet_value` - Values within facets
5. `search_system` - Search configuration and indexing

**Naming Conventions**:
- IA ID: `ia_<name>` (e.g., `ia_ecommerce`)
- Hierarchy Node ID: `hn_<name>` (e.g., `hn_products`)
- Facet ID: `facet_<name>` (e.g., `facet_category`)
- Search System ID: `search_<name>` (e.g., `search_products`)

**Cross-References**:
- `information_architecture.hierarchy_nodes` → `hn_*` (string pattern)
- `information_architecture.facets` → `facet_*` (string pattern)
- `information_architecture.search_system` → `search_*` (string pattern)
- `hierarchy_node.parent_ref` → `hn_*` (string pattern)
- `facet.facet_value_refs` → `fv_*` (string pattern)

**DDD Groundings**:
- `information_architecture` → `ddd:Domain` (semantic alignment)
- `hierarchy_node` → `ddd:BoundedContext` (structural mapping)

**Key Patterns**:
- Hierarchical IA
- Faceted classification
- Search indexing
- Controlled vocabularies

### Partition 2: navigation-ux.schema.yaml

**Purpose**: Define how users navigate and find their way through the system

**Concepts** (4 concepts, ~400 lines):
1. `navigation` - Navigation structures (global, local, contextual)
2. `page` - Page definitions with sections and layout
3. `page_section` - Sections within pages
4. `breadcrumb` - Breadcrumb navigation trails

**Naming Conventions**:
- Navigation ID: `nav_<name>` (e.g., `nav_global`)
- Page ID: `page_<name>` (e.g., `page_product_detail`)
- Page Section ID: `sect_<name>` (e.g., `sect_header`)
- Breadcrumb ID: `bc_<name>` (e.g., `bc_product_path`)

**Cross-References**:
- `navigation.items.target` → `page_*` (string pattern)
- `page.information_architecture_ref` → `ia_*` (cross-partition to structure)
- `page.navigation_ref` → `nav_*` (string pattern)
- `page.sections` → `sect_*` (string pattern)
- `page.bounded_context_ref` → `bc_*` (cross-domain to DDD)
- `breadcrumb.page_refs` → `page_*` (string pattern)

**DDD Groundings**:
- `page` → `ddd:BoundedContext` (many-to-one, required) - **PRIMARY GROUNDING**
- `navigation` → `ddd:Domain` (semantic alignment)

**Key Patterns**:
- Global navigation (top nav, sidebar)
- Local navigation (contextual links)
- Breadcrumb trails
- Page templates

### Partition 3: interaction-ux.schema.yaml

**Purpose**: Define how users interact with UI elements and complete tasks

**Concepts** (8 concepts, ~500 lines):
1. `workflow` - Multi-step user workflows
2. `component` - Reusable UI components
3. `behavior` - Interactive behaviors and event handling
4. `animation` - Animation specifications
5. `validation_config` - Form validation rules
6. `responsive_config` - Responsive breakpoints and layouts
7. `design_tokens` - Design system tokens (colors, spacing, typography)
8. `accessibility_spec` - Accessibility specifications (WCAG compliance)

**Naming Conventions**:
- Workflow ID: `wf_<name>` (e.g., `wf_checkout`)
- Component ID: `cmp_<name>` (e.g., `cmp_button`)
- Behavior ID: `beh_<name>` (e.g., `beh_dropdown`)
- Animation ID: `anim_<name>` (e.g., `anim_fade_in`)

**Cross-References**:
- `workflow.pages` → `page_*` (cross-partition to navigation)
- `workflow.components` → `cmp_*` (string pattern)
- `workflow.aggregate_refs` → `agg_*` (cross-domain to DDD)
- `component.page_refs` → `page_*` (cross-partition to navigation)
- `component.behaviors` → `beh_*` (string pattern)
- `component.design_token_refs` → `dt_*` (string pattern)

**DDD Groundings**:
- `workflow` → `ddd:Aggregate` (many-to-many, required) - **PRIMARY GROUNDING**
- `workflow.steps` → `ddd:Aggregate.invariants` (constraint validation)
- `component` → `ddd:Domain` (semantic alignment via ubiquitous language)

**Key Patterns**:
- Multi-step workflows
- Atomic design components
- Progressive disclosure
- Form validation
- Responsive design
- Accessibility patterns

## Cross-Partition Dependencies

### Structure → Navigation
- Pages reference IA nodes for organization

### Navigation → Interaction
- Pages contain workflows and components
- Workflows span multiple pages

### Structure ← Navigation ← Interaction (Dependency Flow)
```
┌──────────────┐
│  Structure   │  Foundation: How info is organized
│  (IA)        │
└──────┬───────┘
       │ grounds
       ↓
┌──────────────┐
│  Navigation  │  Wayfinding: How users navigate
│  (Pages)     │
└──────┬───────┘
       │ grounds
       ↓
┌──────────────┐
│  Interaction │  Action: How users interact
│  (Workflows) │
└──────────────┘
```

## Implementation Plan

### Phase 1: Setup and Backup (15 min)

**Actions**:
```bash
cd domains/ux

# Create directories
mkdir -p schemas examples/partitioned

# Backup original schema
cp model-schema.yaml model-schema.yaml.backup
```

### Phase 2: Create structure-ux.schema.yaml (1-2 hours)

**Extract concepts**:
- information_architecture
- hierarchy_node
- facet
- facet_value
- search_system

**File**: `domains/ux/schemas/structure-ux.schema.yaml`

**Metadata**:
```yaml
$schema: https://json-schema.org/draft/2020-12/schema
$id: https://canonical-grounding.org/schemas/ux/structure/v1
title: UX Information Architecture Schema
description: Information architecture, organization schemes, and content structure patterns

metadata:
  author: "Igor Music"
  created: "2025-10-17"
  updated: "2025-10-17"
  license: "MIT"
  version: "1.0.0"
  partition: "structure"
  references:
    - "Louis Rosenfeld & Peter Morville - Information Architecture (4th ed, 2015)"
    - "Donna Spencer - A Practical Guide to Information Architecture (2014)"
```

**Naming conventions**:
```yaml
naming_conventions:
  information_architecture_id: "ia_<name>"
  hierarchy_node_id: "hn_<name>"
  facet_id: "facet_<name>"
  facet_value_id: "fv_<name>"
  search_system_id: "search_<name>"
```

### Phase 3: Create navigation-ux.schema.yaml (1-2 hours)

**Extract concepts**:
- navigation
- page
- page_section
- breadcrumb

**File**: `domains/ux/schemas/navigation-ux.schema.yaml`

**Metadata**:
```yaml
$schema: https://json-schema.org/draft/2020-12/schema
$id: https://canonical-grounding.org/schemas/ux/navigation/v1
title: UX Navigation Schema
description: Navigation patterns, page structures, and wayfinding systems

metadata:
  author: "Igor Music"
  created: "2025-10-17"
  updated: "2025-10-17"
  license: "MIT"
  version: "1.0.0"
  partition: "navigation"
  references:
    - "Steve Krug - Don't Make Me Think (3rd ed, 2014)"
    - "Jakob Nielsen - Navigation Design Patterns"
```

**Naming conventions**:
```yaml
naming_conventions:
  navigation_id: "nav_<name>"
  page_id: "page_<name>"
  page_section_id: "sect_<name>"
  breadcrumb_id: "bc_<name>"
```

### Phase 4: Create interaction-ux.schema.yaml (2-3 hours)

**Extract concepts**:
- workflow
- component
- behavior
- animation
- validation_config
- responsive_config
- design_tokens
- accessibility_spec

**File**: `domains/ux/schemas/interaction-ux.schema.yaml`

**Metadata**:
```yaml
$schema: https://json-schema.org/draft/2020-12/schema
$id: https://canonical-grounding.org/schemas/ux/interaction/v1
title: UX Interaction Schema
description: User workflows, UI components, behaviors, and interaction patterns

metadata:
  author: "Igor Music"
  created: "2025-10-17"
  updated: "2025-10-17"
  license: "MIT"
  version: "1.0.0"
  partition: "interaction"
  references:
    - "Brad Frost - Atomic Design (2016)"
    - "Dan Saffer - Microinteractions (2013)"
    - "WCAG 2.1 - Web Content Accessibility Guidelines"
```

**Naming conventions**:
```yaml
naming_conventions:
  workflow_id: "wf_<name>"
  component_id: "cmp_<name>"
  behavior_id: "beh_<name>"
  animation_id: "anim_<name>"
  validation_config_id: "val_<name>"
  design_token_id: "dt_<name>"
```

### Phase 5: Create Partitioned Examples (2-3 hours)

Create 3 examples demonstrating e-commerce product catalog:

**File**: `examples/partitioned/structure-example.yaml`
- Information architecture for product catalog
- Hierarchical organization (Categories → Subcategories → Products)
- Faceted search (Brand, Price, Rating, Color)
- Search system configuration

**File**: `examples/partitioned/navigation-example.yaml`
- Global navigation (Home, Products, Cart, Account)
- Product detail page structure
- Breadcrumb trail (Home → Electronics → Laptops → MacBook Pro)
- Page sections (Header, ProductInfo, Reviews, RelatedProducts)

**File**: `examples/partitioned/interaction-example.yaml`
- Add to cart workflow
- Product image carousel component
- Rating widget component
- Form validation (email, credit card)
- Design tokens (colors, spacing)
- Accessibility specs (ARIA labels, keyboard navigation)

### Phase 6: Validate All Schemas (30 min)

```bash
source venv/bin/activate

# Validate structure
python3 partition-examples/tools/validate_multifile_schema.py \
  domains/ux/schemas/structure-ux.schema.yaml \
  domains/ux/examples/partitioned/structure-example.yaml

# Validate navigation
python3 partition-examples/tools/validate_multifile_schema.py \
  domains/ux/schemas/navigation-ux.schema.yaml \
  domains/ux/examples/partitioned/navigation-example.yaml

# Validate interaction
python3 partition-examples/tools/validate_multifile_schema.py \
  domains/ux/schemas/interaction-ux.schema.yaml \
  domains/ux/examples/partitioned/interaction-example.yaml
```

### Phase 7: Update Grounding References (1-2 hours)

**File**: `research-output/interdomain-map.yaml`

Update UX model entry:
```yaml
- id: "model_ux"
  name: "User Experience"
  version: "2.0.0"  # Updated for partition
  layer: "derived"
  closure_percentage: 100  # Expected improvement
  description: "User interface and interaction patterns (partitioned by architectural layer)"
  partition_note: "Schema partitioned into 3 schemas: structure, navigation, interaction"
  partitions:
    - id: "model_ux_structure"
      name: "UX Structure"
      schema_file: "schemas/structure-ux.schema.yaml"
      concepts: ["information_architecture", "hierarchy_node", "facet", "facet_value", "search_system"]
      layer: "foundation"
    - id: "model_ux_navigation"
      name: "UX Navigation"
      schema_file: "schemas/navigation-ux.schema.yaml"
      concepts: ["navigation", "page", "page_section", "breadcrumb"]
      layer: "wayfinding"
    - id: "model_ux_interaction"
      name: "UX Interaction"
      schema_file: "schemas/interaction-ux.schema.yaml"
      concepts: ["workflow", "component", "behavior", "animation", "validation_config", "responsive_config", "design_tokens", "accessibility_spec"]
      layer: "interaction"
```

Update groundings:
```yaml
# Update grounding_ux_ddd_001
- id: "grounding_ux_ddd_001"
  source: "model_ux_navigation"  # Changed from model_ux
  target: "model_ddd"
  # ... rest unchanged

# Update grounding_ux_ddd_002
- id: "grounding_ux_ddd_002"
  source: "model_ux_interaction"  # Changed from model_ux
  target: "model_ddd"
  # ... rest unchanged

# Update grounding_ux_ddd_003
- id: "grounding_ux_ddd_003"
  source: "model_ux_navigation"  # Changed from model_ux
  target: "model_ddd"
  # ... rest unchanged

# Update grounding_ux_ddd_004
- id: "grounding_ux_ddd_004"
  source: "model_ux_interaction"  # Changed from model_ux
  target: "model_ddd"
  # ... rest unchanged

# Update grounding_ux_ddd_005
- id: "grounding_ux_ddd_005"
  source: "model_ux_interaction"  # Changed from model_ux
  target: "model_ddd"
  # ... rest unchanged
```

Update metadata:
```yaml
metadata:
  version: "2.2.0"  # Increment
  total_groundings: 32  # Unchanged
  last_updated: "2025-10-17"
  change_note: "UX schema partitioned into 3 schemas; grounding references updated to specific partitions"
```

### Phase 8: Create Documentation (1-2 hours)

**File**: `domains/ux/README.md`
- Overview of UX canonical domain model
- Schema organization (3 partitions)
- Cross-references and ID conventions
- DDD grounding relationships
- Usage examples
- Validation instructions

**File**: `domains/ux/MIGRATION.md`
- Migration guide from monolithic to partitioned
- Before/after comparison
- Step-by-step migration process
- Benefits of partitioning

## Timeline Estimate

| Phase | Duration | Risk |
|-------|----------|------|
| Phase 1: Setup | 15 min | Low |
| Phase 2: Structure schema | 1-2 hours | Low |
| Phase 3: Navigation schema | 1-2 hours | Medium |
| Phase 4: Interaction schema | 2-3 hours | Medium |
| Phase 5: Examples | 2-3 hours | Medium |
| Phase 6: Validation | 30 min | Low |
| Phase 7: Grounding updates | 1-2 hours | Medium |
| Phase 8: Documentation | 1-2 hours | Low |
| **Total** | **9-14 hours (~2 days)** | Medium |

## Success Criteria

### Technical Validation
- [ ] All 3 schemas validate as JSON Schema 2020-12 ✅
- [ ] All 3 examples validate against their schemas ✅
- [ ] All cross-partition references use string patterns ✅
- [ ] No circular dependencies between partitions ✅

### Grounding Validation
- [ ] All 5 UX → DDD groundings updated to reference partitions ✅
- [ ] Grounding map validates successfully ✅
- [ ] Pages correctly reference bounded contexts (navigation partition) ✅
- [ ] Workflows correctly reference aggregates (interaction partition) ✅

### Completeness
- [ ] Original 12 concepts distributed across 3 partitions ✅
- [ ] No concepts lost or duplicated ✅
- [ ] Concept distribution balanced (structure: 5, navigation: 4, interaction: 8) ✅

### Documentation
- [ ] README.md created with usage guide ✅
- [ ] MIGRATION.md created with migration path ✅
- [ ] Examples demonstrate realistic use cases ✅

## Risk Mitigation

### Risk 1: Complex Cross-Partition References
**Impact**: Medium
**Mitigation**: Use string pattern validation, create comprehensive examples

### Risk 2: DDD Grounding Ambiguity
**Impact**: High (affects semantic correctness)
**Mitigation**: Research existing groundings thoroughly, validate with examples

### Risk 3: Concept Distribution Imbalance
**Impact**: Low
**Mitigation**: Use established UX architectural layers, review with UX practitioners

## Benefits

1. **Clearer Boundaries**: Separation by architectural layer (IA → Navigation → Interaction)
2. **Better Alignment**: Matches UX professional practice and team structures
3. **Improved Maintainability**: Smaller files (~350-500 lines vs 1,141 lines)
4. **Flexible Usage**: Use only what you need (e.g., just navigation patterns)
5. **Stronger DDD Grounding**: Partition-specific groundings are more precise
6. **Better Collaboration**: UX architects, interaction designers, and accessibility specialists work on separate files

## Open Questions

1. **Should design_tokens be in a separate partition?**
   - Current: In interaction partition
   - Alternative: Create design-system-ux.schema.yaml
   - Decision: Keep in interaction (closely tied to components)

2. **Should accessibility_spec span all partitions?**
   - Current: In interaction partition
   - Alternative: Duplicate in all 3 partitions
   - Decision: Keep in interaction (most accessibility issues are interaction-related)

3. **Should page_section be its own concept or nested in page?**
   - Current: Separate concept
   - Alternative: Nested property of page
   - Decision: Keep separate (allows reuse across pages)

## References

- **Information Architecture**: Rosenfeld & Morville - Information Architecture for the Web and Beyond (4th ed)
- **Interaction Design**: Dan Saffer - Designing for Interaction (2nd ed)
- **Atomic Design**: Brad Frost - Atomic Design (2016)
- **Accessibility**: WCAG 2.1 - Web Content Accessibility Guidelines
- **DDD Grounding**: Evans - Domain-Driven Design (2003)
