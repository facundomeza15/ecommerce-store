from flask import Flask, render_template, request, redirect, url_for, session
from database import db, app
from insert_products_data import insert_products
from models import Product


@app.route("/")
def home():
    cart = session.get("cart", {})
    products = Product.query.all()
    return render_template("index.html", cart=cart, products=products)

@app.route("/login")
def login():
    cart = session.get("cart", {})
    return render_template("login.html", cart=cart)

@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    product_id = request.form.get("product_id")

    
    cart = session.get("cart", {})

    
    cart[product_id] = cart.get(product_id, 0) + 1

    
    session["cart"] = cart

    return redirect(url_for("home"))
@app.route("/checkout")
def checkout():
    cart = session.get("cart", {})
    total_price = 0
    cart_items = []

    for product_id, quantity in cart.items():
        product = Product.query.get(product_id)
        if product:
            total_price += product.price * quantity
            cart_items.append({
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