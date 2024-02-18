from flask import Blueprint

bp = Blueprint('vcsp', __name__)

from app.vcsp import routes
