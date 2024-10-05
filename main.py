from fastapi import FastAPI, Path, Query
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(
    item_id: int = Path(..., ge=1, le=1000, description="The ID of the item (1-1000)"),
    q: str | None = Query(None, min_length=3, max_length=50, description="Search query string"),
    sort_order: str = Query("asc", pattern="^(asc|desc)$", description="Sort order: 'asc' or 'desc'")
):
    item = {
        "item_id": item_id,
        "description": f"This is a sample item that matches the query {q}" if q else "This is a sample item.",
        "sort_order": sort_order
    }
    return item

@app.put("/items/{item_id}")
async def update_item(
    item_id: int = Path(..., ge=1, le=1000, description="The ID of the item (1-1000)"),
    item: Item = None,
    q: str | None = Query(None, min_length=3, max_length=50, description="Search query string")
):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result
