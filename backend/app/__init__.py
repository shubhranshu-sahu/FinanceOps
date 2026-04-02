from flask import Flask
from .models import db
from flask_migrate import Migrate
import os


def create_app():
    app = Flask(__name__)

    # Config
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://root:1234@localhost/financeops"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Init extensions
    db.init_app(app)
    migrate = Migrate(app, db)

    return app