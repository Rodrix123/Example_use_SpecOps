"""Pruebas del almacén JSON (TASK-004: TEST-009 a TEST-012; TASK-005: TEST-013 a TEST-015)."""

import json
import os
import tempfile
import unittest
from datetime import date
from unittest import mock
from pathlib import Path

from gestor_prestamos import almacen
from gestor_prestamos.almacen import Almacen, ErrorAlmacen
from gestor_prestamos.modelos import Libro, Prestamo

RAIZ = Path(__file__).resolve().parent.parent


class PruebaCargar(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.carpeta = Path(self._tmp.name)
        self.ruta = self.carpeta / "biblioteca.json"

    def tearDown(self):
        self._tmp.cleanup()

    def test_009_archivo_inexistente_devuelve_vacio(self):
        libros, prestamos = Almacen(self.ruta).cargar()
        self.assertEqual(libros, [])
        self.assertEqual(prestamos, [])
        self.assertFalse(self.ruta.exists())

    def test_010_archivo_valido_con_tildes(self):
        datos = {
            "libros": [
                {"id": "L-001", "titulo": "Cien años de soledad", "autor": "Gabriel García Márquez"}
            ],
            "prestamos": [
                {"libro_id": "L-001", "estudiante": "Ana Pérez",
                 "fecha_prevista": "2026-12-15", "activo": True}
            ],
        }
        self.ruta.write_text(json.dumps(datos, ensure_ascii=False), encoding="utf-8")
        libros, prestamos = Almacen(self.ruta).cargar()
        self.assertEqual(libros, [Libro("L-001", "Cien años de soledad", "Gabriel García Márquez")])
        self.assertEqual(prestamos, [Prestamo("L-001", "Ana Pérez", date(2026, 12, 15), True)])
        self.assertIsInstance(prestamos[0].fecha_prevista, date)

    def test_011_json_invalido_lanza_error_sin_modificar(self):
        self.ruta.write_bytes("{ no es json".encode("utf-8"))
        antes = self.ruta.read_bytes()
        with self.assertRaises(ErrorAlmacen):
            Almacen(self.ruta).cargar()
        self.assertEqual(self.ruta.read_bytes(), antes)

    def test_012_ruta_por_defecto_independiente_del_directorio(self):
        original = os.getcwd()
        try:
            os.chdir(RAIZ)
            desde_raiz = almacen.ruta_por_defecto()
            os.chdir(self.carpeta)
            desde_otra = almacen.ruta_por_defecto()
        finally:
            os.chdir(original)
        self.assertEqual(desde_raiz, desde_otra)
        self.assertEqual(desde_raiz, RAIZ / "ops" / "biblioteca.json")
        self.assertEqual(Almacen().ruta, desde_raiz)


def datos_de_prueba():
    """Datos de TEST-013 y TEST-014."""
    libros = [
        Libro("L-001", "Cien años de soledad", "Gabriel García Márquez"),
        Libro("L-002", "El Aleph", "Jorge Luis Borges"),
    ]
    prestamos = [
        Prestamo("L-001", "Ana Pérez", date(2026, 12, 15), True),
        Prestamo("L-002", "Luis Gómez", date(2026, 11, 10), False),
    ]
    return libros, prestamos


class PruebaGuardar(unittest.TestCase):
    """TASK-005: TEST-013 a TEST-015."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.carpeta = Path(self._tmp.name)
        self.ruta = self.carpeta / "biblioteca.json"

    def tearDown(self):
        self._tmp.cleanup()

    def test_013_guardar_y_cargar_devuelve_lo_mismo(self):
        libros, prestamos = datos_de_prueba()
        Almacen(self.ruta).guardar(libros, prestamos)
        cargados = Almacen(self.ruta).cargar()
        self.assertEqual(cargados, (libros, prestamos))
        self.assertIs(cargados[1][1].activo, False)

    def test_014_fechas_iso_y_tildes_sin_escapar(self):
        libros, prestamos = datos_de_prueba()
        Almacen(self.ruta).guardar(libros, prestamos)
        texto = self.ruta.read_bytes().decode("utf-8")
        self.assertIn("2026-12-15", texto)
        self.assertIn("2026-11-10", texto)
        self.assertNotIn("15/12/2026", texto)
        self.assertIn("Cien años de soledad", texto)
        self.assertIn("Gabriel García Márquez", texto)
        self.assertNotIn("\\u", texto)

    def test_015_falla_de_reemplazo_deja_el_original_intacto(self):
        libros, prestamos = datos_de_prueba()
        Almacen(self.ruta).guardar(libros, prestamos)
        antes = self.ruta.read_bytes()
        otros = [Libro("L-003", "Rayuela", "Julio Cortázar")]
        with mock.patch("gestor_prestamos.almacen.os.replace", side_effect=OSError("simulado")):
            with self.assertRaises(ErrorAlmacen):
                Almacen(self.ruta).guardar(otros, [])
        self.assertEqual(self.ruta.read_bytes(), antes)
        self.assertEqual(list(self.carpeta.glob("*.tmp")), [])


if __name__ == "__main__":
    unittest.main()
