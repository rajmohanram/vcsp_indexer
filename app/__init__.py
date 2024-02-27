from flask import Flask
from config import Config
from app.extensions import db


# Flask application factory function.
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)
    from app.models.vcsp import Event
    with app.app_context():
        db.create_all()

    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.vcsp import bp as vcsp_bp
    app.register_blueprint(vcsp_bp, url_prefix='/vcsp')

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app

