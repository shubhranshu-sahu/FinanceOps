from flask import Blueprint, request, jsonify
from app.services.auth_service import register_user, login_user
from app.limiter import limiter

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["POST"])
@limiter.limit("5 per minute")
def register():
    data = request.get_json()
 
    try:
        user = register_user(data)
        return jsonify({"message": "User registered successfully"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@auth_bp.route("/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    data = request.get_json()

    try:
        token, user = login_user(data)
        return jsonify({
            "token": token,
            "user": {
                "id": user.id,
                "email": user.email,
                "role": user.role.value
            }
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 401