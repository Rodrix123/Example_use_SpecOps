"""Pruebas del punto de entrada (TASK-019; TEST-092).

El punto de entrada siempre usa `ops/biblioteca.json` (design Decisión 10). Según el supuesto S-5
del plan de pruebas, la prueba respalda ese archivo si existe, lo reemplaza por uno corrupto y lo
restaura al terminar.
"""

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ENTRADA = RAIZ / "src" / "gestor_prestamos" / "__main__.py"
DATOS = RAIZ / "ops" / "biblioteca.json"


class PruebaPuntoDeEntrada(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.respaldo = Path(self._tmp.name) / "biblioteca.json"
        self.habia_datos = DATOS.exists()
        if self.habia_datos:
            shutil.copy2(DATOS, self.respaldo)

    def tearDown(self):
        if self.habia_datos:
            shutil.copy2(self.respaldo, DATOS)
        elif DATOS.exists():
            DATOS.unlink()
        self._tmp.cleanup()

    def test_092_archivo_corrupto_termina_con_error_sin_sobrescribir(self):
        DATOS.write_bytes("{ no es json".encode("utf-8"))
        antes = DATOS.read_bytes()
        resultado = subprocess.run(
            [sys.executable, "-B", str(ENTRADA)],
            input="", capture_output=True, text=True, encoding="utf-8", timeout=30,
            cwd=self._tmp.name,
        )
        self.assertNotEqual(resultado.returncode, 0)
        self.assertIn("No se pudo leer el archivo de datos", resultado.stderr)
        self.assertEqual(DATOS.read_bytes(), antes)


if __name__ == "__main__":
    unittest.main()
