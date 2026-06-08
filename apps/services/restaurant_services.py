import json
from sqlalchemy.orm import Session
from apps.models import Restaurant
from apps.utils.cache import get_cached, set_cache


def get_all_restaurants_service(
    db: Session,
    limit: int,
    offset: int,
    name: str | None
):
    cache_key = f"restaurants:{limit}:{offset}:{name}"
    cached_data = get_cached(cache_key)
    if cached_data:
        return cached_data

    query = db.query(Restaurant)
    if name:
        query = query.filter(Restaurant.name.ilike(f"%{name}%"))
    restaurants = query.offset(offset).limit(limit).all()

    restaurant_data = [
        {"id": r.id, "name": r.name, "user_id": r.user_id}
        for r in restaurants
    ]
    set_cache(cache_key, restaurant_data)
    return restaurant_data


def get_restaurant_id(id: int, db: Session):
    cache_key = f"restaurant:{id}"
    cached_data = get_cached(cache_key)
    if cached_data:
        return cached_data

    restaurant = db.query(Restaurant).filter(Restaurant.id == id).first()
    if restaurant is None:
        return None

    restaurant_data = {
        "id": restaurant.id,
        "name": restaurant.name,
        "user_id": restaurant.user_id
    }
    set_cache(cache_key, restaurant_data)
    return restaurant_data