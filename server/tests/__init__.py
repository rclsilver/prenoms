from app import get_app
from app.database import SessionLocal
from app.models import Base
from datetime import datetime
from fastapi.testclient import TestClient
from pytest import fixture
from typing import Any
from uuid import UUID


def serialize_value(value: Any) -> str:
    if isinstance(value, list):
        return list(
            serialize_value(v) for v in value
        )
    elif isinstance(value, dict):
        return {
            k: serialize_value(v) for k, v in value.items()
        }
    elif isinstance(value, Base):
        return serialize_value({
            k: v for k, v in list(
                (c, getattr(value, c)) for c in list(
                    str(c).split('.')[1] for c in value.__table__.columns
                )
            )
        })
    elif isinstance(value, datetime):
        return value.strftime('%Y-%m-%dT%H:%M:%S.%f+00:00')
    elif isinstance(value, UUID):
        return str(value)
    else:
        return value


@fixture
def client():
    # Create the application
    app = get_app(
        debug=True,
        production=False,
    )

    # Return the test client
    yield TestClient(app)


@fixture
def database():
    try:
        db = SessionLocal()
        yield db
    finally:
        # Clear data
        for table_name in ['user', 'name']:
            db.execute(f'TRUNCATE TABLE "{table_name}" CASCADE;')
        db.commit()

        # Close the connection
        db.close()
