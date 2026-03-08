from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    id: Optional[str] = None
    name: str
    age: int
    email: str