import os
import logging
from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Log the JWT token from environment
jwt_token = os.getenv('JWT_TOKEN')
logger.info(f"JWT Token from environment: {jwt_token}")

# Initialize extensions
mongo = PyMongo()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    # Load Config
    app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["MONGO_DBNAME"] = os.getenv("MONGO_DBNAME")
    app.config["REFRESH_SECRET_KEY"] = os.getenv("REFRESH_SECRET_KEY")

    # Initialize Extensions
    mongo.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Register blueprints
    from app.routes.auth import auth_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app