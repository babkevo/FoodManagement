from flask import Blueprint, render_template
from flask_login import login_required
from database.database import get_food_items

home_bp = Blueprint('home_bp', __name__)

@home_bp.route('/')
@login_required
def index():
    # Add logic to fetch the inventory items from the database
    items = get_food_items()

    return render_template('index.html', items=items)
