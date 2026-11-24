# Design

Fuentes: [`proposal.md`](proposal.md), specs [`catalogo`](specs/catalogo/spec.md),
[`prestamos`](specs/prestamos/spec.md) y [`datos`](specs/datos/spec.md).

## Context

Sistema nuevo, sin código previo. Restricciones técnicas vigentes: aplicación de consola en Python,
ejecución local, un único usuario sin autenticación, sin integraciones externas ni red
(RS-01 a RS-04, PER-01). Los specs no fijan almacenamiento, formato de fecha ni qué es una fecha
"válida"; esas decisiones se toman aquí (ver Decisiones 2, 4 y 5). La máquina de desarrollo usa
Windows y Python 3.14.4.

## Goals / Non-Goals

**Goals:**
- Que las reglas RN-01 a RN-04 vivan en un solo lugar, sin depender de la consola ni del archivo,
  para poder probarlas de forma aislada.
- Que una operación rechazada nunca deje datos a medias (RNF-03) y que cada operación aceptada
  quede guardada al terminar (RNF-01).
- Cero dependencias de terceros.

**Non-Goals:**
- Consulta de libros disponibles (CU-002, flujo 1b): ninguna HU ni spec la respalda, por lo que no
  se diseña.
- Control de concurrencia o bloqueo de archivo: el uso simultáneo está excluido (intent §6).
- Versionado o migración del formato del archivo de datos.
- Editar o eliminar libros, buscar, catálogo independiente de estudiantes (product-spec §4).

## Decisions

### 1. Estructura en tres capas con un paquete en `src/`

| Módulo | Responsabilidad |
|---|---|
| `modelos` | Datos de `Libro` y `Prestamo`. |
| `servicio` | Operaciones y reglas de negocio (HU-001 a HU-005, RN-01 a RN-04). Sin entrada/salida. |
| `almacen` | Leer y escribir el archivo JSON. |
| `consola` | Menú, preguntas al usuario y formato de la salida. |

`servicio` recibe el almacén y el proveedor de fecha actual (Decisión 6) en lugar de crearlos, para
poder probarlo con datos y fecha simulados. `consola` es la única capa que imprime o lee del
teclado.
*Alternativa descartada:* un solo script. Mezcla reglas y entrada/salida, y las reglas dejan de
poder probarse sin simular el teclado.

### 2. Almacenamiento en un archivo JSON (RNF-01)

Un archivo `biblioteca.json` en UTF-8 (con `ensure_ascii=False`, porque títulos y autores llevan
tildes), con dos listas:

```json
{
  "libros":    [{"id": "L-001", "titulo": "...", "autor": "..."}],
  "prestamos": [{"libro_id": "L-001", "estudiante": "...",
                 "fecha_prevista": "2026-12-15", "activo": true}]
}
```

- Si el archivo no existe, se parte de un catálogo vacío.
- Se guarda después de cada operación aceptada, no solo al salir; si la aplicación se cierra mal,
  no se pierde lo ya confirmado.
- La escritura es atómica: se escribe un archivo temporal en la misma carpeta y se reemplaza el
  original con `os.replace`. Un fallo a mitad de escritura no deja el archivo corrupto.

*Alternativas descartadas:* SQLite (el motor aplicaría las restricciones, pero el archivo no es
legible y el volumen no lo justifica); CSV (dos archivos que deben mantenerse consistentes entre sí).

### 3. El estado del libro se deriva; no se guarda

Un libro está *prestado* si y solo si tiene un préstamo con `activo: true`; si no, está
*disponible*. Así el estado del catálogo no puede contradecir a los préstamos, y RN-02 se reduce a
una comprobación: "no existe ya un préstamo activo de ese libro".

El préstamo devuelto se conserva con `activo: false` (HU-004 lo "cierra"; HU-005 exige distinguirlo
de los activos). No se guarda fecha de devolución porque ningún requisito la pide.

### 4. Fechas: se escriben y muestran como DD/MM/AAAA; se guardan como AAAA-MM-DD

El bibliotecario ingresa y ve `DD/MM/AAAA`. En el archivo la fecha se guarda en ISO
(`AAAA-MM-DD`), que no es ambigua y se compara sin conversiones. La conversión ocurre solo en
`consola`; `servicio` trabaja con fechas ya convertidas.

### 5. Qué es una fecha prevista "válida" (HU-003)

Una fecha es válida si (a) existe en el calendario, (b) respeta el formato `DD/MM/AAAA` y (c) no es
anterior a la fecha actual. La fecha de hoy se acepta, porque RN-03 solo declara vencido un préstamo
cuya fecha es anterior a hoy.

### 6. La fecha actual se inyecta

`servicio` obtiene "hoy" de un proveedor que por defecto devuelve la fecha del sistema. Las reglas
RN-03 y la validación de la Decisión 5 dependen de la fecha, y sin esa inyección sus pruebas
dependerían del día en que se ejecuten.

### 7. Rechazos y orden de validación (RNF-03)

Toda operación valida primero y modifica después. Un rechazo se señala con un error de negocio que
lleva el motivo; `consola` lo muestra y no se guarda nada. El orden sigue los casos de uso:

- Registrar libro (CU-001 paso 4): datos completos → identificador no repetido.
- Prestar (CU-003 paso 4): libro existe → libro disponible → estudiante indicado → fecha válida.
- Devolver (CU-004 paso 4): libro existe → libro prestado.

Un dato "falta" si queda vacío tras quitar espacios al inicio y al final. El identificador se
compara sin distinguir mayúsculas de minúsculas, tras quitar esos espacios: `L-001` y `l-001` son el
mismo libro (RN-01). Se guarda tal como se escribió, y la misma comparación se usa para buscar el
libro al prestar y al devolver.

### 8. Interfaz: menú numérico interactivo

Un menú con una opción por operación (registrar libro, consultar catálogo, registrar préstamo,
registrar devolución, consultar vencidos) y salir. Cada operación pregunta un dato por vez, como
describen los flujos de CU-001, CU-003 y CU-004 ("el sistema solicita…"), sin confirmaciones
adicionales (RNF-02). Un menú no exige que el bibliotecario recuerde comandos ni argumentos.
*Alternativa descartada:* subcomandos de línea de comandos (`prog prestar …`); exigen conocer la
sintaxis y no encajan con el flujo de preguntas de los CU.

### 9. Trazabilidad de requisitos a decisiones

| Requisito | Decisión |
|---|---|
| HU-001, RN-01 | 1 (`servicio`), 7 |
| HU-002 | 3 (estado derivado), 1 (`consola`) |
| HU-003, RN-02, RN-04 | 3, 5, 6, 7 |
| HU-004 | 3, 7 |
| HU-005, RN-03 | 3, 6 |
| RNF-01 | 2 |
| RNF-02 | 8 |
| RNF-03 | 2 (escritura atómica), 7 |

### 10. Versión de Python y ruta del archivo de datos

- Versión mínima soportada: Python 3.12. Solo se usa la biblioteca estándar.
- El archivo de datos es `ops/biblioteca.json`. La ruta se calcula desde la raíz del proyecto, no
  desde el directorio de ejecución, de modo que ejecutar la aplicación desde otra carpeta no crea un
  catálogo vacío nuevo.
- El archivo se excluye de Git con `ops/.gitignore` (CLAUDE.md §3 no admite otros archivos en la raíz).
- La ruta se documenta en el README.

## Risks / Trade-offs

- **Archivo de datos corrupto o editado a mano** → al iniciar, si el JSON no se puede leer, la
  aplicación muestra el error y termina sin sobrescribirlo, para no perder los datos restantes.
- **Dos instancias abiertas a la vez** → sin bloqueo, la última en guardar gana. Se acepta porque el
  uso simultáneo está fuera del alcance (intent §6).
- **Sin respaldo automático** → el archivo es el único registro. Se acepta en la primera versión;
  copiar el archivo es suficiente para respaldar.
- **Estado derivado** → cada consulta de catálogo recorre los préstamos. Con el volumen de una
  biblioteca pequeña el costo es despreciable.
- **Ruta del archivo relativa al directorio de ejecución** → ejecutar desde otra carpeta crearía un
  catálogo vacío nuevo. Mitigación: la ruta se calcula desde la raíz del proyecto (Decisión 10).

## Open Questions

Ninguna. Se resolvieron al planificar tareas (2026-11-24): mayúsculas en el identificador (Decisión
7), versión mínima de Python y ruta del archivo de datos (Decisión 10).
