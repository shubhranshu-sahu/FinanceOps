from flask import Blueprint, request, jsonify
from app.services.transaction_service import (
    create_transaction,
    get_transactions,
    update_transaction,
    delete_transaction,
    permanent_delete,
    restore_transaction
)
from app.middleware.auth_middleware import login_required, role_required

txn_bp = Blueprint("transactions", __name__, url_prefix="/transactions")


@txn_bp.route("", methods=["POST"])
@login_required
@role_required("ADMIN")
def create_txn():
    data = request.get_json()

    try:
        txn = create_transaction(data, request.user.id)
        return jsonify({"message": "Transaction created"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@txn_bp.route("", methods=["GET"])
@login_required
def list_txns():
    filters = request.args.to_dict()
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))

    try:
        pagination = get_transactions(filters, page=page, per_page=per_page)

        result = []
        for t in pagination.items:
            result.append({
                "id": t.id,
                "amount": float(t.amount),
                "type": t.type.value,
                "category": t.category.name,
                "date": str(t.date),
                "description": t.description,
                "created_by": t.user.name
            })

        return jsonify({
            "transactions": result,
            "total": pagination.total,
            "page": pagination.page,
            "pages": pagination.pages,
            "per_page": pagination.per_page
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@txn_bp.route("/<int:txn_id>", methods=["PUT"])
@login_required
@role_required("ADMIN")
def update_txn(txn_id):
    data = request.get_json()

    try:
        update_transaction(txn_id, data)
        return jsonify({"message": "Transaction updated"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@txn_bp.route("/<int:txn_id>", methods=["DELETE"])
@login_required
@role_required("ADMIN")
def delete_txn(txn_id):
    try:
        delete_transaction(txn_id)
        return jsonify({"message": "Transaction deleted"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@txn_bp.route("/<int:txn_id>/restore", methods=["PUT"])
@login_required
@role_required("ADMIN")
def restore_txn(txn_id):
    try:
        restore_transaction(txn_id)
        return jsonify({"message": "Transaction restored"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@txn_bp.route("/<int:txn_id>/permanent", methods=["DELETE"])
@login_required
@role_required("ADMIN")
def permanent_delete_txn(txn_id):
    try:
        permanent_delete(txn_id)
        return jsonify({"message": "Deleted permanently"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400