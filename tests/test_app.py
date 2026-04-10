import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

import pytest
from app import app as flask_app

@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c

def test_home_returns_200(client):
    res = client.get("/")
    assert res.status_code == 200

def test_home_contains_hospital(client):
    res = client.get("/")
    assert b"Hospital" in res.data

def test_health_endpoint(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert b"ok" in res.data

def test_patient_detail_valid(client):
    res = client.get("/patient/P001")
    assert res.status_code == 200
    assert b"Ramesh Kumar" in res.data

def test_patient_detail_invalid(client):
    res = client.get("/patient/P999")
    assert res.status_code == 404

def test_doctors_page(client):
    res = client.get("/doctors")
    assert res.status_code == 200
    assert b"Cardiology" in res.data

def test_search(client):
    res = client.get("/search?q=suresh")
    assert res.status_code == 200
    assert b"Suresh" in res.data

def test_critical_patients_shown(client):
    res = client.get("/")
    assert b"Critical" in res.data
