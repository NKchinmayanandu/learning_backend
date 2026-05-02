from sqlalchemy import Column,String,Float,Integer,ForeignKey
from apps.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String, default="user")
    restaurants = relationship("Restaurant", back_populates="owner")
  

class Restaurant(Base):
    __tablename__ = "restaurants"
    
    id = Column(Integer, primary_key=True)
    name = Column(String,nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="restaurants")
    foods = relationship("Food", back_populates="restaurant")

class Food(Base):
    __tablename__ = "foods"
    id = Column(Integer,primary_key=True)
    name = Column(String,nullable=False)
    price = Column(Float,nullable=False)
    description = Column(String)
    restaurant_id = Column(Integer,ForeignKey("restaurants.id"))
    restaurant = relationship("Restaurant",back_populates="foods")

    