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

    app.state._test_engine = engine
    with TestClient(app) as client:
        yield client




def test_create_measurement_derive_weight_kg(client: TestClient):
    payload = {
        'device_mac': '11:22:33:44:55:66',
        'device_name': 'Feelfit scale',
        'weight_lb': 154.3,
        'body_fat_pct': 20.5,
        'bmi': 22.86,
    }

    response = client.post('/measurements', json=payload)
    assert response.status_code == 200
    result = response.json()
    assert result['weight_kg'] == pytest.approx(69.97, rel=1e-3)

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
    assert 'slope' in trends_data
    assert 'category' in trends_data


    trends_bmi = client.get('/trends?metric=bmi')
    assert trends_bmi.status_code == 200
    assert trends_bmi.json()['metric'] == 'bmi'
    assert 'slope' in trends_bmi.json()
    assert 'category' in trends_bmi.json()


def test_summary_no_data(client: TestClient):
    # Reset DB by creating a new session or assuming test ordering allows empty DB scenario
    # Here we use a separate endpoint with clean session by re-initializing if needed.
    # For module-scope fixture we can only assert summary returns structured response when no measurement exists
    # This is a soft compatibility check for /summary no-data behavior.
    # Delete all measurements before call
    # Use the test engine bound to the TestClient fixture to avoid touching disk DB.
    with Session(client.app.state._test_engine) as session:
        session.execute(text('DELETE FROM measurement'))
        session.commit()

    response = client.get('/summary')
    assert response.status_code == 200
    data = response.json()
    assert data['total'] == 0
    assert data['average_weight_kg'] == 0.0
    assert data['min_weight_kg'] == 0.0
    assert data['max_weight_kg'] == 0.0
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

def test_alerts_and_goals(client: TestClient):
    # create data for alerts
    client.post('/measurements', json={
        'device_mac': 'AA:AA:AA:AA:AA:AA',
        'device_name': 'Scale A',
        'weight_lb': 170.0,
        'weight_kg': 77.1,
        'body_fat_pct': 31.5,
        'bmi': 31.0,
    })
    client.post('/measurements', json={
        'device_mac': 'BB:BB:BB:BB:BB:BB',
        'device_name': 'Scale B',
        'weight_lb': 173.0,
        'weight_kg': 78.5,
        'body_fat_pct': 30.1,
        'bmi': 31.5,
    })

    # Alerts should detect high bg and rapid gain
    alerts_response = client.get('/alerts')
    assert alerts_response.status_code == 200
    alerts = alerts_response.json()['alerts']
    assert any(a['metric'] == 'body_fat_pct' for a in alerts)
    assert any(a['metric'] == 'weight_kg' for a in alerts)

    # Goals create/read
    goal_payload = {'target_weight_lb': 160.0, 'target_date': '2026-12-31', 'type': 'weight'}
    goal_res = client.post('/goals', json=goal_payload)
    assert goal_res.status_code == 201
    assert goal_res.json()['target_weight_lb'] == 160.0

    goals_list = client.get('/goals')
    assert goals_list.status_code == 200
    assert any(g['target_weight_lb'] == 160.0 for g in goals_list.json())

def test_measurements_pagination(client: TestClient):
    # Prepare dataset
    for i in range(5):
        client.post('/measurements', json={
            'device_mac': f'00:11:22:33:44:{50 + i}',
            'device_name': f'Scale {i}',
            'weight_lb': 140.0 + i,
            'weight_kg': (140.0 + i) * 0.45359237,
            'body_fat_pct': 20.0 + i,
            'bmi': 21.0 + i,
        })

    r = client.get('/measurements?offset=1&limit=2&sort=asc')
    assert r.status_code == 200
    assert len(r.json()) == 2

    # Check range filter by timestamp
    all_meas = client.get('/measurements').json()
    assert len(all_meas) >= 5

    from_ts = all_meas[1]['timestamp']
    to_ts = all_meas[3]['timestamp']
    r2 = client.get(f'/measurements?from={from_ts}&to={to_ts}&limit=10')
    assert r2.status_code == 200
    data2 = r2.json()
    assert len(data2) >= 2

def test_bulk_import_xlsx(client: TestClient, tmp_path):
    import pandas as pd
    from pathlib import Path

    data = [
        {'timestamp': '2026-03-20T08:00:00Z', 'device_mac': 'AA:AA:AA:AA:AA:AA', 'device_name': 'Scale A', 'weight_lb': 150.0, 'weight_kg': 68.0, 'body_fat_pct': 19.0, 'bmi': 22.8},
        {'timestamp': '2026-03-21T08:00:00Z', 'device_mac': 'BB:BB:BB:BB:BB:BB', 'device_name': 'Scale B', 'weight_lb': 160.0, 'weight_kg': 72.6, 'body_fat_pct': 20.5, 'bmi': 24.0},
    ]
    df = pd.DataFrame(data)
    file_path = tmp_path / 'measurements.xlsx'
    df.to_excel(file_path, index=False)

    with open(file_path, 'rb') as f:
        response = client.post('/measurements/bulk-import/xlsx', files={'file': ('measurements.xlsx', f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')})

    assert response.status_code == 201
    result = response.json()
    assert result['imported'] == 2
    assert result['skipped'] == 0

    spanish_data = [
        {'Tiempo de medición': '2026-03-22T08:00:00Z', 'Mac dispositivo': 'DD:DD:DD:DD:DD:DD', 'Nombre dispositivo': 'Scale D', 'Peso(lb)': 180.0, 'weight_kg': 81.6, 'Grasa corporal(%)': 22.1, 'bmi': 26.4},
        {'Tiempo de medición': '2026-03-23T08:00:00Z', 'Mac dispositivo': 'EE:EE:EE:EE:EE:EE', 'Nombre dispositivo': 'Scale E', 'Peso(lb)': 190.0, 'weight_kg': 86.2, 'Grasa corporal(%)': 23.5, 'bmi': 27.0},
    ]
    df2 = pd.DataFrame(spanish_data)
    file_path2 = tmp_path / 'measurements_es.xlsx'
    df2.to_excel(file_path2, index=False)

    with open(file_path2, 'rb') as f:
        response2 = client.post('/measurements/bulk-import/xlsx', files={'file': ('measurements_es.xlsx', f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')})
    assert response2.status_code == 201
    result2 = response2.json()
    assert result2['imported'] == 2
    assert result2['skipped'] == 0

    all_meas = client.get('/measurements')
    assert all_meas.status_code == 200
    assert any(m['device_mac'] == 'AA:AA:AA:AA:AA:AA' for m in all_meas.json())
