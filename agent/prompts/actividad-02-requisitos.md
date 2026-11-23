# Actividad 2 — Registro de interacción con la IA

Referencia: Iroko (2026), cap. 3, sección 3.2. Prompt 3.1.
Entrada: [`docs/intent.md`](../../docs/intent.md) v1.0 (versión ajustada por el equipo).
Artefacto resultante: [`docs/requirements.md`](../../docs/requirements.md)

## Prompt 3.1 — Draft requirements from intent (completado según el taller)

```text
Use this Engineering Intent Document to draft clear software requirements.
Intent: [contenido de docs/intent.md]
Return functional requirements, non-functional requirements, business rules, permissions,
constraints, and acceptance criteria. Do not choose implementation tools yet.

Instrucciones adicionales:
- Expresa los requisitos funcionales como historias de usuario con identificador (HU-001, HU-002…)
  y criterios de aceptación verificables.
- Expresa requisitos no funcionales, reglas de negocio, permisos y restricciones como
  declaraciones explícitas con identificador; no los fuerces al formato de historia de usuario.
- Cada requisito debe derivarse de una capacidad, objetivo, restricción o criterio de éxito del
  intent. No agregues funcionalidades que no estén en el intent.
- Sé breve: una historia por capacidad, criterios cortos.
```

## Revisión crítica de la respuesta

| Propuesta de la IA | Decisión | Justificación |
|---|---|---|
| HU-001 a HU-005, una por cada capacidad CAP-01 a CAP-05 | Aceptada | Correspondencia directa con el intent. |
| CAP-06 (conservar información) como historia de usuario | **Corregida** → RNF-01 | Es una cualidad del sistema, no una acción del bibliotecario. |
| HU "Buscar libro por título o autor" | **Rechazada** | No está en las capacidades del intent. |
| HU "Editar / eliminar libro" | **Rechazada** | El intent solo pide registrar y consultar (CAP-01, CAP-02). |
| HU "Registrar estudiante" | **Rechazada** | El registro de estudiantes está excluido (intent §6). |
| Datos del estudiante: código, nombre, correo, carrera | **Reducida** a "el estudiante" | El enunciado solo dice que el préstamo se asocia a un estudiante; los campos concretos se fijan en el diseño técnico. |
| Registrar fecha de préstamo y fecha real de devolución | **Rechazada** | No la exige ninguna capacidad ni regla; el vencimiento solo depende de la fecha prevista (RN-03). |
| Regla "la fecha prevista no puede ser anterior a hoy" | **Rechazada** | No está especificada en el negocio; se deja solo "fecha válida". |
| Formato de fecha AAAA-MM-DD | **Diferida** | Decisión de diseño (Actividad 4). |
| RNF "Almacenar los datos en JSON/SQLite" | **Rechazada** | Herramienta de implementación; el prompt pide no elegirlas. Se mantiene solo la necesidad (RNF-01). |
| RNF "tiempo de respuesta < 1 s" y "soporte de 10 000 libros" | **Rechazadas** | Cifras inventadas; no provienen del intent. Se conserva CE-04 como RNF-02. |
| RNF "Registro de auditoría de operaciones" | **Rechazada** | No solicitado. |
| Duplicación: "el libro prestado no puede prestarse" aparecía como HU y como regla | **Corregida** | Queda como RN-02 y el criterio de HU-003 la referencia. |

**Lección registrada:** aun con la instrucción de no agregar funcionalidades, la IA propuso
búsqueda, edición, registro de estudiantes, cifras de rendimiento y tecnologías de almacenamiento.
Se contrastó cada propuesta con una capacidad, objetivo o criterio del intent; lo que no tenía
origen se eliminó.
