from sqlalchemy import Column,String,Float,Integer,ForeignKey
from apps.database import Base
from sqlalchemy.orm import relationship
class Restaurant(Base):
    __tablename__ = "restaurants"
    id = Column(Integer,primary_key=True)
    name = Column(String)
    foods = relationship("food",back_populates="restaurant")

class Food(Base):
    __tablename__ = "foods"
    id = Column(Integer,primary_key=True)
    name = Column(String)
    price = Column(Float)
    restaurant_id = Column(Integer,ForeignKey(Restaurant.id))
    restaurant = relationship("restaurant",back_populates="food")
