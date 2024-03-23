from app import app, db, Property, Agent

# Define a function to remove existing records
def remove_existing_records():
    with app.app_context():
        # Query for existing agents
        existing_agents = Agent.query.all()
        # Delete existing agents
        for agent in existing_agents:
            db.session.delete(agent)

        # Query for existing properties
        existing_properties = Property.query.all()
        # Delete existing properties
        for property in existing_properties:
            db.session.delete(property)

        # Commit the session to apply changes
        db.session.commit()

# Call the function to remove existing records
remove_existing_records()

