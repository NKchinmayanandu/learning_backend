from pydantic import BaseModel

class FoodCreate(BaseModel):
    name : str
    restaurant_id : int
    price : float 

class FoodResponse(BaseModel):
    id : int
    name : str
    restaurant_id : int
    price : float
    class Config:
        from_attributes = True

class RestaurantCreate(BaseModel):
    name : str

class RestaurantResponse(BaseModel):
    id : int 
    name : str
    foods : list[FoodResponse] = []
    class Config:
        from_attributes = True
        
