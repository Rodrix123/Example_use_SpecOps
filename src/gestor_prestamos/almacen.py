"""Lectura y escritura del archivo JSON de datos (TASK-004, TASK-005; RNF-01; design Decisiones 2 y 10).

Formato del archivo (UTF-8; fechas en ISO `AAAA-MM-DD`):

    {"libros":    [{"id": "L-001", "titulo": "...", "autor": "..."}],
     "prestamos": [{"libro_id": "L-001", "estudiante": "...",
                    "fecha_prevista": "2026-12-15", "activo": true}]}
"""

import json
import os
import tempfile
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

    def guardar(self, libros, prestamos):
        """Escribe libros y préstamos de forma atómica (RNF-01, RNF-03; design Decisión 2).

        Escribe un archivo temporal en la misma carpeta y lo reemplaza con `os.replace`: si algo
        falla, el archivo original queda intacto y se lanza `ErrorAlmacen`.
        """
        datos = {
            "libros": [
                {"id": libro.identificador, "titulo": libro.titulo, "autor": libro.autor}
                for libro in libros
            ],
            "prestamos": [
                {
                    "libro_id": prestamo.libro_id,
                    "estudiante": prestamo.estudiante,
                    "fecha_prevista": prestamo.fecha_prevista.isoformat(),
                    "activo": prestamo.activo,
                }
                for prestamo in prestamos
            ],
        }
        texto = json.dumps(datos, ensure_ascii=False, indent=2)
        temporal = None
        try:
            self.ruta.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(
                "w", encoding="utf-8", dir=self.ruta.parent, suffix=".tmp", delete=False
            ) as archivo:
                temporal = Path(archivo.name)
                archivo.write(texto)
            os.replace(temporal, self.ruta)
        except OSError as error:
            if temporal is not None and temporal.exists():
                temporal.unlink()
            raise ErrorAlmacen(f"No se pudo guardar el archivo de datos {self.ruta}: {error}") from error
