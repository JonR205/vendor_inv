from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///vendor.db"
app.run(debug=True)
app.templates_auto_reload = True
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
            prod_name,
            prood_description,
            cost_to_make,
            price,
            category,
            prood_notes,
            qty,
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
        return f"Event Name: {self.event_name} Description: {self.event_description} Start Date: {self.event_start_date} End Date: {self.event_end_date} Notes: {self.event_notes}  event_inventory: {self.event_event_inventory}"


# DB table for Inventory Brought to Events
class EventInventory(db.Model):
    event_inv_id = db.Column(db.Integer, primary_key=True)
    sku_num = db.Column(db.Integer, db.ForeignKey("products.sku"))
    qty_brought = db.Column(db.Integer)
    qty_sold = db.Column(db.Integer)
    event_name = db.Column(db.String(500), db.ForeignKey("events.event_name"))

    def __init__(self, sku_num, qty_brought, qty_sold, event_name) -> None:
        self.sku_num = sku_num
        self.qty_brought = qty_brought
        self.qty_sold = qty_sold
        self.event_name = event_name

    def __repr__(self):
        return f"ID: {self.event_inv_id} SKU: {self.sku_num} Qty Brought: {self.qty_brought} Qty sold: {self.qty_sold} Event Name: {self.event_name}"


db.create_all()


# Routes for webpages

# Home page lists all products in table
@app.route("/", methods=["POST", "GET"])
def prod_list():
    products = Products.query.order_by(Products.sku)
    if request.method == "POST":
        sku_num = request.form["sku"]
        product = Products.query.get_or_404(sku_num)
        db.session.delete(product)
        db.session.commit()
        return render_template("prod_list_page.html", products=products)
    else:
        return render_template("prod_list_page.html", products=products)


# Product detail page shows single SKU and all details
@app.route("/prod_details<sku_num>", methods=["GET", "POST"])
def prod_details(sku_num):
    product = Products.query.filter_by(sku=str(sku_num)).first()
    return render_template("prod_details.html", product=product)


# Page is a view of products filter by a give type and parameter
@app.route("/prod_filter_by", methods=["GET", "POST"])
def prod_filter_by():
    filter_type = request.args.get('filter_type')
    pram = request.args.get('pram')

    if filter_type == "price":
        products = Products.query.filter_by(price=str(pram)).all()
    if filter_type == "cost":
        products = Products.query.filter_by(cost_to_make=str(pram)).all()
    if filter_type == "category":
        products = Products.query.filter_by(category=str(pram)).all()

    return render_template("prod_list_page.html", products=products)


# Page to add new product to Products table
@app.route("/new_product_page", methods=["POST", "GET"])
def new_product():
    if request.method == "POST":
        np = Products(
            prod_name=request.form["productName"],
            prood_description=request.form["productDescription"],
            cost_to_make=request.form["productCost"],
            price=request.form["productPrice"],
            category=request.form["productCategory"],
            prood_notes=request.form["productNotes"],
            qty=request.form["productQuantity"],
        )
        db.session.add(np)
        db.session.commit()
        return redirect(url_for("prod_list"))
    else:
        return render_template("product_form_page.html", pu_curr=None)


# page to update product details
@app.route("/prod_update<sku_num>", methods=["GET", "POST"])
def prod_update(sku_num):
    if request.method == "POST":
        up = Products.query.filter_by(sku=sku_num)
        up.update(
            dict(
                prod_name=request.form["Product Name"],
                prood_description=request.form["Product Description"],
                cost_to_make=request.form["Cost to Make"],
                price=request.form["Selling Price"],
                category=request.form["Product Category"],
                prood_notes=request.form["Notes"],
                qty=request.form["Quantity"],
            )
        )
        db.session.commit()
        return redirect(url_for("prod_list"))
    else:
        pu_curr = Products.query.filter_by(sku=sku_num).first()
        return render_template("product_form_page.html", pu_curr=pu_curr)


# Event lists all events in table
@app.route("/event_list_page", methods=["POST", "GET"])
def event_list():
    events = Events.query.order_by(Events.id)
    return render_template("event_list_page.html", events=events)
    # test


# Event detail page shows single event and all details
@app.route("/event_details<id_num>", methods=["GET", "POST"])
def event_details(id_num):
    event = Events.query.filter_by(id=str(id_num)).first()
    events_inventory = EventInventory.query.filter_by(
        event_name=str(event.event_name)
    ).all()
    if request.method == "POST" and request.form["close_inventory"]:
        for ei in events_inventory:
            pu_qty = Products.query.filter_by(sku=ei.sku_num).first()
            current_qty = pu_qty.qty
            ei_qty = EventInventory.query.filter_by(
                event_inv_id=str(ei.event_inv_id)
            ).first()
            ei_current_qty = ei_qty.qty_brought
            ei_qty_sold = ei_qty.qty_sold
            if ei_qty_sold:
                math = int(ei_current_qty) - int(ei_qty_sold)
                pu = Products.query.filter_by(sku=str(ei.sku_num))
                pu.update(dict(qty=current_qty + math))
                db.session.commit()
        return redirect(url_for("event_list"))
    else:
        return render_template(
            "event_details.html", event=event, events_inventory=events_inventory
        )


@app.route("/modal_<event_inv_id_num>_<sku_num_num>", methods=["GET", "POST"])
def modal(event_inv_id_num, sku_num_num):
    ei = EventInventory.query.filter_by(event_inv_id=str(event_inv_id_num))
    pu_qty = Products.query.filter_by(sku=sku_num_num).first()
    current_qty = pu_qty.qty
    ei_qty = EventInventory.query.filter_by(event_inv_id=str(event_inv_id_num)).first()
    ei_current_qty = ei_qty.qty_brought
    if request.method == "POST":
        if request.form["QTY Brought"]:
            ei.update(dict(qty_brought=int(request.form["QTY Brought"])))
            math = int(request.form["QTY Brought"]) - ei_current_qty
            print(f"MATH: {math}")
            pu = Products.query.filter_by(sku=str(sku_num_num))
            pu.update(dict(qty=current_qty - math))

        if request.form["Event QTY Sold"]:
            ei.update(dict(qty_sold=int(request.form["Event QTY Sold"])))

        # ei.sku_num = ei.sku_num
        # #     ei.event_name = (str(event_name_name),)
        # #     if request.form["QTY Brought"]:
        # #         ei.qty_brought = (int(request.form["QTY Brought"]),)
        # #     else:
        # #         ei.qty_brought = ei.qty_brought
        # ei.qty_sold = (int(request.form["Event QTY Sold"]),)
        db.session.commit()
        return redirect(url_for("event_list"))
    else:
        return render_template("modal.html", ei=ei, ei_current_qty=ei_current_qty)


@app.route("/new_event_page", methods=["POST", "GET"])
def new_event():
    if request.method == "POST":
        ne = Events(
            event_name=request.form["eventName"],
            event_description=request.form["eventDescription"],
            event_start_date=datetime.strptime(
                request.form["eventStartDate"], "%Y-%m-%d"
            ),
            event_end_date=datetime.strptime(
                request.form["eventEndDate"], "%Y-%m-%d"
            ),
            event_notes=request.form["eventNotes"],
        )
        db.session.add(ne)
        db.session.commit()
        return redirect(url_for("event_list"))
    else:
        return render_template("new_event_page.html")


# -------------------------------------------------------------------------------

# Event Inventory lists everythiong in table
@app.route("/event_inventory_list_page", methods=["POST", "GET"])
def event_inventory_list():
    products = Products.query.order_by(Products.sku)
    events = Events.query.order_by(Events.id)
    events_inventory = EventInventory.query.order_by(EventInventory.event_inv_id)
    return render_template(
        "event_inventory_list_page.html",
        events=events,
        products=products,
        events_inventory=events_inventory,
    )


@app.route("/new_event_inventory_page", methods=["POST", "GET"])
def event_inv_crteate():
    if request.method == "POST":
        nei = EventInventory(
            sku_num=request.form["SKU Number"],
            qty_brought=request.form["QTY Brought"],
            qty_sold=request.form["Event QTY Sold"],
            event_name=request.form["Event Name"],
        )
        pu = Products.query.filter_by(sku=str(request.form["SKU Number"]))
        # puq = pu.qty
        pu.update(dict(qty=request.form["QTY Brought"]))
        db.session.add(nei)
        db.session.commit()
        return redirect(url_for("event_inventory_list"))
    else:
        return render_template("new_event_inventory_page.html")

# Page to add new product to Products table
