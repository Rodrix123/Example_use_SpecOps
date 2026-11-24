"""Pruebas de la consola (TASK-012 a TASK-018; TEST-057 a TEST-091)."""

import unittest
from datetime import date

from gestor_prestamos.consola import ejecutar_menu, fecha_a_texto, texto_a_fecha


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


if __name__ == "__main__":
    unittest.main()
