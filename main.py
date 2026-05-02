from apps.routers import restaurants,auth
from fastapi import FastAPI
from apps.database import Base,engine
app = FastAPI()
app.include_router(restaurants.router)
app.include_router(auth.router)

