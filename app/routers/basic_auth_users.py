from fastapi import Depends, HTTPException, APIRouter, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/basic-auth",
    tags=["basic-auth"]
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username: str
    full_name: str
    age: int
    email: str
    disable: bool

class UserDB(User):
    password: str


users_db = {
    "user1": {
        "username": "user1", 
        "full_name": "User One",
         "age": 30, 
         "email": "user1@example.com",
         "disable": False,
         "password": "password1"
    },
    "user2": {
        "username": "user2",
        "full_name": "User Two",
        "age": 25,
        "email": "user2@example.com",
        "disable": False,
        "password": "password2"
    },
    "user3": {
        "username": "user3",
        "full_name": "User Three",
        "age": 28,
        "email": "user3@example.com",
        "disable": True,
        "password": "password3"
    },
    "user4": {
        "username": "user4",
        "full_name": "User Four",
        "age": 32,
        "email": "user4@example.com",
        "disable": False,
        "password": "password4"
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    
async def current_user(token: str = Depends(oauth2_scheme)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    if user.disable:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return user

    
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = search_user_db(form_data.username)
    if not user or user.password != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid credentials"
            )
    return {
        "access_token": user.username, 
        "token_type": "bearer"
        }

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user