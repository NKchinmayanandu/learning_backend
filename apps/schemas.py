from pydantic import BaseModel,EmailStr
from pydantic import ConfigDict
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role : str = "user"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    model_config = ConfigDict(from_attributes=True)

class FoodCreate(BaseModel):
    name : str
    restaurant_id : int
    price : float 

class FoodResponse(BaseModel):
    id : int
    name : str
    restaurant_id : int
    price : float
    model_config = ConfigDict(from_attributes=True)

class RestaurantCreate(BaseModel):
    name : str

class RestaurantResponse(BaseModel):
    id : int 
    name : str
    foods : list[FoodResponse] = []
    model_config = ConfigDict(from_attributes=True)

