from flask import Flask, render_template, request, redirect, url_for
from database import db, app
from insert_products_data import insert_products


cart = {}  # cart dict to store cart items qty

@app.route("/")
def home():
    return render_template("index.html", cart=cart)

@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    product_id = request.form.get("product_id")
    if product_id:
        cart[product_id] = cart.get(product_id, 0) + 1
    return redirect(url_for("home"))

@app.route("/checkout")
def checkout():
    total_price = 0
    for product_id, quantity in cart.items():
        total_price += quantity * get_product_price(product_id)
    
    return render_template("checkout.html", cart=cart, total_price=total_price)

@app.template_filter('dict_sum') #not needed lol
def dict_sum(d):
    return sum(d.values())

def get_product_price(product_id): #also not needed
    prices = {
        "1": 20.99,
        "2": 17.00,
        "3": 14.00,
        "4": 30.99,
        "5": 34.50,
        "6": 16.50,
        "7": 19.99
    }
    return prices.get(product_id, 0)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create database tables
        insert_products()  # Insert sample products
    app.run()