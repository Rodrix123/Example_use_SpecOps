"""Pruebas de los modelos (TASK-003; TEST-005 a TEST-008)."""

import dataclasses
import unittest
from datetime import date

from gestor_prestamos.modelos import Libro, Prestamo


class PruebaModelos(unittest.TestCase):
    def test_005_libro_conserva_sus_campos(self):
        libro = Libro("L-001", "Cien años de soledad", "Gabriel García Márquez")
        self.assertEqual(libro.identificador, "L-001")
        self.assertEqual(libro.titulo, "Cien años de soledad")
        self.assertEqual(libro.autor, "Gabriel García Márquez")

    def test_006_prestamo_conserva_sus_campos(self):
        prestamo = Prestamo("L-001", "Ana Pérez", date(2026, 12, 15), True)
        self.assertEqual(prestamo.libro_id, "L-001")
        self.assertEqual(prestamo.estudiante, "Ana Pérez")
        self.assertEqual(prestamo.fecha_prevista, date(2026, 12, 15))
        self.assertIs(prestamo.activo, True)

    def test_007_fecha_prevista_es_fecha(self):
        prestamo = Prestamo("L-001", "Ana Pérez", date(2026, 12, 15), True)
        self.assertIsInstance(prestamo.fecha_prevista, date)
        self.assertNotIsInstance(prestamo.fecha_prevista, str)
        self.assertEqual(prestamo.fecha_prevista, date(2026, 12, 15))

    def test_008_libro_sin_campo_de_estado(self):
        campos = {campo.name for campo in dataclasses.fields(Libro)}
        self.assertEqual(campos, {"identificador", "titulo", "autor"})


if __name__ == "__main__":
    unittest.main()
