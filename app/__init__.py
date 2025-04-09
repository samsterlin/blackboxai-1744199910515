from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Initialize Flask extensions
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configure the Flask application
    app.config['SECRET_KEY'] = 'your-secret-key'  # Change this to a secure secret key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ota_manager.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize CORS
    CORS(app)
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    from app.routes.ota_settings import ota_settings_bp
    from app.routes.channel_manager import channel_manager_bp
    
    app.register_blueprint(ota_settings_bp, url_prefix='/api/settings')
    app.register_blueprint(channel_manager_bp, url_prefix='/api/channels')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
