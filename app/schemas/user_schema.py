from marshmallow import Schema, fields, validate, ValidationError


# 🔹 Custom Error Messages for Validation
def must_not_be_blank(value):
    if not value or value.strip() == "":
        raise ValidationError("Field cannot be empty.")


# 🔹 Base User Schema
class UserSchema(Schema):
    email = fields.Email(
        required=True,
        validate=must_not_be_blank,
        error_messages={
            "required": "Email is required",
            "invalid": "Invalid email format",
        },
    )
    name = fields.String(
        required=True,
        validate=[must_not_be_blank, validate.Length(min=2, max=50)],
        error_messages={
            "required": "Name is required",
            "invalid": "Name must be between 2-50 characters",
        },
    )
    password = fields.String(
        required=True,
        validate=validate.Length(min=6),
        error_messages={
            "required": "Password is required",
            "invalid": "Password must be at least 6 characters long",
        },
    )
    user_type = fields.String(
        required=True,
        validate=validate.OneOf(["individual", "organization", "department"]),
        error_messages={
            "required": "User type is required",
            "invalid": "Invalid user type",
        },
    )


# 🔹 Organization Schema (Extends UserSchema)
class OrganizationSchema(UserSchema):
    organization_name = fields.String(
        required=True,
        validate=[must_not_be_blank, validate.Length(min=3, max=100)],
        error_messages={
            "required": "Organization name is required",
            "invalid": "Organization name must be 3-100 characters long",
        },
    )
    address = fields.String(
        required=True,
        validate=[must_not_be_blank, validate.Length(min=5, max=200)],
        error_messages={
            "required": "Organization address is required",
            "invalid": "Address must be 5-200 characters long",
        },
    )


# 🔹 Department Schema (Extends UserSchema)
class DepartmentSchema(UserSchema):
    organization = fields.String(
        required=True,
        validate=must_not_be_blank,
        error_messages={"required": "Organization ID is required"},
    )
    department_name = fields.String(
        required=True,
        validate=[must_not_be_blank, validate.Length(min=2, max=100)],
        error_messages={
            "required": "Department name is required",
            "invalid": "Department name must be 2-100 characters long",
        },
    )


# 🔹 Login Schema
class LoginSchema(Schema):
    email = fields.Email(
        required=True,
        validate=must_not_be_blank,
        error_messages={
            "required": "Email is required",
            "invalid": "Invalid email format",
        },
    )
    password = fields.String(
        required=True,
        validate=must_not_be_blank,
        error_messages={"required": "Password is required"},
    )
