from flask import Blueprint

subscribe_api_blueprint = Blueprint('service', __name__)

from . import subscribe
from . import model
