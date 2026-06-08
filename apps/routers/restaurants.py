#there are still places in which endpoints are still doing bussiness rules in delete update and patch we need to seprate it
#Duplicate DB logic appearing

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from apps.utils.deps import get_current_user
from apps.models import User
from apps.services.restaurant_services import get_all_restaurants_service
from apps.schemas import (
    RestaurantCreate,
    RestaurantResponse,
    FoodCreate,
    FoodResponse,
    UpdateRestaurant
)
from apps.models import Restaurant, Food
from apps.database import get_db
from sqlalchemy.orm import joinedload
from apps.redis import redis_client
from apps.services.restaurant_services import (
    get_all_restaurants_service,
    get_restaurant_id
)
router = APIRouter(prefix="/restaurant", tags=["restaurants"])


# 🔹 Get all restaurants (with filters)
@router.get("/", response_model=list[RestaurantResponse])
def get_all_restaurants(
    limit: int = 10,
    offset: int = 0,
    name: str | None = None,
    db: Session = Depends(get_db),  
):  
    return get_all_restaurants_service(
        limit=limit,
        offset=offset,
        name=name,
        db=db
    )
@router.get("/{id}",response_model=RestaurantResponse)
def get_restaurant_through_id(id:int,db:Session=Depends(get_db)):
    return get_restaurant_id(
        id=id,
        db=db
    )

# 🔹 Create restaurant
@router.post("/", response_model=RestaurantResponse)
def add_restaurant(data: RestaurantCreate, db: Session = Depends(get_db),
                   current_user : User = Depends(get_current_user)):
    if current_user.role != "owner":
        raise HTTPException(status_code=403, detail="Only owners can create restaurants")
    new_restaurant = Restaurant(name=data.name, user_id=current_user.id)

    db.add(new_restaurant)
    db.commit()
    db.refresh(new_restaurant)

    return new_restaurant


# 🔹 Create food
@router.post("/foods", response_model=FoodResponse)
def add_foods(data: FoodCreate, db: Session = Depends(get_db),
              current_user : User = Depends(get_current_user)):
    restaurant = db.query(Restaurant).filter(
        Restaurant.id == data.restaurant_id
    ).first()

    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    if restaurant.user_id != current_user.id:
        raise HTTPException(status_code=403,detail="Not Allowed")
    new_food = Food(
        name=data.name,
        price=data.price,
        restaurant_id=data.restaurant_id  
    )
    #there is still inconsistency in this 

    db.add(new_food)
    db.commit()
    db.refresh(new_food)
    return new_food


# 🔹 Get restaurants by food name
@router.get("/food", response_model=list[RestaurantResponse])
def get_restaurant_food(name: str, db: Session = Depends(get_db)):
    foods = db.query(Food).options(joinedload(Food.restaurant)).filter(Food.name==name).all()

    if not foods:
        raise HTTPException(status_code=404, detail="Food not found")

    return [food.restaurant for food in foods]

@router.delete("/{id}")
def delete_restaurant(id: int, db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_user)):
    restaurant = db.query(Restaurant).filter(Restaurant.id == id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="restaurant not found")
    if restaurant.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="not allowed")
    
    db.delete(restaurant)
    db.commit()
    redis_client.delete(f"restaurant:{id}")
    return {"message": "restaurant deleted"}

@router.patch("/{id}")
def update_restaurant(
    id:int,
    data:UpdateRestaurant,
    db:Session=Depends(get_db),
    current_user:User=Depends(get_current_user)
):
    restaurant = db.query(Restaurant).filter(Restaurant.id==id).first()
    if not restaurant:
        raise HTTPException(status_code=404,detail="restaurant not found")
    if restaurant.user_id != current_user.id:
        raise HTTPException(status_code=403,detail="not allowed")
    if data.name is not None:
        restaurant.name = data.name
    db.commit()
    db.refresh(restaurant)
    redis_client.delete(f"restaurant:{id}")
    return {
        "message":"the restaurant has been updated"
    }