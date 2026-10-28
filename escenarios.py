from decimal import Decimal
from cargar_csv import load_fixture
from app.domain import DomainException, Money, OrderItem
from app.specifications import discount_rate


def intentar(o, nombre, accion):
    try:
        accion()
        print(f"   {nombre}: OK -> estado {o.status.value}")
    except DomainException as e:
        print(f"   {nombre}: RECHAZADO ({type(e).__name__}: {e})")

def descuento(o):
    print(f"   evaluar_descuento: {int(discount_rate(o) * 100)}%")

def confirmar(o):
    intentar(o, "confirm", o.confirm)

def e08(o):
    intentar(o, "add_item SKU003 x2",
             lambda: o.add_item(OrderItem("SKU003", 2, Money(Decimal("120.00")))))
    print(f"   unidades después: {o.units}")

def e11(o):
    intentar(o, "confirm", o.confirm)
    intentar(o, "ship sin guía", lambda: o.ship(""))

def e12(o):
    intentar(o, "confirm #1", o.confirm)
    intentar(o, "confirm #2", o.confirm)

def e13(o):
    intentar(o, "confirm", o.confirm)
    intentar(o, "ship", lambda: o.ship("GUIA-014"))
    intentar(o, "cancel", lambda: o.cancel("cambio de opinión"))

def e14(o):
    intentar(o, "confirm", o.confirm)
    intentar(o, "ship", lambda: o.ship("GUIA-015"))
    intentar(o, "return_order", o.return_order)

def e15(o):
    intentar(o, "confirm", o.confirm)
    intentar(o, "ship", lambda: o.ship("GUIA-016"))
    intentar(o, "deliver", o.deliver)

CASOS = [
    ("E01", "O001", descuento), ("E02", "O002", descuento),
    ("E03", "O003", confirmar), ("E04", "O005", descuento),
    ("E05", "O006", descuento), ("E06", "O007", confirmar),
    ("E07", "O008", confirmar), ("E08", "O009", e08),
    ("E09", "O010", descuento), ("E10", "O011", descuento),
    ("E11", "O012", e11), ("E12", "O013", e12),
    ("E13", "O014", e13), ("E14", "O015", e14), ("E15", "O016", e15),
]

for caso, oid, operacion in CASOS:
    o = load_fixture()[oid]     
    print(f"\n{caso} | pedido {oid} | estado inicial {o.status.value} | "
          f"{o.units} uds | total {o.total.amount}")
    operacion(o)
    print(f"   estado final: {o.status.value} | "
          f"eventos: {[e.name for e in o.events] or 'ninguno'}")