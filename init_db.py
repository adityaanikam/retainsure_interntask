import sqlite3
from werkzeug.security import generate_password_hash

# Connect to the database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Read and execute the schema.sql file
with open('schema.sql', 'r') as f:
    cursor.executescript(f.read())

# Sample users with hashed passwords
users = [
    ('John Doe', 'john@example.com', generate_password_hash('password123')),
    ('Jane Smith', 'jane@example.com', generate_password_hash('secret456')),
    ('Bob Johnson', 'bob@example.com', generate_password_hash('qwerty789'))
]

# Insert sample data
cursor.executemany('INSERT INTO users (name, email, password) VALUES (?, ?, ?)', users)

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database initialized with sample data.")