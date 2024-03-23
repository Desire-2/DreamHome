from app import db, User, app

# Assuming the User model is defined and imported correctly
def add_desire_user():
    with app.app_context():
        # Create a new user object
        desire = User(username='Desire-2', email='bikorimanadesire5@gmail.com')
        desire.set_password('desire')
        desire.is_admin = True
        # Add the user to the session and commit the transaction
        db.session.add(desire)
        db.session.commit()
if __name__ == "__main__":
    add_desire_user()
