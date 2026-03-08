from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers import basic_auth_users, jwt_auth_user, products, users, usersDB

app = FastAPI()

app.include_router(products.router)
app.include_router(users.router)
app.include_router(usersDB.router)
app.include_router(jwt_auth_user.router)
app.include_router(basic_auth_users.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")   
async def root():
    return {"message": "Hello World"}

@app.get("/url")
async def url():
    return {"url": "http://example.com"}