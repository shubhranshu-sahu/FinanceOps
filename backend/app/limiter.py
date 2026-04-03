from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Global default limits: Max 200 hits per day, 50 per hour
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
