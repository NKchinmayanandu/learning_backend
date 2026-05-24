import json
from apps.redis import redis_client
from sqlalchemy.orm import Session

from apps.models import Restaurant
from apps.utils.cache import get_cached,set_cache
def get_all_restaurants_service(
        db:Session,
        limit:int,
        offset:int,
        name:str|None
):
    cache_key = f"restaurants:{limit}:{offset}:{name}"
    #get cached by the cache file
    cached_data = get_cached(cache_key)
    if cached_data:
        print("from cache")
        return cached_data
    
    print("from db")
    query = db.query(Restaurant)
    if name:
        query = query.filter(Restaurant.name.ilike(f"%{name}%"))
    restaurants = query.offset(offset).limit(limit).all()

    restaurant_data = []
    for restaurant in restaurants:
        restaurant_data.append({
            "id":restaurant.id,
            "name":restaurant.name,
            "user_id":restaurant.user_id
        })
    #set cache key for to get cached by the redis for the next time
    set_cache(cache_key,restaurant_data)

    return restaurant_data
def get_restaurant_id(id:int,db:Session):
    cache_key = f"restaurant:{id}"
    cached_data = get_cached(cache_key)
    if cached_data:
        print("from cache")
        return cached_data
    print("from db")
    restaurant = db.query(Restaurant).filter(Restaurant.id == id).first()
    if not restaurant:
        return None
    restaurant_data = {
        "id" : restaurant.id,
        "name" : restaurant.name,
        "user_id" : restaurant.user_id
    }
    set_cache(cache_key,restaurant_data)

    return restaurant_data
