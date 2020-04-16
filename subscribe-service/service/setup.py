import os

from flask import Flask
from subscribe_api import subscribe_api_blueprint
import model.model as model

SWAGGER_URL = '/service/docs'
API_URL = '/service/subscribe/docs.json'


def create_app():
    app = Flask(__name__)

    basedir = os.path.abspath(__file__)

    app.config.update(
        dict(
            SECRET_KEY="subscribe secretkey",
            WTF_CSRF_SECRET_KEY="subscribe csrf secret key",
            #SQLALCHEMY_DATABASE_URI=f'mysql+mysqlconnector://root:test@flexigym-subscribe-service-db/subscribe',
            SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(basedir) + 'flexigym-subscribe.db',
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JSON_SORT_KEYS=False
        )
    )

    model.init_app(app)
    model.create_tables(app)

    app.register_blueprint(subscribe_api_blueprint)
    return app
