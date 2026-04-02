import jwt
import datetime
import os

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey") 


def generate_token(user):
    payload = {
        "user_id": user.id,
        "role": user.role.value,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None