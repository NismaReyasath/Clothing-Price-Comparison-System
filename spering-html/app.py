from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)  # Enable CORS to allow frontend requests

# Database Connection
db = pymysql.connect(
    host="localhost",
    user="root",  # Change if necessary
    password="2332",  # Change if necessary
    database="price_compare"
)
cursor = db.cursor()

# Signup Route
@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.json
        fullname = data.get("fullname")
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not fullname or not username or not email or not password:
            return jsonify({"status": "error", "message": "All fields are required."}), 400

        # Check if username already exists
        cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
        if cursor.fetchone():
            return jsonify({"status": "error", "message": "Username taken. Please try another one."}), 409

        # Insert new user
        cursor.execute("INSERT INTO user (fullname, username, email, password) VALUES (%s, %s, %s, %s)", 
                       (fullname, username, email, password))
        db.commit()

        return jsonify({"status": "success", "message": "Signup successful! Redirecting..."}), 201

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Login Route
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        email_or_username = data.get("email_or_username")
        password = data.get("password")

        if not email_or_username or not password:
            return jsonify({"status": "error", "message": "All fields are required."}), 400

        # Check if email/username exists
        cursor.execute("SELECT password FROM user WHERE email = %s OR username = %s", (email_or_username, email_or_username))
        result = cursor.fetchone()

        if not result or result[0] != password:
            return jsonify({"status": "error", "message": "Wrong Mail ID/Username or Password entered."}), 401

        return jsonify({"status": "success", "message": "Login successful!"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
