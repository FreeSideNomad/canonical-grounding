# Canonical Domain Model Glossary

**Total Concepts:** 117
**Domains:** 5

## Concepts by Domain

- **Agile**: 35 concepts
- **DDD**: 13 concepts
- **Data-Eng**: 26 concepts
- **QE**: 27 concepts
- **UX**: 18 concepts

---

## Agile Domain

### agile_release_train

**Domain:** Agile

**Description:** Long-lived team of agile teams (50-125 people)

**Required Fields:** id, name, teams

**Total Properties:** 10

**Key Properties:**

- `id` (string) *(required)*
- `name` (string) *(required)*
- `mission` (string) 
  - ART mission statement
- `valueStream` (string) 
  - Value stream this ART supports
- `teams` (array) *(required)*
  - teams in this ART

---

### architectural_runway

**Domain:** Agile

**Description:** Technical foundation enabling future business functionality

**Required Fields:** runwayId, description, enablers

**Total Properties:** 5

**Key Properties:**

- `runwayId` (string) *(required)*
  - Unique identifier for the runway
- `description` (string) *(required)*
  - Description of architectural runway
- `enablers` (array) *(required)*
  - enabler work items that build runway
- `technicalDebtRefs` (array) 
  - Technical debt items addressed by this runway
- `runwayScore` (number) 
  - Assessment of runway adequacy (0-10)

---

### cadence

**Domain:** Agile

**Description:** Regular rhythm or heartbeat for team activities

**Required Fields:** cadenceId, name, frequency

**Total Properties:** 5

**Key Properties:**

- `cadenceId` (string) *(required)*
  - Unique identifier for the cadence
- `name` (string) *(required)*
  - Name of the cadence (e.g., 'sprint cadence', 'PI cadence')
- `frequency` (string) *(required)*
  - How often activities occur
- `duration` (string) 
  - Duration of each cycle (e.g., '2 weeks', '10 weeks')
- `purpose` (string) 
  - Purpose of this cadence

---

### ceremony

**Domain:** Agile

**Description:** Agile ceremony or event

**Required Fields:** ceremonyId, type, cadence

**Total Properties:** 5

**Key Properties:**

- `ceremonyId` (string) *(required)*
  - Unique identifier for the ceremony
- `type` (string) *(required)*
  - Type of ceremony
- `cadence` (string) *(required)*
  - How often ceremony occurs (e.g., 'daily', 'per sprint', 'per PI')
- `durationMinutes` (integer) 
  - Typical duration in minutes
- `participants` (array) 
  - Participants in this ceremony

---

### definition_of_ready

**Domain:** Agile

**Description:** Criteria that work items must meet before being pulled into sprint

**Required Fields:** dorId, criteria, teamRef

**Total Properties:** 4

**Key Properties:**

- `dorId` (string) *(required)*
  - Unique identifier for the DoR
- `criteria` (array) *(required)*
  - Readiness criteria
- `teamRef` (string) *(required)*
  - team that owns this DoR
- `lastUpdated` (string) 
  - When DoR was last updated

---

### enabler

**Domain:** Agile

**Description:** Work item that extends architectural runway

**Required Fields:** enablerId, type, description

**Total Properties:** 5

**Key Properties:**

- `enablerId` (string) *(required)*
  - Unique identifier for the enabler
- `type` (string) *(required)*
  - Type of enabler work
- `description` (string) *(required)*
  - Description of what the enabler provides
- `relatedFeatures` (array) 
  - features that depend on this enabler
- `boundedContextRef` (string) 
  - DDD bounded context this enabler supports

---

### epic

**Domain:** Agile

**Description:** Large body of work spanning multiple features

**Required Fields:** id, title, type

**Total Properties:** 13

**Key Properties:**

- `id` (string) *(required)*
- `title` (string) *(required)*
- `type` (string) *(required)*
  - Business epic delivers value, enabler extends runway
- `description` (string) 
- `hypothesis` (string) 
  - epic hypothesis statement

---

### estimation_technique

**Domain:** Agile

**Description:** Technique for estimating work items

**Required Fields:** techniqueId, name, description

**Total Properties:** 4

**Key Properties:**

- `techniqueId` (string) *(required)*
  - Unique identifier for the technique
- `name` (string) *(required)*
  - Name of estimation technique
- `description` (string) *(required)*
  - Description of how technique works
- `whenToUse` (string) 
  - Guidance on when to use this technique

---

### feature

**Domain:** Agile

**Description:** Service provided by the system, sized for a Program increment

**Required Fields:** id, title, type, bounded_context_ref

**Total Properties:** 17

**Key Properties:**

- `bounded_context_ref` (string) *(required)*
  - DDD bounded context this feature belongs to (required - explicit grounding)
- `id` (string) *(required)*
- `title` (string) *(required)*
- `type` (string) *(required)*
- `description` (string) 

---

### feedback_loop

**Domain:** Agile

**Description:** Mechanism for gathering and acting on feedback

**Required Fields:** loopId, type, cadence

**Total Properties:** 5

**Key Properties:**

- `loopId` (string) *(required)*
  - Unique identifier for the feedback loop
- `type` (string) *(required)*
  - Scope of feedback loop
- `cadence` (string) *(required)*
  - How often feedback is collected (e.g., 'per sprint', 'quarterly')
- `participants` (array) 
  - Who participates in this feedback loop
- `metricsReviewed` (array) 
  - metrics reviewed in this feedback loop

---

### impediment

**Domain:** Agile

**Description:** Blocker or obstacle preventing progress

**Required Fields:** impedimentId, description, severity, status

**Total Properties:** 7

**Key Properties:**

- `impedimentId` (string) *(required)*
  - Unique identifier for the impediment
- `description` (string) *(required)*
  - Description of the impediment
- `severity` (string) *(required)*
  - Impact severity
- `teamRef` (string) 
  - team affected by this impediment
- `resolutionPlan` (string) 
  - Plan for resolving the impediment

---

### increment

**Domain:** Agile

**Description:** Potentially shippable product increment from a sprint

**Required Fields:** incrementId, sprintRef, deliverables, acceptanceStatus

**Total Properties:** 5

**Key Properties:**

- `incrementId` (string) *(required)*
  - Unique identifier for the increment
- `sprintRef` (string) *(required)*
  - sprint that produced this increment
- `deliverables` (array) *(required)*
  - What was delivered in this increment
- `acceptanceStatus` (string) *(required)*
  - Whether increment was accepted
- `demoDate` (string) 
  - When increment was demonstrated

---

### iteration

**Domain:** Agile

**Description:** Time-boxed iteration in SAFe (typically 2 weeks)

**Required Fields:** id, name, startDate, endDate, piId

**Total Properties:** 11

**Key Properties:**

- `id` (string) *(required)*
- `name` (string) *(required)*
- `number` (integer) 
  - iteration number within PI
- `startDate` (string) *(required)*
- `endDate` (string) *(required)*

---

### metadata

**Domain:** Agile

**Description:** No description available

**Total Properties:** 6

**Key Properties:**

- `created` (string) 
- `updated` (string) 
- `createdBy` (string) 
- `updatedBy` (string) 
- `tags` (array) 

---

### metric

**Domain:** Agile

**Description:** No description available

**Required Fields:** name

**Total Properties:** 5

**Key Properties:**

- `name` (string) *(required)*
- `description` (string) 
- `target` (number) 
- `current` (number) 
- `unit` (string) 

---

### non_functional_requirement

**Domain:** Agile

**Description:** Quality attributes and constraints for system behavior (NFR)

**Required Fields:** nfrId, category, description, acceptanceCriteria

**Total Properties:** 6

**Key Properties:**

- `nfrId` (string) *(required)*
  - Unique identifier for the NFR
- `category` (string) *(required)*
  - NFR category
- `description` (string) *(required)*
  - Description of the non-functional requirement
- `acceptanceCriteria` (array) *(required)*
  - Testable criteria for meeting this NFR
- `relatedFeatures` (array) 
  - features that must satisfy this NFR

---

### portfolio

**Domain:** Agile

**Description:** No description available

**Total Properties:** 4

**Key Properties:**

- `id` (string) 
- `name` (string) 
- `strategicThemes` (array) 
- `budgets` (array) 

---

### product

**Domain:** Agile

**Description:** The primary organizational unit representing the solution being developed

**Required Fields:** id, name, vision

**Total Properties:** 12

**Key Properties:**

- `id` (string) *(required)*
  - Unique identifier for the product
- `name` (string) *(required)*
  - product name
- `description` (string) 
  - Brief product description
- `vision` (unknown) *(required)*
- `roadmap` (unknown) 

---

### program_increment

**Domain:** Agile

**Description:** Time-boxed planning increment in SAFe (8-12 weeks)

**Required Fields:** id, name, startDate, endDate, artId

**Total Properties:** 14

**Key Properties:**

- `id` (string) *(required)*
- `name` (string) *(required)*
- `number` (integer) 
- `startDate` (string) *(required)*
- `endDate` (string) *(required)*

---

### release

**Domain:** Agile

**Description:** Time-boxed delivery of value spanning one or more Program increments

**Required Fields:** id, name, vision, startDate, endDate

**Total Properties:** 18

**Key Properties:**

- `id` (string) *(required)*
- `name` (string) *(required)*
  - release name (e.g., 'Spring 2025 release', 'Version 2.0')
- `version` (string) 
  - Semantic version number
- `vision` (unknown) *(required)*
- `startDate` (string) *(required)*

---

### release_vision

**Domain:** Agile

**Description:** Focused vision for a specific release, derived from product vision

**Required Fields:** releaseGoal, targetCustomers, keyCapabilities

**Total Properties:** 13

**Key Properties:**

- `releaseGoal` (string) *(required)*
  - Clear statement of what this release aims to achieve
- `targetCustomers` (array) *(required)*
  - Customer segments targeted by this release
- `keyCapabilities` (array) *(required)*
  - Top 3-5 capabilities being delivered in this release
- `customerValue` (string) 
  - Clear articulation of value to customers
- `businessValue` (string) 
  - Business value expected from this release

---

### risk

**Domain:** Agile

**Description:** No description available

**Required Fields:** id, description, roam

**Total Properties:** 7

**Key Properties:**

- `id` (string) *(required)*
- `description` (string) *(required)*
- `impact` (string) 
- `probability` (string) 
- `roam` (string) *(required)*
  - ROAM classification

---

### roadmap

**Domain:** Agile

**Description:** Strategic view of deliverables over time

**Required Fields:** timeHorizon, level, items

**Total Properties:** 6

**Key Properties:**

- `level` (string) *(required)*
  - Level of roadmap (portfolio, product, release, or PI)
- `timeHorizon` (string) *(required)*
  - roadmap time horizon (e.g., '12 months', '4 PIs', '3 releases')
- `items` (array) *(required)*
  - roadmap items organized by timeframe
- `lastReviewed` (string) 
  - When roadmap was last reviewed/updated
- `reviewCadence` (string) 
  - How often roadmap is reviewed (e.g., 'quarterly', 'per PI')

---

### role

**Domain:** Agile

**Description:** Agile role with defined responsibilities

**Required Fields:** roleId, type, responsibilities

**Total Properties:** 4

**Key Properties:**

- `roleId` (string) *(required)*
  - Unique identifier for the role
- `type` (string) *(required)*
  - role type
- `responsibilities` (array) *(required)*
  - Key responsibilities of this role
- `authorityLevel` (string) 
  - Level at which this role operates

---

### sprint

**Domain:** Agile

**Description:** Time-boxed iteration in Scrum (1-4 weeks)

**Required Fields:** id, name, startDate, endDate, goal

**Total Properties:** 18

**Key Properties:**

- `id` (string) *(required)*
- `name` (string) *(required)*
- `startDate` (string) *(required)*
- `endDate` (string) *(required)*
- `goal` (string) *(required)*
  - sprint Goal - objective for this sprint

---

### stakeholder

**Domain:** Agile

**Description:** No description available

**Required Fields:** id, name, role

**Total Properties:** 5

**Key Properties:**

- `id` (string) *(required)*
- `name` (string) *(required)*
- `role` (string) *(required)*
- `influence` (string) 
- `interest` (string) 

---

### task

**Domain:** Agile

**Description:** Technical task for implementing a story

**Required Fields:** id, description

**Total Properties:** 6

**Key Properties:**

- `id` (string) *(required)*
- `description` (string) *(required)*
- `estimateHours` (number) 
- `remainingHours` (number) 
- `status` (string) 

---

### team

**Domain:** Agile

**Description:** Agile team (5-11 people)

**Required Fields:** id, name, members

**Total Properties:** 17

**Key Properties:**

- `id` (string) *(required)*
- `name` (string) *(required)*
- `type` (string) 
  - team methodology
- `members` (array) *(required)*
  - team members
- `roles` (object) 

---

### team_member

**Domain:** Agile

**Description:** No description available

**Required Fields:** id, name

**Total Properties:** 6

**Key Properties:**

- `id` (string) *(required)*
- `name` (string) *(required)*
- `email` (string) 
- `role` (string) 
  - Primary role
- `skills` (array) 
  - Skills this person has

---

### team_topology

**Domain:** Agile

**Description:** Team type and interaction patterns (Team Topologies model)

**Required Fields:** topologyId, type, responsibilities

**Total Properties:** 4

**Key Properties:**

- `topologyId` (string) *(required)*
  - Unique identifier for the topology
- `type` (string) *(required)*
  - team topology type
- `responsibilities` (array) *(required)*
  - Key responsibilities of this team type
- `interactionModes` (array) 
  - How this team interacts with others (collaboration, X-as-a-Service, facilitating)

---

### technical_debt

**Domain:** Agile

**Description:** Technical debt requiring remediation

**Required Fields:** debtId, description, impact, priority

**Total Properties:** 8

**Key Properties:**

- `debtId` (string) *(required)*
  - Unique identifier for the debt
- `description` (string) *(required)*
  - Description of the technical debt
- `impact` (string) *(required)*
  - Impact on system quality
- `priority` (integer) *(required)*
  - Priority for addressing debt (1=highest)
- `boundedContextRef` (string) 
  - DDD bounded context containing this debt

---

### user_story

**Domain:** Agile

**Description:** Small, vertical slice of functionality

**Required Fields:** id, title, asA, iWant, soThat

**Total Properties:** 19

**Key Properties:**

- `ux_artifact_refs` (object) 
  - UX artifacts implementing this story (explicit grounding)
- `id` (string) *(required)*
- `title` (string) *(required)*
- `asA` (string) *(required)*
  - User role (As a...)
- `iWant` (string) *(required)*
  - Goal (I want...)

---

### value_stream

**Domain:** Agile

**Description:** No description available

**Required Fields:** id, name

**Total Properties:** 4

**Key Properties:**

- `id` (string) *(required)*
- `name` (string) *(required)*
- `type` (string) 
- `steps` (array) 
  - Steps in the value stream

---

### vision

**Domain:** Agile

**Description:** Comprehensive product vision following SAFe best practices

**Required Fields:** futureStateDescription, customerNeeds

**Total Properties:** 8

**Key Properties:**

- `futureStateDescription` (string) *(required)*
  - Clear description of the intended future state
- `customerNeeds` (object) *(required)*
  - Target customers and problems being solved
- `solutionIntent` (object) 
  - Proposed solution approach
- `boundaries` (object) 
  - Context and boundaries of the product
- `strategicAlignment` (object) 
  - Connection to business objectives

---

### working_agreement

**Domain:** Agile

**Description:** team norms and practices

**Required Fields:** agreementId, teamRef, norms

**Total Properties:** 6

**Key Properties:**

- `agreementId` (string) *(required)*
  - Unique identifier for the working agreement
- `teamRef` (string) *(required)*
  - team that owns this agreement
- `norms` (array) *(required)*
  - team norms and behavioral agreements
- `practices` (array) 
  - Engineering and collaboration practices
- `createdDate` (string) 
  - When agreement was created

---

## DDD Domain

### aggregate

**Domain:** DDD

**Description:** Cluster of entities and value objects with defined consistency boundary

**Required Fields:** id, name, bounded_context_ref, root_ref

**Total Properties:** 10

**Key Properties:**

- `id` (string) *(required)*
  - Unique aggregate identifier
- `name` (string) *(required)*
  - Aggregate name from ubiquitous language
- `bounded_context_ref` (reference) *(required)*
  - Bounded context this aggregate belongs to
- `root_ref` (reference) *(required)*
  - The aggregate root entity
- `entities` (array) 
  - Entities within this aggregate (including root)

---

### application_service

**Domain:** DDD

**Description:** Orchestrates use cases, transaction boundaries

**Required Fields:** id, name, bounded_context_ref

**Total Properties:** 8

**Key Properties:**

- `id` (string) *(required)*
  - Unique application service identifier
- `name` (string) *(required)*
  - Service name representing use case
- `bounded_context_ref` (reference) *(required)*
  - Context this service belongs to
- `use_case` (string) 
  - Business use case this service implements
- `orchestrates` (array) 
  - What this service orchestrates

---

### bounded_context

**Domain:** DDD

**Description:** Explicit boundary within which a domain model is defined and applicable

**Required Fields:** id, name, domain_ref

**Total Properties:** 12

**Key Properties:**

- `id` (string) *(required)*
  - Unique bounded context identifier
- `name` (string) *(required)*
  - Context name from ubiquitous language
- `domain_ref` (reference) *(required)*
  - Parent domain
- `description` (string) 
  - Purpose and scope of this context
- `ubiquitous_language` (object) 
  - Key terms and definitions specific to this context

---

### context_mapping

**Domain:** DDD

**Description:** Relationship between two bounded contexts

**Required Fields:** id, upstream_context, downstream_context, relationship_type

**Total Properties:** 9

**Key Properties:**

- `id` (string) *(required)*
  - Unique mapping identifier
- `upstream_context` (reference) *(required)*
  - Context that influences
- `downstream_context` (reference) *(required)*
  - Context that is influenced
- `relationship_type` (enum) *(required)*
  - Type of relationship between contexts
- `integration_pattern` (string) 
  - How integration is implemented (REST API, messaging, shared DB, etc.)

---

### domain_event

**Domain:** DDD

**Description:** Something that happened in the domain

**Required Fields:** id, name, aggregate_ref

**Total Properties:** 9

**Key Properties:**

- `id` (string) *(required)*
  - Unique event identifier
- `name` (string) *(required)*
  - Event name in past tense (e.g., OrderPlaced)
- `bounded_context_ref` (reference) 
  - Context this event belongs to
- `aggregate_ref` (reference) *(required)*
  - Aggregate that publishes this event
- `description` (string) 
  - What happened and why it matters

---

### domain_service

**Domain:** DDD

**Description:** Stateless operation that doesn't belong to an entity

**Required Fields:** id, name, bounded_context_ref

**Total Properties:** 7

**Key Properties:**

- `id` (string) *(required)*
  - Unique domain service identifier
- `name` (string) *(required)*
  - Service name from ubiquitous language
- `bounded_context_ref` (reference) *(required)*
  - Context this service belongs to
- `description` (string) 
  - What this service does and why it exists
- `operations` (array) 
  - Service operations

---

### entity

**Domain:** DDD

**Description:** Object with unique identity and lifecycle

**Required Fields:** id, name, bounded_context_ref, identity_field

**Total Properties:** 11

**Key Properties:**

- `id` (string) *(required)*
  - Unique entity definition identifier
- `name` (string) *(required)*
  - Entity name from ubiquitous language
- `bounded_context_ref` (reference) *(required)*
  - Context this entity belongs to
- `aggregate_ref` (reference) 
  - Aggregate this entity belongs to
- `is_aggregate_root` (boolean) 
  - True if this entity is an aggregate root

---

### factory

**Domain:** DDD

**Description:** Encapsulates complex object creation

**Required Fields:** id, name, creates_type

**Total Properties:** 8

**Key Properties:**

- `id` (string) *(required)*
  - Unique factory identifier
- `name` (string) *(required)*
  - Factory name
- `bounded_context_ref` (reference) 
  - Context this factory belongs to
- `creates_type` (enum) *(required)*
  - What kind of object this creates
- `creates_ref` (reference) 
  - Reference to what it creates

---

### repository

**Domain:** DDD

**Description:** Persistence abstraction for aggregates

**Required Fields:** id, name, aggregate_ref

**Total Properties:** 7

**Key Properties:**

- `id` (string) *(required)*
  - Unique repository identifier
- `name` (string) *(required)*
  - Repository name (e.g., CustomerRepository)
- `bounded_context_ref` (reference) 
  - Context this repository belongs to
- `aggregate_ref` (reference) *(required)*
  - Aggregate this repository manages
- `interface_methods` (array) 
  - Repository interface methods

---

### specification

**Domain:** DDD

**Description:** Encapsulates business rule or query criteria

**Required Fields:** id, name, bounded_context_ref

**Total Properties:** 7

**Key Properties:**

- `id` (string) *(required)*
  - Unique specification identifier
- `name` (string) *(required)*
  - Specification name
- `bounded_context_ref` (reference) *(required)*
  - Context this specification belongs to
- `applies_to` (reference) 
  - Entity or VO this specification applies to
- `rule` (string) 
  - Business rule being checked

---

### value_object

**Domain:** DDD

**Description:** Immutable object defined by its attributes

**Required Fields:** id, name, bounded_context_ref

**Total Properties:** 10

**Key Properties:**

- `id` (string) *(required)*
  - Unique value object definition identifier
- `name` (string) *(required)*
  - Value object name from ubiquitous language
- `bounded_context_ref` (reference) *(required)*
  - Context this value object belongs to
- `description` (string) 
  - What this value object represents
- `attributes` (array) 
  - Value object attributes

---

## Data-Eng Domain

### check

**Domain:** Data-Eng

**Description:** No description available

**Required Fields:** id, name, type, dataset

**Total Properties:** 9

**Key Properties:**

- `id` (string) *(required)*
- `name` (string) *(required)*
- `type` (string) *(required)*
- `dataset` (string) *(required)*
- `validation_rule_type_ref` (string) 
  - Reference to data_validation_rule_type ID

---

### contract

**Domain:** Data-Eng

**Description:** No description available

**Required Fields:** id, name, dataset, version

**Total Properties:** 9

**Key Properties:**

- `id` (string) *(required)*
- `name` (string) *(required)*
- `dataset` (string) *(required)*
- `version` (string) *(required)*
  - Semantic version (MAJOR.MINOR.PATCH)
- `schema` (object) 

---

### data_access_pattern

**Domain:** Data-Eng

**Description:** No description available

**Required Fields:** id, type

**Total Properties:** 4

**Key Properties:**

- `id` (string) *(required)*
- `type` (string) *(required)*
- `characteristics` (string) 
- `optimization_hints` (array) 

---

### data_catalog_entry

**Domain:** Data-Eng

**Description:** No description available

**Required Fields:** id, dataset_ref

**Total Properties:** 6

**Key Properties:**

- `id` (string) *(required)*
- `dataset_ref` (string) *(required)*
  - Reference to dataset ID
- `tags` (array) 
- `documentation` (string) 
- `last_updated` (string) 

---

### data_contract

**Domain:** Data-Eng

**Description:** No description available

**Required Fields:** id, provider, consumer, version, status

**Total Properties:** 7

**Key Properties:**

- `id` (string) *(required)*
- `provider` (string) *(required)*
- `consumer` (string) *(required)*
- `schema_ref` (string) 
  - Reference to schema definition
- `sla` (object) 

---

### data_monitoring_metric

**Domain:** Data-Eng

**Description:** No description available

**Required Fields:** id, name, type

**Total Properties:** 5

**Key Properties:**

- `id` (string) *(required)*
- `name` (string) *(required)*
- `type` (string) *(required)*
- `threshold` (number) 
- `alert_config` (object) 

---

### data_partition_strategy

**Domain:** Data-Eng

**Description:** No description available

**Required Fields:** id, type, partition_key

**Total Properties:** 4

**Key Properties:**

- `id` (string) *(required)*
- `type` (string) *(required)*
- `partition_key` (string) *(required)*
- `partition_size` (string) 

---

### data_pipeline_template

**Domain:** Data-Eng

**Description:** No description available

**Required Fields:** id, name, stages

**Total Properties:** 5

**Key Properties:**

- `id` (string) *(required)*
- `name` (string) *(required)*
- `description` (string) 
- `stages` (array) *(required)*
- `parameters` (object) 
  - Template parameters (flexible)

---

### data_product

**Domain:** Data-Eng

**Description:** No description available

**Required Fields:** id, name, owner, datasets

**Total Properties:** 8

**Key Properties:**

- `id` (string) *(required)*
- `name` (string) *(required)*
- `description` (string) 
- `owner` (unknown) *(required)*
- `datasets` (array) *(required)*
  - References to dataset IDs

---

### data_quality_dimension

**Domain:** Data-Eng

**Description:** No description available

**Required Fields:** id, name

**Total Properties:** 4

**Key Properties:**

- `id` (string) *(required)*
- `name` (string) *(required)*
- `description` (string) 
- `measurement_method` (string) 

---

### data_replication_config

**Domain:** Data-Eng

**Description:** No description available

**Required Fields:** id, replication_factor, replication_type

**Total Properties:** 4

**Key Properties:**

- `id` (string) *(required)*
- `replication_factor` (number) *(required)*
- `replication_type` (string) *(required)*
- `target_regions` (array) 

---

### data_retention_tier

**Domain:** Data-Eng

**Description:** No description available

**Required Fields:** id, name, retention_days

**Total Properties:** 4

**Key Properties:**

- `id` (string) *(required)*
- `name` (string) *(required)*
- `retention_days` (number) *(required)*
- `storage_class` (string) 

---

### data_transformation_function

**Domain:** Data-Eng

**Description:** No description available

**Required Fields:** id, name, input_schema, output_schema

**Total Properties:** 5

**Key Properties:**

- `id` (string) *(required)*
- `name` (string) *(required)*
- `input_schema` (object) *(required)*
  - Input schema definition
- `output_schema` (object) *(required)*
  - Output schema definition
- `logic_description` (string) 

---

### data_validation_rule_type

**Domain:** Data-Eng

**Description:** No description available

**Required Fields:** id, category

**Total Properties:** 3

**Key Properties:**

- `id` (string) *(required)*
- `category` (string) *(required)*
- `description` (string) 

---

### dataset

**Domain:** Data-Eng

**Description:** No description available

**Required Fields:** id, name, type, format

**Total Properties:** 16

**Key Properties:**

- `id` (string) *(required)*
- `name` (string) *(required)*
- `description` (string) 
- `type` (string) *(required)*
- `format` (string) *(required)*

---

### domain

**Domain:** Data-Eng

**Description:** No description available

**Required Fields:** id, name, pipelines

**Total Properties:** 5

**Key Properties:**

- `id` (string) *(required)*
- `name` (string) *(required)*
- `description` (string) 
- `owners` (array) 
- `pipelines` (array) *(required)*
  - References to pipeline IDs

---

### field

**Domain:** Data-Eng

**Description:** No description available

**Required Fields:** name, type

**Total Properties:** 5

**Key Properties:**

- `name` (string) *(required)*
- `type` (string) *(required)*
- `nullable` (boolean) 
- `description` (string) 
- `pii` (boolean) 

---

### governance

**Domain:** Data-Eng

**Description:** No description available

**Total Properties:** 3

**Key Properties:**

- `retention` (array) 
- `access` (array) 
- `pii_handling` (array) 

---

### lineage

**Domain:** Data-Eng

**Description:** No description available

**Required Fields:** id, upstream, downstream

**Total Properties:** 5

**Key Properties:**

- `id` (string) *(required)*
- `upstream` (string) *(required)*
- `downstream` (string) *(required)*
- `transform` (string) 
- `relationship` (string) 

---

### observability

**Domain:** Data-Eng

**Description:** No description available

**Total Properties:** 3

**Key Properties:**

- `metrics` (array) 
- `slos` (array) 
- `alerts` (array) 

---

### owner

**Domain:** Data-Eng

**Description:** No description available

**Required Fields:** team

**Total Properties:** 2

**Key Properties:**

- `team` (string) *(required)*
- `contact` (string) 

---

### pipeline

**Domain:** Data-Eng

**Description:** No description available

**Required Fields:** id, name, mode, stages

**Total Properties:** 9

**Key Properties:**

- `id` (string) *(required)*
- `name` (string) *(required)*
- `description` (string) 
- `mode` (string) *(required)*
- `schedule` (unknown) 

---

### schedule

**Domain:** Data-Eng

**Description:** No description available

**Required Fields:** id, type

**Total Properties:** 5

**Key Properties:**

- `id` (string) *(required)*
- `type` (string) *(required)*
- `cron_expression` (string) 
  - Standard cron expression (if type=cron)
- `interval_minutes` (number) 
  - Interval in minutes (if type=interval)
- `triggers` (array) 

---

### stage

**Domain:** Data-Eng

**Description:** No description available

**Required Fields:** id, name

**Total Properties:** 8

**Key Properties:**

- `id` (string) *(required)*
- `name` (string) *(required)*
- `description` (string) 
- `uses_patterns` (array) 
  - References to pattern UIDs from taxonomy
- `inputs` (array) 
  - Dataset IDs consumed by this stage

---

### system

**Domain:** Data-Eng

**Description:** No description available

**Required Fields:** id, name, domains

**Total Properties:** 7

**Key Properties:**

- `id` (string) *(required)*
  - Unique system identifier (format: sys-{kebab-name})
- `name` (string) *(required)*
- `description` (string) 
- `owners` (array) 
- `domains` (array) *(required)*
  - References to domain IDs

---

### transform

**Domain:** Data-Eng

**Description:** No description available

**Required Fields:** id, type

**Total Properties:** 5

**Key Properties:**

- `id` (string) *(required)*
- `type` (string) *(required)*
- `function_ref` (string) 
  - Reference to data_transformation_function ID
- `description` (string) 
- `config` (object) 
  - Transform-specific configuration (flexible)

---

## QE Domain

### contract_test

**Domain:** QE

**Description:** string

**Total Properties:** 0

---

### coverage_target

**Domain:** QE

**Description:** No description available

**Total Properties:** 0

---

### defect

**Domain:** QE

**Description:** string

**Total Properties:** 0

---

### incident_report

**Domain:** QE

**Description:** string

**Total Properties:** 0

---

### quality_characteristics

**Domain:** QE

**Description:** Can add domain-specific quality metrics

**Total Properties:** 0

---

### test_assertion

**Domain:** QE

**Description:** No description available

**Total Properties:** 0

---

### test_automation

**Domain:** QE

**Description:** No description available

**Total Properties:** 0

---

### test_case

**Domain:** QE

**Description:** string

**Total Properties:** 0

---

### test_configuration

**Domain:** QE

**Description:** No description available

**Total Properties:** 0

---

### test_coverage_type

**Domain:** QE

**Description:** No description available

**Total Properties:** 0

---

### test_data

**Domain:** QE

**Description:** string

**Total Properties:** 0

---

### test_double

**Domain:** QE

**Description:** No description available

**Total Properties:** 0

---

### test_environment

**Domain:** QE

**Description:** No description available

**Total Properties:** 0

---

### test_execution_order

**Domain:** QE

**Description:** No description available

**Total Properties:** 0

---

### test_execution_plan

**Domain:** QE

**Description:** string

**Total Properties:** 0

---

### test_fixture

**Domain:** QE

**Description:** No description available

**Total Properties:** 0

---

### test_harness

**Domain:** QE

**Description:** No description available

**Total Properties:** 0

---

### test_metrics

**Domain:** QE

**Description:** No description available

**Total Properties:** 0

---

### test_oracle

**Domain:** QE

**Description:** No description available

**Total Properties:** 0

---

### test_priority_scheme

**Domain:** QE

**Description:** No description available

**Total Properties:** 0

---

### test_scenario

**Domain:** QE

**Description:** No description available

**Total Properties:** 0

---

### test_script

**Domain:** QE

**Description:** No description available

**Total Properties:** 0

---

### test_stakeholder_role

**Domain:** QE

**Description:** No description available

**Total Properties:** 0

---

### test_strategy

**Domain:** QE

**Description:** string

**Total Properties:** 0

---

### test_suite

**Domain:** QE

**Description:** string

**Total Properties:** 0

---

### test_tool

**Domain:** QE

**Description:** No description available

**Total Properties:** 0

---

### testing_technique_spec

**Domain:** QE

**Description:** No description available

**Total Properties:** 0

---

## UX Domain

### accessibility_spec

**Domain:** UX

**Description:** Accessibility specifications

**Total Properties:** 6

**Key Properties:**

- `wcag_level` (string) 
  - Target WCAG conformance level
- `aria` (object) 
  - ARIA attributes and patterns
- `keyboard` (object) 
  - Keyboard navigation support
- `screen_reader` (object) 
  - Screen reader support
- `color_contrast` (object) 
  - Color contrast requirements

---

### animation

**Domain:** UX

**Description:** Animation specification

**Total Properties:** 4

**Key Properties:**

- `type` (string) 
- `duration` (integer) 
  - Milliseconds
- `easing` (string) 
- `trigger` (string) 

---

### behavior

**Domain:** UX

**Description:** Interactive behavior specification

**Required Fields:** behavior_id, type

**Total Properties:** 11

**Key Properties:**

- `behavior_id` (string) *(required)*
- `type` (string) *(required)*
- `trigger` (string) 
  - What triggers this behavior
- `trigger_source` (string) 
  - Specific trigger (e.g., event name for domain_event)
- `action` (string) 
  - What action occurs

---

### caching_config

**Domain:** UX

**Description:** Client-side caching strategy

**Total Properties:** 3

**Key Properties:**

- `strategy` (string) 
- `ttl` (integer) 
  - Time to live (seconds)
- `invalidation` (object) 

---

### component

**Domain:** UX

**Description:** Reusable UI component

**Required Fields:** component_id, name, atomic_level

**Total Properties:** 12

**Key Properties:**

- `component_id` (string) *(required)*
- `name` (string) *(required)*
  - Component name
- `atomic_level` (string) *(required)*
  - Atomic design classification
- `category` (string) 
- `description` (string) 

---

### design_tokens

**Domain:** UX

**Description:** Design system tokens

**Total Properties:** 4

**Key Properties:**

- `colors` (object) 
  - Color palette
- `typography` (object) 
  - Typography scale
- `spacing` (object) 
  - Spacing scale
- `breakpoints` (object) 
  - Responsive breakpoints

---

### facet

**Domain:** UX

**Description:** Faceted classification dimension for filtering and navigation

**Required Fields:** facet_id, label, type

**Total Properties:** 6

**Key Properties:**

- `facet_id` (string) *(required)*
- `label` (string) *(required)*
  - Display label
- `type` (string) *(required)*
- `ddd_mapping` (string) 
  - Maps to DDD value object or property
- `values` (array) 
  - Available facet values (for select types)

---

### facet_value

**Domain:** UX

**Description:** Value within a faceted classification dimension

**Total Properties:** 3

**Key Properties:**

- `value` (string) 
- `label` (string) 
- `count` (integer) 
  - Number of items with this value (dynamic)

---

### hierarchy_node

**Domain:** UX

**Description:** Node in a hierarchical information architecture

**Total Properties:** 5

**Key Properties:**

- `id` (string) 
- `label` (string) 
  - Display label (use ubiquitous language)
- `bounded_context` (string) 
  - Associated DDD bounded context
- `url` (string) 
  - URL path
- `children` (array) 
  - Child node IDs

---

### information_architecture

**Domain:** UX

**Description:** Defines how information is organized, labeled, and accessed

**Required Fields:** organization_scheme, navigation_systems

**Total Properties:** 6

**Key Properties:**

- `organization_scheme` (string) *(required)*
  - Primary organization pattern
- `hierarchy` (object) 
  - Hierarchical structure (if applicable)
- `facets` (array) 
  - Faceted classification dimensions
- `navigation_systems` (object) *(required)*
  - Types of navigation available
- `search_system` (unknown) 

---

### navigation

**Domain:** UX

**Description:** Navigation structures and patterns

**Required Fields:** global_navigation

**Total Properties:** 5

**Key Properties:**

- `global_navigation` (object) *(required)*
  - Primary navigation across entire system
- `local_navigation` (array) 
  - Context-specific navigation sections
- `utility_navigation` (object) 
  - Utility functions (user menu, settings, help)
- `mobile_navigation` (object) 
  - Mobile-specific navigation patterns
- `cross_context_navigation` (array) 
  - Navigation between bounded contexts

---

### page

**Domain:** UX

**Description:** Individual page definition

**Required Fields:** page_id, name, type, url

**Total Properties:** 11

**Key Properties:**

- `page_id` (string) *(required)*
- `name` (string) *(required)*
  - Page name/title
- `type` (string) *(required)*
  - Page type classification
- `url` (string) *(required)*
  - URL path
- `bounded_context` (string) 
  - Primary bounded context

---

### page_section

**Domain:** UX

**Description:** Section within a page

**Required Fields:** section_id, type

**Total Properties:** 7

**Key Properties:**

- `section_id` (string) *(required)*
- `type` (string) *(required)*
- `title` (string) 
  - Section heading
- `components` (array) 
  - Component IDs used in section
- `collapsible` (boolean) 
  - Can section be collapsed

---

### pagination_config

**Domain:** UX

**Description:** Pagination configuration

**Total Properties:** 5

**Key Properties:**

- `type` (string) 
- `page_size` (integer) 
  - Items per page
- `page_size_options` (array) 
  - User-selectable page sizes
- `show_total` (boolean) 
  - Display total item count
- `repository_method` (string) 
  - DDD repository pagination method

---

### responsive_config

**Domain:** UX

**Description:** Responsive behavior configuration across device breakpoints

**Total Properties:** 3

**Key Properties:**

- `mobile` (string) 
  - Mobile layout pattern
- `tablet` (string) 
  - Tablet layout pattern
- `desktop` (string) 
  - Desktop layout pattern

---

### search_system

**Domain:** UX

**Description:** Search configuration

**Total Properties:** 4

**Key Properties:**

- `type` (string) 
- `scope` (string) 
- `features` (array) 
- `indexed_fields` (array) 
  - Fields included in search index

---

### validation_config

**Domain:** UX

**Description:** Validation behavior configuration

**Total Properties:** 3

**Key Properties:**

- `timing` (string) 
- `debounce_ms` (integer) 
  - Debounce delay (milliseconds)
- `rules` (array) 

---

### workflow

**Domain:** UX

**Description:** Multi-step user workflows

**Required Fields:** workflow_id, name, type, steps

**Total Properties:** 10

**Key Properties:**

- `workflow_id` (string) *(required)*
- `name` (string) *(required)*
  - Workflow name
- `type` (string) *(required)*
  - Workflow pattern type
- `bounded_contexts` (array) 
  - Bounded contexts involved in workflow
- `application_service` (string) 
  - DDD application service implementing workflow

---

## Alphabetical Index

- **accessibility_spec** (UX)
- **aggregate** (DDD)
- **agile_release_train** (Agile)
- **animation** (UX)
- **application_service** (DDD)
- **architectural_runway** (Agile)
- **behavior** (UX)
- **bounded_context** (DDD)
- **caching_config** (UX)
- **cadence** (Agile)
- **ceremony** (Agile)
- **check** (Data-Eng)
- **component** (UX)
- **context_mapping** (DDD)
- **contract** (Data-Eng)
- **contract_test** (QE)
- **coverage_target** (QE)
- **data_access_pattern** (Data-Eng)
- **data_catalog_entry** (Data-Eng)
- **data_contract** (Data-Eng)
- **data_monitoring_metric** (Data-Eng)
- **data_partition_strategy** (Data-Eng)
- **data_pipeline_template** (Data-Eng)
- **data_product** (Data-Eng)
- **data_quality_dimension** (Data-Eng)
- **data_replication_config** (Data-Eng)
- **data_retention_tier** (Data-Eng)
- **data_transformation_function** (Data-Eng)
- **data_validation_rule_type** (Data-Eng)
- **dataset** (Data-Eng)
- **defect** (QE)
- **definition_of_ready** (Agile)
- **design_tokens** (UX)
- **domain** (Data-Eng)
- **domain_event** (DDD)
- **domain_service** (DDD)
- **enabler** (Agile)
- **entity** (DDD)
- **epic** (Agile)
- **estimation_technique** (Agile)
- **facet** (UX)
- **facet_value** (UX)
- **factory** (DDD)
- **feature** (Agile)
- **feedback_loop** (Agile)
- **field** (Data-Eng)
- **governance** (Data-Eng)
- **hierarchy_node** (UX)
- **impediment** (Agile)
- **incident_report** (QE)
- **increment** (Agile)
- **information_architecture** (UX)
- **iteration** (Agile)
- **lineage** (Data-Eng)
- **metadata** (Agile)
- **metric** (Agile)
- **navigation** (UX)
- **non_functional_requirement** (Agile)
- **observability** (Data-Eng)
- **owner** (Data-Eng)
- **page** (UX)
- **page_section** (UX)
- **pagination_config** (UX)
- **pipeline** (Data-Eng)
- **portfolio** (Agile)
- **product** (Agile)
- **program_increment** (Agile)
- **quality_characteristics** (QE)
- **release** (Agile)
- **release_vision** (Agile)
- **repository** (DDD)
- **responsive_config** (UX)
- **risk** (Agile)
- **roadmap** (Agile)
- **role** (Agile)
- **schedule** (Data-Eng)
- **search_system** (UX)
- **specification** (DDD)
- **sprint** (Agile)
- **stage** (Data-Eng)
- **stakeholder** (Agile)
- **system** (Data-Eng)
- **task** (Agile)
- **team** (Agile)
- **team_member** (Agile)
- **team_topology** (Agile)
- **technical_debt** (Agile)
- **test_assertion** (QE)
- **test_automation** (QE)
- **test_case** (QE)
- **test_configuration** (QE)
- **test_coverage_type** (QE)
- **test_data** (QE)
- **test_double** (QE)
- **test_environment** (QE)
- **test_execution_order** (QE)
- **test_execution_plan** (QE)
- **test_fixture** (QE)
- **test_harness** (QE)
- **test_metrics** (QE)
- **test_oracle** (QE)
- **test_priority_scheme** (QE)
- **test_scenario** (QE)
- **test_script** (QE)
- **test_stakeholder_role** (QE)
- **test_strategy** (QE)
- **test_suite** (QE)
- **test_tool** (QE)
- **testing_technique_spec** (QE)
- **transform** (Data-Eng)
- **user_story** (Agile)
- **validation_config** (UX)
- **value_object** (DDD)
- **value_stream** (Agile)
- **vision** (Agile)
- **workflow** (UX)
- **working_agreement** (Agile)