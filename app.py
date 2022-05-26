from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import datetime
from sqlalchemy import DateTime


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)


class Products(db.Model):
    prod_id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.Integer, unique=True, nullable=False)
    prod_name = db.Column(db.String(100), unique=True, nullable=False)
    prood_description = db.Column(db.String(500), unique=True, nullable=False)
    cost_to_make = db.Column(db.Float(), unique=False, nullable=False)
    price = db.Column(db.Float(), unique=False, nullable=False)
    category = db.Column(db.String(500), unique=False, nullable=False)
    prood_notes = db.Column(db.String(1000), unique=False, nullable=False)
    # p1 = Products(sku=1234,prod_name="shirt",prood_description="holloween specials",cost_to_make=12.55,price=19.99,category="clothing",prood_notes="All sales are final!")

    def __repr__(self):
        return f"SKU: {self.sku} Name: {self.prod_name} Description: {self.prood_description} cost to make: {self.cost_to_make} Price: {self.price} Category: {self.category} Notes: {self.prood_notes}"


class Events(db.Model):
    event_id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(100), unique=True, nullable=False)
    event_description = db.Column(db.String(500), unique=True, nullable=False)
    event_start_date = db.Column(db.String(20), unique=True, nullable=False)
    event_end_date = db.Column(db.String(20), unique=True, nullable=False)
    products_bought = db.Column(db.Integer, unique=True, nullable=True)
    products_sold = db.Column(db.Integer, unique=True, nullable=True)
    event_notes = db.Column(db.String(1000), unique=False, nullable=False)

    def __repr__(self):
        return f"Event Name: {self.event_name} Description: {self.event_description} Start Datew: {self.event_start_date} End Date: {self.event_end_date} Products Brought: {self.products_bought} Products Sold: {self.products_sold} Notes: {self.event_notes}"


#     e1 = Events(event_name="Bent river fest", event_description="3 day outdoor event",event_start_date="2022-07-04",event_end_date="2022-07-07 11:59:59.715782", products_bought=1234,event_notes="will be hot bring water")


@app.route("/")
def hello():
    return render_template("home_page.html")
