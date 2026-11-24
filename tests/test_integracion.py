"""Pruebas de integración (TASK-020: TEST-096 a TEST-101; TASK-021: TEST-102).

Almacén y servicio reales sobre un archivo en una carpeta temporal; nunca `ops/biblioteca.json`.
"""

import tempfile
import unittest
from datetime import date
from pathlib import Path

from gestor_prestamos.almacen import Almacen
from gestor_prestamos.consola import Consola
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


class PruebaFlujoCompletoPorConsola(ConArchivoTemporal):
    """TASK-021: TEST-102.

    Supuesto S-2 del plan: la fecha simulada es 01/11/2026 en los pasos 1 y 2 y 01/12/2026 desde el
    paso 3, para que el préstamo registrado con fecha válida quede vencido al consultar.
    """

    def test_102_flujo_completo(self):
        reloj = {"hoy": date(2026, 11, 1)}
        servicio = Servicio(Almacen(self.ruta), hoy=lambda: reloj["hoy"])
        pasos = [
            ["1", *L001],                                   # (1) registrar libro
            ["3", "L-001", "Ana Pérez", "10/11/2026"],       # (2) registrar préstamo
            ["2"],                                           # (3) consultar catálogo
            ["5"],                                           # (4) consultar vencidos
            ["3", "L-001", "Luis Gómez", "15/12/2026"],      # (5) segundo préstamo
            ["4", "L-001"],                                  # (6) devolución
            ["2"],                                           # (7) consultar catálogo
            ["5"],                                           # (8) consultar vencidos
            ["6"],                                           # salir
        ]
        entradas = [entrada for paso in pasos for entrada in paso]
        cambio_de_fecha = len(pasos[0]) + len(pasos[1])
        salida = []
        marcas = []  # posición en la salida al empezar cada paso

        def leer(pregunta=""):
            salida.append(pregunta)
            if leer.consumidas == cambio_de_fecha:
                reloj["hoy"] = HOY
            inicio = sum(len(paso) for paso in pasos[: len(marcas)])
            if leer.consumidas == inicio:
                marcas.append(len(salida))
            leer.consumidas += 1
            return entradas[leer.consumidas - 1]

        leer.consumidas = 0
        Consola(servicio, leer, salida.append).ejecutar()

        def texto_del_paso(numero):
            fin = marcas[numero] if numero < len(marcas) else len(salida)
            return "\n".join(salida[marcas[numero - 1]:fin])

        self.assertIn("Libro registrado: L-001", texto_del_paso(1))
        self.assertIn("Préstamo registrado: L-001 a Ana Pérez", texto_del_paso(2))
        self.assertIn("L-001 | Cien años de soledad | Gabriel García Márquez | prestado | Ana Pérez | 10/11/2026",
                      texto_del_paso(3))
        self.assertIn("L-001 | Cien años de soledad | Ana Pérez | 10/11/2026", texto_del_paso(4))
        self.assertIn("ya está prestado", texto_del_paso(5))
        self.assertIn("Devolución registrada: L-001", texto_del_paso(6))
        self.assertIn("L-001 | Cien años de soledad | Gabriel García Márquez | disponible", texto_del_paso(7))
        self.assertIn("No hay préstamos vencidos.", texto_del_paso(8))


if __name__ == "__main__":
    unittest.main()
