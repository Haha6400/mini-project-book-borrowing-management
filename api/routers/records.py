from fastapi import APIRouter, Request, HTTPException

from playhouse.shortcuts import model_to_dict
from peewee import fn

from models.records import Records
from models.books import Books
from models.borrowers import Borrowers
from datetime import datetime, date
from pydantic import BaseModel
import psycopg2


router = APIRouter()
    

class Record(BaseModel):
    borrower_id: int
    borrow_date: date
    return_date: date
    total_deposit: int
    fee: int = 0
    status: str = "BORROWING"
    note: str = ""
    
class RecordBookCreatePayload(BaseModel):
    borrower_id: int
    borrow_date: date
    return_date: date
    total_deposit: int
    fee: int = 0
    status: str = "BORROWING"
    note: str = ""
    book_list: list[dict]

'''
@desc Get all records
@method GET /records
@access public 
'''
@router.get("/records")
def get_all_records():
    records = get_all_records_with_borrower_name()
    if not records:
        raise HTTPException(status_code=404, detail="Records not found")
    return records


def get_all_records_with_borrower_name():
    try:
        connection = psycopg2.connect(user="postgres",
                                        password="postgres",
                                        host="db",
                                        port=5432,
                                      database="mini-project-bbm")
        cursor = connection.cursor()
        query = """
            SELECT records.*, borrowers.name
            FROM records
            INNER JOIN borrowers ON records.borrower_id = borrowers.id
        """
        cursor.execute(query)
        records = cursor.fetchall()
        cursor.close()
        connection.close()
        records_with_attributes = []
        for record in records:
            record_dict = {
                "id": record[0], 
                "borrower_id": record[1],
                "borrow_date": record[2],
                "return_date": record[3],
                "total_deposit": record[4],
                "fee": record[5],
                "status": record[6],
                "note": record[7],
                "borrowerName": record[-1]
            }
            records_with_attributes.append(record_dict)
        
        return records_with_attributes
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)

'''
@desc Get a record by id
@method GET /record/{id}
@access public 
'''
@router.get("/record/{id}")
def get_record_by_id(id: int):
    try:
        record = Records.get(Records.id == id)
        book_list = Books.select().where(Books.record_id == id).execute()
        book_list = [model_to_dict(book) for book in book_list]
        return model_to_dict(record), book_list
    except Records.DoesNotExist:
        return "Record does not exist"
    

'''
@desc Create a new record
@method POST /record
@access public 
'''
@router.post("/record")
def create_record(payload_: RecordBookCreatePayload):
    payload = payload_.dict()
    new_record = Records.create(
            borrower_id = payload["borrower_id"],
            borrow_date= payload["borrow_date"],
            return_date= payload["return_date"],
            total_deposit= payload["total_deposit"],
            fee = 0,
            status = "BORROWING",
            note = payload["note"],
    )
    book_ids = [book["id"] for book in payload["book_list"]]
    Books.update(record_id=new_record.id).where(Books.id.in_(book_ids)).execute()
    return model_to_dict(new_record)

'''
@desc Update a new record
@method PATCH /record/{id}
@access public 
'''
@router.patch("/record/{id}")
def update_record(id: int, payload_: RecordBookCreatePayload):
    payload = payload_.dict()
    try:
        Records.update(
            borrower_id=payload["borrower_id"],
            borrow_date=payload["borrow_date"],
            return_date=payload["return_date"],
            total_deposit=payload["total_deposit"],
            fee=payload["fee"],
            status=payload["status"],
            note=payload["note"]
        ).where(Records.id == id).execute()
        if(payload["status"] == "RETURNED"): id = 0
        for book in payload["book_list"]:
            # if (payload["status"] == "RETURNED"): id = ''
            (Books
                .update(record_id= id)
                .where(Books.id == book["id"])
                .execute())
        return model_to_dict(Records.get_by_id(id))
    except Records.DoesNotExist:
        raise HTTPException(status_code=404, detail="Record does not exist") 

'''
@desc Delete a record
@method DELETE /record/{id}
@access public 
'''
@router.delete("/record/{id}")
def delete_record(id: int):
    record = Records.get_by_id(id)
    Books.update(record_id= 0).where(Books.record_id == id).execute()
    record.delete_instance()
