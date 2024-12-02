from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

# Define models (tables)
class User(UserMixin,db.Model):
    __tablename__ = 'users'  
    id = db.Column(db.Integer, primary_key=True)  # Auto-incrementing primary key
    userId = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    contact = db.Column(db.Integer, nullable=False)
    alternate_contact = db.Column(db.Integer, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    pincode = db.Column(db.Integer, nullable=False)
    state = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)  

    # Relationship to Appointment
    appointments = db.relationship('Appointment', backref='user', lazy=True)

class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key to the User model
    appointment_time = db.Column(db.DateTime, nullable=False)
    status_of_appointment = db.Column(db.Boolean, default=False)  # False = Not completed, True = Completed/Cancelled
    doctor_id = db.Column(db.Integer, nullable=False)  # Doctor ID, that we will get from doctor model
    is_payment_made = db.Column(db.Boolean, default=False)
    user_informed = db.Column(db.Boolean, default=False)
    doctor_informed = db.Column(db.Boolean, default=False)
    payment_to_doctor = db.Column(db.Boolean, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    # Relationship to Payment
    payment = db.relationship('Payment', backref='appointment', lazy=True)

    # Relationship to AppointmentHistory
    history = db.relationship('AppointmentHistory', backref='appointment', lazy=True)

class AppointmentHistory(db.Model):
    __tablename__ = 'appointment_history'

    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=False)  # Foreign key to Appointment
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key to User (optional)
    doctor_id = db.Column(db.Integer, nullable=False)  # The doctor ID for the historical appointment
    original_appointment_time = db.Column(db.DateTime, nullable=False)  # Original appointment time
    updated_appointment_time = db.Column(db.DateTime, nullable=True)  # Updated appointment time (if changed)
    status = db.Column(db.String(50), nullable=False, default="Scheduled")  # Status of the appointment (Scheduled, Cancelled, Rescheduled, etc.)
    cancellation_reason = db.Column(db.String(200), nullable=True)  # Reason for cancellation (if applicable)
    payment_status = db.Column(db.String(50), nullable=True)  # Payment status at the time of the history record
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)  # When the history entry was created
    # updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)  # When the history entry was last updated


    # Relationship to User (optional if you want to track which user made changes)
    # user = db.relationship('User', backref='history', lazy=True)

class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key to the User model
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    tax = db.Column(db.Float, nullable=False)
    total_paid = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.now, nullable=False)
    payment_method = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(50), default="Completed", nullable=False)