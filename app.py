from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import database.database
from models.user import User
from flask_login import login_user, logout_user
from pyzbar import pyzbar
from PIL import Image
from datetime import datetime, date
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'food_items.db')

db = SQLAlchemy(app)

# Initialize the LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Set the login view route


@login_manager.user_loader
def load_user(user_id):
    # Implement your logic to load the user from the database based on user_id
    return User.query.get(int(user_id))  # Replace User with your user model


class FoodItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    expiration_date = db.Column(db.Date, nullable=False)
    barcode = db.Column(db.String(100))  # Add a barcode column to the database


@app.route('/')
def index():
    items = FoodItem.query.all()
    current_date = date.today()  # Get the current date
    expired_items = database.database.get_expired_items()
    suggested_items = database.database.get_suggested_items()
    return render_template('index.html', items=items, current_date=current_date, expired_items=expired_items, suggested_items=suggested_items)


@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']

        # Perform barcode scanning
        barcode = scan_barcode()  # Call the scan_barcode function to get the barcode

        expiration_date_str = request.form['expiration_date']
        expiration_date = datetime.strptime(expiration_date_str, '%Y-%m-%d').date()  # Convert string to date object

        item = FoodItem(name=name, expiration_date=expiration_date, barcode=barcode)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_item.html')


def scan_barcode():
    # Open the image file captured from the barcode scanner
    image_path = 'static/barcode_image.jpg'  # Path to the image file
    with open(image_path, 'rb') as image_file:
        image = Image.open(image_file)
        gray_image = image.convert('L')  # Convert the image to grayscale

        # Scan the barcode from the image
        barcode_results = pyzbar.decode(gray_image)

        # Retrieve the barcode data
        if barcode_results:
            barcode_data = barcode_results[0].data.decode('utf-8')
            print("Scanned Barcode:", barcode_data)  # Print the barcode data
            return barcode_data
        else:
            return None


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_item(id):
    item = FoodItem.query.get(id)
    if request.method == 'POST':
        item.name = request.form['name']
        expiration_date_str = request.form['expiration_date']
        item.expiration_date = datetime.strptime(expiration_date_str, '%Y-%m-%d').date()
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_item.html', item=item)


@app.route('/delete/<int:id>')
def delete_item(id):
    item = FoodItem.query.get(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get the registration form data
        username = request.form['username']
        password = request.form['password']

        # Create a new user object
        new_user = User(username=username, password=password)

        # Add the user to the database
        db.session.add(new_user)
        db.session.commit()

        # Flash a success message and redirect to the login page
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))

    # Render the registration form template for GET requests
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get the login form data
        username = request.form['username']
        password = request.form['password']

        # Find the user in the database
        user = User.query.filter_by(username=username).first()

        # Check if the user exists and the password is correct
        if user and user.check_password(password):
            # Log in the user
            login_user(user)

            # Redirect to the index page or any other desired page
            return redirect(url_for('index'))

        # Flash an error message for invalid credentials
        flash('Invalid username or password.')

    # Render the login form template for GET requests
    return render_template('login.html')


@app.route('/logout')
def logout():
    # Log out the user
    logout_user()

    # Flash a logout message and redirect to the index page or any other desired page
    flash('You have been logged out.')
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
