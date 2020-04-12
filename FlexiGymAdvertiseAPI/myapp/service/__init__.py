from flask import Blueprint

advertise_api_blueprint = Blueprint('service', __name__)

from . import advertise
from . import models