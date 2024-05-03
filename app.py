from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, send_from_directory, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import logging
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from forms import RegistrationForm
from forms import EditProfileForm, AdminForm
import pandas as pd
from flask import send_file
import random
from io import BytesIO
import os
from flask_login import current_user



UPLOAD_FOLDER = os.path.join('static', 'images')




app = Flask(__name__)


app.secret_key = '4f4cfedba9320657d8b531d8cb92827e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Configure Flask-Mail settings
app.config['MAIL_SERVER'] = 'smtp.example.com'  # Update with your SMTP server
app.config['MAIL_PORT'] = 587  # Update with your SMTP port
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@example.com'  # Update with your email credentials
app.config['MAIL_PASSWORD'] = 'your_email_password'  # Update with your email password
app.config['MAIL_DEFAULT_SENDER'] = 'your_email@example.com'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

mail = Mail(app)

from models import Property, db, User, Image
db.init_app(app)
migrate = Migrate(app, db)

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

logging.basicConfig(filename='app.log', level=logging.ERROR)

@app.route('/')
def home():
    # Retrieve recently added properties (e.g., last 5 properties added)
    recently_added_properties = Property.query.order_by(Property.id.desc()).limit(5).all()

    # Retrieve most viewed properties (you need to define a method to track views)
    most_viewed_properties = Property.query.order_by(Property.views.desc()).limit(5).all()

    # Pass the properties to the home template
    return render_template('home.html', recently_added_properties=recently_added_properties, most_viewed_properties=most_viewed_properties)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error_message='Page not found'), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error.html', error_message='Internal server error'), 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('dashboard', logged_in=True))
        else:
            flash('Invalid email or password.', 'error')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()  # Instantiate the registration form
    
    if request.method == 'POST' and form.validate_on_submit():
        # Check if the email is already registered
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email address is already registered. Please use a different email.', 'error')
            return redirect(url_for('register'))

        # Create a new user object with form data
        new_user = User(username=form.username.data, email=form.email.data)
        new_user.set_password(form.password.data)  # Assuming you have a method to hash and set the password securely

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        flash('User registered successfully. You can now login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/export_data')
def export_data():
    # Query properties data from the database
    properties = Property.query.all()
    
    # Convert properties data to a DataFrame
    data = {
        'Title': [property.title for property in properties],
        'Description': [property.description for property in properties],
        'Price': [property.price for property in properties],
        'Num Bedrooms': [property.num_bedrooms for property in properties],
        'Num Bathrooms': [property.num_bathrooms for property in properties],
        # Add more columns as needed
    }
    df = pd.DataFrame(data)
    
    # Create a BytesIO object to store the Excel file
    excel_file = BytesIO()
    
    # Write DataFrame to Excel
    df.to_excel(excel_file, index=False)
    
    # Set the position to the beginning of the BytesIO object
    excel_file.seek(0)
    
    # Send the Excel file as a response
    return send_file(
        excel_file,
        as_attachment=True,
        attachment_filename='properties.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )


@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        return redirect(url_for('dashboard'))

    properties = Property.query.all()
    user_id = current_user.id  # This line is moved here to ensure it's always defined
    users = User.query.all()
    return render_template('admin_dashboard.html', properties=properties, user_id=user_id, users=users)

# Route to view admins
@app.route('/admin/manage_admins')
@login_required
def manage_admins():
    if not current_user.is_admin:
        flash('You are not authorized to access this page.', 'error')
        return redirect(url_for('admin_dashboard'))

    admins = User.query.filter_by(is_admin=True).all()
    return render_template('manage_admins.html', admins=admins)

# Route to add admin
@app.route('/admin/add_admin', methods=['GET', 'POST'])
@login_required
def add_admin():
    if not current_user.is_admin:
        flash('You are not authorized to access this page.', 'error')
        return redirect(url_for('admin_dashboard'))

    form = AdminForm()
    if form.validate_on_submit():
        # Create a new admin user
        new_admin = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            is_admin=True
        )
        db.session.add(new_admin)
        db.session.commit()
        flash('Admin added successfully.', 'success')
        return redirect(url_for('manage_admins'))
    return render_template('add_admin.html', form=form)

# Route to edit admin
@app.route('/admin/edit_admin/<int:admin_id>', methods=['GET', 'POST'])
@login_required
def edit_admin(admin_id):
    if not current_user.is_admin:
        flash('You are not authorized to access this page.', 'error')
        return redirect(url_for('admin_dashboard'))

    admin = User.query.get_or_404(admin_id)
    form = AdminForm(obj=admin)
    if form.validate_on_submit():
        admin.username = form.username.data
        admin.email = form.email.data
        admin.password = form.password.data
        db.session.commit()
        flash('Admin updated successfully.', 'success')
        return redirect(url_for('manage_admins'))
    return render_template('edit_admin.html', form=form, admin=admin)

# Route to delete admin
@app.route('/admin/delete_admin/<int:admin_id>', methods=['POST'])
@login_required
def delete_admin(admin_id):
    if not current_user.is_admin:
        flash('You are not authorized to access this page.', 'error')
        return redirect(url_for('admin_dashboard'))

    admin = User.query.get_or_404(admin_id)
    db.session.delete(admin)
    db.session.commit()
    flash('Admin deleted successfully.', 'success')
    return redirect(url_for('manage_admins'))

@app.route('/admin/delete_property/<int:property_id>', methods=['POST'])
@login_required
def delete_property(property_id):
    # Query the database to find the property with the given ID
    property = Property.query.get(property_id)

    if property:
        # Delete associated images first
        images = Image.query.filter_by(property_id=property_id).all()
        for image in images:
            db.session.delete(image)
        
        # Delete the property from the database
        db.session.delete(property)
        db.session.commit()
        flash('Property deleted successfully.', 'success')
    else:
        flash('Property not found.', 'error')

    # Redirect the user to the admin dashboard
    return redirect(url_for('admin_dashboard'))

@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    # Retrieve the user object from the database
    user = User.query.get_or_404(user_id)

    # Delete the user
    db.session.delete(user)
    db.session.commit()

    # Flash a success message
    flash('User deleted successfully.', 'success')

    # Redirect to an appropriate page (e.g., user dashboard, admin panel, etc.)
    return redirect(url_for('user_dashboard')) 

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm()

    if request.method == 'POST' and form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data

        # You can add more fields as needed

        db.session.commit()
        flash('Your profile has been updated successfully.', 'success')
        return redirect(url_for('dashboard'))

    elif request.method == 'GET':
        # Pre-populate the form with the current user information
        form.username.data = current_user.username
        form.email.data = current_user.email

    return render_template('edit_profile.html', form=form)

@app.route('/view_users')
def view_users():
    users = User.query.all()
    return render_template('view_users.html', users=users)

@app.route('/view_reports')
def view_reports():
    # Query the database to fetch report data
    return render_template('view_reports.html')

@app.route('/dashboard')
@login_required
def dashboard():
    # Fetch user-specific data from the database
    user_properties = Property.query.all()
    return render_template('dashboard.html', properties=user_properties, logged_in=True)

# Define the allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Function to check if a file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/properties')
def view_properties():
    properties = Property.query.filter_by(is_for_sale=True).all()
    return render_template('properties.html', properties=properties)
    

@app.route('/property/<int:property_id>')
def view_property(property_id):
    property = Property.query.get_or_404(property_id)

     # Increment the views count for the property
    property.views += 1
    db.session.commit()
    
    return render_template('property_detail.html', property=property)
    

@app.route('/add-property', methods=['GET', 'POST'])
@login_required
def add_property():
    if request.method == 'POST':
        # Extract property data from the form
        title = request.form['title']
        description = request.form['description']
        price = request.form['price']
        num_bedrooms = request.form['num_bedrooms']
        num_bathrooms = request.form['num_bathrooms']
        location = request.form['location']
        year_built = request.form['year_built']
        property_type = request.form['property_type']
        amenities = request.form['amenities']
        
        # Check if the property is for sale or for rent
        is_for_sale = property_type == 'For Sale'
        is_for_rent = property_type == 'For Rent'

        # Check if files were uploaded
        if 'image' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)

        # Get the uploaded files
        files = request.files.getlist('image')

        # Create a new Property object associated with the current user
        new_property = Property(
            title=title, description=description, price=price,
            num_bedrooms=num_bedrooms, num_bathrooms=num_bathrooms, location=location, year_built=year_built,
            is_for_sale=is_for_sale, is_for_rent=is_for_rent, amenities=amenities,
            user_id=current_user.id  # Associate with the current user
        )

        # Add the property to the database session to generate the property ID
        db.session.add(new_property)
        db.session.commit()

        # Process each uploaded file
        for file in files:
            if file and allowed_file(file.filename):
                # Save the file to the uploads folder
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                # Generate URL for the uploaded image
                image_url = url_for('uploaded_file', filename=filename)

                # Create a new Image object for each file and associate it with the property
                image = Image(filename=filename, url=image_url, property_id=new_property.id)
                db.session.add(image)

        # Commit the changes to the database session
        db.session.commit()

        flash('Property added successfully.', 'success')
        return redirect(url_for('dashboard'))

    return render_template('add_property.html')


@app.route('/modify_properties/<int:property_id>', methods=['GET', 'POST'])
def modify_properties(property_id):
    # Retrieve the property object from the database
    property = Property.query.get_or_404(property_id)

    if request.method == 'POST':
        # Update property details based on form submission
        property.title = request.form['title']
        property.description = request.form['description']
        property.price = float(request.form['price'])
        property.num_bedrooms = int(request.form['num_bedrooms'])
        property.num_bathrooms = int(request.form['num_bathrooms'])
        property.location = request.form['location']
        property.year_built = int(request.form['year_built'])

        # Check if any image files were uploaded
        if 'images' in request.files:
            images = request.files.getlist('images')
            for image in images:
                if image and allowed_file(image.filename):
                    filename = secure_filename(image.filename)
                    image_path = os.path.join(UPLOAD_FOLDER, filename)
                    image.save(image_path)
                    # Create a new Image object and associate it with the property
                    new_image = Image(filename=filename, property_id=property.id)
                    db.session.add(new_image)

                    # Remove the old image if it exists
                    old_image = Image.query.filter_by(property_id=property.id).first()
                    if old_image:
                        old_image_path = os.path.join(UPLOAD_FOLDER, old_image.filename)
                        if os.path.exists(old_image_path):
                            os.remove(old_image_path)
                        db.session.delete(old_image)

        db.session.commit()
        # Redirect to the property details page or another appropriate route
        return redirect(url_for('property_listing', property_id=property.id))

    # Render the form for modifying property details
    return render_template('modify_properties.html', property=property)

@app.route('/search', methods=['GET', 'POST'])
def search_properties():
    if request.method == 'POST':
        location = request.form['location']
        properties = Property.query.filter_by(location=location).all()
        return render_template('properties.html', properties=properties)

    # Handling GET requests for search
    search_query = request.args.get('query')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    sort_by = request.args.get('sort_by', 'id')
    order = request.args.get('order', 'asc')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    min_bedrooms = request.args.get('min_bedrooms')
    max_bedrooms = request.args.get('max_bedrooms')

    # Initialize the base query
    query = Property.query

    # Apply filters
    if min_price:
        query = query.filter(Property.price >= float(min_price))
    if max_price:
        query = query.filter(Property.price <= float(max_price))
    if min_bedrooms:
        query = query.filter(Property.num_bedrooms >= int(min_bedrooms))
    if max_bedrooms:
        query = query.filter(Property.num_bedrooms <= int(max_bedrooms))

    # Apply search query
    if search_query:
        query = query.filter(Property.title.ilike(f'%{search_query}%'))

    # Apply sorting
    if order == 'asc':
        query = query.order_by(getattr(Property, sort_by).asc())
    else:
        query = query.order_by(getattr(Property, sort_by).desc())

    # Paginate the results
    paginated_results = query.paginate(page=page, per_page=per_page, error_out=False)

    # Render the search template with the paginated results and pagination metadata
    return render_template('search.html', results=paginated_results)

@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Create a Flask-Mail message
        msg = Message('New Contact Form Submission', sender=email, recipients=['your_recipient@example.com'])
        msg.body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

        # Send the email
        mail.send(msg)

        # Redirect to a thank you page
        return redirect(url_for('thank_you'))

    return render_template('contact.html')

# Route for property listing (optional)
@app.route('/properties')
def property_listing():
    properties = Property.query.all()
    return render_template('property_listing.html', properties=properties)

# Route for properties for sale
@app.route('/properties/sale')
def properties_for_sale():
    properties = Property.query.filter_by(is_for_sale=True).all()
    return render_template('properties_for_sale.html', properties=properties)

# Route for properties for rent
@app.route('/properties/rent')
def properties_for_rent():
    properties = Property.query.filter_by(is_for_rent=True).all()
    return render_template('properties_for_rent.html', properties=properties)


@app.route('/blog_news')
def blog_news():
    return render_template('blog_news.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
