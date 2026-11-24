"""Menú, preguntas al usuario y formato de salida (TASK-012 a TASK-018; design Decisiones 1, 4 y 8).

Es la única capa que lee del teclado o imprime. El bibliotecario escribe y ve las fechas como
`DD/MM/AAAA` (design Decisión 4).
"""

import re
from datetime import date

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
