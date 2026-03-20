import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from movefit import app, db, models


@pytest.fixture(scope='module')
def client() -> TestClient:
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    def get_session_override():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[db.get_session] = get_session_override

    with TestClient(app) as client:
        yield client


def test_create_and_read_measurement(client: TestClient):
    payload = {
        'device_mac': '00:11:22:33:44:55',
        'device_name': 'Feelfit scale',
        'weight_lb': 154.3,
        'weight_kg': 69.97,
        'body_fat_pct': 20.5,
        'bmi': 22.86,
    }

    response = client.post('/measurements', json=payload)
    assert response.status_code == 200
    result = response.json()
    assert result['device_mac'] == payload['device_mac']
    assert result['weight_kg'] == pytest.approx(payload['weight_kg'], rel=1e-3)

    measurement_id = result['id']
    get_response = client.get(f'/measurements/{measurement_id}')
    assert get_response.status_code == 200
    assert get_response.json()['id'] == measurement_id


def test_read_measurements_list(client: TestClient):
    response = client.get('/measurements')
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_measurement_not_found(client: TestClient):
    response = client.get('/measurements/999999')
    assert response.status_code == 404
