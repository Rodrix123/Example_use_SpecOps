# Actividad 0 — Instrucciones del asistente (CLAUDE.md)

Referencia: Iroko (2026), sección 4.7 (plantilla) y Prompt 4.3.
Artefacto resultante: [`CLAUDE.md`](../../CLAUDE.md) (raíz del proyecto)

## Punto de partida

Plantilla "AGENT.md starter template" de la sección 4.7, completada con el objetivo del proyecto y
la lista de carpetas exigida por el taller.

## Prompt 4.3 — Improve an agent instruction file

```text
Review this agent instruction file for a beginner spec-driven AI engineering project.
Instruction file: [plantilla 4.7 completada]
Find vague rules, missing boundaries, missing test expectations, and anything that could allow
the assistant to make uncontrolled changes. Return a cleaner version.
```

## Revisión crítica

| Hallazgo / propuesta de la IA | Decisión | Cambio en CLAUDE.md |
|---|---|---|
| "Follow the current task only" es vago antes de la fase 7 (aún no hay tareas). | Aceptado | Se separa "una fase a la vez" (regla 3) de "una tarea a la vez" (regla 4) y se agrega la tabla de fases. |
| Falta definir qué es "funcionalidad no solicitada". | Aceptado | Regla 1: la referencia son `docs/intent.md` y `docs/requirements.md`, y lo excluido en el intent §6. |
| Faltan carpetas `agent/` y `ops/` en la plantilla. | Aceptado | Sección 3 con las siete carpetas del taller. |
| Faltan expectativas de prueba. | Aceptado | Regla 8: pruebas definidas antes de implementar y resultado real reportado. |
| No hay convenciones de identificadores. | Aceptado | Sección 4 (HU, CU, TASK, TEST y los ya usados en intent y requisitos). |
| Nada impide commits o cambios de rama automáticos. | Aceptado | Regla 10. |
| Falta la regla de mantenimiento "especificación antes que código". | Aceptado | Regla 5 (Actividad 9 del taller). |
| Agregar reglas de estilo de código (PEP 8, type hints, docstrings) y cobertura mínima del 80 %. | **Diferido** | Son decisiones de diseño técnico (fase 4); la cifra de cobertura no proviene del taller. |
| Agregar reglas de seguridad (sanitización, cifrado de datos). | **Rechazado** | Sin autenticación ni red; no hay requisito que lo justifique. |
| Exigir que la IA genere automáticamente diagramas UML. | **Rechazado** | El taller indica que no se exige UML. |
| Extender el archivo con ejemplos de prompts por fase. | **Rechazado** | La sección 4.7 recomienda un archivo corto; los prompts se guardan en `agent/prompts/`. |
