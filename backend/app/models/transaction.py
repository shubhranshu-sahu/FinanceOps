from datetime import datetime
from . import db
from .enums import TransactionType


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)

    amount = db.Column(db.Numeric(12, 2), nullable=False)

    type = db.Column(
        db.Enum(TransactionType, name="transaction_types"),
        nullable=False
    )

    # category = db.Column(db.String(100), nullable=False, index=True)
    category_id = db.Column(
    db.Integer,
    db.ForeignKey("categories.id"),
    nullable=False,
    index=True )



    date = db.Column(db.Date, nullable=False, index=True)

    description = db.Column(db.Text, nullable=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    is_deleted = db.Column(db.Boolean, default=False, nullable=False)

    created_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # Relationship
    category = db.relationship("Category", backref="transactions")
    
    def __repr__(self):
        return f"<Transaction {self.id} - {self.type}>"