from flask import Flask, render_template, request, redirect, url_for
from database import db, app
from insert_products_data import insert_products
from models import Product


cart = {}  

@app.route("/")
def home():
    products = Product.query.all()
    return render_template("index.html", cart=cart, products=products)

@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    product_id = request.form.get("product_id")
    product = Product.query.get(product_id)
    if product:
        if product_id in cart:
            cart[product_id] += 1
        else:
            cart[product_id] = 1
    return redirect(url_for("home"))

@app.route("/checkout")
def checkout():
    total_price = 0
    cart_items = []

    for product_id, quantity in cart.items():
        product = Product.query.get(product_id)
        if product:
            total_price += product.price * quantity
            cart_items.append ({
            'name': product.product_name,
            'quantity': quantity,
            'price': product.price
        })
    total_price = round(total_price, 2)

    return render_template("checkout.html", cart_items=cart_items, total_price=total_price, cart=cart)

@app.template_filter('dict_sum') 
def dict_sum(d):
    return sum(d.values())

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  
        insert_products()  
    app.run()