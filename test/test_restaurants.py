import pytest
from fastapi.testclient import TestClient
from main import app
import uuid

client = TestClient(app)

@pytest.fixture
def auth_header():
    # Create a unique user
    email = f"user_{uuid.uuid4()}@example.com"
    client.post("/auth/signup", json={
        "email": email,
        "password": "password123",
        "role": "owner"
    })
    
    # Login to get token
    response = client.post("/auth/login", json={
        "email": email,
        "password": "password123"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_create_restaurant(auth_header):
    restaurant_name = f"Test Restaurant {uuid.uuid4()}"
    response = client.post(
        "/restaurant/",
        json={"name": restaurant_name},
        headers=auth_header
    )
    assert response.status_code == 200
    assert response.json()["name"] == restaurant_name
def test_delete_restaurant(auth_header):
    # Create a restaurant
    res_response = client.post(
        "/restaurant/",
        json={"name": "To Be Deleted"},
        headers=auth_header
    )
    restaurant_id = res_response.json()["id"]
    
    # Delete it
    response = client.delete(f"/restaurant/{restaurant_id}", headers=auth_header)
    assert response.status_code == 200
    assert response.json()["message"] == "restaurant deleted"

def test_get_all_restaurants(auth_header):
    response = client.get("/restaurant/", headers=auth_header)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_add_food(auth_header):
    # Create a restaurant first
    res_response = client.post(
        "/restaurant/",
        json={"name": "Food Test Restaurant"},
        headers=auth_header
    )
    restaurant_id = res_response.json()["id"]
    
    food_name = "Burger"
    response = client.post(
        "/restaurant/foods",
        json={
            "name": food_name,
            "restaurant_id": restaurant_id,
            "price": 10.5
        },
        headers=auth_header
    )
    assert response.status_code == 200
    assert response.json()["name"] == food_name

def test_get_foods(auth_header):
    response = client.get("/restaurant/foods", headers=auth_header)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_specific_restaurant_foods(auth_header):
    # Create a restaurant
    res_response = client.post(
        "/restaurant/",
        json={"name": "Specific Food Test"},
        headers=auth_header
    )
    restaurant_id = res_response.json()["id"]
    
    response = client.get(f"/restaurant/{restaurant_id}/foods", headers=auth_header)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
