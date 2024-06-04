from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)

database_file = os.path.join(app.instance_path, "products.db")
if not os.path.exists(database_file):
    os.makedirs(app.instance_path, exist_ok=True)
    open(database_file, "w").close()
    
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()