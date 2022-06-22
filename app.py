from cmath import e
from distutils.log import debug
from email.policy import default
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import DateTime
import requests
from datetime import datetime, date

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///vendor.db"
# app.run(debug=True)
db = SQLAlchemy(app)

# DB table for products
class Products(db.Model):
    sku = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    prod_name = db.Column(db.String(100), unique=True, nullable=False)
    prood_description = db.Column(db.String(500), unique=True, nullable=False)
    cost_to_make = db.Column(db.Float(), unique=False, nullable=False)
    price = db.Column(db.Float(), unique=False, nullable=False)
    category = db.Column(db.String(500), unique=False, nullable=False)
    qty = db.Column(db.Integer)
    prood_notes = db.Column(db.String(1000), unique=False, nullable=False)
    event_inventory = db.relationship("EventInventory", backref="products")

    def __init__(
        self,
        # sku,
        prod_name,
        prood_description,
        cost_to_make,
        price,
        category,
        prood_notes,
        qty,
        # event_inventory,
    ) -> None:
        # self.sku = sku
        self.prod_name = prod_name
        self.prood_description = prood_description
        self.cost_to_make = cost_to_make
        self.price = price
        self.category = category
        self.prood_notes = prood_notes
        self.qty = qty
        # self.event_inventory = event_inventory

    def __repr__(self):
        return f"SKU: {self.sku} Name: {self.prod_name} Description: {self.prood_description} cost to make: {self.cost_to_make} Price: {self.price} Category: {self.category} Notes: {self.prood_notes} event_inventory: {self.event_inventory}"


# DB table for Events
class Events(db.Model):
    # __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(100), unique=True, nullable=False)
    event_description = db.Column(db.String(500), unique=True, nullable=False)
    event_start_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    event_end_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    # products_brought = db.Column(db.Integer, unique=True, nullable=True)
    # products_sold = db.Column(db.Integer, unique=True, nullable=True)
    event_notes = db.Column(db.String(1000), unique=False, nullable=False)
    event_event_inventory = db.relationship("EventInventory", backref="events")

    def __init__(
        self,
        event_name,
        event_description,
        event_start_date,
        event_end_date,
        # products_brought,
        # products_sold,
        event_notes,
    ) -> None:
        # self.sku = sku
        self.event_name = event_name
        self.event_description = event_description
        self.event_start_date = event_start_date
        self.event_end_date = event_end_date
        # self.products_brought = products_brought
        # self.products_sold = products_sold
        self.event_notes = event_notes

    def __repr__(self):
        return f"Event Name: {self.event_name} Description: {self.event_description} Start Datew: {self.event_start_date} End Date: {self.event_end_date} Notes: {self.event_notes}  event_inventory: {self.event_event_inventory}"


# DB table for Inventory Brought to Events
class EventInventory(db.Model):
    event_inv_id = db.Column(db.Integer, primary_key=True)
    sku_num = db.Column(db.Integer, db.ForeignKey("products.sku"))
    qty_brought = db.Column(db.Integer)
    qty_sold = db.Column(db.Integer)
    event_name = db.Column(db.Integer, db.ForeignKey("events.event_name"))

    def __init__(self, sku_num, qty_brought, qty_sold, event_name) -> None:
        self.sku_num = sku_num
        self.qty_brought = qty_brought
        self.qty_sold = qty_sold
        self.event_name = event_name

    def __repr__(self):
        return f"ID: {self.event_inv_id} SKU: {self.sku_num} Qty Brought: {self.qty_brought} Qty sold: {self.qty_sold} Event Name: {self.event_name}"


# Routes for webpages

# Home page lists all products in table
@app.route("/", methods=["POST", "GET"])
def prod_list():
    products = Products.query.order_by(Products.sku)
    if request.method == "POST":
        sku_num = request.form["sku"]
        return redirect(url_for("prod_details", sku_num=sku_num))
    else:
        return render_template("prod_list_page.html", products=products)


# Event lists all events in table
@app.route("/events_list_page", methods=["POST", "GET"])
def event_list():
    events = Events.query.order_by(Events.id)
    return render_template("event_list_page.html", events=events)


# Event Inventory lists everythiong in table
@app.route("/event_inventory_list_page", methods=["POST", "GET"])
def event_inventory_list():
    products = Products.query.order_by(Products.sku)
    events = Events.query.order_by(Events.id)
    return render_template(
        "event_inventory_list_page.html",
        events=events,
        products=products,
    )


# Page to add new product to Products table
@app.route("/new_product_page", methods=["POST", "GET"])
def sku_search():
    if request.method == "POST":
        np = Products(
            # sku=request.form["sku"],
            prod_name=request.form["Product Name"],
            prood_description=request.form["Product Description"],
            cost_to_make=request.form["Cost to Make"],
            price=request.form["Selling Price"],
            category=request.form["Product Category"],
            prood_notes=request.form["Notes"],
            qty=request.form["Quantity"],
        )
        db.session.add(np)
        db.session.commit()
        return redirect(url_for("prod_list"))
    else:
        return render_template("new_product_page.html")


@app.route("/new_event_inventory_page", methods=["POST", "GET"])
def event_inv_crteate():
    if request.method == "POST":
        nei = EventInventory(
            sku_num=request.form["SKU Number"],
            qty_brought=request.form["QTY Brought"],
            qty_sold=request.form["Event QTY Sold"],
            event_name=request.form["Event Name"],
        )
        # nei = EventInventory(sku_num=1,qty_brought=2,qty_sold='')
        db.session.add(nei)
        db.session.commit()
        return redirect(url_for("event_inventory_list"))
    else:
        return render_template("new_event_inventory_page.html")


@app.route("/new_event_page", methods=["POST", "GET"])
def new_event():
    if request.method == "POST":
        # print(response.content)
        ne = Events(
            event_name=request.form["Event Name"],
            event_description=request.form["Event Description"],
            event_start_date=datetime.strptime(
                request.form["Event Start Date"], "%Y-%m-%d"
            ),
            event_end_date=datetime.strptime(
                request.form["Event End Date"], "%Y-%m-%d"
            ),
            # products_brought=request.form["Products Brought"],
            # products_sold=request.form["Products Sold"],
            event_notes=request.form["Event Notes"],
        )
        db.session.add(ne)
        db.session.commit()
        return redirect(url_for("event_list"))
    else:
        return render_template("new_event_page.html")


# Page is a view of like priced items accessed by clicking on price from any product list
@app.route("/prod_filter_by_price_<price_num>", methods=["GET", "POST"])
def prod_filter_by_price(price_num):
    products = Products.query.filter_by(price=str(price_num)).all()
    return render_template("prod_filter_by_price.html", products=products)


# Page is a view of items with same category accessed by clicking on price from any product list
@app.route("/prod_filter_by_category_<category>", methods=["GET", "POST"])
def prod_filter_by_category(category):
    products = Products.query.filter_by(category=str(category)).all()
    return render_template("prod_filter_by_category.html", products=products)


# Page to add new product to Products table


# Event detail page shows single event and all details
@app.route("/event_details<id_num>", methods=["GET", "POST"])
def event_details(id_num):
    event = Events.query.filter_by(id=str(id_num)).first()
    events_inventory = EventInventory.query.filter_by(
        event_name=str(event.event_name)
    ).all()

    return render_template(
        "event_details.html", event=event, events_inventory=events_inventory
    )


# Product detail page shows single SKU and all details
@app.route("/prod_details<sku_num>", methods=["GET", "POST"])
def prod_details(sku_num):
    product = Products.query.filter_by(sku=str(sku_num)).first()
    return render_template("prod_details.html", product=product)
