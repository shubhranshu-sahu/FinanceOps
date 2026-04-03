# 📡 FinanceOps API Reference Documentation

This document outlines the complete RESTful HTTP structure for the FinanceOps backend.

### 🛑 Global Authorization Rules
Except for the `/auth` endpoints, **EVERY** endpoint requires a validated JSON Web Token.
**Header Injection:**
```http
Authorization: Bearer <your_jwt_token_here>
```

Failure to supply a valid token will yield `401 Unauthorized`.
Attempting an action beyond your Role's permissions yields `403 Forbidden`.

---

## 🛡️ Authentication Pipeline

### 1. Register User
Registers a new user into the database. (Default role assigned internally is typically `VIEWER`).
- **Path:** `POST /auth/register`
- **Access Level:** Public
- **Rate Limit:** 5 requests per minute

**Request Payload:**
```json
{
  "name": "Jane Finance",
  "email": "jane@example.com",
  "password": "securepassword123"
}
```

**Success Response (201 Created):**
```json
{
  "message": "User registered successfully"
}
```

### 2. Login & Token Generation
Authenticates a user and generates the JWT signature required for all subsequent operations.
- **Path:** `POST /auth/login`
- **Access Level:** Public
- **Rate Limit:** 5 requests per minute

**Request Payload:**
```json
{
  "email": "jane@example.com",
  "password": "securepassword123"
}
```

**Success Response (200 OK):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5c... (Base64 JWT)",
  "user": {
    "id": 16,
    "email": "jane@example.com",
    "role": "ADMIN"
  }
}
```
**Error Response (401 Unauthorized):** `{"error": "Invalid password"}`

---

## 📊 Dashboard Analytics

### 3. Fetch Dashboard Summaries
Performs heavy structural database aggregation for plotting high-level numbers for interfaces.
- **Path:** `GET /dashboard/summary`
- **Access Level:** `VIEWER`, `ANALYST`, `ADMIN`

**Success Response (200 OK):**
```json
{
  "total_income": 45000.50,
  "total_expense": 12000.00,
  "net_balance": 33000.50,
  "category_breakdown": [
    { "category": "Corporate Sales", "total": 45000.50 },
    { "category": "Server Infrastructure", "total": 12000.00 }
  ],
  "recent_transactions": [
    {
      "id": 104,
      "amount": 12000.00,
      "type": "EXPENSE",
      "category": "Server Infrastructure",
      "date": "2026-04-03"
    }
  ],
  "monthly_trends": [
    { "month": "2026-04", "total": 33000.50 }
  ]
}
```

---

## 💵 Transaction Management

### 4. Fetch Transactions (With Filtering / Pagination)
Retrieves the raw ledger of data vectors alongside extensive dynamic filtration parameters.
- **Path:** `GET /transactions`
- **Access Level:** `ANALYST`, `ADMIN` *(Viewers will hit 403 Forbidden).*

**Query Parameters:**
- `page` (int, default: 1)
- `per_page` (int, default: 10)
- `deleted` (bool, default: false) - Access Soft-Deleted Bin. *(403 Forbidden for Analysts)*.
- `search` (str) - Searches description substring.
- `type` (str) - `INCOME` or `EXPENSE`.
- `category_id` (int) - The integer ID of the parent category.
- `date` (str) - `YYYY-MM-DD`.
- `sort_by` (str) - Options: `date_desc`, `date_asc`, `amount_desc`, `amount_asc`.

**Success Response (200 OK):**
```json
{
  "transactions": [
    {
      "id": 44,
      "amount": 350.0,
      "type": "EXPENSE",
      "category": "Advertising",
      "date": "2026-04-02",
      "description": "Google Ads Campaign",
      "created_by": 16
    }
  ],
  "total": 54,
  "pages": 6,
  "page": 1
}
```

### 5. Insert Transaction
Appends a new financial record to the Active database. Protected by `Marshmallow` validation schemas.
- **Path:** `POST /transactions`
- **Access Level:** `ADMIN`

**Request Payload:**
```json
{
  "amount": 12500.50,
  "type": "INCOME",
  "category_id": 3,
  "date": "2026-04-05",
  "description": "Q1 Retainer Fee"
}
```
**Success Response (201 Created):** `{"message": "Transaction created"}`  
**Error Response (400 Bad Request - Validation Error):** 
```json
{
  "error": "Validation failed",
  "fields": { "date": ["Missing data for required field."] }
}
```

### 6. Update/Edit Transaction
Modifies a pre-existing transaction row. Supports partial data updates.
- **Path:** `PUT /transactions/<int:id>`
- **Access Level:** `ADMIN`

**Request Payload (Example Partial Edit):**
```json
{
  "amount": 15000.00,
  "description": "Q1 Retainer Fee (Adjusted)"
}
```

### 7. Soft Delete Transaction
Moves a transaction to the Recycle Bin (`is_deleted=True`). It no longer affects Dashboard summaries, but remains accessible.
- **Path:** `DELETE /transactions/<int:id>`
- **Access Level:** `ADMIN`
- **Success Response (200 OK):** `{"message": "Transaction logically deleted"}`

### 8. Restore Transaction
Recovers a Soft-Deleted transaction back to the Active ledger.
- **Path:** `PUT /transactions/<int:id>/restore`
- **Access Level:** `ADMIN`

### 9. Permanent Delete Transaction
Executes raw SQL query to irreversibly drop the row from the database volume.
- **Path:** `DELETE /transactions/<int:id>/permanent`
- **Access Level:** `ADMIN`

---

## 🏷️ Category Schemas

### 10. Fetch Categories
- **Path:** `GET /categories`
- **Access Level:** `ANALYST`, `ADMIN`
- **Query Params:** `?all=true` (Will include `DISABLED` categories).

**Success Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Payroll",
    "is_active": true
  },
  {
    "id": 2,
    "name": "Infrastructure (Deprecated)",
    "is_active": false
  }
]
```

### 11. Create Category
- **Path:** `POST /categories`
- **Access Level:** `ADMIN`
- **Request Payload:** `{"name": "Legal Fees"}`

### 12. Rename Category
- **Path:** `PUT /categories/<int:id>`
- **Access Level:** `ADMIN`
- **Request Payload:** `{"name": "Contractor Legal Fees"}`

### 13. Toggle Category Status (Freeze Node)
Prevents a category from being used in future Transactions while retaining historical attachments.
- **Path:** `PUT /categories/<int:id>/status`
- **Access Level:** `ADMIN`
- **Request Payload:** `{"is_active": false}`

---

## 👥 Personnel / User Operations

### 14. List Associated Users
Extracts the identity matrix of all users on the platform.
- **Path:** `GET /users`
- **Access Level:** `ADMIN`

**Success Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "CEO Identity",
    "email": "ceo@corp.com",
    "role": "ADMIN",
    "is_active": true
  },
  {
    "id": 14,
    "name": "Data Node Worker",
    "email": "worker@corp.com",
    "role": "VIEWER",
    "is_active": true
  }
]
```

### 15. Modify / Escalate User Role
Transforms a user's RBAC classification on the backend routing level.
- **Path:** `PUT /users/<int:id>/role`
- **Access Level:** `ADMIN`
- **Request Payload:** `{"role": "ANALYST"}` *(Values: VIEWER, ANALYST, ADMIN).*

### 16. Freeze / Unfreeze System Access
Terminates a user's ability to extract dashboard endpoints via global session `HTTP 401 Unauthorized` locks without deleting them from the system.
- **Path:** `PUT /users/<int:id>/status`
- **Access Level:** `ADMIN`
- **Request Payload:** `{"is_active": false}`
