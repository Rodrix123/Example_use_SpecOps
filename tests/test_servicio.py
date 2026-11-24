"""Pruebas del servicio (TASK-006 a TASK-011).

Usan un almacén simulado en memoria con contador de llamadas a `guardar` y una fecha fija
(tests/test-plan.md §2 y §3).
"""

import copy
import unittest
from datetime import date

from gestor_prestamos.modelos import Libro, Prestamo
from gestor_prestamos.servicio import ErrorNegocio, Servicio

HOY = date(2026, 12, 1)
AYER = date(2026, 11, 30)
PASADA = date(2026, 11, 10)
FUTURA = date(2026, 12, 15)

L001 = ("L-001", "Cien años de soledad", "Gabriel García Márquez")
L002 = ("L-002", "El Aleph", "Jorge Luis Borges")
L003 = ("L-003", "Rayuela", "Julio Cortázar")


class AlmacenSimulado:
    """Almacén en memoria: cuenta las cargas y las llamadas a `guardar`."""

    def __init__(self, libros=(), prestamos=()):
        self.libros = list(libros)
        self.prestamos = list(prestamos)
        self.cargas = 0
        self.guardados = 0

    def cargar(self):
        self.cargas += 1
        return copy.deepcopy(self.libros), copy.deepcopy(self.prestamos)

    def guardar(self, libros, prestamos):
        self.guardados += 1
        self.libros = copy.deepcopy(libros)
        self.prestamos = copy.deepcopy(prestamos)


def crear(libros=(), prestamos=(), hoy=HOY):
    """Servicio con almacén simulado y fecha fija."""
    almacen = AlmacenSimulado([Libro(*datos) for datos in libros], prestamos)
    return Servicio(almacen, hoy=lambda: hoy), almacen


def instantanea(servicio):
    return copy.deepcopy(servicio.libros), copy.deepcopy(servicio.prestamos)


class PruebaBaseServicio(unittest.TestCase):
    """TASK-006: TEST-016 a TEST-018."""

    def test_016_usa_la_fecha_inyectada(self):
        servicio, _ = crear([L001])
        self.assertEqual(servicio.hoy(), HOY)

    def test_017_carga_los_datos_del_almacen_al_crearse(self):
        prestamo = Prestamo("L-001", "Ana Pérez", FUTURA, True)
        servicio, almacen = crear([L001], [prestamo])
        self.assertEqual(almacen.cargas, 1)
        self.assertEqual(servicio.libros, [Libro(*L001)])
        self.assertEqual(servicio.prestamos, [prestamo])

    def test_018_error_de_negocio_expone_el_motivo(self):
        error = ErrorNegocio("Identificador repetido")
        self.assertEqual(error.motivo, "Identificador repetido")
        self.assertEqual(str(error), "Identificador repetido")


if __name__ == "__main__":
    unittest.main()
