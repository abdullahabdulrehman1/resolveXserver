import os

from dotenv import load_dotenv

load_dotenv()  # Load environment variables

class Config:
    MONGO_URI = os.getenv("MONGO_URI")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    MONGO_DBNAME = os.getenv("MONGO_DBNAME")

    # MongoEngine settings
    
