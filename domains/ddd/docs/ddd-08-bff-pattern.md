# DDD-08: Backend for Frontend (BFF) Pattern

**Version:** 1.0.0
**Status:** final
**Last Updated:** 2025-10-18
**Part of:** DDD Documentation Series

---

## Table of Contents

1. [Overview](#1-overview)
2. [BFF Scope and Purpose](#2-bff-scope-and-purpose)
3. [BFF vs API Gateway](#3-bff-vs-api-gateway)
4. [BFF Interface Design](#4-bff-interface-design)
5. [Integration with Application Services](#5-integration-with-application-services)
6. [OpenAPI Specification](#6-openapi-specification)
7. [Examples from Knight Codebase](#7-examples-from-knight-codebase)
8. [Best Practices](#8-best-practices)
9. [Anti-Patterns to Avoid](#9-anti-patterns-to-avoid)
10. [References](#10-references)

---

## 1. Overview

### 1.1 Definition

> "A server-side component tightly coupled to a specific user interface, providing one BFF per user interface type (web, mobile, tablet, etc.)."
> — Phil Calçado, "The Back-end for Front-end Pattern (BFF)"

The **Backend for Frontend (BFF)** pattern is an architectural pattern where you create separate backend services for different frontend experiences. Each BFF is optimized for a specific client type and owned by the team building that frontend.

### 1.2 Origin

First introduced by **Phil Calçado** and colleagues at **SoundCloud** in 2011, documented in the seminal article "The Back-end for Front-end Pattern (BFF)" (September 18, 2015). The pattern emerged from SoundCloud's transition from a monolithic Rails application to microservices architecture.

### 1.3 Key Principle

**"One experience, one BFF"**

- **Scope by Client:** One BFF serves ONE user interface type (web, iOS, Android, partner API)
- **Scope by Data:** One BFF aggregates data from MULTIPLE bounded contexts/microservices
- BFF scope is defined by CLIENT TYPE, not by bounded contexts

### 1.4 Core Characteristics

| Characteristic | Description |
|---------------|-------------|
| **Client-Specific** | Tailored to one client type |
| **Data Aggregation** | Combines data from multiple services |
| **Team Ownership** | Owned by frontend team (Conway's Law) |
| **Presentation Logic** | Contains client-specific logic, not business logic |
| **API Orchestration** | Coordinates multiple downstream calls |
| **Format Translation** | Transforms domain models to client formats |

---

## 2. BFF Scope and Purpose

### 2.1 Single UI Focus

**Principle:** Each BFF serves exactly **one type of user interface**

**Examples:**
- **Web BFF** → Serves web applications
- **iOS BFF** → Serves iOS mobile apps
- **Android BFF** → Serves Android mobile apps
- **Partner API BFF** → Serves third-party integrations
- **Desktop BFF** → Serves desktop applications
- **IoT BFF** → Serves IoT devices

**Why One BFF Per Client:**
- Different data needs (mobile needs less data due to bandwidth)
- Different authentication mechanisms
- Different performance requirements
- Different team ownership
- Independent evolution and deployment

### 2.2 Multiple Bounded Context Aggregation

**Critical Distinction:** BFF scope is defined by the CLIENT TYPE, not by bounded contexts.

A single BFF typically **aggregates data from multiple bounded contexts/microservices**.

**Example Scenario:**

```
User Dashboard (Web BFF)
    ↓ aggregates from
    ├─ User Context (user profile data)
    ├─ Order Context (recent orders)
    ├─ Payment Context (payment methods)
    ├─ Notification Context (unread notifications)
    └─ Analytics Context (usage statistics)
```

**Single BFF Endpoint:**
```http
GET /api/web/user-dashboard
```

**Aggregates data from 5 bounded contexts into unified response:**
```json
{
  "user": {
    "id": "user_123",
    "name": "John Doe",
    "email": "john@example.com"
  },
  "recentOrders": [
    { "orderId": "order_456", "status": "shipped" }
  ],
  "paymentMethods": [
    { "type": "credit_card", "last4": "1234" }
  ],
  "unreadNotifications": 5,
  "usageStats": {
    "loginCount": 42,
    "lastLogin": "2025-10-17"
  }
}
```

### 2.3 Core Responsibilities

#### What BFFs SHOULD Do:

1. **Data Aggregation**
   - Consolidate multiple downstream service calls into single endpoints
   - Example: Replace 5-10 API calls with one `GET /user-profile/123`
   - Make parallel or sequential downstream calls as needed

2. **Client-Specific Customization**
   - Provide API tailored to what that client type needs
   - Different data formats, granularity, and response structures per client
   - Platform-specific optimizations (mobile bandwidth vs. desktop)

3. **Presentation Logic**
   - Implement client-specific logic not shared across client types
   - Coordinate multiple bounded context interactions
   - Handle client-specific workflow requirements

4. **Format Translation**
   - Transform domain models into client-friendly formats
   - Map complex domain structures to view models
   - Aggregate data from multiple contexts into unified responses

5. **Error Handling**
   - Handle partial failures gracefully
   - Provide degraded responses when some services fail
   - Client-appropriate error messages

#### What BFFs Should NOT Do:

According to Sam Newman and Phil Calçado:

- **Generic cross-cutting concerns** (authentication, logging) → Use API Gateway upstream
- **Shared business logic** → Belongs in domain services, not duplicated across BFFs
- **Data persistence** → Delegate to downstream services
- **Direct database access** → Always call application services/microservices

### 2.4 Data Aggregation Strategies

**1. Parallel Calls** (when data is independent):
```java
CompletableFuture<User> userFuture =
    CompletableFuture.supplyAsync(() -> userService.getUser(userId));
CompletableFuture<List<Order>> ordersFuture =
    CompletableFuture.supplyAsync(() -> orderService.getOrders(userId));

CompletableFuture.allOf(userFuture, ordersFuture).join();

return new DashboardDTO(
    userFuture.get(),
    ordersFuture.get()
);
```

**2. Sequential Calls** (when data depends on prior responses):
```java
User user = userService.getUser(userId);
List<Order> orders = orderService.getOrders(user.getAccountId());
PaymentMethods payments = paymentService.getPaymentMethods(user.getAccountId());

return new DashboardDTO(user, orders, payments);
```

**3. Conditional Calls** (based on business logic):
```java
User user = userService.getUser(userId);

// Only fetch premium features for premium users
if (user.isPremium()) {
    PremiumFeatures features = premiumService.getFeatures(userId);
    return new PremiumDashboardDTO(user, features);
} else {
    return new StandardDashboardDTO(user);
}
```

### 2.5 Team Ownership and Conway's Law

**Conway's Law:**
> "Organizations design systems that mirror their communication structure."

**BFF Ownership Model:**
- **Owned by frontend team** developing the interface
- Enables independent evolution of frontend and backend
- Allows rapid iteration without cross-team dependencies
- **"One team, one BFF"** principle

**Benefits:**
1. Frontend teams retain autonomy over their API needs
2. Reduces bottlenecks from centralized API teams
3. Faster time-to-market for new features
4. Clear ownership boundaries
5. Frontend team understands client needs best

**Quote from Research:**
> "The simple act of limiting the number of consumers they support makes BFFs much easier to work with and change, and helps teams developing customer-facing applications retain more autonomy."

---

## 3. BFF vs API Gateway

### 3.1 API Gateway Pattern

**What is an API Gateway?**
- **Single point of entry** for all clients
- Provides **generic, cross-cutting concerns**
- Infrastructure-level pattern

**API Gateway Responsibilities:**
- SSL termination
- Authentication and authorization
- Rate limiting and throttling
- Request logging and monitoring
- Response caching
- Protocol translation (HTTP → gRPC)
- Load balancing

**When to Use API Gateway:**
- Single client type or very similar clients
- Need centralized infrastructure management
- Generic cross-cutting concerns only
- Simple pass-through with common transformations

**Limitations:**
- Becomes bloated when serving multiple diverse client types
- Difficult to optimize for specific clients
- Centralized team becomes bottleneck
- One size fits all approach

### 3.2 BFF Pattern

**What is a BFF?**
- **Multiple entry points**, one per client type
- Provides **client-specific API tailoring**
- Application-level pattern

**BFF Responsibilities:**
- Client-specific data aggregation
- View model composition
- Client-specific business logic
- Format transformation
- Client-optimized responses

**When to Use BFF:**
- Multiple diverse client types (web, mobile, IoT, partners)
- Different team ownership
- Varying authentication mechanisms
- Client-specific business logic needed
- Need to optimize independently per client
- Conway's Law: Team structure mirrors architecture

### 3.3 Decision Matrix

| Factor | Use API Gateway | Use BFF |
|--------|----------------|---------|
| **Number of client types** | 1-2 similar clients | 3+ diverse clients |
| **Team structure** | Single centralized team | Multiple client teams |
| **Business logic variance** | Minimal differences | Significant per client |
| **Authentication** | Uniform mechanism | Client-specific mechanisms |
| **Future scalability** | Limited growth expected | Ecosystem of apps planned |
| **Organizational structure** | Centralized control | Decentralized (Conway's Law) |
| **Primary need** | Cross-cutting concerns | Client optimization |
| **Data aggregation** | Simple pass-through | Complex multi-service aggregation |
| **Response format** | Standardized | Client-specific |

### 3.4 Hybrid Approach (Recommended)

**Best Practice:** Use BOTH patterns together

```
┌──────────────────┐
│   Web Client     │
└────────┬─────────┘
         │
┌────────▼──────────┐
│   API Gateway     │  ← Cross-cutting concerns
│  (SSL, Auth, etc) │
└────────┬──────────┘
         │
    ┌────┴────┬──────────┬──────────┐
    ▼         ▼          ▼          ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│Web BFF │ │iOS BFF │ │Android │ │Partner │
│        │ │        │ │  BFF   │ │API BFF │
└───┬────┘ └───┬────┘ └───┬────┘ └───┬────┘
    │          │          │          │
    └──────────┴──────────┴──────────┘
               │
         ┌─────┴──────┬──────────┬──────────┐
         ▼            ▼          ▼          ▼
    ┌────────┐  ┌────────┐ ┌────────┐ ┌────────┐
    │  User  │  │ Order  │ │Payment │ │Notify  │
    │Context │  │Context │ │Context │ │Context │
    └────────┘  └────────┘ └────────┘ └────────┘
```

**Layering:**
1. **API Gateway** (upstream) → Infrastructure concerns
2. **BFFs** (downstream) → Client-specific orchestration
3. **Microservices/Bounded Contexts** → Business logic

### 3.5 BFF vs API Gateway Summary

**API Gateway:**
- Infrastructure layer
- Owned by platform/infrastructure team
- Generic, reusable functionality
- One gateway for all clients
- Cross-cutting concerns only

**BFF:**
- Integration/Application layer
- Owned by frontend team
- Client-specific functionality
- One BFF per client type
- Data aggregation and orchestration

**Key Distinction:**
- API Gateway is about **infrastructure management**
- BFF is about **client optimization**

---

## 4. BFF Interface Design

### 4.1 REST Resource Mapping

**Principle:** BFF endpoints should align with **client use cases**, not just domain aggregates.

**Traditional Domain-Aligned API:**
```
GET /api/users/123
GET /api/users/123/orders
GET /api/users/123/payment-methods
GET /api/notifications?userId=123
```

**Client makes 4+ separate calls**

**BFF Client-Optimized API:**
```
GET /api/web/user-dashboard/123
```

**Single call returns aggregated response:**
```json
{
  "user": { "id": "123", "name": "John Doe" },
  "recentOrders": [...],
  "paymentMethods": [...],
  "unreadNotifications": 5
}
```

### 4.2 HTTP Verb to Command/Query Mapping

**CQRS Mapping in BFF:**

| Operation Type | HTTP Method | BFF Endpoint | Delegates To |
|---------------|-------------|--------------|--------------|
| **Query (single)** | GET | `/api/web/users/123` | GetUserQuery |
| **Query (collection)** | GET | `/api/web/users?status=active` | ListUsersQuery |
| **Command (create)** | POST | `/api/web/users` | CreateUserCommand |
| **Command (action)** | POST | `/api/web/users/123/activate` | ActivateUserCommand |
| **Command (update)** | PUT/PATCH | `/api/web/users/123` | UpdateUserCommand |
| **Command (delete)** | DELETE | `/api/web/users/123` | DeleteUserCommand |

**Knight Pattern (Command-Oriented):**

All commands use POST with action-based paths:

```
POST /commands/users/create
POST /commands/users/activate
POST /commands/users/deactivate
POST /commands/users/lock
```

**Benefits:**
- Clear intent (not just CRUD)
- Captures business operations
- Aligns with domain ubiquitous language
- Easier to extend with new operations

### 4.3 Request/Response DTOs

**Principle:** BFF DTOs are **separate** from API Command/Query records

**API Layer (Command Definition):**
```java
public interface UserCommands {
    record CreateUserCmd(
        String email,
        String userType,
        ClientId clientId
    ) {}
}
```

**BFF Layer (Request DTO):**
```java
@Controller("/api/web/users")
public class UserBFFController {

    // Separate DTO for BFF interface
    public record CreateUserRequest(
        String email,
        String userType,
        String clientUrn  // String, not ClientId
    ) {}

    @Post("/create")
    public CreateUserResult createUser(@Body CreateUserRequest req) {
        // Convert BFF DTO to API Command
        ClientId clientId = ClientId.of(req.clientUrn());
        var cmd = new UserCommands.CreateUserCmd(
            req.email(),
            req.userType(),
            clientId
        );

        // Delegate to application service
        UserId userId = userCommands.createUser(cmd);

        // Convert domain response to BFF DTO
        return new CreateUserResult(userId.id());
    }

    public record CreateUserResult(String userId) {}
}
```

**Why Separate DTOs:**
1. **Different serialization** - BFF uses strings, API uses value objects
2. **Client-specific fields** - BFF may add/remove fields per client
3. **Version independence** - BFF can evolve separately from API
4. **Clear boundaries** - BFF layer vs. API layer separation

### 4.4 Value Object Conversion

**BFF Responsibility:** Convert between **string URNs** and **value objects**

**Conversion Pattern:**

```java
// String → Value Object (incoming request)
ClientId clientId = ClientId.of(request.clientUrn());
UserId userId = UserId.of(request.userId());
ServicingProfileId profileId = ServicingProfileId.fromUrn(request.profileUrn());

// Value Object → String (outgoing response)
String clientUrn = clientId.urn();
String userId = userId.id();
String profileUrn = profileId.urn();
```

**Example in Controller:**

```java
@Post("/enroll-service")
public void enrollService(@Body EnrollServiceRequest req) {
    // Convert URN strings to value objects
    var profileId = ServicingProfileId.fromUrn(req.profileUrn());

    // Create command with value objects
    var cmd = new SpmCommands.EnrollServiceCmd(
        profileId,
        req.serviceType(),
        req.configurationJson()
    );

    // Delegate to application service
    commands.enrollService(cmd);
}

public record EnrollServiceRequest(
    String profileUrn,      // String in BFF
    String serviceType,
    String configurationJson
) {}
```

---

## 5. Integration with Application Services

### 5.1 BFF Delegates to Application Services

**Architectural Flow:**

```
Client Request
    ↓
BFF Controller (REST endpoint)
    ↓ converts DTO to Command
Application Service (use case orchestration)
    ↓ delegates business logic
Domain Aggregate (business rules)
    ↓ persisted via
Repository
    ↓
Database
```

**Key Principle:** BFF contains **no business logic**, only:
- Value object conversion
- Request/response mapping
- Error handling
- Client-specific formatting

### 5.2 No Business Logic in BFF

**❌ Anti-Pattern (Business Logic in BFF):**

```java
@Post("/create-order")
public CreateOrderResult createOrder(@Body CreateOrderRequest req) {
    // WRONG: Business logic in BFF
    BigDecimal total = BigDecimal.ZERO;
    for (OrderItem item : req.items()) {
        total = total.add(item.price().multiply(item.quantity()));
    }

    if (total.compareTo(new BigDecimal("1000")) > 0) {
        // WRONG: Business rule in BFF
        throw new OrderTooLargeException();
    }

    // ...
}
```

**✓ Correct Pattern (BFF Delegates):**

```java
@Post("/create-order")
public CreateOrderResult createOrder(@Body CreateOrderRequest req) {
    // Convert DTO to Command
    var cmd = new OrderCommands.PlaceOrderCmd(
        CustomerId.of(req.customerId()),
        req.items(),
        req.shippingAddress()
    );

    // Delegate to application service (business logic there)
    OrderId orderId = orderCommands.placeOrder(cmd);

    // Convert response
    return new CreateOrderResult(orderId.value());
}
```

### 5.3 BFF Integration Patterns

**Pattern 1: Single Context Call**

```java
@Get("/users/{userId}")
public UserProfileDTO getUserProfile(@PathVariable String userId) {
    // Single bounded context call
    var userSummary = userQueries.getUserSummary(UserId.of(userId));

    return new UserProfileDTO(
        userSummary.userId(),
        userSummary.email(),
        userSummary.status()
    );
}
```

**Pattern 2: Multi-Context Aggregation**

```java
@Get("/dashboard/{userId}")
public DashboardDTO getDashboard(@PathVariable String userId) {
    UserId id = UserId.of(userId);

    // Call multiple bounded contexts
    var userSummary = userQueries.getUserSummary(id);
    var orders = orderQueries.getRecentOrders(id);
    var notifications = notificationQueries.getUnreadCount(id);

    // Aggregate into client-specific DTO
    return new DashboardDTO(
        userSummary,
        orders,
        notifications
    );
}
```

**Pattern 3: Error Handling with Degraded Response**

```java
@Get("/dashboard/{userId}")
public DashboardDTO getDashboard(@PathVariable String userId) {
    UserId id = UserId.of(userId);

    var userSummary = userQueries.getUserSummary(id);

    // Gracefully handle service failures
    List<OrderSummary> orders;
    try {
        orders = orderQueries.getRecentOrders(id);
    } catch (ServiceUnavailableException e) {
        orders = Collections.emptyList(); // Degraded response
    }

    int notificationCount;
    try {
        notificationCount = notificationQueries.getUnreadCount(id);
    } catch (ServiceUnavailableException e) {
        notificationCount = 0; // Degraded response
    }

    return new DashboardDTO(userSummary, orders, notificationCount);
}
```

---

## 6. OpenAPI Specification

### 6.1 Role of OpenAPI Specs

**OpenAPI (formerly Swagger)** specifications define the contract for BFF interfaces:

- **API-First Design:** Define contract before implementation
- **Client Generation:** Generate client SDKs automatically
- **Documentation:** Self-documenting APIs
- **Validation:** Request/response validation
- **Testing:** Contract testing

### 6.2 BFF OpenAPI Structure

**Recommended Structure:**

```yaml
openapi: 3.0.3
info:
  title: User Management Web BFF API
  version: 1.0.0
  description: BFF API for web client user management features

servers:
  - url: https://api.example.com/web
    description: Production Web BFF
  - url: https://api-staging.example.com/web
    description: Staging Web BFF

paths:
  /users:
    post:
      summary: Create new user (Command)
      operationId: createUser
      tags:
        - User Commands
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
      responses:
        '201':
          description: User created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CreateUserResult'
        '400':
          $ref: '#/components/responses/BadRequest'
        '500':
          $ref: '#/components/responses/InternalError'

  /users/{userId}:
    get:
      summary: Get user profile (Query)
      operationId: getUserProfile
      tags:
        - User Queries
      parameters:
        - $ref: '#/components/parameters/UserId'
      responses:
        '200':
          description: User profile retrieved
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserProfileDTO'
        '404':
          $ref: '#/components/responses/NotFound'

  /users/{userId}/activate:
    post:
      summary: Activate user account (Command)
      operationId: activateUser
      tags:
        - User Commands
      parameters:
        - $ref: '#/components/parameters/UserId'
      responses:
        '200':
          description: User activated successfully
        '404':
          $ref: '#/components/responses/NotFound'

components:
  schemas:
    CreateUserRequest:
      type: object
      required:
        - email
        - userType
        - clientUrn
      properties:
        email:
          type: string
          format: email
          example: john.doe@example.com
        userType:
          type: string
          enum:
            - DIRECT
            - INDIRECT
        clientUrn:
          type: string
          pattern: '^(srf|gid|ind):[A-Za-z0-9_-]+$'
          example: srf:12345

    CreateUserResult:
      type: object
      properties:
        userId:
          type: string
          format: uuid

    UserProfileDTO:
      type: object
      properties:
        userId:
          type: string
        email:
          type: string
        status:
          type: string
          enum:
            - PENDING
            - ACTIVE
            - LOCKED
            - DEACTIVATED
        userType:
          type: string

  parameters:
    UserId:
      name: userId
      in: path
      required: true
      schema:
        type: string
        format: uuid

  responses:
    BadRequest:
      description: Invalid request
      content:
        application/json:
          schema:
            type: object
            properties:
              error:
                type: string
              message:
                type: string

    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            type: object
            properties:
              error:
                type: string

    InternalError:
      description: Internal server error
      content:
        application/json:
          schema:
            type: object
            properties:
              error:
                type: string
```

### 6.3 Task-Based Operations in OpenAPI

**Prefer task-based operations over generic CRUD:**

**✓ Good (Task-Based):**
```yaml
paths:
  /invoices/{invoiceId}/approve:
    post:
      summary: Approve invoice
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                approvedBy:
                  type: string
                approvalNotes:
                  type: string
```

**❌ Less Ideal (Generic CRUD):**
```yaml
paths:
  /invoices/{invoiceId}:
    patch:
      summary: Update invoice
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                status:
                  type: string
                updatedBy:
                  type: string
```

---

## 7. Examples from Knight Codebase

### 7.1 UserCommandController as BFF Endpoint

**Complete example from Knight:**

```java
@Controller("/commands/users")
@ExecuteOn(TaskExecutors.BLOCKING)
public class UserCommandController {

    @Inject
    UserCommands commands;

    @Post("/create")
    public CreateUserResult createUser(@Body CreateUserRequest req) {
        // 1. Convert URN string to value object
        var clientId = ClientId.of(req.clientUrn());

        // 2. Create command with value objects
        var userId = commands.createUser(new UserCommands.CreateUserCmd(
            req.email(),
            req.userType(),
            req.identityProvider(),
            clientId
        ));

        // 3. Convert domain ID to string for response
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
        commands.deactivateUser(new UserCommands.DeactivateUserCmd(
            userId,
            req.reason()
        ));
    }

    @Post("/lock")
    public void lockUser(@Body LockUserRequest req) {
        var userId = UserId.of(req.userId());
        commands.lockUser(new UserCommands.LockUserCmd(
            userId,
            req.reason()
        ));
    }

    @Post("/unlock")
    public void unlockUser(@Body UnlockUserRequest req) {
        var userId = UserId.of(req.userId());
        commands.unlockUser(new UserCommands.UnlockUserCmd(userId));
    }

    // BFF-specific DTOs (separate from API command records)
    public record CreateUserRequest(
        String email,
        String userType,
        String identityProvider,
        String clientUrn
    ) {}

    public record CreateUserResult(String userId) {}

    public record ActivateUserRequest(String userId) {}

    public record DeactivateUserRequest(String userId, String reason) {}

    public record LockUserRequest(String userId, String reason) {}

    public record UnlockUserRequest(String userId) {}
}
```

**Key Observations:**

1. **URL Pattern:** `/commands/{context}/{entity}/{action}`
2. **All POST:** No PUT/PATCH/DELETE verbs (command semantics)
3. **Blocking Execution:** `@ExecuteOn(TaskExecutors.BLOCKING)`
4. **String Conversion:** URN strings → value objects in controller
5. **Separate DTOs:** Request/Result records different from API commands
6. **No Business Logic:** Pure delegation to application service
7. **No Validation:** Validation happens in domain layer

### 7.2 Service Profile BFF Controller

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

    @Post("/enroll-account")
    public void enrollAccount(@Body EnrollAccountRequest req) {
        var profileId = ServicingProfileId.fromUrn(req.profileUrn());
        commands.enrollAccount(new SpmCommands.EnrollAccountCmd(
            profileId,
            req.serviceEnrollmentId(),
            req.accountId()
        ));
    }

    public record CreateProfileRequest(
        String clientUrn,
        String createdBy
    ) {}

    public record CreateProfileResult(String profileUrn) {}

    public record EnrollServiceRequest(
        String profileUrn,
        String serviceType,
        String configurationJson
    ) {}

    public record EnrollAccountRequest(
        String profileUrn,
        String serviceEnrollmentId,
        String accountId
    ) {}
}
```

**Pattern Highlights:**

1. **Nested Path:** `/commands/service-profiles/servicing` (multi-level context)
2. **URN Conversion:** `ServicingProfileId.fromUrn()` for compound IDs
3. **Audit Fields:** `createdBy` passed through controller
4. **Configuration:** JSON string for schema flexibility
5. **Hierarchical Operations:** Create profile → Enroll service → Enroll account

---

## 8. Best Practices

### 8.1 BFF Design Principles

1. **One BFF Per Client Type**
   - Web BFF for web applications
   - iOS BFF for iOS apps
   - Android BFF for Android apps
   - Partner API BFF for third-party integrations
   - Do NOT serve multiple client types from one BFF

2. **Owned by Frontend Team**
   - Team building the frontend owns the BFF
   - Conway's Law: Team structure mirrors architecture
   - Enables autonomy and rapid iteration
   - Frontend team knows client needs best

3. **Client-Optimized Responses**
   - Mobile: Minimize payload size, optimize for bandwidth
   - Web: Rich data, nested structures acceptable
   - Partner API: Stable contract, comprehensive data
   - IoT: Minimal data, highly compressed

4. **Aggregate from Multiple Contexts**
   - BFF should call multiple bounded contexts
   - Single endpoint replaces multiple client calls
   - Reduces network overhead
   - Simplifies client-side logic

5. **No Business Logic**
   - BFF contains presentation logic only
   - Delegate all business logic to domain services
   - Do NOT duplicate business rules across BFFs

### 8.2 API Design Best Practices

1. **Use Task-Based Operations**
   - `POST /orders/{id}/approve` (captures intent)
   - NOT `PATCH /orders/{id}` with `{status: "approved"}`
   - Aligns with domain ubiquitous language
   - Easier to extend with new operations

2. **Clear Endpoint Naming**
   - Use business domain terms
   - Follow consistent patterns across BFFs
   - Examples: `/user-dashboard`, `/order-history`, `/payment-methods`

3. **Version Your APIs**
   - Use semantic versioning (v1, v2)
   - BFFs can version independently of services
   - Maintain backward compatibility for public APIs
   - Example: `/api/v1/web/users`, `/api/v2/web/users`

4. **Error Handling**
   - Return client-appropriate error messages
   - Hide internal implementation details
   - Provide actionable error information
   - Use standard HTTP status codes

5. **Graceful Degradation**
   - Handle partial service failures
   - Return degraded responses when possible
   - Don't fail entire request if one service is down
   - Log failures for monitoring

### 8.3 Performance Optimization

1. **Parallel Calls**
   - Make independent service calls in parallel
   - Use async/CompletableFuture for aggregation
   - Reduce total latency

2. **Caching Strategies**
   - Cache frequently accessed data
   - Use client-specific cache TTLs
   - Invalidate cache on relevant events

3. **Response Size Optimization**
   - Mobile: Minimal fields, compressed payloads
   - Web: Full data, optional fields via parameters
   - Field selection: Allow clients to specify needed fields

4. **Pagination**
   - Implement pagination for large datasets
   - Mobile: Small page sizes (10-20 items)
   - Web: Larger page sizes (50-100 items)

### 8.4 Security Considerations

1. **Delegate to API Gateway**
   - Authentication handled by API Gateway upstream
   - BFF receives authenticated requests
   - BFF validates authorization for specific operations

2. **Input Validation**
   - Validate all incoming data
   - Sanitize inputs before delegating
   - Prevent injection attacks

3. **Rate Limiting**
   - Per-client rate limiting in API Gateway
   - BFF-specific rate limits if needed
   - Protect downstream services

4. **HTTPS Only**
   - All BFF endpoints must use HTTPS
   - No sensitive data in URLs
   - Secure headers (CORS, CSP)

---

## 9. Anti-Patterns to Avoid

### 9.1 Generic BFF (Serving Multiple Client Types)

**❌ Anti-Pattern:**

```java
@Controller("/api/generic")
public class GenericBFFController {

    @Get("/dashboard")
    public DashboardDTO getDashboard(
        @QueryValue String userId,
        @QueryValue String clientType  // WRONG: Client type parameter
    ) {
        if (clientType.equals("mobile")) {
            // Mobile-specific logic
        } else if (clientType.equals("web")) {
            // Web-specific logic
        }
        // ...
    }
}
```

**✓ Correct Pattern:**

```java
// Separate BFFs for each client
@Controller("/api/web")
public class WebBFFController {
    @Get("/dashboard/{userId}")
    public WebDashboardDTO getDashboard(@PathVariable String userId) {
        // Web-optimized response
    }
}

@Controller("/api/mobile")
public class MobileBFFController {
    @Get("/dashboard/{userId}")
    public MobileDashboardDTO getDashboard(@PathVariable String userId) {
        // Mobile-optimized response
    }
}
```

### 9.2 Business Logic in BFF

**❌ Anti-Pattern:**

```java
@Post("/create-order")
public CreateOrderResult createOrder(@Body CreateOrderRequest req) {
    // WRONG: Business logic in BFF
    if (req.items().size() > 100) {
        throw new TooManyItemsException();
    }

    BigDecimal total = calculateTotal(req.items()); // WRONG: Calculation in BFF

    if (total.compareTo(MINIMUM_ORDER) < 0) { // WRONG: Business rule in BFF
        throw new OrderTooSmallException();
    }

    // ...
}
```

**✓ Correct Pattern:**

```java
@Post("/create-order")
public CreateOrderResult createOrder(@Body CreateOrderRequest req) {
    // Delegate to application service (business logic there)
    var cmd = new OrderCommands.PlaceOrderCmd(
        CustomerId.of(req.customerId()),
        req.items()
    );

    OrderId orderId = orderCommands.placeOrder(cmd);
    return new CreateOrderResult(orderId.value());
}
```

### 9.3 Direct Database Access

**❌ Anti-Pattern:**

```java
@Get("/users/{userId}")
public UserProfileDTO getUserProfile(@PathVariable String userId) {
    // WRONG: Direct database query in BFF
    String sql = "SELECT * FROM users WHERE id = ?";
    UserEntity user = jdbcTemplate.queryForObject(sql, UserEntity.class, userId);

    return new UserProfileDTO(user.getId(), user.getEmail());
}
```

**✓ Correct Pattern:**

```java
@Get("/users/{userId}")
public UserProfileDTO getUserProfile(@PathVariable String userId) {
    // Delegate to application service/query handler
    var userSummary = userQueries.getUserSummary(UserId.of(userId));

    return new UserProfileDTO(
        userSummary.userId(),
        userSummary.email()
    );
}
```

### 9.4 Shared DTOs Across BFFs

**❌ Anti-Pattern:**

```java
// Shared DTO used by multiple BFFs
public record SharedUserDTO(
    String userId,
    String email,
    String status,
    // Too many fields for mobile
    String fullAddress,
    List<OrderHistory> orders,
    Map<String, Object> preferences
) {}

// Web BFF uses all fields
// Mobile BFF wastes bandwidth on unused fields
```

**✓ Correct Pattern:**

```java
// Web-specific DTO (comprehensive)
public record WebUserDTO(
    String userId,
    String email,
    String status,
    String fullAddress,
    List<OrderHistory> orders,
    Map<String, Object> preferences
) {}

// Mobile-specific DTO (minimal)
public record MobileUserDTO(
    String userId,
    String email,
    String status
) {}
```

### 9.5 BFF Calling BFF

**❌ Anti-Pattern:**

```
Web BFF → Mobile BFF → Application Services
```

**✓ Correct Pattern:**

```
Web BFF → Application Services
Mobile BFF → Application Services
```

BFFs should **never call each other**. Each BFF calls application services directly.

---

## 10. References

### Primary Sources

1. **Calçado, Phil.** "The Back-end for Front-end Pattern (BFF)". September 18, 2015.
   https://philcalcado.com/2015/09/18/the_back_end_for_front_end_pattern_bff.html

2. **Newman, Sam.** "Backends For Frontends".
   https://samnewman.io/patterns/architectural/bff/

3. **Newman, Sam.** *Building Microservices: Designing Fine-Grained Systems, 2nd Edition*. O'Reilly Media, 2021.

4. **ThoughtWorks.** "BFF @ SoundCloud".
   https://www.thoughtworks.com/insights/blog/bff-soundcloud

### Supporting Research

5. **Richardson, Chris.** *Microservices Patterns*. Manning Publications, 2018.

6. **Cloud Adoption Patterns.** "Backend for Frontend".
   https://kgb1001001.github.io/cloudadoptionpatterns/Microservices/Backend-For-Frontend/

7. **Microservices.io Pattern Catalog.** Chris Richardson.
   https://microservices.io/patterns/

8. **Microsoft Azure Architecture Center.** "Backends for Frontends pattern".
   https://learn.microsoft.com/en-us/azure/architecture/patterns/backends-for-frontends

### Related Patterns

9. **API Gateway Pattern** - Complementary pattern often used with BFF
10. **Strangler Fig Pattern** - Migration strategy for introducing BFFs
11. **Aggregate Pattern** - How BFFs combine data from multiple sources

### Internal References

- [DDD-01: DDD Foundations](ddd-01-ddd-foundations.md)
- [DDD-02: Strategic Patterns](ddd-02-strategic-patterns.md)
- [DDD-07: Application Layer](ddd-07-application-layer.md)

---

**Document Control:**
- Version: 1.0.0
- Status: final
- Last Updated: 2025-10-18
- Approved By: DDD Documentation Team
