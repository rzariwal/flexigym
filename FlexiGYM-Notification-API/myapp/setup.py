from flask import Flask
from notification_api import notification_api_blueprint
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
import models as models
import os

SWAGGER_URL = '/api/docs'
API_URL = '/api/sms/docs.json'


def create_app():
    app = Flask(__name__)
    cors = CORS(app)

    basedir = os.path.abspath(__file__)

    app.config.update(dict(
        SECRET_KEY="powerful secretkey",
        WTF_CSRF_SECRET_KEY="a csrf secret key",
        # SQLALCHEMY_DATABASE_URI='mysql+mysqlconnector://root:test@notification_db/notification',
        SQLALCHEMY_DATABASE_URI=f'mysql+mysqlconnector://root:test@flexigym-notification-api-db/notification',
        #SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(basedir + 'flexigym-notification_api.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JSON_SORT_KEYS=False

    ))

    models.init_app(app)
    models.create_tables(app)

    app.register_blueprint(notification_api_blueprint)

    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
    )
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

    return app
