from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from apps.utils.deps import get_current_user
from apps.models import User, Restaurant, Food
from apps.services.restaurant_services import get_all_restaurants_service, get_restaurant_id
from apps.schemas import RestaurantCreate, RestaurantResponse, FoodCreate, FoodResponse, UpdateRestaurant
from apps.database import get_db
from apps.redis import redis_client

router = APIRouter(prefix="/restaurant", tags=["restaurants"])


@router.get("/", response_model=list[RestaurantResponse])
def get_all_restaurants(
    limit: int = 10,
    offset: int = 0,
    name: str | None = None,
    db: Session = Depends(get_db),
):
    return get_all_restaurants_service(limit=limit, offset=offset, name=name, db=db)


@router.get("/{id}", response_model=RestaurantResponse)
def get_restaurant_through_id(id: int, db: Session = Depends(get_db)):
    restaurant = get_restaurant_id(id=id, db=db)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant


@router.post("/", response_model=RestaurantResponse)
def add_restaurant(
    data: RestaurantCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "owner":
        raise HTTPException(status_code=403, detail="Only owners can create restaurants")
    new_restaurant = Restaurant(name=data.name, user_id=current_user.id)
    db.add(new_restaurant)
    db.commit()
    db.refresh(new_restaurant)
    return new_restaurant


@router.post("/foods", response_model=FoodResponse)
def add_foods(
    data: FoodCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    restaurant = db.query(Restaurant).filter(Restaurant.id == data.restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    if restaurant.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    new_food = Food(name=data.name, price=data.price, restaurant_id=data.restaurant_id)
    db.add(new_food)
    db.commit()
    db.refresh(new_food)
    return new_food


@router.get("/food", response_model=list[RestaurantResponse])
def get_restaurant_food(name: str, db: Session = Depends(get_db)):
    foods = db.query(Food).options(joinedload(Food.restaurant)).filter(Food.name == name).all()
    if not foods:
        raise HTTPException(status_code=404, detail="Food not found")
    return [food.restaurant for food in foods]


@router.delete("/{id}")
def delete_restaurant(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    restaurant = db.query(Restaurant).filter(Restaurant.id == id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    if restaurant.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    db.delete(restaurant)
    db.commit()
    redis_client.delete(f"restaurant:{id}")
    return {"message": "Restaurant deleted"}


@router.patch("/{id}")
def update_restaurant(
    id: int,
    data: UpdateRestaurant,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    restaurant = db.query(Restaurant).filter(Restaurant.id == id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    if restaurant.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    if data.name is not None:
        restaurant.name = data.name
    db.commit()
    db.refresh(restaurant)
    redis_client.delete(f"restaurant:{id}")
    return {"message": "Restaurant updated"}