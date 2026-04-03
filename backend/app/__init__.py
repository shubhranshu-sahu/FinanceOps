from flask import Flask
from .models import db
from .limiter import limiter
from flask_migrate import Migrate
import os
from flask_cors import CORS   

from dotenv import load_dotenv

load_dotenv()



def create_app(test_config=None):
    app = Flask(__name__)

    # Config
    if test_config is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
            "DATABASE_URL",
            "mysql+pymysql://root:1234@localhost/financeops"
        )
    else:
        app.config.update(test_config)

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
   
    allowed_origins = os.getenv("CORS_ORIGINS", "").split(",")

    CORS(app, origins=allowed_origins)


    # Init extensions 
    db.init_app(app)
    limiter.init_app(app)
    migrate = Migrate(app, db)

    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes.user_routes import user_bp
    app.register_blueprint(user_bp)

    from app.routes.transaction_routes import txn_bp
    app.register_blueprint(txn_bp)

    from app.routes.category_routes import cat_bp
    app.register_blueprint(cat_bp)

    from app.routes.dashboard_routes import dashboard_bp
    app.register_blueprint(dashboard_bp)

    return app