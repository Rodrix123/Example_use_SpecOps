"""Punto de entrada de la aplicación (TASK-019; RNF-01, RS-01, RS-03, PER-01; design Decisión 10).

Uso, desde cualquier carpeta: `python <raíz del proyecto>/src/gestor_prestamos/__main__.py`.
Crea el almacén con la ruta por defecto (`ops/biblioteca.json`), el servicio con la fecha del
sistema y ejecuta el menú. Si el archivo de datos no se puede leer, muestra el error y termina con
código 1 sin sobrescribirlo.
"""

import sys
from pathlib import Path

if not __package__:
    # Ejecutado como script: agrega `src/` a la ruta para importar el paquete.
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from gestor_prestamos.consola import iniciar  # noqa: E402

if __name__ == "__main__":
    sys.exit(iniciar())
