from flask import jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token
from marshmallow import ValidationError

from app.libs.error_helper import handle_error
from app.models.userModel import Department, Individual, Organization, User
from app.schemas.user_schema import (DepartmentSchema, OrganizationSchema,
                                     UserSchema)


def register():
    try:
        data = request.get_json()
        user_type = data.get("user_type")

        if not user_type:
            return handle_error("User type is required", 400)

        # Check for existing user before validation
        existing_user = User.find_user_by_email(data.get("email"))
        if existing_user:
            return handle_error("Email already registered", 409)

        # Validate and create user based on type
        if user_type == "individual":
            schema = UserSchema()
            data = schema.load(data)
            user_id = Individual.create_individual(
                name=data["name"], email=data["email"], password=data["password"]
            )

        elif user_type == "organization":
            schema = OrganizationSchema()
            data = schema.load(data)
            user_id = Organization.create_organization(
                organization_name=data["organization_name"],
                address=data["address"],
                email=data["email"],
                password=data["password"],
            )

        elif user_type == "department":
            schema = DepartmentSchema()
            data = schema.load(data)
            user_id = Department.create_department(
                name=data["name"],
                department_name=data["department_name"],
                organization_id=data["organization"],
                email=data["email"],
                password=data["password"],
            )

        else:
            return handle_error("Invalid user type", 400)

        # Get the created user
        user = User.find_user_by_id(user_id)
        if not user:
            return handle_error("User not found after creation", 404)

        user_id = str(user["_id"])

        # Generate tokens using authhelper
        access_token = create_access_token(identity=user_id, fresh=True)
        refresh_token = create_refresh_token(identity=user_id)

        return (
            jsonify(
                {
                    "message": "User created successfully",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user_type": user_type,
                    "user_id": str(user["_id"]),
                }
            ),
            201,
        )

    except ValidationError as err:
        return handle_error("Validation failed", 400, details=err.messages)
    except ValueError as ve:
        return handle_error(str(ve), 400)
    except Exception as e:
        return handle_error(f"Registration failed: {str(e)}", 500)