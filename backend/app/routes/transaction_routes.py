from flask import Blueprint, request, jsonify
from app.services.transaction_service import (
    create_transaction,
    get_transactions,
    update_transaction,
    delete_transaction
)
from app.middleware.auth_middleware import login_required, role_required

txn_bp = Blueprint("transactions", __name__, url_prefix="/transactions")


@txn_bp.route("/", methods=["POST"])
@login_required
@role_required("ADMIN")
def create_txn():
    data = request.get_json()

    try:
        txn = create_transaction(data, request.user.id)
        return jsonify({"message": "Transaction created"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@txn_bp.route("/", methods=["GET"])
@login_required
def list_txns():
    filters = request.args.to_dict()

    txns = get_transactions(filters)

    result = []
    for t in txns:
        result.append({
            "id": t.id,
            "amount": float(t.amount),
            "type": t.type.value,
            "category": t.category.name,
            "date": str(t.date),
            "description": t.description,
            "created_by": t.user.name
        })

    return jsonify(result), 200


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