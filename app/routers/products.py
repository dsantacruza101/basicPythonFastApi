from fastapi import APIRouter

router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={404: {"description": "Not found"}}
)

products_list = ["Product 1", "Product 2", "Product 3"]

@router.get("/")
async def get_products():
    return products_list

@router.get("/{id}")
async def get_product(id: int):
    return products_list[id]