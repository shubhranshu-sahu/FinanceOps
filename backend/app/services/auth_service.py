from app.models import db
from app.models.user import User
from app.models.enums import UserRole
from app.utils.password_utils import hash_password, verify_password
from app.utils.jwt_utils import generate_token


def register_user(data):
    existing_user = User.query.filter_by(email=data["email"]).first()

    if existing_user:
        raise ValueError("Email already exists")

    user = User(
        name=data["name"],
        email=data["email"],
        password_hash=hash_password(data["password"]),
        role=UserRole.VIEWER
    )

    db.session.add(user)
    db.session.commit()

    return user


def login_user(data):
    user = User.query.filter_by(email=data["email"]).first()

    if not user or not verify_password(data["password"], user.password_hash):
        raise ValueError("Invalid credentials")

    token = generate_token(user)

    return token, user