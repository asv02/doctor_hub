from flask import Flask
from flask_login import LoginManager, login_required
import os
from routes import register, login, logout, book_appointment, update_appointment
from models import db

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/demo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Initialize the database
db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# User loader for login manager
@login_manager.user_loader
def load_user(id):
    from models import User
    return User.query.get(int(id))

# Associate routes to the app
app.add_url_rule('/auth/register', view_func=register, methods=['POST'])
app.add_url_rule('/auth/login', view_func=login, methods=['POST'])
app.add_url_rule('/auth/logout', view_func=logout, methods=['POST'])

# Routes that require login
app.add_url_rule('/appointments/book', view_func=login_required(book_appointment), methods=['POST'])
app.add_url_rule('/appointments/update/<int:appointment_id>', view_func=login_required(update_appointment), methods=['PUT'])

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
