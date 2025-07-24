# Refactoring Changes

This document details the issues identified in the original codebase and the changes made to address them, as per the refactoring challenge.

## 1. Major Issues Identified

The original `app.py` had several critical issues that made it unsuitable for a production environment:

* **Security - SQL Injection**: The most severe vulnerability was the use of f-strings to construct SQL queries. This would allow an attacker to execute arbitrary SQL commands on the database simply by crafting a malicious request.
* **Security - Plain Text Passwords**: Passwords were stored and compared in plain text. If the database were ever exposed, all user credentials would be compromised instantly.
* **Code Organization**: All logic—including the Flask application, routes, and direct database calls—was located in the single `app.py` file, making the code difficult to read, maintain, and scale.
* **Error Handling**: The application lacked proper error handling. It would often crash on bad input (like malformed JSON) and returned plain string messages instead of structured JSON responses with appropriate HTTP status codes.
* **Database Connection Management**: A single global database connection was used, which is not safe for the multi-threaded environments typical of web servers.

## 2. Changes Made and Justification

### a. Code Organization
I restructured the project to follow the principle of **separation of concerns**:

* **`database.py`**: A new file was created to abstract all database operations. This centralizes database logic, making the main `app.py` file cleaner and the database code reusable.
* **`schema.sql`**: A new SQL file now defines the database schema. This is a standard practice that separates the data structure from the application logic.
* **`tests/`**: A new directory was added to house tests, separating testing code from application code.

### b. Security Enhancements
Security was the top priority:

* **Preventing SQL Injection**: All SQL queries in `database.py` now use **parameterized statements** (`?` placeholder). This is the standard, effective way to prevent SQL injection attacks because it separates the SQL command from the user-supplied data.
* **Password Hashing**: I used the `generate_password_hash` and `check_password_hash` functions from **Werkzeug** (a core Flask dependency) to handle passwords securely. Passwords are now hashed before being stored, and the login endpoint compares the hash of the provided password against the stored hash.

### c. Best Practices and Code Quality
Several improvements were made to align with modern web development standards:

* **JSON Responses & Status Codes**: All endpoints now return structured **JSON responses** and use appropriate **HTTP status codes** (e.g., `200 OK`, `201 Created`, `404 Not Found`, `400 Bad Request`). This makes the API predictable and easier for client applications to consume.
* **Database Connection Management**: The database connection is now managed on a **per-request basis** using Flask's application context (`g`). This is a much safer and more robust pattern for web applications.
* **Input Validation**: Basic checks were added to ensure that required data is present in `POST` and `PUT` requests, preventing errors from incomplete data.

## 3. Assumptions and Trade-offs

* **Simplicity Over New Dependencies**: I intentionally avoided adding new major libraries (like SQLAlchemy or Flask-RESTful) to keep the solution simple and focused on fixing the core issues with the existing tools, as per the "What NOT to Do" section of the `README.md`.
* **Minimal Testing**: As instructed, I wrote a few critical tests for user creation and login functionality in `tests/test_app.py` rather than aiming for comprehensive test coverage.

## 4. What I Would Do With More Time

* **Configuration Management**: I would move configuration details (like the database name) into a separate configuration file or environment variables instead of hardcoding them.
* **Advanced Validation**: I would integrate a library like `Flask-Marshmallow` or `Pydantic` for more robust and declarative data validation and serialization (converting database objects to JSON).
* **Authentication Mechanism**: For a real production app, I would implement a more stateless and scalable authentication system using JWT (JSON Web Tokens) instead of a simple success/fail login response.