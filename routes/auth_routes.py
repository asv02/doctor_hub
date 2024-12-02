from flask import Flask, jsonify, request
from models import db, User
from flask_login import LoginManager,login_user,logout_user
import bcrypt  
import os

def register():
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Validate input data
        required_fields = ["first_name", "last_name", "email", "password", "date_of_birth", "contact"]
        if not data or not all(key in data for key in required_fields):
            return jsonify({"error": "Invalid input data"}), 400

        # Check if the email is already in use
        if User.query.filter_by(email=data["email"]).first():
            return jsonify({"error": "Email already registered"}), 409

        # Hash the password
        hashed_password = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt())

        # Create a new User instance
        new_user = User(
            first_name=data["first_name"],
            userId=data["userId"],
            last_name=data["last_name"],
            email=data["email"],
            password=hashed_password.decode('utf-8'),  # Store the hashed password as a string
            date_of_birth=data["date_of_birth"],
            contact=data["contact"],
            alternate_contact=data.get("alternate_contact"),
            address=data["address"],
            pincode=data["pincode"],
            state=data["state"]
        )

        # Add the user to the database
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User registered successfully"}), 201

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

def login():
    
    data = request.get_json()
    # Validate input
    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Email and password are required"}), 400

    if request.method=='POST': 
        data = request.get_json()
        email=data['email']
        password=data['password']
        user= User.query.filter_by(email=email).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            loginuser=login_user(user)
        return jsonify({"Success":"Login Successfull"}), 201
    else:
        return jsonify({"error": "Invalid credentials"}), 400
    
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200

def recoverPassword():
    pass