from fastapi import FastAPI
from apps.routers import restaurants, auth

app = FastAPI(title="Restaurant Listing API")
app.include_router(auth.router)
app.include_router(restaurants.router)
