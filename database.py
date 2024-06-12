from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.secret_key = 'mock_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///default.db'

os.makedirs(app.instance_path, exist_ok=True)

app.config['SQLALCHEMY_BINDS'] = {
    'products': 'sqlite:///products.db',
    'users': 'sqlite:///users.db'
}

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()