from models import db, Property, Image, User
import pytest

@pytest.fixture
def app():
    from flask import Flask
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    db.init_app(app)
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_delete_property(client):
    property = Property(title='Test Property', description='Test Description', price=100000)
    db.session.add(property)
    db.session.commit()

    # Delete the property
    db.session.delete(property)
    db.session.commit()

    # Check if the property is deleted
    assert Property.query.filter_by(title='Test Property').first() is None

def test_delete_user(client):
    user = User(username='testuser', email='test@example.com', password='password')
    db.session.add(user)
    db.session.commit()

    # Delete the user
    db.session.delete(user)
    db.session.commit()

    # Check if the user is deleted
    assert User.query.filter_by(username='testuser').first() is None

def test_set_password():
    user = User(username='testuser', email='test@example.com')
    user.set_password('password')
    assert user.password is not None
    assert user.password != 'password'

def test_property_creation(client):
    # Create a new property
    property = Property(title='Test Property', description='Test Description', price=100000)
    db.session.add(property)
    db.session.commit()

    # Retrieve the property from the database
    retrieved_property = Property.query.filter_by(title='Test Property').first()

    # Assert that the property was successfully created and persisted
    assert retrieved_property is not None
    assert retrieved_property.title == 'Test Property'
    assert retrieved_property.description == 'Test Description'
    assert retrieved_property.price == 100000

def test_property_relationships(client):
    # Create a new user
    user = User(username='testuser', email='test@example.com', password='password')
    db.session.add(user)
    db.session.commit()

    # Create a new property associated with the user
    property = Property(title='Test Property', description='Test Description', price=100000, user_id=user.id)
    db.session.add(property)
    db.session.commit()

    # Retrieve the user from the database along with their properties
    retrieved_user = User.query.filter_by(username='testuser').first()

    # Assert that the user's properties relationship is correctly established
    assert len(retrieved_user.properties) == 1
    assert retrieved_user.properties[0].title == 'Test Property'

def test_delete_property_again(client):  # Renamed to avoid duplicate test names
    # Create a new property
    property = Property(title='Test Property', description='Test Description', price=100000)
    db.session.add(property)
    db.session.commit()

    # Delete the property
    db.session.delete(property)
    db.session.commit()

    # Try to retrieve the deleted property from the database
    retrieved_property = Property.query.filter_by(title='Test Property').first()

    # Assert that the property was successfully deleted
    assert retrieved_property is None

if __name__ == '__main__':
    pytest.main()
