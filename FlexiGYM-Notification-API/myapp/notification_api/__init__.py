from flask import Blueprint

notification_api_blueprint = Blueprint('notification_api', __name__)

from . import routes