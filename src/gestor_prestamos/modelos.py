"""Datos de Libro y Prestamo (TASK-003; HU-001, HU-003, RN-04; design Decisiones 1, 2 y 3).

Solo datos: sin reglas de negocio ni entrada/salida. El libro no guarda su estado; un libro está
prestado si y solo si tiene un préstamo activo (design Decisión 3).
"""

from dataclasses import dataclass
from datetime import date


@dataclass
class Libro:
    """Libro del catálogo (HU-001, RES-05)."""

    identificador: str
    titulo: str
    autor: str


@dataclass
class Prestamo:
    """Préstamo de un libro a un estudiante (HU-003, RES-06).

    `activo` es verdadero desde que se registra hasta que se registra su devolución (RN-04).
    """

    libro_id: str
    estudiante: str
    fecha_prevista: date
    activo: bool = True
