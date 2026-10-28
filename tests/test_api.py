import pytest
from fastapi.testclient import TestClient
from app import api
from cargar_csv import load_fixture

client = TestClient(api.app)


@pytest.fixture(autouse=True)
def datos_limpios():
    api.orders.clear()
    api.orders.update(load_fixture())


def test_404():
    assert client.post("/orders/NOPE/confirm").status_code == 404


def test_confirmar_y_doble_409():
    assert client.post("/orders/O013/confirm").status_code == 200
    assert client.post("/orders/O013/confirm").status_code == 409


def test_vacio_422():
    assert client.post("/orders/O007/confirm").status_code == 422