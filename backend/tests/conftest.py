import pytest
from app import create_app
from app.models import db
from app.models.user import User
from app.models.enums import UserRole
from app.utils.password_utils import hash_password

@pytest.fixture
def app():
    # Execute App Factory using specialized Mock Environment parameters
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "RATELIMIT_ENABLED": False,  # Turn off DDoS protections so tests execute at logic speed
        "SECRET_KEY": "automation-test-key-0000000"
    })

    with app.app_context():
        db.create_all()
        # Seed foundational database architecture for Testing Environment
        admin_vector = User(
            name="Automated Prime", 
            email="prime@test.com", 
            password_hash=hash_password("prime123"), 
            role=UserRole.ADMIN
        )
        db.session.add(admin_vector)
        db.session.commit()
        
        yield app
        
        # Immediate demolition of database variables post-testing execution to secure memory
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
