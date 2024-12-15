from flask import Flask, jsonify, request
from flask_login import current_user 
from models import db, User,Doctor,datetime
from flask_login import LoginManager,login_user,logout_user
import cloudinary.uploader
import bcrypt  
from utilities  import verify_email,generate_verification_token
from flask import Flask, jsonify, request
from redis import redis_client
import bcrypt
from models import db, User, Doctor


def gen_patient_id():
   count = db.session.query(User).count()
   return f"P_{count+1}"

def gen_doctor_id():
   count = db.session.query(Doctor).count()
   return f"D_{count+1}"


# Cloudinary configuration
cloudinary.config(
    cloud_name="dni5wcbsz",
    api_key="271365318367474",
    api_secret="L2ZC4nw7qdIjYZsLI1DlIX7JUc4"
)

#user register and send a verification email to personal email, if verified then only access.
def register_user():
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ["first_name", "last_name", "email", "password", "date_of_birth", "contact"]
        if not data or not all(field in data for field in required_fields):
            return jsonify({"error": "Invalid input data"}), 400

        # Check if the email is already in use
        if redis_client.get(data["email"]) or User.query.filter_by(email=data["email"]).first():
            return jsonify({"error": "Email already registered"}), 409

        # Hash the password
        hashed_password = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt())

        # Store user data temporarily in Redis
        user_data = {
            "first_name": data["first_name"],
            "userId": gen_patient_id(),
            "last_name": data["last_name"],
            "email": data["email"],
            "password": hashed_password.decode('utf-8'),
            "date_of_birth": data["date_of_birth"],
            "contact": data["contact"],
            "alternate_contact": data.get("alternate_contact"),
            "address": data["address"],
            "pincode": data["pincode"],
            "state": data["state"]
        }
        redis_client.set(data["email"], str(user_data), ex=3600)  # Expire after 1 hour

        # Generate a token with role = user
        token = generate_verification_token(data["email"], role="user")
        send_verification_email.delay(data["email"], token)

        return jsonify({"message": "Verification email sent"}), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

def register_doctor():
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ["first_name", "last_name", "email", "password", "contact", "specialization", "years_of_experience", "clinic_address", "clinic_pincode", "state", "available_time_start"]
        if not data or not all(field in data for field in required_fields):
            return jsonify({"error": "Invalid input data"}), 400

        # Check if the email is already in use
        if redis_client.get(data["email"]) or Doctor.query.filter_by(email=data["email"]).first():
            return jsonify({"error": "Email already registered"}), 409

        # Hash the password
        hashed_password = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt())

        # Store doctor data temporarily in Redis
        doctor_data = {
            "first_name": data["first_name"],
            "doctorId": gen_doctor_id(),
            "last_name": data["last_name"],
            "email": data["email"],
            "password": hashed_password.decode('utf-8'),
            "contact": data["contact"],
            "alternate_contact": data.get("alternate_contact"),
            "specialization": data["specialization"],
            "years_of_experience": int(data["years_of_experience"]),
            "clinic_address": data["clinic_address"],
            "clinic_pincode": data["clinic_pincode"],
            "state": data["state"],
            "available_time_start": data["available_time_start"],
            "available_time_end": data.get("available_time_end"),
        }
        redis_client.set(data["email"], str(doctor_data), ex=3600)  # Expire after 1 hour

        # Generate a token with role = doctor
        token = generate_verification_token(data["email"], role="doctor")
        send_verification_email.delay(data["email"], token)

        return jsonify({"message": "Verification email sent"}), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

#should be used for user and doctors both
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
        doctor = Doctor.query.filter_by(email=email).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            loginuser=login_user(user)
            print(current_user)
        elif doctor and bcrypt.checkpw(password.encode('utf-8'), doctor.password.encode('utf-8')):
            logindoctor=login_user(doctor) 
        print("current_user directory->",current_user,dir(current_user))
        return jsonify({"Success":"Login Successfull"}), 201
    else:
        return jsonify({"error": "Invalid credentials"}), 400
    
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200

def recoverPassword():
    pass