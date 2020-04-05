import os

import model as models
from flask import Flask

SWAGGER_URL = '/api/docs'
API_URL = '/api/subscribe/docs.json'


def create_app():
    app = Flask(__name__)

    basedir = os.path.abspath(__file__)

    app.config.update(
        dict(
        SECRET_KEY="subscribe secretkey",
        WTF_CSRF_SECRET_KEY="subscribe csrf secret key",
        # SQLALCHEMY_DATABASE_URI='mysql+mysqlconnector://root:test@notification_db/notification',
        SQLALCHEMY_DATABASE_URI=f'mysql+mysqlconnector://root:test@flexigym-subscribe-api-db/subscribe',
        # SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(basedir + 'flexigym-notification_api.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JSON_SORT_KEYS=False
        )
    )

    models.init_app(app)
    models.create_tables(app)

    return app
