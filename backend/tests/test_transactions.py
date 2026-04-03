import pytest

@pytest.fixture
def auth_headers(client):
    # Fetch Administrator access token
    res = client.post("/auth/login", json={"email": "prime@test.com", "password": "prime123"})
    token = res.get_json()["token"]
    return {"Authorization": f"Bearer {token}"}


def test_transaction_marshmallow_validation_barrier(client, auth_headers):
    # Intentional payload failure: Missing 'date' and 'type' keys
    response = client.post("/transactions", json={
        "amount": 500,
        "category_id": 1,
        "description": "Validation Breach Test"
    }, headers=auth_headers)
    
    # Prove Validation Firewall captures the execution request
    assert response.status_code == 400
    data = response.get_json()
    assert "Validation failed" in data["error"]
    assert "date" in data["fields"]
    assert "type" in data["fields"]


def test_transaction_creation_lifecycle(client, auth_headers):
    # Step 1: Pre-requisite category initialization
    client.post("/categories", json={"name": "Testing Equipment"}, headers=auth_headers)
    res_cats = client.get("/categories?all=true", headers=auth_headers)
    cat_id = res_cats.get_json()[-1]["id"]

    # Step 2: Perfect Data Request Insertion
    response = client.post("/transactions", json={
        "amount": 250.50,
        "type": "EXPENSE",
        "category_id": cat_id,
        "date": "2026-04-03",
        "description": "Purchased automated test servers"
    }, headers=auth_headers)

    # Prove actual insertion is flawless given pure schemas
    assert response.status_code == 201
    assert response.get_json()["message"] == "Transaction created"


def test_unauthorized_token_rejection(client):
    response = client.get("/transactions")
    # Missing header means absolute rejection from backend.
    assert response.status_code == 401
