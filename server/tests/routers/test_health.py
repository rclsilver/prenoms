from .. import client
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch


def test_success_health(client: TestClient):
    r = client.get('/health')
    assert r.status_code == 200
    assert r.json() == { 'status': 'ok' }

def test_error_health(client: TestClient):
    session = MagicMock()
    session.side_effect = Exception
    with patch('app.database.SessionLocal', return_value=session):
        r = client.get('/health')
    assert r.status_code == 500
    assert r.json() == { 'status': 'error' }
