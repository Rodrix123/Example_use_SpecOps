"""Lectura y escritura del archivo JSON de datos (TASK-004, TASK-005; RNF-01; design Decisiones 2 y 10).

Formato del archivo (UTF-8; fechas en ISO `AAAA-MM-DD`):

    {"libros":    [{"id": "L-001", "titulo": "...", "autor": "..."}],
     "prestamos": [{"libro_id": "L-001", "estudiante": "...",
                    "fecha_prevista": "2026-12-15", "activo": true}]}
"""

import json
from datetime import date
from pathlib import Path

from gestor_prestamos.modelos import Libro, Prestamo

# src/gestor_prestamos/almacen.py -> raíz del proyecto (design Decisión 10).
_RAIZ_PROYECTO = Path(__file__).resolve().parent.parent.parent


class ErrorAlmacen(Exception):
    """El archivo de datos no se puede leer o escribir."""


def ruta_por_defecto() -> Path:
    """Ruta de `ops/biblioteca.json`, calculada desde la raíz del proyecto y no desde el directorio
    de ejecución (design Decisión 10)."""
    return _RAIZ_PROYECTO / "ops" / "biblioteca.json"


class Almacen:
    """Almacén de libros y préstamos en un archivo JSON."""

    def __init__(self, ruta=None):
        self.ruta = Path(ruta) if ruta is not None else ruta_por_defecto()

    def cargar(self):
        """Devuelve `(libros, prestamos)`.

        Si el archivo no existe, devuelve listas vacías. Si no se puede leer o su contenido no es
        válido, lanza `ErrorAlmacen` sin modificar el archivo.
        """
        if not self.ruta.exists():
            return [], []
        try:
            datos = json.loads(self.ruta.read_text(encoding="utf-8"))
            libros = [
                Libro(item["id"], item["titulo"], item["autor"]) for item in datos["libros"]
            ]
            prestamos = [
                Prestamo(
                    item["libro_id"],
                    item["estudiante"],
                    date.fromisoformat(item["fecha_prevista"]),
                    bool(item["activo"]),
                )
                for item in datos["prestamos"]
            ]
        except (OSError, ValueError, KeyError, TypeError) as error:
            raise ErrorAlmacen(f"No se pudo leer el archivo de datos {self.ruta}: {error}") from error
        return libros, prestamos
