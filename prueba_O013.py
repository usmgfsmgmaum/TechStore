from cargar_csv import load_fixture
from app.domain import InvalidOrderTransition

o = load_fixture()["O013"]
print("Inicio:", o.status.value, len(o.events))

o.confirm()
print("Primera confirmación:", o.status.value, [e.name for e in o.events])

try:
    o.confirm()
except InvalidOrderTransition as e:
    print("Segunda confirmación RECHAZADA:", e)

print("Final:", o.status.value, len(o.events), "evento(s)")