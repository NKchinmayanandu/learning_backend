from apps.redis import redis_client
import json 

def set_cache(key:str,data,expire:int=60):
    redis_client.set(
        key,
        json.dumps(data),
        ex=expire
    )

def get_cached(key:str):
    data = redis_client.get(key)
    if data is None:
        return None
    return json.loads(data)