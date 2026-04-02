import enum


class UserRole(enum.Enum):
    VIEWER = "VIEWER"
    ANALYST = "ANALYST"
    ADMIN = "ADMIN"


class TransactionType(enum.Enum):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"