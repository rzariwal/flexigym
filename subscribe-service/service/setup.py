import os

from flask import Flask
from subscribe_api import subscribe_api_blueprint
import model.model as model
#from flask_cors import CORS

SWAGGER_URL = '/api/docs'
API_URL = '/api/subscribe/docs.json'


def create_app():
    app = Flask(__name__)
    # CORS(app)

    basedir = os.path.abspath(__file__)

    app.config.update(
        dict(
            SECRET_KEY="subscribe secretkey",
            WTF_CSRF_SECRET_KEY="subscribe csrf secret key",
            # SQLALCHEMY_DATABASE_URI=f'mysql+mysqlconnector://root:test@flexigym-subscribe-api-db/subscribe',
            SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(basedir) + 'flexigym-subscribe.db',
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JSON_SORT_KEYS=False
        )
    )

    model.init_app(app)
    model.create_tables(app)

    app.register_blueprint(subscribe_api_blueprint)

    return app
