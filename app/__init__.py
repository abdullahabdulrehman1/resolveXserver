import os
import logging
from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from flask_cors import CORS
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
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 60 * 60 * 24  # 24 hours
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = 60 * 60 * 24 * 30  # 7 days
    app.config['MAILJET_API_SECRET'] = os.getenv('MAILJET_API_SECRET')
    app.config['MAILJET_API_KEY'] = os.getenv('MAILJET_API_KEY')
    app.config['MAILJET_SENDER'] = os.getenv('MAILJET_SENDER')
    CORS(app,supports_credentials=True)
    # Initialize Extensions
    mongo.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Register blueprints
    from app.routes.auth import auth_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app