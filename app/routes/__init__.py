from flask import Blueprint


from app.routes.misc import misc_bp
from app.routes.auth import auth_bp
# Optional: Define an overall Blueprint (if needed)
bp = Blueprint("main", __name__)

# Expose all blueprints for import
__all__ = ["misc_bp","auth_bp"]
