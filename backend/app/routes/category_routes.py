from flask import Blueprint, request, jsonify
from app.services.category_service import create_category, get_categories, update_category_status, update_category_name
from app.middleware.auth_middleware import login_required, role_required

cat_bp = Blueprint("categories", __name__, url_prefix="/categories")


@cat_bp.route("", methods=["POST"])
@login_required
@role_required("ADMIN")
def create_cat():
    data = request.get_json()

    try:
        category = create_category(data, request.user.id)
        return jsonify({"message": "Category created"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@cat_bp.route("", methods=["GET"])
@login_required
def list_categories():
    include_disabled = request.args.get("all") == "true"
    categories = get_categories(include_disabled)

    result = []
    for c in categories:
        result.append({
            "id": c.id,
            "name": c.name,
            "is_active": c.is_active
        })

    return jsonify(result), 200


@cat_bp.route("/<int:cat_id>/status", methods=["PUT"])
@login_required
@role_required("ADMIN")
def change_category_status(cat_id):
    data = request.get_json()

    try:
        update_category_status(cat_id, data["is_active"])
        return jsonify({"message": "Category status updated"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@cat_bp.route("/<int:cat_id>", methods=["PUT"])
@login_required
@role_required("ADMIN")
def rename_category(cat_id):
    data = request.get_json()
    try:
        update_category_name(cat_id, data["name"])
        return jsonify({"message": "Category renamed"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400