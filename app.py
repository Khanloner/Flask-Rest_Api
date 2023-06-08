from flask import Flask,request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)
# print(app, '4444444444')
basedir = os.path.abspath(os.path.dirname(__file__))
# print(basedir, '2222222222')

# db config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'db.sqlite')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///product.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False


# init db
db = SQLAlchemy(app)

# init ma
ma = Marshmallow(app)

# product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

# Product schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id','name','description','price','quantity')

# Init schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

@app.route('/createdb')
def create_database():
    db.create_all()
    return "<h1>database created successfully</h1>"

# Create a product
@app.route('/product', methods=['POST'])
def add_products():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    quantity = request.json['quantity']

    new_product = Product(name, description, price, quantity)
    db.session.add(new_product)
    db.session.commit()
    return product_schema.jsonify(new_product)

# get all the product
@app.route('/product',methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)   #doubt here
    # print("allproducts ",result)
    # print("result ",result)
    return jsonify(result)

# get single product
@app.route('/product/<id>', methods=['GET'])
def get_particularproduct(id):
    product = Product.query.get(id)
    # print("particular product ",product)
    # print("particular dump value ",product_schema.dump(product))
    return product_schema.jsonify(product)


# Update a product
@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    quantity = request.json['quantity']

    product.name = name
    product.description = description
    product.price = price
    product.quantity = quantity

    db.session.commit()
    return product_schema.jsonify(product)
    

# delete
@app.route('/product/<id>',methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return product_schema.jsonify(product)

# with app.app_context():
#     db.create_all()

if __name__ == "__main__":
    app.run(debug=True)

