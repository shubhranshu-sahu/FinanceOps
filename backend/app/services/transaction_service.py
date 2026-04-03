from app.models.transaction import Transaction
from app.models.category import Category
from app.models import db
from app.models.enums import TransactionType


# CREATE
def create_transaction(data, user_id):
    try:
        txn_type = TransactionType(data["type"])
    except ValueError:
        raise ValueError("Invalid transaction type")

    #  Validate category
    category = Category.query.get(data["category_id"])
    if not category or not category.is_active:
        raise ValueError("Invalid or inactive category")

    txn = Transaction(
        amount=data["amount"],
        type=txn_type,
        category_id=data["category_id"],
        date=data["date"],
        description=data.get("description"),
        user_id=user_id
    )

    db.session.add(txn)
    db.session.commit()

    return txn


# READ (WITH FILTERS, SORTING AND PAGINATION)
def get_transactions(filters, page=1, per_page=10):
    query = Transaction.query

    if filters.get("deleted") == "true":
        query = query.filter(Transaction.is_deleted == True)
    else:
        query = query.filter(Transaction.is_deleted == False)

    # Type filter (ENUM safe)
    if "type" in filters:
        try:
            txn_type = TransactionType(filters["type"])
            query = query.filter(Transaction.type == txn_type)
        except ValueError:
            raise ValueError("Invalid transaction type filter")

    # Category filter (by ID)
    if "category_id" in filters:
        query = query.filter(Transaction.category_id == filters["category_id"])

    # filter by category name (JOIN)
    if "category" in filters:
        query = query.join(Category).filter(Category.name == filters["category"].lower())

    # Date filter
    if "date" in filters:
        query = query.filter(Transaction.date == filters["date"])

    # Sorting -> latest first by actual creation time
    query = query.order_by(Transaction.created_at.desc())

    # Return paginated results
    return query.paginate(page=page, per_page=per_page, error_out=False)


# UPDATE
def update_transaction(txn_id, data):
    txn = Transaction.query.get(txn_id)

    if not txn or txn.is_deleted:
        raise ValueError("Transaction not found")

    if "amount" in data:
        txn.amount = data["amount"]

    if "type" in data:
        try:
            txn.type = TransactionType(data["type"])
        except ValueError:
            raise ValueError("Invalid transaction type")

    # Update category_id instead of category
    if "category_id" in data:
        category = Category.query.get(data["category_id"])
        if not category or not category.is_active:
            raise ValueError("Invalid or inactive category")

        txn.category_id = data["category_id"]

    if "date" in data:
        txn.date = data["date"]

    if "description" in data:
        txn.description = data["description"]

    db.session.commit()
    return txn


# DELETE (SOFT)
def delete_transaction(txn_id):
    txn = Transaction.query.get(txn_id)

    if not txn or txn.is_deleted:
        raise ValueError("Transaction not found")

    txn.is_deleted = True
    db.session.commit()

    return txn

# RESTORE (SOFT)
def restore_transaction(txn_id):
    txn = Transaction.query.get(txn_id)

    if not txn or not txn.is_deleted:
        raise ValueError("Transaction not found or not currently in recycle bin")

    txn.is_deleted = False
    db.session.commit()

    return txn


def permanent_delete(txn_id):
    txn = Transaction.query.get(txn_id)

    if not txn:
        raise ValueError("Transaction not found")

    db.session.delete(txn)
    db.session.commit()