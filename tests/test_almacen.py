"""Pruebas del almacén JSON (TASK-004: TEST-009 a TEST-012)."""

import json
import os
import tempfile
import unittest
from datetime import date
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


if __name__ == "__main__":
    unittest.main()
