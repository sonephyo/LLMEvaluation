from contextlib import asynccontextmanager
from fastapi import FastAPI
from typing import List
from pydantic import BaseModel
from app.postgresdb import books, database

class BookCreate(BaseModel):
    title: str
    author: str
    price: float

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    price: float

class Config:
  orm_mode=True
  
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    await database.connect()
    yield
    # Clean up the ML models and release the resources
    await database.disconnect()


app = FastAPI(lifespan=lifespan)

@app.post("/books/")
async def create_book(book: BookCreate):
    query = books.insert().values(title=book.title, author=book.author, price=book.price)
    last_book_id = await database.execute(query)

    query = books.select().where(books.c.id == last_book_id)
    inserted_book = await database.fetch_one(query)
    return inserted_book

@app.get("/books/", response_model=List[BookResponse])
async def get_books():
    query = books.select()
    return await database.fetch_all(query)

