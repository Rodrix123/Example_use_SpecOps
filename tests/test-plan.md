# Plan de pruebas — Gestor de préstamos de libros

| Campo | Valor |
|---|---|
| Versión | 0.1 (borrador, pendiente de aprobación del equipo) |
| Fase | 6. Planificación de pruebas (Actividad 6) |
| Fecha | 2026-11-24 |
| Fuentes | specs [`catalogo`](../openspec/changes/gestor-prestamos-v1/specs/catalogo/spec.md), [`prestamos`](../openspec/changes/gestor-prestamos-v1/specs/prestamos/spec.md) y [`datos`](../openspec/changes/gestor-prestamos-v1/specs/datos/spec.md); [`tasks.md`](../openspec/changes/gestor-prestamos-v1/tasks.md); [`design.md`](../openspec/changes/gestor-prestamos-v1/design.md) |
| Alcance | Define qué se prueba, con qué datos y qué se espera. No contiene código de pruebas: se implementa en la fase 7, una tarea a la vez. |

## 1. Alcance y reglas del plan

- **105 pruebas (TEST-001 a TEST-105) para las 22 tareas (TASK-001 a TASK-022)**, definidas antes de implementar cada tarea (CLAUDE.md §5, regla 8).
- Cada uno de los 20 Scenarios de las tres specs tiene al menos una prueba de aceptación (sección 6.2 de este plan).
- Cada criterio de aceptación de las tareas tiene al menos una prueba (sección 6.3 de este plan).
- Las pruebas de TASK-001 a TASK-006, TASK-012 y TASK-013 verifican criterios de tarea y decisiones del diseño; no corresponden a un Scenario y citan el requisito que la tarea declara.
- Toda prueba que depende de la fecha usa una fecha fija inyectada (sección 2); ninguna lee el reloj del sistema.
- Fuera del plan, por no estar en las specs: CU-002 flujo 1b (libros disponibles; design «Non-Goals»), lo excluido en intent §6 y product-spec §4, el control de concurrencia y RS-04 (solo delimita el alcance).

## 2. Datos de prueba comunes

| Dato | Valor |
|---|---|
| Fecha simulada («hoy») | 01/12/2026 (`2026-12-01`), entregada por el proveedor de fecha inyectado (design Decisión 6). Única excepción: TEST-102 (S-2). |
| Fechas de referencia | Ayer 30/11/2026 · Pasada 10/11/2026 · Futura 15/12/2026 |
| L-001 | «Cien años de soledad» / «Gabriel García Márquez» |
| L-002 | «El Aleph» / «Jorge Luis Borges» |
| L-003 | «Rayuela» / «Julio Cortázar» |
| L-004, L-005 | Libros adicionales, solo en TEST-055 y TEST-091; título y autor sin relevancia |
| Estudiantes | «Ana Pérez», «Luis Gómez» |
| Identificador inexistente | «L-099» |

## 3. Tipos de prueba y convenciones

| Tipo | Qué verifica | Cantidad |
|---|---|---|
| aceptación | Un Scenario de las specs (WHEN/THEN), en la capa donde su resultado es observable: consola para lo que ve el bibliotecario; servicio para estado interno (RN-04); archivo real para persistencia. Incluye la ejecución manual de RNF-02. | 24 |
| unitaria | Una regla o función aislada, camino válido. | 37 |
| fallo | Camino de rechazo o error: entrada inválida, archivo corrupto, escritura que falla. | 31 |
| integración | Varias capas reales juntas (servicio + almacén con archivo temporal, o menú completo). | 6 |
| manual | Verificación hecha por una persona o con comandos del entorno (Git, README). | 7 |

Convenciones de lectura:

- **Entradas de consola:** se listan en el orden en que se leen, entre «». «» es una línea vacía. La opción del menú cuenta como una entrada; «consume exactamente N entradas» se refiere a las que la operación lee después de elegirla. La numeración del menú es un supuesto (S-1).
- **Pruebas de servicio:** almacén simulado en memoria con contador de llamadas a `guardar` y proveedor de fecha fijo (design Decisiones 1 y 6).
- **Pruebas de consola:** servicio con almacén simulado, con entrada y salida inyectadas (TASK-013).
- **Pruebas de integración:** archivo en una carpeta temporal; nunca `ops/biblioteca.json`.
- **«Sin cambios»:** libros y préstamos iguales a los iniciales; en pruebas de servicio, además, el contador de `guardar` no aumenta (RNF-03).
- **«Motivo»:** el rechazo muestra o expone un motivo no vacío que corresponde a la causa indicada.
- El comando de pruebas lo fija TASK-001; las pruebas automatizadas se ejecutan con él.

## 4. Pruebas por tarea

### TASK-001 — Crear el paquete `gestor_prestamos` y fijar el comando de pruebas

Archivo: `tests/test_humo.py`; verificación manual del README.

| TEST | Tipo | Requisito | TASK | Condiciones iniciales | Entradas | Resultado esperado |
|---|---|---|---|---|---|---|
| TEST-001 | unitaria | RS-01, RS-02, RS-03 | TASK-001 | Paquete `src/gestor_prestamos/` con los cuatro módulos; sin variables de entorno definidas. | Ejecutar el comando de pruebas desde la raíz del proyecto; `tests/test_humo.py` importa `modelos`, `servicio`, `almacen` y `consola`. | Los cuatro módulos se importan sin error; 0 fallos y 0 errores. |
| TEST-002 | manual | RS-02 | TASK-001 | README con la sección «Pruebas»; terminal en la raíz del proyecto, sin `PYTHONPATH` ni otras variables definidas. | Copiar y ejecutar tal cual el comando indicado en la sección «Pruebas». | El comando está documentado, ejecuta la prueba de humo y termina con código 0. |

### TASK-002 — Excluir de Git el archivo de datos

Archivo: verificación manual con Git.

| TEST | Tipo | Requisito | TASK | Condiciones iniciales | Entradas | Resultado esperado |
|---|---|---|---|---|---|---|
| TEST-003 | manual | RNF-01 | TASK-002 | `ops/.gitignore` creado con la entrada `biblioteca.json`; `ops/biblioteca.json` puede no existir. | `git check-ignore ops/biblioteca.json` desde la raíz. | Imprime `ops/biblioteca.json` (el archivo está ignorado). |
| TEST-004 | manual | RNF-01 | TASK-002 | `ops/.gitignore` creado y todavía sin versionar. | `git status` desde la raíz (si Git muestra solo `ops/`, usar `git status -uall`). | `ops/.gitignore` aparece como archivo por versionar; no aparece ningún archivo nuevo en la raíz. |

### TASK-003 — Definir `Libro` y `Prestamo`

Archivo: `tests/test_modelos.py`.

| TEST | Tipo | Requisito | TASK | Condiciones iniciales | Entradas | Resultado esperado |
|---|---|---|---|---|---|---|
| TEST-005 | unitaria | HU-001 | TASK-003 | Ninguna. | Crear un `Libro` con identificador «L-001», título «Cien años de soledad» y autor «Gabriel García Márquez». | El objeto conserva los tres campos con los mismos valores, incluidas las tildes. |
| TEST-006 | unitaria | HU-003, RN-04 | TASK-003 | Ninguna. | Crear un `Prestamo` con libro «L-001», estudiante «Ana Pérez», fecha prevista 15/12/2026 y activo = verdadero. | El objeto conserva los cuatro campos con los mismos valores. |
| TEST-007 | unitaria | HU-003 | TASK-003 | Un `Prestamo` creado con fecha prevista 15/12/2026. | Leer `fecha_prevista`. | Es de tipo fecha (no texto) y vale 15/12/2026. |
| TEST-008 | unitaria | HU-002 | TASK-003 | Un `Libro` creado. | Inspeccionar los campos del objeto. | No existe un campo de estado: el estado se deriva de los préstamos (design Decisión 3). |

### TASK-004 — Cargar los datos desde `ops/biblioteca.json`

Archivo: `tests/test_almacen.py`.

| TEST | Tipo | Requisito | TASK | Condiciones iniciales | Entradas | Resultado esperado |
|---|---|---|---|---|---|---|
| TEST-009 | unitaria | RNF-01 | TASK-004 | Carpeta temporal; el archivo de datos no existe. | `cargar` sobre esa ruta. | Devuelve libros y préstamos vacíos, sin error. |
| TEST-010 | unitaria | RNF-01 | TASK-004 | Archivo JSON válido, UTF-8, con 1 libro (título «Cien años de soledad», autor «Gabriel García Márquez») y 1 préstamo activo con fecha «2026-12-15». | `cargar`. | Devuelve objetos `Libro` y `Prestamo` con los mismos valores; las tildes están intactas y `fecha_prevista` es la fecha 15/12/2026. |
| TEST-011 | fallo | RNF-01 | TASK-004 | Archivo cuyo contenido es «{ no es json»; copia de sus bytes guardada. | `cargar`. | Lanza el error de almacén; el contenido del archivo queda byte a byte igual. |
| TEST-012 | unitaria | RNF-01 | TASK-004 | Sin indicar ruta (se usa la ruta por defecto). | Obtener la ruta por defecto desde dos directorios de trabajo distintos (la raíz del proyecto y una carpeta temporal). | La ruta es la misma en ambos casos y corresponde a `ops/biblioteca.json` dentro de la raíz del proyecto. |

### TASK-005 — Guardar los datos de forma atómica

Archivo: `tests/test_almacen.py`.

| TEST | Tipo | Requisito | TASK | Condiciones iniciales | Entradas | Resultado esperado |
|---|---|---|---|---|---|---|
| TEST-013 | unitaria | RNF-01 | TASK-005 | Carpeta temporal. Datos: libros L-001 y L-002 con tildes; préstamos: uno activo (L-001, «Ana Pérez», 15/12/2026) y uno devuelto (L-002, «Luis Gómez», 10/11/2026, inactivo). | `guardar` y a continuación `cargar` sobre el mismo archivo. | Los datos cargados son idénticos a los guardados, incluidas las tildes y el préstamo inactivo. |
| TEST-014 | unitaria | RNF-01 | TASK-005 | Mismos datos que TEST-013. | `guardar` y leer el texto del archivo. | Contiene `2026-12-15` y `2026-11-10`, no contiene `15/12/2026`; las tildes aparecen sin escapar (sin secuencias `\u`); codificación UTF-8. |
| TEST-015 | fallo | RNF-01, RNF-03 | TASK-005 | Archivo con datos válidos previos; copia de sus bytes guardada; `os.replace` simulado para que falle. | `guardar` con datos distintos de los del archivo. | La operación termina con error; el archivo original queda byte a byte igual. |

### TASK-006 — Base del servicio: error de negocio, almacén y fecha inyectados

Archivo: `tests/test_servicio.py`.

| TEST | Tipo | Requisito | TASK | Condiciones iniciales | Entradas | Resultado esperado |
|---|---|---|---|---|---|---|
| TEST-016 | unitaria | RNF-03 | TASK-006 | Almacén simulado con datos; proveedor de fecha fijo en 01/12/2026. | Crear el servicio y comprobar la fecha que obtiene del proveedor. | El servicio usa 01/12/2026 (la del proveedor inyectado); no consulta el reloj del sistema. |
| TEST-017 | unitaria | RNF-03 | TASK-006 | Almacén simulado cuya carga devuelve el libro L-001 y un préstamo activo de L-001. | Crear el servicio. | Se invoca la carga del almacén al crearse; el servicio contiene el libro y el préstamo entregados. |
| TEST-018 | unitaria | RNF-03 | TASK-006 | Ninguna. | Crear el error de negocio con el motivo «Identificador repetido». | El error expone ese mismo motivo. |

### TASK-007 — Registrar libro

Archivo: `tests/test_servicio.py`.

| TEST | Tipo | Requisito | TASK | Condiciones iniciales | Entradas | Resultado esperado |
|---|---|---|---|---|---|---|
| TEST-019 | unitaria | HU-001, RN-01, CU-001 | TASK-007 | Catálogo vacío; almacén simulado con contador de llamadas a `guardar`. | Registrar libro «L-001», «Cien años de soledad», «Gabriel García Márquez». | El libro queda en el catálogo con esos valores tal como se escribieron y en estado disponible; `guardar` se llamó exactamente una vez. |
| TEST-020 | fallo | HU-001, RNF-03, CU-001 | TASK-007 | Catálogo vacío; contador de `guardar` en 0. | Registrar con identificador «» (vacío), título «Cien años de soledad» y autor «Gabriel García Márquez». | Rechazo; el motivo indica que falta el identificador; el catálogo sigue vacío y `guardar` no se llamó. |
| TEST-021 | fallo | HU-001, RNF-03, CU-001 | TASK-007 | Catálogo vacío; contador de `guardar` en 0. | Registrar con identificador «L-001», título «» (vacío) y autor «Gabriel García Márquez». | Rechazo; el motivo indica que falta el título; el catálogo sigue vacío y `guardar` no se llamó. |
| TEST-022 | fallo | HU-001, RNF-03, CU-001 | TASK-007 | Catálogo vacío; contador de `guardar` en 0. | Registrar con identificador «L-001», título «Cien años de soledad» y autor «» (vacío). | Rechazo; el motivo indica que falta el autor; el catálogo sigue vacío y `guardar` no se llamó. |
| TEST-023 | fallo | HU-001, CU-001 | TASK-007 | Catálogo vacío; contador de `guardar` en 0. | Registrar con identificador «L-001», título «   » (solo espacios) y autor «Gabriel García Márquez». | Un dato con solo espacios cuenta como faltante: rechazo con motivo «falta el título»; sin cambios ni llamadas a `guardar`. |
| TEST-024 | fallo | RN-01, RNF-03, CU-001 | TASK-007 | Catálogo con L-001 (registrado con `guardar` llamado 1 vez). | Registrar «L-001», «El Aleph», «Jorge Luis Borges». | Rechazo; el motivo indica identificador repetido; el catálogo conserva un solo libro (el original) y `guardar` sigue en 1 llamada. |
| TEST-025 | fallo | RN-01, RNF-03, CU-001 | TASK-007 | Catálogo con L-001 (`guardar` llamado 1 vez). | Registrar «l-001» (minúscula), «El Aleph», «Jorge Luis Borges». | Rechazo por identificador repetido (no distingue mayúsculas); el catálogo conserva un solo libro y `guardar` sigue en 1 llamada. |
| TEST-026 | fallo | RN-01, RNF-03, CU-001 | TASK-007 | Catálogo con L-001 (`guardar` llamado 1 vez). | Registrar « L-001 » (con espacios al inicio y al final), «El Aleph», «Jorge Luis Borges». | Rechazo por identificador repetido (se comparan sin los espacios); el catálogo conserva un solo libro y `guardar` sigue en 1 llamada. |
| TEST-027 | fallo | RNF-03, CU-001 | TASK-007 | L-001 prestado a «Ana Pérez» (activo, prevista 15/12/2026) y L-002 disponible; contador de `guardar` anotado. | Registrar (a) «L-002» repetido y (b) un libro nuevo con autor «». | Ambos rechazados con motivo; libros y préstamos idénticos a los iniciales; el contador de `guardar` no cambia. |
| TEST-028 | fallo | HU-001, RN-01, CU-001 | TASK-007 | Catálogo con L-001. | Registrar «L-001» (repetido) con título «» (vacío). | El motivo es el dato faltante (título), no el identificador repetido: primero se valida que los datos estén completos (design Decisión 7). |

### TASK-008 — Consultar el catálogo con el estado de cada libro

Archivo: `tests/test_servicio.py`.

| TEST | Tipo | Requisito | TASK | Condiciones iniciales | Entradas | Resultado esperado |
|---|---|---|---|---|---|---|
| TEST-029 | unitaria | HU-002, CU-002 | TASK-008 | Catálogo con L-001, L-002 y L-003, sin préstamos. | Consultar el catálogo. | Devuelve 3 entradas, cada una con identificador, título, autor y estado «disponible». |
| TEST-030 | unitaria | HU-002, CU-002 | TASK-008 | L-001 disponible; L-002 prestado a «Ana Pérez» (activo, prevista 15/12/2026). | Consultar el catálogo. | L-002: estado prestado, estudiante «Ana Pérez» y fecha 15/12/2026. L-001: estado disponible, sin estudiante ni fecha. |
| TEST-031 | unitaria | HU-002, CU-002 | TASK-008 | L-001 con un préstamo devuelto (inactivo, prevista 10/11/2026) y sin préstamo activo. | Consultar el catálogo. | L-001 aparece con estado disponible. |
| TEST-032 | unitaria | HU-002, CU-002 | TASK-008 | Catálogo vacío. | Consultar el catálogo. | Devuelve una lista vacía, sin error. |
| TEST-033 | unitaria | HU-002, CU-002 | TASK-008 | L-001 disponible y L-002 prestado; contador de `guardar` anotado. | Consultar el catálogo. | Libros y préstamos sin cambios; el contador de `guardar` no cambia (CU-002: no se modifica ningún dato). |

### TASK-009 — Registrar préstamo

Archivo: `tests/test_servicio.py`.

| TEST | Tipo | Requisito | TASK | Condiciones iniciales | Entradas | Resultado esperado |
|---|---|---|---|---|---|---|
| TEST-034 | unitaria | HU-003, RN-04, CU-003 | TASK-009 | L-001 disponible. Fecha simulada 01/12/2026. | Prestar L-001 a «Ana Pérez» con fecha prevista 15/12/2026. | Se crea un préstamo activo con esos datos; L-001 pasa a prestado; `guardar` se llamó exactamente una vez. |
| TEST-035 | fallo | HU-003, RNF-03, CU-003 | TASK-009 | Catálogo con L-001 disponible. Fecha simulada 01/12/2026. | Prestar «L-099» a «Ana Pérez» con fecha 15/12/2026. | Rechazo; el motivo indica que el libro no existe; sin cambios y sin llamadas a `guardar`. |
| TEST-036 | fallo | HU-003, RN-02, RNF-03, CU-003 | TASK-009 | L-001 prestado a «Ana Pérez» (activo, prevista 15/12/2026). Fecha simulada 01/12/2026. | Prestar L-001 a «Luis Gómez» con fecha 20/12/2026. | Rechazo; el motivo indica que el libro ya está prestado; L-001 conserva un solo préstamo activo (el de Ana Pérez) y no hay llamadas nuevas a `guardar`. |
| TEST-037 | fallo | HU-003, RNF-03, CU-003 | TASK-009 | L-001 disponible. Fecha simulada 01/12/2026. | Prestar L-001 con estudiante (a) «» y (b) «   » (solo espacios), fecha 15/12/2026. | Ambos rechazados; el motivo indica que falta el estudiante; sin cambios y sin llamadas a `guardar`. |
| TEST-038 | fallo | HU-003, RNF-03, CU-003 | TASK-009 | L-001 disponible. Fecha simulada 01/12/2026. | Prestar L-001 a «Ana Pérez» con fecha «sin fecha» (`None`). | Rechazo; el motivo indica que la fecha no es válida; sin cambios y sin llamadas a `guardar`. |
| TEST-039 | fallo | HU-003, RNF-03, CU-003 | TASK-009 | L-001 disponible. Fecha simulada 01/12/2026. | Prestar L-001 a «Ana Pérez» con fecha 30/11/2026 (ayer). | Rechazo; el motivo indica que la fecha es anterior a hoy; sin cambios y sin llamadas a `guardar`. |
| TEST-040 | unitaria | HU-003, CU-003 | TASK-009 | L-001 disponible. Fecha simulada 01/12/2026. | Prestar L-001 a «Ana Pérez» con fecha 01/12/2026 (hoy). | Aceptado: préstamo activo registrado y L-001 prestado (design Decisión 5: la fecha de hoy es válida). |
| TEST-041 | unitaria | HU-003, CU-003 | TASK-009 | L-001 disponible. Fecha simulada 01/12/2026. | Prestar «l-001» (minúscula) a «Ana Pérez» con fecha 15/12/2026. | El préstamo se registra sobre L-001: la búsqueda del libro no distingue mayúsculas. |
| TEST-042 | fallo | RNF-03, CU-003 | TASK-009 | L-001 prestado a «Ana Pérez» (activo, prevista 15/12/2026) y L-002 disponible; contador de `guardar` anotado. Fecha simulada 01/12/2026. | Cuatro intentos: (a) «L-099»; (b) L-001 ya prestado; (c) L-002 con estudiante «»; (d) L-002 con fecha 30/11/2026. | Los cuatro se rechazan con motivo; libros y préstamos idénticos a los iniciales; el contador de `guardar` no cambia. |
| TEST-043 | fallo | HU-003, CU-003 | TASK-009 | L-001 prestado, L-002 disponible. Fecha simulada 01/12/2026. | Tres intentos con estudiante «» y fecha `None`: (a) «L-099»; (b) L-001; (c) L-002. | Motivos en el orden de validación (design Decisión 7): (a) el libro no existe; (b) el libro ya está prestado; (c) falta el estudiante. |

### TASK-010 — Registrar devolución

Archivo: `tests/test_servicio.py`.

| TEST | Tipo | Requisito | TASK | Condiciones iniciales | Entradas | Resultado esperado |
|---|---|---|---|---|---|---|
| TEST-044 | unitaria | HU-004, RN-04, CU-004 | TASK-010 | L-001 prestado a «Ana Pérez» (activo, prevista 15/12/2026). | Devolver L-001. | El préstamo queda inactivo y se conserva (sigue habiendo 1 préstamo en total); L-001 queda disponible; `guardar` se llamó exactamente una vez. |
| TEST-045 | fallo | HU-004, RNF-03, CU-004 | TASK-010 | Catálogo con L-001. | Devolver «L-099». | Rechazo; el motivo indica que el libro no existe; sin cambios y sin llamadas a `guardar`. |
| TEST-046 | fallo | HU-004, RNF-03, CU-004 | TASK-010 | L-001 disponible, sin préstamos. | Devolver L-001. | Rechazo; el motivo indica que el libro no está prestado; sin cambios y sin llamadas a `guardar`. |
| TEST-047 | unitaria | HU-004, RN-02, CU-004 | TASK-010 | L-001 prestado a «Ana Pérez» (activo, prevista 15/12/2026). Fecha simulada 01/12/2026. | Devolver L-001 y luego prestar L-001 a «Luis Gómez» con fecha 15/12/2026. | El segundo préstamo se acepta; L-001 tiene 2 préstamos (el de Ana Pérez inactivo, el de Luis Gómez activo) y queda prestado. |
| TEST-048 | fallo | RNF-03, CU-004 | TASK-010 | L-001 prestado y L-002 disponible; contador de `guardar` anotado. | Devolver (a) «L-099» y (b) L-002. | Ambos rechazados con motivo; libros y préstamos idénticos a los iniciales; el contador de `guardar` no cambia. |
| TEST-049 | aceptación | RN-04, CU-004<br>*Scenario:* «Préstamo recién registrado» | TASK-010 | L-001 disponible. Fecha simulada 01/12/2026. | (1) Prestar L-001 a «Ana Pérez» con fecha 15/12/2026; (2) consultar el catálogo; (3) devolver L-001. | Tras (1) el préstamo está activo; tras (2) sigue activo; tras (3) está inactivo: el préstamo es activo desde su registro hasta su devolución. |

### TASK-011 — Consultar préstamos vencidos

Archivo: `tests/test_servicio.py`.

| TEST | Tipo | Requisito | TASK | Condiciones iniciales | Entradas | Resultado esperado |
|---|---|---|---|---|---|---|
| TEST-050 | unitaria | HU-005, RN-03, CU-002 | TASK-011 | L-001 prestado a «Ana Pérez» (activo, prevista 30/11/2026). Fecha simulada 01/12/2026. | Consultar los préstamos vencidos. | Devuelve 1 préstamo: libro L-001 (identificador y título «Cien años de soledad»), estudiante «Ana Pérez» y fecha 30/11/2026. |
| TEST-051 | unitaria | RN-03, CU-002 | TASK-011 | L-001 prestado (activo, prevista 01/12/2026, igual a hoy). Fecha simulada 01/12/2026. | Consultar los préstamos vencidos. | Lista vacía: un préstamo con fecha de hoy no está vencido. |
| TEST-052 | unitaria | RN-03, CU-002 | TASK-011 | L-001 prestado (activo, prevista 15/12/2026). Fecha simulada 01/12/2026. | Consultar los préstamos vencidos. | Lista vacía: un préstamo con fecha futura no está vencido. |
| TEST-053 | unitaria | HU-005, CU-002 | TASK-011 | L-001 con un préstamo devuelto (inactivo, prevista 10/11/2026). Fecha simulada 01/12/2026. | Consultar los préstamos vencidos. | Lista vacía: el préstamo devuelto no aparece aunque su fecha ya pasó. |
| TEST-054 | unitaria | HU-005, CU-002 | TASK-011 | (a) Sin préstamos; (b) L-001 prestado (activo, prevista 15/12/2026). Fecha simulada 01/12/2026. | Consultar los préstamos vencidos en cada caso. | Devuelve una lista vacía en ambos casos. |
| TEST-055 | unitaria | HU-005, RN-03, CU-002 | TASK-011 | Préstamos: L-001 activo prevista 10/11/2026; L-002 activo 30/11/2026; L-003 activo 01/12/2026; L-004 activo 15/12/2026; L-005 devuelto (inactivo) 10/11/2026. Fecha simulada 01/12/2026. | Consultar los préstamos vencidos. | Devuelve exactamente L-001 y L-002, cada uno con libro, estudiante y fecha prevista; L-003, L-004 y L-005 no aparecen. |
| TEST-056 | unitaria | HU-005, CU-002 | TASK-011 | L-001 vencido (activo, prevista 30/11/2026); contador de `guardar` anotado. Fecha simulada 01/12/2026. | Consultar los préstamos vencidos. | Libros y préstamos sin cambios; el contador de `guardar` no cambia. |

### TASK-012 — Convertir fechas `DD/MM/AAAA`

Archivo: `tests/test_consola.py`.

| TEST | Tipo | Requisito | TASK | Condiciones iniciales | Entradas | Resultado esperado |
|---|---|---|---|---|---|---|
| TEST-057 | unitaria | HU-003 | TASK-012 | Ninguna. | Convertir el texto «15/12/2026». | Devuelve la fecha 15/12/2026. |
| TEST-058 | fallo | HU-003 | TASK-012 | Ninguna. | Convertir el texto «31/02/2026». | Devuelve `None`: la fecha no existe en el calendario. |
| TEST-059 | fallo | HU-003 | TASK-012 | Ninguna. | Convertir el texto «2026-12-15». | Devuelve `None`: el formato no es `DD/MM/AAAA`. |
| TEST-060 | fallo | HU-003 | TASK-012 | Ninguna. | Convertir el texto «5/1/2026». | Devuelve `None`: día y mes no tienen dos dígitos. |
| TEST-061 | fallo | HU-003 | TASK-012 | Ninguna. | Convertir el texto «» (vacío). | Devuelve `None`. |
| TEST-062 | fallo | HU-003 | TASK-012 | Ninguna. | Convertir (a) «abc» y (b) «dd/mm/aaaa». | Ambos devuelven `None`: texto no numérico. |
| TEST-063 | unitaria | HU-003 | TASK-012 | Ninguna. | Convertir «15/12/2026» a fecha y esa fecha otra vez a texto. | El texto resultante es «15/12/2026»; la fecha se conserva en la ida y vuelta. |
| TEST-064 | unitaria | HU-003 | TASK-012 | Ninguna. | Convertir a texto la fecha 5 de enero de 2026. | Devuelve «05/01/2026» (dos dígitos de día y de mes, cuatro de año). |

### TASK-013 — Menú principal

Archivo: `tests/test_consola.py`.

| TEST | Tipo | Requisito | TASK | Condiciones iniciales | Entradas | Resultado esperado |
|---|---|---|---|---|---|---|
| TEST-065 | unitaria | RNF-02 | TASK-013 | Operaciones simuladas que no hacen nada. | Entradas: «6» (salir). | La salida muestra seis opciones numeradas: registrar libro, consultar catálogo, registrar préstamo, registrar devolución, consultar vencidos y salir. |
| TEST-066 | unitaria | RNF-02 | TASK-013 | Operaciones simuladas que registran sus llamadas. | Cinco ejecuciones; entradas de cada una: (opción 1 a 5), «6». | Cada opción invoca únicamente su operación, una vez; el menú se vuelve a mostrar antes de leer la entrada siguiente. |
| TEST-067 | fallo | RNF-02 | TASK-013 | Operaciones simuladas que registran sus llamadas. | Entradas: «9», «6». | Se muestra un aviso de opción inválida, sin error ni excepción; el menú se vuelve a mostrar; ninguna operación se invoca. |
| TEST-068 | fallo | RNF-02 | TASK-013 | Operaciones simuladas que registran sus llamadas. | Entradas: «abc», «6». | Se muestra un aviso, sin error ni excepción; el menú se vuelve a mostrar; ninguna operación se invoca. |
| TEST-069 | fallo | RNF-02 | TASK-013 | Operaciones simuladas que registran sus llamadas. | Entradas: «» (vacía), «6». | Se muestra un aviso, sin error ni excepción; el menú se vuelve a mostrar; ninguna operación se invoca. |
| TEST-070 | unitaria | RNF-02 | TASK-013 | Operaciones simuladas que registran sus llamadas. | Entradas: «6» y una entrada sobrante «1». | El ciclo termina; ninguna operación se invoca; la entrada sobrante no se consume. |

### TASK-014 — Opción «Registrar libro»

Archivo: `tests/test_consola.py`.

| TEST | Tipo | Requisito | TASK | Condiciones iniciales | Entradas | Resultado esperado |
|---|---|---|---|---|---|---|
| TEST-071 | aceptación | HU-001, CU-001<br>*Scenario:* «Registro con datos completos» | TASK-014 | Catálogo vacío. | Menú: «1», «L-001», «Cien años de soledad», «Gabriel García Márquez», «6». | Se solicitan identificador, título y autor, uno por vez y en ese orden; se muestra la confirmación del registro; el servicio contiene L-001 con esos datos y estado disponible; se vuelve al menú. |
| TEST-072 | aceptación | HU-001, RNF-03, CU-001<br>*Scenario:* «Falta un dato» | TASK-014 | Catálogo vacío. | Menú: «1», «» (identificador vacío), «Cien años de soledad», «Gabriel García Márquez», «6». | Se muestra que falta el identificador; no hay confirmación; el catálogo sigue vacío; se vuelve al menú. |
| TEST-073 | aceptación | HU-001, RNF-03, CU-001<br>*Scenario:* «Falta un dato» | TASK-014 | Catálogo vacío. | Menú: «1», «L-001», «» (título vacío), «Gabriel García Márquez», «6». | Se muestra que falta el título; no hay confirmación; el catálogo sigue vacío; se vuelve al menú. |
| TEST-074 | aceptación | HU-001, RNF-03, CU-001<br>*Scenario:* «Falta un dato» | TASK-014 | Catálogo vacío. | Menú: «1», «L-001», «Cien años de soledad», «» (autor vacío), «6». | Se muestra que falta el autor; no hay confirmación; el catálogo sigue vacío; se vuelve al menú. |
| TEST-075 | aceptación | RN-01, RNF-03, CU-001<br>*Scenario:* «Identificador repetido»; «Rechazo en cualquier operación» | TASK-014 | Catálogo con L-001 «Cien años de soledad». | Menú: «1», «L-001», «El Aleph», «Jorge Luis Borges», «6». | Se muestra el motivo (identificador repetido); no hay confirmación; el catálogo conserva un solo libro, el original; se vuelve al menú. |

### TASK-015 — Opción «Consultar catálogo»

Archivo: `tests/test_consola.py`.

| TEST | Tipo | Requisito | TASK | Condiciones iniciales | Entradas | Resultado esperado |
|---|---|---|---|---|---|---|
| TEST-076 | aceptación | HU-002, CU-002<br>*Scenario:* «Catálogo con libros» | TASK-015 | L-001 disponible; L-002 prestado a «Ana Pérez» (activo, prevista 15/12/2026). | Menú: «2», «6». | La salida lista L-001 y L-002, cada uno con identificador, título, autor y estado (disponible / prestado). |
| TEST-077 | aceptación | HU-002, CU-002<br>*Scenario:* «Libro prestado en el catálogo» | TASK-015 | Mismos datos que TEST-076. | Menú: «2», «6». | Para L-002 la salida incluye «Ana Pérez» y «15/12/2026» (formato DD/MM/AAAA, nunca «2026-12-15»); para L-001 no muestra estudiante ni fecha. |
| TEST-078 | aceptación | HU-002, CU-002<br>*Scenario:* «Catálogo vacío» | TASK-015 | Catálogo vacío. | Menú: «2», «6». | La salida informa que no hay libros registrados; no hay error. |

### TASK-016 — Opción «Registrar préstamo»

Archivo: `tests/test_consola.py`.

| TEST | Tipo | Requisito | TASK | Condiciones iniciales | Entradas | Resultado esperado |
|---|---|---|---|---|---|---|
| TEST-079 | aceptación | HU-003, RN-04, RNF-02, CU-003<br>*Scenario:* «Préstamo de libro disponible» | TASK-016 | L-001 disponible. Fecha simulada 01/12/2026. | Menú: «3», «L-001», «Ana Pérez», «15/12/2026», «6». | Se piden exactamente tres datos (libro, estudiante, fecha) y no se pide ninguna confirmación adicional; se confirma el préstamo; L-001 queda prestado con un préstamo activo (Ana Pérez, 15/12/2026); se vuelve al menú. |
| TEST-080 | aceptación | HU-003, RNF-03, CU-003<br>*Scenario:* «Falta el estudiante o la fecha no es válida» | TASK-016 | L-001 disponible. Fecha simulada 01/12/2026. | Menú: «3», «L-001», «Ana Pérez», «2026-12-15» (formato inválido), «6». | Se muestra el motivo (fecha no válida); no hay confirmación; L-001 sigue disponible y sin préstamos; se vuelve al menú. |
| TEST-081 | aceptación | HU-003, RNF-03, CU-003<br>*Scenario:* «Falta el estudiante o la fecha no es válida» | TASK-016 | L-001 disponible. Fecha simulada 01/12/2026. | Menú: «3», «L-001», «» (estudiante vacío), «15/12/2026», «6». | Se muestra el motivo (falta el estudiante); no hay confirmación; L-001 sigue disponible y sin préstamos; se vuelve al menú. |
| TEST-082 | aceptación | HU-003, RNF-03, CU-003<br>*Scenario:* «Libro inexistente»; «Rechazo en cualquier operación» | TASK-016 | Catálogo con L-001 disponible. Fecha simulada 01/12/2026. | Menú: «3», «L-099», «Ana Pérez», «15/12/2026», «6». | Se muestra el motivo (el libro no existe); no hay confirmación; los datos no cambian; se vuelve al menú. |
| TEST-083 | aceptación | HU-003, RN-02, RNF-03, CU-003<br>*Scenario:* «Libro ya prestado»; «Rechazo en cualquier operación» | TASK-016 | L-001 prestado a «Ana Pérez» (activo, prevista 15/12/2026). Fecha simulada 01/12/2026. | Menú: «3», «L-001», «Luis Gómez», «20/12/2026», «6». | Se muestra el motivo (el libro ya está prestado); no hay confirmación; L-001 conserva un solo préstamo activo, el de Ana Pérez; se vuelve al menú. |
| TEST-084 | fallo | HU-003, RNF-03, CU-003 | TASK-016 | L-001 disponible. Fecha simulada 01/12/2026. | Dos ejecuciones; fecha ingresada: (a) «30/11/2026», (b) «31/02/2026». Resto: «3», «L-001», «Ana Pérez», «6». | En ambas se muestra el motivo (fecha no válida: anterior a hoy / inexistente); L-001 sigue disponible y sin préstamos. |

### TASK-017 — Opción «Registrar devolución»

Archivo: `tests/test_consola.py`.

| TEST | Tipo | Requisito | TASK | Condiciones iniciales | Entradas | Resultado esperado |
|---|---|---|---|---|---|---|
| TEST-085 | aceptación | HU-004, RNF-02, CU-004<br>*Scenario:* «Devolución de libro prestado» | TASK-017 | L-001 prestado a «Ana Pérez» (activo, prevista 15/12/2026). | Menú: «4», «L-001», «6». | La operación consume exactamente una entrada y no pide confirmaciones adicionales; se confirma la devolución; L-001 queda disponible y su préstamo, inactivo; se vuelve al menú. |
| TEST-086 | aceptación | HU-004, RNF-03, CU-004<br>*Scenario:* «Libro no prestado o inexistente»; «Rechazo en cualquier operación» | TASK-017 | Catálogo con L-001. | Menú: «4», «L-099», «6». | Se muestra el motivo (el libro no existe); no hay confirmación; los datos no cambian; se vuelve al menú. |
| TEST-087 | aceptación | HU-004, RNF-03, CU-004<br>*Scenario:* «Libro no prestado o inexistente»; «Rechazo en cualquier operación» | TASK-017 | L-001 disponible, sin préstamos. | Menú: «4», «L-001», «6». | Se muestra el motivo (el libro no está prestado); no hay confirmación; los datos no cambian; se vuelve al menú. |

### TASK-018 — Opción «Consultar préstamos vencidos»

Archivo: `tests/test_consola.py`.

| TEST | Tipo | Requisito | TASK | Condiciones iniciales | Entradas | Resultado esperado |
|---|---|---|---|---|---|---|
| TEST-088 | aceptación | HU-005, RN-03, CU-002<br>*Scenario:* «Préstamo activo con fecha pasada» | TASK-018 | L-001 prestado a «Ana Pérez» (activo, prevista 30/11/2026). Fecha simulada 01/12/2026. | Menú: «5», «6». | La salida lista el préstamo con libro (L-001, «Cien años de soledad»), estudiante «Ana Pérez» y fecha «30/11/2026» (DD/MM/AAAA). |
| TEST-089 | aceptación | HU-005, CU-002<br>*Scenario:* «Préstamos devueltos» | TASK-018 | L-001 con préstamo devuelto (inactivo, prevista 10/11/2026); L-002 prestado a «Luis Gómez» (activo, prevista 30/11/2026). Fecha simulada 01/12/2026. | Menú: «5», «6». | La salida incluye L-002 y no incluye L-001. |
| TEST-090 | aceptación | HU-005, CU-002<br>*Scenario:* «Sin préstamos vencidos» | TASK-018 | L-001 prestado a «Ana Pérez» (activo, prevista 15/12/2026), no vencido. Fecha simulada 01/12/2026. | Menú: «5», «6». | La salida informa que no hay préstamos vencidos y no lista L-001. |
| TEST-091 | aceptación | HU-005, RN-03, CU-002<br>*Scenario:* «Hay préstamos vencidos» | TASK-018 | Mismos préstamos que TEST-055. Fecha simulada 01/12/2026. | Menú: «5», «6». | La salida lista exactamente L-001 y L-002, con libro, estudiante y fecha en DD/MM/AAAA; no aparecen L-003, L-004 ni L-005. |

### TASK-019 — Punto de entrada y uso en el README

Archivo: `tests/test_entrada.py`; verificación manual del README.

| TEST | Tipo | Requisito | TASK | Condiciones iniciales | Entradas | Resultado esperado |
|---|---|---|---|---|---|---|
| TEST-092 | fallo | RNF-01, RS-01 | TASK-019 | Archivo de datos con el contenido «{ no es json» en la ruta que usa el punto de entrada; copia de sus bytes guardada (ver S-5). | Ejecutar el punto de entrada en un subproceso, sin entradas. | Muestra el error de lectura; termina con código distinto de 0; el archivo queda byte a byte igual. |
| TEST-093 | manual | RS-01, RS-03, PER-01 | TASK-019 | README con el comando de inicio; terminal en la raíz del proyecto. | Ejecutar el comando documentado y elegir la opción de salir. | Se muestra el menú en consola, sin pedir usuario ni contraseña ni abrir ventanas; el programa termina al salir. |
| TEST-094 | manual | RNF-01 | TASK-019 | Terminal en una carpeta distinta de la raíz; `ops/biblioteca.json` inexistente al comenzar (si ya existe, respaldarlo antes y restaurarlo al terminar). | (1) Ejecutar el comando documentado desde la raíz, registrar L-001 y salir; (2) ejecutar el mismo comando desde la otra carpeta y consultar el catálogo. | En (2) se muestra el menú y el catálogo contiene L-001: se usó el mismo `ops/biblioteca.json`; no se creó ningún archivo de datos en la otra carpeta. |
| TEST-095 | manual | RNF-01, RS-02 | TASK-019 | README con la sección de uso. | Leer la sección de uso. | Documenta el comando de inicio, la ruta de datos `ops/biblioteca.json`, Python 3.12 como mínimo y que copiar el archivo sirve de respaldo. |

### TASK-020 — Verificar persistencia y rechazos de extremo a extremo

Archivo: `tests/test_integracion.py`.

| TEST | Tipo | Requisito | TASK | Condiciones iniciales | Entradas | Resultado esperado |
|---|---|---|---|---|---|---|
| TEST-096 | aceptación | RNF-01<br>*Scenario:* «Cerrar y reabrir la aplicación» | TASK-020 | Archivo temporal inexistente; almacén y servicio reales. Fecha simulada 01/12/2026. | Registrar L-001 «Cien años de soledad» y L-002 «El Aleph»; prestar L-001 a «Ana Pérez» hasta 15/12/2026; descartar almacén y servicio; crear nuevos sobre el mismo archivo; consultar el catálogo. | El catálogo es idéntico al de antes del cierre: L-001 prestado (Ana Pérez, 15/12/2026), L-002 disponible; títulos y autores iguales, con tildes. |
| TEST-097 | integración | RNF-01 | TASK-020 | Estado final de TEST-096. | Devolver L-001; descartar y crear nuevos almacén y servicio sobre el mismo archivo; consultar el catálogo. | L-001 aparece disponible y su préstamo devuelto se conserva como inactivo. |
| TEST-098 | integración | HU-001, RN-01, RNF-03 | TASK-020 | Archivo temporal con L-001 prestado a «Ana Pérez» (activo, prevista 15/12/2026) y L-002 disponible; copia de sus bytes guardada. | Registrar el libro «L-002» (repetido). | Rechazo con motivo; el archivo queda byte a byte igual. |
| TEST-099 | integración | HU-003, RNF-03 | TASK-020 | Mismo archivo que TEST-098. Fecha simulada 01/12/2026. | Prestar «L-099» a «Luis Gómez» con fecha 20/12/2026. | Rechazo con motivo; el archivo queda byte a byte igual. |
| TEST-100 | integración | RN-02, RNF-03 | TASK-020 | Mismo archivo que TEST-098. Fecha simulada 01/12/2026. | Prestar L-001 a «Luis Gómez» con fecha 20/12/2026. | Rechazo con motivo; el archivo queda byte a byte igual. |
| TEST-101 | integración | HU-004, RNF-03 | TASK-020 | Mismo archivo que TEST-098. | Devolver L-002 (no prestado). | Rechazo con motivo; el archivo queda byte a byte igual. |

### TASK-021 — Verificar el flujo completo por consola

Archivo: `tests/test_integracion.py`.

| TEST | Tipo | Requisito | TASK | Condiciones iniciales | Entradas | Resultado esperado |
|---|---|---|---|---|---|---|
| TEST-102 | integración | HU-001, HU-002, HU-003, HU-004, HU-005, RN-02, RN-03 | TASK-021 | Catálogo vacío; servicio real; fecha simulada 01/11/2026 en los pasos 1 y 2 y 01/12/2026 desde el paso 3 (ver S-2). | Menú, en orden: (1) registrar L-001 «Cien años de soledad», «Gabriel García Márquez»; (2) registrar préstamo de L-001 a «Ana Pérez», fecha 10/11/2026; (3) consultar catálogo; (4) consultar vencidos; (5) registrar préstamo de L-001 a «Luis Gómez», fecha 15/12/2026; (6) registrar devolución de L-001; (7) consultar catálogo; (8) consultar vencidos; salir. | (1) y (2) confirmados; (3) L-001 prestado a Ana Pérez con 10/11/2026; (4) lista L-001 / Ana Pérez / 10/11/2026; (5) rechazado, el libro ya está prestado; (6) confirmada; (7) L-001 disponible; (8) informa que no hay préstamos vencidos. |

### TASK-022 — Verificar RNF-02 con un usuario sin capacitación

Archivo: `review/verificacion-rnf-02.md`.

| TEST | Tipo | Requisito | TASK | Condiciones iniciales | Entradas | Resultado esperado |
|---|---|---|---|---|---|---|
| TEST-103 | aceptación | RNF-02, CU-003<br>*Scenario:* «Usuario sin capacitación previa» | TASK-022 | Ejecución manual. Persona sin capacitación previa (se anota solo su rol); aplicación abierta con L-001 disponible; cronómetro. | Pedir a la persona que registre el préstamo de L-001 con el estudiante y la fecha prevista que indica el evaluador; medir el tiempo (ver S-3). | El préstamo queda registrado en menos de 1 minuto. |
| TEST-104 | aceptación | RNF-02, CU-004<br>*Scenario:* «Usuario sin capacitación previa» | TASK-022 | Ejecución manual. Misma persona; L-001 prestado; cronómetro. | Pedir a la persona que registre la devolución de L-001; medir el tiempo (ver S-3). | La devolución queda registrada en menos de 1 minuto. |
| TEST-105 | manual | RNF-02 | TASK-022 | Tiempos de TEST-103 y TEST-104 medidos. | Revisar `review/verificacion-rnf-02.md` con el equipo. | El archivo indica fecha, rol de la persona (sin datos personales), tiempo de cada operación y resultado (cumple si ambos son menores de 1 minuto); el equipo lo revisó. |

## 5. Supuestos, preguntas abiertas y riesgos

| ID | Tema | Supuesto o pregunta | Efecto en el plan |
|---|---|---|---|
| S-1 | Numeración del menú | TASK-013 no fija los números. Supuesto: 1 registrar libro, 2 consultar catálogo, 3 registrar préstamo, 4 registrar devolución, 5 consultar vencidos, 6 salir (el orden en que TASK-013 las enumera). | Si cambia, solo se ajustan las entradas de TEST-065–091 y TEST-102. |
| S-2 | TASK-021 y fecha ya pasada | TASK-021 pide registrar un préstamo «con fecha ya pasada» usando fecha fija, pero TASK-009 y design Decisión 5 rechazan fechas anteriores a hoy. Supuesto: TEST-102 usa dos fechas simuladas fijas consecutivas: 01/11/2026 al registrar (fecha prevista 10/11/2026, válida) y 01/12/2026 desde la consulta (la fecha prevista ya pasó). **Pregunta:** ¿se acepta esa lectura o se reformula el criterio de TASK-021? | Solo afecta a TEST-102. |
| S-3 | Medición de RNF-02 | La spec no dice cuándo empieza ni termina el tiempo. Supuesto: desde que la persona elige la opción del menú hasta que ve la confirmación, con la aplicación ya abierta. **Pregunta:** ¿lo acepta el equipo? | Afecta a TEST-103 y TEST-104. |
| S-4 | Identificador «tal como se escribió» | Design Decisión 7 no aclara si se conservan los espacios al inicio y al final del identificador guardado. **Pregunta:** ¿se conservan o se recortan? | Ninguna prueba fija ese punto; solo se prueba que la comparación ignora mayúsculas y espacios (TEST-025, TEST-026, TEST-041). |
| S-5 | Archivo corrupto en TASK-019 | Ni TASK-019 ni design Decisión 10 definen cómo la prueba hace que el punto de entrada use un archivo corrupto sin tocar el real (parámetro de ruta, variable de entorno u otro). **Pregunta:** ¿qué mecanismo se admite? | TEST-092 solo exige un archivo corrupto en la ruta que use el punto de entrada. Si esa ruta es `ops/biblioteca.json`, la prueba debe respaldarlo y restaurarlo. |

## 6. Cobertura

### 6.1 Requisito → TEST → TASK

| Requisito | TEST | TASK |
|---|---|---|
| HU-001 | TEST-005 | TASK-003 |
| HU-001 | TEST-019–023, TEST-028 | TASK-007 |
| HU-001 | TEST-071–074 | TASK-014 |
| HU-001 | TEST-098 | TASK-020 |
| HU-001 | TEST-102 | TASK-021 |
| HU-002 | TEST-008 | TASK-003 |
| HU-002 | TEST-029–033 | TASK-008 |
| HU-002 | TEST-076–078 | TASK-015 |
| HU-002 | TEST-102 | TASK-021 |
| HU-003 | TEST-006, TEST-007 | TASK-003 |
| HU-003 | TEST-034–041, TEST-043 | TASK-009 |
| HU-003 | TEST-057–064 | TASK-012 |
| HU-003 | TEST-079–084 | TASK-016 |
| HU-003 | TEST-099 | TASK-020 |
| HU-003 | TEST-102 | TASK-021 |
| HU-004 | TEST-044–047 | TASK-010 |
| HU-004 | TEST-085–087 | TASK-017 |
| HU-004 | TEST-101 | TASK-020 |
| HU-004 | TEST-102 | TASK-021 |
| HU-005 | TEST-050, TEST-053–056 | TASK-011 |
| HU-005 | TEST-088–091 | TASK-018 |
| HU-005 | TEST-102 | TASK-021 |
| RN-01 | TEST-019, TEST-024–026, TEST-028 | TASK-007 |
| RN-01 | TEST-075 | TASK-014 |
| RN-01 | TEST-098 | TASK-020 |
| RN-02 | TEST-036 | TASK-009 |
| RN-02 | TEST-047 | TASK-010 |
| RN-02 | TEST-083 | TASK-016 |
| RN-02 | TEST-100 | TASK-020 |
| RN-02 | TEST-102 | TASK-021 |
| RN-03 | TEST-050–052, TEST-055 | TASK-011 |
| RN-03 | TEST-088, TEST-091 | TASK-018 |
| RN-03 | TEST-102 | TASK-021 |
| RN-04 | TEST-006 | TASK-003 |
| RN-04 | TEST-034 | TASK-009 |
| RN-04 | TEST-044, TEST-049 | TASK-010 |
| RN-04 | TEST-079 | TASK-016 |
| RNF-01 | TEST-003, TEST-004 | TASK-002 |
| RNF-01 | TEST-009–012 | TASK-004 |
| RNF-01 | TEST-013–015 | TASK-005 |
| RNF-01 | TEST-092, TEST-094, TEST-095 | TASK-019 |
| RNF-01 | TEST-096, TEST-097 | TASK-020 |
| RNF-02 | TEST-065–070 | TASK-013 |
| RNF-02 | TEST-079 | TASK-016 |
| RNF-02 | TEST-085 | TASK-017 |
| RNF-02 | TEST-103–105 | TASK-022 |
| RNF-03 | TEST-015 | TASK-005 |
| RNF-03 | TEST-016–018 | TASK-006 |
| RNF-03 | TEST-020–022, TEST-024–027 | TASK-007 |
| RNF-03 | TEST-035–039, TEST-042 | TASK-009 |
| RNF-03 | TEST-045, TEST-046, TEST-048 | TASK-010 |
| RNF-03 | TEST-072–075 | TASK-014 |
| RNF-03 | TEST-080–084 | TASK-016 |
| RNF-03 | TEST-086, TEST-087 | TASK-017 |
| RNF-03 | TEST-098–101 | TASK-020 |
| CU-001 | TEST-019–028 | TASK-007 |
| CU-001 | TEST-071–075 | TASK-014 |
| CU-002 | TEST-029–033 | TASK-008 |
| CU-002 | TEST-050–056 | TASK-011 |
| CU-002 | TEST-076–078 | TASK-015 |
| CU-002 | TEST-088–091 | TASK-018 |
| CU-003 | TEST-034–043 | TASK-009 |
| CU-003 | TEST-079–084 | TASK-016 |
| CU-003 | TEST-103 | TASK-022 |
| CU-004 | TEST-044–049 | TASK-010 |
| CU-004 | TEST-085–087 | TASK-017 |
| CU-004 | TEST-104 | TASK-022 |
| RS-01 | TEST-001 | TASK-001 |
| RS-01 | TEST-092, TEST-093 | TASK-019 |
| RS-02 | TEST-001, TEST-002 | TASK-001 |
| RS-02 | TEST-095 | TASK-019 |
| RS-03 | TEST-001 | TASK-001 |
| RS-03 | TEST-093 | TASK-019 |
| PER-01 | TEST-093 | TASK-019 |
| RS-04 | — (restricción de alcance; se controla con la sección 1) | — |

### 6.2 Scenario → prueba de aceptación

| Spec | Requisito | Scenario | TEST de aceptación | TASK |
|---|---|---|---|---|
| catalogo | HU-001 | Registro con datos completos | TEST-071 | TASK-014 |
| catalogo | HU-001 | Falta un dato | TEST-072–074 | TASK-014 |
| catalogo | RN-01 | Identificador repetido | TEST-075 | TASK-014 |
| catalogo | HU-002 | Catálogo con libros | TEST-076 | TASK-015 |
| catalogo | HU-002 | Libro prestado en el catálogo | TEST-077 | TASK-015 |
| catalogo | HU-002 | Catálogo vacío | TEST-078 | TASK-015 |
| prestamos | HU-003 | Préstamo de libro disponible | TEST-079 | TASK-016 |
| prestamos | HU-003 | Libro inexistente | TEST-082 | TASK-016 |
| prestamos | HU-003 | Falta el estudiante o la fecha no es válida | TEST-080, TEST-081 | TASK-016 |
| prestamos | RN-02 | Libro ya prestado | TEST-083 | TASK-016 |
| prestamos | RN-04 | Préstamo recién registrado | TEST-049 | TASK-010 |
| prestamos | HU-004 | Devolución de libro prestado | TEST-085 | TASK-017 |
| prestamos | HU-004 | Libro no prestado o inexistente | TEST-086, TEST-087 | TASK-017 |
| prestamos | RN-03 | Préstamo activo con fecha pasada | TEST-088 | TASK-018 |
| prestamos | HU-005 | Hay préstamos vencidos | TEST-091 | TASK-018 |
| prestamos | HU-005 | Préstamos devueltos | TEST-089 | TASK-018 |
| prestamos | HU-005 | Sin préstamos vencidos | TEST-090 | TASK-018 |
| prestamos | RNF-02 | Usuario sin capacitación previa | TEST-103, TEST-104 | TASK-022 |
| datos | RNF-01 | Cerrar y reabrir la aplicación | TEST-096 | TASK-020 |
| datos | RNF-03 | Rechazo en cualquier operación | TEST-075, TEST-082, TEST-083, TEST-086, TEST-087 | TASK-014, TASK-016, TASK-017 |

### 6.3 Criterio de aceptación de cada tarea → TEST

| TASK | Criterio de aceptación | TEST |
|---|---|---|
| TASK-001 | Importa los cuatro módulos (prueba de humo) | TEST-001 |
| TASK-001 | Desde la raíz, sin variables de entorno, el comando de pruebas termina con 0 fallos | TEST-001, TEST-002 |
| TASK-002 | `git check-ignore ops/biblioteca.json` imprime la ruta | TEST-003 |
| TASK-002 | `ops/.gitignore` aparece en `git status` como archivo por versionar | TEST-004 |
| TASK-003 | Ambos objetos conservan sus campos | TEST-005, TEST-006 |
| TASK-003 | `fecha_prevista` es de tipo fecha | TEST-007 |
| TASK-003 | `Libro` no tiene campo de estado | TEST-008 |
| TASK-004 | Archivo inexistente → catálogo vacío | TEST-009 |
| TASK-004 | Archivo válido con tildes en título y autor | TEST-010 |
| TASK-004 | JSON inválido → error y contenido del archivo sin cambios | TEST-011 |
| TASK-004 | La ruta por defecto es la misma tras cambiar el directorio de trabajo | TEST-012 |
| TASK-005 | `cargar(guardar(x))` devuelve datos idénticos (tildes y préstamos devueltos) | TEST-013 |
| TASK-005 | El archivo contiene las fechas en formato ISO | TEST-014 |
| TASK-005 | Si `os.replace` falla (simulado), el archivo original queda intacto | TEST-015 |
| TASK-006 | Usa la fecha fija inyectada | TEST-016 |
| TASK-006 | Carga los datos del almacén | TEST-017 |
| TASK-006 | El error de negocio expone su motivo | TEST-018 |
| TASK-007 | Registro completo | TEST-019 |
| TASK-007 | Falta identificador, título o autor (motivo correcto) | TEST-020–022 |
| TASK-007 | Identificador repetido: igual, con distinta mayúscula y con espacios alrededor | TEST-024–026 |
| TASK-007 | En los rechazos los datos y las llamadas a `guardar` no cambian | TEST-020–022, TEST-024–027 |
| TASK-007 | Complemento del «Resultado esperado»: dato con solo espacios y orden de validación | TEST-023, TEST-028 |
| TASK-008 | Catálogo con varios libros | TEST-029 |
| TASK-008 | Libro prestado (incluye estudiante y fecha) | TEST-030 |
| TASK-008 | Libro devuelto aparece disponible | TEST-031 |
| TASK-008 | Catálogo vacío devuelve una lista vacía | TEST-032 |
| TASK-008 | Complemento del «Resultado esperado»: la consulta no modifica datos | TEST-033 |
| TASK-009 | Préstamo válido (libro prestado, préstamo activo) | TEST-034 |
| TASK-009 | Libro inexistente | TEST-035 |
| TASK-009 | Libro ya prestado (RN-02) | TEST-036 |
| TASK-009 | Estudiante vacío | TEST-037 |
| TASK-009 | Fecha `None` | TEST-038 |
| TASK-009 | Fecha de ayer rechazada y fecha de hoy aceptada, con fecha simulada | TEST-039, TEST-040 |
| TASK-009 | Identificador con distinta mayúscula encuentra el libro | TEST-041 |
| TASK-009 | En los rechazos los datos y `guardar` no cambian | TEST-035–039, TEST-042 |
| TASK-009 | Complemento del «Resultado esperado»: orden de validación | TEST-043 |
| TASK-010 | Devolución válida (préstamo cerrado y conservado, libro disponible) | TEST-044 |
| TASK-010 | Libro inexistente | TEST-045 |
| TASK-010 | Libro no prestado | TEST-046 |
| TASK-010 | Tras devolver, el libro puede prestarse de nuevo | TEST-047 |
| TASK-010 | En los rechazos los datos y `guardar` no cambian | TEST-045, TEST-046, TEST-048 |
| TASK-010 | Complemento (RN-04): el préstamo está activo hasta su devolución | TEST-049 |
| TASK-011 | Préstamo con fecha pasada aparece | TEST-050 |
| TASK-011 | Préstamo con fecha de hoy o futura no aparece | TEST-051, TEST-052 |
| TASK-011 | Préstamo devuelto con fecha pasada no aparece | TEST-053 |
| TASK-011 | Sin vencidos devuelve una lista vacía | TEST-054 |
| TASK-011 | Varios vencidos se devuelven todos | TEST-055 |
| TASK-011 | Complemento del «Resultado esperado»: la consulta no modifica datos | TEST-056 |
| TASK-012 | `15/12/2026` es válida | TEST-057 |
| TASK-012 | `31/02/2026` devuelve `None` | TEST-058 |
| TASK-012 | `2026-12-15` devuelve `None` | TEST-059 |
| TASK-012 | `5/1/2026` devuelve `None` | TEST-060 |
| TASK-012 | Texto vacío devuelve `None` | TEST-061 |
| TASK-012 | Texto no numérico devuelve `None` | TEST-062 |
| TASK-012 | Ida y vuelta conserva la fecha | TEST-063 |
| TASK-012 | Complemento del «Resultado esperado»: fecha a texto con dos dígitos | TEST-064 |
| TASK-013 | Se muestran las seis opciones | TEST-065 |
| TASK-013 | Una opción válida invoca la operación y vuelve al menú | TEST-066 |
| TASK-013 | `9`, `abc` y vacío muestran aviso sin error | TEST-067–069 |
| TASK-013 | La opción de salir termina el ciclo | TEST-070 |
| TASK-014 | Registro exitoso: confirmación y el libro aparece en el servicio | TEST-071 |
| TASK-014 | Falta un dato: muestra cuál falta | TEST-072–074 |
| TASK-014 | Identificador repetido: muestra el motivo | TEST-075 |
| TASK-014 | En los rechazos los datos no cambian | TEST-072–075 |
| TASK-015 | Salida con un libro disponible y uno prestado (todos los campos, fecha en DD/MM/AAAA) | TEST-076, TEST-077 |
| TASK-015 | Catálogo vacío muestra el aviso | TEST-078 |
| TASK-016 | Préstamo exitoso con exactamente tres entradas consumidas | TEST-079 |
| TASK-016 | Fecha con formato inválido rechazada con motivo | TEST-080, TEST-084 |
| TASK-016 | Libro inexistente rechazado con motivo | TEST-082 |
| TASK-016 | Libro ya prestado rechazado con motivo | TEST-083 |
| TASK-016 | Estudiante vacío rechazado con motivo | TEST-081 |
| TASK-016 | En los rechazos los datos no cambian | TEST-080–084 |
| TASK-017 | Devolución exitosa con exactamente una entrada consumida | TEST-085 |
| TASK-017 | Libro inexistente rechazado con motivo | TEST-086 |
| TASK-017 | Libro no prestado rechazado con motivo | TEST-087 |
| TASK-017 | En los rechazos los datos no cambian | TEST-086, TEST-087 |
| TASK-018 | Salida con un vencido (libro, estudiante y fecha en DD/MM/AAAA) | TEST-088, TEST-091 |
| TASK-018 | Un préstamo devuelto no aparece | TEST-089 |
| TASK-018 | Sin vencidos muestra el aviso | TEST-090 |
| TASK-019 | Con archivo de datos corrupto el programa termina con código distinto de 0 y el archivo no cambia | TEST-092 |
| TASK-019 | El comando del README, desde la raíz, muestra el menú | TEST-093 |
| TASK-019 | El comando del README, desde otra carpeta, muestra el menú y usa el mismo archivo | TEST-094 |
| TASK-019 | Complemento del «Resultado esperado»: el README documenta inicio, ruta, Python 3.12 y respaldo | TEST-095 |
| TASK-020 | Registrar libros y un préstamo, reabrir con nuevas instancias y obtener datos idénticos | TEST-096, TEST-097 |
| TASK-020 | Tras un rechazo de libro repetido, el archivo es byte a byte el mismo | TEST-098 |
| TASK-020 | Tras un rechazo de préstamo de libro inexistente, el archivo es byte a byte el mismo | TEST-099 |
| TASK-020 | Tras un rechazo de préstamo de libro prestado, el archivo es byte a byte el mismo | TEST-100 |
| TASK-020 | Tras un rechazo de devolución de libro no prestado, el archivo es byte a byte el mismo | TEST-101 |
| TASK-021 | Flujo: registrar libro → préstamo → catálogo prestado → vencidos lo lista → segundo préstamo rechazado → devolución → catálogo disponible → vencidos vacío | TEST-102 |
| TASK-022 | El registro indica fecha, rol, tiempo de cada operación y resultado; el equipo lo revisa | TEST-105 |
| TASK-022 | Tiempo medido del préstamo y de la devolución (resultado esperado de la tarea) | TEST-103, TEST-104 |
