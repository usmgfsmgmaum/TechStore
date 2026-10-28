import pytest
from decimal import Decimal
from app.domain import (Money, OrderItem, InvalidOrderData,
                        InvalidOrderTransition, OrderItemLimitExceeded)
from app.specifications import discount_rate
from cargar_csv import load_fixture


def test_money_negativo():
    with pytest.raises(InvalidOrderData):
        Money(Decimal("-1"))


def test_pedido_o001_inicia_draft():
    orders = load_fixture()
    assert orders["O001"].status.value == "DRAFT"
    assert orders["O001"].units == 4
    assert orders["O001"].total.amount == Decimal("2100.00")


def test_21_unidades():
    o = load_fixture()["O009"]
    with pytest.raises(OrderItemLimitExceeded):
        o.add_item(OrderItem("SKU003", 2, Money(Decimal("120.00"))))
    assert o.units == 19


def test_cliente_inactivo():
    with pytest.raises(InvalidOrderData):
        load_fixture()["O003"].confirm()


def test_pedido_vacio():
    with pytest.raises(InvalidOrderData):
        load_fixture()["O007"].confirm()


def test_descuento_vip():
    assert discount_rate(load_fixture()["O001"]) == Decimal("0.10")


def test_promocion_activa():
    assert discount_rate(load_fixture()["O005"]) == 0


def test_envio_sin_guia():
    o = load_fixture()["O012"]
    o.confirm()
    with pytest.raises(InvalidOrderData):
        o.ship("")
    assert o.status.value == "CONFIRMED"


def test_confirmacion_doble():
    o = load_fixture()["O013"]
    o.confirm()
    with pytest.raises(InvalidOrderTransition):
        o.confirm()
    assert len(o.events) == 1


def test_cancelar_desde_shipped():
    o = load_fixture()["O014"]
    o.confirm()
    o.ship("G-1")
    with pytest.raises(InvalidOrderTransition):
        o.cancel("x")