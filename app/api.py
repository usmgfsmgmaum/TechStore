from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from cargar_csv import load_fixture
from app.domain import (InvalidOrderTransition, InvalidOrderData,
                        OrderItemLimitExceeded)

app = FastAPI(title="TechStore U4")
orders = load_fixture()


class ShipIn(BaseModel):
    tracking_number: str = ""


class CancelIn(BaseModel):
    reason: str = ""


def buscar(order_id):
    order = orders.get(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="No existe")
    return order


def ejecutar(fn, *args):
    try:
        fn(*args)
    except (InvalidOrderTransition, OrderItemLimitExceeded) as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    except InvalidOrderData as exc:
        raise HTTPException(status_code=422, detail=str(exc))


def vista(order):
    return {"id": order.id, "status": order.status.value,
            "units": order.units, "total": str(order.total.amount),
            "events": [e.name for e in order.events]}


@app.get("/orders/{order_id}")
def get_order(order_id: str):
    return vista(buscar(order_id))


@app.post("/orders/{order_id}/confirm")
def confirm_order(order_id: str):
    order = buscar(order_id)
    ejecutar(order.confirm)
    return vista(order)


@app.post("/orders/{order_id}/ship")
def ship_order(order_id: str, data: ShipIn):
    order = buscar(order_id)
    ejecutar(order.ship, data.tracking_number)
    return vista(order)


@app.post("/orders/{order_id}/cancel")
def cancel_order(order_id: str, data: CancelIn):
    order = buscar(order_id)
    ejecutar(order.cancel, data.reason)
    return vista(order)