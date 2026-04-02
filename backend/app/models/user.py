from datetime import datetime
from . import db
from .enums import UserRole


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False, index=True)

    password_hash = db.Column(db.String(255), nullable=False)

    role = db.Column(
        db.Enum(UserRole, name="user_roles"),
        nullable=False,
        default=UserRole.VIEWER,
    )

    is_active = db.Column(db.Boolean, default=True, nullable=False)

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
    transactions = db.relationship(
        "Transaction",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User {self.email}>"