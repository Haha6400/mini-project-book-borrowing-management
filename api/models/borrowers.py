import peewee as p

from . import PeeweeBaseModel


class Borrowers (PeeweeBaseModel):
    name = p.CharField()
    
Borrowers.create_table()