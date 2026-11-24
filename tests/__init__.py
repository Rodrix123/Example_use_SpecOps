"""Paquete de pruebas (TASK-001; RS-02).

Agrega `src/` a la ruta de importación para que las pruebas encuentren `gestor_prestamos`
sin variables de entorno. Se ejecuta al descubrir las pruebas con `-t .` desde la raíz.
"""

import sys
from pathlib import Path

_SRC = str(Path(__file__).resolve().parent.parent / "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)
