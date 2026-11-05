"""Entry point: builds the Flask app. The real code lives in the other modules."""
import os

from flask import Flask

from db import DB_PATH, init_db  # the tests import init_db from here, so keep it
from routes import register_routes

app = Flask(__name__)
register_routes(app)

if not os.path.exists(DB_PATH):
    init_db()
