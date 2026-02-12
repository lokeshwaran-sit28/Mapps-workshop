from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize the database
db = SQLAlchemy()

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(100), default="Student Name")
    college = db.Column(db.String(100), default="ABC College")
    dept = db.Column(db.String(50), default="Computer Science")
    year = db.Column(db.String(20), default="3rd Year")

    # Set password (hash it)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Check password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
