from email.policy import default
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import DateTime


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///vendor.db"
db = SQLAlchemy(app)
headings = (
    "sku",
    "Product Name",
    "Product Description",
    "Cost to Make",
    "Price",
    "Category",
    "Notes",
)

data = (
    ("Jon", "rhine", "3", "4", "5", "6", "7"),
    ("Jon", "rhine", "3", "4", "5", "6", "7"),
    ("Jon", "rhine", "3", "4", "5", "6", "7"),
)

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
@app.route("/")
def hello():
    return render_template("home_page.html")


@app.route("/prod_list_page")
def prod_list():
    products = Products.query.order_by(Products.sku)
    return render_template(
        "prod_list_page.html", headings=headings, data=data, products=products
    )
