# Spec Delta

## Purpose

Garantiza que la información del catálogo y de los préstamos se conserve entre ejecuciones y que
una entrada rechazada no modifique los datos. Fuente: RNF-01, RNF-03.

## ADDED Requirements

### Requirement: RNF-01 Conservación entre ejecuciones
La información del catálogo y de los préstamos MUST conservarse entre ejecuciones de la aplicación.

#### Scenario: Cerrar y reabrir la aplicación
- **WHEN** el bibliotecario registra datos, cierra la aplicación y la vuelve a abrir
- **THEN** los datos son idénticos

### Requirement: RNF-03 Entrada rechazada
Ante una entrada rechazada, el sistema MUST mostrar el motivo y MUST NOT modificar los datos.

#### Scenario: Rechazo en cualquier operación
- **WHEN** el sistema rechaza un registro de libro, un préstamo o una devolución (HU-001 a HU-004)
- **THEN** muestra el motivo del rechazo y los datos quedan sin cambios
