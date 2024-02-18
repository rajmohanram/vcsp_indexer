from flask import Flask, url_for
from config import Config


# Flask application factory function.
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here

    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.vcsp import bp as vcsp_bp
    app.register_blueprint(vcsp_bp, url_prefix='/vcsp')

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app
