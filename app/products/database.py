
import os
from tinydb import TinyDB, Query

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

DATABASE_PATH = os.path.join(DATA_DIR, "products.json")

db = TinyDB(DATABASE_PATH, indent=4)

products_table = db.table("products")
metadata_table = db.table("metadata")

ProductQuery = Query()