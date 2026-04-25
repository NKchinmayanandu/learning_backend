from fastapi.testclient import TestClient
from main import app
client = TestClient(app)
def test_login():
    response = client.post("/auth/login",json ={
        "email":"test@gmail.com",
        "password":"123"
    })

    assert response.status_code == 200