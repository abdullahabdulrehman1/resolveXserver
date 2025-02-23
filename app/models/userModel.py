from bson.objectid import ObjectId
from flask import current_app
from pymongo import MongoClient
from werkzeug.security import check_password_hash, generate_password_hash

from app import mongo


class User:
    """Base User Model"""

    @staticmethod
    def create_user(email, password, user_type, extra_fields={}):
        """Create a new user in MongoDB"""
        user_data = {
            "email": email,
            "password": generate_password_hash(password),  # Hash password before saving
            "user_type": user_type,
            "otp_request_count": 0,  # Initialize OTP request count
            "last_request_time": None  # Initialize last request time
        }
        user_data.update(extra_fields)  # Add additional fields

        result = mongo.db.users.insert_one(user_data)  # Insert into MongoDB
        return str(result.inserted_id)

    @staticmethod
    def check_user(email, password):
        """Check if user exists and validate password"""
        user = mongo.db.users.find_one({"email": email})
        if user and check_password_hash(user["password"], password):
            return user  # Return full user data
        return None

    @staticmethod
    def find_user_by_email(email):
        """Fetch user by email"""
        client = MongoClient(current_app.config["MONGO_URI"])
        db = client[current_app.config["MONGO_DBNAME"]]
        user = db.users.find_one({"email": email})
        return user

    @staticmethod
    def find_user_by_id(user_id):
        """Fetch user by ID"""
        try:
            return mongo.db.users.find_one({"_id": ObjectId(user_id)})
        except:
            return None
    @staticmethod
    def update_user_by_id(user_id, update_data):
        """Update a user by ID"""
        return mongo.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})


class Individual(User):
    """Individual User Model"""

    @staticmethod
    def create_individual(name, email, password):
        return User.create_user(email, password, "individual", {"name": name})


class Organization(User):
    """Organization User Model"""

    @staticmethod
    def create_organization(organization_name, address, email, password):
        return User.create_user(
            email,
            password,
            "organization",
            {"organization_name": organization_name, "address": address},
        )


class Department(User):
    """Department User Model"""

    @staticmethod
    def create_department(name, department_name, organization_id, email, password):
        return User.create_user(
            email,
            password,
            "department",
            {
                "name": name,
                "department_name": department_name,
                "organization_id": organization_id,
            },
        )
