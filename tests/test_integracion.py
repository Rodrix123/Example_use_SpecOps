"""Pruebas de integración (TASK-020: TEST-096 a TEST-101).

Almacén y servicio reales sobre un archivo en una carpeta temporal; nunca `ops/biblioteca.json`.
"""

import tempfile
import unittest
from datetime import date
from pathlib import Path

from gestor_prestamos.almacen import Almacen
from gestor_prestamos.modelos import Libro, Prestamo
from gestor_prestamos.servicio import DISPONIBLE, PRESTADO, ErrorNegocio, Servicio

HOY = date(2026, 12, 1)
FUTURA = date(2026, 12, 15)
L001 = ("L-001", "Cien años de soledad", "Gabriel García Márquez")
L002 = ("L-002", "El Aleph", "Jorge Luis Borges")


class ConArchivoTemporal(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.ruta = Path(self._tmp.name) / "biblioteca.json"

    def tearDown(self):
        self._tmp.cleanup()

    def abrir(self, hoy=HOY):
        """Equivale a abrir la aplicación: almacén y servicio nuevos sobre el mismo archivo."""
        return Servicio(Almacen(self.ruta), hoy=lambda: hoy)


class PruebaPersistencia(ConArchivoTemporal):
    """TEST-096 y TEST-097."""

    def test_096_cerrar_y_reabrir_conserva_los_datos(self):
        servicio = self.abrir()
        servicio.registrar_libro(*L001)
        servicio.registrar_libro(*L002)
        servicio.registrar_prestamo("L-001", "Ana Pérez", FUTURA)
        antes = servicio.consultar_catalogo()
        del servicio

        reabierto = self.abrir()
        self.assertEqual(reabierto.consultar_catalogo(), antes)
        l001, l002 = reabierto.consultar_catalogo()
        self.assertEqual((l001.titulo, l001.autor), L001[1:])
        self.assertEqual((l001.estado, l001.estudiante, l001.fecha_prevista),
                         (PRESTADO, "Ana Pérez", FUTURA))
        self.assertEqual(l002.estado, DISPONIBLE)

    def test_097_devolucion_se_conserva_tras_reabrir(self):
        self.test_096_cerrar_y_reabrir_conserva_los_datos()
        self.abrir().registrar_devolucion("L-001")

        reabierto = self.abrir()
        self.assertEqual(reabierto.consultar_catalogo()[0].estado, DISPONIBLE)
        self.assertEqual(reabierto.prestamos, [Prestamo("L-001", "Ana Pérez", FUTURA, False)])


class PruebaRechazosNoTocanElArchivo(ConArchivoTemporal):
    """TEST-098 a TEST-101: tras cada rechazo el archivo queda byte a byte igual."""

    def setUp(self):
        super().setUp()
        Almacen(self.ruta).guardar(
            [Libro(*L001), Libro(*L002)], [Prestamo("L-001", "Ana Pérez", FUTURA, True)]
        )
        self.bytes_iniciales = self.ruta.read_bytes()

    def assertRechazoSinCambios(self, operacion, *argumentos):
        servicio = self.abrir()
        with self.assertRaises(ErrorNegocio) as contexto:
            getattr(servicio, operacion)(*argumentos)
        self.assertTrue(contexto.exception.motivo)
        self.assertEqual(self.ruta.read_bytes(), self.bytes_iniciales)

    def test_098_libro_repetido(self):
        self.assertRechazoSinCambios("registrar_libro", *L002)

    def test_099_prestamo_de_libro_inexistente(self):
        self.assertRechazoSinCambios("registrar_prestamo", "L-099", "Luis Gómez", date(2026, 12, 20))

    def test_100_prestamo_de_libro_prestado(self):
        self.assertRechazoSinCambios("registrar_prestamo", "L-001", "Luis Gómez", date(2026, 12, 20))

    def test_101_devolucion_de_libro_no_prestado(self):
        self.assertRechazoSinCambios("registrar_devolucion", "L-002")


if __name__ == "__main__":
    unittest.main()
