"""Operaciones y reglas de negocio (TASK-006 a TASK-011; design Decisiones 1, 3, 5, 6 y 7).

El servicio no lee del teclado ni imprime: recibe el almacén y el proveedor de la fecha actual,
valida primero y modifica después. Un rechazo se señala con `ErrorNegocio`, que lleva el motivo
(RNF-03).
"""

from datetime import date


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
