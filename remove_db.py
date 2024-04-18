from flask import Flask
from models import Property, db

# Create a Flask application instance
app = Flask(__name__)

# Assuming 'Property' is your SQLAlchemy model for properties

# Function to delete all properties
def delete_all_properties():
    with app.app_context():
        # Delete all properties
        db.session.query(Property).delete()

        # Commit the transaction to apply the changes
        db.session.commit()

# Call the function to delete all properties
delete_all_properties()
