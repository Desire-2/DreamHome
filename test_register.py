from app import app, db
from flask import url_for
from models import User
import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

def test_register_get(client):
    response = client.get('/register')
    assert response.status_code == 200
    assert b'<form' in response.data  # Check if the registration form is rendered

def test_register_post_success(client):
    data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password',
        'confirm_password': 'password'
    }
    response = client.post('/register', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b'User registered successfully' in response.data  # Check for success message
    assert b'Login' in response.data  # Check if redirected to login page after successful registration
    # Check if the user is added to the database
    assert User.query.filter_by(username='testuser').first() is not None

def test_register_post_existing_email(client):
    # Create a user with the same email before attempting to register with it again
    existing_user = User(username='existing_user', email='test@example.com', password='password')
    db.session.add(existing_user)
    db.session.commit()


    data = {
        'username': 'testuser',
        'email': 'test@example.com',  # Use the same email as the existing user
        'password': 'password',  # Include a password for the new user
        'confirm_password': 'password'
    }
    response = client.post('/register', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b'Email address is already registered' in response.data  # Check for error message
    assert b'register' in response.data  # Check if redirected back to registration page
    # Check if the user is not added to the database
    assert User.query.filter_by(username='testuser').first() is None


def test_register_post_new_email(client):
    # Ensure there's no existing user with the provided email
    assert User.query.filter_by(email='newuser@example.com').first() is None

    data = {
        'username': 'newuser',
        'email': 'newuser@example.com',  # Use a new email
        'password': 'password',
        'confirm_password': 'password'
    }
    response = client.post('/register', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b'User registered successfully' in response.data  # Check for success message
    assert b'Login' in response.data  # Check if redirected to login page after successful registration
    # Check if the new user is added to the database
    assert User.query.filter_by(email='newuser@example.com').first() is not None
