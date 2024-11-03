from typing import Annotated, List, Dict
from datetime import datetime, time, timedelta
from uuid import UUID

from fastapi import FastAPI, Path, Query, Body, Cookie
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

class Offer(BaseModel):
    name: str
    discount: float
    items: List[Item]

class User(BaseModel):
    username: str = Field(..., examples={"example": "user123"})
    email: str = Field(..., examples={"example": "user123@example.com"})
    full_name: str | None = Field(None, examples={"example": "John Doe"})

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(
    item_id: int = Path(..., ge=1, le=1000, description="The ID of the item (1-1000)"),
    q: str | None = Query(None, min_length=3, max_length=50, description="Search query string"),
    sort_order: str = Query("asc", pattern="^(asc|desc)$", description="Sort order: 'asc' or 'desc'"),
):
    item = {
        "item_id": item_id,
        "description": f"This is a sample item that matches the query {q}" if q else "This is a sample item.",
        "sort_order": sort_order,
    }
    return item

@app.put("/items/{item_id}")
async def update_item(
    item_id: int = Path(..., ge=1, le=1000, description="The ID of the item (1-1000)"),
    item: Item = None,
    q: str | None = Query(None, min_length=3, max_length=50, description="Search query string"),
):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result

# New API for multiple query parameters handling
@app.post("/items/filter/")
async def filter_items(
    price_min: float = Query(0, description="Minimum price of the item"),
    price_max: float = Query(10000, description="Maximum price of the item"),
    tax_included: bool = Query(True, description="Whether the price includes tax or not"),
    tags: List[str] = Query([], description="Tags to filter items"),
):
    filtered_items = {
        "price_range": [price_min, price_max],
        "tax_included": tax_included,
        "tags": tags,
        "message": "This is a filtered list of items based on the provided criteria.",
    }
    return filtered_items

# New API for practicing usage of Body fields
@app.post("/items/create_with_fields/")
async def create_item_with_fields(
    item: Item = Body(
        ..., 
        examples={
            "example": {
                "name": "Sample Item",
                "description": "A sample item for demonstration purposes",
                "price": 99.99,
                "tax": 9.99,
            }
        },
    ),
    importance: int = Body(..., gt=0, description="The importance level of the item"),
):
    return {"item": item, "importance": importance}

# New API for practicing nested models
@app.post("/offers/")
async def create_offer(offer: Offer):
    return {"offer_name": offer.name, "discount": offer.discount, "items": offer.items}

# New API with extra schema example
@app.post("/users/")
async def create_user(user: User):
    return {"username": user.username, "email": user.email, "full_name": user.full_name}

# New API for practicing extra data types
@app.post("/items/extra_data_types/")
async def create_item_with_extra_data(
    start_time: datetime = Body(..., description="The start time of the item availability"),
    end_time: time = Body(..., description="The end time of the item availability"),
    repeat_every: timedelta = Body(..., description="Interval at which the item should be repeated"),
    process_id: UUID = Body(..., description="Unique identifier for the process"),
):
    return {
        "start_time": start_time,
        "end_time": end_time,
        "repeat_every": repeat_every,
        "process_id": process_id,
        "message": "This is an item with extra data types."
    }

# New API for practicing Cookie parameters
@app.get("/items/cookies/")
async def read_items_from_cookies(
    session_id: str | None = Cookie(None, description="Session ID stored in the client's cookies"),
):
    return {"session_id": session_id, "message": "This is the session ID obtained from the cookies."}

