"""Pruebas del servicio (TASK-006 a TASK-011; TEST-016 a TEST-056).

Usan un almacén simulado en memoria con contador de llamadas a `guardar` y una fecha fija
(tests/test-plan.md §2 y §3).
"""

import copy
import unittest
from datetime import date

from gestor_prestamos.modelos import Libro, Prestamo
from gestor_prestamos.servicio import DISPONIBLE, PRESTADO, ErrorNegocio, Servicio

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


class PruebaRegistrarLibro(unittest.TestCase):
    """TASK-007: TEST-019 a TEST-028."""

    def assertRechazo(self, servicio, almacen, palabras, *argumentos):
        """El registro se rechaza con un motivo que contiene `palabras`, sin cambios ni guardado."""
        antes = instantanea(servicio)
        guardados = almacen.guardados
        with self.assertRaises(ErrorNegocio) as contexto:
            servicio.registrar_libro(*argumentos)
        self.assertIn(palabras, contexto.exception.motivo.lower())
        self.assertEqual(instantanea(servicio), antes)
        self.assertEqual(almacen.guardados, guardados)

    def test_019_registro_completo(self):
        servicio, almacen = crear()
        servicio.registrar_libro(*L001)
        self.assertEqual(servicio.libros, [Libro(*L001)])
        self.assertEqual(servicio.prestamos, [])  # sin préstamo activo: disponible
        self.assertEqual(almacen.guardados, 1)
        self.assertEqual(almacen.libros, [Libro(*L001)])

    def test_020_falta_identificador(self):
        servicio, almacen = crear()
        self.assertRechazo(servicio, almacen, "falta el identificador", "", L001[1], L001[2])
        self.assertEqual(servicio.libros, [])

    def test_021_falta_titulo(self):
        servicio, almacen = crear()
        self.assertRechazo(servicio, almacen, "falta el título", "L-001", "", L001[2])

    def test_022_falta_autor(self):
        servicio, almacen = crear()
        self.assertRechazo(servicio, almacen, "falta el autor", "L-001", L001[1], "")

    def test_023_solo_espacios_cuenta_como_faltante(self):
        servicio, almacen = crear()
        self.assertRechazo(servicio, almacen, "falta el título", "L-001", "   ", L001[2])

    def _con_l001(self):
        servicio, almacen = crear()
        servicio.registrar_libro(*L001)
        self.assertEqual(almacen.guardados, 1)
        return servicio, almacen

    def test_024_identificador_repetido(self):
        servicio, almacen = self._con_l001()
        self.assertRechazo(servicio, almacen, "ya existe", "L-001", "El Aleph", "Jorge Luis Borges")
        self.assertEqual(servicio.libros, [Libro(*L001)])
        self.assertEqual(almacen.guardados, 1)

    def test_025_repetido_con_distinta_mayuscula(self):
        servicio, almacen = self._con_l001()
        self.assertRechazo(servicio, almacen, "ya existe", "l-001", "El Aleph", "Jorge Luis Borges")
        self.assertEqual(len(servicio.libros), 1)

    def test_026_repetido_con_espacios_alrededor(self):
        servicio, almacen = self._con_l001()
        self.assertRechazo(servicio, almacen, "ya existe", " L-001 ", "El Aleph", "Jorge Luis Borges")
        self.assertEqual(len(servicio.libros), 1)

    def test_027_rechazos_no_modifican_datos(self):
        prestamo = Prestamo("L-001", "Ana Pérez", FUTURA, True)
        servicio, almacen = crear([L001, L002], [prestamo])
        self.assertRechazo(servicio, almacen, "ya existe", *L002)
        self.assertRechazo(servicio, almacen, "falta el autor", "L-003", "Rayuela", "")
        self.assertEqual(almacen.guardados, 0)

    def test_028_primero_se_validan_datos_completos(self):
        servicio, almacen = crear([L001])
        self.assertRechazo(servicio, almacen, "falta el título", "L-001", "", L001[2])


class PruebaConsultarCatalogo(unittest.TestCase):
    """TASK-008: TEST-029 a TEST-033."""

    def test_029_varios_libros_disponibles(self):
        servicio, _ = crear([L001, L002, L003])
        catalogo = servicio.consultar_catalogo()
        self.assertEqual(len(catalogo), 3)
        for entrada, datos in zip(catalogo, (L001, L002, L003)):
            self.assertEqual((entrada.identificador, entrada.titulo, entrada.autor), datos)
            self.assertEqual(entrada.estado, DISPONIBLE)

    def test_030_libro_prestado_incluye_estudiante_y_fecha(self):
        servicio, _ = crear([L001, L002], [Prestamo("L-002", "Ana Pérez", FUTURA, True)])
        l001, l002 = servicio.consultar_catalogo()
        self.assertEqual(l002.estado, PRESTADO)
        self.assertEqual(l002.estudiante, "Ana Pérez")
        self.assertEqual(l002.fecha_prevista, FUTURA)
        self.assertEqual(l001.estado, DISPONIBLE)
        self.assertIsNone(l001.estudiante)
        self.assertIsNone(l001.fecha_prevista)

    def test_031_libro_devuelto_aparece_disponible(self):
        servicio, _ = crear([L001], [Prestamo("L-001", "Ana Pérez", PASADA, False)])
        (entrada,) = servicio.consultar_catalogo()
        self.assertEqual(entrada.estado, DISPONIBLE)

    def test_032_catalogo_vacio(self):
        servicio, _ = crear()
        self.assertEqual(servicio.consultar_catalogo(), [])

    def test_033_consultar_no_modifica_datos(self):
        servicio, almacen = crear([L001, L002], [Prestamo("L-002", "Ana Pérez", FUTURA, True)])
        antes = instantanea(servicio)
        servicio.consultar_catalogo()
        self.assertEqual(instantanea(servicio), antes)
        self.assertEqual(almacen.guardados, 0)


def rechazo(prueba, servicio, almacen, operacion, palabras, *argumentos):
    """La operación se rechaza con un motivo que contiene `palabras`; datos y guardado sin cambios."""
    antes = instantanea(servicio)
    guardados = almacen.guardados
    with prueba.assertRaises(ErrorNegocio) as contexto:
        getattr(servicio, operacion)(*argumentos)
    prueba.assertIn(palabras, contexto.exception.motivo.lower())
    prueba.assertEqual(instantanea(servicio), antes)
    prueba.assertEqual(almacen.guardados, guardados)
    return contexto.exception.motivo


def activos(servicio, libro_id):
    return [p for p in servicio.prestamos if p.libro_id == libro_id and p.activo]


class PruebaRegistrarPrestamo(unittest.TestCase):
    """TASK-009: TEST-034 a TEST-043."""

    def test_034_prestamo_valido(self):
        servicio, almacen = crear([L001])
        servicio.registrar_prestamo("L-001", "Ana Pérez", FUTURA)
        self.assertEqual(servicio.prestamos, [Prestamo("L-001", "Ana Pérez", FUTURA, True)])
        self.assertEqual(servicio.consultar_catalogo()[0].estado, PRESTADO)
        self.assertEqual(almacen.guardados, 1)

    def test_035_libro_inexistente(self):
        servicio, almacen = crear([L001])
        rechazo(self, servicio, almacen, "registrar_prestamo", "no existe", "L-099", "Ana Pérez", FUTURA)

    def test_036_libro_ya_prestado(self):
        servicio, almacen = crear([L001], [Prestamo("L-001", "Ana Pérez", FUTURA, True)])
        rechazo(self, servicio, almacen, "registrar_prestamo", "ya está prestado",
                "L-001", "Luis Gómez", date(2026, 12, 20))
        self.assertEqual(activos(servicio, "L-001"), [Prestamo("L-001", "Ana Pérez", FUTURA, True)])

    def test_037_falta_el_estudiante(self):
        servicio, almacen = crear([L001])
        for estudiante in ("", "   "):
            with self.subTest(estudiante=estudiante):
                rechazo(self, servicio, almacen, "registrar_prestamo", "falta el estudiante",
                        "L-001", estudiante, FUTURA)

    def test_038_fecha_sin_valor(self):
        servicio, almacen = crear([L001])
        rechazo(self, servicio, almacen, "registrar_prestamo", "no es válida", "L-001", "Ana Pérez", None)

    def test_039_fecha_anterior_a_hoy(self):
        servicio, almacen = crear([L001])
        rechazo(self, servicio, almacen, "registrar_prestamo", "anterior a hoy", "L-001", "Ana Pérez", AYER)

    def test_040_fecha_de_hoy_se_acepta(self):
        servicio, _ = crear([L001])
        servicio.registrar_prestamo("L-001", "Ana Pérez", HOY)
        self.assertEqual(activos(servicio, "L-001"), [Prestamo("L-001", "Ana Pérez", HOY, True)])

    def test_041_busqueda_sin_distinguir_mayusculas(self):
        servicio, _ = crear([L001])
        servicio.registrar_prestamo("l-001", "Ana Pérez", FUTURA)
        self.assertEqual(activos(servicio, "L-001"), [Prestamo("L-001", "Ana Pérez", FUTURA, True)])

    def test_042_rechazos_no_modifican_datos(self):
        servicio, almacen = crear([L001, L002], [Prestamo("L-001", "Ana Pérez", FUTURA, True)])
        casos = [
            ("no existe", ("L-099", "Luis Gómez", FUTURA)),
            ("ya está prestado", ("L-001", "Luis Gómez", FUTURA)),
            ("falta el estudiante", ("L-002", "", FUTURA)),
            ("anterior a hoy", ("L-002", "Luis Gómez", AYER)),
        ]
        for palabras, argumentos in casos:
            with self.subTest(palabras=palabras):
                rechazo(self, servicio, almacen, "registrar_prestamo", palabras, *argumentos)
        self.assertEqual(almacen.guardados, 0)

    def test_043_orden_de_validacion(self):
        servicio, almacen = crear([L001, L002], [Prestamo("L-001", "Ana Pérez", FUTURA, True)])
        rechazo(self, servicio, almacen, "registrar_prestamo", "no existe", "L-099", "", None)
        rechazo(self, servicio, almacen, "registrar_prestamo", "ya está prestado", "L-001", "", None)
        rechazo(self, servicio, almacen, "registrar_prestamo", "falta el estudiante", "L-002", "", None)


class PruebaRegistrarDevolucion(unittest.TestCase):
    """TASK-010: TEST-044 a TEST-049."""

    def test_044_devolucion_valida(self):
        servicio, almacen = crear([L001], [Prestamo("L-001", "Ana Pérez", FUTURA, True)])
        servicio.registrar_devolucion("L-001")
        self.assertEqual(servicio.prestamos, [Prestamo("L-001", "Ana Pérez", FUTURA, False)])
        self.assertEqual(servicio.consultar_catalogo()[0].estado, DISPONIBLE)
        self.assertEqual(almacen.guardados, 1)

    def test_045_libro_inexistente(self):
        servicio, almacen = crear([L001])
        rechazo(self, servicio, almacen, "registrar_devolucion", "no existe", "L-099")

    def test_046_libro_no_prestado(self):
        servicio, almacen = crear([L001])
        rechazo(self, servicio, almacen, "registrar_devolucion", "no está prestado", "L-001")

    def test_047_tras_devolver_se_puede_prestar_de_nuevo(self):
        servicio, _ = crear([L001], [Prestamo("L-001", "Ana Pérez", FUTURA, True)])
        servicio.registrar_devolucion("L-001")
        servicio.registrar_prestamo("L-001", "Luis Gómez", FUTURA)
        self.assertEqual(
            servicio.prestamos,
            [Prestamo("L-001", "Ana Pérez", FUTURA, False), Prestamo("L-001", "Luis Gómez", FUTURA, True)],
        )
        self.assertEqual(servicio.consultar_catalogo()[0].estado, PRESTADO)

    def test_048_rechazos_no_modifican_datos(self):
        servicio, almacen = crear([L001, L002], [Prestamo("L-001", "Ana Pérez", FUTURA, True)])
        rechazo(self, servicio, almacen, "registrar_devolucion", "no existe", "L-099")
        rechazo(self, servicio, almacen, "registrar_devolucion", "no está prestado", "L-002")
        self.assertEqual(almacen.guardados, 0)

    def test_049_prestamo_activo_desde_registro_hasta_devolucion(self):
        servicio, _ = crear([L001])
        servicio.registrar_prestamo("L-001", "Ana Pérez", FUTURA)
        self.assertTrue(servicio.prestamos[0].activo)
        servicio.consultar_catalogo()
        self.assertTrue(servicio.prestamos[0].activo)
        servicio.registrar_devolucion("L-001")
        self.assertFalse(servicio.prestamos[0].activo)


class PruebaConsultarVencidos(unittest.TestCase):
    """TASK-011: TEST-050 a TEST-056."""

    def ids(self, servicio):
        return [entrada.libro_id for entrada in servicio.consultar_vencidos()]

    def test_050_prestamo_con_fecha_pasada_aparece(self):
        servicio, _ = crear([L001], [Prestamo("L-001", "Ana Pérez", AYER, True)])
        (vencido,) = servicio.consultar_vencidos()
        self.assertEqual(vencido.libro_id, "L-001")
        self.assertEqual(vencido.titulo, "Cien años de soledad")
        self.assertEqual(vencido.estudiante, "Ana Pérez")
        self.assertEqual(vencido.fecha_prevista, AYER)

    def test_051_fecha_de_hoy_no_esta_vencida(self):
        servicio, _ = crear([L001], [Prestamo("L-001", "Ana Pérez", HOY, True)])
        self.assertEqual(servicio.consultar_vencidos(), [])

    def test_052_fecha_futura_no_esta_vencida(self):
        servicio, _ = crear([L001], [Prestamo("L-001", "Ana Pérez", FUTURA, True)])
        self.assertEqual(servicio.consultar_vencidos(), [])

    def test_053_prestamo_devuelto_no_aparece(self):
        servicio, _ = crear([L001], [Prestamo("L-001", "Ana Pérez", PASADA, False)])
        self.assertEqual(servicio.consultar_vencidos(), [])

    def test_054_sin_vencidos_lista_vacia(self):
        sin_prestamos, _ = crear([L001])
        no_vencido, _ = crear([L001], [Prestamo("L-001", "Ana Pérez", FUTURA, True)])
        self.assertEqual(sin_prestamos.consultar_vencidos(), [])
        self.assertEqual(no_vencido.consultar_vencidos(), [])

    def test_055_devuelve_exactamente_los_vencidos(self):
        libros = [L001, L002, L003, ("L-004", "Libro 4", "Autor 4"), ("L-005", "Libro 5", "Autor 5")]
        prestamos = [
            Prestamo("L-001", "Ana Pérez", PASADA, True),
            Prestamo("L-002", "Luis Gómez", AYER, True),
            Prestamo("L-003", "Ana Pérez", HOY, True),
            Prestamo("L-004", "Luis Gómez", FUTURA, True),
            Prestamo("L-005", "Ana Pérez", PASADA, False),
        ]
        servicio, _ = crear(libros, prestamos)
        vencidos = servicio.consultar_vencidos()
        self.assertEqual([v.libro_id for v in vencidos], ["L-001", "L-002"])
        self.assertEqual([(v.estudiante, v.fecha_prevista) for v in vencidos],
                         [("Ana Pérez", PASADA), ("Luis Gómez", AYER)])

    def test_056_consultar_no_modifica_datos(self):
        servicio, almacen = crear([L001], [Prestamo("L-001", "Ana Pérez", AYER, True)])
        antes = instantanea(servicio)
        servicio.consultar_vencidos()
        self.assertEqual(instantanea(servicio), antes)
        self.assertEqual(almacen.guardados, 0)


if __name__ == "__main__":
    unittest.main()
