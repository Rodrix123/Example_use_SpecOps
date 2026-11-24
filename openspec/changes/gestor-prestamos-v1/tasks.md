# Tasks

Fuentes: [`proposal.md`](proposal.md), [`design.md`](design.md) y specs
[`catalogo`](specs/catalogo/spec.md), [`prestamos`](specs/prestamos/spec.md),
[`datos`](specs/datos/spec.md). Este documento solo planifica; no contiene código.


**Convenciones**
- Las pruebas usan `unittest` (biblioteca estándar; design.md exige cero dependencias de terceros).
  TASK-001 fija el comando de pruebas; en adelante se le llama «el comando de pruebas».
- Los casos de prueba de cada tarea se registran como TEST-NNN en `tests/test-plan.md` (fase 6)
  antes de implementar la tarea. Aquí solo se indica qué debe cubrirse.
- Una tarea no está terminada si sus pruebas no se ejecutaron y pasaron.
- Cada tarea modifica solo los archivos de su «Límites de modificación».

## 1. Preparación del proyecto

- [x] 1.1 TASK-001 Crear el paquete `gestor_prestamos` y fijar el comando de pruebas
  - **Objetivo:** Dejar la estructura base en `src/` y una forma única de ejecutar las pruebas.
  - **Requisito asociado:** RS-01, RS-02, RS-03; design Decisiones 1 y 10.
  - **Resultado esperado:** Paquete `src/gestor_prestamos/` con los módulos `modelos`, `servicio`,
    `almacen` y `consola` (vacíos), una prueba de humo en `tests/` y la sección «Pruebas» del
    README con el comando de pruebas.
  - **Criterio de aceptación:** Desde la raíz del proyecto, sin variables de entorno, el comando de
    pruebas ejecuta la prueba de humo (importa los cuatro módulos) y termina con 0 fallos.
  - **Límites de modificación:** `src/gestor_prestamos/*.py`, `tests/test_humo.py`,
    `tests/__init__.py` (solo si hace falta), `README.md` (solo la sección «Pruebas»).

- [x] 1.2 TASK-002 Excluir de Git el archivo de datos
  - **Objetivo:** Que `ops/biblioteca.json` no se versione.
  - **Requisito asociado:** RNF-01; design Decisión 10.
  - **Resultado esperado:** `ops/.gitignore` que excluye `biblioteca.json`. No se crea archivo
    alguno en la raíz (CLAUDE.md §3).
  - **Criterio de aceptación:** `git check-ignore ops/biblioteca.json` imprime la ruta (está
    ignorado) y `ops/.gitignore` aparece en `git status` como archivo por versionar.
  - **Límites de modificación:** `ops/.gitignore`.

## 2. Modelos

- [x] 2.1 TASK-003 Definir `Libro` y `Prestamo`
  - **Objetivo:** Representar los datos del dominio sin lógica ni entrada/salida.
  - **Requisito asociado:** HU-001, HU-003, RN-04; design Decisiones 2 y 3.
  - **Resultado esperado:** `Libro` (identificador, título, autor) y `Prestamo` (identificador del
    libro, estudiante, fecha prevista como fecha, activo). `Libro` no guarda estado: el estado se
    deriva de los préstamos.
  - **Criterio de aceptación:** `tests/test_modelos.py` comprueba que ambos objetos conservan sus
    campos, que `fecha_prevista` es de tipo fecha y que `Libro` no tiene campo de estado; el comando
    de pruebas pasa.
  - **Límites de modificación:** `src/gestor_prestamos/modelos.py`, `tests/test_modelos.py`.

## 3. Almacén

- [x] 3.1 TASK-004 Cargar los datos desde `ops/biblioteca.json`
  - **Objetivo:** Leer libros y préstamos del archivo JSON.
  - **Requisito asociado:** RNF-01; design Decisión 2 y Riesgos (archivo corrupto, ruta).
  - **Resultado esperado:** Función `cargar` que devuelve libros y préstamos como objetos del
    modelo (fechas convertidas de `AAAA-MM-DD`). Si el archivo no existe, devuelve un catálogo
    vacío. Si el JSON no se puede leer, lanza un error de almacén y no modifica el archivo. La ruta
    por defecto se calcula desde la raíz del proyecto, no desde el directorio de ejecución.
  - **Criterio de aceptación:** `tests/test_almacen.py` cubre: archivo inexistente → vacío; archivo
    válido con tildes en título y autor; JSON inválido → error y contenido del archivo sin cambios;
    la ruta por defecto es la misma tras cambiar el directorio de trabajo. El comando de pruebas
    pasa.
  - **Límites de modificación:** `src/gestor_prestamos/almacen.py`, `tests/test_almacen.py`.

- [x] 3.2 TASK-005 Guardar los datos de forma atómica
  - **Objetivo:** Escribir libros y préstamos sin riesgo de dejar el archivo corrupto.
  - **Requisito asociado:** RNF-01, RNF-03; design Decisión 2.
  - **Resultado esperado:** Función `guardar` que escribe UTF-8 sin escapar tildes, con fechas
    `AAAA-MM-DD`, usando un archivo temporal en la misma carpeta y `os.replace`.
  - **Criterio de aceptación:** `tests/test_almacen.py` cubre: `cargar(guardar(x))` devuelve datos
    idénticos (incluidas tildes y préstamos devueltos); el archivo contiene las fechas en formato
    ISO; si `os.replace` falla (simulado), el archivo original queda intacto. El comando de pruebas
    pasa.
  - **Límites de modificación:** `src/gestor_prestamos/almacen.py`, `tests/test_almacen.py`.

## 4. Servicio: reglas de negocio

- [x] 4.1 TASK-006 Base del servicio: error de negocio, almacén y fecha inyectados
  - **Objetivo:** Preparar el servicio para probarse con datos y fecha simulados.
  - **Requisito asociado:** RNF-03; design Decisiones 1, 6 y 7.
  - **Resultado esperado:** Error de negocio que lleva el motivo del rechazo; servicio que recibe el
    almacén y un proveedor de fecha actual (por defecto, la fecha del sistema) y carga los datos al
    crearse. El servicio no lee ni imprime nada.
  - **Criterio de aceptación:** `tests/test_servicio.py` crea el servicio con un almacén simulado y
    una fecha fija, y comprueba que usa esa fecha, que carga los datos del almacén y que el error de
    negocio expone su motivo. El comando de pruebas pasa.
  - **Límites de modificación:** `src/gestor_prestamos/servicio.py`, `tests/test_servicio.py`.

- [x] 4.2 TASK-007 Registrar libro
  - **Objetivo:** Implementar el registro de un libro con sus validaciones.
  - **Requisito asociado:** HU-001, RN-01, RNF-03; CU-001; design Decisión 7.
  - **Resultado esperado:** Operación que valida primero datos completos (vacío tras quitar espacios
    = falta; el motivo indica cuál falta) y luego identificador no repetido (sin distinguir
    mayúsculas, tras quitar espacios). Si es válido, agrega el libro tal como se escribió, queda
    disponible y se guarda una vez. Si se rechaza, no cambia ni guarda nada.
  - **Criterio de aceptación:** `tests/test_servicio.py` cubre: registro completo; falta
    identificador, título o autor (motivo correcto); identificador repetido igual, con distinta
    mayúscula (`l-001` vs `L-001`) y con espacios alrededor; en los rechazos los datos y las
    llamadas a `guardar` no cambian. El comando de pruebas pasa.
  - **Límites de modificación:** `src/gestor_prestamos/servicio.py`, `tests/test_servicio.py`.

- [x] 4.3 TASK-008 Consultar el catálogo con el estado de cada libro
  - **Objetivo:** Devolver todos los libros con su estado derivado de los préstamos.
  - **Requisito asociado:** HU-002; CU-002 (flujo principal); design Decisión 3.
  - **Resultado esperado:** Operación que devuelve, por libro, identificador, título, autor y estado
    (disponible / prestado); para un libro prestado, además el estudiante y la fecha prevista del
    préstamo activo. No modifica datos.
  - **Criterio de aceptación:** `tests/test_servicio.py` cubre: catálogo con varios libros; libro
    prestado (incluye estudiante y fecha); libro devuelto aparece disponible; catálogo vacío devuelve
    una lista vacía. El comando de pruebas pasa.
  - **Límites de modificación:** `src/gestor_prestamos/servicio.py`, `tests/test_servicio.py`.

- [x] 4.4 TASK-009 Registrar préstamo
  - **Objetivo:** Implementar el préstamo de un libro disponible a un estudiante.
  - **Requisito asociado:** HU-003, RN-02, RN-04, RNF-03; CU-003; design Decisiones 3, 5, 6 y 7.
  - **Resultado esperado:** Operación que valida en orden: libro existe (búsqueda sin distinguir
    mayúsculas) → disponible → estudiante indicado (no vacío tras quitar espacios) → fecha válida
    (la fecha llega ya convertida; `None` o anterior a hoy se rechaza; hoy se acepta). Si es válido,
    crea el préstamo activo, el libro pasa a prestado y se guarda una vez. Si se rechaza, no cambia
    ni guarda nada.
  - **Criterio de aceptación:** `tests/test_servicio.py` cubre: préstamo válido (libro prestado,
    préstamo activo); libro inexistente; libro ya prestado (RN-02); estudiante vacío; fecha `None`;
    fecha de ayer rechazada y fecha de hoy aceptada con fecha simulada; id con distinta mayúscula
    encuentra el libro; en los rechazos los datos y `guardar` no cambian. El comando de pruebas pasa.
  - **Límites de modificación:** `src/gestor_prestamos/servicio.py`, `tests/test_servicio.py`.

- [x] 4.5 TASK-010 Registrar devolución
  - **Objetivo:** Implementar la devolución de un libro prestado.
  - **Requisito asociado:** HU-004, RN-04, RN-02, RNF-03; CU-004; design Decisiones 3 y 7.
  - **Resultado esperado:** Operación que valida en orden: libro existe → está prestado. Si es
    válido, el préstamo activo pasa a inactivo (se conserva), el libro queda disponible y se guarda
    una vez. Si se rechaza, no cambia ni guarda nada.
  - **Criterio de aceptación:** `tests/test_servicio.py` cubre: devolución válida (préstamo cerrado y
    conservado, libro disponible); libro inexistente; libro no prestado; tras devolver, el libro
    puede prestarse de nuevo; en los rechazos los datos y `guardar` no cambian. El comando de
    pruebas pasa.
  - **Límites de modificación:** `src/gestor_prestamos/servicio.py`, `tests/test_servicio.py`.

- [x] 4.6 TASK-011 Consultar préstamos vencidos
  - **Objetivo:** Devolver exactamente los préstamos vencidos.
  - **Requisito asociado:** HU-005, RN-03; CU-002 (flujo alternativo 1a); design Decisión 6.
  - **Resultado esperado:** Operación que devuelve los préstamos activos con fecha prevista anterior
    a hoy, con libro (identificador y título), estudiante y fecha prevista. No modifica datos.
  - **Criterio de aceptación:** `tests/test_servicio.py`, con fecha simulada, cubre: préstamo con
    fecha pasada aparece; préstamo con fecha de hoy o futura no aparece; préstamo devuelto con fecha
    pasada no aparece; sin vencidos devuelve una lista vacía; varios vencidos se devuelven todos. El
    comando de pruebas pasa.
  - **Límites de modificación:** `src/gestor_prestamos/servicio.py`, `tests/test_servicio.py`.

## 5. Consola

- [x] 5.1 TASK-012 Convertir fechas `DD/MM/AAAA`
  - **Objetivo:** Traducir la fecha escrita por el bibliotecario a fecha y viceversa.
  - **Requisito asociado:** HU-003; design Decisiones 4 y 5.
  - **Resultado esperado:** Funciones en `consola` que convierten texto `DD/MM/AAAA` a fecha
    (devolviendo `None` si no cumple el formato o no existe en el calendario) y fecha a texto
    `DD/MM/AAAA`. El formato es exacto: dos dígitos de día y mes, cuatro de año.
  - **Criterio de aceptación:** `tests/test_consola.py` cubre: `15/12/2026` válida; `31/02/2026`,
    `2026-12-15`, `5/1/2026`, texto vacío y texto no numérico devuelven `None`; ida y vuelta
    conserva la fecha. El comando de pruebas pasa.
  - **Límites de modificación:** `src/gestor_prestamos/consola.py`, `tests/test_consola.py`.

- [x] 5.2 TASK-013 Menú principal
  - **Objetivo:** Ofrecer el menú numérico y el ciclo de la aplicación.
  - **Requisito asociado:** RNF-02; design Decisión 8.
  - **Resultado esperado:** Menú con una opción numerada por operación (registrar libro, consultar
    catálogo, registrar préstamo, registrar devolución, consultar vencidos) y una para salir. Tras
    cada operación vuelve al menú. Una opción inválida muestra un aviso y vuelve a mostrar el menú.
    La entrada y la salida se pueden inyectar para probar sin teclado.
  - **Criterio de aceptación:** `tests/test_consola.py` con entradas simuladas comprueba: se muestran
    las seis opciones; una opción válida invoca la operación y vuelve al menú; `9`, `abc` y vacío
    muestran aviso sin error; la opción de salir termina el ciclo. El comando de pruebas pasa.
  - **Límites de modificación:** `src/gestor_prestamos/consola.py`, `tests/test_consola.py`.

- [x] 5.3 TASK-014 Opción «Registrar libro»
  - **Objetivo:** Conectar CU-001 con el servicio.
  - **Requisito asociado:** HU-001, RN-01, RNF-03; CU-001.
  - **Resultado esperado:** La opción solicita identificador, título y autor, uno por vez; confirma
    el registro o muestra el motivo del rechazo y vuelve al menú.
  - **Criterio de aceptación:** `tests/test_consola.py` cubre: registro exitoso muestra confirmación
    y el libro aparece en el servicio; falta un dato muestra cuál falta; identificador repetido
    muestra el motivo; en los rechazos los datos no cambian. El comando de pruebas pasa.
  - **Límites de modificación:** `src/gestor_prestamos/consola.py`, `tests/test_consola.py`.

- [x] 5.4 TASK-015 Opción «Consultar catálogo»
  - **Objetivo:** Mostrar el catálogo con el estado de cada libro.
  - **Requisito asociado:** HU-002; CU-002 (flujo principal).
  - **Resultado esperado:** La opción lista cada libro con identificador, título, autor y estado; si
    está prestado, también estudiante y fecha prevista en formato `DD/MM/AAAA`. Con el catálogo
    vacío lo informa.
  - **Criterio de aceptación:** `tests/test_consola.py` cubre: salida con un libro disponible y uno
    prestado (contiene todos los campos y la fecha en `DD/MM/AAAA`); catálogo vacío muestra el aviso.
    El comando de pruebas pasa.
  - **Límites de modificación:** `src/gestor_prestamos/consola.py`, `tests/test_consola.py`.

- [x] 5.5 TASK-016 Opción «Registrar préstamo»
  - **Objetivo:** Conectar CU-003 con el servicio.
  - **Requisito asociado:** HU-003, RN-02, RN-04, RNF-02, RNF-03; CU-003.
  - **Resultado esperado:** La opción solicita identificador del libro, estudiante y fecha prevista
    (`DD/MM/AAAA`), convierte la fecha, llama al servicio y confirma o muestra el motivo del rechazo.
    No pide confirmaciones adicionales.
  - **Criterio de aceptación:** `tests/test_consola.py` cubre: préstamo exitoso con exactamente tres
    entradas consumidas; fecha con formato inválido rechazada con motivo; libro inexistente, libro
    ya prestado y estudiante vacío rechazados con motivo; en los rechazos los datos no cambian. El
    comando de pruebas pasa.
  - **Límites de modificación:** `src/gestor_prestamos/consola.py`, `tests/test_consola.py`.

- [x] 5.6 TASK-017 Opción «Registrar devolución»
  - **Objetivo:** Conectar CU-004 con el servicio.
  - **Requisito asociado:** HU-004, RNF-02, RNF-03; CU-004.
  - **Resultado esperado:** La opción solicita el identificador del libro, llama al servicio y
    confirma o muestra el motivo del rechazo. No pide confirmaciones adicionales.
  - **Criterio de aceptación:** `tests/test_consola.py` cubre: devolución exitosa con exactamente
    una entrada consumida; libro inexistente y libro no prestado rechazados con motivo; en los
    rechazos los datos no cambian. El comando de pruebas pasa.
  - **Límites de modificación:** `src/gestor_prestamos/consola.py`, `tests/test_consola.py`.

- [x] 5.7 TASK-018 Opción «Consultar préstamos vencidos»
  - **Objetivo:** Mostrar los préstamos vencidos.
  - **Requisito asociado:** HU-005, RN-03; CU-002 (flujo alternativo 1a).
  - **Resultado esperado:** La opción lista cada préstamo vencido con libro, estudiante y fecha
    prevista en formato `DD/MM/AAAA`. Si no hay ninguno, lo informa.
  - **Criterio de aceptación:** `tests/test_consola.py`, con fecha simulada, cubre: salida con un
    vencido (contiene libro, estudiante y fecha en `DD/MM/AAAA`); un préstamo devuelto no aparece;
    sin vencidos muestra el aviso. El comando de pruebas pasa.
  - **Límites de modificación:** `src/gestor_prestamos/consola.py`, `tests/test_consola.py`.

- [x] 5.8 TASK-019 Punto de entrada y uso en el README
  - **Objetivo:** Poder iniciar la aplicación completa con un solo comando.
  - **Requisito asociado:** RNF-01, RS-01, RS-03, PER-01; design Decisión 10 y Riesgos.
  - **Resultado esperado:** Punto de entrada que crea el almacén con la ruta por defecto
    (`ops/biblioteca.json`), el servicio con la fecha del sistema y ejecuta el menú. Si el archivo de
    datos no se puede leer, muestra el error y termina con código distinto de 0 sin sobrescribirlo.
    El README documenta el comando de inicio, la ruta de datos, Python 3.12 como mínimo y que
    copiar el archivo sirve de respaldo.
  - **Criterio de aceptación:** `tests/test_entrada.py` comprueba que con un archivo de datos
    corrupto el programa termina con código distinto de 0 y el archivo no cambia. Además, el comando
    documentado en el README, ejecutado desde la raíz y desde otra carpeta, muestra el menú y usa el
    mismo archivo. El comando de pruebas pasa.
  - **Límites de modificación:** `src/gestor_prestamos/__main__.py` (y `consola.py` solo para exponer
    el arranque), `tests/test_entrada.py`, `README.md` (sección de uso).

## 6. Verificación de integración

- [x] 6.1 TASK-020 Verificar persistencia y rechazos de extremo a extremo
  - **Objetivo:** Comprobar sobre un archivo real que los datos sobreviven al reinicio y que un
    rechazo no los altera.
  - **Requisito asociado:** RNF-01, RNF-03.
  - **Resultado esperado:** Pruebas de integración con un archivo temporal que cubren el escenario
    «cerrar y reabrir la aplicación» y los rechazos de HU-001 a HU-004.
  - **Criterio de aceptación:** `tests/test_integracion.py` cubre: registrar libros y un préstamo,
    crear nuevas instancias de almacén y servicio sobre el mismo archivo y obtener datos idénticos;
    tras cada tipo de rechazo (libro repetido, préstamo de libro inexistente, préstamo de libro
    prestado, devolución de libro no prestado) el contenido del archivo es byte a byte el mismo. El
    comando de pruebas pasa.
  - **Límites de modificación:** `tests/test_integracion.py`.

- [ ] 6.2 TASK-021 Verificar el flujo completo por consola
  - **Objetivo:** Comprobar que HU-001 a HU-005 funcionan encadenadas desde el menú.
  - **Requisito asociado:** HU-001, HU-002, HU-003, HU-004, HU-005, RN-02, RN-03.
  - **Resultado esperado:** Una prueba de integración que recorre el menú con entradas simuladas y
    fecha fija.
  - **Criterio de aceptación:** `tests/test_integracion.py` ejecuta: registrar libro → registrar
    préstamo con fecha ya pasada → catálogo muestra prestado → vencidos lo lista → intento de
    segundo préstamo rechazado → devolución → catálogo muestra disponible → vencidos vacío. El
    comando de pruebas pasa.
  - **Límites de modificación:** `tests/test_integracion.py`.

- [ ] 6.3 TASK-022 Verificar RNF-02 con un usuario sin capacitación
  - **Objetivo:** Confirmar que registrar un préstamo o una devolución toma menos de un minuto.
  - **Requisito asociado:** RNF-02.
  - **Resultado esperado:** Registro de la prueba con una persona que no recibió capacitación previa,
    con el tiempo medido de un préstamo y de una devolución.
  - **Criterio de aceptación:** `review/verificacion-rnf-02.md` indica fecha, rol de la persona (sin
    datos personales), tiempo de cada operación y el resultado (cumple si ambos son menores de un
    minuto); el equipo lo revisa.
  - **Límites de modificación:** `review/verificacion-rnf-02.md`.

## Workflow follow-up

- Revisión y entrega (fase 8): registrar los resultados en `review/` tras ejecutar todas las
  pruebas.
- Actualizar la tabla de fases de CLAUDE.md cuando el equipo apruebe la fase.
- Archivar el cambio tras la aprobación del equipo.
