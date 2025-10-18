# DDD-07: Application Layer in Domain-Driven Design

**Version:** 1.0.0
**Status:** final
**Last Updated:** 2025-10-18
**Part of:** DDD Documentation Series

---

## Table of Contents

1. [Overview](#1-overview)
2. [Application Layer Position](#2-application-layer-position)
3. [Application Service Pattern](#3-application-service-pattern)
4. [Command/Query Separation (CQRS)](#4-commandquery-separation-cqrs)
5. [Transaction Boundaries](#5-transaction-boundaries)
6. [Integration with Tactical Patterns](#6-integration-with-tactical-patterns)
7. [Examples from Knight Codebase](#7-examples-from-knight-codebase)
8. [Best Practices](#8-best-practices)
9. [Anti-Patterns to Avoid](#9-anti-patterns-to-avoid)
10. [References](#10-references)

---

## 1. Overview

The **Application Layer** is a critical architectural layer in Domain-Driven Design that sits between the User Interface and the Domain Layer. Its primary responsibility is to orchestrate use case execution without containing business logic.

### 1.1 Definition

> "Defines an application's boundary with a layer of services that establishes a set of available operations and coordinates the application's response in each operation."
> — Martin Fowler, *Patterns of Enterprise Application Architecture*

### 1.2 Alternative Names

- **Application Layer** (Eric Evans, *DDD Blue Book*)
- **Service Layer** (Martin Fowler, *PoEAA*)
- **Use Case Layer** (Clean Architecture)
- **Command/Query Handlers** (CQRS architecture)

### 1.3 Key Characteristics

| Characteristic | Description |
|---------------|-------------|
| **Stateless** | Holds no domain state between operations |
| **Thin** | Contains no business logic, only orchestration |
| **Coordinates** | Orchestrates domain objects and domain services |
| **Transaction Boundary** | Manages database transactions |
| **Use Case Focused** | One operation per use case |
| **External Interface** | API exposed to external clients |

---

## 2. Application Layer Position

### 2.1 Eric Evans' Four-Layer Architecture

```
┌─────────────────────────────────────────────────┐
│   User Interface Layer                          │
│   (Presentation, UI Controls, REST APIs)        │
├─────────────────────────────────────────────────┤
│   APPLICATION LAYER ← THIS LAYER                │
│   (Application Services, Use Case Orchestration)│
├─────────────────────────────────────────────────┤
│   Domain Layer                                  │
│   (Entities, Value Objects, Domain Services)    │
├─────────────────────────────────────────────────┤
│   Infrastructure Layer                          │
│   (Persistence, External Services, Messaging)   │
└─────────────────────────────────────────────────┘
```

### 2.2 Application Layer Responsibilities

**What the Application Layer DOES:**
- Defines jobs the software is supposed to do
- Directs domain objects to work out problems
- Coordinates domain layer objects to perform actual work
- Manages transaction boundaries
- Publishes domain events
- Performs security and authorization checks
- Validates input format and required fields

**What the Application Layer DOES NOT DO:**
- Contain business logic (belongs in Domain Layer)
- Make business decisions (delegates to domain)
- Directly access infrastructure (uses interfaces)
- Maintain state between operations

### 2.3 Dependency Direction

```
UI Layer → Application Layer → Domain Layer
```

Dependencies flow in **one direction**:
- User Interface depends on Application Layer
- Application Layer depends on Domain Layer
- Domain Layer is independent (core of the system)

---

## 3. Application Service Pattern

### 3.1 What is an Application Service?

An **Application Service** is a stateless object that orchestrates use case execution by:
1. Fetching domain objects from repositories
2. Executing domain operations on aggregates
3. Persisting changes back to repositories
4. Managing transaction boundaries
5. Publishing domain events to external systems

### 3.2 Application Service vs Domain Service

This distinction is critical in DDD:

| Aspect | Application Service | Domain Service |
|--------|-------------------|----------------|
| **Business Logic** | None | Contains domain logic |
| **Transaction Management** | Yes | No |
| **Repository Access** | Yes | No |
| **External Dependencies** | Yes (repos, infrastructure) | No |
| **Parameters/Return Types** | DTOs, primitives | Domain objects |
| **Called By** | UI, API controllers, BFFs | Application services, other domain services |
| **Validation** | Input format validation | Business rule validation |
| **Ubiquitous Language** | Use case names | Domain concept names |
| **Example** | `RegisterUserApplicationService` | `UserAuthenticationDomainService` |

#### 3.2.1 Application Service Example

```java
@Singleton
public class UserApplicationService {
    private final UserRepository repository;
    private final ApplicationEventPublisher eventPublisher;

    @Transactional
    public UserId createUser(CreateUserCmd cmd) {
        // 1. Validate input format
        if (cmd.email() == null || !cmd.email().contains("@")) {
            throw new ValidationException("Invalid email format");
        }

        // 2. Create aggregate (business logic in aggregate)
        UserId userId = UserId.of(UUID.randomUUID().toString());
        User user = User.create(userId, cmd.email(), cmd.userType());

        // 3. Persist
        repository.save(user);

        // 4. Publish event
        eventPublisher.publishEvent(new UserCreated(userId));

        // 5. Return domain ID
        return userId;
    }
}
```

#### 3.2.2 Domain Service Example

```java
public class UserAuthenticationDomainService {

    // Business logic for authentication spanning multiple domain concepts
    public boolean authenticate(User user, Password password,
                               SecurityPolicy policy) {
        // Domain logic: check password strength
        if (!policy.meetsRequirements(password)) {
            return false;
        }

        // Domain logic: verify credentials
        boolean valid = user.verifyPassword(password);

        // Domain logic: update authentication metadata
        if (valid) {
            user.recordSuccessfulLogin();
        } else {
            user.recordFailedLoginAttempt();
        }

        return valid;
    }
}
```

### 3.3 Granularity and Operations

**Principle:** One application service method = One use case

#### Good Examples (Fine-Grained, Use Case Aligned)
```java
public interface UserCommands {
    UserId createUser(CreateUserCmd cmd);
    void activateUser(ActivateUserCmd cmd);
    void deactivateUser(DeactivateUserCmd cmd);
    void lockUser(LockUserCmd cmd);
    void unlockUser(UnlockUserCmd cmd);
}
```

#### Bad Example (Too Generic)
```java
// Anti-pattern: Generic method handling multiple use cases
public void manageUser(String action, UserData data) {
    // Violates single responsibility principle
}
```

### 3.4 What Belongs in Application Service Operations

**✓ INCLUDE:**
- Fetching aggregates from repositories
- Executing domain operations
- Persisting changes
- Publishing domain events
- Transaction management
- Security/authorization checks
- Input validation (format, nullability, required fields)
- Coordinating multiple domain service calls
- Converting domain objects to DTOs for return

**✗ EXCLUDE:**
- Business logic calculations
- Domain rule enforcement (delegate to domain)
- Direct database queries (use repositories)
- External service integration (use domain/infrastructure services)
- UI concerns (formatting, presentation logic)

### 3.5 Validation in Application Services

**Two-Level Validation Strategy:**

#### Level 1: Application Service - Input Validation
- Format validation (email format, date format)
- Required field validation
- Data type validation
- Lookup validation (checking reference data exists)
- **Action:** Throws exceptions if validation fails
- **Tool:** JSR-303, custom validators

#### Level 2: Domain Level - Business Rule Validation
- Business invariant enforcement
- Complex domain rules
- Cross-entity validation
- **Action:** Domain returns result indicating success/failure with reasons
- **Location:** Domain aggregates and domain services

**Example Flow:**
```java
@Transactional
public void placeOrder(PlaceOrderCmd cmd) {
    // 1. Application-level input validation
    if (cmd.items().isEmpty()) {
        throw new ValidationException("Order must have at least one item");
    }

    // 2. Load aggregate
    Order order = Order.create(cmd.orderId(), cmd.customerId());

    // 3. Invoke domain operation (domain validates business rules)
    Result result = order.addItems(cmd.items());

    // 4. Check business rule validation result
    if (!result.isSuccess()) {
        throw new BusinessRuleViolationException(result.getErrors());
    }

    // 5. Persist and commit
    repository.save(order);
}
```

---

## 4. Command/Query Separation (CQRS)

### 4.1 Pattern Definition

> "Use a different model to update information than the model you use to read information."
> — Martin Fowler

**CQRS** (Command Query Responsibility Segregation) extends the Command-Query Separation (CQS) principle:
- **CQS:** Methods are either commands (change state) or queries (return data)
- **CQRS:** Separate **object models** for commands and queries

### 4.2 Commands vs Queries

| Aspect | Commands | Queries |
|--------|---------|---------|
| **Purpose** | Change state | Retrieve data |
| **Side Effects** | Yes - modifies data | No - read-only |
| **Return Value** | void / result status | Business data |
| **Naming** | Imperative verbs (PlaceOrder, CancelOrder) | Query verbs (GetOrder, ListOrders) |
| **Validation** | Business rules enforced | Input parameter validation only |
| **Model Used** | Write model (domain model) | Read model (query model) |
| **Optimization** | Consistency, integrity | Performance, denormalization |
| **Database** | Write database | Read database (potentially separate) |
| **Example** | `PlaceOrder`, `CancelOrder` | `GetOrderDetails`, `ListOrders` |

### 4.3 Command Pattern

**Characteristics:**
- Represent user **intent** or **actions**
- Named with imperative verbs
- Contain all data needed to perform operation
- Return void, acknowledgment, or operation result (not business data)
- Processed through **write model**
- Validate business rules
- Enforce invariants
- Modify aggregates
- Publish domain events

**Command Structure (Knight Pattern):**
```java
public interface OrderCommands {

    OrderId placeOrder(PlaceOrderCmd cmd);

    record PlaceOrderCmd(
        CustomerId customerId,
        List<OrderItem> items,
        Address shippingAddress
    ) {}

    void cancelOrder(CancelOrderCmd cmd);

    record CancelOrderCmd(
        OrderId orderId,
        String reason
    ) {}
}
```

### 4.4 Query Pattern

**Characteristics:**
- Named with query verbs (Get, List, Find, Search)
- Return **data** (DTOs, view models)
- NO side effects - do not modify state
- Processed through **read model**
- Optimized for specific views
- May bypass domain model entirely
- Can use denormalized data structures
- May read from separate read database

**Query Structure (Knight Pattern):**
```java
public interface OrderQueries {

    record OrderSummary(
        String orderId,
        String customerId,
        String status,
        int itemCount,
        BigDecimal totalAmount
    ) {}

    OrderSummary getOrderSummary(OrderId orderId);

    List<OrderSummary> listOrders(OrderFilter filter);
}
```

### 4.5 When to Use CQRS vs Simple CRUD

#### Use CQRS When:
1. **Complex Domains** - Significant differences between read and write operations
2. **Performance Requirements** - High read-to-write ratio, need independent scaling
3. **Collaborative Domains** - Multiple users operating on same data
4. **Event-Driven Architecture** - Already using Event Sourcing
5. **Specific Bounded Contexts** - Apply to portions of system, not entire system

#### Do NOT Use CQRS When:
1. **Simple CRUD Applications** - Straightforward create/read/update/delete operations
2. **Low Complexity Domains** - No significant difference between read and write needs
3. **Small Systems** - Complexity overhead not justified
4. **Starting New Projects** - Begin simpler, add CQRS later if needed

**Martin Fowler's Caution:**
> "You should be very cautious about using CQRS. Many information systems fit well with the notion of an information base that is updated in the same way that it's read, adding CQRS to such a system can add significant complexity."

### 4.6 Knight Codebase Pattern: Commands as Nested Records

The Knight codebase demonstrates a particularly elegant pattern:

**Commands Interface:**
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
}
```

**Application Service Implementation:**
```java
@Singleton
public class UserApplicationService implements UserCommands, UserQueries {

    @Override
    @Transactional
    public UserId createUser(CreateUserCmd cmd) {
        // Implementation
    }

    @Override
    @Transactional
    public void activateUser(ActivateUserCmd cmd) {
        // Implementation
    }

    @Override
    public UserSummary getUserSummary(UserId userId) {
        // Implementation
    }
}
```

**Key Benefits:**
- Immutable command objects (records are final)
- Type-safe parameters
- Clear intent (one command per operation)
- Minimal boilerplate
- Grouped by aggregate root

---

## 5. Transaction Boundaries

### 5.1 Fundamental Rule

> "Modify only ONE aggregate instance per transaction"
> — Vaughn Vernon, *Implementing Domain-Driven Design*

### 5.2 One Aggregate Per Transaction

**Transaction Management Principles:**

1. **Single Aggregate Rule**
   - Application service method runs inside a transaction
   - Load one aggregate root from repository
   - Execute operations on that aggregate
   - Persist changes
   - Commit transaction

2. **Transaction Flow:**
```
Application Service Method {
  BEGIN TRANSACTION
    1. Load Aggregate from Repository
    2. Execute Domain Operation on Aggregate
    3. Save Aggregate to Repository
    4. Publish Domain Events (if any)
  COMMIT TRANSACTION
}
```

3. **Example:**
```java
@Transactional
public void approveOrder(ApproveOrderCmd cmd) {
    // BEGIN TRANSACTION (managed by framework)

    // 1. Load ONE aggregate
    Order order = orderRepository.findById(cmd.orderId())
        .orElseThrow(() -> new OrderNotFoundException(cmd.orderId()));

    // 2. Execute domain operation
    order.approve(cmd.approvedBy());

    // 3. Save aggregate
    orderRepository.save(order);

    // 4. Publish event
    eventPublisher.publishEvent(new OrderApproved(order.getId()));

    // COMMIT TRANSACTION
}
```

### 5.3 Multi-Aggregate Coordination via Eventual Consistency

**Problem:** What if a use case needs to modify multiple aggregates?

**Solution:** Use **eventual consistency** via domain events

**Pattern:**
```
// Command Handler - Transaction 1
Application Service: ApproveInvoiceCommandHandler

BEGIN TRANSACTION
  invoice = invoiceRepository.load(invoiceId)
  invoice.approve(approvedBy)
  invoiceRepository.save(invoice)
  events = invoice.getDomainEvents()  // InvoiceApproved
COMMIT TRANSACTION

eventPublisher.publish(events)

// Event Handler - Transaction 2 (separate)
ON EVENT InvoiceApproved
  BEGIN TRANSACTION
    account = accountRepository.load(event.accountId)
    account.recordPayment(event.amount)
    accountRepository.save(account)
  COMMIT TRANSACTION
```

### 5.4 Sagas for Complex Workflows

For long-running processes spanning multiple aggregates, use the **Saga Pattern**:

```
OrderSaga coordinating Order, Inventory, Payment, Shipping

Step 1: Create Order
  BEGIN TRANSACTION
    order = Order.create()
    orderRepository.save(order)
  COMMIT
  PUBLISH OrderCreated

Step 2: Reserve Inventory (event handler)
  ON EVENT OrderCreated
    BEGIN TRANSACTION
      inventory.reserve(items)
      inventoryRepository.save(inventory)
    COMMIT
    PUBLISH InventoryReserved

Step 3: Process Payment (event handler)
  ON EVENT InventoryReserved
    BEGIN TRANSACTION
      payment.process(amount)
      paymentRepository.save(payment)
    COMMIT
    PUBLISH PaymentProcessed (or PaymentFailed)

Step 4: Complete Order (event handler)
  ON EVENT PaymentProcessed
    BEGIN TRANSACTION
      order.complete()
      orderRepository.save(order)
    COMMIT
    PUBLISH OrderCompleted

// Compensation on failure
  ON EVENT PaymentFailed
    BEGIN TRANSACTION
      inventory.release(items)
      inventoryRepository.save(inventory)
    COMMIT
    BEGIN TRANSACTION
      order.cancel()
      orderRepository.save(order)
    COMMIT
```

### 5.5 Consistency Boundaries

**Two Types:**

1. **Transactional Consistency** (Immediate, Atomic)
   - Within one aggregate
   - ACID guarantees
   - Enforced immediately
   - Example: Order total must equal sum of line items

2. **Eventual Consistency** (Deferred)
   - Between aggregates
   - Achieved asynchronously via events
   - Temporary inconsistency acceptable
   - Example: Inventory adjusted after order placed

**Determining Which to Use:**

Ask these questions:
- Is it the user's job to make data consistent in this use case? → Transactional
- Can consistency be achieved asynchronously? → Eventual
- Must invariant be enforced immediately? → Transactional (true invariant)
- Can the business tolerate a delay? → Eventual

### 5.6 Event Publishing Pattern

**Domain events are published AFTER successful transaction commit:**

```java
@Transactional
public OrderId placeOrder(PlaceOrderCmd cmd) {
    BEGIN TRANSACTION
      // 1. Create aggregate
      Order order = Order.create(cmd.orderId(), cmd.customerId());

      // 2. Execute domain operations
      order.addItems(cmd.items());

      // 3. Persist aggregate
      orderRepository.save(order);

      // 4. Collect domain events from aggregate
      List<DomainEvent> events = order.getDomainEvents();
    COMMIT TRANSACTION

    // 5. Publish events AFTER transaction commit
    for (DomainEvent event : events) {
        eventPublisher.publish(event);
    }

    return order.getId();
}
```

**Key Principles:**
- Events published AFTER successful transaction commit
- Events represent facts that have occurred
- Events are immutable
- Event names are past-tense verbs (OrderPlaced, InvoiceApproved)
- Events contain data needed by subscribers

---

## 6. Integration with Tactical Patterns

### 6.1 Relationship to Aggregates

**Application Services coordinate Aggregates:**

```
Application Service
    ↓ loads/saves
Repository
    ↓ persists/retrieves
Aggregate Root
    ↓ contains
Entities + Value Objects
```

**Example:**
```java
@Transactional
public void enrollService(EnrollServiceCmd cmd) {
    // Load aggregate via repository
    ServicingProfile profile = repository.findById(cmd.profileId())
        .orElseThrow(() -> new NotFoundException());

    // Delegate to aggregate for business logic
    profile.enrollService(cmd.serviceType(), cmd.configuration());

    // Save aggregate via repository
    repository.save(profile);
}
```

### 6.2 Relationship to Repositories

**Repository Pattern Integration:**

**Interface Defined in Application Layer:**
```java
public class UserApplicationService {

    // Repository interface defined in application layer
    public interface UserRepository {
        void save(User user);
        Optional<User> findById(UserId userId);
    }

    private final UserRepository repository;

    // Application service uses repository interface
    @Transactional
    public void activateUser(ActivateUserCmd cmd) {
        User user = repository.findById(cmd.userId())
            .orElseThrow(() -> new UserNotFoundException());
        user.activate();
        repository.save(user);
    }
}
```

**Implementation in Infrastructure Layer:**
```java
@Singleton
public class JpaUserRepository implements UserApplicationService.UserRepository {

    @Override
    public void save(User user) {
        // JPA implementation
    }

    @Override
    public Optional<User> findById(UserId userId) {
        // JPA implementation
    }
}
```

### 6.3 Relationship to Domain Events

**Application Services publish Domain Events:**

**Event Definition (API Layer):**
```java
public record OrderPlaced(
    String orderId,
    String customerId,
    Instant placedAt
) {}
```

**Application Service publishes event:**
```java
@Transactional
public OrderId placeOrder(PlaceOrderCmd cmd) {
    Order order = Order.create(cmd.orderId(), cmd.customerId());
    order.addItems(cmd.items());

    repository.save(order);

    // Publish domain event
    eventPublisher.publishEvent(new OrderPlaced(
        order.getId().value(),
        order.getCustomerId().value(),
        Instant.now()
    ));

    return order.getId();
}
```

---

## 7. Examples from Knight Codebase

### 7.1 UserApplicationService

**Complete example showing all patterns:**

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
        // 1. Generate domain ID
        UserId userId = UserId.of(UUID.randomUUID().toString());

        // 2. Parse enums (input validation)
        User.UserType userType = User.UserType.valueOf(cmd.userType());
        User.IdentityProvider identityProvider =
            User.IdentityProvider.valueOf(cmd.identityProvider());

        // 3. Create aggregate (business logic in aggregate)
        User user = User.create(
            userId,
            cmd.email(),
            userType,
            identityProvider,
            cmd.clientId()
        );

        // 4. Save aggregate
        repository.save(user);

        // 5. Publish event (after persistence)
        eventPublisher.publishEvent(new UserCreated(
            userId.id(),
            cmd.email(),
            cmd.userType(),
            cmd.identityProvider(),
            Instant.now()
        ));

        // 6. Return domain ID
        return userId;
    }

    @Override
    @Transactional
    public void activateUser(ActivateUserCmd cmd) {
        // 1. Load aggregate
        User user = repository.findById(cmd.userId())
            .orElseThrow(() -> new IllegalArgumentException(
                "User not found: " + cmd.userId().id()));

        // 2. Execute domain operation
        user.activate();

        // 3. Save aggregate
        repository.save(user);

        // 4. Publish event
        eventPublisher.publishEvent(new UserActivated(
            user.getUserId().id(),
            Instant.now()
        ));
    }

    @Override
    public UserSummary getUserSummary(UserId userId) {
        // 1. Load aggregate
        User user = repository.findById(userId)
            .orElseThrow(() -> new IllegalArgumentException(
                "User not found: " + userId.id()));

        // 2. Map domain aggregate to DTO
        return new UserSummary(
            user.getUserId().id(),
            user.getEmail(),
            user.getStatus().name(),
            user.getUserType().name(),
            user.getIdentityProvider().name()
        );
    }

    // Repository interface (inner interface pattern)
    public interface UserRepository {
        void save(User user);
        Optional<User> findById(UserId userId);
    }
}
```

### 7.2 Command/Query Interfaces

**UserCommands Interface:**
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

**UserQueries Interface:**
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

---

## 8. Best Practices

### 8.1 Application Service Design

1. **Keep it Thin**
   - No business logic
   - Only orchestration and coordination
   - Delegate to domain for business rules

2. **One Method Per Use Case**
   - Each method represents one business operation
   - Clear, descriptive names (createUser, placeOrder, approveInvoice)
   - Avoid generic methods handling multiple use cases

3. **Stateless Always**
   - Application services must not maintain state between calls
   - All needed data passed via method parameters
   - Use dependency injection for infrastructure dependencies

4. **Transaction Boundary = Method Boundary**
   - Each method defines one transaction
   - @Transactional annotation on command methods
   - No transactions for query methods

5. **ID Generation**
   - Generate domain IDs in application service (not database)
   - Use UUID or domain-specific ID generation strategy
   - Return domain IDs for creation operations

### 8.2 Command Design

1. **Immutable Commands**
   - Use record types or final fields
   - Commands represent intent, should not be modified

2. **Imperative Verb Naming**
   - CreateUser, PlaceOrder, CancelOrder, ApproveInvoice
   - Captures business intent clearly

3. **Include Audit Fields**
   - Who performed the action (initiatedBy, approvedBy)
   - Why the action was taken (reason, comments)
   - When it happened (timestamp)

4. **Return Types**
   - Creation commands: Return domain ID (UserId, OrderId)
   - State transitions: Return void
   - Async operations: Return acknowledgment

### 8.3 Query Design

1. **No Side Effects**
   - Queries must be read-only
   - Never modify state in a query

2. **Return DTOs, Not Aggregates**
   - Serialize complex types to strings
   - Use flat structure (no nested objects)
   - Return aggregate counts, not full collections

3. **Query-Specific Optimization**
   - Use denormalized read models where beneficial
   - Apply caching strategies
   - Consider separate read database for high-volume reads

### 8.4 Validation Strategy

1. **Two-Level Validation**
   - **Application Layer:** Input format, required fields, data types
   - **Domain Layer:** Business rules, invariants, complex validations

2. **Fail Fast**
   - Validate input at application layer before calling domain
   - Throw exceptions for format validation failures
   - Return result objects for business rule violations

### 8.5 Event Publishing

1. **Publish After Success**
   - Events only published after successful transaction commit
   - Events represent facts that have occurred
   - Never publish events for failed operations

2. **Event Naming**
   - Past-tense verbs (UserCreated, OrderPlaced, InvoiceApproved)
   - Include essential data for subscribers
   - Immutable event objects

3. **Event Handling Patterns**
   - In-memory event bus for local subscribers
   - Outbox pattern for guaranteed delivery
   - Kafka/message queue for distributed systems

---

## 9. Anti-Patterns to Avoid

### 9.1 Business Logic in Application Service

**❌ Anti-Pattern:**
```java
@Transactional
public void placeOrder(PlaceOrderCmd cmd) {
    Order order = new Order(cmd.orderId());

    // WRONG: Business logic in application service
    BigDecimal total = BigDecimal.ZERO;
    for (OrderItem item : cmd.items()) {
        BigDecimal lineTotal = item.quantity()
            .multiply(item.unitPrice());
        total = total.add(lineTotal);
    }
    order.setTotal(total);

    repository.save(order);
}
```

**✓ Correct Pattern:**
```java
@Transactional
public void placeOrder(PlaceOrderCmd cmd) {
    Order order = Order.create(cmd.orderId());

    // Business logic delegated to aggregate
    order.addItems(cmd.items());

    repository.save(order);
}
```

### 9.2 Modifying Multiple Aggregates in One Transaction

**❌ Anti-Pattern:**
```java
@Transactional
public void processOrder(ProcessOrderCmd cmd) {
    // WRONG: Modifying multiple aggregates in one transaction
    Order order = orderRepository.findById(cmd.orderId());
    order.confirm();
    orderRepository.save(order);

    Inventory inventory = inventoryRepository.findById(cmd.warehouseId());
    inventory.reserve(order.getItems());
    inventoryRepository.save(inventory);
}
```

**✓ Correct Pattern:**
```java
@Transactional
public void confirmOrder(ConfirmOrderCmd cmd) {
    Order order = orderRepository.findById(cmd.orderId());
    order.confirm();
    orderRepository.save(order);

    // Publish event for eventual consistency
    eventPublisher.publishEvent(new OrderConfirmed(order.getId()));
}

// Separate event handler
@EventListener
@Transactional
public void onOrderConfirmed(OrderConfirmed event) {
    Inventory inventory = inventoryRepository.findById(event.warehouseId());
    inventory.reserve(event.items());
    inventoryRepository.save(inventory);
}
```

### 9.3 Generic Application Service Methods

**❌ Anti-Pattern:**
```java
// WRONG: Generic method handling multiple operations
public void updateUser(String action, Map<String, Object> data) {
    switch (action) {
        case "activate": // ...
        case "deactivate": // ...
        case "lock": // ...
    }
}
```

**✓ Correct Pattern:**
```java
// Specific methods for each use case
public void activateUser(ActivateUserCmd cmd) { }
public void deactivateUser(DeactivateUserCmd cmd) { }
public void lockUser(LockUserCmd cmd) { }
```

### 9.4 Anemic Domain Model

**❌ Anti-Pattern:**
```java
// Anemic aggregate with only getters/setters
public class Order {
    private OrderId id;
    private BigDecimal total;

    public void setTotal(BigDecimal total) { this.total = total; }
    public BigDecimal getTotal() { return total; }
}

// Application service contains business logic (WRONG)
@Transactional
public void placeOrder(PlaceOrderCmd cmd) {
    Order order = new Order();
    order.setId(cmd.orderId());

    // Business logic here (should be in aggregate)
    BigDecimal total = calculateTotal(cmd.items());
    order.setTotal(total);

    repository.save(order);
}
```

**✓ Correct Pattern:**
```java
// Rich domain model with behavior
public class Order {
    private final OrderId id;
    private BigDecimal total;
    private List<OrderItem> items;

    // Business logic in aggregate
    public void addItems(List<OrderItem> items) {
        this.items.addAll(items);
        this.total = calculateTotal();
    }

    private BigDecimal calculateTotal() {
        return items.stream()
            .map(item -> item.quantity().multiply(item.unitPrice()))
            .reduce(BigDecimal.ZERO, BigDecimal::add);
    }
}

// Application service orchestrates (thin)
@Transactional
public void placeOrder(PlaceOrderCmd cmd) {
    Order order = Order.create(cmd.orderId());
    order.addItems(cmd.items());  // Business logic in aggregate
    repository.save(order);
}
```

### 9.5 Direct Database Access in Application Service

**❌ Anti-Pattern:**
```java
@Transactional
public void createUser(CreateUserCmd cmd) {
    // WRONG: Direct SQL in application service
    String sql = "INSERT INTO users (id, email, status) VALUES (?, ?, ?)";
    jdbcTemplate.update(sql, cmd.userId(), cmd.email(), "ACTIVE");
}
```

**✓ Correct Pattern:**
```java
@Transactional
public void createUser(CreateUserCmd cmd) {
    User user = User.create(cmd.userId(), cmd.email());
    repository.save(user);  // Repository abstracts persistence
}
```

---

## 10. References

### Primary Sources

1. **Fowler, Martin.** "Service Layer". *Patterns of Enterprise Application Architecture Catalog*.
   https://martinfowler.com/eaaCatalog/serviceLayer.html

2. **Fowler, Martin.** *Patterns of Enterprise Application Architecture*. Addison-Wesley Professional, 2002.

3. **Evans, Eric.** *Domain-Driven Design: Tackling Complexity in the Heart of Software*. Addison-Wesley Professional, 2003.

4. **Vernon, Vaughn.** *Implementing Domain-Driven Design*. Addison-Wesley Professional, 2013.

5. **Fowler, Martin.** "CQRS". Martin Fowler's Bliki.
   https://martinfowler.com/bliki/CQRS.html

6. **Young, Greg.** "CQRS Documents".
   https://cqrs.files.wordpress.com/2010/11/cqrs_documents.pdf

7. **Microsoft Azure Architecture Center.** "Command and Query Responsibility Segregation (CQRS) Pattern".
   https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs

### Supporting Research

8. **Gorodinski, Lev.** "Services in Domain-Driven Design (DDD)". April 14, 2012.
   http://gorodinski.com/blog/2012/04/14/services-in-domain-driven-design-ddd/

9. **Xebia.** "Domain-Driven Design Part 2 - Application Services And Domain Services".
   https://xebia.com/blog/domain-driven-design-part-2-application-services-and-domain-services/

10. **Enterprise Craftsmanship.** "Domain services vs Application services".
    https://enterprisecraftsmanship.com/posts/domain-vs-application-services/

### Internal References

- [DDD-01: DDD Foundations](ddd-01-ddd-foundations.md)
- [DDD-03: Tactical Patterns](ddd-03-tactical-patterns.md)
- [DDD-05: PoEAA Integration](ddd-05-poeaa-integration.md)
- [DDD-08: BFF Pattern](ddd-08-bff-pattern.md)

---

**Document Control:**
- Version: 1.0.0
- Status: final
- Last Updated: 2025-10-18
- Approved By: DDD Documentation Team
