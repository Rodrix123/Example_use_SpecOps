# Actividad 1 — Registro de interacción con la IA

Referencia: Iroko (2026), cap. 2, secciones 2.1–2.7. Prompts 2.1, 2.2, 2.3 y 2.4.
Artefacto resultante: [`docs/intent.md`](../../docs/intent.md)

Este registro guarda, para cada prompt, el texto enviado, un resumen de la respuesta de la IA y la
revisión crítica del equipo (qué se aceptó, qué se corrigió y qué se rechazó).

---

## Prompt 2.1 — Clarify a raw idea

**Prompt enviado**

```text
You are helping me clarify a raw software idea before writing requirements.
Idea: Una pequeña biblioteca universitaria administra manualmente el préstamo de libros a
estudiantes mediante hojas de cálculo. Esto dificulta conocer qué ejemplares están disponibles,
cuáles están prestados y qué préstamos están vencidos. Se desea una aplicación sencilla para
administrar el catálogo y registrar préstamos y devoluciones.
Ask me the smallest set of questions needed to identify the problem, users, goals, constraints,
and scope boundaries. Do not design the solution yet.
```

**Respuesta de la IA (preguntas) y respuestas del equipo**

| # | Pregunta de la IA | Respuesta (fuente) |
|---|---|---|
| P1 | ¿Quién usará la aplicación? ¿Los estudiantes también la usan? | Solo el bibliotecario. Los estudiantes no interactúan con el sistema (condiciones del taller). |
| P2 | ¿Un "libro" es un título o un ejemplar físico? ¿Puede haber varios ejemplares del mismo título? | **No definido en el enunciado.** Decisión del equipo para v1: cada libro registrado representa un ejemplar físico con identificador único. Dos ejemplares del mismo título se registran como dos libros con identificadores distintos. |
| P3 | ¿Qué datos del libro se registran? | Identificador, título y autor (condiciones del taller). |
| P4 | ¿Cómo se identifica al estudiante? ¿Existe un registro de estudiantes? | **No definido.** Decisión v1: el estudiante se identifica por un código (p. ej. carné) y su nombre, capturados al registrar el préstamo. No se administra un registro de estudiantes aparte. |
| P5 | ¿Qué significa "préstamo vencido"? | Préstamo no devuelto cuya fecha prevista de devolución es anterior a la fecha actual. |
| P6 | ¿Qué incluye "administrar el catálogo"? ¿Registrar, editar, eliminar? | **No definido.** Decisión v1: registrar y consultar libros. Editar y dar de baja quedan como pregunta abierta para la Actividad 2. |
| P7 | ¿La información debe conservarse al cerrar la aplicación? | No se menciona, pero el problema actual es llevar el registro; si los datos se pierden al cerrar, la aplicación no reemplaza a la hoja de cálculo. Decisión: los datos deben conservarse entre ejecuciones. |
| P8 | ¿Hay multas, renovaciones, reservas o límite de préstamos por estudiante? | No forman parte de las condiciones iniciales; quedan fuera de la v1. |
| P9 | ¿Restricciones técnicas? | Consola; Python o Java; sin autenticación, interfaz gráfica ni integración externa (condiciones del taller). |

**Revisión crítica**

- Útil: P2, P4, P6 y P7 revelaron ambigüedades reales del enunciado que dos desarrolladores
  resolverían de forma distinta (prueba de ambigüedad, sección 2.6).
- Las respuestas a P2, P4, P6 y P7 son **decisiones del equipo**, no hechos del enunciado; se
  marcan como supuestos en `docs/intent.md` para validarlas con el docente/cliente.

---

## Prompt 2.2 — Improve a problem statement

**Prompt enviado**

```text
Rewrite this vague software request as a clear problem statement.
Request: "Queremos una aplicación para gestionar los préstamos de libros de la biblioteca."
Use this structure: affected user, current difficulty, consequence, desired improvement. Keep it
specific and do not invent features.
```

**Respuesta de la IA**

> El bibliotecario de una pequeña biblioteca universitaria registra el catálogo y los préstamos en
> hojas de cálculo. Con este registro manual le resulta difícil saber qué ejemplares están
> disponibles, cuáles están prestados y qué préstamos están vencidos. Como consecuencia, puede
> prestar un ejemplar que ya está prestado, tarda en responder a los estudiantes y no detecta a
> tiempo los préstamos atrasados. El sistema debe ofrecer un registro único del catálogo y de los
> préstamos que muestre en todo momento el estado de cada ejemplar.

**Revisión crítica**

- Aceptado con una corrección: la primera versión de la respuesta decía "pérdida de libros". Se
  eliminó porque el enunciado no lo menciona; es una consecuencia inventada.
- Se verificó que no aparecen funcionalidades (el prompt pide no inventarlas).

---

## Prompt 2.3 — Translate business need into software direction

**Prompt enviado**

```text
Convert this business need into software direction.
Business need: La biblioteca necesita saber en todo momento qué ejemplares están disponibles,
cuáles están prestados y qué préstamos están vencidos, y evitar que un ejemplar se preste a dos
estudiantes a la vez.
Return: primary users, main capabilities, key data, quality expectations, and what should be
excluded from the first version.
```

**Respuesta de la IA (resumen) y decisión del equipo**

| Propuesta de la IA | Decisión | Justificación |
|---|---|---|
| Usuario principal: bibliotecario | Aceptada | Coincide con el enunciado. |
| Usuario secundario: estudiantes que consultan disponibilidad | **Rechazada** | El enunciado indica un solo usuario (bibliotecario). |
| Registrar y consultar libros | Aceptada | "Administrar el catálogo". |
| Registrar préstamo con fecha prevista de devolución | Aceptada | Condición del taller. |
| Registrar devolución | Aceptada | Condición del taller. |
| Consultar estado/disponibilidad de los libros | Aceptada | Es el problema central. |
| Listar préstamos vencidos | Aceptada | Es el problema central. |
| Búsqueda por título o autor | **Diferida** | No pedida; se puede proponer en la Actividad 2 si un requisito la necesita. |
| Cálculo de multas por retraso | **Rechazada** | No está en el problema; aumenta el alcance. |
| Notificaciones por correo a estudiantes | **Rechazada** | Implica integración externa, excluida explícitamente. |
| Renovación de préstamos y reservas | **Rechazada** | Fuera de las condiciones iniciales. |
| Reportes y estadísticas de uso | **Rechazada** | No responde al problema planteado. |
| Importar las hojas de cálculo existentes | **Rechazada** | No solicitado; se anota como posible evolución. |
| Datos clave: libro (id, título, autor), préstamo (libro, estudiante, fecha de préstamo, fecha prevista, fecha de devolución) | Aceptada | La "fecha de préstamo" y la "fecha de devolución real" no están en el enunciado, pero se necesitan para registrar la devolución y el historial; se confirmarán en requisitos. |
| Usar SQLite como almacenamiento | **Rechazada en esta fase** | Es una decisión de implementación (sección 2.2); se decide en el diseño técnico (Actividad 4). |
| Calidad: operaciones rápidas, mensajes claros, validación de entradas | Aceptada | Se reflejan en los criterios de éxito. |

**Lección registrada:** la IA tiende a ampliar el alcance (multas, notificaciones, reportes) y a
adelantar decisiones técnicas (SQLite). Se aplicó la regla del taller: no aceptar automáticamente
características adicionales.

---

## Prompt 2.4 — Create an Engineering Intent Document

**Prompt enviado**

```text
Use the information below to draft an Engineering Intent Document.
Project idea: Aplicación de consola para administrar el catálogo y registrar préstamos y
devoluciones de libros en una pequeña biblioteca universitaria.
Known users: Bibliotecario (único usuario). Los estudiantes son los prestatarios, no usuarios.
Known business need: [problem statement aprobado del Prompt 2.2]
Known constraints: consola; Python o Java; sin autenticación, interfaz gráfica ni integración
externa; un ejemplar no puede prestarse a dos estudiantes a la vez; cada libro tiene id, título y
autor; cada préstamo tiene estudiante y fecha prevista de devolución.
Return a concise document with: problem statement, users, goals, core capabilities, out of scope,
constraints, risks, and success criteria.
```

**Revisión crítica del borrador**

- Se reescribieron los objetivos que estaban redactados como funcionalidades ("permitir registrar
  préstamos") para expresarlos como resultados (sección 2.4: un objetivo no es una funcionalidad).
- Se volvieron medibles los criterios de éxito (el borrador decía "el sistema es fácil de usar").
- Se agregó la sección de supuestos y preguntas abiertas para no ocultar las decisiones de P2, P4,
  P6 y P7.
- Se añadió explícitamente "límite de préstamos por estudiante" a las exclusiones para que el
  alcance de la v1 quede claro.

Versión aprobada: [`docs/intent.md`](../../docs/intent.md).
