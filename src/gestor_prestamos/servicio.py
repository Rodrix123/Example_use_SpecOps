"""Operaciones y reglas de negocio (TASK-006 a TASK-011; design Decisiones 1, 3, 5, 6 y 7).

El servicio no lee del teclado ni imprime: recibe el almacén y el proveedor de la fecha actual,
valida primero y modifica después. Un rechazo se señala con `ErrorNegocio`, que lleva el motivo
(RNF-03).
"""

from dataclasses import dataclass
from datetime import date

from gestor_prestamos.modelos import Libro

DISPONIBLE = "disponible"
PRESTADO = "prestado"


@dataclass(frozen=True)
class EntradaCatalogo:
    """Un libro del catálogo con su estado; estudiante y fecha solo si está prestado (HU-002)."""

    identificador: str
    titulo: str
    autor: str
    estado: str
    estudiante: str | None = None
    fecha_prevista: date | None = None


class ErrorNegocio(Exception):
    """Rechazo de una operación por una regla de negocio; `motivo` explica la causa."""

    def __init__(self, motivo: str):
        super().__init__(motivo)
        self.motivo = motivo


class Servicio:
    """Catálogo y préstamos en memoria, guardados en el almacén tras cada operación aceptada."""

    def __init__(self, almacen, hoy=date.today):
        self._almacen = almacen
        self._hoy = hoy
        self.libros, self.prestamos = almacen.cargar()

    def hoy(self) -> date:
        """Fecha actual según el proveedor inyectado (design Decisión 6)."""
        return self._hoy()

    # --- Apoyo -------------------------------------------------------------------------------

    def _buscar_libro(self, identificador):
        """Libro cuyo identificador coincide sin distinguir mayúsculas ni espacios al inicio y al
        final (design Decisión 7), o `None`."""
        clave = _clave(identificador)
        for libro in self.libros:
            if _clave(libro.identificador) == clave:
                return libro
        return None

    def _prestamo_activo(self, libro):
        """Préstamo activo del libro, o `None`: el libro está prestado si y solo si lo tiene."""
        for prestamo in self.prestamos:
            if prestamo.activo and _clave(prestamo.libro_id) == _clave(libro.identificador):
                return prestamo
        return None

    def _guardar(self, libros, prestamos):
        """Guarda y, solo si el guardado tuvo éxito, reemplaza los datos en memoria."""
        self._almacen.guardar(libros, prestamos)
        self.libros, self.prestamos = libros, prestamos

    # --- Operaciones ---------------------------------------------------------------------------

    def registrar_libro(self, identificador, titulo, autor):
        """Registra un libro disponible (HU-001, RN-01; CU-001).

        Valida primero que los tres datos estén completos y luego que el identificador no exista.
        El libro se guarda tal como se escribió.
        """
        for valor, nombre in ((identificador, "el identificador"), (titulo, "el título"), (autor, "el autor")):
            if _falta(valor):
                raise ErrorNegocio(f"Falta {nombre}.")
        if self._buscar_libro(identificador) is not None:
            raise ErrorNegocio(f"Ya existe un libro con el identificador {identificador.strip()}.")
        libro = Libro(identificador, titulo, autor)
        self._guardar(self.libros + [libro], list(self.prestamos))
        return libro

    def consultar_catalogo(self):
        """Todos los libros con su estado derivado de los préstamos (HU-002; CU-002; design
        Decisión 3). No modifica datos."""
        entradas = []
        for libro in self.libros:
            activo = self._prestamo_activo(libro)
            entradas.append(
                EntradaCatalogo(
                    identificador=libro.identificador,
                    titulo=libro.titulo,
                    autor=libro.autor,
                    estado=PRESTADO if activo else DISPONIBLE,
                    estudiante=activo.estudiante if activo else None,
                    fecha_prevista=activo.fecha_prevista if activo else None,
                )
            )
        return entradas


def _falta(valor) -> bool:
    """Un dato falta si queda vacío tras quitar espacios al inicio y al final (design Decisión 7)."""
    return valor is None or not str(valor).strip()


def _clave(identificador) -> str:
    """Forma de comparar identificadores: sin espacios alrededor y sin distinguir mayúsculas."""
    return str(identificador).strip().casefold()
