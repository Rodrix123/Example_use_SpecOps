# Especificación de requisitos — Gestor de préstamos de libros

| Campo | Valor |
|---|---|
| Versión | 1.0 |
| Fuente | [`docs/intent.md`](intent.md) v1.0 y Prompt 3.1 (Iroko, 2026, cap. 3.2) |
| Registro de la IA | [`agent/prompts/actividad-02-requisitos.md`](../agent/prompts/actividad-02-requisitos.md) |

## 1. Historias de usuario

### HU-001 — Registrar un libro

**Como** bibliotecario, **quiero** registrar un libro con su identificador, título y autor, **para**
tenerlo en el catálogo.

Criterios de aceptación:
1. Si ingreso identificador, título y autor, el libro queda registrado y en estado *disponible*.
2. Si falta alguno de los tres datos, el sistema rechaza el registro e indica el dato faltante.
3. Si el identificador ya existe, el sistema rechaza el registro (RN-01).

### HU-002 — Consultar el catálogo

**Como** bibliotecario, **quiero** ver los libros del catálogo con su estado, **para** saber cuáles
están disponibles y cuáles prestados.

Criterios de aceptación:
1. Se muestran todos los libros registrados con identificador, título, autor y estado
   (*disponible* / *prestado*).
2. Para cada libro prestado se muestra el estudiante y la fecha prevista de devolución.
3. Si no hay libros registrados, el sistema lo informa.

### HU-003 — Registrar un préstamo

**Como** bibliotecario, **quiero** registrar el préstamo de un libro a un estudiante con una fecha
prevista de devolución, **para** saber quién lo tiene y cuándo debe devolverlo.

Criterios de aceptación:
1. Si el libro existe y está disponible, e ingreso el estudiante y una fecha prevista de devolución
   válida, el préstamo queda registrado y el libro pasa a *prestado*.
2. Si el libro ya está prestado, el sistema rechaza el préstamo (RN-02).
3. Si el identificador del libro no existe, el sistema rechaza el préstamo.
4. Si falta el estudiante o la fecha no es válida, el sistema rechaza el préstamo.

### HU-004 — Registrar una devolución

**Como** bibliotecario, **quiero** registrar la devolución de un libro prestado, **para** que vuelva
a estar disponible.

Criterios de aceptación:
1. Si el libro está prestado, el préstamo se cierra y el libro pasa a *disponible*.
2. Si el libro no está prestado o no existe, el sistema rechaza la devolución.

### HU-005 — Consultar préstamos vencidos

**Como** bibliotecario, **quiero** ver los préstamos vencidos, **para** identificar los libros
atrasados sin revisar el registro manualmente.

Criterios de aceptación:
1. Se muestran exactamente los préstamos activos cuya fecha prevista de devolución es anterior a la
   fecha actual (RN-03), con libro, estudiante y fecha prevista.
2. Los préstamos devueltos no aparecen.
3. Si no hay préstamos vencidos, el sistema lo informa.

## 2. Reglas de negocio

| ID | Regla | Origen |
|---|---|---|
| RN-01 | El identificador de cada libro es único en el catálogo. | RES-05 |
| RN-02 | Un libro no puede tener más de un préstamo activo a la vez. | RES-07, OBJ-02 |
| RN-03 | Un préstamo está vencido si sigue activo y su fecha prevista de devolución es anterior a la fecha actual. | OBJ-03, CE-03 |
| RN-04 | Un préstamo está activo desde que se registra hasta que se registra su devolución. | CAP-03, CAP-04 |

## 3. Requisitos no funcionales

| ID | Requisito | Verificación | Origen |
|---|---|---|---|
| RNF-01 | La información del catálogo y de los préstamos se conserva entre ejecuciones. | Registrar datos, cerrar y reabrir: los datos son idénticos. | CAP-06, CE-05 |
| RNF-02 | Registrar un préstamo o una devolución toma menos de un minuto. | Prueba con un usuario sin capacitación previa. | CE-04 |
| RNF-03 | Ante una entrada rechazada, el sistema muestra el motivo y no modifica los datos. | Pruebas de los criterios de rechazo de HU-001 a HU-004. | OBJ-02, OBJ-04 |

## 4. Permisos

| ID | Permiso |
|---|---|
| PER-01 | El bibliotecario es el único usuario y puede realizar todas las operaciones, sin autenticación (RES-03). |

## 5. Restricciones

| ID | Restricción | Origen |
|---|---|---|
| RS-01 | Aplicación de consola. | RES-01 |
| RS-02 | Implementada en Python. | RES-02 |
| RS-03 | Sin interfaz gráfica ni integraciones externas; ejecución local. | RES-04 |
| RS-04 | Lo listado en la sección 6 de `docs/intent.md` queda fuera del alcance. | Intent §6 |

## 6. Trazabilidad

| Historia | Capacidad | Objetivo | Criterio de éxito | Reglas |
|---|---|---|---|---|
| HU-001 | CAP-01 | OBJ-04 | — | RN-01 |
| HU-002 | CAP-02 | OBJ-01 | CE-01 | — |
| HU-003 | CAP-03 | OBJ-02, OBJ-04 | CE-02, CE-04 | RN-02, RN-04 |
| HU-004 | CAP-04 | OBJ-01, OBJ-04 | CE-04 | RN-04 |
| HU-005 | CAP-05 | OBJ-03 | CE-03 | RN-03 |
| RNF-01 | CAP-06 | OBJ-04 | CE-05 | — |
