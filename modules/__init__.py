from flask import Blueprint

controller_bp = Blueprint('controller', __name__)

from modules import controller
