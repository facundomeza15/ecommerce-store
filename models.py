from database import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    

def __init__(self, product_name, price, image_url=None):
        self.product_name = product_name
        self.price = price
        