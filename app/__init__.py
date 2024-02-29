from flask import Flask
from config import Config
from app.extensions import db, scheduler
from app.helpers import validate_env_vars
import sys, logging


# Flask application factory function.
def create_app(config_class=Config):
    # Setup logging and handlers
    logging.getLogger().handlers.clear()
    formatter = logging.Formatter('%(asctime)s %(levelname)s VCSP %(message)s')
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(logging.INFO)

    # Validate Env. vars
    validate_env_vars()

    # Flask app instance
    logging.info("Initializing VCSP S3 Indexer Flask application.")
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions
    logging.info("Validating / Initializing sqlite3 application DB.")
    # Extension: SQLAlchemy
    from app.models.vcsp import Event
    db.init_app(app)
    with app.app_context():
        db.create_all()
    # Extension: APScheduler
    scheduler.init_app(app)
    scheduler.start()

    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.vcsp import bp as vcsp_bp
    app.register_blueprint(vcsp_bp, url_prefix='/vcsp')

    return app

