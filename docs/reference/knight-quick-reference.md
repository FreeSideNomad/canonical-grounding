# Knight Architecture Quick Reference

## Pattern Cheat Sheet

### 🎯 Command Pattern
```java
// Location: {context}/api/.../commands/{Entity}Commands.java
public interface UserCommands {
    UserId createUser(CreateUserCmd cmd);
    record CreateUserCmd(String email, String userType, ClientId clientId) {}
}
```
**Key:** Interface + nested records | Immutable | Returns ID or void

---

### 🔍 Query Pattern
```java
// Location: {context}/api/.../queries/{Entity}Queries.java
public interface UserQueries {
    record UserSummary(String userId, String email, String status) {}
    UserSummary getUserSummary(UserId userId);
}
```
**Key:** Interface + result records | All strings (serialization) | No filtering

---

### ⚙️ Application Service Pattern
```java
// Location: {context}/app/.../service/{Entity}ApplicationService.java
@Singleton
public class UserApplicationService implements UserCommands, UserQueries {
    @Transactional
    public UserId createUser(CreateUserCmd cmd) {
        // 1. Generate ID
        // 2. Create aggregate
        // 3. Save
        // 4. Publish event
        return userId;
    }
}
```
**Key:** Implements Commands + Queries | @Transactional | Orchestrates aggregate + repo + events

---

### 🌐 BFF/Controller Pattern
```java
// Location: {context}/infra/.../rest/{Entity}CommandController.java
@Controller("/commands/users")
@ExecuteOn(TaskExecutors.BLOCKING)
public class UserCommandController {
    @Post("/create")
    public CreateUserResult createUser(@Body CreateUserRequest req) {
        var userId = commands.createUser(new UserCommands.CreateUserCmd(...));
        return new CreateUserResult(userId.id());
    }

    record CreateUserRequest(String email, String userType, String clientUrn) {}
    record CreateUserResult(String userId) {}
}
```
**Key:** All POST | URL: /commands/{context}/{action} | Separate DTOs from Commands

---

### 🏛️ Aggregate Pattern
```java
// Location: {context}/domain/.../aggregate/{Entity}.java
public class User {
    private final UserId userId;
    private Status status;

    private User(...) { /* private constructor */ }

    public static User create(...) {
        // Validation
        return new User(...);
    }

    public void activate() {
        // Business logic + invariants
        this.status = Status.ACTIVE;
    }
}
```
**Key:** Private constructor | Factory method | Business logic in methods | No infra dependencies

---

### 📢 Event Pattern
```java
// Location: {context}/api/.../events/{Event}.java
public record UserCreated(
    String userId,
    String email,
    Instant createdAt
) {}
```
**Key:** Record type | Past tense | All strings + timestamp | Published AFTER persistence

---

### 💎 Value Object Pattern
```java
// Location: platform/shared-kernel/.../sharedkernel/{Name}Id.java
public final class UserId {
    private final String id;

    private UserId(String id) { /* validate */ }

    public static UserId of(String id) {
        return new UserId(id);
    }

    public String id() { return id; }
}
```
**Key:** Final class | Factory method | Validation | URN format | equals/hashCode

---

## Architecture Layers

```
┌──────────────────────────────────────────┐
│ INFRA (Controllers, Repos, Kafka)       │
└──────────────────┬───────────────────────┘
                   │ implements
┌──────────────────▼───────────────────────┐
│ APP (Application Services)               │
│ - Implements Commands + Queries          │
│ - Defines Repository interfaces          │
│ - @Transactional boundaries              │
└──────────────────┬───────────────────────┘
                   │ uses
┌──────────────────▼───────────────────────┐
│ DOMAIN (Aggregates)                      │
│ - Pure business logic                    │
│ - No infrastructure dependencies         │
└──────────────────┬───────────────────────┘
                   │ uses
┌──────────────────▼───────────────────────┐
│ API (Commands, Queries, Events)          │
│ - Interfaces + Records                   │
│ - Published contract                     │
└──────────────────┬───────────────────────┘
                   │ uses
┌──────────────────▼───────────────────────┐
│ SHARED KERNEL (Value Objects)            │
└──────────────────────────────────────────┘
```

---

## File Organization per Bounded Context

```
{context}/
├── api/
│   ├── commands/{Entity}Commands.java
│   ├── queries/{Entity}Queries.java
│   └── events/{Event}.java
├── app/
│   └── service/{Entity}ApplicationService.java
├── domain/
│   └── aggregate/{Entity}.java
└── infra/
    ├── rest/{Entity}CommandController.java
    └── persistence/{Entity}RepositoryImpl.java
```

---

## Bounded Contexts Found

1. **users/users** - User lifecycle management
2. **users/policy** - Authorization policies
3. **service-profiles/management** - Servicing profile enrollment
4. **service-profiles/indirect-clients** - Indirect client onboarding
5. **approval-workflows/engine** - Generic approval workflows

---

## REST URL Conventions

```
POST /commands/users/create
POST /commands/users/activate
POST /commands/service-profiles/servicing/create
POST /commands/service-profiles/servicing/enroll-service
POST /commands/approval-workflows/initiate
POST /commands/approval-workflows/record-approval
```

**Pattern:** `/commands/{context}/{entity}/{action}` (all POST)

---

## Transaction & Event Flow

```
1. HTTP POST → Controller
2. Controller → Application Service
3. Application Service:
   a. @Transactional begin
   b. Load/Create Aggregate
   c. Aggregate.businessMethod()
   d. Repository.save()
   e. EventPublisher.publish() (same transaction)
   f. @Transactional commit
4. Return DTO
```

---

## Key Design Decisions

| Decision | Knight Choice |
|----------|---------------|
| Command structure | Interface + nested records |
| Query read model | Same database (no CQRS separation) |
| ID generation | Application Service (UUID) |
| Event publishing | After persistence, same transaction |
| HTTP verbs | POST for all commands |
| BFF scope | One controller per bounded context |
| Repository interface | Defined in app layer |
| Validation | Domain layer (aggregates) |
| DTO vs Command | Separate (Controller DTOs ≠ Command records) |

---

## Value Object Examples

```java
// Simple ID
UserId.of("123e4567-e89b-12d3-a456-426614174000")

// URN-based ID
ClientId.of("srf:12345")
  .system()       // → "srf"
  .clientNumber() // → "12345"

// Compound ID
ServicingProfileId.of(clientId)
  .urn()         // → "servicing:srf:12345"
  .clientId()    // → ClientId("srf:12345")

ServicingProfileId.fromUrn("servicing:srf:12345")
```

---

## Common Patterns

### Creation Command
```java
// Returns entity ID
UserId createUser(CreateUserCmd cmd);
```

### State Transition Command
```java
// Returns void
void activateUser(ActivateUserCmd cmd);
```

### Query
```java
// Returns DTO
UserSummary getUserSummary(UserId userId);
```

### Aggregate Factory
```java
public static User create(...) {
    // Validation
    return new User(...);
}
```

### Aggregate Mutation
```java
public void activate() {
    // Invariant check
    this.status = Status.ACTIVE;
}
```

---

## Code Snippets by Layer

### API Layer (Contracts)
```java
// Commands
public interface UserCommands {
    UserId createUser(CreateUserCmd cmd);
    record CreateUserCmd(String email, ClientId clientId) {}
}

// Queries
public interface UserQueries {
    record UserSummary(String userId, String email) {}
    UserSummary getUserSummary(UserId userId);
}

// Events
public record UserCreated(String userId, Instant createdAt) {}
```

### Application Layer (Orchestration)
```java
@Singleton
public class UserApplicationService implements UserCommands, UserQueries {
    private final UserRepository repository;
    private final ApplicationEventPublisher eventPublisher;

    @Transactional
    public UserId createUser(CreateUserCmd cmd) {
        UserId userId = UserId.of(UUID.randomUUID().toString());
        User user = User.create(userId, cmd.email());
        repository.save(user);
        eventPublisher.publishEvent(new UserCreated(userId.id(), Instant.now()));
        return userId;
    }

    public interface UserRepository {
        void save(User user);
        Optional<User> findById(UserId userId);
    }
}
```

### Domain Layer (Business Logic)
```java
public class User {
    private final UserId userId;
    private Status status;

    private User(UserId userId) {
        this.userId = userId;
        this.status = Status.PENDING;
    }

    public static User create(UserId userId, String email) {
        if (email == null || !email.contains("@")) {
            throw new IllegalArgumentException("Invalid email");
        }
        return new User(userId);
    }

    public void activate() {
        if (status == Status.LOCKED) {
            throw new IllegalStateException("Cannot activate locked user");
        }
        this.status = Status.ACTIVE;
    }
}
```

### Infrastructure Layer (Adapters)
```java
@Controller("/commands/users")
@ExecuteOn(TaskExecutors.BLOCKING)
public class UserCommandController {
    @Inject UserCommands commands;

    @Post("/create")
    public CreateUserResult createUser(@Body CreateUserRequest req) {
        var userId = commands.createUser(new UserCommands.CreateUserCmd(
            req.email(), ClientId.of(req.clientUrn())
        ));
        return new CreateUserResult(userId.id());
    }

    record CreateUserRequest(String email, String clientUrn) {}
    record CreateUserResult(String userId) {}
}
```

---

## Files Analyzed (Total: 30+)

### Commands
- `/Users/igor/code/knight/contexts/users/users/api/.../UserCommands.java`
- `/Users/igor/code/knight/contexts/service-profiles/management/api/.../SpmCommands.java`
- `/Users/igor/code/knight/contexts/approval-workflows/engine/api/.../ApprovalWorkflowCommands.java`
- `/Users/igor/code/knight/contexts/users/policy/api/.../PolicyCommands.java`
- `/Users/igor/code/knight/contexts/service-profiles/indirect-clients/api/.../IndirectClientCommands.java`

### Queries
- `/Users/igor/code/knight/contexts/users/users/api/.../UserQueries.java`
- `/Users/igor/code/knight/contexts/service-profiles/management/api/.../SpmQueries.java`
- `/Users/igor/code/knight/contexts/approval-workflows/engine/api/.../ApprovalWorkflowQueries.java`
- `/Users/igor/code/knight/contexts/users/policy/api/.../PolicyQueries.java`
- `/Users/igor/code/knight/contexts/service-profiles/indirect-clients/api/.../IndirectClientQueries.java`

### Application Services
- `/Users/igor/code/knight/contexts/users/users/app/.../UserApplicationService.java`
- `/Users/igor/code/knight/contexts/service-profiles/management/app/.../SpmApplicationService.java`
- `/Users/igor/code/knight/contexts/approval-workflows/engine/app/.../ApprovalWorkflowApplicationService.java`
- `/Users/igor/code/knight/contexts/users/policy/app/.../PolicyApplicationService.java`
- `/Users/igor/code/knight/contexts/service-profiles/indirect-clients/app/.../IndirectClientApplicationService.java`

### Controllers
- `/Users/igor/code/knight/contexts/users/users/infra/.../UserCommandController.java`
- `/Users/igor/code/knight/contexts/service-profiles/management/infra/.../SpmCommandController.java`
- `/Users/igor/code/knight/contexts/approval-workflows/engine/infra/.../ApprovalWorkflowCommandController.java`
- `/Users/igor/code/knight/contexts/users/policy/infra/.../PolicyCommandController.java`
- `/Users/igor/code/knight/contexts/service-profiles/indirect-clients/infra/.../IndirectClientCommandController.java`

### Aggregates
- `/Users/igor/code/knight/contexts/users/users/domain/.../User.java`
- `/Users/igor/code/knight/contexts/service-profiles/management/domain/.../ServicingProfile.java`
- `/Users/igor/code/knight/contexts/approval-workflows/engine/domain/.../ApprovalWorkflow.java`
- `/Users/igor/code/knight/contexts/users/policy/domain/.../Policy.java`

### Events
- `/Users/igor/code/knight/contexts/users/users/api/.../UserCreated.java`
- `/Users/igor/code/knight/contexts/service-profiles/management/api/.../ServicingProfileCreated.java`
- `/Users/igor/code/knight/contexts/approval-workflows/engine/api/.../WorkflowInitiated.java`

### Value Objects
- `/Users/igor/code/knight/platform/shared-kernel/.../UserId.java`
- `/Users/igor/code/knight/platform/shared-kernel/.../ClientId.java`
- `/Users/igor/code/knight/platform/shared-kernel/.../ServicingProfileId.java`
