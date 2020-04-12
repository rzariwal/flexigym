import os

from flask import Flask
from service import advertise_api_blueprint
import service.models as model

SWAGGER_URL = '/service/docs'
API_URL = '/service/advertise/docs.json'


def create_app():
    app = Flask(__name__)

    basedir = os.path.abspath(__file__)

    app.config.update(
        dict(
            SECRET_KEY="advertise secretkey",
            WTF_CSRF_SECRET_KEY="advertise csrf secret key",
            #SQLALCHEMY_DATABASE_URI=f'mysql+mysqlconnector://root:1234@localhost:3306/flexigym-advertise-service',
            #SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(basedir) + 'advertise-service.db',
            SQLALCHEMY_DATABASE_URI=f'mysql+mysqlconnector://root:1234@flexigym-advertise-service-db/flexigym-advertise-service',
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JSON_SORT_KEYS=False
        )
    )

    model.init_app(app)
    model.create_tables(app)

    app.register_blueprint(advertise_api_blueprint)
    return app
