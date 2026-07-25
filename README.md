# Expense Tracker REST API

A secure and scalable RESTful Expense Tracker API built with **FastAPI**, **SQLAlchemy**, **SQLite**, and **JWT Authentication**. The application enables users to securely manage their expenses with features like authentication, CRUD operations, expense analytics, filtering, searching, sorting, and pagination.

## Features

### Authentication
- User Registration
- User Login
- JWT-based Authentication
- Password Hashing using Passlib
- OAuth2 Bearer Token Authentication
- Protected Endpoints

### Expense Management
- Create Expense
- View All Expenses
- View Expense by ID
- Update Expense
- Delete Expense

### Analytics
- Expense Summary
    - Total Expenses
    - Total Transactions
    - Highest Expense
    - Average Expense

### Advanced Query Features
- Category Filtering
- Title Search
- Sorting
    - Date
    - Amount
    - Title
    - Category
- Pagination

---

# Tech Stack

| Technology | Purpose |
|------------|---------|
| FastAPI | Backend Framework |
| Python | Programming Language |
| SQLAlchemy | ORM |
| SQLite | Database |
| JWT (python-jose) | Authentication |
| Passlib + bcrypt | Password Hashing |
| Pydantic | Data Validation |
| Uvicorn | ASGI Server |

---

# Project Structure

```
ExpenseTrackerAPI/
│
├── app/
│   ├── auth.py
│   ├── crud.py
│   ├── database.py
│   ├── dependencies.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── utils.py
│   └── routers/
│       ├── auth.py
│       └── expenses.py
│
├── requirements.txt
├── README.md
├── .gitignore
└── expense.db
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/ShreshthaJha6/Expense-Tracker-API.git
cd Expense-Tracker-API
```

## Create Virtual Environment

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Run the Server

```bash
python -m uvicorn app.main:app --reload
```

Server:

```
http://127.0.0.1:8000
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

ReDoc:

```
http://127.0.0.1:8000/redoc
```

---
## Running with Docker

### Build the image

```bash
docker build -t expense-tracker-api .
```

### Run the container

```bash
docker run -d -p 8000:8000 --name expense-api expense-tracker-api
```

### Stop the container

```bash
docker stop expense-api
```

### Remove the container

```bash
docker rm expense-api
```

The API will be available at:

```
http://localhost:8000/docs
```
---

# Authentication Flow

1. Register a new user

```
POST /register
```

2. Login

```
POST /login
```

3. Copy the generated JWT access token.

4. Click **Authorize** in Swagger and authenticate using the Bearer token.

5. Access all protected expense endpoints.

---

# API Endpoints

## Authentication

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/register` | Register a new user |
| POST | `/login` | User Login |
| GET | `/me` | Get current user profile |

---

## Expenses

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/expenses` | Create Expense |
| GET | `/expenses` | Get Expenses |
| GET | `/expenses/{id}` | Get Expense by ID |
| PUT | `/expenses/{id}` | Update Expense |
| DELETE | `/expenses/{id}` | Delete Expense |
| GET | `/expenses/summary` | Expense Analytics |

---

# Query Parameters

Filtering

```
GET /expenses?category=Food
```

Search

```
GET /expenses?search=dominos
```

Sorting

```
GET /expenses?sort_by=amount&order=desc
```

Pagination

```
GET /expenses?skip=0&limit=10
```

Combined Example

```
GET /expenses?category=Food&search=pizza&sort_by=date&order=desc&skip=0&limit=5
```

---

# Example Expense Summary Response

```json
{
  "total_expenses": 3100,
  "total_transactions": 4,
  "highest_expense": 1500,
  "average_expense": 775
}
```

---

# Security

- JWT Authentication
- Password Hashing
- User-specific Expense Authorization
- Input Validation using Pydantic
- Protected API Routes

---

# Future Improvements

- Docker Support
- PostgreSQL Integration
- Alembic Database Migrations
- Role-Based Authorization
- Expense Charts & Dashboard
- Monthly Budget Tracking
- Email Notifications

---

# Author

**Shreshtha Jha**

GitHub: https://github.com/ShreshthaJha6

---

# License

This project is intended for educational and portfolio purposes.