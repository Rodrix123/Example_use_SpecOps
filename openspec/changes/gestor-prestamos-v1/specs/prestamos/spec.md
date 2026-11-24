# Spec Delta

## Purpose

Permite al bibliotecario registrar préstamos y devoluciones de libros y consultar los préstamos
vencidos. Fuente: HU-003, HU-004, HU-005, RN-02, RN-03, RN-04, RNF-02, CU-002, CU-003, CU-004.

## ADDED Requirements

### Requirement: HU-003 Registrar un préstamo
El sistema MUST permitir registrar el préstamo de un libro existente y disponible a un estudiante,
con una fecha prevista de devolución válida. Al registrarlo, el libro MUST pasar a prestado.

#### Scenario: Préstamo de libro disponible
- **WHEN** el libro existe y está disponible, y el bibliotecario ingresa el estudiante y una fecha prevista de devolución válida
- **THEN** el préstamo queda registrado y el libro pasa a prestado

#### Scenario: Libro inexistente
- **WHEN** el identificador del libro no existe
- **THEN** el sistema rechaza el préstamo

#### Scenario: Falta el estudiante o la fecha no es válida
- **WHEN** falta el estudiante o la fecha prevista de devolución no es válida
- **THEN** el sistema rechaza el préstamo

### Requirement: RN-02 Un solo préstamo activo por libro
Un libro MUST NOT tener más de un préstamo activo a la vez.

#### Scenario: Libro ya prestado
- **WHEN** el bibliotecario intenta prestar un libro que ya está prestado
- **THEN** el sistema rechaza el préstamo

### Requirement: RN-04 Préstamo activo
Un préstamo MUST estar activo desde que se registra hasta que se registra su devolución.

#### Scenario: Préstamo recién registrado
- **WHEN** se registra un préstamo
- **THEN** el préstamo queda activo hasta que se registre su devolución

### Requirement: HU-004 Registrar una devolución
El sistema MUST permitir registrar la devolución de un libro prestado. Al registrarla, el préstamo
MUST cerrarse y el libro MUST pasar a disponible.

#### Scenario: Devolución de libro prestado
- **WHEN** el bibliotecario registra la devolución de un libro prestado
- **THEN** el préstamo se cierra y el libro pasa a disponible

#### Scenario: Libro no prestado o inexistente
- **WHEN** el libro no está prestado o no existe
- **THEN** el sistema rechaza la devolución

### Requirement: RN-03 Préstamo vencido
Un préstamo MUST considerarse vencido si sigue activo y su fecha prevista de devolución es anterior
a la fecha actual.

#### Scenario: Préstamo activo con fecha pasada
- **WHEN** un préstamo sigue activo y su fecha prevista de devolución es anterior a la fecha actual
- **THEN** el préstamo se considera vencido

### Requirement: HU-005 Consultar préstamos vencidos
El sistema MUST mostrar exactamente los préstamos vencidos (RN-03), con libro, estudiante y fecha
prevista de devolución.

#### Scenario: Hay préstamos vencidos
- **WHEN** el bibliotecario consulta los préstamos vencidos
- **THEN** se muestran exactamente los préstamos activos con fecha prevista anterior a la fecha actual, con libro, estudiante y fecha prevista

#### Scenario: Préstamos devueltos
- **WHEN** el bibliotecario consulta los préstamos vencidos y existen préstamos devueltos
- **THEN** los préstamos devueltos no aparecen

#### Scenario: Sin préstamos vencidos
- **WHEN** el bibliotecario consulta los préstamos vencidos y no hay ninguno
- **THEN** el sistema lo informa

### Requirement: RNF-02 Tiempo de registro
Registrar un préstamo o una devolución MUST tomar menos de un minuto.

#### Scenario: Usuario sin capacitación previa
- **WHEN** un usuario sin capacitación previa registra un préstamo o una devolución
- **THEN** la operación toma menos de un minuto
