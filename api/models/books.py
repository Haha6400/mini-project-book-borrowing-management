import peewee as p

from . import PeeweeBaseModel


class Books (PeeweeBaseModel):
    name = p.CharField()
    deposit = p.BigIntegerField()
    record_id = p.BigIntegerField()

Books.create_table()