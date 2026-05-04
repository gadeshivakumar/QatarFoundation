from extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Admin(UserMixin, db.Model):
    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    # Relationship
    opportunities = db.relationship("Opportunity", backref="admin", lazy=True)

    # 🔐 Password methods
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Opportunity(db.Model):
    __tablename__ = "opportunities"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    skills = db.Column(db.Text, nullable=False)  # store as comma-separated
    category = db.Column(db.String(50), nullable=False)
    future_opportunities = db.Column(db.Text, nullable=False)
    max_applicants = db.Column(db.Integer)

    # 🔗 Foreign Key
    admin_id = db.Column(db.Integer, db.ForeignKey("admins.id"), nullable=False)