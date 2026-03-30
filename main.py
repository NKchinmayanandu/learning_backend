from fastapi import FastAPI
from apps.routers import restaurants,auth

app = FastAPI()
app.include_router(restaurants.router)
app.include_router(auth.router)
