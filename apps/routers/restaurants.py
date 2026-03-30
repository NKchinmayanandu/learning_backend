from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from apps.utils.deps import get_current_user
from apps.models import User

from apps.schemas import (
    RestaurantCreate,
    RestaurantResponse,
    FoodCreate,
    FoodResponse
)
from apps.models import Restaurant, Food
from apps.database import get_db

router = APIRouter(prefix="/restaurant", tags=["restaurants"])


# 🔹 Get all restaurants (with filters)
@router.get("/", response_model=list[RestaurantResponse])
def get_all_restaurants(
    limit: int = 10,
    offset: int = 0,
    name: str | None = None,
    db: Session = Depends(get_db),
    current_user : User = Depends(get_current_user)
):
    query = db.query(Restaurant)

    if name:
        query = query.filter(Restaurant.name.ilike(f"%{name}%"))

    restaurants = query.offset(offset).limit(limit).all()
    return restaurants


# 🔹 Get all foods
@router.get("/foods", response_model=list[FoodResponse])
def get_all_food(db: Session = Depends(get_db),
                 current_user : User = Depends(get_current_user)):
    return db.query(Food).all()


# 🔹 Get foods of a specific restaurant
@router.get("/{id}/foods", response_model=list[FoodResponse])
def get_food_restaurant(id: int, db: Session = Depends(get_db)
                        ,current_user : User = Depends(get_current_user)):
    restaurant = db.query(Restaurant).filter(Restaurant.id == id).first()

    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    return restaurant.foods


# 🔹 Create restaurant
@router.post("/", response_model=RestaurantResponse)
def add_restaurant(data: RestaurantCreate, db: Session = Depends(get_db),
                   current_user : User = Depends(get_current_user)):
    new_restaurant = Restaurant(name=data.name)

    db.add(new_restaurant)
    db.commit()
    db.refresh(new_restaurant)

    return new_restaurant


# 🔹 Create food
@router.post("/foods", response_model=FoodResponse)
def add_foods(data: FoodCreate, db: Session = Depends(get_db),
              current_user : User = Depends(get_current_user)):
    # check if restaurant exists
    restaurant = db.query(Restaurant).filter(
        Restaurant.id == data.restaurant_id
    ).first()

    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    new_food = Food(
        name=data.name,
        price=data.price,
        restaurant_id=data.restaurant_id  
    )

    db.add(new_food)
    db.commit()
    db.refresh(new_food)

    return new_food


# 🔹 Get restaurants by food name
@router.get("/food", response_model=list[RestaurantResponse])
def get_restaurant_food(name: str, db: Session = Depends(get_db),
                        current_user : User = Depends(get_current_user)):
    foods = db.query(Food).filter(Food.name == name).all()

    if not foods:
        raise HTTPException(status_code=404, detail="Food not found")

    return [food.restaurant for food in foods]
