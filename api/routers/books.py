from fastapi import APIRouter, HTTPException

from playhouse.shortcuts import model_to_dict
from peewee import fn
from models.books import Books
from pydantic import BaseModel

router = APIRouter()
    

class Book(BaseModel):
    name: str
    deposit: int
    # record_id: int 

@router.post("/book")
def create_book(payload_: Book):
    payload = payload_.dict()
    new_book = Books.create(
        name = payload["name"],
        deposit = payload["deposit"],
        record_id = 0
    )
    return model_to_dict(new_book)

@router.get("/books/{record_id}")
def get_book_list(record_id: int):
    book_list = Books.select().where(Books.record_id == record_id).execute()
    book_list = [model_to_dict(book) for book in book_list]
    return book_list

'''
@desc Get a book by id
@method GET /books/{id}
@access public 
'''
@router.get("/book/{id}")
def get_book_by_id(id: int):
    try:
        book = Books.get(Books.id == id)
        return model_to_dict(book)
    except Books.DoesNotExist:
        raise HTTPException(status_code=404, detail="Book does not exist") 
 
@router.get("/book/check/{id}")
def check_available_book(id: int):
    try:
        book = Books.get_by_id(id)
        if(book.record_id != 0): raise HTTPException(status_code=404, detail="Book is being borrowed") 
        return model_to_dict(book)
    except Books.DoesNotExist:
        raise HTTPException(status_code=404, detail="Book does not exist") 