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
from app.schemas.transaction_schema import transaction_schema, transaction_update_schema
from marshmallow import ValidationError

txn_bp = Blueprint("transactions", __name__, url_prefix="/transactions")


@txn_bp.route("", methods=["POST"])
@login_required
@role_required("ADMIN")
def create_txn():
    """
    Insert a financial record into the database.
    ---
    tags:
      - Transactions
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            amount:
              type: number
              example: 450.50
            type:
              type: string
              example: EXPENSE
            category_id:
              type: integer
              example: 1
            date:
              type: string
              example: 2026-04-05
            description:
              type: string
              example: Quarterly taxes
    responses:
      201:
        description: Transaction inserted perfectly.
      400:
        description: Schema validation failed.
    """
    data = request.get_json()

    try:
        validated_data = transaction_schema.load(data)
    except ValidationError as err:
        return jsonify({"error": "Validation failed", "fields": err.messages}), 400

    try:
        txn = create_transaction(validated_data, request.user.id)
        return jsonify({"message": "Transaction created"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@txn_bp.route("", methods=["GET"])
@login_required
@role_required("ADMIN", "ANALYST")
def list_txns():
    """
    Query, search, limit, and extract transaction vectors.
    ---
    tags:
      - Transactions
    security:
      - Bearer: []
    parameters:
      - name: page
        in: query
        type: integer
      - name: per_page
        in: query
        type: integer
      - name: deleted
        in: query
        type: boolean
        description: Access Recycle Bin (Blocks Analysts)
    responses:
      200:
        description: Returns paginated response blocks.
    """
    filters = request.args.to_dict()

    if request.user.role.value == "ANALYST" and filters.get("deleted") == "true":
        return jsonify({"error": "Forbidden: Analysts cannot access the recycle bin."}), 403

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
    """
    Partially edit a transaction parameter.
    ---
    tags:
      - Transactions
    security:
      - Bearer: []
    parameters:
      - name: txn_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            amount:
              type: number
              example: 500.00
    responses:
      200:
        description: Successfully mutated data.
    """
    data = request.get_json()

    try:
        validated_data = transaction_update_schema.load(data)
    except ValidationError as err:
        return jsonify({"error": "Validation failed", "fields": err.messages}), 400

    try:
        update_transaction(txn_id, validated_data)
        return jsonify({"message": "Transaction updated"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@txn_bp.route("/<int:txn_id>", methods=["DELETE"])
@login_required
@role_required("ADMIN")
def delete_txn(txn_id):
    """
    Soft Delete a Transaction into the bin.
    ---
    tags:
      - Transactions
    security:
      - Bearer: []
    parameters:
      - name: txn_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Hidden from main query maps.
    """
    try:
        delete_transaction(txn_id)
        return jsonify({"message": "Transaction deleted"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@txn_bp.route("/<int:txn_id>/restore", methods=["PUT"])
@login_required
@role_required("ADMIN")
def restore_txn(txn_id):
    """
    Rescue a Soft-Deleted record.
    ---
    tags:
      - Transactions
    security:
      - Bearer: []
    parameters:
      - name: txn_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Restored accurately.
    """
    try:
        restore_transaction(txn_id)
        return jsonify({"message": "Transaction restored"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@txn_bp.route("/<int:txn_id>/permanent", methods=["DELETE"])
@login_required
@role_required("ADMIN")
def permanent_delete_txn(txn_id):
    """
    Forcefully drop row from persistent MySQL volumes.
    ---
    tags:
      - Transactions
    security:
      - Bearer: []
    parameters:
      - name: txn_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Irreversible database drop accomplished.
    """
    try:
        permanent_delete(txn_id)
        return jsonify({"message": "Deleted permanently"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400