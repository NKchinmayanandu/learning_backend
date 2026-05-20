import json
from apps.redis import redis_client

def get_user_from_db(user_id:int):
    print("Fetching from db")
    return {
        "user_id":user_id,
        "name":"chinmay"
    }

def get_user(user_id:int):
    cache_key = f"user:{user_id}"
    cached_user =  redis_client.get(cache_key)
    if cached_user:
        print("from cache")
        return json.loads(cached_user)
    user = get_user_from_db(user_id)
    redis_client.set(
        cache_key,
        json.dumps(user),
        ex=60
    )
    print("saved to cache")
    return user