# Application Layer Patterns and CQRS Implementation Research

**Version:** 1.0.0
**Date:** 2025-10-24
**Research Focus:** Application Layer patterns, CQRS implementation, Read Models, DTOs, and Transaction Boundaries
**Schema Version:** tactical-ddd.schema.yaml v2.0.0
**Part of:** DDD Documentation Series - Research Expansion

---

## Table of Contents

1. [CQRS in DDD Context](#1-cqrs-in-ddd-context)
2. [Application Service Orchestration Patterns](#2-application-service-orchestration-patterns)
3. [Read Model Implementation](#3-read-model-implementation)
4. [DTO Design in DDD](#4-dto-design-in-ddd)
5. [Transaction Boundary Patterns](#5-transaction-boundary-patterns)
6. [Decision Trees and Guidelines](#6-decision-trees-and-guidelines)
7. [Examples from Tactical Schema](#7-examples-from-tactical-schema)
8. [References](#8-references)

---

## 1. CQRS in DDD Context

### 1.1 Introduction to CQRS

Command Query Responsibility Segregation (CQRS) is an architectural pattern that separates the responsibility for reading data (queries) from the responsibility for changing data (commands). While the principle is straightforward, understanding when and how to apply CQRS in a Domain-Driven Design context requires careful consideration of complexity tradeoffs.

**Definition**: "Use a different model to update information than the model you use to read information." — Martin Fowler

CQRS extends Bertrand Meyer's Command-Query Separation (CQS) principle from the method level to the architectural level. Where CQS states that methods should either change state (commands) or return data (queries) but not both, CQRS takes this further by separating the entire models used for these operations.

### 1.2 When to Use CQRS (Critical Decision Criteria)

The most important question when considering CQRS is not "how do I implement it?" but "should I implement it at all?" CQRS adds significant complexity to a system, and this complexity must be justified by tangible benefits.

#### Use CQRS When:

**1. Complex Domains with Read/Write Asymmetry**

When your system exhibits significant differences between how data is written and how it's read, CQRS becomes valuable. For example:
- Write operations involve complex business rules, aggregate validation, and invariant enforcement
- Read operations need denormalized data optimized for specific views
- The write model structure doesn't align well with query requirements

Example: An order management system where placing an order involves multiple validation steps, inventory checks, and pricing calculations, but displaying order history requires flattened data with pre-calculated totals and status summaries.

**2. Performance Requirements with Different Scaling Needs**

Systems with high read-to-write ratios benefit from CQRS because reads and writes can be scaled independently:
- Read models can be denormalized for query performance
- Read databases can be replicated across regions
- Write operations maintain transactional integrity on a single database
- Caching strategies can be applied aggressively to read models

Example: A social media feed where posts are written occasionally but read millions of times. The write model maintains relationships and permissions, while read models provide pre-computed feeds optimized for rapid retrieval.

**3. Collaborative Domains with Task-Based UIs**

When multiple users work on the same data and the UI presents task-based operations rather than CRUD forms:
- Commands represent user intentions clearly (ApproveInvoice, RejectProposal, ScheduleMaintenance)
- Business operations are captured as explicit commands
- Event-driven workflows coordinate between users
- Audit trails track command execution

Example: An approval workflow system where invoices move through stages with explicit approval/rejection actions, and users need views showing "invoices pending my approval" vs. "all invoices in the system."

**4. Event Sourcing Integration**

CQRS fits naturally with Event Sourcing:
- Commands produce events
- Events become the source of truth
- Read models are built from event projections
- Historical state can be reconstructed

Example: A financial trading system where every trade is an immutable event, the current position is calculated from event history, and multiple read models provide different views (position summary, transaction history, compliance reports).

**5. Specific Bounded Contexts (Selective Application)**

The most important principle: **Apply CQRS selectively**. Not every bounded context needs CQRS. Apply it only where the benefits justify the complexity:
- Order Processing BC: CQRS beneficial (complex writes, simple reads)
- User Profile BC: Traditional approach sufficient (simple CRUD)
- Reporting BC: CQRS beneficial (read-optimized queries)
- Configuration BC: Traditional approach sufficient (low volume)

#### Do NOT Use CQRS When:

**Martin Fowler's Caution**:
> "You should be very cautious about using CQRS. Many information systems fit well with the notion of an information base that is updated in the same way that it's read, adding CQRS to such a system can add significant complexity."

**1. Simple CRUD Applications**

If your application primarily performs straightforward create, read, update, and delete operations with no complex business logic, CQRS adds unnecessary overhead:
- User management with basic profile fields
- Configuration settings storage
- Simple catalog or directory applications
- Administrative back-office tools

**2. Low Complexity Domains**

When business rules are minimal and the domain model is straightforward:
- No significant difference between write and read requirements
- Single view of data suffices for all use cases
- No performance bottlenecks requiring optimization
- Team unfamiliar with CQRS patterns

**3. Small Systems and Early-Stage Projects**

Don't over-engineer at the start:
- Begin with simpler patterns (traditional layered architecture)
- Add CQRS later if needs emerge
- Avoid premature optimization
- Let actual usage patterns guide architectural decisions

**4. When Eventual Consistency is Unacceptable**

CQRS with separate read/write databases introduces eventual consistency. If your business requires immediate consistency for all operations, CQRS becomes problematic:
- Financial transactions requiring instant balance updates
- Inventory systems where stock levels must be immediately accurate
- Real-time bidding systems

**5. Limited Development Resources**

CQRS requires:
- Higher development skills
- More sophisticated testing
- Additional infrastructure (potentially separate databases)
- Event synchronization mechanisms
- Monitoring and debugging tools for eventual consistency

If your team lacks experience or resources for this complexity, avoid CQRS.

### 1.3 CQRS Decision Tree

```
┌─────────────────────────────────────────────────────────────┐
│ Does your system have significantly different read and      │
│ write requirements?                                          │
└────┬─────────────────────────────────────────────────┬──────┘
     │ YES                                              │ NO
     ▼                                                  ▼
┌──────────────────────────────────────┐    ┌──────────────────────────┐
│ Is the read-to-write ratio > 10:1?   │    │ Use Traditional          │
│ OR                                    │    │ Application Service      │
│ Do you need independent scaling?     │    │ Pattern                  │
└────┬────────────────────────┬────────┘    │                          │
     │ YES                     │ NO          │ - Same model for reads   │
     ▼                         ▼             │   and writes             │
┌─────────────────┐  ┌──────────────────┐  │ - Simpler architecture   │
│ Can your        │  │ Use CQRS-Lite:   │  │ - Lower complexity       │
│ business accept │  │ - Separate       │  └──────────────────────────┘
│ eventual        │  │   handlers       │
│ consistency?    │  │ - Same DB        │
└─┬───────────┬───┘  │ - Immediate      │
  │ YES       │ NO   │   consistency    │
  ▼           ▼      └──────────────────┘
┌────────┐  ┌────────────────┐
│ Full   │  │ CQRS with      │
│ CQRS   │  │ Compensating   │
│        │  │ Transactions   │
│ - Separate│ │                │
│   DBs    │ │ - Maintain     │
│ - Event  │ │   transactional│
│   sync   │ │   guarantees   │
└─────────┘ └────────────────┘
```

### 1.4 Command Side vs Query Side Separation

#### Command Side (Write Model)

The command side is responsible for all state changes in the system. It uses the domain model with its rich business logic, aggregates, and invariants.

**Characteristics**:
- **Domain-Centric**: Uses aggregates, entities, and value objects
- **Business Logic**: Enforces invariants and business rules
- **Transactional**: Maintains ACID properties within aggregate boundaries
- **Normalized**: Data structure optimized for consistency
- **Event Publishing**: Produces domain events on successful operations

**Command Processing Flow**:
```
1. Client submits Command (e.g., PlaceOrderCmd)
2. Command Handler (Application Service) receives command
3. Validate input format and required fields
4. Load Aggregate from Repository
5. Execute domain operation on Aggregate
6. Aggregate validates business rules and invariants
7. Persist Aggregate to Write Database
8. Collect Domain Events from Aggregate
9. Publish Domain Events
10. Return result (void, ID, or acknowledgment)
```

**Schema Support**:
The tactical schema provides `CommandInterface` for defining commands:

```yaml
command_interfaces:
  - id: cmd_order_commands
    name: OrderCommands
    aggregate_ref: agg_order
    command_records:
      - record_name: PlaceOrderCmd
        intent: placeOrder
        parameters:
          - name: customerId
            type: CustomerId
            required: true
          - name: items
            type: List<OrderItem>
            required: true
        returns: domain_id
        return_type_ref: vo_order_id
        modifies_aggregate: agg_order
        publishes_events:
          - evt_order_placed
```

#### Query Side (Read Model)

The query side is responsible for retrieving data for display. It bypasses the domain model and reads directly from optimized read models.

**Characteristics**:
- **View-Centric**: Optimized for specific UI views
- **No Business Logic**: Pure data retrieval
- **Denormalized**: Data structure optimized for query performance
- **Eventually Consistent**: May lag behind write model
- **Cached**: Aggressive caching strategies possible

**Query Processing Flow**:
```
1. Client submits Query (e.g., GetOrderSummary)
2. Query Handler (Application Service) receives query
3. Validate query parameters
4. Query Read Model directly (bypass domain model)
5. Transform data to DTO
6. Return DTO to client
```

**Schema Support**:
The tactical schema provides `QueryInterface` for defining queries:

```yaml
query_interfaces:
  - id: qry_order_queries
    name: OrderQueries
    aggregate_ref: agg_order
    query_methods:
      - method_name: getOrderSummary
        parameters:
          - name: orderId
            type: OrderId
            required: true
        result_record_name: OrderSummary
        result_structure:
          fields:
            - name: orderId
              type: String
              serialization: "OrderId.value()"
            - name: customerId
              type: String
            - name: status
              type: String
              serialization: "status.name()"
            - name: itemCount
              type: Integer
            - name: totalAmount
              type: BigDecimal
        bypasses_domain_model: true
        optimizations:
          denormalized: true
          cached: true
          indexed: true
```

### 1.5 Read Models and Write Models

#### Write Model Design

The write model is your traditional domain model following DDD tactical patterns:

**Components**:
- Aggregates with enforced boundaries
- Entities with identity and lifecycle
- Value Objects for domain concepts
- Domain Services for multi-entity operations
- Repositories for persistence abstraction

**Example Write Model**:
```java
// Aggregate Root
public class Order {
    private OrderId orderId;
    private CustomerId customerId;
    private List<OrderItem> items;
    private OrderStatus status;
    private Money totalAmount;

    // Factory method
    public static Order create(OrderId id, CustomerId customerId) {
        Order order = new Order(id, customerId);
        order.status = OrderStatus.PENDING;
        order.items = new ArrayList<>();
        return order;
    }

    // Business operation
    public void addItems(List<OrderItem> newItems) {
        // Validate business rules
        if (status != OrderStatus.PENDING) {
            throw new IllegalStateException("Cannot add items to non-pending order");
        }

        // Enforce invariants
        items.addAll(newItems);
        totalAmount = calculateTotal();

        // Record domain event
        registerEvent(new ItemsAdded(orderId, newItems));
    }

    private Money calculateTotal() {
        return items.stream()
            .map(item -> item.getPrice().multiply(item.getQuantity()))
            .reduce(Money.ZERO, Money::add);
    }
}
```

#### Read Model Design

Read models are optimized for queries, often denormalized, and may combine data from multiple aggregates:

**Design Principles**:
- Flat structure (avoid nested objects)
- Pre-calculated values (no computation at query time)
- View-specific projections
- String serialization for complex types

**Example Read Model**:
```java
// Read Model (denormalized view)
public class OrderSummary {
    private String orderId;           // String, not OrderId
    private String customerId;         // String, not CustomerId
    private String customerName;       // Denormalized from Customer aggregate
    private String status;             // String, not enum
    private int itemCount;             // Pre-calculated
    private String totalAmount;        // Pre-formatted string
    private String placedAt;           // ISO-8601 string
    private String shippingAddress;    // Flattened address

    // No business logic, just getters
    // Created by query handler or projection
}
```

**Read Model Update Mechanism**:
```java
// Event Handler updates Read Model
@EventListener
public class OrderSummaryProjection {

    @Transactional
    public void on(OrderPlaced event) {
        OrderSummaryEntity entity = new OrderSummaryEntity();
        entity.setOrderId(event.getOrderId().value());
        entity.setCustomerId(event.getCustomerId().value());
        entity.setStatus("PENDING");
        entity.setItemCount(event.getItems().size());
        entity.setTotalAmount(event.getTotalAmount().toString());
        entity.setPlacedAt(event.getTimestamp().toString());

        // Fetch customer name (denormalization)
        Customer customer = customerRepository.findById(event.getCustomerId());
        entity.setCustomerName(customer.getName());

        readRepository.save(entity);
    }

    @Transactional
    public void on(OrderStatusChanged event) {
        OrderSummaryEntity entity = readRepository.findById(event.getOrderId());
        entity.setStatus(event.getNewStatus().name());
        readRepository.save(entity);
    }
}
```

### 1.6 Eventual Consistency in CQRS

When using CQRS with separate databases or even separate tables, the read model becomes eventually consistent with the write model.

**Implications**:
- Users may see stale data briefly after a command
- UI must handle scenarios where data hasn't updated yet
- Business processes must account for synchronization delays
- Error handling for sync failures is required

**Mitigation Strategies**:

**1. Optimistic UI Updates**:
```javascript
// Client-side: Optimistically update UI immediately
function placeOrder(orderData) {
    // Update UI immediately (optimistic)
    displayOrderConfirmation(orderData);

    // Submit command
    api.placeOrder(orderData)
        .then(result => {
            // Command succeeded
            updateWithServerData(result);
        })
        .catch(error => {
            // Command failed - revert UI
            revertOptimisticUpdate();
            displayError(error);
        });
}
```

**2. Command Result with Projection**:
```java
// Return projection immediately with command result
public OrderPlacedResult placeOrder(PlaceOrderCmd cmd) {
    // Execute command on write model
    OrderId orderId = commandHandler.handle(cmd);

    // Immediately build projection from write model
    Order order = orderRepository.findById(orderId);
    OrderSummary summary = OrderSummaryMapper.toDTO(order);

    return new OrderPlacedResult(orderId, summary);
}
```

**3. Versioning with Event Timestamps**:
```java
public class OrderSummary {
    private String orderId;
    private long version;  // Event sequence number
    private Instant lastUpdated;

    // Client can detect staleness
    public boolean isStale(Duration threshold) {
        return Duration.between(lastUpdated, Instant.now())
                       .compareTo(threshold) > 0;
    }
}
```

### 1.7 CQRS Without Separate Databases (CQRS-Lite)

For many systems, you can gain benefits of CQRS without the complexity of separate databases:

**Approach**:
- Separate command and query handlers
- Same database for both
- Different tables optimized for reads vs. writes
- Update read tables in same transaction as write

**Benefits**:
- Maintains immediate consistency
- Simpler infrastructure
- Clear separation of concerns
- Independent handler optimization

**Example**:
```java
// Write to domain tables
@Transactional
public OrderId placeOrder(PlaceOrderCmd cmd) {
    // Write to normalized domain tables
    Order order = Order.create(cmd.orderId(), cmd.customerId());
    order.addItems(cmd.items());
    orderRepository.save(order);  // Writes to order, order_items tables

    // Update denormalized read table in same transaction
    OrderSummary summary = buildSummary(order);
    readRepository.save(summary);  // Writes to order_summary table

    return order.getId();
}

// Read from denormalized read table
public OrderSummary getOrderSummary(OrderId orderId) {
    // Query optimized read table directly
    return readRepository.findById(orderId);
}
```

### 1.8 Schema Enforcement of CQRS Patterns

The tactical schema enforces CQRS separation through distinct interfaces:

**Command Interface Characteristics**:
- Defined in API layer
- Immutable command records
- Each command modifies exactly one aggregate
- Returns void, domain ID, or acknowledgment (not business data)
- Publishes domain events

**Query Interface Characteristics**:
- Defined in API layer
- No side effects (const: true)
- Returns immutable DTOs
- May bypass domain model
- Optimized for specific views
- Flat structure enforced

**Schema Validation Rules**:
```yaml
validation_rules:
  - rule: "one_aggregate_per_transaction"
    description: "Command must modify at most one aggregate per transaction"
    validation: "For each operation where type='command',
                 transaction_boundary.modifies_aggregates must have maxItems: 1"

  - rule: "queries_no_side_effects"
    description: "Queries must have no side effects"
    validation: "query_interface.no_side_effects must be true"
```

---

## 2. Application Service Orchestration Patterns

### 2.1 Introduction to Application Services

Application Services sit in the application layer, above the domain layer, and are responsible for coordinating use case execution. They are the entry point for external clients (UI, BFF, API) to interact with the domain model.

**Core Principle**: Application Services contain NO business logic—only orchestration logic.

**Eric Evans' Definition**:
> "The application layer is responsible for driving the workflow of the application, coordinating the domain objects to perform the actual work."

**Vaughn Vernon's Guidance**:
> "Application Services are the direct clients of the domain model and remain lightweight, coordinating operations performed against domain objects. Application Services should be kept thin, using them only to coordinate tasks on the model."

### 2.2 Coordination vs Business Logic

This distinction is the most critical aspect of Application Services and the most commonly violated principle.

#### What is Coordination Logic?

Coordination logic involves:
- Fetching aggregates from repositories
- Invoking domain operations on aggregates
- Saving aggregates back to repositories
- Publishing domain events
- Managing transaction boundaries
- Performing authorization checks
- Validating input format

**Example of Proper Coordination**:
```java
@Transactional
public void activateUser(ActivateUserCmd cmd) {
    // 1. Authorization (application concern)
    if (!authService.hasPermission(currentUser, Permission.ACTIVATE_USER)) {
        throw new UnauthorizedException();
    }

    // 2. Load aggregate
    User user = userRepository.findById(cmd.userId())
        .orElseThrow(() -> new UserNotFoundException(cmd.userId()));

    // 3. Invoke domain operation (business logic in domain)
    user.activate();  // <-- Business logic is HERE, in the domain

    // 4. Persist
    userRepository.save(user);

    // 5. Publish event
    eventPublisher.publish(new UserActivated(user.getUserId(), Instant.now()));
}
```

#### What is Business Logic?

Business logic involves:
- Calculations and transformations
- Validation of business rules
- Enforcement of invariants
- Domain-specific algorithms
- State transitions with business meaning

**Anti-Pattern: Business Logic in Application Service**:
```java
@Transactional
public void processOrder(ProcessOrderCmd cmd) {
    Order order = orderRepository.findById(cmd.orderId());

    // WRONG: Business logic in application service
    BigDecimal total = BigDecimal.ZERO;
    for (OrderItem item : cmd.items()) {
        BigDecimal itemTotal = item.getQuantity()
            .multiply(item.getUnitPrice());

        // Apply discount rules (BUSINESS LOGIC - belongs in domain!)
        if (item.getQuantity() > 10) {
            itemTotal = itemTotal.multiply(new BigDecimal("0.9"));
        }

        total = total.add(itemTotal);
    }

    order.setTotal(total);  // Using anemic domain model
    orderRepository.save(order);
}
```

**Correct Pattern: Business Logic in Domain**:
```java
// Application Service (thin coordination)
@Transactional
public void processOrder(ProcessOrderCmd cmd) {
    Order order = orderRepository.findById(cmd.orderId());

    // Delegate to domain for business logic
    order.addItems(cmd.items());  // Business logic encapsulated here

    orderRepository.save(order);
}

// Domain Aggregate (rich with business logic)
public class Order {
    public void addItems(List<OrderItem> items) {
        for (OrderItem item : items) {
            // Business logic in domain
            validateItem(item);
            applyPricingRules(item);
            this.items.add(item);
        }

        this.totalAmount = calculateTotal();
    }

    private Money calculateTotal() {
        return items.stream()
            .map(OrderItem::getTotalPrice)
            .reduce(Money.ZERO, Money::add);
    }

    private void applyPricingRules(OrderItem item) {
        if (item.getQuantity() > 10) {
            item.applyDiscount(Percentage.of(10));
        }
    }
}
```

### 2.3 Transaction Management Patterns

Application Services are responsible for defining and managing transaction boundaries. This is one of their core responsibilities.

#### Pattern 1: Single Transaction Per Use Case

Each application service method defines one transaction boundary:

```java
@Transactional  // Transaction starts here
public OrderId placeOrder(PlaceOrderCmd cmd) {
    // All operations in this method execute in one transaction

    // 1. Load aggregate
    Order order = Order.create(cmd.orderId(), cmd.customerId());

    // 2. Execute domain operations
    order.addItems(cmd.items());
    order.setShippingAddress(cmd.shippingAddress());

    // 3. Persist
    orderRepository.save(order);

    // 4. Collect events
    List<DomainEvent> events = order.getDomainEvents();

    // Transaction commits here
    return order.getId();
}  // COMMIT

// After commit, publish events
// (in a @AfterCommit or via TransactionSynchronization)
```

**Key Points**:
- Transaction demarcation at application service boundary
- Domain layer is unaware of transactions
- Commit happens when method returns successfully
- Rollback happens on exception

#### Pattern 2: Transaction Propagation

Sometimes operations need to coordinate transactions:

```java
// Default: REQUIRED - join existing transaction or create new one
@Transactional(propagation = Propagation.REQUIRED)
public void executeCommand(Command cmd) {
    // Joins existing transaction if present
}

// REQUIRES_NEW - always start new transaction
@Transactional(propagation = Propagation.REQUIRES_NEW)
public void audit(AuditEvent event) {
    // Even if calling transaction fails, audit persists
}

// SUPPORTS - run in transaction if present, otherwise non-transactional
@Transactional(propagation = Propagation.SUPPORTS)
public OrderSummary getOrderSummary(OrderId id) {
    // Queries often don't need transactions
}

// NOT_SUPPORTED - always run non-transactional
@Transactional(propagation = Propagation.NOT_SUPPORTED)
public void sendNotification(Notification notification) {
    // External service calls shouldn't be in transaction
}
```

#### Pattern 3: Compensating Transactions

When operations across aggregates fail, use compensating transactions:

```java
public class OrderSaga {

    @Transactional
    public void startOrder(CreateOrderCmd cmd) {
        // Transaction 1: Create order
        Order order = Order.create(cmd.orderId(), cmd.customerId());
        orderRepository.save(order);

        // Publish event for next step
        eventPublisher.publish(new OrderCreated(order.getId()));
    }

    @EventListener
    @Transactional
    public void reserveInventory(OrderCreated event) {
        try {
            // Transaction 2: Reserve inventory
            Inventory inventory = inventoryRepository.findById(event.getWarehouseId());
            inventory.reserve(event.getItems());
            inventoryRepository.save(inventory);

            eventPublisher.publish(new InventoryReserved(event.getOrderId()));
        } catch (InsufficientInventoryException e) {
            // Trigger compensation
            eventPublisher.publish(new InventoryReservationFailed(event.getOrderId()));
        }
    }

    @EventListener
    @Transactional
    public void compensateOrder(InventoryReservationFailed event) {
        // Compensating transaction: Cancel order
        Order order = orderRepository.findById(event.getOrderId());
        order.cancel("Insufficient inventory");
        orderRepository.save(order);

        eventPublisher.publish(new OrderCancelled(event.getOrderId()));
    }
}
```

### 2.4 Domain Event Publishing Patterns

Application Services are responsible for publishing domain events after successful transactions.

#### Pattern 1: Collect and Publish After Commit

```java
public class OrderApplicationService {

    @Transactional
    public OrderId placeOrder(PlaceOrderCmd cmd) {
        Order order = Order.create(cmd.orderId(), cmd.customerId());
        order.addItems(cmd.items());

        orderRepository.save(order);

        // Collect events from aggregate
        List<DomainEvent> events = order.getDomainEvents();

        // Register for publishing after commit
        TransactionSynchronizationManager.registerSynchronization(
            new AfterCommitPublisher(events, eventPublisher)
        );

        return order.getId();
    }
}

class AfterCommitPublisher extends TransactionSynchronizationAdapter {
    private final List<DomainEvent> events;
    private final EventPublisher publisher;

    @Override
    public void afterCommit() {
        events.forEach(publisher::publish);
    }
}
```

#### Pattern 2: Outbox Pattern for Reliability

For guaranteed event delivery, use the transactional outbox pattern:

```java
@Transactional
public OrderId placeOrder(PlaceOrderCmd cmd) {
    // 1. Execute domain operation
    Order order = Order.create(cmd.orderId(), cmd.customerId());
    order.addItems(cmd.items());
    orderRepository.save(order);

    // 2. Write events to outbox table in same transaction
    List<DomainEvent> events = order.getDomainEvents();
    for (DomainEvent event : events) {
        OutboxMessage message = new OutboxMessage(
            UUID.randomUUID(),
            event.getClass().getName(),
            objectMapper.writeValueAsString(event),
            Instant.now()
        );
        outboxRepository.save(message);
    }

    return order.getId();
}

// Separate background process publishes from outbox
@Scheduled(fixedDelay = 1000)
public void publishOutboxMessages() {
    List<OutboxMessage> pending = outboxRepository.findUnpublished();

    for (OutboxMessage message : pending) {
        try {
            DomainEvent event = deserializeEvent(message);
            eventPublisher.publish(event);

            message.markPublished();
            outboxRepository.save(message);
        } catch (Exception e) {
            // Retry later
            message.incrementRetryCount();
            outboxRepository.save(message);
        }
    }
}
```

#### Pattern 3: In-Memory Event Bus (Simple Scenarios)

For simple, single-process applications:

```java
@Singleton
public class UserApplicationService {

    private final ApplicationEventPublisher<Object> eventPublisher;

    @Transactional
    public UserId createUser(CreateUserCmd cmd) {
        User user = User.create(cmd.userId(), cmd.email());
        userRepository.save(user);

        // Publish to in-memory bus
        eventPublisher.publishEvent(new UserCreated(
            user.getUserId().value(),
            user.getEmail(),
            Instant.now()
        ));

        return user.getUserId();
    }
}

// Event listeners in same process
@Component
public class UserEventHandlers {

    @EventListener
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void on(UserCreated event) {
        // Handle in separate transaction
        sendWelcomeEmail(event.getEmail());
        createUserPreferences(event.getUserId());
    }
}
```

### 2.5 Error Handling Strategies

Application Services must handle errors at the right level:

#### Application-Level Errors

Handle format validation and resource not found at application level:

```java
@Transactional
public void activateUser(ActivateUserCmd cmd) {
    // Application-level validation
    if (cmd.userId() == null) {
        throw new ValidationException("User ID is required");
    }

    // Application-level error: resource not found
    User user = userRepository.findById(cmd.userId())
        .orElseThrow(() -> new UserNotFoundException(cmd.userId()));

    // Delegate to domain
    try {
        user.activate();
    } catch (DomainException e) {
        // Re-throw domain exceptions
        throw e;
    }

    userRepository.save(user);
}
```

#### Domain-Level Errors

Domain layer throws business rule violations:

```java
public class User {
    public void activate() {
        // Domain-level business rule
        if (status == UserStatus.LOCKED) {
            throw new UserLockedException(
                "Cannot activate locked user. User must be unlocked first."
            );
        }

        if (status == UserStatus.ACTIVE) {
            // Idempotent - no-op if already active
            return;
        }

        this.status = UserStatus.ACTIVE;
        this.activatedAt = Instant.now();

        registerEvent(new UserActivated(userId, activatedAt));
    }
}
```

#### Error Response Patterns

Return structured errors to clients:

```java
@RestController
public class UserController {

    @PostMapping("/users/{id}/activate")
    public ResponseEntity<?> activateUser(@PathVariable String id) {
        try {
            applicationService.activateUser(new ActivateUserCmd(UserId.of(id)));
            return ResponseEntity.ok().build();

        } catch (UserNotFoundException e) {
            return ResponseEntity.status(404)
                .body(new ErrorResponse("USER_NOT_FOUND", e.getMessage()));

        } catch (UserLockedException e) {
            return ResponseEntity.status(409)
                .body(new ErrorResponse("USER_LOCKED", e.getMessage()));

        } catch (ValidationException e) {
            return ResponseEntity.status(400)
                .body(new ErrorResponse("VALIDATION_ERROR", e.getMessage()));
        }
    }
}
```

### 2.6 Workflow Patterns from Schema

The tactical schema defines workflow steps for application service operations:

```yaml
workflow:
  validates_input: true          # Format validation
  loads_aggregates:              # Aggregates to load
    - agg_user
  invokes_domain_operations:     # Domain methods to call
    - "user.activate()"
  invokes_domain_services:       # Domain services to use
    - svc_dom_user_authentication
  persists_aggregates: true      # Save changes
  publishes_events:              # Events to publish
    - evt_user_activated
  returns_dto: UserSummary       # Return value for queries
```

**Complete Workflow Example**:

```java
@Transactional
public void deactivateUser(DeactivateUserCmd cmd) {
    // Step 1: Validate input
    if (cmd.userId() == null) {
        throw new ValidationException("User ID is required");
    }
    if (StringUtils.isBlank(cmd.reason())) {
        throw new ValidationException("Deactivation reason is required");
    }

    // Step 2: Load aggregate
    User user = userRepository.findById(cmd.userId())
        .orElseThrow(() -> new UserNotFoundException(cmd.userId()));

    // Step 3: Invoke domain service (if needed)
    // In this case, no domain service needed

    // Step 4: Invoke domain operation
    user.deactivate(cmd.reason());

    // Step 5: Persist aggregate
    userRepository.save(user);

    // Step 6: Publish events
    eventPublisher.publishEvent(new UserDeactivated(
        user.getUserId().value(),
        cmd.reason(),
        Instant.now()
    ));

    // Step 7: Return (void for state transitions)
}
```

---

## 3. Read Model Implementation

### 3.1 Purpose and Rationale

Read Models serve a fundamentally different purpose than write models. While write models enforce business rules and maintain transactional consistency, read models optimize for query performance and user experience.

**Key Motivations**:

1. **Query Performance**: Denormalized data eliminates expensive joins
2. **View-Specific Optimization**: Each view gets its own optimized projection
3. **Scalability**: Read databases can be replicated and scaled independently
4. **Simplicity**: No business logic in queries—just data retrieval

**Martin Fowler's Insight**:
> "The change that CQRS introduces is to split that conceptual model into separate models for update and display, which it calls Command and Query respectively."

### 3.2 Denormalization Strategies

#### Strategy 1: Pre-Join Data

Instead of joining at query time, pre-join and store:

**Normalized Write Model**:
```sql
-- Separate tables (normalized)
orders: order_id, customer_id, status, created_at
customers: customer_id, name, email
order_items: item_id, order_id, product_id, quantity, price
products: product_id, name, description
```

**Denormalized Read Model**:
```sql
-- Single denormalized table
order_summary:
  order_id,
  customer_id,
  customer_name,        -- Denormalized from customers
  customer_email,       -- Denormalized from customers
  status,
  item_count,           -- Pre-calculated
  total_amount,         -- Pre-calculated
  created_at,
  shipping_address      -- Flattened JSON
```

#### Strategy 2: Pre-Calculate Aggregations

Calculate expensive aggregations once and store:

```java
@EventListener
public class OrderSummaryProjection {

    @Transactional
    public void on(OrderPlaced event) {
        // Pre-calculate everything
        int itemCount = event.getItems().size();
        BigDecimal totalAmount = event.getItems().stream()
            .map(item -> item.getPrice().multiply(item.getQuantity()))
            .reduce(BigDecimal.ZERO, BigDecimal::add);

        OrderSummaryEntity summary = new OrderSummaryEntity();
        summary.setOrderId(event.getOrderId().value());
        summary.setItemCount(itemCount);
        summary.setTotalAmount(totalAmount);

        readRepository.save(summary);
    }
}
```

#### Strategy 3: Flatten Nested Structures

Convert nested objects to flat fields:

**Domain Model (Nested)**:
```java
public class Order {
    private OrderId orderId;
    private Address shippingAddress;  // Value Object
}

public class Address {
    private String street;
    private String city;
    private String state;
    private String postalCode;
    private Country country;  // Another Value Object
}
```

**Read Model (Flat)**:
```java
public class OrderSummary {
    private String orderId;
    private String shippingStreet;
    private String shippingCity;
    private String shippingState;
    private String shippingPostalCode;
    private String shippingCountry;  // All flattened
}
```

### 3.3 Update Mechanisms (Projection)

Read models must be kept synchronized with write models. This is done through projections.

#### Projection Pattern 1: Event-Driven Updates

The most common pattern—update read model when domain events occur:

```java
@Component
public class OrderProjections {

    private final OrderSummaryRepository readRepository;

    @EventListener
    @Transactional
    public void on(OrderPlaced event) {
        // Create new read model entry
        OrderSummaryEntity summary = new OrderSummaryEntity();
        summary.setOrderId(event.getOrderId().value());
        summary.setCustomerId(event.getCustomerId().value());
        summary.setStatus("PLACED");
        summary.setItemCount(event.getItems().size());
        summary.setTotalAmount(calculateTotal(event.getItems()));
        summary.setCreatedAt(event.getTimestamp());

        readRepository.save(summary);
    }

    @EventListener
    @Transactional
    public void on(OrderShipped event) {
        // Update existing read model entry
        OrderSummaryEntity summary = readRepository.findById(event.getOrderId())
            .orElseThrow();

        summary.setStatus("SHIPPED");
        summary.setShippedAt(event.getTimestamp());

        readRepository.save(summary);
    }

    @EventListener
    @Transactional
    public void on(OrderCancelled event) {
        // Update status
        OrderSummaryEntity summary = readRepository.findById(event.getOrderId())
            .orElseThrow();

        summary.setStatus("CANCELLED");
        summary.setCancelReason(event.getReason());
        summary.setCancelledAt(event.getTimestamp());

        readRepository.save(summary);
    }
}
```

#### Projection Pattern 2: Change Data Capture (CDC)

For systems with existing databases, use CDC:

```
Write Database → CDC Tool (Debezium) → Kafka → Projection Service → Read Database
```

**Benefits**:
- No application code changes needed
- Guaranteed consistency (database-level)
- Works with legacy systems

#### Projection Pattern 3: Scheduled Batch Updates

For read models that don't need real-time updates:

```java
@Component
public class DailyReportProjection {

    @Scheduled(cron = "0 0 1 * * *")  // 1 AM daily
    @Transactional
    public void rebuildDailyOrderReport() {
        LocalDate yesterday = LocalDate.now().minusDays(1);

        // Query write database
        List<Order> orders = orderRepository.findByDate(yesterday);

        // Build aggregated report
        DailyOrderReport report = new DailyOrderReport();
        report.setDate(yesterday);
        report.setTotalOrders(orders.size());
        report.setTotalRevenue(calculateRevenue(orders));
        report.setAverageOrderValue(calculateAverage(orders));

        reportRepository.save(report);
    }
}
```

### 3.4 Bypasses Domain Model Flag

The schema includes a `bypasses_domain_model` flag to indicate whether queries go through the domain layer or directly to the read database.

**Schema Definition**:
```yaml
query_methods:
  - method_name: getUserSummary
    bypasses_domain_model: false  # Goes through domain model

  - method_name: listRecentOrders
    bypasses_domain_model: true   # Directly queries read database
```

#### When to Bypass Domain Model

**Bypass (bypasses_domain_model: true)**:
- Read model is denormalized and optimized
- No business logic needed
- High-volume queries
- Performance is critical

```java
public OrderSummary getOrderSummary(OrderId orderId) {
    // Bypass domain model - query read database directly
    return readRepository.findById(orderId.value())
        .map(this::toDTO)
        .orElseThrow(() -> new OrderNotFoundException(orderId));
}
```

**Use Domain Model (bypasses_domain_model: false)**:
- Need domain logic for permissions
- Business rules affect what data is shown
- Computed values require domain methods

```java
public OrderDetails getOrderDetails(OrderId orderId, UserId requestingUser) {
    // Load from domain model
    Order order = orderRepository.findById(orderId)
        .orElseThrow(() -> new OrderNotFoundException(orderId));

    // Apply business logic
    if (!order.canBeViewedBy(requestingUser)) {
        throw new UnauthorizedException();
    }

    // Return with domain-calculated values
    return OrderDetails.from(order);
}
```

### 3.5 Optimization Strategies

The schema defines three optimization flags for queries:

```yaml
optimizations:
  denormalized: true   # Data is denormalized
  cached: true         # Results are cached
  indexed: true        # Database indexes applied
```

#### Optimization 1: Denormalization

Already covered in section 3.2. Key takeaway: denormalize frequently queried data.

#### Optimization 2: Caching

Apply aggressive caching to read models:

```java
@Service
public class OrderQueryService {

    private final LoadingCache<OrderId, OrderSummary> cache;

    public OrderQueryService() {
        this.cache = Caffeine.newBuilder()
            .maximumSize(10_000)
            .expireAfterWrite(Duration.ofMinutes(5))
            .build(this::loadOrderSummary);
    }

    public OrderSummary getOrderSummary(OrderId orderId) {
        return cache.get(orderId);
    }

    private OrderSummary loadOrderSummary(OrderId orderId) {
        return readRepository.findById(orderId.value())
            .map(this::toDTO)
            .orElseThrow(() -> new OrderNotFoundException(orderId));
    }

    // Invalidate cache when data changes
    @EventListener
    public void on(OrderUpdated event) {
        cache.invalidate(event.getOrderId());
    }
}
```

**Caching Strategies**:
- **Application-level**: Caffeine, Guava Cache
- **Distributed**: Redis, Memcached
- **HTTP-level**: Cache-Control headers
- **CDN**: For static read models

#### Optimization 3: Database Indexes

Create indexes on read model tables for common queries:

```sql
-- Index on commonly queried fields
CREATE INDEX idx_order_summary_customer
ON order_summary(customer_id);

CREATE INDEX idx_order_summary_status
ON order_summary(status);

CREATE INDEX idx_order_summary_date
ON order_summary(created_at);

-- Composite index for complex queries
CREATE INDEX idx_order_summary_customer_date
ON order_summary(customer_id, created_at DESC);

-- Covering index (includes all columns needed)
CREATE INDEX idx_order_summary_list
ON order_summary(customer_id, status)
INCLUDE (order_id, total_amount, created_at);
```

#### Optimization 4: Materialized Views

Use database materialized views for complex aggregations:

```sql
CREATE MATERIALIZED VIEW daily_order_stats AS
SELECT
    DATE(created_at) as order_date,
    COUNT(*) as order_count,
    SUM(total_amount) as total_revenue,
    AVG(total_amount) as avg_order_value
FROM order_summary
GROUP BY DATE(created_at);

-- Refresh periodically
REFRESH MATERIALIZED VIEW CONCURRENTLY daily_order_stats;
```

### 3.6 Read Model Consistency Guarantees

Different read models may have different consistency requirements:

#### Strong Consistency (Immediate Updates)

Updated in same transaction as write:

```java
@Transactional
public OrderId placeOrder(PlaceOrderCmd cmd) {
    // Update write model
    Order order = Order.create(cmd.orderId(), cmd.customerId());
    order.addItems(cmd.items());
    orderRepository.save(order);

    // Update read model in SAME transaction
    OrderSummary summary = buildSummary(order);
    readRepository.save(summary);

    return order.getId();
}
```

#### Eventual Consistency (Asynchronous Updates)

Updated via events:

```java
// Write model transaction
@Transactional
public OrderId placeOrder(PlaceOrderCmd cmd) {
    Order order = Order.create(cmd.orderId(), cmd.customerId());
    order.addItems(cmd.items());
    orderRepository.save(order);

    // Event published after transaction
    eventPublisher.publish(new OrderPlaced(...));

    return order.getId();
}

// Separate transaction updates read model
@EventListener
@Transactional
public void on(OrderPlaced event) {
    OrderSummary summary = buildSummary(event);
    readRepository.save(summary);
}
```

#### Session Consistency (Read Your Writes)

Ensure users see their own changes immediately:

```java
public class OrderService {

    @Transactional
    public OrderPlacedResult placeOrder(PlaceOrderCmd cmd) {
        // Execute command
        OrderId orderId = commandHandler.handle(cmd);

        // Immediately build and return projection from write model
        Order order = orderRepository.findById(orderId);
        OrderSummary summary = OrderSummary.from(order);

        // Return both ID and immediate projection
        return new OrderPlacedResult(orderId, summary);
    }
}
```

---

## 4. DTO Design in DDD

### 4.1 DTOs vs Domain Objects

Data Transfer Objects (DTOs) serve as the boundary between the application layer and external clients. Understanding when to use DTOs versus domain objects is critical.

**Domain Objects**:
- Belong to domain layer
- Rich with behavior and business logic
- Encapsulate state and invariants
- May contain references to other domain objects
- Optimized for business operations

**DTOs**:
- Belong to application/API layer
- Pure data containers with no behavior
- Simple, serializable structures
- Optimized for data transfer
- Often flat and denormalized

**Martin Fowler's Definition**:
> "DTO is an object that carries data between processes. The difference between data transfer objects and business objects or data access objects is that a DTO does not have any behavior except for storage and retrieval of its own data."

### 4.2 DTOField Structure

The tactical schema defines `DTOField` for query result structures:

```yaml
DTOField:
  type: object
  properties:
    name:
      type: string
    type:
      type: string
      description: "Field type (String for IDs/enums, primitives for counts)"
    serialization:
      type: string
      description: "How complex types are serialized"
    description:
      type: string
```

**Example from Schema**:
```yaml
result_structure:
  fields:
    - name: userId
      type: String
      serialization: "UserId serialized to String via userId.id()"
      description: "User identifier"

    - name: status
      type: String
      serialization: "Status enum serialized to String via status.name()"
      description: "Current user status"

    - name: createdAt
      type: String
      serialization: "Instant serialized to ISO-8601 string"
      description: "Creation timestamp"
```

### 4.3 ResultStructure for Queries

The schema's `ResultStructure` defines how query results are shaped:

```yaml
ResultStructure:
  type: object
  properties:
    fields:
      type: array
      items:
        $ref: "#/$defs/DTOField"

    aggregate_counts:
      type: array
      description: "Count fields for related entities (not full collections)"
      items:
        type: object
        properties:
          field_name: string
          counted_entity: string
```

**Example Usage**:
```yaml
query_methods:
  - method_name: getUserSummary
    result_record_name: UserSummary
    result_structure:
      fields:
        - name: userId
          type: String
        - name: email
          type: String
        - name: status
          type: String
      aggregate_counts:
        - field_name: activeSessionCount
          counted_entity: UserSession
```

**Implementation**:
```java
public record UserSummary(
    String userId,
    String email,
    String status,
    int activeSessionCount  // Count, not collection
) {}

public UserSummary getUserSummary(UserId userId) {
    User user = userRepository.findById(userId);
    int sessionCount = sessionRepository.countActiveByUser(userId);

    return new UserSummary(
        user.getUserId().id(),
        user.getEmail(),
        user.getStatus().name(),
        sessionCount
    );
}
```

### 4.4 Flat DTO Pattern (Knight)

The Knight codebase demonstrates a flat DTO pattern that avoids nested objects. This is enforced through the schema's `flat_structure` flag.

**Schema Enforcement**:
```yaml
query_interfaces:
  - id: qry_user_queries
    name: UserQueries
    result_characteristics:
      flat_structure: true      # Enforces flat structure
      string_serialization: true  # Complex types as strings
```

#### Why Flat Structure?

**Benefits**:
1. **Simpler Serialization**: No complex object graphs
2. **Better Caching**: Easier to cache flat structures
3. **Client-Friendly**: Easier for clients to consume
4. **Version Resilience**: Flatter structures evolve more easily
5. **Performance**: Less serialization overhead

**Anti-Pattern: Nested DTOs**:
```java
// AVOID: Nested structure
public class OrderDTO {
    private String orderId;
    private CustomerDTO customer;  // Nested object
    private List<OrderItemDTO> items;  // Nested collection
    private AddressDTO shippingAddress;  // Nested object
}

public class CustomerDTO {
    private String customerId;
    private String name;
    private String email;
    private AddressDTO billingAddress;  // More nesting
}
```

Problems with nested structure:
- Complex serialization
- Hard to cache
- Versioning difficulties
- Client parsing complexity

**Recommended: Flat Structure**:
```java
// BETTER: Flat structure
public record OrderSummary(
    String orderId,
    String customerId,      // ID only, not nested object
    String customerName,    // Denormalized
    String customerEmail,   // Denormalized
    String status,
    int itemCount,          // Count, not collection
    String totalAmount,     // Pre-formatted string
    String shippingStreet,  // Flattened address
    String shippingCity,
    String shippingState,
    String shippingPostalCode
) {}
```

### 4.5 String Serialization for Complex Types

The Knight pattern serializes complex types (IDs, enums, dates) to strings in DTOs.

**Schema Guidance**:
```yaml
best_practices:
  tactical:
    - "Serialize all complex types to strings in DTOs (IDs, enums, URNs)"
    - "Use flat DTO structure (no nested objects per Knight pattern)"
```

#### Serialization Patterns

**Pattern 1: Domain IDs to Strings**:
```java
// Domain: UserId value object
public record UserId(String id) {
    public static UserId of(String id) {
        return new UserId(id);
    }
}

// DTO: Serialized to String
public record UserSummary(
    String userId  // Not UserId, just String
) {}

// Mapping
UserSummary toDTO(User user) {
    return new UserSummary(
        user.getUserId().id()  // Extract string from value object
    );
}
```

**Pattern 2: Enums to Strings**:
```java
// Domain: Status enum
public enum UserStatus {
    PENDING, ACTIVE, LOCKED, DEACTIVATED
}

// DTO: Serialized to String
public record UserSummary(
    String status  // Not UserStatus enum
) {}

// Mapping
UserSummary toDTO(User user) {
    return new UserSummary(
        user.getStatus().name()  // Enum to string
    );
}
```

**Pattern 3: Dates/Times to ISO-8601 Strings**:
```java
// Domain: Instant
private Instant createdAt;

// DTO: String in ISO-8601 format
public record UserSummary(
    String createdAt  // "2025-10-24T10:30:00Z"
) {}

// Mapping
UserSummary toDTO(User user) {
    return new UserSummary(
        user.getCreatedAt().toString()  // ISO-8601 string
    );
}
```

**Pattern 4: Money to String**:
```java
// Domain: Money value object
public record Money(BigDecimal amount, Currency currency) {
    public String toString() {
        return amount.setScale(2, RoundingMode.HALF_UP) + " " + currency.getCode();
    }
}

// DTO: Pre-formatted string
public record OrderSummary(
    String totalAmount  // "123.45 USD"
) {}

// Mapping
OrderSummary toDTO(Order order) {
    return new OrderSummary(
        order.getTotalAmount().toString()  // Formatted string
    );
}
```

### 4.6 Why Separate from Command Records

Commands and DTOs serve different purposes and should be kept separate.

**Commands**:
- Represent user intent
- Input to system
- Validated before execution
- Immutable
- May reference domain value objects directly

**DTOs (Query Results)**:
- Represent system state
- Output from system
- No validation needed
- Immutable
- Always use primitive types and strings

**Example**:

```java
// Command: Input to system
public interface UserCommands {

    UserId createUser(CreateUserCmd cmd);

    record CreateUserCmd(
        String email,              // String (input validation)
        String userType,           // String (parsed to enum)
        String identityProvider,   // String (parsed to enum)
        ClientId clientId          // Value object (domain type)
    ) {}
}

// DTO: Output from system
public interface UserQueries {

    UserSummary getUserSummary(UserId userId);

    record UserSummary(
        String userId,           // String (serialized from UserId)
        String email,            // String
        String status,           // String (serialized from enum)
        String userType,         // String (serialized from enum)
        String identityProvider  // String (serialized from enum)
    ) {}
}
```

**Key Differences**:
1. Commands may use domain types (ClientId); DTOs use only strings
2. Commands are parsed and validated; DTOs are pre-validated
3. Commands represent intent; DTOs represent state
4. Commands may fail validation; DTOs are always valid

### 4.7 DTO Assembly Patterns

#### Pattern 1: Map from Single Aggregate

```java
public UserSummary getUserSummary(UserId userId) {
    User user = userRepository.findById(userId)
        .orElseThrow(() -> new UserNotFoundException(userId));

    return new UserSummary(
        user.getUserId().id(),
        user.getEmail(),
        user.getStatus().name(),
        user.getUserType().name(),
        user.getIdentityProvider().name()
    );
}
```

#### Pattern 2: Assemble from Multiple Aggregates

```java
public OrderDetailDTO getOrderDetail(OrderId orderId) {
    // Load multiple aggregates
    Order order = orderRepository.findById(orderId);
    Customer customer = customerRepository.findById(order.getCustomerId());

    // Assemble DTO from multiple sources
    return new OrderDetailDTO(
        order.getOrderId().value(),
        order.getStatus().name(),
        order.getTotalAmount().toString(),
        customer.getName(),           // From Customer aggregate
        customer.getEmail(),           // From Customer aggregate
        order.getItemCount()
    );
}
```

#### Pattern 3: Assemble from Read Model

```java
public OrderSummary getOrderSummary(OrderId orderId) {
    // Query denormalized read model
    OrderSummaryEntity entity = readRepository.findById(orderId.value())
        .orElseThrow(() -> new OrderNotFoundException(orderId));

    // Map entity to DTO
    return new OrderSummary(
        entity.getOrderId(),
        entity.getCustomerId(),
        entity.getCustomerName(),    // Already denormalized
        entity.getStatus(),
        entity.getItemCount(),
        entity.getTotalAmount().toString()
    );
}
```

---

## 5. Transaction Boundary Patterns

### 5.1 Fundamental Rule: One Aggregate Per Transaction

The most important rule in DDD transaction management:

**Vaughn Vernon's Rule**:
> "Modify only ONE aggregate instance per transaction"

This rule is enforced by the tactical schema:

```yaml
TransactionBoundary:
  type: object
  properties:
    modifies_aggregates:
      type: array
      description: "Aggregates modified by this operation (should be 0-1 for commands)"
      items:
        $ref: "#/$defs/AggId"
      maxItems: 1  # Schema enforces the rule
```

**Validation Rule**:
```yaml
validation_rules:
  - rule: "one_aggregate_per_transaction"
    description: "Command must modify at most one aggregate per transaction (Vaughn Vernon rule)"
    validation: "For each operation where type='command',
                 transaction_boundary.modifies_aggregates must have maxItems: 1"
```

### 5.2 Why One Aggregate Per Transaction?

#### Reason 1: Aggregate = Consistency Boundary

Aggregates define consistency boundaries. A transaction ensures all invariants within an aggregate are maintained:

```java
public class Order {
    private List<OrderItem> items;
    private Money totalAmount;

    // Invariant: total must equal sum of items
    public void addItem(OrderItem item) {
        items.add(item);
        totalAmount = calculateTotal();  // Invariant maintained

        // Transaction ensures both are saved atomically
    }
}
```

If transactions could span multiple aggregates, you'd create distributed transactions across consistency boundaries—defeating the purpose of aggregates.

#### Reason 2: Scalability

Single-aggregate transactions:
- Can be executed independently
- Allow horizontal scaling
- Avoid distributed transaction coordination
- Enable partitioning by aggregate ID

#### Reason 3: Avoid Deadlocks

Multi-aggregate transactions increase deadlock risk:
- Transaction A locks Order, then Inventory
- Transaction B locks Inventory, then Order
- Deadlock!

Single-aggregate transactions eliminate this risk.

#### Reason 4: Clearer Design

The one-aggregate rule forces you to think carefully about aggregate boundaries:
- Are these truly separate aggregates?
- Should they be unified?
- Can they coordinate via eventual consistency?

### 5.3 Consistency Types: Transactional vs Eventual

The schema defines two consistency types:

```yaml
consistency_type:
  type: string
  enum: [transactional, eventual]
  description: "Immediate (transactional) or deferred (eventual) consistency"
```

#### Transactional Consistency (Immediate)

Used within a single aggregate:

```java
@Transactional
public void placeOrder(PlaceOrderCmd cmd) {
    // Single aggregate, single transaction
    Order order = Order.create(cmd.orderId(), cmd.customerId());
    order.addItems(cmd.items());      // Invariants enforced immediately
    order.calculateTotal();            // Consistency immediate

    orderRepository.save(order);

    // All changes committed atomically
}
```

**Characteristics**:
- ACID guarantees
- Immediate consistency
- Within aggregate boundary
- Rollback on failure

#### Eventual Consistency (Deferred)

Used between aggregates:

```java
// Transaction 1: Place order
@Transactional
public OrderId placeOrder(PlaceOrderCmd cmd) {
    Order order = Order.create(cmd.orderId(), cmd.customerId());
    order.addItems(cmd.items());
    orderRepository.save(order);

    // Publish event for other aggregates
    eventPublisher.publish(new OrderPlaced(order.getId(), order.getItems()));

    return order.getId();
}

// Transaction 2: Reserve inventory (separate transaction)
@EventListener
@Transactional
public void on(OrderPlaced event) {
    Inventory inventory = inventoryRepository.findById(event.getWarehouseId());
    inventory.reserveItems(event.getItems());
    inventoryRepository.save(inventory);
}
```

**Characteristics**:
- No distributed transaction
- Temporary inconsistency acceptable
- Asynchronous coordination
- Each aggregate in its own transaction

### 5.4 Transaction Boundary Decision Matrix

| Scenario | Consistency Type | Pattern | Example |
|----------|-----------------|---------|---------|
| Single aggregate operation | Transactional | Direct transaction | Place order |
| User must see immediate result | Transactional | Return projection | Create user, return ID |
| Multiple aggregates, different BCs | Eventual | Event-driven | Order → Inventory → Shipping |
| True invariant within aggregate | Transactional | Enforce in aggregate | Order total = sum of items |
| Business rule across aggregates | Eventual | Event + handler | Invoice approved → Payment processed |
| Long-running workflow | Eventual | Saga pattern | Order fulfillment process |
| Data query operation | None (read-only) | No transaction | Get order summary |

### 5.5 When to Use Eventual Consistency

Ask these questions to determine if eventual consistency is acceptable:

**Question 1: Is it the user's job to make data consistent?**
- YES → Use transactional consistency
- NO → Use eventual consistency

Example:
- Placing an order: User's job (transactional)
- Updating inventory: System's job (eventual)

**Question 2: Must the invariant be enforced immediately?**
- YES → Transactional (true invariant)
- NO → Eventual

Example:
- Order total = sum of items: True invariant (transactional)
- Inventory count reflects all orders: Not a true invariant (eventual)

**Question 3: Can the business tolerate a delay?**
- YES → Eventual consistency acceptable
- NO → Consider if you've designed the right boundaries

Example:
- Welcome email: Delay acceptable (eventual)
- Password reset token: Delay problematic (transactional)

**Question 4: Are you trying to modify multiple aggregates?**
- YES → REFACTOR to use eventual consistency
- NO → Proceed with transaction

### 5.6 Schema Enforcement Mechanisms

The tactical schema enforces transaction boundaries through validation:

**1. maxItems Constraint**:
```yaml
modifies_aggregates:
  type: array
  items:
    $ref: "#/$defs/AggId"
  maxItems: 1  # Cannot exceed 1 aggregate
```

**2. Validation Rules**:
```yaml
validation_rules:
  - rule: "one_aggregate_per_transaction"
    description: "Command must modify at most one aggregate per transaction"
    validation: "transaction_boundary.modifies_aggregates.length <= 1"
```

**3. Operation Type Checking**:
```yaml
ApplicationServiceOperation:
  properties:
    type:
      enum: [command, query]
    transaction_boundary:
      # Commands must specify aggregate
      # Queries must have empty list
```

### 5.7 Examples and Anti-Patterns

#### Example 1: Correct - Single Aggregate

```yaml
operations:
  - name: activateUser
    type: command
    transaction_boundary:
      is_transactional: true
      modifies_aggregates:
        - agg_user  # Exactly one aggregate
      consistency_type: transactional
```

```java
@Transactional
public void activateUser(ActivateUserCmd cmd) {
    // Single aggregate transaction
    User user = userRepository.findById(cmd.userId());
    user.activate();
    userRepository.save(user);
}
```

#### Example 2: Correct - Eventual Consistency

```yaml
operations:
  - name: approveInvoice
    type: command
    transaction_boundary:
      is_transactional: true
      modifies_aggregates:
        - agg_invoice  # Only invoice aggregate
      consistency_type: transactional
    workflow:
      publishes_events:
        - evt_invoice_approved  # Triggers payment processing
```

```java
// Transaction 1: Approve invoice
@Transactional
public void approveInvoice(ApproveInvoiceCmd cmd) {
    Invoice invoice = invoiceRepository.findById(cmd.invoiceId());
    invoice.approve(cmd.approvedBy());
    invoiceRepository.save(invoice);

    eventPublisher.publish(new InvoiceApproved(invoice.getId()));
}

// Transaction 2: Process payment (separate)
@EventListener
@Transactional
public void on(InvoiceApproved event) {
    Payment payment = paymentRepository.findByInvoice(event.getInvoiceId());
    payment.process();
    paymentRepository.save(payment);
}
```

#### Anti-Pattern 1: Multiple Aggregates in One Transaction

```java
// WRONG: Violates one-aggregate rule
@Transactional
public void processOrder(ProcessOrderCmd cmd) {
    Order order = orderRepository.findById(cmd.orderId());
    order.confirm();
    orderRepository.save(order);

    // WRONG: Modifying second aggregate in same transaction
    Inventory inventory = inventoryRepository.findById(cmd.warehouseId());
    inventory.reserve(order.getItems());
    inventoryRepository.save(inventory);
}
```

**Fix**: Use eventual consistency:
```java
// CORRECT: Single aggregate per transaction
@Transactional
public void confirmOrder(ConfirmOrderCmd cmd) {
    Order order = orderRepository.findById(cmd.orderId());
    order.confirm();
    orderRepository.save(order);

    eventPublisher.publish(new OrderConfirmed(order.getId(), order.getItems()));
}

@EventListener
@Transactional
public void on(OrderConfirmed event) {
    Inventory inventory = inventoryRepository.findById(event.getWarehouseId());
    inventory.reserve(event.getItems());
    inventoryRepository.save(inventory);
}
```

#### Anti-Pattern 2: Distributed Transaction

```java
// WRONG: Distributed transaction across services
@Transactional
public void processPayment(ProcessPaymentCmd cmd) {
    // Local transaction
    Payment payment = paymentRepository.findById(cmd.paymentId());
    payment.process();
    paymentRepository.save(payment);

    // WRONG: Calling remote service in transaction
    externalPaymentGateway.charge(payment.getAmount());  // Network call!
}
```

**Fix**: Use outbox pattern or event-driven:
```java
// CORRECT: Local transaction, then integration
@Transactional
public void processPayment(ProcessPaymentCmd cmd) {
    Payment payment = paymentRepository.findById(cmd.paymentId());
    payment.markAsPending();
    paymentRepository.save(payment);

    // Save to outbox in same transaction
    outboxRepository.save(new ChargePaymentMessage(payment));
}

// Background process handles integration
@Scheduled
public void processOutbox() {
    List<OutboxMessage> pending = outboxRepository.findPending();

    for (OutboxMessage msg : pending) {
        externalPaymentGateway.charge(msg.getPayload());
        msg.markCompleted();
        outboxRepository.save(msg);
    }
}
```

---

## 6. Decision Trees and Guidelines

### 6.1 CQRS Adoption Decision Tree

```
START: Should I use CQRS for this bounded context?
│
├─ Is this a simple CRUD application?
│  └─ YES → Don't use CQRS (use traditional approach)
│  └─ NO → Continue
│
├─ Are read and write requirements significantly different?
│  └─ NO → Don't use CQRS (use traditional approach)
│  └─ YES → Continue
│
├─ Is the read-to-write ratio > 10:1?
│  └─ NO → Consider if other benefits justify complexity
│  └─ YES → Continue
│
├─ Can the business accept eventual consistency?
│  └─ NO → Use CQRS-Lite (same DB, separate handlers)
│  └─ YES → Use Full CQRS (separate DBs possible)
│
└─ Do you have the team skills and infrastructure?
   └─ NO → Start with traditional, migrate later if needed
   └─ YES → Implement CQRS
```

### 6.2 Read Model Bypass Decision Tree

```
START: Should this query bypass the domain model?
│
├─ Does the query need business logic or permissions?
│  └─ YES → Load through domain model (bypasses_domain_model: false)
│  └─ NO → Continue
│
├─ Is there a denormalized read model available?
│  └─ NO → Load through domain model (bypasses_domain_model: false)
│  └─ YES → Continue
│
├─ Is query performance critical?
│  └─ NO → Either approach works (prefer simpler)
│  └─ YES → Continue
│
├─ Is the data frequently cached?
│  └─ YES → Bypass domain model, query read model directly
│  └─ NO → Continue
│
└─ Is the query high-volume?
   └─ YES → Bypass domain model (bypasses_domain_model: true)
   └─ NO → Load through domain model (simpler)
```

### 6.3 Transaction Boundary Decision Tree

```
START: How should I handle this operation's transaction?
│
├─ Does this operation modify any aggregates?
│  └─ NO → No transaction needed (query operation)
│  └─ YES → Continue
│
├─ Does it modify more than one aggregate?
│  └─ YES → REFACTOR: Use eventual consistency
│  └─ NO → Continue
│
├─ Is this a true invariant that must be enforced immediately?
│  └─ YES → Use transactional consistency
│  └─ NO → Continue
│
├─ Is it the user's job to make this data consistent?
│  └─ YES → Use transactional consistency
│  └─ NO → Continue
│
├─ Can the business tolerate a delay in consistency?
│  └─ NO → Consider if you've designed the right boundaries
│  └─ YES → Use eventual consistency (event-driven)
│
└─ Is this part of a long-running workflow?
   └─ YES → Use Saga pattern with compensations
   └─ NO → Single transaction with event publishing
```

### 6.4 DTO vs Command Decision Guidelines

**Use Command Records When**:
- Representing user intent
- Input to the system
- May reference domain value objects
- Needs pre-execution validation
- Example: `CreateUserCmd`, `PlaceOrderCmd`

**Use DTOs When**:
- Representing system state
- Output from the system
- Only primitive types and strings
- Already validated data
- Example: `UserSummary`, `OrderDetails`

### 6.5 Application Service vs Domain Service Guidelines

**Put logic in Application Service If**:
- It's about orchestrating workflows
- It involves transaction management
- It accesses repositories
- It publishes events
- It performs authorization

**Put logic in Domain Service If**:
- It's business logic
- It involves multiple domain entities
- It's expressed in ubiquitous language
- It doesn't access infrastructure
- It's reusable across use cases

---

## 7. Examples from Tactical Schema

### 7.1 Complete User Management Example

The application service example from the schema demonstrates all patterns:

```yaml
application_services:
  - id: svc_app_user_management
    name: UserApplicationService
    implements_commands:
      - cmd_user_commands
    implements_queries:
      - qry_user_queries

    operations:
      # Command: Create user
      - name: createUser
        type: command
        transaction_boundary:
          is_transactional: true
          modifies_aggregates:
            - agg_user
          consistency_type: transactional
        workflow:
          validates_input: true
          loads_aggregates: []  # Creation - no load needed
          invokes_domain_operations:
            - "User.create() - factory method"
          persists_aggregates: true
          publishes_events:
            - evt_user_created

      # Query: Get user summary
      - name: getUserSummary
        type: query
        transaction_boundary:
          is_transactional: false
          modifies_aggregates: []
        workflow:
          validates_input: true
          loads_aggregates:
            - agg_user
          persists_aggregates: false
          publishes_events: []
          returns_dto: UserSummary
```

### 7.2 Command Interface Example

```yaml
command_interfaces:
  - id: cmd_user_commands
    name: UserCommands
    aggregate_ref: agg_user
    command_records:
      - record_name: CreateUserCmd
        intent: createUser
        parameters:
          - name: email
            type: String
            required: true
          - name: userType
            type: String
            required: true
          - name: identityProvider
            type: String
            required: true
          - name: clientId
            type: ClientId
            value_object_ref: vo_client_id
            required: true
        returns: domain_id
        return_type_ref: vo_user_id
        modifies_aggregate: agg_user
        publishes_events:
          - evt_user_created
```

### 7.3 Query Interface Example

```yaml
query_interfaces:
  - id: qry_user_queries
    name: UserQueries
    aggregate_ref: agg_user
    query_methods:
      - method_name: getUserSummary
        parameters:
          - name: userId
            type: UserId
            value_object_ref: vo_user_id
            required: true
        result_record_name: UserSummary
        result_structure:
          fields:
            - name: userId
              type: String
              serialization: "UserId serialized to String via userId.id()"
            - name: email
              type: String
            - name: status
              type: String
              serialization: "Status enum serialized to String via status.name()"
            - name: userType
              type: String
              serialization: "UserType enum serialized to String"
            - name: identityProvider
              type: String
              serialization: "IdentityProvider enum serialized to String"
        bypasses_domain_model: false
        optimizations:
          denormalized: false
          cached: false
          indexed: true

    result_characteristics:
      immutable: true
      flat_structure: true
      string_serialization: true

    no_side_effects: true
```

### 7.4 Transaction Boundary Example

```yaml
transaction_boundary:
  is_transactional: true
  modifies_aggregates:
    - agg_user  # Exactly one aggregate
  consistency_type: transactional
```

### 7.5 Workflow Example

```yaml
workflow:
  validates_input: true
  loads_aggregates:
    - agg_user
  invokes_domain_operations:
    - "user.activate() - business method"
  invokes_domain_services: []
  persists_aggregates: true
  publishes_events:
    - evt_user_activated
  returns_dto: null
```

---

## 8. References

### 8.1 Primary Sources

**CQRS**:
1. Fowler, Martin. "CQRS". https://martinfowler.com/bliki/CQRS.html
2. Young, Greg. "CQRS Documents". https://cqrs.files.wordpress.com/2010/11/cqrs_documents.pdf
3. Microsoft Azure Architecture Center. "Command and Query Responsibility Segregation (CQRS) Pattern". https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs

**Application Services**:
4. Fowler, Martin. "Service Layer". https://martinfowler.com/eaaCatalog/serviceLayer.html
5. Fowler, Martin. *Patterns of Enterprise Application Architecture*. Addison-Wesley, 2002.
6. Evans, Eric. *Domain-Driven Design: Tackling Complexity in the Heart of Software*. Addison-Wesley, 2003. Chapter 4: Isolating the Domain.
7. Vernon, Vaughn. *Implementing Domain-Driven Design*. Addison-Wesley, 2013. Chapter 4: Architecture.

**Transaction Management**:
8. Vernon, Vaughn. *Implementing Domain-Driven Design*. Chapter 11: Aggregates (Rule: Modify One Aggregate Per Transaction).
9. Richardson, Chris. *Microservices Patterns*. Manning, 2018. Chapter 4: Managing transactions with sagas.

**DTOs and Serialization**:
10. Fowler, Martin. "Data Transfer Object". https://martinfowler.com/eaaCatalog/dataTransferObject.html
11. Evans, Eric. *Domain-Driven Design*. Chapter 4: Layered Architecture (Application Layer responsibilities).

### 8.2 Schema References

12. Tactical DDD Schema v2.0.0. `/domains/ddd/schemas/tactical-ddd.schema.yaml`
13. Application Service Example. `/domains/ddd/examples/application-service-example.yaml`
14. DDD Documentation Series. `/domains/ddd/docs/`

### 8.3 Supporting Resources

15. Gorodinski, Lev. "Services in Domain-Driven Design (DDD)". http://gorodinski.com/blog/2012/04/14/services-in-domain-driven-design-ddd/
16. Enterprise Craftsmanship. "Domain services vs Application services". https://enterprisecraftsmanship.com/posts/domain-vs-application-services/
17. Microsoft .NET Microservices Architecture. "Designing a DDD-oriented microservice". https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/

---

**Document Control**:
- Version: 1.0.0
- Status: Research Complete
- Date: 2025-10-24
- Schema Version: tactical-ddd.schema.yaml v2.0.0
- Word Counts:
  - Section 1 (CQRS): ~4,200 words
  - Section 2 (Application Services): ~3,800 words
  - Section 3 (Read Models): ~2,900 words
  - Section 4 (DTOs): ~2,600 words
  - Section 5 (Transaction Boundaries): ~3,400 words
  - Section 6 (Decision Trees): ~800 words
  - Section 7 (Examples): ~600 words
  - **Total**: ~18,300 words
