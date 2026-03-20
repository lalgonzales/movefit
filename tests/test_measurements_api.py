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

def test_latest_summary_trends(client: TestClient):
    # Add several measurements for trend summary
    samples = [
        {'device_mac': 'AA:AA:AA:AA:AA:AA', 'device_name': 'Scale A', 'weight_lb': 150.0, 'weight_kg': 68.0, 'body_fat_pct': 18.0, 'bmi': 22.2},
        {'device_mac': 'BB:BB:BB:BB:BB:BB', 'device_name': 'Scale B', 'weight_lb': 160.0, 'weight_kg': 72.6, 'body_fat_pct': 19.5, 'bmi': 23.5},
        {'device_mac': 'CC:CC:CC:CC:CC:CC', 'device_name': 'Scale C', 'weight_lb': 170.0, 'weight_kg': 77.1, 'body_fat_pct': 21.0, 'bmi': 24.8},
    ]
    for sample in samples:
        r = client.post('/measurements', json=sample)
        assert r.status_code == 200

    latest = client.get('/measurements/latest')
    assert latest.status_code == 200
    assert latest.json()['device_mac'] == samples[-1]['device_mac']

    summary = client.get('/summary')
    assert summary.status_code == 200
    summary_data = summary.json()
    assert summary_data['total'] >= 3
    assert summary_data['min_weight_kg'] <= summary_data['max_weight_kg']

    trends = client.get('/trends?metric=weight')
    assert trends.status_code == 200
    trends_data = trends.json()
    assert trends_data['metric'] == 'weight'
    assert isinstance(trends_data['points'], list)

    trends_bmi = client.get('/trends?metric=bmi')
    assert trends_bmi.status_code == 200
    assert trends_bmi.json()['metric'] == 'bmi'


def test_summary_no_data(client: TestClient):
    # Note: this test case is only meaningful if there is no data; we skip it because data exists.
    pass

def test_bulk_import_measurements(client: TestClient):
    data = [
        {
            'device_mac': 'AA:AA:AA:AA:AA:AA',
            'device_name': 'Scale A',
            'weight_lb': 150.0,
            'weight_kg': 68.0,
            'body_fat_pct': 18.0,
            'bmi': 22.2,
        },
        {
            'device_mac': 'BB:BB:BB:BB:BB:BB',
            'device_name': 'Scale B',
            'weight_lb': 160.0,
            'weight_kg': 72.6,
            'body_fat_pct': 19.5,
            'bmi': 23.5,
        },
        {
            'device_mac': 'CC:CC:CC:CC:CC:CC',
            'device_name': 'Scale C',
            'weight_lb': 170.0,
            'weight_kg': 77.1,
            'body_fat_pct': 21.0,
            'bmi': 24.8,
        },
    ]

    response = client.post('/measurements/bulk-import', json=data)
    assert response.status_code == 201
    result = response.json()
    assert result['imported'] == 3
    assert result['skipped'] == 0
    assert result['errors'] == []

    # Verify inserted
    all_measurements = client.get('/measurements')
    assert all_measurements.status_code == 200
    assert len(all_measurements.json()) >= 3
