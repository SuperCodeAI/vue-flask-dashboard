from flask import Flask
from flask_cors import CORS
from config import Config
from .extensions import db
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate  # Import Migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    app.config['JWT_SECRET_KEY'] = '123456'  # Change this!
    jwt = JWTManager(app)
    
    db.init_app(app)
    CORS(app)
    
    migrate = Migrate(app, db)  # Initialize Migrate here
    
    with app.app_context():
        from .models import User
        db.create_all()

    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app