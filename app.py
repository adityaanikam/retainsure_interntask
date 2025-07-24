from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import database as db

app = Flask(__name__)
db.init_app(app)

# Helper function to convert user Row object to dictionary
def user_to_dict(user):
    if user:
        return {"id": user['id'], "name": user['name'], "email": user['email']}
    return None

@app.route('/')
def home():
    return "User Management System"

@app.route('/users', methods=['GET'])
def get_all_users():
    users = db.get_all_users()
    return jsonify([user_to_dict(user) for user in users]), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = db.get_user_by_id(user_id)
    if user:
        return jsonify(user_to_dict(user)), 200
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or 'name' not in data or 'email' not in data or 'password' not in data:
        return jsonify({"error": "Invalid data. Name, email, and password are required."}), 400

    name = data['name']
    email = data['email']
    password = data['password']

    hashed_password = generate_password_hash(password)
    new_user_id = db.create_user(name, email, hashed_password)

    return jsonify({"message": "User created", "user_id": new_user_id}), 201

@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = db.get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    if not data or ('name' not in data and 'email' not in data):
        return jsonify({"error": "Invalid data. Name or email is required."}), 400

    name = data.get('name', user['name'])
    email = data.get('email', user['email'])

    db.update_user(user_id, name, email)
    return jsonify({"message": "User updated"}), 200

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = db.get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.delete_user(user_id)
    return jsonify({"message": f"User {user_id} deleted"}), 200

@app.route('/search', methods=['GET'])
def search_users():
    name = request.args.get('name')
    if not name:
        return jsonify({"error": "Please provide a name to search"}), 400

    users = db.search_users_by_name(name)
    return jsonify([user_to_dict(u) for u in users]), 200

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"error": "Email and password are required."}), 400

    email = data['email']
    password = data['password']

    user = db.get_user_by_email(email)

    if user and check_password_hash(user['password'], password):
        return jsonify({"status": "success", "user_id": user['id']}), 200
    else:
        return jsonify({"status": "failed", "error": "Invalid credentials"}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)