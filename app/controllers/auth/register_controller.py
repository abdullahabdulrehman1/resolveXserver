from flask import request, jsonify
from marshmallow import ValidationError
from app.libs.authhelper import generate_token, generate_refresh_token
from app.models.userModel import User, Individual, Organization, Department
from app.schemas.user_schema import UserSchema, OrganizationSchema, DepartmentSchema


def register():
    try:
        data = request.get_json()
        user_type = data.get("user_type")

        if not user_type:
            return jsonify({"error": "User type is required"}), 400

        # Check for existing user before validation
        existing_user = User.find_user_by_email(data.get("email"))
        if existing_user:
            return jsonify({"error": "Email already registered"}), 409

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
            return jsonify({"error": "Invalid user type"}), 400

        # Get the created user
        user = User.find_user_by_id(user_id)
        if not user:
            raise ValueError("User not found after creation")

        # Generate tokens
        access_token = generate_token(user)
        refresh_token = generate_refresh_token(user)

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
        return jsonify({"error": "Validation failed", "details": err.messages}), 400
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": f"Registration failed: {str(e)}"}), 500
