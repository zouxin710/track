from flask import Flask
from playhouse.flask_utils import FlaskDB

from apps.models import mysql_database
from apps.shipments.views import order_bp, track_bp


def create_app():
    app = Flask(__name__)

    FlaskDB(app, mysql_database)
    init_routes(app)

    return app


def init_routes(app):
    app.register_blueprint(order_bp, url_prefix="/shipments")
    app.register_blueprint(track_bp, url_prefix="/shipments")


app = create_app()