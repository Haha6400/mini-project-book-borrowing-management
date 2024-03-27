import peewee as p
from enum import Enum
from . import PeeweeBaseModel

    
class Records (PeeweeBaseModel):
    borrower_id = p.BigIntegerField()
    borrow_date = p.DateField()
    return_date = p.DateField()
    total_deposit = p.BigIntegerField()
    fee = p.BigIntegerField()
    status = p.TextField()
    note = p.TextField()
    
Records.create_table()
