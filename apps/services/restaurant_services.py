import json
from apps.redis import redis_client
from sqlalchemy.orm import Session

from apps.models import Restaurant

def get_all_restaurants_service(
        db:Session,
        limit:int,
        offset:int,
        name:str|None
):
    cache_key = f"restaurants:{limit}:{offset}:{name}"
    cached_restaurants = redis_client.get(cache_key)
    if cached_restaurants:
        print("from cache")
        return json.loads(cached_restaurants)
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

    redis_client.set(
        cache_key,
        json.dumps(restaurant_data),
        ex=60
    )
    return restaurant_data
def get_restaurant_id(id:int,db:Session):
    cache_key = f"restaurant:{id}"
    cached_restaurants = redis_client.get(cache_key)
    if cached_restaurants:
        print("from cache")
        return json.loads(cached_restaurants)
    print("from db")
    restaurant = db.query(Restaurant).filter(Restaurant.id == id).first()
    if not restaurant:
        return None
    restaurant_data = {
        "id" : restaurant.id,
        "name" : restaurant.name,
        "user_id" : restaurant.user_id
    }
    redis_client.set(
        cache_key,
        json.dumps(restaurant_data),
        ex=60
    )

    return restaurant_data
