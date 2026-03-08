from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# Endpoint to get a list of users

class User(BaseModel):
    id: int
    name: str
    age: int
    email: str

users_list = [User(id=1, name="daniel", age=30, email="daniel@example.com"),
         User(id=2, name="alice", age=25, email="alice@example.com"),
         User(id=3, name="bob", age=28, email="bob@example.com"),
         User(id=4, name="charlie", age=22, email="charlie@example.com")
        ]

@router.get("/")
async def getUsers():
    return users_list

@router.get("/{id}")
async def user(id: int):
    return search_users(id)
    

@router.get("/userquery/")
async def user(id: int):
    return search_users(id)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    if search_users(user.id, raise_error=False):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )
    users_list.append(user)
    return user

@router.put("/", status_code=status.HTTP_200_OK)
async def update_user(user: User):
    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
            break

    if not found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_user(id: int):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
            break
    if not found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return {"success": "User deleted successfully"}

def search_users(id: int, raise_error: bool = True):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except IndexError:
        if raise_error:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return None
    
