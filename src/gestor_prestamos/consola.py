"""Menú, preguntas al usuario y formato de salida (TASK-012 a TASK-018; design Decisiones 1, 4 y 8).

Es la única capa que lee del teclado o imprime. El bibliotecario escribe y ve las fechas como
`DD/MM/AAAA` (design Decisión 4).
"""

import re
from datetime import date

from gestor_prestamos.almacen import ErrorAlmacen
from gestor_prestamos.servicio import ErrorNegocio

_FORMATO_FECHA = re.compile(r"(\d{2})/(\d{2})/(\d{4})")


def texto_a_fecha(texto):
    """Convierte `DD/MM/AAAA` (dos dígitos de día y mes, cuatro de año) a fecha.

    Devuelve `None` si el texto no cumple el formato o la fecha no existe en el calendario.
    """
    coincidencia = _FORMATO_FECHA.fullmatch(texto or "")
    if coincidencia is None:
        return None
    dia, mes, anio = (int(parte) for parte in coincidencia.groups())
    try:
        return date(anio, mes, dia)
    except ValueError:
        return None


def fecha_a_texto(fecha: date) -> str:
    """Convierte una fecha a `DD/MM/AAAA`."""
    return f"{fecha.day:02d}/{fecha.month:02d}/{fecha.year:04d}"


# --- Menú principal (TASK-013; RNF-02; design Decisión 8) ----------------------------------------

OPCIONES = (
    "Registrar libro",
    "Consultar catálogo",
    "Registrar préstamo",
    "Registrar devolución",
    "Consultar préstamos vencidos",
)
SALIR = str(len(OPCIONES) + 1)


def ejecutar_menu(operaciones, leer=input, escribir=print):
    """Muestra el menú numerado y ejecuta la operación elegida hasta que se elige salir.

    `operaciones` son cinco funciones sin argumentos, en el orden de `OPCIONES`. `leer` y `escribir`
    se inyectan para poder probar sin teclado. Si la entrada se agota, el ciclo termina.
    """
    while True:
        escribir("")
        for numero, titulo in enumerate(OPCIONES, start=1):
            escribir(f"{numero}. {titulo}")
        escribir(f"{SALIR}. Salir")
        try:
            opcion = leer("Elija una opción: ").strip()
        except EOFError:
            return
        if opcion == SALIR:
            return
        if opcion.isdigit() and 1 <= int(opcion) <= len(operaciones):
            operaciones[int(opcion) - 1]()
        else:
            escribir(f"Opción no válida. Escriba un número del 1 al {SALIR}.")


# --- Opciones del menú (TASK-014 a TASK-018) ------------------------------------------------------


class Consola:
    """Conecta los casos de uso con el servicio: pregunta un dato por vez y muestra el resultado
    o el motivo del rechazo, sin confirmaciones adicionales (RNF-02, RNF-03)."""

    def __init__(self, servicio, leer=input, escribir=print):
        self.servicio = servicio
        self.leer = leer
        self.escribir = escribir

    def ejecutar(self):
        """Ciclo del menú principal."""
        operaciones = [
            self.registrar_libro,
            self.consultar_catalogo,
            self._pendiente,
            self._pendiente,
            self._pendiente,
        ]
        ejecutar_menu(operaciones, self.leer, self.escribir)

    def _pendiente(self):
        self.escribir("Opción no disponible todavía.")

    def _intentar(self, operacion, accion):
        """Ejecuta `operacion`; si el servicio la rechaza o no puede guardar, muestra el motivo."""
        try:
            return operacion()
        except ErrorNegocio as error:
            self.escribir(f"No se pudo {accion}: {error.motivo}")
        except ErrorAlmacen as error:
            self.escribir(f"No se pudo {accion}: {error}")
        return None

    def registrar_libro(self):
        """CU-001: solicita identificador, título y autor (HU-001, RN-01)."""
        identificador = self.leer("Identificador: ")
        titulo = self.leer("Título: ")
        autor = self.leer("Autor: ")
        libro = self._intentar(
            lambda: self.servicio.registrar_libro(identificador, titulo, autor), "registrar el libro"
        )
        if libro is not None:
            self.escribir(f"Libro registrado: {libro.identificador} - {libro.titulo}.")

    def consultar_catalogo(self):
        """CU-002, flujo principal: lista los libros con su estado (HU-002)."""
        catalogo = self.servicio.consultar_catalogo()
        if not catalogo:
            self.escribir("No hay libros registrados.")
            return
        for entrada in catalogo:
            linea = f"{entrada.identificador} | {entrada.titulo} | {entrada.autor} | {entrada.estado}"
            if entrada.estudiante is not None:
                linea += f" | {entrada.estudiante} | {fecha_a_texto(entrada.fecha_prevista)}"
            self.escribir(linea)
