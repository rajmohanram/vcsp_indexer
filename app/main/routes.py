from flask import render_template, send_from_directory, url_for, redirect
from app.main import bp
import os


@bp.route('/')
def index():
    return redirect(url_for('vcsp.index'))


@bp.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(bp.root_path, '../static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


