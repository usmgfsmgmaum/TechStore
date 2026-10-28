TECHSTORE U4 - 

EQUIPO 5: 
Rodrigo Noguera Pérez Matrícula:2136238
Andrik Hasiel Pérez Limón Matrícula:2118898
Erick Antonio Paez Estrada Matrícula:2120761

Nombre del profesor: Miguel Ángel Gómez Marroquín
Actividad 4 de Componentes de Lógica de Negocio (Unidad 4: Desarrollo de Componentes de Negocio), UANL-FIME.

OBJETIVO: usar datos reproducibles para la Actividad 4 de CLN.
Descripción del Proyecto
Este proyecto implementa el núcleo de reglas de negocio para la gestión de pedidos de la tienda ficticia TechStore. Construido bajo los principios de Diseño Guiado por el Dominio (DDD), el sistema garantiza que todas las operaciones cumplan estrictamente con las políticas comerciales antes de efectuar cualquier cambio de estado.

La arquitectura se centra en el dominio y se expone a través de una API REST. Todo el almacenamiento funciona de manera volátil en memoria utilizando datos iniciales cargados desde archivos CSV, por lo que los cambios no persisten entre ejecuciones.

Características Principales
Entidades y Objetos de Valor: Validación intrínseca y encapsulamiento (ej. uso de Decimal para la clase Money evitando valores negativos).   Patrón Specification: Lógica combinable (AND, OR, NOT) para la evaluación dinámica de reglas de descuento.Máquina de Estados y Eventos: Control riguroso del ciclo de vida del pedido con registro de eventos (Domain Events) por cada transición exitosa.API REST con FastAPI: Interfaz HTTP que traduce peticiones directamente a operaciones de las entidades del dominio sin contener reglas de negocio.Pruebas Automatizadas: Suite completa con pytest para garantizar el cumplimiento de invariantes y manejo de excepciones.

Requisitos
Python 3.11 o superior.   Dependencias: fastapi, uvicorn, pytest, httpx.

CONTENIDO
 datos/clientes.csv: 12 clientes (es_vip y activo: 1=si, 0=no).
 datos/productos.csv: 12 productos (precio_mxn en formato decimal).
 datos/pedidos.csv: 16 pedidos, todos inicialmente DRAFT.
 datos/detalle_pedidos.csv: 21 lineas de articulos.
 datos/escenarios.csv: 15 situaciones de evaluacion. La columna objetivo contiene solo el tipo general de resultado, no la resolucion numerica.
 cargar_csv.py: convierte los CSV a objetos Order del proyecto de referencia.

USO
 1. Crea tu proyecto de la Actividad 4 (Python 3.11+, FastAPI y pytest).
 2. Copia cargar_csv.py y la carpeta datos/ a la raiz del proyecto, junto a app/.
 3. Ejecuta python cargar_csv.py. Si usas tu propio modelo, adapta los nombres de clases y parametros del cargador.
 4. Implementa y ejecuta los escenarios E01 a E15.
 5. Documenta para cada escenario: precondiciones, operacion, resultado, evento y prueba.
 6. No cambies las reglas de la Actividad 4 para que un caso pase.

REGLAS DIDACTICAS
 - Money no admite importes negativos; usar Decimal, no float.
 - Maximo 20 unidades por pedido (no 20 lineas).
 - Descuento 10%: cliente VIP, total >500 MXN, >=4 unidades, sin promocion.
 - Descuento 5%: total >5000 MXN, sin promocion. Prioridad 10% si ambas condiciones se cumplen.
 - Todos los pedidos empiezan DRAFT para que la maquina de estados sea ejecutada por el alumno.
 - El stock de productos es contexto de catalogo: no se implementa control de inventario en el dominio de este laboratorio.
 - El repositorio en memoria no persiste cambios entre ejecuciones.

ADVERTENCIA
 No entregamos la base SQLite en el paquete del alumno: la persistencia es opcional y no debe desplazar el objetivo de reglas y transiciones.

Instalación
Abre la terminal en la carpeta principal del proyecto.

Crea el entorno virtual:

Bash
python -m venv .venv
Activa el entorno virtual:

Windows (PowerShell): .venv\Scripts\Activate.ps1

Windows (CMD): .venv\Scripts\activate.bat

Mac / Linux: source .venv/bin/activate
Instala las librerías necesarias:

Bash
pip install -r requirements.txt
Ejecución y Scripts de Prueba
El proyecto incluye varios scripts para evaluar la lógica en consola sin necesidad de levantar la API:

Cargar base de datos en memoria:

Bash
python cargar_csv.py
Convierte los registros de clientes.csv, productos.csv y pedidos.csv en objetos del dominio.   


Ejecutar casos de evaluación:

Bash
python escenarios.py
Corre 15 situaciones de evaluación (E01 a E15) y muestra la bitácora de transiciones y eventos resultantes.   


Prueba de doble confirmación:

Bash
python prueba_O013.py
Valida que el sistema rechace confirmar un pedido que ya no se encuentra en estado DRAFT.   


Ejecutar Pruebas Unitarias:

Bash
pytest -q
Levantar la API REST:

Bash
uvicorn app.api:app --reload
Una vez iniciada, visita [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) para interactuar con el Swagger UI.

Reglas de Negocio Implementadas
Restricciones Generales
Un pedido no puede superar un máximo de 20 unidades físicas en total.   


Solo es posible agregar artículos si el pedido mantiene el estado inicial DRAFT.   


El sistema no gestiona el control de inventario; las existencias de los productos son únicamente contexto de catálogo.   

Reglas de Descuento
Descuento del 10%: Aplica si el cliente es VIP, el monto total es estrictamente mayor a $500 MXN, el pedido tiene 4 unidades o más, y no cuenta con promoción activa.   

Descuento del 5%: Aplica si el monto total es mayor a $5,000 MXN y no cuenta con promoción activa.   


Nota de prioridad: Si el carrito cumple con las condiciones de ambas reglas, el sistema asignará el descuento mayor (10%).   

Máquina de Estados
Todas las transiciones de estado evalúan condiciones específicas antes de completarse.

DRAFT ➔ confirm() ➔ CONFIRMED (Requiere artículos y un cliente activo)

CONFIRMED ➔ ship(guía) ➔ SHIPPED (Requiere un número de guía válido)

CONFIRMED ➔ cancel(motivo) ➔ CANCELLED (Requiere justificación)

SHIPPED ➔ deliver() ➔ DELIVERED

SHIPPED ➔ return_order() ➔ RETURNED

