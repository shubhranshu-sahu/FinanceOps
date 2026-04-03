from app.models.transaction import Transaction
from app.models.category import Category
from app.models.enums import TransactionType
from app.models import db
from sqlalchemy import func


def get_dashboard_summary():

    # 🔹 Total Income
    total_income = db.session.query(
        func.coalesce(func.sum(Transaction.amount), 0)
    ).filter(
        Transaction.type == TransactionType.INCOME,
        Transaction.is_deleted == False
    ).scalar()

    # 🔹 Total Expense
    total_expense = db.session.query(
        func.coalesce(func.sum(Transaction.amount), 0)
    ).filter(
        Transaction.type == TransactionType.EXPENSE,
        Transaction.is_deleted == False
    ).scalar()

    # 🔹 Net Balance
    net_balance = total_income - total_expense

    # 🔹 Category Breakdown
    category_data = db.session.query(
        Category.name,
        func.sum(Transaction.amount)
    ).join(Transaction).filter(
        Transaction.is_deleted == False
    ).group_by(Category.name).all()

    category_breakdown = [
        {"category": name, "total": float(total)}
        for name, total in category_data
    ]

    # 🔹 Recent Transactions (last 5)
    recent = Transaction.query.filter_by(is_deleted=False) \
        .order_by(Transaction.created_at.desc()) \
        .limit(5).all()

    recent_transactions = [
        {
            "id": t.id,
            "amount": float(t.amount),
            "type": t.type.value,
            "category": t.category.name,
            "date": str(t.date)
        }
        for t in recent
    ]

    # 🔹 Monthly Trends
    monthly_data = db.session.query(
        func.date_format(Transaction.date, "%Y-%m"),
        func.sum(Transaction.amount)
    ).filter(
        Transaction.is_deleted == False
    ).group_by(
        func.date_format(Transaction.date, "%Y-%m")
    ).all()

    monthly_trends = [
        {"month": month, "total": float(total)}
        for month, total in monthly_data
    ]

    return {
        "total_income": float(total_income),
        "total_expense": float(total_expense),
        "net_balance": float(net_balance),
        "category_breakdown": category_breakdown,
        "recent_transactions": recent_transactions,
        "monthly_trends": monthly_trends
    }