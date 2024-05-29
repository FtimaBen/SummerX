from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app, origins=r'https://www.amazon.com/*')

# Configure your database URI here
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reviews.db'

db = SQLAlchemy(app)

# Define a model for your products
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)

# Define a model for your reviews
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship('Product', backref=db.backref('reviews', lazy='dynamic'))

# Create the database tables
db.create_all()

def get_or_create_product(product_name):
    """
    Get the product from the database by name if it exists, 
    otherwise, create a new product with the given name.
    """
    product = Product.query.filter_by(name=product_name).first()
    if not product:
        product = Product(name=product_name)
        db.session.add(product)
    return product

def save_reviews(reviews, product):
    """
    Save the provided reviews associated with the given product.
    """
    for review_text in reviews:
        new_review = Review(content=review_text, product=product)
        db.session.add(new_review)
    db.session.commit()

@app.route('/', methods=['GET', 'POST', 'OPTIONS'])
def index():
    if request.headers.get('content-type') == 'application/json':
        reviews = request.get_json().get('reviews')
        product_name = request.get_json().get('product_name')
        smX = SummerizX(reviews).summerize()

        product = get_or_create_product(product_name)
        save_reviews(reviews, product)

        return json.dumps({'template': render_template('index.html', smX=smX), 'review': smX})

    return render_template('index.html', smX='')

if __name__ == '__main__':
    app.run(debug=True)
