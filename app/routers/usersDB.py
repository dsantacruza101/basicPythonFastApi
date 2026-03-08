from fastapi import APIRouter, HTTPException, status
from app.db.client import db_client
from app.models.user import User
from app.schemas.user import user_schema, users_schema
from bson import ObjectId


router = APIRouter(
    prefix="/usersdb",
    tags=["usersdb"]
)

# Endpoint to get a list of users

@router.get("/", response_model=list[User])
async def getUsers():
    return users_schema(db_client.local.users.find())

@router.get("/{id}", response_model=User)
async def user(id: str):
    try:
        object_id = ObjectId(id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ID format"
        )
    return search_users("_id", object_id, raise_error=False)


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    if search_users("email", user.email, raise_error=False):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )
    
    user_dict = dict(user)
    del user_dict["id"]
    
    id = db_client.local.users.insert_one(user_dict).inserted_id
    
    new_user = user_schema(db_client.local.users.find_one({"_id": id}))

    return User(**new_user)

@router.put("/", status_code=status.HTTP_200_OK)
async def update_user(user: User):
    
    found = search_users("_id", ObjectId(user.id), raise_error=False)

    if not found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user_dict = dict(user)

    del user_dict["id"]
    
    db_client.local.users.update_one({"_id": ObjectId(user.id)}, {"$set": user_dict})

    return user

@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_user(id: str):
    try:
        object_id = ObjectId(id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ID format"
        )
    found = search_users("_id", object_id, raise_error=False)
    
    if not found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    db_client.local.users.delete_one({"_id": object_id})
    return {"success": "User deleted successfully"}

def search_users(key: str, value: str, raise_error: bool = True):
    user = db_client.local.users.find_one({key: value})

    if not user:
        if raise_error:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return None

    return user_schema(user)
    
