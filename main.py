from fastapi import FastAPI,APIRouter
from apps.routers import restaurants
from apps.routers.restaurants import router
app = FastAPI()
app.include_router(restaurants.router)
