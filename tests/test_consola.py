"""Pruebas de la consola (TASK-012 a TASK-018; TEST-057 a TEST-091)."""

import unittest
from datetime import date

from gestor_prestamos.consola import fecha_a_texto, texto_a_fecha


class PruebaFechas(unittest.TestCase):
    """TASK-012: TEST-057 a TEST-064."""

    def test_057_fecha_valida(self):
        self.assertEqual(texto_a_fecha("15/12/2026"), date(2026, 12, 15))

    def test_058_fecha_inexistente(self):
        self.assertIsNone(texto_a_fecha("31/02/2026"))

    def test_059_formato_iso_rechazado(self):
        self.assertIsNone(texto_a_fecha("2026-12-15"))

    def test_060_dia_y_mes_sin_dos_digitos(self):
        self.assertIsNone(texto_a_fecha("5/1/2026"))

    def test_061_texto_vacio(self):
        self.assertIsNone(texto_a_fecha(""))

    def test_062_texto_no_numerico(self):
        self.assertIsNone(texto_a_fecha("abc"))
        self.assertIsNone(texto_a_fecha("dd/mm/aaaa"))

    def test_063_ida_y_vuelta(self):
        self.assertEqual(fecha_a_texto(texto_a_fecha("15/12/2026")), "15/12/2026")

    def test_064_fecha_a_texto_con_dos_digitos(self):
        self.assertEqual(fecha_a_texto(date(2026, 1, 5)), "05/01/2026")


if __name__ == "__main__":
    unittest.main()
