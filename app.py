from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{0}'.format(os.path.join(basedir, 'db.sqlite'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

ma = Marshmallow(app)


class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'quantity')


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


@app.route('/', methods=['GET'])
def index():
    data = {
        'msg': 'It works!'
    }
    return jsonify(data) 

@app.route('/product/add', methods=['POST'])
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    quantity = request.json['quantity']

    new_product = Product(name, description, price, quantity)
    
    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)

@app.route('/product/<product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)

    return product_schema.jsonify(product)

@app.route('/product/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    db.session.delete(product)

    db.session.commit()

    return product_schema.jsonify(product)


@app.route('/product/<product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get(product_id)
    
    product.name = request.json['name']
    product.description = request.json['description']
    product.price = request.json['price']
    product.quantity = request.json['quantity']
    db.session.commit()

    return product_schema.jsonify(product)

@app.route('/products/', methods=['GET'])
def products():
    all_products = Product.query.all()
    data = products_schema.dump(all_products)

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
