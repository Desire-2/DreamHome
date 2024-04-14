import os
import tempfile
import pytest
from app import app, db
from models import User, Property

@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Create test users
            user1 = User(username='test_user1', email='test1@example.com')
            user1.set_password('test_password1')
            user2 = User(username='test_user2', email='test2@example.com')
            user2.set_password('test_password2')
            db.session.add(user1)
            db.session.add(user2)
            
            # Create test properties
            property1 = Property(title='Test Property 1', description='Description 1', price=100000, num_bedrooms=3, num_bathrooms=2, location='Test Location 1')
            property2 = Property(title='Test Property 2', description='Description 2', price=150000, num_bedrooms=4, num_bathrooms=3, location='Test Location 2')
            db.session.add(property1)
            db.session.add(property2)
            
            db.session.commit()
            
        yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to DreamHome' in response.data

def test_login(client):
    response = client.post('/login', data={'email': 'test1@example.com', 'password': 'test_password1'})
    assert response.status_code == 302  # Redirects to dashboard after successful login

def test_logout(client):
    response = client.get('/logout')
    assert response.status_code == 302  # Redirects to home page after logout

def test_register(client):
    response = client.post('/register', data={'username': 'test_user3', 'email': 'test3@example.com', 'password': 'test_password3'})
    assert response.status_code == 302  # Redirects to login page after registration

def test_view_users(client):
    response = client.get('/view_users')
    assert response.status_code == 200
    assert b'List of Users' in response.data

def test_view_properties(client):
    response = client.get('/properties')
    assert response.status_code == 200
    assert b'Properties' in response.data

def test_view_property(client):
    # Assuming there's a property with ID=1 in the database
    response = client.get('/property/1')
    assert response.status_code == 200
    assert b'Test Property 1' in response.data

def test_add_property(client):
    # Simulate adding a property
    response = client.post('/add-property', data={
        'title': 'New Test Property',
        'description': 'New Description',
        'price': 200000,
        'num_bedrooms': 3,
        'num_bathrooms': 2,
        'area': 1500,
        'location': 'New Location',
        'year_built': 2020,
        'property_type': 'House',
        'amenities': 'Gym, Pool'
    }, content_type='multipart/form-data')

    assert response.status_code == 302  # Redirects after adding a property

def test_modify_property(client):
    # Assuming there's a property with ID=1 in the database
    response = client.post('/modify_properties/1', data={
        'title': 'Modified Test Property',
        'description': 'Modified Description',
        'price': 250000,
        'num_bedrooms': 4,
        'num_bathrooms': 3,
        'location': 'Modified Location',
        'year_built': 2015
    })

    assert response.status_code == 302  # Redirects after modifying a property

def test_delete_property(client):
    # Assuming there's a property with ID=2 in the database
    response = client.post('/admin/delete_property/2')
    assert response.status_code == 302  # Redirects after deleting a property


def test_admin_dashboard(client):
    # Assuming a user is logged in as an admin
    # The test database should contain properties for testing
    response = client.get('/admin/dashboard')
    assert response.status_code == 200
    assert b'Admin Dashboard' in response.data
    assert b'List of Properties' in response.data

def test_admin_manage_admins(client):
    # Assuming a user is logged in as an admin
    response = client.get('/admin/manage_admins')
    assert response.status_code == 200
    assert b'Manage Admins' in response.data

def test_search_properties(client):
    # Test search with a query string
    response = client.get('/search?query=Test')
    assert response.status_code == 200
    assert b'Search Results' in response.data

def test_search_properties_with_filters(client):
    # Test search with filters
    response = client.get('/search?min_price=100000&max_price=200000&min_bedrooms=3&max_bedrooms=4')
    assert response.status_code == 200
    assert b'Search Results' in response.data

def test_contact_page(client):
    response = client.get('/contact')
    assert response.status_code == 200
    assert b'Contact Us' in response.data

def test_about_page(client):
    response = client.get('/about')
    assert response.status_code == 200
    assert b'About Us' in response.data

def test_services_page(client):
    response = client.get('/services')
    assert response.status_code == 200
    assert b'Our Services' in response.data

def test_blog_news_page(client):
    response = client.get('/blog_news')
    assert response.status_code == 200
    assert b'Blog & News' in response.data

def test_faq_page(client):
    response = client.get('/faq')
    assert response.status_code == 200
    assert b'Frequently Asked Questions' in response.data

def test_thank_you_page(client):
    response = client.get('/thank-you')
    assert response.status_code == 200
    assert b'Thank You' in response.data

def test_export_data(client):
    # Assuming there's data in the database for exporting
    response = client.get('/export_data')
    assert response.status_code == 200
    assert b'properties.xlsx' in response.data

def test_import_data(client):
    # Simulate importing data
    response = client.post('/import_data', data={
        'file': (open('test_data/properties.xlsx', 'rb'), 'properties.xlsx')
    }, content_type='multipart/form-data')

    assert response.status_code == 302  # Redirects after importing data
def test_view_users(client):
    # Assuming there are users in the database
    response = client.get('/view_users')
    assert response.status_code == 200
    assert b'View Users' in response.data

def test_view_reports(client):
    # Assuming there are reports in the database
    response = client.get('/view_reports')
    assert response.status_code == 200
    assert b'View Reports' in response.data

def test_edit_profile(client):
    # Assuming a user is logged in
    response = client.get('/edit_profile')
    assert response.status_code == 200
    assert b'Edit Profile' in response.data

def test_view_properties(client):
    # Assuming there are properties in the database
    response = client.get('/properties')
    assert response.status_code == 200
    assert b'Properties' in response.data

def test_add_property(client):
    # Assuming a user is logged in
    response = client.get('/add-property')
    assert response.status_code == 200
    assert b'Add Property' in response.data

def test_property_detail(client):
    # Assuming there is a property with the given ID in the database
    property_id = 1  # Adjust as needed
    response = client.get(f'/property/{property_id}')
    assert response.status_code == 200
    assert b'Property Details' in response.data

def test_modify_properties(client):
    # Assuming there is a property with the given ID in the database
    property_id = 1  # Adjust as needed
    response = client.get(f'/modify_properties/{property_id}')
    assert response.status_code == 200
    assert b'Modify Property' in response.data

def test_delete_property(client):
    # Assuming there is a property with the given ID in the database
    property_id = 1  # Adjust as needed
    response = client.post(f'/admin/delete_property/{property_id}')
    assert response.status_code == 302  # Redirects to another page after deletion

def test_delete_user(client):
    # Assuming there is a user with the given ID in the database
    user_id = 1  # Adjust as needed
    response = client.post(f'/delete_user/{user_id}')
    assert response.status_code == 302  # Redirects to another page after deletion

def test_search_properties(client):
    # Test search with a search query
    response = client.post('/search', data={'location': 'New York'})
    assert response.status_code == 200
    assert b'Search Results' in response.data

    # Test search without a search query (GET request)
    response = client.get('/search?query=')
    assert response.status_code == 200
    assert b'Search Properties' in response.data

def test_thank_you(client):
    response = client.get('/thank-you')
    assert response.status_code == 200
    assert b'Thank You' in response.data

def test_services(client):
    response = client.get('/services')
    assert response.status_code == 200
    assert b'Services' in response.data

def test_about(client):
    response = client.get('/about')
    assert response.status_code == 200
    assert b'About Us' in response.data

def test_contact_get(client):
    response = client.get('/contact')
    assert response.status_code == 200
    assert b'Contact Us' in response.data

def test_contact_post(client):
    # Assuming the contact form fields are properly named
    response = client.post('/contact', data={'name': 'John Doe', 'email': 'john@example.com', 'message': 'Test message'})
    assert response.status_code == 302  # Redirects to thank-you page after submission

def test_property_listing(client):
    # Assuming there are properties in the database
    response = client.get('/properties')
    assert response.status_code == 200
    assert b'Property Listing' in response.data

def test_properties_for_sale(client):
    # Assuming there are properties for sale in the database
    response = client.get('/properties/sale')
    assert response.status_code == 200
    assert b'Properties for Sale' in response.data

def test_properties_for_rent(client):
    # Assuming there are properties for rent in the database
    response = client.get('/properties/rent')
    assert response.status_code == 200
    assert b'Properties for Rent' in response.data

def test_blog_news(client):
    response = client.get('/blog_news')
    assert response.status_code == 200
    assert b'Blog & News' in response.data

def test_faq(client):
    response = client.get('/faq')
    assert response.status_code == 200
    assert b'FAQ' in response.data


