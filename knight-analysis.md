# Knight Codebase Analysis: DDD + CQRS + BFF Patterns

**Analysis Date:** 2025-10-18
**Codebase:** `/Users/igor/code/knight/contexts`
**Purpose:** Ground canonical schemas in real-world implementation patterns

---

## Executive Summary

The Knight codebase implements a **clean hexagonal architecture** with strict separation between:
- **API layer** (Commands, Queries, Events as interfaces/records)
- **Application layer** (Application Services implementing CQRS interfaces)
- **Domain layer** (Aggregates with pure business logic)
- **Infrastructure layer** (REST Controllers, JPA Repositories, Kafka)

Each bounded context follows **identical patterns**, making the architecture highly consistent and predictable.

---

## 1. Command Pattern Analysis

### Pattern Overview
Commands are defined as **record types nested inside interface contracts** in the API layer. This creates immutable, type-safe command objects with minimal boilerplate.

### Key Characteristics
- **Location:** `{context}/api/src/main/java/.../api/commands/`
- **Structure:** Interface with nested `record` types for each command
- **Naming:** `{Entity}Commands` interface, `{Action}{Entity}Cmd` records
- **Return types:** Domain identifiers (UserId, ServicingProfileId) or void
- **Parameters:** Primitive types + SharedKernel value objects

### Representative Examples

#### Example 1: User Management Commands
**File:** `/Users/igor/code/knight/contexts/users/users/api/src/main/java/com/knight/contexts/users/users/api/commands/UserCommands.java`

```java
public interface UserCommands {

    UserId createUser(CreateUserCmd cmd);

    record CreateUserCmd(
        String email,
        String userType,
        String identityProvider,
        ClientId clientId
    ) {}

    void activateUser(ActivateUserCmd cmd);
    record ActivateUserCmd(UserId userId) {}

    void deactivateUser(DeactivateUserCmd cmd);
    record DeactivateUserCmd(UserId userId, String reason) {}

    void lockUser(LockUserCmd cmd);
    record LockUserCmd(UserId userId, String reason) {}

    void unlockUser(UnlockUserCmd cmd);
    record UnlockUserCmd(UserId userId) {}
}
```

**Pattern observations:**
- Creation commands return identifiers (UserId)
- State transition commands return void
- Commands include business intent (activate/deactivate/lock/unlock)
- Reason parameters for audit trail

#### Example 2: Service Profile Management Commands
**File:** `/Users/igor/code/knight/contexts/service-profiles/management/api/src/main/java/com/knight/contexts/serviceprofiles/management/api/commands/SpmCommands.java`

```java
public interface SpmCommands {

    ServicingProfileId createServicingProfile(ClientId clientId, String createdBy);

    record EnrollServiceCmd(
        ServicingProfileId profileId,
        String serviceType,
        String configurationJson
    ) {}
    void enrollService(EnrollServiceCmd cmd);

    record EnrollAccountCmd(
        ServicingProfileId profileId,
        String serviceEnrollmentId,
        String accountId
    ) {}
    void enrollAccount(EnrollAccountCmd cmd);

    record SuspendProfileCmd(
        ServicingProfileId profileId,
        String reason
    ) {}
    void suspendProfile(SuspendProfileCmd cmd);
}
```

**Pattern observations:**
- Nested enrollment pattern (service → account)
- Configuration passed as JSON string (schema flexibility)
- Audit trail with `createdBy` parameter
- Hierarchical identifiers (profileId → serviceEnrollmentId)

#### Example 3: Approval Workflow Commands
**File:** `/Users/igor/code/knight/contexts/approval-workflows/engine/api/src/main/java/com/knight/contexts/approvalworkflows/engine/api/commands/ApprovalWorkflowCommands.java`

```java
public interface ApprovalWorkflowCommands {

    String initiateWorkflow(InitiateWorkflowCmd cmd);

    record InitiateWorkflowCmd(
        String resourceType,
        String resourceId,
        int requiredApprovals,
        String initiatedBy
    ) {}

    void recordApproval(RecordApprovalCmd cmd);

    record RecordApprovalCmd(
        String workflowId,
        String approverUserId,
        String decision,
        String comments
    ) {}

    void expireWorkflow(ExpireWorkflowCmd cmd);
    record ExpireWorkflowCmd(String workflowId) {}
}
```

**Pattern observations:**
- Generic workflow engine (resourceType/resourceId pattern)
- Decision as string enum (validated in domain layer)
- Lifecycle management (initiate → record → expire)
- Metadata fields (comments, initiatedBy)

#### Example 4: Policy Management Commands
**File:** `/Users/igor/code/knight/contexts/users/policy/api/src/main/java/com/knight/contexts/users/policy/api/commands/PolicyCommands.java`

```java
public interface PolicyCommands {

    String createPolicy(CreatePolicyCmd cmd);

    record CreatePolicyCmd(
        String policyType,
        String subject,
        String action,
        String resource,
        Integer approverCount
    ) {}

    void updatePolicy(UpdatePolicyCmd cmd);

    record UpdatePolicyCmd(
        String policyId,
        String action,
        String resource,
        Integer approverCount
    ) {}

    void deletePolicy(DeletePolicyCmd cmd);
    record DeletePolicyCmd(String policyId) {}
}
```

**Pattern observations:**
- CRUD pattern (create/update/delete)
- Subject-Action-Resource authorization pattern
- Conditional fields (approverCount for APPROVAL policy type)

#### Example 5: Indirect Client Commands
**File:** `/Users/igor/code/knight/contexts/service-profiles/indirect-clients/api/src/main/java/com/knight/contexts/serviceprofiles/indirectclients/api/commands/IndirectClientCommands.java`

```java
public interface IndirectClientCommands {

    IndirectClientId createIndirectClient(CreateIndirectClientCmd cmd);

    record CreateIndirectClientCmd(
        ClientId parentClientId,
        String businessName,
        String taxId
    ) {}

    void addRelatedPerson(AddRelatedPersonCmd cmd);

    record AddRelatedPersonCmd(
        IndirectClientId indirectClientId,
        String name,
        String role,
        String email
    ) {}

    void updateBusinessInfo(UpdateBusinessInfoCmd cmd);

    record UpdateBusinessInfoCmd(
        IndirectClientId indirectClientId,
        String businessName,
        String taxId
    ) {}
}
```

**Pattern observations:**
- Hierarchical relationships (parentClientId)
- Entity collection management (addRelatedPerson)
- Partial update patterns (updateBusinessInfo)

### Command Pattern Summary

| Aspect | Pattern |
|--------|---------|
| **Structure** | Interface + nested record types |
| **Mutability** | Immutable records (final fields) |
| **Validation** | Deferred to Application/Domain layer |
| **Naming** | `{Action}{Entity}Cmd` |
| **Return Types** | Domain IDs (create) or void (transitions) |
| **Parameters** | Primitives + SharedKernel value objects |
| **Organization** | One interface per aggregate root |

---

## 2. Query Pattern Analysis

### Pattern Overview
Queries follow the same interface pattern as commands, with **nested record types for results** (DTOs). Queries are read-only operations that return projections of domain state.

### Key Characteristics
- **Location:** `{context}/api/src/main/java/.../api/queries/`
- **Structure:** Interface with nested `record` result types
- **Naming:** `{Entity}Queries` interface, `{Entity}Summary` result records
- **Return types:** Record DTOs (never domain aggregates)
- **Parameters:** Domain identifiers

### Representative Examples

#### Example 1: User Queries
**File:** `/Users/igor/code/knight/contexts/users/users/api/src/main/java/com/knight/contexts/users/users/api/queries/UserQueries.java`

```java
public interface UserQueries {

    record UserSummary(
        String userId,
        String email,
        String status,
        String userType,
        String identityProvider
    ) {}

    UserSummary getUserSummary(UserId userId);
}
```

**Pattern observations:**
- Single summary query per aggregate
- All IDs serialized to strings
- Enums serialized to strings (status, userType, identityProvider)
- Flat structure (no nested objects)

#### Example 2: Service Profile Queries
**File:** `/Users/igor/code/knight/contexts/service-profiles/management/api/src/main/java/com/knight/contexts/serviceprofiles/management/api/queries/SpmQueries.java`

```java
public interface SpmQueries {

    record ServicingProfileSummary(
        String profileUrn,
        String status,
        int enrolledServices,
        int enrolledAccounts
    ) {}

    ServicingProfileSummary getServicingProfileSummary(ServicingProfileId profileId);
}
```

**Pattern observations:**
- Aggregate counts (enrolledServices, enrolledAccounts)
- URN serialization for compound identifiers
- No collection details in summary

#### Example 3: Approval Workflow Queries
**File:** `/Users/igor/code/knight/contexts/approval-workflows/engine/api/src/main/java/com/knight/contexts/approvalworkflows/engine/api/queries/ApprovalWorkflowQueries.java`

```java
public interface ApprovalWorkflowQueries {

    record ApprovalWorkflowSummary(
        String workflowId,
        String status,
        String resourceType,
        String resourceId,
        int requiredApprovals,
        int receivedApprovals
    ) {}

    ApprovalWorkflowSummary getWorkflowSummary(String workflowId);
}
```

**Pattern observations:**
- Progress indicators (requiredApprovals vs receivedApprovals)
- Generic resource references (resourceType + resourceId)

#### Example 4: Policy Queries
**File:** `/Users/igor/code/knight/contexts/users/policy/api/src/main/java/com/knight/contexts/users/policy/api/queries/PolicyQueries.java`

```java
public interface PolicyQueries {

    record PolicySummary(
        String policyId,
        String policyType,
        String subject,
        String action,
        String resource,
        Integer approverCount
    ) {}

    PolicySummary getPolicySummary(String policyId);
}
```

**Pattern observations:**
- Complete snapshot of policy state
- Nullable fields (Integer approverCount)

#### Example 5: Indirect Client Queries
**File:** `/Users/igor/code/knight/contexts/service-profiles/indirect-clients/api/src/main/java/com/knight/contexts/serviceprofiles/indirectclients/api/queries/IndirectClientQueries.java`

```java
public interface IndirectClientQueries {

    record IndirectClientSummary(
        String indirectClientUrn,
        String businessName,
        String status,
        int relatedPersonsCount
    ) {}

    IndirectClientSummary getIndirectClientSummary(IndirectClientId id);
}
```

### Query Pattern Summary

| Aspect | Pattern |
|--------|---------|
| **Structure** | Interface + nested record result types |
| **Naming** | `{Entity}Summary` for result records |
| **Serialization** | All complex types → strings (IDs, enums) |
| **Aggregation** | Counts, not collections |
| **Scope** | Single aggregate per query |
| **Filtering** | No filtering parameters (direct ID lookup) |

---

## 3. Application Service Pattern Analysis

### Pattern Overview
Application Services **implement both Commands and Queries interfaces** in a single class. They orchestrate:
1. Aggregate retrieval/creation
2. Business logic delegation to aggregates
3. Persistence via repository
4. Event publishing
5. Transaction management (@Transactional)

### Key Characteristics
- **Location:** `{context}/app/src/main/java/.../app/service/`
- **Annotation:** `@Singleton` (Micronaut DI)
- **Implements:** Both `{Entity}Commands` and `{Entity}Queries`
- **Dependencies:** Repository, EventPublisher
- **Transactions:** All commands @Transactional, queries not transactional

### Representative Example: User Application Service

**File:** `/Users/igor/code/knight/contexts/users/users/app/src/main/java/com/knight/contexts/users/users/app/service/UserApplicationService.java`

```java
@Singleton
public class UserApplicationService implements UserCommands, UserQueries {

    private final UserRepository repository;
    private final ApplicationEventPublisher<Object> eventPublisher;

    public UserApplicationService(
        UserRepository repository,
        ApplicationEventPublisher<Object> eventPublisher
    ) {
        this.repository = repository;
        this.eventPublisher = eventPublisher;
    }

    @Override
    @Transactional
    public UserId createUser(CreateUserCmd cmd) {
        UserId userId = UserId.of(java.util.UUID.randomUUID().toString());

        // Parse enums
        User.UserType userType = User.UserType.valueOf(cmd.userType());
        User.IdentityProvider identityProvider = User.IdentityProvider.valueOf(cmd.identityProvider());

        // Create aggregate
        User user = User.create(userId, cmd.email(), userType, identityProvider, cmd.clientId());

        // Save
        repository.save(user);

        // Publish event
        eventPublisher.publishEvent(new UserCreated(
            userId.id(),
            cmd.email(),
            cmd.userType(),
            cmd.identityProvider(),
            Instant.now()
        ));

        return userId;
    }

    @Override
    @Transactional
    public void activateUser(ActivateUserCmd cmd) {
        User user = repository.findById(cmd.userId())
            .orElseThrow(() -> new IllegalArgumentException("User not found: " + cmd.userId().id()));

        user.activate();

        repository.save(user);

        eventPublisher.publishEvent(new Object()); // UserActivated event
    }

    @Override
    public UserSummary getUserSummary(UserId userId) {
        User user = repository.findById(userId)
            .orElseThrow(() -> new IllegalArgumentException("User not found: " + userId.id()));

        return new UserSummary(
            user.getUserId().id(),
            user.getEmail(),
            user.getStatus().name(),
            user.getUserType().name(),
            user.getIdentityProvider().name()
        );
    }

    // Repository interface (to be implemented in infra layer)
    public interface UserRepository {
        void save(User user);
        java.util.Optional<User> findById(UserId userId);
    }
}
```

**Pattern observations:**
1. **ID Generation:** Application service generates IDs (not database)
2. **Enum parsing:** Strings → domain enums in app service
3. **Aggregate delegation:** Business logic in `user.activate()`
4. **Save pattern:** Always save after mutation
5. **Event timing:** After persistence (in-memory publisher)
6. **Repository interface:** Defined in app layer, implemented in infra
7. **Query mapping:** Domain aggregate → DTO record

### Application Service Pattern: Service Profile Management

**File:** `/Users/igor/code/knight/contexts/service-profiles/management/app/src/main/java/com/knight/contexts/serviceprofiles/management/app/service/SpmApplicationService.java`

```java
@Singleton
public class SpmApplicationService implements SpmCommands, SpmQueries {

    private final SpmRepository repository;
    private final ServicingProfileEventProducer eventProducer;

    @Override
    @Transactional
    public ServicingProfileId createServicingProfile(ClientId clientId, String createdBy) {
        ServicingProfileId profileId = ServicingProfileId.of(clientId);

        // 1. Create aggregate
        ServicingProfile profile = ServicingProfile.create(profileId, clientId, createdBy);

        // 2. Save aggregate
        repository.save(profile);

        // 3. Save event to outbox (SAME TRANSACTION)
        ServicingProfileCreated event = new ServicingProfileCreated(
            profileId.urn(),
            clientId.urn(),
            profile.getStatus().name(),
            createdBy,
            Instant.now()
        );
        eventProducer.publishServicingProfileCreated(event);

        return profileId;
    }

    @Override
    @Transactional
    public void enrollService(EnrollServiceCmd cmd) {
        ServicingProfile profile = repository.findById(cmd.profileId())
            .orElseThrow(() -> new IllegalArgumentException("Profile not found: " + cmd.profileId().urn()));

        profile.enrollService(cmd.serviceType(), cmd.configurationJson());

        repository.save(profile);
    }

    // Inner interface for event producer (implemented in infra layer)
    public interface ServicingProfileEventProducer {
        void publishServicingProfileCreated(ServicingProfileCreated event);
    }

    public interface SpmRepository {
        void save(ServicingProfile profile);
        java.util.Optional<ServicingProfile> findById(ServicingProfileId profileId);
    }
}
```

**Pattern observations:**
1. **Outbox pattern:** Custom event producer (not ApplicationEventPublisher)
2. **Transactional event:** Event saved in same transaction as aggregate
3. **Derived IDs:** ServicingProfileId derived from ClientId
4. **Nested operations:** enrollService returns ServiceEnrollment but not exposed in API

### Application Service Pattern Summary

| Aspect | Pattern |
|--------|---------|
| **Scope** | Single aggregate root |
| **Implements** | Commands + Queries interfaces |
| **Transaction boundary** | @Transactional on all commands |
| **ID generation** | Application service (UUID) |
| **Validation** | Aggregate methods (domain layer) |
| **Error handling** | IllegalArgumentException for not found |
| **Event publishing** | After persistence, same transaction |
| **Repository pattern** | Interface in app layer, impl in infra |

---

## 4. BFF/Controller Pattern Analysis

### Pattern Overview
REST Controllers act as **Backend-for-Frontend (BFF)** adapters. They:
1. Map HTTP requests to command/query objects
2. Convert string URNs to value objects
3. Delegate to Application Services
4. Convert results to JSON-serializable DTOs

### Key Characteristics
- **Location:** `{context}/infra/src/main/java/.../infra/rest/`
- **Annotation:** `@Controller("/commands/{context}/{entity}")`
- **HTTP Verbs:** All commands use POST (not PUT/PATCH)
- **Blocking:** `@ExecuteOn(TaskExecutors.BLOCKING)`
- **DTOs:** Nested record types in controller

### Representative Example: User Command Controller

**File:** `/Users/igor/code/knight/contexts/users/users/infra/src/main/java/com/knight/contexts/users/users/infra/rest/UserCommandController.java`

```java
@Controller("/commands/users")
@ExecuteOn(TaskExecutors.BLOCKING)
public class UserCommandController {

    @Inject
    UserCommands commands;

    @Post("/create")
    public CreateUserResult createUser(@Body CreateUserRequest req) {
        var clientId = ClientId.of(req.clientUrn());
        var userId = commands.createUser(new UserCommands.CreateUserCmd(
            req.email(),
            req.userType(),
            req.identityProvider(),
            clientId
        ));
        return new CreateUserResult(userId.id());
    }

    @Post("/activate")
    public void activateUser(@Body ActivateUserRequest req) {
        var userId = UserId.of(req.userId());
        commands.activateUser(new UserCommands.ActivateUserCmd(userId));
    }

    @Post("/deactivate")
    public void deactivateUser(@Body DeactivateUserRequest req) {
        var userId = UserId.of(req.userId());
        commands.deactivateUser(new UserCommands.DeactivateUserCmd(userId, req.reason()));
    }

    public record CreateUserRequest(String email, String userType, String identityProvider, String clientUrn) {}
    public record CreateUserResult(String userId) {}
    public record ActivateUserRequest(String userId) {}
    public record DeactivateUserRequest(String userId, String reason) {}
}
```

**Pattern observations:**
1. **URL structure:** `/commands/{context}/{entity}/{action}`
2. **All POST:** No PUT/PATCH/DELETE verbs
3. **String conversion:** URN strings → value objects (ClientId, UserId)
4. **Request/Result records:** Separate DTOs from API command records
5. **Synchronous:** Blocking execution (not reactive)
6. **No validation:** Validation happens in domain layer

### BFF Pattern: Service Profile Controller

**File:** `/Users/igor/code/knight/contexts/service-profiles/management/infra/src/main/java/com/knight/contexts/serviceprofiles/management/infra/rest/SpmCommandController.java`

```java
@Controller("/commands/service-profiles/servicing")
@ExecuteOn(TaskExecutors.BLOCKING)
public class SpmCommandController {

    @Inject
    SpmCommands commands;

    @Post("/create")
    public CreateProfileResult createProfile(@Body CreateProfileRequest req) {
        var clientId = ClientId.of(req.clientUrn());
        var profileId = commands.createServicingProfile(clientId, req.createdBy());
        return new CreateProfileResult(profileId.urn());
    }

    @Post("/enroll-service")
    public void enrollService(@Body EnrollServiceRequest req) {
        var profileId = ServicingProfileId.fromUrn(req.profileUrn());
        commands.enrollService(new SpmCommands.EnrollServiceCmd(
            profileId,
            req.serviceType(),
            req.configurationJson()
        ));
    }

    public record CreateProfileRequest(String clientUrn, String createdBy) {}
    public record CreateProfileResult(String profileUrn) {}
    public record EnrollServiceRequest(String profileUrn, String serviceType, String configurationJson) {}
}
```

**Pattern observations:**
1. **Nested paths:** `/commands/service-profiles/servicing` (multi-level context)
2. **URN conversion:** `ServicingProfileId.fromUrn()` for compound IDs
3. **Audit fields:** `createdBy` passed through controller

### BFF Pattern: Approval Workflow Controller

**File:** `/Users/igor/code/knight/contexts/approval-workflows/engine/infra/src/main/java/com/knight/contexts/approvalworkflows/engine/infra/rest/ApprovalWorkflowCommandController.java`

```java
@Controller("/commands/approval-workflows")
@ExecuteOn(TaskExecutors.BLOCKING)
public class ApprovalWorkflowCommandController {

    @Inject
    ApprovalWorkflowCommands commands;

    @Post("/initiate")
    public InitiateWorkflowResult initiateWorkflow(@Body InitiateWorkflowRequest req) {
        var workflowId = commands.initiateWorkflow(new ApprovalWorkflowCommands.InitiateWorkflowCmd(
            req.resourceType(),
            req.resourceId(),
            req.requiredApprovals(),
            req.initiatedBy()
        ));
        return new InitiateWorkflowResult(workflowId);
    }

    @Post("/record-approval")
    public void recordApproval(@Body RecordApprovalRequest req) {
        commands.recordApproval(new ApprovalWorkflowCommands.RecordApprovalCmd(
            req.workflowId(),
            req.approverUserId(),
            req.decision(),
            req.comments()
        ));
    }

    public record InitiateWorkflowRequest(String resourceType, String resourceId, int requiredApprovals, String initiatedBy) {}
    public record InitiateWorkflowResult(String workflowId) {}
    public record RecordApprovalRequest(String workflowId, String approverUserId, String decision, String comments) {}
}
```

### BFF Pattern Summary

| Aspect | Pattern |
|--------|---------|
| **URL convention** | `/commands/{context}/{entity}/{action}` |
| **HTTP verbs** | POST only (command semantics) |
| **DTO layer** | Separate Request/Result records (not API records) |
| **Value object conversion** | Controller responsibility |
| **Execution model** | Blocking (TaskExecutors.BLOCKING) |
| **BFF scope** | One controller per bounded context |
| **Error handling** | Framework default (not shown) |

---

## 5. Domain Aggregate Pattern Analysis

### Pattern Overview
Aggregates are **pure domain objects** with:
1. Private constructors
2. Static factory methods (`create()`, `initiate()`)
3. Business logic in instance methods
4. Invariant protection
5. No infrastructure dependencies

### Representative Example: User Aggregate

**File:** `/Users/igor/code/knight/contexts/users/users/domain/src/main/java/com/knight/contexts/users/users/domain/aggregate/User.java`

```java
public class User {

    public enum Status {
        PENDING, ACTIVE, LOCKED, DEACTIVATED
    }

    public enum UserType {
        DIRECT, INDIRECT
    }

    public enum IdentityProvider {
        OKTA, A_AND_P
    }

    private final UserId userId;
    private final String email;
    private final UserType userType;
    private final IdentityProvider identityProvider;
    private final ClientId clientId;
    private Status status;
    private final Instant createdAt;
    private Instant updatedAt;
    private String lockReason;
    private String deactivationReason;

    private User(UserId userId, String email, UserType userType,
                IdentityProvider identityProvider, ClientId clientId) {
        this.userId = userId;
        this.email = email;
        this.userType = userType;
        this.identityProvider = identityProvider;
        this.clientId = clientId;
        this.status = Status.PENDING;
        this.createdAt = Instant.now();
        this.updatedAt = Instant.now();
    }

    public static User create(UserId userId, String email, UserType userType,
                             IdentityProvider identityProvider, ClientId clientId) {
        if (userId == null) {
            throw new IllegalArgumentException("User ID cannot be null");
        }
        if (email == null || email.isBlank() || !email.contains("@")) {
            throw new IllegalArgumentException("Valid email is required");
        }
        // ... more validation
        return new User(userId, email, userType, identityProvider, clientId);
    }

    public void activate() {
        if (this.status == Status.LOCKED) {
            throw new IllegalStateException("Cannot activate locked user. Unlock first.");
        }
        if (this.status == Status.ACTIVE) {
            return; // Already active
        }
        this.status = Status.ACTIVE;
        this.updatedAt = Instant.now();
        this.deactivationReason = null;
    }

    public void lock(String reason) {
        if (this.status == Status.LOCKED) {
            return; // Already locked
        }
        if (reason == null || reason.isBlank()) {
            throw new IllegalArgumentException("Lock reason is required");
        }
        this.status = Status.LOCKED;
        this.lockReason = reason;
        this.updatedAt = Instant.now();
    }
}
```

**Pattern observations:**
1. **Immutable identity:** Final userId, email, userType, identityProvider, clientId
2. **Mutable state:** status, lockReason, updatedAt
3. **State machine:** PENDING → ACTIVE → LOCKED/DEACTIVATED
4. **Invariant enforcement:** Cannot activate locked user
5. **Idempotency:** activate() on ACTIVE is no-op
6. **Metadata:** createdAt/updatedAt managed by aggregate

### Domain Pattern: Servicing Profile Aggregate

**File:** `/Users/igor/code/knight/contexts/service-profiles/management/domain/src/main/java/com/knight/contexts/serviceprofiles/management/domain/aggregate/ServicingProfile.java`

```java
public class ServicingProfile {

    public static class ServiceEnrollment {
        private final String enrollmentId;
        private final String serviceType;
        private final String configuration;
        private Status status;
        private final Instant enrolledAt;

        public ServiceEnrollment(String serviceType, String configuration) {
            this.enrollmentId = UUID.randomUUID().toString();
            this.serviceType = serviceType;
            this.configuration = configuration;
            this.status = Status.ACTIVE;
            this.enrolledAt = Instant.now();
        }
    }

    public static class AccountEnrollment {
        private final String enrollmentId;
        private final String serviceEnrollmentId;
        private final String accountId;
        private Status status;
        private final Instant enrolledAt;

        public AccountEnrollment(String serviceEnrollmentId, String accountId) {
            this.enrollmentId = UUID.randomUUID().toString();
            this.serviceEnrollmentId = serviceEnrollmentId;
            this.accountId = accountId;
            this.status = Status.ACTIVE;
            this.enrolledAt = Instant.now();
        }
    }

    private final ServicingProfileId profileId;
    private final ClientId clientId;
    private Status status;
    private final List<ServiceEnrollment> serviceEnrollments;
    private final List<AccountEnrollment> accountEnrollments;

    public ServiceEnrollment enrollService(String serviceType, String configuration) {
        if (this.status != Status.ACTIVE && this.status != Status.PENDING) {
            throw new IllegalStateException("Cannot enroll service to profile in status: " + this.status);
        }

        ServiceEnrollment enrollment = new ServiceEnrollment(serviceType, configuration);
        this.serviceEnrollments.add(enrollment);
        this.updatedAt = Instant.now();

        // Activate profile if it was pending and now has services
        if (this.status == Status.PENDING && !this.serviceEnrollments.isEmpty()) {
            this.status = Status.ACTIVE;
        }

        return enrollment;
    }

    public AccountEnrollment enrollAccount(String serviceEnrollmentId, String accountId) {
        if (this.status != Status.ACTIVE) {
            throw new IllegalStateException("Cannot enroll account to profile in status: " + this.status);
        }

        // Verify service enrollment exists
        boolean serviceExists = serviceEnrollments.stream()
            .anyMatch(se -> se.getEnrollmentId().equals(serviceEnrollmentId));
        if (!serviceExists) {
            throw new IllegalArgumentException("Service enrollment not found: " + serviceEnrollmentId);
        }

        AccountEnrollment enrollment = new AccountEnrollment(serviceEnrollmentId, accountId);
        this.accountEnrollments.add(enrollment);
        this.updatedAt = Instant.now();

        return enrollment;
    }
}
```

**Pattern observations:**
1. **Entity collections:** ServiceEnrollment, AccountEnrollment as nested entities
2. **ID generation:** Entities generate their own UUIDs
3. **Referential integrity:** Verify serviceEnrollmentId exists before enrollAccount
4. **State transitions:** PENDING → ACTIVE when first service enrolled
5. **Defensive copies:** `getServiceEnrollments()` returns `List.copyOf()`

### Domain Pattern: Approval Workflow Aggregate

**File:** `/Users/igor/code/knight/contexts/approval-workflows/engine/domain/src/main/java/com/knight/contexts/approvalworkflows/engine/domain/aggregate/ApprovalWorkflow.java`

```java
public class ApprovalWorkflow {

    public enum Status {
        PENDING, APPROVED, REJECTED, EXPIRED
    }

    public enum Decision {
        APPROVE, REJECT
    }

    public static class Approval {
        private final String approvalId;
        private final String approverUserId;
        private final Decision decision;
        private final String comments;
        private final Instant approvedAt;

        public Approval(String approverUserId, Decision decision, String comments) {
            this.approvalId = UUID.randomUUID().toString();
            this.approverUserId = approverUserId;
            this.decision = decision;
            this.comments = comments;
            this.approvedAt = Instant.now();
        }
    }

    private final String workflowId;
    private final String resourceType;
    private final String resourceId;
    private final int requiredApprovals;
    private Status status;
    private final List<Approval> receivedApprovals;

    public void recordApproval(String approverUserId, Decision decision, String comments) {
        if (this.status != Status.PENDING) {
            throw new IllegalStateException("Cannot record approval for workflow in status: " + this.status);
        }

        // Check if approver already approved
        boolean alreadyApproved = receivedApprovals.stream()
            .anyMatch(a -> a.getApproverUserId().equals(approverUserId));
        if (alreadyApproved) {
            throw new IllegalStateException("User has already provided approval: " + approverUserId);
        }

        Approval approval = new Approval(approverUserId, decision, comments);
        this.receivedApprovals.add(approval);

        // If rejected, immediately reject the workflow
        if (decision == Decision.REJECT) {
            this.status = Status.REJECTED;
            this.completedAt = Instant.now();
            return;
        }

        // Check if we have enough approvals
        long approveCount = receivedApprovals.stream()
            .filter(a -> a.getDecision() == Decision.APPROVE)
            .count();

        if (approveCount >= requiredApprovals) {
            this.status = Status.APPROVED;
            this.completedAt = Instant.now();
        }
    }
}
```

**Pattern observations:**
1. **Business rules:** One rejection → workflow rejected
2. **Threshold logic:** Count approvals, auto-approve when threshold met
3. **Duplicate prevention:** Check if user already approved
4. **Terminal states:** APPROVED/REJECTED/EXPIRED cannot transition

### Domain Aggregate Pattern Summary

| Aspect | Pattern |
|--------|---------|
| **Constructor** | Private |
| **Factory method** | `create()`, `initiate()` |
| **ID generation** | Aggregate or app service |
| **Validation** | In factory + mutation methods |
| **State transitions** | Explicit methods (activate, lock, etc.) |
| **Entity collections** | List of nested entity classes |
| **Defensive copies** | `List.copyOf()` on getters |
| **Dependencies** | Only SharedKernel value objects |

---

## 6. Event Pattern Analysis

### Pattern Overview
Events are **immutable record types** representing facts that have occurred. They are:
1. Defined in API layer (published contract)
2. Created by Application Services
3. Published after persistence
4. Serialized to Kafka via Outbox pattern

### Representative Examples

#### Example 1: UserCreated Event
**File:** `/Users/igor/code/knight/contexts/users/users/api/src/main/java/com/knight/contexts/users/users/api/events/UserCreated.java`

```java
public record UserCreated(
    String userId,
    String email,
    String userType,
    String identityProvider,
    Instant createdAt
) {}
```

#### Example 2: ServicingProfileCreated Event
**File:** `/Users/igor/code/knight/contexts/service-profiles/management/api/src/main/java/com/knight/contexts/serviceprofiles/management/api/events/ServicingProfileCreated.java`

```java
public record ServicingProfileCreated(
    String profileId,
    String clientId,
    String status,
    String createdBy,
    Instant createdAt
) {}
```

#### Example 3: WorkflowInitiated Event
**File:** `/Users/igor/code/knight/contexts/approval-workflows/engine/api/src/main/java/com/knight/contexts/approvalworkflows/engine/api/events/WorkflowInitiated.java`

```java
public record WorkflowInitiated(
    String workflowId,
    String resourceType,
    String resourceId,
    int requiredApprovals,
    Instant initiatedAt
) {}
```

### Event Pattern Summary

| Aspect | Pattern |
|--------|---------|
| **Structure** | Record type (immutable) |
| **Naming** | Past tense verb (UserCreated, WorkflowInitiated) |
| **Fields** | All strings (for serialization) + timestamp |
| **Location** | API layer (published contract) |
| **Publishing** | Application Service → EventPublisher/Outbox |

---

## 7. Value Object Pattern Analysis

### Pattern Overview
Value Objects in SharedKernel provide **type-safe identifiers** with built-in validation and URN serialization.

### Representative Examples

#### Example 1: UserId
**File:** `/Users/igor/code/knight/platform/shared-kernel/src/main/java/com/knight/platform/sharedkernel/UserId.java`

```java
public final class UserId {
    private final String id;

    private UserId(String id) {
        if (id == null || id.isBlank()) {
            throw new IllegalArgumentException("UserId cannot be null or blank");
        }
        this.id = id;
    }

    public static UserId of(String id) {
        return new UserId(id);
    }

    public String id() {
        return id;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        UserId userId = (UserId) o;
        return id.equals(userId.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }
}
```

#### Example 2: ClientId (URN-based)
**File:** `/Users/igor/code/knight/platform/shared-kernel/src/main/java/com/knight/platform/sharedkernel/ClientId.java`

```java
public final class ClientId {
    private static final Pattern PATTERN = Pattern.compile("^(srf|gid|ind):[A-Za-z0-9_-]+$");

    private final String urn;

    private ClientId(String urn) {
        if (urn == null || !PATTERN.matcher(urn).matches()) {
            throw new IllegalArgumentException(
                "Invalid ClientId format. Expected: {system}:{client_number} where system is srf, gid, or ind");
        }
        this.urn = urn;
    }

    public static ClientId of(String urn) {
        return new ClientId(urn);
    }

    public String urn() {
        return urn;
    }

    public String system() {
        return urn.split(":")[0];
    }

    public String clientNumber() {
        return urn.split(":")[1];
    }
}
```

#### Example 3: ServicingProfileId (Compound)
**File:** `/Users/igor/code/knight/platform/shared-kernel/src/main/java/com/knight/platform/sharedkernel/ServicingProfileId.java`

```java
public final class ServicingProfileId {
    private final ClientId clientId;
    private final String urn;

    private ServicingProfileId(ClientId clientId) {
        if (clientId == null) {
            throw new IllegalArgumentException("ClientId cannot be null");
        }
        String system = clientId.system();
        if (!"srf".equals(system) && !"gid".equals(system)) {
            throw new IllegalArgumentException("ServicingProfileId requires SRF or GID client");
        }
        this.clientId = clientId;
        this.urn = "servicing:" + clientId.urn();
    }

    public static ServicingProfileId of(ClientId clientId) {
        return new ServicingProfileId(clientId);
    }

    public static ServicingProfileId fromUrn(String urn) {
        if (urn == null || !urn.startsWith("servicing:")) {
            throw new IllegalArgumentException("Invalid ServicingProfileId URN format");
        }
        String clientUrn = urn.substring("servicing:".length());
        return new ServicingProfileId(ClientId.of(clientUrn));
    }

    public ClientId clientId() {
        return clientId;
    }

    public String urn() {
        return urn;
    }
}
```

### Value Object Pattern Summary

| Aspect | Pattern |
|--------|---------|
| **Immutability** | Final class, final field |
| **Validation** | In private constructor |
| **Factory method** | `of()` for creation, `fromUrn()` for deserialization |
| **Equality** | Based on value (equals/hashCode) |
| **URN format** | `{prefix}:{value}` or `{prefix}:{system}:{id}` |
| **Parsing** | Business logic in value object (clientId.system()) |

---

## 8. Architecture Observations

### Hexagonal Architecture (Ports & Adapters)

```
┌─────────────────────────────────────────────────────────────┐
│ INFRASTRUCTURE LAYER (infra/)                               │
│ - REST Controllers (Micronaut)                              │
│ - JPA Repositories                                          │
│ - Kafka Producers/Consumers                                 │
│ - Outbox Publisher                                          │
└─────────────────────────────────────────────────────────────┘
                           ▲
                           │ implements
                           │
┌─────────────────────────────────────────────────────────────┐
│ APPLICATION LAYER (app/)                                    │
│ - Application Services (Commands + Queries)                 │
│ - Repository Interfaces (inner interfaces)                  │
│ - Event Producer Interfaces                                 │
│ - Transaction Boundaries (@Transactional)                   │
└─────────────────────────────────────────────────────────────┘
                           ▲
                           │ uses
                           │
┌─────────────────────────────────────────────────────────────┐
│ DOMAIN LAYER (domain/)                                      │
│ - Aggregates (pure business logic)                          │
│ - Entities (nested in aggregates)                           │
│ - Enums (domain concepts)                                   │
└─────────────────────────────────────────────────────────────┘
                           ▲
                           │ uses
                           │
┌─────────────────────────────────────────────────────────────┐
│ API LAYER (api/)                                            │
│ - Command Interfaces + Records                              │
│ - Query Interfaces + Result Records                         │
│ - Domain Event Records                                      │
└─────────────────────────────────────────────────────────────┘
                           ▲
                           │ uses
                           │
┌─────────────────────────────────────────────────────────────┐
│ SHARED KERNEL (platform/shared-kernel/)                     │
│ - Value Objects (UserId, ClientId, etc.)                    │
└─────────────────────────────────────────────────────────────┘
```

### CQRS Implementation

**Command Side:**
- Commands interface → Application Service → Aggregate → Repository → Database
- Events published after persistence
- Transactional consistency

**Query Side:**
- Queries interface → Application Service → Repository → Database
- Returns DTOs (not aggregates)
- No transactions (read-only)
- **No separate read model** (queries use same database as commands)

### BFF Pattern

**One BFF per Bounded Context:**
- `/commands/users/*` → User context
- `/commands/service-profiles/servicing/*` → Service Profile Management context
- `/commands/service-profiles/indirect-clients/*` → Indirect Client context
- `/commands/approval-workflows/*` → Approval Workflow context
- `/commands/users/policy/*` → Policy context

**REST Conventions:**
- All commands via POST (not REST CRUD)
- URL structure: `/commands/{context}/{entity}/{action}`
- No query controllers shown (queries may be in separate `/queries/*` controllers)

### Transaction & Event Patterns

**In-Memory Event Bus (User context):**
```java
eventPublisher.publishEvent(new UserCreated(...));
```

**Outbox Pattern (Service Profile context):**
```java
eventProducer.publishServicingProfileCreated(event);
// → Writes to outbox table in same transaction
// → OutboxPublisher reads and publishes to Kafka asynchronously
```

---

## 9. Pattern Mapping: Knight ↔ Schema Concepts

| Schema Concept | Knight Implementation | File Location |
|----------------|----------------------|---------------|
| **Command** | Interface + nested record | `{context}/api/.../commands/{Entity}Commands.java` |
| **CommandHandler** | Application Service method | `{context}/app/.../service/{Entity}ApplicationService.java` |
| **Query** | Interface + result record | `{context}/api/.../queries/{Entity}Queries.java` |
| **QueryHandler** | Application Service method | `{context}/app/.../service/{Entity}ApplicationService.java` |
| **Aggregate** | Domain class with factory method | `{context}/domain/.../aggregate/{Entity}.java` |
| **Entity** | Nested class in Aggregate | Same file as Aggregate |
| **ValueObject** | Final class with validation | `platform/shared-kernel/src/.../sharedkernel/{Name}Id.java` |
| **DomainEvent** | Record type | `{context}/api/.../events/{Event}.java` |
| **Repository** | Interface in app, impl in infra | App: `{Entity}ApplicationService.{Entity}Repository`<br>Infra: `{context}/infra/.../persistence/{Entity}RepositoryImpl.java` |
| **ApplicationService** | @Singleton class | `{context}/app/.../service/{Entity}ApplicationService.java` |
| **BFF/Controller** | @Controller class | `{context}/infra/.../rest/{Entity}CommandController.java` |
| **RequestDTO** | Nested record in Controller | Same file as Controller |
| **ResponseDTO** | Nested record in Controller | Same file as Controller |

---

## 10. Code Examples Summary

### Command Examples (5)
1. **UserCommands** - User lifecycle (create, activate, deactivate, lock, unlock)
2. **SpmCommands** - Hierarchical enrollment (profile → service → account)
3. **ApprovalWorkflowCommands** - Generic workflow engine
4. **PolicyCommands** - CRUD with conditional fields
5. **IndirectClientCommands** - Parent-child relationships

### Query Examples (5)
1. **UserQueries** - Flat summary with enum serialization
2. **SpmQueries** - Summary with aggregate counts
3. **ApprovalWorkflowQueries** - Progress indicators
4. **PolicyQueries** - Complete state snapshot
5. **IndirectClientQueries** - Related entity counts

### Application Service Examples (3)
1. **UserApplicationService** - In-memory event publisher
2. **SpmApplicationService** - Outbox event pattern
3. **IndirectClientApplicationService** - Sequence generation

### Controller Examples (3)
1. **UserCommandController** - Simple value object conversion
2. **SpmCommandController** - URN-based identifiers
3. **ApprovalWorkflowCommandController** - Generic resource pattern

### Aggregate Examples (3)
1. **User** - State machine with invariants
2. **ServicingProfile** - Entity collections with referential integrity
3. **ApprovalWorkflow** - Business rule engine (threshold logic)

### Event Examples (3)
1. **UserCreated** - Simple creation event
2. **ServicingProfileCreated** - Event with audit metadata
3. **WorkflowInitiated** - Event with configuration data

### Value Object Examples (3)
1. **UserId** - Simple UUID wrapper
2. **ClientId** - URN with regex validation
3. **ServicingProfileId** - Compound ID derived from ClientId

---

## 11. Recommendations for Schema Modeling

### 1. Command Schema Design

**Recommendation:** Model commands as nested within a `CommandInterface` schema, not standalone.

```yaml
# GOOD (matches Knight)
CommandInterface:
  name: UserCommands
  commands:
    - CreateUserCmd:
        parameters:
          - email: String
          - userType: String
          - identityProvider: String
          - clientId: ClientId
        returns: UserId

# NOT (doesn't match Knight)
Command:
  name: CreateUserCommand
  handler: UserCommandHandler
```

### 2. Application Service Schema

**Recommendation:** Application Service implements BOTH Commands AND Queries.

```yaml
ApplicationService:
  name: UserApplicationService
  implements:
    - UserCommands
    - UserQueries
  dependencies:
    - UserRepository
    - ApplicationEventPublisher
```

### 3. BFF/Controller Schema

**Recommendation:** Separate RequestDTO and ResponseDTO from API Command records.

```yaml
Controller:
  path: /commands/users
  endpoints:
    - CreateUser:
        httpMethod: POST
        path: /create
        requestDTO: CreateUserRequest  # Not CreateUserCmd
        responseDTO: CreateUserResult
        delegatesTo: UserCommands.createUser()
```

### 4. Event Publishing Schema

**Recommendation:** Events are published AFTER persistence, in same transaction.

```yaml
CommandHandler:
  transactionBoundary: REQUIRED
  steps:
    1. Load/Create Aggregate
    2. Invoke business logic
    3. Save to repository
    4. Publish event (same transaction)
```

### 5. Value Object Schema

**Recommendation:** Value Objects include URN serialization + parsing logic.

```yaml
ValueObject:
  name: ClientId
  urnFormat: "{system}:{clientNumber}"
  validation: "^(srf|gid|ind):[A-Za-z0-9_-]+$"
  methods:
    - of(String urn)
    - fromUrn(String urn)
    - system(): String
    - clientNumber(): String
```

---

## 12. Validation: Schema Concepts vs Reality

### ✅ Confirmed Patterns
- Commands as nested records in interfaces
- Application Service implements Commands + Queries
- Aggregates with private constructors + factory methods
- Value Objects with URN serialization
- Events as immutable records
- BFF controllers map HTTP → Commands
- Repository interfaces in app layer, impls in infra

### ❌ Mismatches Found
- **No separate Query controllers** (queries not exposed via REST in examples)
- **No CQRS read models** (queries use same database)
- **Event versioning not shown** (need schema evolution strategy)
- **No OpenAPI specs** (no `/openapi.yml` files found)

### 🔶 Gaps to Address
- **Validation annotations:** Not shown in command records (happens in domain)
- **Error handling:** Not shown in controllers (framework default)
- **Authentication/Authorization:** Not shown
- **API versioning:** Not evident in URLs
- **Multi-context aggregation:** No examples of BFF combining multiple contexts

---

## 13. Conclusion

The Knight codebase demonstrates **exceptionally clean DDD + CQRS + Hexagonal Architecture**:

1. **Clear layer separation:** API → App → Domain → Infra
2. **Consistent patterns:** Every context follows identical structure
3. **Type safety:** Value objects prevent primitive obsession
4. **Testability:** Pure domain logic, repository interfaces
5. **Event-driven:** Outbox pattern for reliable event publishing

**Key insight:** The Application Service is the **orchestration hub** that implements both Commands and Queries, manages transactions, and coordinates aggregate + repository + events.

The schemas should model this **service-centric architecture**, not a traditional CRUD/REST approach.
