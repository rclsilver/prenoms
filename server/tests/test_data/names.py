from . import create_row, load_defaults
from app.models.names import Name
from sqlalchemy.orm.session import Session


def insert_name(database: Session, **kwargs):
    return create_row(database, Name, load_defaults('name.json'), kwargs)
