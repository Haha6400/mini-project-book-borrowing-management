from fastapi import APIRouter, HTTPException

from playhouse.shortcuts import model_to_dict
from peewee import fn
from models.borrowers import Borrowers
from pydantic import BaseModel

router = APIRouter()
    

class Borrower(BaseModel):
    name: str

'''
@desc Create a new borrower
@method POST /borrower
@access public 
'''
@router.post("/borrower")
def create_borrower(payload_: Borrower):
    payload = payload_.dict()
    newBorrower = Borrowers.create(**payload)
    return newBorrower.id


'''
@desc Get borrower by id
@method GET /borrower/{id}
@access public 
'''
@router.get("/borrower/{id}")
def get_borrower_by_id(id: int):
    try:
        borrower = Borrowers.get(Borrowers.id == id)
        return model_to_dict(borrower)
    except Borrowers.DoesNotExist:
        raise HTTPException(status_code=404, detail="Borrower does not exist") 