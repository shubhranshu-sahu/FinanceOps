from flask import Blueprint, jsonify, request
from app.services.user_service import (
    get_all_users,
    update_user_role,
    update_user_status
)
from app.middleware.auth_middleware import login_required, role_required

user_bp = Blueprint("users", __name__, url_prefix="/users")


@user_bp.route("", methods=["GET"])
@login_required
@role_required("ADMIN")
def list_users():
    users = get_all_users()

    result = []
    for u in users:
        result.append({
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "role": u.role.value,
            "is_active": u.is_active
        })

    return jsonify(result), 200


@user_bp.route("/<int:user_id>/role", methods=["PUT"])
@login_required
@role_required("ADMIN")
def change_role(user_id):
    data = request.get_json()

    try:
        user = update_user_role(user_id, data["role"])
        return jsonify({"message": "Role updated"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@user_bp.route("/<int:user_id>/status", methods=["PUT"])
@login_required
@role_required("ADMIN")
def change_status(user_id):
    data = request.get_json()

    try:
        user = update_user_status(user_id, data["is_active"])
        return jsonify({"message": "Status updated"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400