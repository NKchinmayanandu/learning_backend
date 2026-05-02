import uuid

def test_signup(client):
    email = f"test_{uuid.uuid4()}@example.com"
    response = client.post("/auth/signup", json={
        "email": email,
        "password": "123",
        "role": "user"
    })
    assert response.status_code == 200

def test_login(client):
    # First signup a user to ensure they exist
    email = f"login_{uuid.uuid4()}@example.com"
    client.post("/auth/signup", json={
        "email": email,
        "password": "123",
        "role": "user"
    })
    
    response = client.post("/auth/login", json={
        "email": email,
        "password": "123"
    })

    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid_credentials(client):
    response = client.post("/auth/login", json={
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "invalid credentials"
