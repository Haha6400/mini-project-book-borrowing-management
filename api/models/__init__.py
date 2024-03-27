from contextvars import ContextVar

from peewee import Model
from playhouse.postgres_ext import PostgresqlExtDatabase

db_context_var: ContextVar[PostgresqlExtDatabase] = ContextVar("db")

DATABASE = "mini-project-bbm"

psql_db = PostgresqlExtDatabase(
    DATABASE,
    user="postgres",
    password="postgres",
    host="db",
    port=5432,
    autorollback=True,
)


def create_db():
    """Create db connection"""
    return psql_db


def _get_db():
    if db_context_var.get(None) is None:
        db_context_var.set(create_db())
    return db_context_var.get()


class _DBProxy:
    def __getattr__(self, item):
        return getattr(_get_db(), item)

    def __setattr__(self, key, value):
        return setattr(_get_db(), key, value)


db = _DBProxy()


class PeeweeBaseModel(Model):
    class Meta:
        database = psql_db
        schema = "public"
        legacy_label_names = False
