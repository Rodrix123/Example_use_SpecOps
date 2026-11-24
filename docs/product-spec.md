# Especificación del producto — Gestor de préstamos de libros

| Campo | Valor |
|---|---|
| Versión | 1.0 |
| Fuente | [`docs/requirements.md`](requirements.md) v1.0 (Iroko, 2026, cap. 3.3) |
| Registro de la IA | [`agent/prompts/actividad-03-producto.md`](../agent/prompts/actividad-03-producto.md) |

## 1. Rol de usuario

| Actor | Objetivo general |
|---|---|
| Bibliotecario | Mantener el catálogo y saber en todo momento qué libros están disponibles, prestados o vencidos (PER-01). |

## 2. Casos de uso

### CU-001 — Registrar libro

| Campo | Contenido |
|---|---|
| Actor principal | Bibliotecario |
| Objetivo | Incorporar un libro al catálogo. |
| Precondiciones | Ninguna. |
| Postcondiciones | El libro queda registrado en estado *disponible* y se conserva entre ejecuciones (RNF-01). |
| Historias relacionadas | HU-001 |

**Flujo principal**
1. El bibliotecario indica que desea registrar un libro.
2. El sistema solicita identificador, título y autor.
3. El bibliotecario ingresa los tres datos.
4. El sistema valida que estén completos y que el identificador no exista (RN-01).
5. El sistema registra el libro como *disponible* y confirma el registro.

**Excepciones**
- 4a. Falta un dato: el sistema indica cuál falta y no registra el libro (RNF-03).
- 4b. El identificador ya existe: el sistema rechaza el registro y no modifica el catálogo (RNF-03).

### CU-002 — Consultar ejemplares

| Campo | Contenido |
|---|---|
| Actor principal | Bibliotecario |
| Objetivo | Conocer el estado de los libros y detectar los préstamos vencidos. |
| Precondiciones | Ninguna. |
| Postcondiciones | No se modifica ningún dato. |
| Historias relacionadas | HU-002, HU-005 |

**Flujo principal (catálogo)**
1. El bibliotecario indica que desea consultar el catálogo.
2. El sistema muestra todos los libros con identificador, título, autor y estado
   (*disponible* / *prestado*).

**Flujo alternativo**
- 1a. El bibliotecario indica que desea consultar los préstamos vencidos:
  1. El sistema muestra los préstamos activos con fecha prevista anterior a la fecha actual
     (RN-03), con libro, estudiante y fecha prevista.
  2. Los préstamos devueltos no se muestran.

- 1b. El bibliotecario indica que desea consultar los libros dsponibles:
  1. El sistema muestra los préstamos activos con fecha prevista anterior a la fecha actual
     (RN-03)
  

**Excepciones**
- 2a. No hay libros registrados: el sistema lo informa.
- 1a.1a. No hay préstamos vencidos: el sistema lo informa.
- 1a.1a. No hay libros disponibles, el sistema lo informa.

### CU-003 — Prestar libro

| Campo | Contenido |
|---|---|
| Actor principal | Bibliotecario |
| Objetivo | Registrar que un estudiante se lleva un libro y cuándo debe devolverlo. |
| Precondiciones | El libro está registrado en el catálogo. |
| Postcondiciones | Existe un préstamo activo (RN-04) del libro al estudiante; el libro queda *prestado*; los datos se conservan (RNF-01). |
| Historias relacionadas | HU-003 |

**Flujo principal**
1. El bibliotecario indica que desea registrar un préstamo.
2. El sistema solicita el identificador del libro, el estudiante y la fecha prevista de devolución.
3. El bibliotecario ingresa los datos.
4. El sistema verifica que el libro exista y esté *disponible* (RN-02), que el estudiante esté
   indicado y que la fecha sea válida.
5. El sistema registra el préstamo, marca el libro como *prestado* y confirma el registro.

**Excepciones**
- 4a. El libro no existe: el sistema rechaza el préstamo.
- 4b. El libro ya está prestado: el sistema rechaza el préstamo (RN-02).
- 4c. Falta el estudiante o la fecha no es válida: el sistema rechaza el préstamo.
- En todas las excepciones el sistema muestra el motivo y no modifica los datos (RNF-03).

### CU-004 — Devolver libro

| Campo | Contenido |
|---|---|
| Actor principal | Bibliotecario |
| Objetivo | Registrar que un libro prestado volvió a la biblioteca. |
| Precondiciones | El libro está registrado y tiene un préstamo activo. |
| Postcondiciones | El préstamo deja de estar activo (RN-04); el libro queda *disponible*; los datos se conservan (RNF-01). |
| Historias relacionadas | HU-004 |

**Flujo principal**
1. El bibliotecario indica que desea registrar una devolución.
2. El sistema solicita el identificador del libro.
3. El bibliotecario ingresa el identificador.
4. El sistema verifica que el libro exista y esté *prestado*.
5. El sistema cierra el préstamo, marca el libro como *disponible* y confirma la devolución.

**Excepciones**
- 4a. El libro no existe o no está prestado: el sistema rechaza la devolución, muestra el motivo y
  no modifica los datos (RNF-03).

## 3. Correspondencia historias – casos de uso

| Historia | Caso de uso |
|---|---|
| HU-001 | CU-001 |
| HU-002 | CU-002 (flujo principal) |
| HU-003 | CU-003 |
| HU-004 | CU-004 |
| HU-005 | CU-002 (flujo alternativo 1a) |

## 4. Funcionalidades excluidas de la primera versión

Se mantienen las exclusiones de `docs/intent.md` §6. En particular, los casos de uso **no** incluyen:

- Editar o eliminar libros.
- Buscar libros por título o autor.
- Registrar o consultar estudiantes de forma independiente.
- Renovar, reservar o limitar préstamos por estudiante.
- Multas, notificaciones, reportes, autenticación o interfaz gráfica.
