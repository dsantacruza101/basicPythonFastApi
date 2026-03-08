from datetime import datetime, timedelta, timezone

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from pwdlib import PasswordHash

from app.core.config import settings

router = APIRouter(
    prefix="/jwt-auth",
    tags=["jwt-auth"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

password_hash = PasswordHash.recommended()

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
         "password": "$argon2id$v=19$m=65536,t=3,p=4$o2hjGi5eDGN0o5sdRvQSOA$7xpIXetC6x7zR4IgcQh350nv0stKcKK/bj4KY1msAck"
    },
    "user2": {
        "username": "user2",
        "full_name": "User Two",
        "age": 25,
        "email": "user2@example.com",
        "disable": False,
        "password": "$argon2id$v=19$m=65536,t=3,p=4$maYV7HB84fD7xOlYbSCstw$qS4BBfDimje5aHUE93wZZiVF55u5JE1TfUncv90fxJs"
    },
    "user3": {
        "username": "user3",
        "full_name": "User Three",
        "age": 28,
        "email": "user3@example.com",
        "disable": True,
        "password": "$argon2id$v=19$m=65536,t=3,p=4$8bb50jDXo5cXPSO4SlyVmg$MdETnmatHA/cE34oI1JCcxTEWj9tbGcDImiSSTnQSOo"
    },
    "user4": {
        "username": "user4",
        "full_name": "User Four",
        "age": 32,
        "email": "user4@example.com",
        "disable": False,
        "password": "$argon2id$v=19$m=65536,t=3,p=4$Fv2vTJSYgsH6KFojSsP8mg$zaFDQNzCW/r9QoHIqE21EuZ2xAgpux5Lu03uNoXruHY"
    }
}

def search_user_db(username: str) -> UserDB:
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

async def auth_user(token: str = Depends(oauth2_scheme)):
    
    exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"}
            )
    
    try:
        username = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        ).get("sub")
        if username is None:
            raise exception
    except jwt.DecodeError:
        raise exception
    
    return search_user(username)

    
async def current_user(user: User = Depends(auth_user)):
    if user.disable:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return user

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = search_user_db(form_data.username)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid credentials"
            )
    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid credentials"
        )
    
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    
    access_token = {
        "sub": user.username,
        "exp": expire
    }


    return {
        "access_token": jwt.encode(
            access_token,
            settings.secret_key,
            algorithm=settings.algorithm,
        ), 
        "token_type": "bearer"
        }

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)