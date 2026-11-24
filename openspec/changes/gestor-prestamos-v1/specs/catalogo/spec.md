# Spec Delta

## Purpose

Permite al bibliotecario registrar los libros del catálogo y consultar el estado de cada uno
(disponible o prestado). Fuente: HU-001, HU-002, RN-01, CU-001, CU-002.

## ADDED Requirements

### Requirement: HU-001 Registrar un libro
El sistema MUST permitir al bibliotecario registrar un libro con identificador, título y autor. El
libro registrado MUST quedar en estado disponible.

#### Scenario: Registro con datos completos
- **WHEN** el bibliotecario ingresa identificador, título y autor
- **THEN** el libro queda registrado y en estado disponible

#### Scenario: Falta un dato
- **WHEN** el bibliotecario omite el identificador, el título o el autor
- **THEN** el sistema rechaza el registro e indica el dato faltante

### Requirement: RN-01 Identificador único
El identificador de cada libro MUST ser único en el catálogo.

#### Scenario: Identificador repetido
- **WHEN** el bibliotecario intenta registrar un libro con un identificador que ya existe
- **THEN** el sistema rechaza el registro

### Requirement: HU-002 Consultar el catálogo
El sistema MUST mostrar todos los libros registrados con identificador, título, autor y estado
(disponible / prestado).

#### Scenario: Catálogo con libros
- **WHEN** el bibliotecario consulta el catálogo
- **THEN** se muestran todos los libros registrados con identificador, título, autor y estado

#### Scenario: Libro prestado en el catálogo
- **WHEN** el bibliotecario consulta el catálogo y un libro está prestado
- **THEN** para ese libro se muestran el estudiante y la fecha prevista de devolución

#### Scenario: Catálogo vacío
- **WHEN** el bibliotecario consulta el catálogo y no hay libros registrados
- **THEN** el sistema lo informa
