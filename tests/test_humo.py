"""Prueba de humo del paquete (TEST-001; TASK-001; RS-01, RS-02, RS-03)."""

import importlib
import unittest

MODULOS = ("modelos", "servicio", "almacen", "consola")


class PruebaDeHumo(unittest.TestCase):
    def test_importa_los_cuatro_modulos(self):
        for nombre in MODULOS:
            with self.subTest(modulo=nombre):
                importlib.import_module(f"gestor_prestamos.{nombre}")


if __name__ == "__main__":
    unittest.main()
