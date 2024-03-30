from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Property(db.Model):
    __tablename__ = 'properties'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    num_bedrooms = db.Column(db.Integer)
    num_bathrooms = db.Column(db.Integer)
    area = db.Column(db.Float)  # Area in square meters
    location = db.Column(db.String(255))
    image_url = db.Column(db.String(255))  # URL to property image
    year_built = db.Column(db.Integer)
    property_type = db.Column(db.String(50))  # E.g., Apartment, House, Condo
    amenities = db.Column(db.String(255))  # Comma-separated list of amenities
    is_featured = db.Column(db.Boolean, default=False)
    is_for_sale = db.Column(db.Boolean, default=True)
    is_for_rent = db.Column(db.Boolean, default=False)

    images = db.relationship('Image', backref='property', lazy=True)
    views = db.Column(db.Integer, default=0)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='properties')


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)  # Corrected foreign key definition

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    properties = db.relationship('Property', foreign_keys='Property.user_id', backref='users', overlaps="owned_properties_user")

    def set_password(self, password):
        """Set the password securely."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check if the provided password matches the stored hashed password."""
        return check_password_hash(self.password_hash, password)
