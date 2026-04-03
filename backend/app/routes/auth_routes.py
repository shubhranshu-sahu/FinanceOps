from flask import Blueprint, request, jsonify
from app.services.auth_service import register_user, login_user
from app.limiter import limiter

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["POST"])
@limiter.limit("5 per minute")
def register():
    """
    Registers a new user inside the system.
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: Jane Doe
            email:
              type: string
              example: jane.doe@example.com
            password:
              type: string
              example: securepassword123
    responses:
      201:
        description: User registered successfully
      400:
        description: Missing fields or invalid format
    """
    data = request.get_json()
 
    try:
        user = register_user(data)
        return jsonify({"message": "User registered successfully"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@auth_bp.route("/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    """
    Generates a secure JSON Web Token for the user.
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              example: jane.doe@example.com
            password:
              type: string
              example: securepassword123
    responses:
      200:
        description: Authentication successful. JWT Payload returned.
      401:
        description: Invalid credentials.
    """
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