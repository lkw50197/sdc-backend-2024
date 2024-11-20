from typing import Annotated, List, Dict
from datetime import datetime, time, timedelta
from uuid import UUID

from fastapi import FastAPI, Path, Query, Body, Cookie, Form, File, UploadFile, HTTPException
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
    username: str
    email: str
    full_name: str | None

class Author(BaseModel):
    name: str
    age: int

class Book(BaseModel):
    title: str
    author: Author
    summary: str | None = None

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
    item: Item = Body(...),
    importance: int = Body(..., gt=0, description="The importance level of the item"),
):
    return {"item": item, "importance": importance}


# # New API for practicing nested models
@app.post("/offers/")
async def create_offer(offer: Offer):
    return {"offer_name": offer.name, "discount": offer.discount, "items": offer.items}

# # New API with extra schema example
@app.post("/users/")
async def create_user(user: User):
    return {"username": user.username, "email": user.email, "full_name": user.full_name}

# # New API for practicing extra data types
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

# # New API for practicing Cookie parameters
@app.get("/items/cookies/")
async def read_items_from_cookies(
    session_id: str | None = Cookie(None, description="Session ID stored in the client's cookies"),
):
    return {"session_id": session_id, "message": "This is the session ID obtained from the cookies."}

# New API for practicing Form parameters
@app.post("/items/form_data/")
async def create_item_with_form(
    name: str = Form(..., description="The name of the item"),
    description: str | None = Form(None, description="The description of the item"),
    price: float = Form(..., description="The price of the item"),
    tax: float | None = Form(None, description="The tax of the item"),
):
    return {
        "name": name,
        "description": description,
        "price": price,
        "tax": tax,
        "message": "This is an item created using form data."
    }

# Integrated API for practicing Form and File parameters
@app.post("/items/form_and_file/")
async def create_item_with_form_and_file(
    name: str = Form(..., description="The name of the item"),
    description: str | None = Form(None, description="The description of the item"),
    price: float = Form(..., description="The price of the item"),
    tax: float | None = Form(None, description="The tax of the item"),
    file: UploadFile = File(..., description="The file associated with the item"),
):
    if price < 0:
        raise HTTPException(status_code=400, detail="Price cannot be negative")
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")
    return {
        "name": name,
        "description": description,
        "price": price,
        "tax": tax,
        "filename": file.filename,
        "message": "This is an item created using form data and a file."
    }

# New API for using lists instead of sets in response model
@app.get("/books/", response_model=List[Book])
async def get_books():
    return [
        Book(title="Book 1", author=Author(name="Author 1", age=45), summary="A great book about..."),
        Book(title="Book 2", author=Author(name="Author 2", age=38), summary="An interesting journey of..."),
    ]

# New API for practicing extra models
@app.post("/books/create_with_author/")
async def create_book_with_author(book: Book):
    return {"title": book.title, "author": book.author, "summary": book.summary}

# New API for response status code
@app.post("/books/", status_code=201)
async def create_book(book: Book):
    return {"title": book.title, "author": book.author, "summary": book.summary}
