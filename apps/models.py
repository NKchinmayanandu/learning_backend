from sqlalchemy import Column,String,Float,Integer,ForeignKey
from apps.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
class Restaurant(Base):
    __tablename__ = "restaurants"
    id = Column(Integer,primary_key=True)
    name = Column(String)
    foods = relationship("Food",back_populates="restaurant")

class Food(Base):
    __tablename__ = "foods"
    id = Column(Integer,primary_key=True)
    name = Column(String)
    price = Column(Float)
    restaurant_id = Column(Integer,ForeignKey("restaurants.id"))
    restaurant = relationship("Restaurant",back_populates="foods")
    