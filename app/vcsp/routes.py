from app.vcsp import bp
from flask import render_template


@bp.route('/')
def index():
    return render_template('vcsp/index.html')


@bp.route('/s3reindex')
def reindex():
    return '<h1>Re-Index MinIO S3 bucket</h1>'
