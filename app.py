from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from database import db, app
from insert_products_data import insert_products
from models import Product, User
from werkzeug.security import generate_password_hash
from sqlalchemy import text

# initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect to login if a login is required

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def inject_user():
    return dict(current_user=current_user)


@app.route("/login", methods=["GET", "POST"])
def login():
    cart = session.get("cart", {})

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Login successful!")
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password.")

    return render_template("login.html", cart=cart)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout successful!")
    return redirect(url_for("login"))

@app.route("/")
def home():
    cart = session.get("cart", {})
    products = Product.query.all()
    return render_template("index.html", cart=cart, products=products)



@app.route("/register", methods=["GET", "POST"])
def register():
    cart = session.get("cart", {})

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
        
        return render_template("register_success.html", username=username, email=email, cart=cart)

    return render_template("register.html", cart=cart)

@app.route("/register_success")
def register_success():
    username = request.args.get("username")
    email = request.args.get("email")
    return render_template("register_success.html", username=username, email=email)

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