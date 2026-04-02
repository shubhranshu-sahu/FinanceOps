# FinanceOps

FinanceOps is a backend-driven finance dashboard system designed to manage financial transactions with role-based access control. It demonstrates clean backend architecture, secure data handling, and scalable API design using Flask and MySQL.

---

## 🚀 Features

* User authentication and management
* Role-based access control (Viewer, Analyst, Admin)
* Financial transaction management (income/expense)
* Filtering and querying transactions
* Dashboard analytics (totals, category breakdown, trends)
* Input validation and error handling

---

## 🏗️ Tech Stack

### Backend

* Flask
* SQLAlchemy
* MySQL
* Alembic (database migrations)

### Frontend

* HTML, CSS, JavaScript (minimal UI for testing APIs)

---

## 📁 Project Structure

```
FinanceOps/
│
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── schemas/
│   │   ├── middleware/
│   │   ├── utils/
│   │   └── __init__.py
│   │
│   ├── config/
│   ├── migrations/
│   ├── run.py
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── index.html
│   ├── css/
│   ├── js/
│   └── pages/
│
├── README.md
└── .gitignore
```

---

## 🔐 Role-Based Access Control

The system supports three roles:

* **Viewer** → Read-only access
* **Analyst** → Can view records and analytics
* **Admin** → Full access (CRUD + user management)

### User Flow

* Users can register publicly
* Default role assigned: **Viewer**
* Admins can promote users to Analyst or Admin
* Access control enforced at backend level

---

## 💰 Financial Records

Each transaction includes:

* Amount
* Type (income / expense)
* Category
* Date
* Description

Supported operations:

* Create
* Read
* Update
* Delete
* Filter by date, type, category

---

## 📊 Dashboard APIs

The backend provides aggregated insights such as:

* Total income
* Total expenses
* Net balance
* Category-wise breakdown
* Recent transactions
* Monthly trends

---

## ⚙️ Setup Instructions

### 1. Clone Repository

```bash
git clone <repo-url>
cd FinanceOps
```

### 2. Backend Setup

```bash
cd backend
python -m venv myenv
myenv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 3. Configure Environment

Create `.env` file in backend:

```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=financeops
SECRET_KEY=your_secret_key
```

### 4. Run Migrations

```bash
alembic upgrade head
```

### 5. Run Server

```bash
python run.py
```

---

## 🧠 Design Principles

* Clean separation of concerns (routes, services, models)
* Backend-first architecture
* Scalable and maintainable code structure
* Secure role-based access control
* Proper validation and error handling

---

## 👨‍💻 Author

Shubhranshu
