# INSTRUCCIONES PARA EL ASISTENTE DE IA

Plantilla base: Iroko (2026), sección 4.7. Revisada con el Prompt 4.3
(ver [`agent/prompts/actividad-00-agent.md`](agent/prompts/actividad-00-agent.md)).

## 1. Objetivo del proyecto

Aplicación de consola en Python para que el bibliotecario de una pequeña biblioteca universitaria
registre libros (identificador, título, autor), consulte el catálogo con el estado de cada libro,
registre préstamos a estudiantes con fecha prevista de devolución, registre devoluciones y consulte
los préstamos vencidos. Un libro no puede prestarse a dos estudiantes a la vez.
Fuente de verdad: [`docs/intent.md`](docs/intent.md).

## 2. Fase actual

| Fase (actividad del taller) | Artefacto | Estado |
|---|---|---|
| 1. Intención de ingeniería | `docs/intent.md` | Aprobado |
| 2. Requisitos | `docs/requirements.md` | Aprobado |
| 3. Especificación del producto | `docs/product-spec.md` | **Siguiente** |
| 4. Diseño técnico | `docs/technical-spec.md` | Pendiente |
| 5. Planificación de tareas | `tasks/` | Pendiente |
| 6. Planificación de pruebas | `tests/test-plan.md` | Pendiente |
| 7. Implementación controlada | `src/`, `tests/` | Pendiente |
| 8. Revisión y entrega | `review/` | Pendiente |
| 9. Mantenimiento | artefactos afectados | Pendiente |

Trabaja solo en la fase actual. No adelantes artefactos de fases posteriores.
Actualiza esta tabla cuando el equipo apruebe una fase.

## 3. Carpetas

- `docs/`: intención, requisitos, especificaciones y trazabilidad.
- `tasks/`: tareas de implementación (`TASK-NNN.md`) e índice de tareas.
- `tests/`: planes, casos de prueba y pruebas automatizadas.
- `src/`: código fuente de la aplicación.
- `review/`: resultados de revisiones y registro de cambios.
- `agent/`: prompts usados con la IA (`agent/prompts/actividad-NN-*.md`).
- `ops/`: mantenimiento y operación.

No crees archivos fuera de estas carpetas, salvo `README.md` y `CLAUDE.md` en la raíz.

## 4. Convenciones de identificadores

| Prefijo | Elemento | Archivo |
|---|---|---|
| OBJ, CAP, RES, CE | Objetivo, capacidad, restricción, criterio de éxito | `docs/intent.md` |
| HU-NNN | Historia de usuario | `docs/requirements.md` |
| RN, RNF, PER, RS | Regla de negocio, req. no funcional, permiso, restricción | `docs/requirements.md` |
| CU-NNN | Caso de uso | `docs/product-spec.md` |
| TASK-NNN | Tarea de implementación | `tasks/` |
| TEST-NNN | Prueba | `tests/` |

Usa tres dígitos (HU-001). No reutilices ni renumeres identificadores existentes: si un elemento
se elimina, su identificador queda retirado.

## 5. Reglas

1. **Alcance.** No agregues funcionalidades, datos, reglas ni cifras que no estén en `docs/intent.md`
   o `docs/requirements.md`. Lo excluido en la sección 6 del intent no se construye.
2. **Supuestos.** Si algo no está especificado, no lo decidas tú: pregúntalo o márcalo como
   pregunta abierta. Pregunta siempre antes de supuestos que afecten alcance, datos o arquitectura.
3. **Una fase a la vez.** No construyas la aplicación completa con una sola respuesta.
4. **Una tarea a la vez** (desde la fase 7). Implementa solo la `TASK` indicada y modifica solo los
   archivos que esa tarea permite. No refactorices ni cambies archivos no relacionados.
5. **Especificación antes que código.** Si un cambio altera el comportamiento, actualiza primero
   los artefactos de `docs/` y después el código (fase 9).
6. **Sin decisiones técnicas prematuras.** No elijas almacenamiento, librerías ni estructura de
   clases antes de la fase 4.
7. **Trazabilidad.** Todo artefacto y todo cambio de código debe citar los identificadores de los
   que deriva (HU, RN, CU, TASK, TEST).
8. **Pruebas.** Cada tarea debe tener pruebas definidas en `tests/` antes de implementarse. No des una
   tarea por terminada si sus pruebas no se ejecutaron y pasaron; reporta el resultado real.
9. **Restricciones técnicas.** Python, consola, ejecución local, sin interfaz gráfica, sin
   autenticación, sin integraciones externas ni dependencias de red.
10. **Git.** No hagas commits, cambios de rama ni push sin aprobación del equipo.
11. **Idioma.** Escribe los artefactos en español, breves y verificables.

## 6. Formato de respuesta

- Resumen de cambios
- Archivos afectados
- Identificadores cubiertos (HU, RN, CU, TASK, TEST)
- Pruebas o verificaciones a ejecutar y su resultado
- Supuestos, preguntas abiertas y riesgos
