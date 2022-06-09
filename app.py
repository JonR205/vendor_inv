from distutils.log import debug
from email.policy import default
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import DateTime


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///vendor.db"
# app.run(debug=True)
db = SQLAlchemy(app)
# headings = (
#     "sku",
#     "Product Name",
#     "Product Description",
#     "Cost to Make",
#     "Price",
#     "Category",
#     "Notes",
# )

# data = (
#     ("Jon", "rhine", "3", "4", "5", "6", "7"),
#     ("Jon", "rhine", "3", "4", "5", "6", "7"),
#     ("Jon", "rhine", "3", "4", "5", "6", "7"),
# )

# DB table for products
class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.Integer, unique=True, nullable=False)
    prod_name = db.Column(db.String(100), unique=True, nullable=False)
    prood_description = db.Column(db.String(500), unique=True, nullable=False)
    cost_to_make = db.Column(db.Float(), unique=False, nullable=False)
    price = db.Column(db.Float(), unique=False, nullable=False)
    category = db.Column(db.String(500), unique=False, nullable=False)
    prood_notes = db.Column(db.String(1000), unique=False, nullable=False)
    qty = db.Column(db.Integer)

    def __init__(self, sku, prod_name, prood_description, cost_to_make, price, category, prood_notes, qty) -> None:
        self.sku = sku
        self.prod_name = prod_name
        self.prood_description = prood_description
        self.cost_to_make = cost_to_make
        self.price = price
        self.category = category
        self.prood_notes = prood_notes
        self.qty = qty
    
# p1=Products(sku=1234,prod_name='shirt', prood_description='holloween specials',cost_to_make=12.55,price=19.99,category='clothing',prood_notes='All sales are final!',qty=2)
# p2=Products(sku=4523,prod_name='Jason Jacket', prood_description='Friday the 13th decals',cost_to_make=22.75,price=39.99,category='clothing',prood_notes='All sales are final!',qty=2)

    def __repr__(self):
        return f"SKU: {self.sku} Name: {self.prod_name} Description: {self.prood_description} cost to make: {self.cost_to_make} Price: {self.price} Category: {self.category} Notes: {self.prood_notes}"


# DB table for Events
class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(100), unique=True, nullable=False)
    event_description = db.Column(db.String(500), unique=True, nullable=False)
    event_start_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    event_end_date = db.Column(db.String(20), unique=True, nullable=False)
    products_bought = db.Column(db.Integer, unique=True, nullable=True)
    products_sold = db.Column(db.Integer, unique=True, nullable=True)
    event_notes = db.Column(db.String(1000), unique=False, nullable=False)

    def __repr__(self):
        return f"Event Name: {self.event_name} Description: {self.event_description} Start Datew: {self.event_start_date} End Date: {self.event_end_date} Products Brought: {self.products_bought} Products Sold: {self.products_sold} Notes: {self.event_notes}"


# Routes for webpages
# @app.route("/")
# def hello():
#     return render_template("home_page.html")


@app.route("/", methods =['POST', 'GET'])
def prod_list():
    products = Products.query.order_by(Products.sku)
    if request.method == "POST":
        sku_num = request.form["sku"]
        return redirect(url_for("prod_details", sku_num=sku_num))
    else:
        return render_template("prod_list_page.html",products=products)


@app.route("/prod_details<sku_num>", methods=['GET', 'POST'])
def prod_details(sku_num):
    product = Products.query.filter_by(sku=str(sku_num)).first()
    return render_template("prod_details.html", product=product)


@app.route("/new_product_page", methods=["POST", "GET"])
def sku_search():
    if request.method == "POST":
        np = Products(sku=request.form["sku"],prod_name=request.form["Product Name"], prood_description=request.form["Product Description"],cost_to_make=request.form["Cost to Make"],price=request.form["Selling Price"],category=request.form["Product Category"],prood_notes=request.form["Quantity"],qty=request.form["Notes"])
        db.session.add(np)
        db.session.commit()
        return redirect(url_for("prod_list"))
    else:
        return render_template("new_product_page.html")


@app.route("/prod_filter_by_price<price_num>", methods=['GET', 'POST'])
def prod_filter_by_price(price_num):
    products =  Products.query.filter_by(price=str(price_num)).all()
    return render_template("prod_filter_by_price.html", products=products)