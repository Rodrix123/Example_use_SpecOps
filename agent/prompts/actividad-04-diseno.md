# Actividad 4 — Registro de interacción con la IA

Referencia: Iroko (2026), cap. 3, sección 3.4. El taller no asigna un prompt del libro a esta
actividad; el diseño se generó con el flujo de OpenSpec (esquema `spec-driven`).
Entrada: cambio de OpenSpec `gestor-prestamos-v1` —
[`proposal.md`](../../openspec/changes/gestor-prestamos-v1/proposal.md) y specs
[`catalogo`](../../openspec/changes/gestor-prestamos-v1/specs/catalogo/spec.md),
[`prestamos`](../../openspec/changes/gestor-prestamos-v1/specs/prestamos/spec.md) y
[`datos`](../../openspec/changes/gestor-prestamos-v1/specs/datos/spec.md), derivados sin cambios de
`docs/intent.md`, `docs/requirements.md` y `docs/product-spec.md`.
Artefacto resultante: [`openspec/changes/gestor-prestamos-v1/design.md`](../../openspec/changes/gestor-prestamos-v1/design.md)

## Cómo se creó `design.md`

1. **Paso intermedio (antes de la fase 4).** Los documentos aprobados de las actividades 1 a 3 se
   trasladaron al formato de OpenSpec en el cambio `gestor-prestamos-v1`: `proposal.md` (por qué y
   qué) y tres specs con requisitos `Requirement` y escenarios `WHEN/THEN`. Cada requisito lleva su
   identificador (HU, RN, RNF). Los documentos originales de `docs/` no se modificaron. Se validó
   con `openspec validate gestor-prestamos-v1 --strict`.
2. **Habilitar la creación de un artefacto por vez.** Con `openspec config profile` se activó el
   flujo `continue`, que crea solo el siguiente artefacto pendiente del cambio. Así se respeta la
   regla del taller de completar y revisar una fase antes de avanzar.
3. **Generar el diseño.** Se ejecutó en Claude Code el skill de OpenSpec:

   ```text
   /openspec-continue-change gestor-prestamos-v1
   ```

   El skill consulta el estado del cambio (`openspec status`), detecta que el siguiente artefacto
   es `design`, obtiene su plantilla e instrucciones (`openspec instructions design`), lee
   `proposal.md` y las specs, y escribe `design.md`. Se detiene ahí: no genera `tasks.md`
   (fase 5) hasta que se vuelva a ejecutar.
4. **Plantilla usada por OpenSpec.** `design.md` sigue las secciones del esquema `spec-driven`:
   *Context*, *Goals / Non-Goals*, *Decisions* (con justificación y alternativa descartada) y
   *Risks / Trade-offs*, más *Open Questions*.
5. **Revisión del equipo.** Ver la sección siguiente. Las correcciones se aplican con
   `/openspec-update-change gestor-prestamos-v1 "<corrección>"`, que mantiene coherentes el diseño
   y los demás artefactos del cambio.

## Contenido del diseño generado

| Exigencia de la Actividad 4 | Dónde está en `design.md` |
|---|---|
| Componentes o clases y responsabilidades | Decisión 1 (`modelos`, `servicio`, `almacen`, `consola`) |
| Modelo de datos | Decisiones 2 y 3 (archivo JSON con `libros` y `prestamos`; estado derivado) |
| Reglas de validación | Decisiones 5 y 7 (fecha válida, orden de validación por CU) |
| Manejo de errores | Decisión 7 (errores de negocio con motivo, sin modificar datos) y *Risks* (archivo corrupto) |
| Decisiones justificadas | Cada decisión indica su motivo y la alternativa descartada |
| Trazabilidad | Decisión 9 (requisito → decisión) |

Decisiones que la Actividad 2 o la 3 habían diferido a esta fase: formato de fecha (Decisión 4) y
menú de consola (Decisión 8).

## Revisión crítica (pendiente de completar por el equipo)

| Punto del diseño | Observación | Decisión |
|---|---|---|
| Decisión 5 (c): la fecha prevista no puede ser anterior a hoy. | En la Actividad 2 se **rechazó** esta regla por no estar en el negocio; los requisitos solo dicen "fecha válida". El diseño la reintroduce como definición técnica de "válida". | Pendiente |
| Non-Goal: consulta de libros disponibles (CU-002, flujo 1b). | Coherente: el flujo 1b no tiene HU ni spec que lo respalde. Si el equipo lo incluye, primero debe actualizar `requirements.md` y las specs. | Pendiente |
| Decisión 2: almacenamiento en JSON con escritura atómica. | Cumple RNF-01 y RNF-03 sin dependencias externas (RS-03). | Pendiente |
| Decisión 3: no se guarda la fecha real de devolución. | Coherente con la Actividad 2, que rechazó ese dato. | Pendiente |
| *Context*: Windows y Python 3.14.4. | Dato del entorno de desarrollo, no un requisito; ver *Open Questions* (versión mínima). | Pendiente |
| *Open Questions*: mayúsculas en el identificador, versión mínima de Python, ruta del archivo de datos. | Deben resolverse antes de planificar tareas (Actividad 5). | Pendiente |

**Verificación a realizar:** cada requisito de las specs (HU-001 a HU-005, RN-01 a RN-04, RNF-01 a
RNF-03) aparece en la tabla de trazabilidad de la Decisión 9, y ninguna decisión agrega
funcionalidades excluidas en `docs/intent.md` §6 o `docs/product-spec.md` §4.
