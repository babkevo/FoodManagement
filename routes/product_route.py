from flask import Blueprint, render_template, request, redirect, url_for
from database.database import insert_food_item

product_bp = Blueprint('product', __name__)

@product_bp.route('/products', methods=['GET', 'POST'])
def products():
    if request.method == 'POST':
        name = request.form['name']
        expiration_date = request.form['expiration_date']
        insert_food_item(name, expiration_date)
        return redirect(url_for('product.products'))

    return render_template('products.html')
