from app.models.user import User
from app.models import db
from app.models.enums import UserRole


def get_all_users():
    return User.query.all()


def update_user_role(user_id, role_str):
    user = User.query.get(user_id)

    if not user:
        raise ValueError("User not found")

    try:
        user.role = UserRole(role_str)
    except ValueError:
        raise ValueError("Invalid role")

    db.session.commit()
    return user


def update_user_status(user_id, is_active):
    user = User.query.get(user_id)

    if not user:
        raise ValueError("User not found")

    user.is_active = is_active
    db.session.commit()
    return user