from functools import wraps
from flask import request, jsonify
from app.utils.jwt_utils import decode_token
from app.models.user import User


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"error": "Missing token"}), 401

        try:
            token = auth_header.split(" ")[1]
        except IndexError:
            return jsonify({"error": "Invalid token format"}), 401

        payload = decode_token(token)

        if not payload:
            return jsonify({"error": "Invalid or expired token"}), 401

        user = User.query.get(payload["user_id"])

        if not user or not user.is_active:
            return jsonify({"error": "User not found or inactive"}), 401

        request.user = user

        return f(*args, **kwargs)

    return wrapper



def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if request.user.role.value not in roles:
                return jsonify({"error": "Forbidden"}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator