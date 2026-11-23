# Engineering Intent Document — Gestor de préstamos de libros

| Campo | Valor |
|---|---|
| Versión | 1.0 |
| Estado | Aprobado para pasar a requisitos (Actividad 2) |
| Fuente | Condiciones iniciales del taller y Prompts 2.1–2.4 (Iroko, 2026, cap. 2) |
| Registro de la IA | [`agent/prompts/actividad-01-intent.md`](../agent/prompts/actividad-01-intent.md) |

## 1. Nombre del proyecto

**Gestor de préstamos de libros** (BiblioPréstamos).

## 2. Problema

El bibliotecario de una pequeña biblioteca universitaria lleva el catálogo y los préstamos en hojas
de cálculo. Con ese registro manual le resulta difícil saber qué ejemplares están disponibles,
cuáles están prestados y qué préstamos están vencidos. Como consecuencia, puede prestar un ejemplar
que ya está prestado, tarda en responder a los estudiantes y no detecta a tiempo los préstamos
atrasados.

El sistema debe ofrecer un registro único del catálogo y de los préstamos que muestre en todo
momento el estado de cada ejemplar.

## 3. Usuarios

| Tipo | Descripción |
|---|---|
| Usuario principal (único) | **Bibliotecario.** Registra libros, presta, recibe devoluciones y consulta el estado del catálogo. |
| Personas afectadas (no usuarios) | **Estudiantes.** Reciben los préstamos; sus datos se registran, pero no usan la aplicación. |

## 4. Objetivos

| ID | Objetivo (resultado esperado) |
|---|---|
| OBJ-01 | El bibliotecario conoce de inmediato si un ejemplar está disponible o prestado, y a quién. |
| OBJ-02 | Ningún ejemplar queda prestado a dos estudiantes al mismo tiempo. |
| OBJ-03 | El bibliotecario identifica sin revisión manual los préstamos vencidos. |
| OBJ-04 | El registro de préstamos y devoluciones deja de depender de hojas de cálculo. |

## 5. Capacidades principales (primera versión)

| ID | Capacidad | Objetivos |
|---|---|---|
| CAP-01 | Registrar libros del catálogo (identificador, título, autor). | OBJ-04 |
| CAP-02 | Consultar el catálogo con el estado de cada ejemplar (disponible / prestado). | OBJ-01 |
| CAP-03 | Registrar un préstamo de un ejemplar disponible a un estudiante, con fecha prevista de devolución. | OBJ-02, OBJ-04 |
| CAP-04 | Registrar la devolución de un ejemplar prestado. | OBJ-01, OBJ-04 |
| CAP-05 | Consultar los préstamos vencidos. | OBJ-03 |
| CAP-06 | Conservar la información entre ejecuciones de la aplicación. | OBJ-04 |

## 6. Fuera del alcance (primera versión)

- Autenticación, usuarios y roles.
- Interfaz gráfica o web.
- Integraciones externas (correo, sistemas académicos, servicios en línea).
- Notificaciones o recordatorios a estudiantes.
- Multas o sanciones por retraso.
- Renovación de préstamos y reservas.
- Límite de préstamos activos por estudiante.
- Registro y administración de estudiantes como catálogo independiente.
- Reportes y estadísticas.
- Importación de las hojas de cálculo existentes.
- Uso simultáneo por varios usuarios.

## 7. Restricciones

| ID | Restricción |
|---|---|
| RES-01 | Aplicación de consola. |
| RES-02 | Lenguaje: Python|
| RES-03 | Un único usuario (bibliotecario), sin autenticación. |
| RES-04 | Sin interfaz gráfica ni integración externa; ejecución local. |
| RES-05 | Cada libro tiene identificador, título y autor. |
| RES-06 | Cada préstamo se asocia a un estudiante y a una fecha prevista de devolución. |
| RES-07 | Un ejemplar no puede prestarse simultáneamente a dos estudiantes. |
| RES-08 | Desarrollo con IA siguiendo el ciclo SDD: una fase a la vez y revisada antes de avanzar. |


## 8. Criterios de éxito

| ID | Criterio | Objetivo |
|---|---|---|
| CE-01 | Con una sola consulta el bibliotecario ve si un ejemplar está disponible o prestado y, si está prestado, a qué estudiante y con qué fecha prevista de devolución. | OBJ-01 |
| CE-02 | El sistema rechaza el 100 % de los intentos de prestar un ejemplar que ya está prestado. | OBJ-02 |
| CE-03 | La consulta de vencidos muestra exactamente los préstamos no devueltos con fecha prevista anterior a la fecha actual. | OBJ-03 |
| CE-04 | Registrar un préstamo o una devolución toma menos de un minuto para un bibliotecario sin capacitación previa. | OBJ-04 |
| CE-05 | Tras cerrar y volver a abrir la aplicación, el catálogo y los préstamos se conservan sin cambios. | OBJ-04 |
