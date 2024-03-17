from flask import Flask 
from flask_sqlalchemy import SQLAlchemy

# global accessible libraries
db = SQLAlchemy()

def create_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    # Initialize Plugins
    db.init_app(app)

    with app.app_context():
        from . import routes
        
        db.create_all()

        return app