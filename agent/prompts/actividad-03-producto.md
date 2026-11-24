# Actividad 3 — Registro de interacción con la IA

Referencia: Iroko (2026), cap. 3, sección 3.3. El taller no asigna un prompt del libro a esta
actividad; se redactó uno a partir de la sección 3.3 y de las indicaciones del taller.
Entrada: [`docs/requirements.md`](../../docs/requirements.md) v1.0.
Artefacto resultante: [`docs/product-spec.md`](../../docs/product-spec.md)

## Prompt enviado

```text
A partir de estas historias de usuario aprobadas, identifica los principales casos de uso del
sistema, en particular consulta, préstamo y devolución de ejemplares.
Requisitos: [contenido de docs/requirements.md]
Represéntalos como casos de uso textuales simplificados (sin UML). Cada caso debe tener:
identificador (CU-001…) y nombre, actor principal y objetivo, precondiciones y postcondiciones,
flujo principal con pasos numerados, flujos alternativos y excepciones, historias relacionadas.
No supongas una correspondencia uno a uno entre historias y casos de uso.
No agregues comportamientos, datos ni reglas que no estén en los requisitos.
Incluye la lista de funcionalidades excluidas de la primera versión.
```

## Revisión crítica

| Propuesta de la IA | Decisión | Justificación |
|---|---|---|
| Un caso de uso por historia (5 casos). | **Corregida** → 4 casos | HU-002 y HU-005 son dos consultas del mismo objetivo; se unieron en CU-002 con un flujo alternativo, como permite el taller. |
| CU "Iniciar sesión" como precondición general. | **Rechazada** | Sin autenticación (PER-01, RS-03). |
| Paso "el sistema muestra los datos del libro y pide confirmación" antes de prestar. | **Rechazada** | Ninguna HU pide confirmación; añade un paso no especificado. |
| Excepción "el libro está prestado: el sistema muestra a quién y ofrece reservarlo". | **Corregida** | Se conserva el rechazo (RN-02); la reserva está excluida. |
| Excepción "el estudiante tiene préstamos vencidos: se bloquea el préstamo". | **Rechazada** | Regla inventada; no existe en los requisitos. |
| Registrar la fecha real en que se devuelve el libro. | **Rechazada** | No está en los requisitos (ya rechazado en la Actividad 2). |
| Menú numerado con opciones 1–6 y opción "Salir". | **Diferida** | Es diseño de la interfaz de consola (Actividad 4). Los flujos dicen "el bibliotecario indica que desea…". |
| Postcondición "se conserva entre ejecuciones" en los casos que modifican datos. | Aceptada | Traza RNF-01 en los casos de uso. |
| Excepciones de lista vacía en las consultas. | Aceptada | HU-002 criterio 3 y HU-005 criterio 3. |

**Verificación:** cada historia aparece en al menos un caso de uso (sección 3 de
`product-spec.md`) y cada excepción corresponde a un criterio de rechazo de las HU.
