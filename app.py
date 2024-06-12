from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from database import db, app
from insert_products_data import insert_products
from models import Product, User
from werkzeug.security import generate_password_hash
from sqlalchemy import text


@app.route("/")
def home():
    cart = session.get("cart", {})
    products = Product.query.all()
    return render_template("index.html", cart=cart, products=products)

@app.route("/login")
def login():
    cart = session.get("cart", {})
    return render_template("login.html", cart=cart)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            return "Passwords don't match."

        
        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            return "Username or email already exists."

        new_user = User(username=username, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))

    cart = session.get("cart", {})
    return render_template("register.html", cart=cart)

@app.route("/check_username", methods=["POST"])
def check_username():
    username = request.json.get('username')
    user = User.query.filter_by(username=username).first()
    return jsonify({"available": user is None})

@app.route("/check_email", methods=["POST"])
def check_email():
    email = request.json.get('email')
    user = User.query.filter_by(email=email).first()
    return jsonify({"available": user is None})


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
        with db.engine.connect() as conn:
            conn.execute(text("CREATE TABLE IF NOT EXISTS product (id INTEGER PRIMARY KEY AUTOINCREMENT, product_name VARCHAR(80), price FLOAT)"))
        with db.get_engine(app, bind='users').connect() as conn:
            conn.execute(text("CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY AUTOINCREMENT, username VARCHAR(80) UNIQUE, email VARCHAR(120) UNIQUE, password_hash VARCHAR(128))"))
    #only add products if the products table is empty
        if Product.query.first is None:
            insert_products() 
    app.run()