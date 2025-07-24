# User Management API

A simple and secure RESTful API for user management, built with Flask. This project is the result of refactoring a legacy codebase to improve security, organization, and maintainability.

---

## Features

* **CRUD Operations**: Full Create, Read, Update, and Delete functionality for users.
* **Secure Authentication**: Passwords are never stored in plain text. Hashing is handled by Werkzeug.
* **SQL Injection Protection**: Uses parameterized queries to prevent SQL injection attacks.
* **Organized Codebase**: The project is structured with a clear separation of concerns (app, database, schema).
* **Testing Suite**: Includes a basic set of unit tests for critical functionality.
* **Standardized Responses**: Returns structured JSON responses with appropriate HTTP status codes.

---

## Project Structure

The codebase is organized to separate the web layer from the data layer.

```
.
├── app.py              # Main Flask app with routes
├── database.py         # Handles all database interactions
├── init_db.py          # Script to initialize the database
├── schema.sql          # Contains the database table structure
├── requirements.txt    # Project dependencies
├── CHANGES.md          # Documents the refactoring process
└── tests/
    └── test_app.py     # Unit tests for the API
```

---

## Setup and Running

Follow these steps to get the application running locally.

### 1. Prerequisites
- Python 3.8+

### 2. Installation

```bash
# Clone this repository
git clone <https://github.com/adityaanikam/retainsure_interntask>
cd <retainsure_interntask>

# Install dependencies
pip install -r requirements.txt
```

### 3. Initialize the Database

This script will create a `users.db` file with the required schema and some sample data.

```bash
python init_db.py
```

### 4. Start the Application

```bash
python app.py

# The API will be running at http://localhost:5000
```

---

## API Endpoints

| Method | Endpoint              | Description                               |
| :---   | :-------------------- | :---------------------------------------- |
| `GET`  | `/`                   | Health check.                             |
| `GET`  | `/users`              | Get a list of all users.                  |
| `POST` | `/users`              | Create a new user.                        |
| `GET`  | `/user/<id>`          | Get a specific user by their ID.          |
| `PUT`  | `/user/<id>`          | Update a user's name or email.            |
| `DELETE`| `/user/<id>`          | Delete a user.                            |
| `GET`  | `/search`             | Search for users by name (e.g., `/search?name=John`). |
| `POST` | `/login`              | Authenticate a user and get their ID.     |

---

## Running Tests

This project includes a set of unit tests to verify core functionality.

**Important**: For consistent results, always reset your database before running the test suite.

```bash
# 1. Delete the existing database file (if it exists)
# (On Windows)
del users.db
# (On macOS/Linux)
rm users.db

# 2. Re-initialize the database
python init_db.py

# 3. Run the tests
python -m unittest tests/test_app.py
```

---

## 📞 Contact & Questions

For any questions about this implementation or approach:
- **Email:** adityanikam9502@gmail.com
- **LinkedIn:** https://www.linkedin.com/in/aditya-nikam-a23868250/
- **GitHub:** https://github.com/adityaanikam

---
## Refactoring Documentation

For a detailed explanation of the major issues identified in the original codebase and the changes that were implemented, please see the `CHANGES.md` file.