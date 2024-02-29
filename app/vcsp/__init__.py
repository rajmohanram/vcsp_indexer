from flask import Blueprint

bp = Blueprint('vcsp', __name__)

from app.vcsp import routes, s3reindex, schedule_reindexing
