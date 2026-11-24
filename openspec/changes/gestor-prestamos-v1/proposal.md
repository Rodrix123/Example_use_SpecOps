# Proposal

Fuentes: [`docs/intent.md`](../../../docs/intent.md) v1.0, [`docs/requirements.md`](../../../docs/requirements.md) v1.0 y [`docs/product-spec.md`](../../../docs/product-spec.md) v1.0.
Este cambio traslada esos documentos al formato de OpenSpec; no agrega requisitos.

## Why

El bibliotecario de una pequeña biblioteca universitaria lleva el catálogo y los préstamos en hojas
de cálculo. Con ese registro manual le resulta difícil saber qué ejemplares están disponibles,
cuáles están prestados y qué préstamos están vencidos (intent §2).

## What Changes

Primera versión del Gestor de préstamos de libros (CAP-01 a CAP-06):

- Registrar libros del catálogo con identificador, título y autor (CAP-01, HU-001, CU-001).
- Consultar el catálogo con el estado de cada libro (CAP-02, HU-002, CU-002).
- Registrar un préstamo de un libro disponible a un estudiante, con fecha prevista de devolución (CAP-03, HU-003, CU-003).
- Registrar la devolución de un libro prestado (CAP-04, HU-004, CU-004).
- Consultar los préstamos vencidos (CAP-05, HU-005, CU-002 flujo alternativo 1a).
- Conservar la información entre ejecuciones (CAP-06, RNF-01).

Fuera del alcance: lo listado en intent §6 y product-spec §4.

## Capabilities

### New Capabilities
- `catalogo`: registro y consulta de los libros del catálogo con su estado (HU-001, HU-002, RN-01).
- `prestamos`: registro de préstamos y devoluciones y consulta de préstamos vencidos (HU-003, HU-004, HU-005, RN-02, RN-03, RN-04, RNF-02).
- `datos`: conservación de la información entre ejecuciones y no modificación de datos ante entradas rechazadas (RNF-01, RNF-03).

### Modified Capabilities
Ninguna.

## Impact

- Sistema nuevo; no hay código existente afectado.
- Restricciones (RS-01 a RS-04, PER-01): aplicación de consola en Python, ejecución local, sin
  interfaz gráfica ni integraciones externas, un único usuario (bibliotecario) sin autenticación.
