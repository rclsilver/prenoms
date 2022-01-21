from .test_data.names import insert_name
from .test_data.users import insert_user
from pytest import fixture
from sqlalchemy.orm.session import Session


@fixture
def name(database: Session):
    yield insert_name(database)

@fixture
def user(database: Session):
    yield insert_user(database)
