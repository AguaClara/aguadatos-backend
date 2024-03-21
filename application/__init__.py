from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
import os

# global accessible libraries
db = SQLAlchemy()

def create_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    config_type = os.getenv('CONFIG_TYPE', 'config.Config')
    app.config.from_object(config_type)

    # Initialize Plugins
    db.init_app(app)

    with app.app_context():
        from . import routes
        
        db.create_all()

        return app