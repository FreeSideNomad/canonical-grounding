# User Experience (UX) Canonical Domain Model

## Overview

The UX canonical domain model provides patterns for user interface design, information architecture, navigation, and interaction design. It covers the full spectrum of UX practice from information organization to component-level interactions.

## Schema Organization

The UX domain schema is **partitioned into 3 schemas** organized by architectural layer:

### Schemas

1. **structure-ux.schema.yaml** - Information Architecture & Structure
   - **Concepts**: information_architecture, hierarchy_node, facet, facet_value, search_system
   - **Use for**: Content organization, taxonomy, faceted navigation, search configuration
   - **Layer**: Foundation - How information is organized and made findable

2. **navigation-ux.schema.yaml** - Navigation & Wayfinding
   - **Concepts**: navigation, page, page_section, breadcrumb, responsive_config
   - **Use for**: Navigation structures, page layouts, breadcrumb trails, wayfinding systems
   - **Layer**: Wayfinding - How users navigate through the system

3. **interaction-ux.schema.yaml** - Interaction & Components
   - **Concepts**: workflow, component, behavior, animation, validation_config, design_tokens, accessibility_spec
   - **Use for**: User workflows, UI components, behaviors, design systems, accessibility
   - **Layer**: Interaction - How users interact with UI elements

### Architectural Layers

```
┌──────────────────┐
│   Structure      │  Foundation: IA, taxonomy, search
│   (5 concepts)   │
└────────┬─────────┘
         │ grounds
         ↓
┌──────────────────┐
│   Navigation     │  Wayfinding: Nav, pages, breadcrumbs
│   (5 concepts)   │
└────────┬─────────┘
         │ grounds
         ↓
┌──────────────────┐
│   Interaction    │  Action: Workflows, components, behaviors
│   (7 concepts)   │
└──────────────────┘
```

## Cross-References

Schemas use **string pattern references** (not JSON Schema `$ref`) for loose coupling across partitions:

### ID Naming Conventions

- **Structure**:
  - Information Architecture: `ia_<name>` (e.g., `ia_ecommerce_products`)
  - Hierarchy Node: `hn_<name>` (e.g., `hn_electronics`)
  - Facet: `facet_<name>` (e.g., `facet_brand`)
  - Facet Value: `fv_<name>` (e.g., `fv_apple`)
  - Search System: `search_<name>` (e.g., `search_products`)

- **Navigation**:
  - Navigation: `nav_<name>` (e.g., `nav_global`)
  - Page: `page_<name>` (e.g., `page_product_detail`)
  - Page Section: `sect_<name>` (e.g., `sect_header`)
  - Breadcrumb: `bc_<name>` (e.g., `bc_product_path`)

- **Interaction**:
  - Workflow: `wf_<name>` (e.g., `wf_checkout`)
  - Component: `cmp_<name>` (e.g., `cmp_button`)
  - Behavior: `beh_<name>` (e.g., `beh_hover`)
  - Animation: `anim_<name>` (e.g., `anim_fade_in`)
  - Design Token: `dt_<name>` (e.g., `dt_color_primary`)

### Example Cross-References

```yaml
# In navigation-ux.schema.yaml
page:
  properties:
    information_architecture_ref:
      type: string
      pattern: "^ia_[a-z0-9_]+$"  # Cross-partition to structure
    bounded_context_ref:
      type: string
      pattern: "^bc_[a-z0-9_]+$"  # Cross-domain to DDD

# In interaction-ux.schema.yaml
workflow:
  properties:
    page_refs:
      type: array
      items:
        type: string
        pattern: "^page_[a-z0-9_]+$"  # Cross-partition to navigation
    aggregate_refs:
      type: array
      items:
        type: string
        pattern: "^agg_[a-z0-9_]+$"  # Cross-domain to DDD
```

## DDD Grounding Relationships

The UX model has strong groundings to DDD:

### Primary Groundings

1. **Page → BoundedContext** (navigation partition)
   - Pages exist within domain contexts
   - `page.bounded_context_ref` → `ddd:BoundedContext` (required)

2. **Workflow → Aggregate** (interaction partition)
   - Workflows manipulate domain aggregates
   - `workflow.aggregate_refs` → `ddd:Aggregate` (many-to-many)

3. **Navigation → Domain** (navigation partition)
   - Navigation structure follows domain decomposition
   - Primary nav sections correspond to domain boundaries

4. **Component → Domain** (interaction partition)
   - Component labels use DDD ubiquitous language
   - UI terminology matches domain terminology (>80%)

5. **Workflow.steps → Aggregate.invariants** (interaction partition)
   - Workflows respect aggregate boundaries
   - Multi-step workflows crossing aggregates require saga pattern

For complete grounding specifications, see `research-output/interdomain-map.yaml`.

## Examples

The domain includes 3 partitioned examples demonstrating e-commerce product catalog:

- **structure-example.yaml**: Product catalog IA with hierarchical categories, faceted filters, and search
- **navigation-example.yaml**: Navigation structures, page layouts, and breadcrumb trails
- **interaction-example.yaml**: Add-to-cart and checkout workflows, components, and design tokens

## Usage

### Validation

Validate schemas and examples:

```bash
cd /path/to/canonical-grounding
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

### Integration

When building UX systems:

1. **Identify your layer**: Structure, Navigation, or Interaction
2. **Load relevant schemas**: You don't need all 3 - just what you use
3. **Use ID references**: Reference concepts by ID (e.g., `page_product_detail`)
4. **Ground in DDD**: Pages reference bounded contexts, workflows reference aggregates
5. **Validate cross-references**: Use pattern validation for well-formed IDs

## Design Principles

### Information Architecture (Structure Layer)
- **Hierarchical organization**: Clear parent-child relationships
- **Faceted classification**: Multi-dimensional filtering
- **Controlled vocabularies**: Consistent terminology from DDD
- **Search optimization**: Indexed fields aligned with user mental models

### Navigation (Wayfinding Layer)
- **Predictable structure**: Navigation follows IA hierarchy
- **Context awareness**: Breadcrumbs show current location
- **Domain alignment**: Nav sections match bounded contexts
- **Responsive patterns**: Mobile vs desktop navigation

### Interaction (Action Layer)
- **Atomic design**: Build complex from simple components
- **Workflow integrity**: Respect aggregate boundaries
- **Accessibility first**: WCAG 2.1 Level AA compliance
- **Design system**: Consistent tokens (colors, spacing, typography)

## Migration Guide

See [MIGRATION.md](MIGRATION.md) for guidance on migrating from the original monolithic schema to the partitioned schemas.

## Statistics

- **Original schema**: 1,141 lines, ~12 concepts
- **Partitioned schemas**: 1,164 lines (3 files), ~17 concepts
- **Partition overhead**: +2% (minimal due to shared metadata)
- **Average partition size**: 388 lines
- **Largest partition**: interaction (602 lines)
- **Smallest partition**: structure (200 lines)

## Key Patterns

### Information Architecture Patterns
- Hierarchical IA (categories, subcategories)
- Faceted navigation (multi-dimensional filtering)
- Tag-based organization
- Search-driven discovery

### Navigation Patterns
- Global navigation (top nav, sidebar)
- Local navigation (contextual links, tabs)
- Breadcrumb trails
- Mega menus
- Mobile navigation (bottom tabs, hamburger, drawer)

### Interaction Patterns
- Multi-step workflows (linear, flexible, conditional)
- Form patterns (validation, progressive disclosure)
- Component behaviors (hover, click, swipe)
- Micro-interactions (animations, transitions)
- Accessibility patterns (keyboard nav, screen readers)

## References

- **Information Architecture**: Rosenfeld & Morville - Information Architecture (4th ed, 2015)
- **Interaction Design**: Dan Saffer - Microinteractions (2013)
- **Atomic Design**: Brad Frost - Atomic Design (2016)
- **Navigation**: Steve Krug - Don't Make Me Think (3rd ed, 2014)
- **Accessibility**: WCAG 2.1 - Web Content Accessibility Guidelines
- **DDD Integration**: Evans - Domain-Driven Design (2003)

## Changelog

### Version 2.0.0 (2025-10-17)
- Partitioned schema into 3 focused schemas by architectural layer
- Created 3 new partitioned examples (e-commerce product catalog)
- Updated interdomain-map.yaml with partition groundings
- All UX → DDD groundings reference specific partitions
- Achieved 100% closure (up from 96%)

### Version 1.0.0 (2025-10-13)
- Initial monolithic schema
- Core concepts: IA, Navigation, Workflow, Page, Component
- Original example: ux-schema-example.yaml
