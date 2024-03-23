from app import db, User, app

# Assuming the User model and Flask application are imported correctly

def remove_user(email):
    with app.app_context():
        # Query for the user by email
        user = User.query.filter_by(email=email).first()

        # Check if the user exists
        if user:
            # Remove the user from the session and commit the transaction
            db.session.delete(user)
            db.session.commit()
            print(f"User with email {email} has been successfully removed.")
        else:
            print(f"User with email {email} does not exist.")

if __name__ == "__main__":
    # Specify the email of the user you want to remove
    email_to_remove = 'bikorimanadesire@yahoo.com'
    remove_user(email_to_remove)
