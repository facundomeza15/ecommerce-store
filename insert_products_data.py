from database import db, app
from models import Product


def add_product(product_name, price):
    with app.app_context():
        new_product = Product(product_name=product_name, price=price)
        db.session.add(new_product)
        db.session.commit()
        print(f"Added product: {product_name}, price: {price}")

def insert_products():
    sample_products = [
        ("DAMN LP", 20.99),
        ("Good Kid Maad City Alternate Cover Cassette", 17.00),
        ("Mr Morale & The Big Steppers CD", 14.00),
        ("Good Kid Maad City Alternate Cover LP", 30.99),
        ("To Pimp A Butterfly CD", 34.50),
        ("Kendrick Lamar untitled unmastered Vinyl", 16.50),
        ("Mr Morale Exclusive Black Cassette", 25.99),
        ("Good Kid Maad City Black Vinyl", 30.00),
        ("untitled unmastered CD", 15.00),
    ]
    
    for product_name, price in sample_products:
            if product_name not in [product.product_name for product in Product.query.all()]: #adding this check to avoid dupes since we're running the app multiple times
                add_product(product_name, price)
        
    print("Products in the database:")
    products = Product.query.all()
    for product in products:
        print(product.id, product.product_name, product.price)

