from pydantic import BaseModel,EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True

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
        
