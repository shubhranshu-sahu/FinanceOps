def test_register_success(client):
    response = client.post("/auth/register", json={
        "name": "Jane User",
        "email": "jane@test.com",
        "password": "password123"
    })
    assert response.status_code == 201
    assert "User registered" in response.get_json()["message"]

def test_login_success(client):
    response = client.post("/auth/login", json={
        "email": "prime@test.com",
        "password": "prime123"
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert "token" in data
    assert data["user"]["role"] == "ADMIN"

def test_login_failure_blockade(client):
    response = client.post("/auth/login", json={
        "email": "prime@test.com",
        "password": "wrong_password_injection"
    })
    
    # Prove the system mathematically catches invalid password hashes
    assert response.status_code == 401
    assert "error" in response.get_json()
