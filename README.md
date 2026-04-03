# 🟩 FinanceOps Backend Architecture

**FinanceOps** is a highly governed, strictly structured financial data processing and access-control API framework. It is engineered primarily as a robust Backend demonstration, featuring a fully decoupled functional structure, impenetrable Role-Based Access Controls (RBAC), and aggressive data validation pipelines.

*(Note: Although this is a backend-focused architecture evaluation, a complimentary **Neobrutalism** styled Vanilla Javascript/HTML frontend was integrated to allow evaluators to easily simulate and test the API visually without strictly requiring Postman).*

---

## 🏗️ System Architecture & Modularity
The codebase is heavily modularized, cleanly separating traffic routing from core business logic to ensure maximal maintainability.

```text
backend/
├── app/
│   ├── middleware/       # JWT extraction and Role guards (@role_required)
│   ├── models/           # SQLAlchemy Data Models (User, Transaction, Category)
│   ├── routes/           # Endpoint controllers (auth, dashboard, txns)
│   ├── schemas/          # Marshmallow Validation mappings
│   ├── services/         # Pure Business Logic (Database interactions)
│   ├── utils/            # Cryptographic token processing
│   ├── __init__.py       # Application Factory & Globals
│   └── limiter.py        # Abstracted Rate Limiter configuration
├── migrations/           # Alembic Database state history
├── .env                  # Environmental configuration
├── requirements.txt      # Dependency map
└── run.py                # Server Ignition
```

---

## 🧠 Core Engineering Decisions & Tradeoffs

1. **Dynamic Category Mapping vs. Static Enums**
   - *Decision:* Rather than hard-coding categories (e.g., "Income", "Utilities") mathematically into a rigid Enum, the system leverages a dedicated `Category` SQL Table linked via Foreign Keys.
   - *Tradeoff:* Requires a slightly more complex JOIN operation during queries, but guarantees infinite flexibility for Admins to create new classification structures in real-time.

2. **Data Pipeline Validation (`flask-marshmallow`)**
   - *Decision:* In order to prevent fatal `500 Internal Python Kernel Crashes` stemming from `KeyError` payload discrepancies, we routed all `POST/PUT` data frames through a strict `Marshmallow` Schema layer.
   - *Result:* Invalid or missing properties automatically trip the barrier, commanding the server to yield a comprehensive `400 Bad Request` citing the exact missing index.

3. **Soft Delete Preservation vs. Hard Erasure**
   - *Decision:* Transactions and Users are rarely deleted forever. We modified the tables to hold an `is_deleted` or `is_active` boolean threshold.
   - *Result:* When an Admin "deletes" a transaction, it is shuttled into a "Recycle Bin" view, preserving system integrity and history until explicitly commanded to execute a `Permanent Delete`.

---

## 🔐 Security Assumptions & RBAC Implementation

Based on realistic financial industry logic, the following Role boundaries and strict assumptions were codified into the `@role_required` middleware:

- **VIEWER:** Restricted completely to the Analytics Summary endpoint. *Assumption:* Viewers are upper-management who don't need to see individual ledger items, but strictly desire high-level numerical aggregation data. Banned from `/transactions`.
- **ANALYST:** Permitted to query, filter, sort, and extrapolate all raw Transactions. *Assumption:* Analysts observe but do not manipulate active ledgers. Banned from `POST / PUT / DELETE` endpoints and actively blocked from viewing the Soft-Deleted Recycle Bin.
- **ADMIN:** Absolute Override Authority. Capable of mutating User classifications, appending ledgers, and permanently erasing data.

*All structural requests demand a cryptographically signed JSON Web Token (JWT).*

---

## 🚀 Additional Enhancements Executed
In direct alignment with the assignment's "Bonus Enhancements" checklist, the following systems were integrated:
- ✅ **Authentication:** Complete JWT generation, decoding, and session authorization.
- ✅ **Pagination:** `per_page` & `page` mappings natively driven into SQLAlchemy.
- ✅ **Search & Filter:** `ilike` substring mapping across string parameters natively in the database.
- ✅ **Soft Deletes:** Preserving data integrity by hiding rows.
- ✅ **Rate Limiting:** `Flask-Limiter` actively protects `/login` pipelines from brute force (5/min).

---

## ⚙️ Setup & Initiation Playbook

### 1. Database 
Ensure your local `MySQL` engine is running. Create an empty database (e.g. `financeops`).
Copy the blueprint configuration into a functional `.env` file inside `/backend`:
```env
DATABASE_URL=mysql+pymysql://<user>:<password>@localhost/financeops
SECRET_KEY=YOUR_SECURE_KEY
CORS_ORIGINS=http://127.0.0.1:5500,http://localhost:5500
```

### 2. Environment Bootstrap
Launch your terminal inside the `/backend` directory:
```bash
# Formulate virtual environment
python -m venv venv
venv\Scripts\activate

# Install exact payload dependencies (Flask, SQLAlchemy, Marshmallow, etc.)
pip install -r requirements.txt

# Migrate the database schemas into MySQL
flask db upgrade

# Ignite the Application
python run.py
```

### 3. Automated Unit Testing Sandbox
The system features a decoupled `pytest` validation suite. Running tests will spin up an isolated **in-memory SQLite database** (`sqlite:///:memory:`), execute 6 simulated REST request workflows (checking Authentication, RBAC, and Marshmallow failure captures), and then safely delete the memory block without polluting your real MySQL Database.

```bash
# Execute the testing module from the backend directory:
$env:PYTHONPATH="."  # Set the environment path
pytest tests/ -v     # Ignite the Pytest Engine
```

### 4. API Documentation
Every endpoint, method, and behavioral configuration has been meticulously mapped.  
👉 **[Click here to read the complete API Documentation](API_DOCS.md)**
