"""Pruebas de la consola (TASK-012 a TASK-018; TEST-057 a TEST-091)."""

import unittest
from datetime import date

from gestor_prestamos.consola import Consola, ejecutar_menu, fecha_a_texto, texto_a_fecha
from gestor_prestamos.modelos import Libro, Prestamo
from gestor_prestamos.servicio import DISPONIBLE, PRESTADO
from tests.test_servicio import AYER, FUTURA, HOY, L001, L002, L003, PASADA, crear

L002_CON_L001 = ("L-001", "El Aleph", "Jorge Luis Borges")


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


class Terminal:
    """Entrada y salida simuladas: entrega las entradas en orden y guarda lo que se escribe."""

    def __init__(self, entradas):
        self.pendientes = list(entradas)
        self.preguntas = []
        self.lineas = []

    def leer(self, pregunta=""):
        self.preguntas.append(pregunta)
        self.lineas.append(pregunta)
        if not self.pendientes:
            raise EOFError
        return self.pendientes.pop(0)

    def escribir(self, texto=""):
        self.lineas.append(texto)

    @property
    def texto(self):
        return "\n".join(self.lineas)


TITULOS_MENU = ("Registrar libro", "Consultar catálogo", "Registrar préstamo",
                "Registrar devolución", "Consultar préstamos vencidos", "Salir")


class PruebaMenu(unittest.TestCase):
    """TASK-013: TEST-065 a TEST-070."""

    def preparar(self, entradas):
        self.llamadas = []
        operaciones = [lambda n=n: self.llamadas.append(n) for n in range(1, 6)]
        terminal = Terminal(entradas)
        ejecutar_menu(operaciones, terminal.leer, terminal.escribir)
        return terminal

    def veces_menu(self, terminal):
        return terminal.lineas.count("6. Salir")

    def test_065_muestra_seis_opciones_numeradas(self):
        terminal = self.preparar(["6"])
        for numero, titulo in enumerate(TITULOS_MENU, start=1):
            self.assertIn(f"{numero}. {titulo}", terminal.lineas)

    def test_066_cada_opcion_invoca_su_operacion(self):
        for opcion in range(1, 6):
            with self.subTest(opcion=opcion):
                terminal = self.preparar([str(opcion), "6"])
                self.assertEqual(self.llamadas, [opcion])
                self.assertEqual(self.veces_menu(terminal), 2)

    def assertAvisoSinOperacion(self, entrada):
        terminal = self.preparar([entrada, "6"])
        self.assertIn("Opción no válida", terminal.texto)
        self.assertEqual(self.llamadas, [])
        self.assertEqual(self.veces_menu(terminal), 2)

    def test_067_opcion_fuera_de_rango(self):
        self.assertAvisoSinOperacion("9")

    def test_068_opcion_no_numerica(self):
        self.assertAvisoSinOperacion("abc")

    def test_069_opcion_vacia(self):
        self.assertAvisoSinOperacion("")

    def test_070_salir_termina_sin_consumir_mas_entradas(self):
        terminal = self.preparar(["6", "1"])
        self.assertEqual(self.llamadas, [])
        self.assertEqual(terminal.pendientes, ["1"])


def ejecutar_consola(entradas, libros=(), prestamos=(), hoy=HOY):
    """Recorre el menú con un servicio real sobre un almacén simulado y fecha fija."""
    servicio, almacen = crear(libros, prestamos, hoy)
    terminal = Terminal(entradas)
    Consola(servicio, terminal.leer, terminal.escribir).ejecutar()
    return terminal, servicio, almacen


def preguntas_de_la_operacion(terminal):
    """Preguntas hechas después de elegir la opción y antes de volver al menú."""
    return [p for p in terminal.preguntas if p != "Elija una opción: "]


class PruebaOpcionRegistrarLibro(unittest.TestCase):
    """TASK-014: TEST-071 a TEST-075."""

    def test_071_registro_con_datos_completos(self):
        terminal, servicio, _ = ejecutar_consola(["1", *L001, "6"])
        self.assertEqual(preguntas_de_la_operacion(terminal), ["Identificador: ", "Título: ", "Autor: "])
        self.assertIn("Libro registrado: L-001", terminal.texto)
        self.assertEqual(servicio.libros, [Libro(*L001)])
        self.assertEqual(servicio.consultar_catalogo()[0].estado, DISPONIBLE)
        self.assertEqual(terminal.lineas.count("6. Salir"), 2)

    def assertFalta(self, entradas, dato):
        terminal, servicio, almacen = ejecutar_consola(["1", *entradas, "6"])
        self.assertIn(f"Falta {dato}", terminal.texto)
        self.assertNotIn("Libro registrado", terminal.texto)
        self.assertEqual(servicio.libros, [])
        self.assertEqual(almacen.guardados, 0)
        self.assertEqual(terminal.lineas.count("6. Salir"), 2)

    def test_072_falta_identificador(self):
        self.assertFalta(["", L001[1], L001[2]], "el identificador")

    def test_073_falta_titulo(self):
        self.assertFalta(["L-001", "", L001[2]], "el título")

    def test_074_falta_autor(self):
        self.assertFalta(["L-001", L001[1], ""], "el autor")

    def test_075_identificador_repetido(self):
        terminal, servicio, almacen = ejecutar_consola(["1", *L002_CON_L001, "6"], libros=[L001])
        self.assertIn("Ya existe un libro con el identificador L-001", terminal.texto)
        self.assertNotIn("Libro registrado", terminal.texto)
        self.assertEqual(servicio.libros, [Libro(*L001)])
        self.assertEqual(almacen.guardados, 0)


def linea_con(terminal, texto):
    """Primera línea de la salida que contiene `texto`."""
    return next(linea for linea in terminal.lineas if texto in linea)


class PruebaOpcionConsultarCatalogo(unittest.TestCase):
    """TASK-015: TEST-076 a TEST-078."""

    def ejecutar(self):
        return ejecutar_consola(["2", "6"], libros=[L001, L002],
                                prestamos=[Prestamo("L-002", "Ana Pérez", FUTURA, True)])[0]

    def test_076_lista_libros_con_su_estado(self):
        terminal = self.ejecutar()
        for datos, estado in ((L001, "disponible"), (L002, "prestado")):
            linea = linea_con(terminal, datos[0])
            for valor in (*datos, estado):
                self.assertIn(valor, linea)

    def test_077_libro_prestado_muestra_estudiante_y_fecha(self):
        terminal = self.ejecutar()
        l002 = linea_con(terminal, "L-002")
        self.assertIn("Ana Pérez", l002)
        self.assertIn("15/12/2026", l002)
        self.assertNotIn("2026-12-15", terminal.texto)
        l001 = linea_con(terminal, "L-001")
        self.assertNotIn("Ana Pérez", l001)
        self.assertNotIn("/", l001)

    def test_078_catalogo_vacio(self):
        terminal, _, _ = ejecutar_consola(["2", "6"])
        self.assertIn("No hay libros registrados.", terminal.lineas)


class PruebaOpcionRegistrarPrestamo(unittest.TestCase):
    """TASK-016: TEST-079 a TEST-084."""

    def assertRechazado(self, entradas, motivo, libros=(L001,), prestamos=()):
        terminal, servicio, almacen = ejecutar_consola(["3", *entradas, "6"], libros, prestamos)
        self.assertIn(motivo, terminal.texto)
        self.assertNotIn("Préstamo registrado", terminal.texto)
        self.assertEqual(almacen.guardados, 0)
        self.assertEqual(servicio.prestamos, list(prestamos))
        self.assertEqual(terminal.lineas.count("6. Salir"), 2)
        return servicio

    def test_079_prestamo_de_libro_disponible(self):
        terminal, servicio, _ = ejecutar_consola(["3", "L-001", "Ana Pérez", "15/12/2026", "6"], [L001])
        self.assertEqual(len(preguntas_de_la_operacion(terminal)), 3)
        self.assertIn("Préstamo registrado", terminal.texto)
        self.assertEqual(servicio.prestamos, [Prestamo("L-001", "Ana Pérez", FUTURA, True)])
        self.assertEqual(servicio.consultar_catalogo()[0].estado, PRESTADO)
        self.assertEqual(terminal.lineas.count("6. Salir"), 2)

    def test_080_fecha_con_formato_invalido(self):
        self.assertRechazado(["L-001", "Ana Pérez", "2026-12-15"], "no es válida")

    def test_081_falta_el_estudiante(self):
        self.assertRechazado(["L-001", "", "15/12/2026"], "Falta el estudiante")

    def test_082_libro_inexistente(self):
        self.assertRechazado(["L-099", "Ana Pérez", "15/12/2026"], "No existe un libro")

    def test_083_libro_ya_prestado(self):
        activo = Prestamo("L-001", "Ana Pérez", FUTURA, True)
        servicio = self.assertRechazado(["L-001", "Luis Gómez", "20/12/2026"], "ya está prestado",
                                        prestamos=[activo])
        self.assertEqual([p for p in servicio.prestamos if p.activo], [activo])

    def test_084_fecha_anterior_a_hoy_o_inexistente(self):
        for fecha, motivo in (("30/11/2026", "anterior a hoy"), ("31/02/2026", "no es válida")):
            with self.subTest(fecha=fecha):
                self.assertRechazado(["L-001", "Ana Pérez", fecha], motivo)


if __name__ == "__main__":
    unittest.main()
