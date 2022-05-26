from multiprocessing import connection
import sqlite3

from colorama import Cursor


connection = sqlite3.connect("vendor_inventory")

cursor = connection.cursor()


command1 = """CREATE TABLE IF NOT EXISTS
warehouse_inv(sku INTEGER PRIMARY KEY, product_name TEXT, prod_descrition TEXT, cost_to_make FLOAT, price FLOAT, category TEXT, notes TEXT)"""

cursor.execute(command1)


command2 = """CREATE TABLE IF NOT EXISTS
event_info(event_id INTEGER PRIMARY KEY, event_name TEXT, event_description TEXT, start_date TEXT, start_date TEXT, products_brought FOREIGNKEY(sku) REFERENCES warehouse_inv(sku), products_sold FOREIGNKEY(sku) REFERENCES warehouse_inv(sku), notes TEXT)"""


cursor.execute(command2)
